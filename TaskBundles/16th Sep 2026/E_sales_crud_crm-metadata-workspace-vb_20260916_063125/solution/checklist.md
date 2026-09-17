# Checklist: Thirty

Source: instruction.md
Sections present: overview, user roles, core features, user flow, ui and ux notes, technical requirements, data model, front-end specification, constraints, deployment contract
Sections absent: build plan
Items: 328
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public marketing site at the root address. `src: Overview para 2`
- [ ] `C-OV-02` `capability` The app serves a signed-in workspace whose schema is stored as data. `src: Overview para 1`
- [ ] `C-OV-03` `capability` The app grows a rail entry for a newly created object. `src: Overview para 1`
- [ ] `C-OV-04` `capability` The app renders every marketing product picture from a live platform component. `src: Overview para 2`
- [ ] `C-OV-05` `constraint` The app contacts no external mail vendor at runtime. `src: Overview para 4`
- [ ] `C-OV-06` `constraint` The app contacts no external identity provider at runtime. `src: Overview para 4`
- [ ] `C-OV-07` `constraint` The app contacts no external language model at runtime. `src: Overview para 4`
- [ ] `C-OV-08` `capability` The app names every dependent of a schema change before the change lands. `src: Overview para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` An owner reads billing. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An owner changes the plan tier. `src: User roles table row 1`
- [ ] `C-RL-03` `constraint` An owner exempts no actor from an audit entry. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An admin reads every record regardless of a row rule. `src: User roles table row 2`
- [ ] `C-RL-05` `role` An admin creates an object. `src: User roles table row 2`
- [ ] `C-RL-06` `role` An admin creates a permission rule. `src: User roles table row 2`
- [ ] `C-RL-07` `constraint` An admin changes no plan tier. `src: User roles table row 2`
- [ ] `C-RL-08` `constraint` An admin deletes no audit entry. `src: User roles table row 2`
- [ ] `C-RL-09` `role` A member reads only the records a permission rule admits. `src: User roles table row 3`
- [ ] `C-RL-10` `constraint` A member creates no object. `src: User roles table row 3`
- [ ] `C-RL-11` `constraint` A member creates no permission rule. `src: User roles table row 3`
- [ ] `C-RL-12` `constraint` A member reads no key. `src: User roles table row 3`
- [ ] `C-RL-13` `constraint` A member reads no other member's private view. `src: User roles table row 3`
- [ ] `C-RL-14` `constraint` A member reaching an admin settings address is refused by the server. `src: User roles, authorization para`
- [ ] `C-RL-15` `constraint` A direct call from a member session to an admin-only endpoint leaves the protected state unchanged. `src: User roles, authorization para`
- [ ] `C-RL-16` `role` A custom role is built from grants taken per object. `src: User roles, custom role para`
- [ ] `C-RL-17` `constraint` A custom role grants no more than the administrator who built one holds. `src: User roles, custom role para`
- [ ] `C-RL-18` `data` The app attributes a row created by a key to the key's own actor identity. `src: User roles, actors para`
- [ ] `C-RL-19` `data` The app attributes a row created by a workflow to the workflow's own actor identity. `src: User roles, actors para`
- [ ] `C-RL-20` `data` The app attributes a row created by an installed app to the app's own actor identity. `src: User roles, actors para`
- [ ] `C-RL-21` `constraint` The app exposes no public registration form. `src: User roles, signup para`
- [ ] `C-RL-22` `literal` The app seeds an owner account at `owner@example.com`. `src: User roles, seeded accounts table`
- [ ] `C-RL-23` `literal` The app seeds an admin account at `admin@example.com`. `src: User roles, seeded accounts table`
- [ ] `C-RL-24` `literal` The app seeds a member account at `member@example.com`. `src: User roles, seeded accounts table`
- [ ] `C-RL-25` `literal` The app seeds a second member account at `member2@example.com`. `src: User roles, seeded accounts table`
- [ ] `C-RL-26` `data` The app gives the first seeded member ownership of five seeded companies. `src: User roles, seeded accounts table`
- [ ] `C-RL-27` `data` The app gives the second seeded member ownership of four seeded companies. `src: User roles, seeded accounts table`

## C-CF Core features

- [ ] `C-CF-01` `capability` The app returns a bearer token on a sign-in with a correct password. `src: Core features, Auth, rule 1`
- [ ] `C-CF-02` `constraint` The app denies a sign-in with a wrong password. `src: Core features, Auth, rule 1`
- [ ] `C-CF-03` `constraint` The app reveals no account existence in a denied sign-in response. `src: Core features, Auth, rule 1`
- [ ] `C-CF-04` `capability` The app asks for a second-factor code when an account has enrolled one. `src: Core features, Auth, rule 2`
- [ ] `C-CF-05` `constraint` The app issues no session for a wrong second-factor code. `src: Core features, Auth, rule 2`
- [ ] `C-CF-06` `constraint` The app writes no membership row for a request without an invitation. `src: Core features, Auth, rule 3`
- [ ] `C-CF-07` `capability` The app refuses a removed member on the next request within a second. `src: Core features, Auth, rule 4`
- [ ] `C-CF-08` `constraint` The app acts on no stored single sign-on configuration. `src: Core features, Auth, rule 5`
- [ ] `C-CF-09` `literal` The app renders the header chips `55.9K` for the repository count. `src: Core features, marketing site, rule 1`
- [ ] `C-CF-10` `literal` The app renders the header chip `7.2K` for the community count. `src: Core features, marketing site, rule 1`
- [ ] `C-CF-11` `ui` The app keeps the marketing header at the top of the page during a scroll. `src: Core features, marketing site, rule 1`
- [ ] `C-CF-12` `ui` The app folds the header centre links into a menu sheet at a narrow width. `src: Core features, marketing site, rule 1`
- [ ] `C-CF-13` `literal` The app renders the footer copyright line `(C) 2026 - Thirty`. `src: Core features, marketing site, rule 2`
- [ ] `C-CF-14` `ui` The app renders four footer columns on every marketing page. `src: Core features, marketing site, rule 2`
- [ ] `C-CF-15` `capability` The app links a terms page from the footer of every page. `src: Core features, marketing site, rule 3`
- [ ] `C-CF-16` `capability` The app links a terms page from the invitation acceptance form. `src: Core features, marketing site, rule 3`
- [ ] `C-CF-17` `capability` The app states on the privacy page how long an archived row is kept before a purge. `src: Core features, marketing site, rule 3`
- [ ] `C-CF-18` `ui` The app renders the eight landing bands in the stated order. `src: Core features, marketing site, rule 4`
- [ ] `C-CF-19` `literal` The app renders the landing headline `Build your Enterprise CRM at AI Speed`. `src: Core features, marketing site, rule 5`
- [ ] `C-CF-20` `literal` The app renders the logo-bar tail `+10k others`. `src: Core features, marketing site, rule 6`
- [ ] `C-CF-21` `ui` The app names the two tradeoffs in the Problem band. `src: Core features, marketing site, rule 7`
- [ ] `C-CF-22` `ui` The app renders three numbered steps in the Solution band triptych. `src: Core features, marketing site, rule 8`
- [ ] `C-CF-23` `ui` The app renders three mock plates in the go-to-market band. `src: Core features, marketing site, rule 9`
- [ ] `C-CF-24` `ui` The app renders three case tiles in the in-production band. `src: Core features, marketing site, rule 10`
- [ ] `C-CF-25` `ui` The app renders a pager showing the current quotation position out of three. `src: Core features, marketing site, rule 11`
- [ ] `C-CF-26` `ui` The app opens one FAQ disclosure row at a time. `src: Core features, marketing site, rule 12`
- [ ] `C-CF-27` `literal` The app names the scaffold command `npx create-thirty-app` in an FAQ answer. `src: Core features, marketing site, rule 12`
- [ ] `C-CF-28` `ui` The app renders the fast-workspace trio on the product page. `src: Core features, marketing site, rule 13`
- [ ] `C-CF-29` `capability` The app draws the product page schema graph from the metadata store. `src: Core features, marketing site, rule 14`
- [ ] `C-CF-30` `capability` The app adds a newly created object to the product page schema graph. `src: Core features, marketing site, rule 14`
- [ ] `C-CF-31` `ui` The app renders metric pairs on the customers index cards. `src: Core features, marketing site, rule 15`
- [ ] `C-CF-32` `ui` The app opens four case pages from the customers index. `src: Core features, marketing site, rule 16`
- [ ] `C-CF-33` `ui` The app renders a region chip on every partner card. `src: Core features, marketing site, rule 17`
- [ ] `C-CF-34` `literal` The app renders four marketplace filter chips reading `All`, `Enrichment`, `Productivity`, `Search`. `src: Core features, marketing site, rule 18`
- [ ] `C-CF-35` `ui` The app renders dated entries on the releases page. `src: Core features, marketing site, rule 19`
- [ ] `C-CF-36` `ui` The app renders the positioning essay in a narrow reading column. `src: Core features, marketing site, rule 20`
- [ ] `C-CF-37` `ui` The app renders the product's own not-found copy line for an unmatched address. `src: Core features, marketing site, rule 21`
- [ ] `C-CF-38` `capability` The app answers an unmatched address as not found. `src: Core features, marketing site, rule 21`
- [ ] `C-CF-39` `capability` The app resolves every internal link on every public page. `src: Core features, marketing site, rule 22`
- [ ] `C-CF-40` `capability` The app renders the hero companies table from the real table view component. `src: Core features, live mocks, rule 1`
- [ ] `C-CF-41` `literal` The app renders the hero view bar label `All Companies - 9`. `src: Core features, live mocks, rule 1`
- [ ] `C-CF-42` `data` The app seeds nine companies with the stated figures. `src: Core features, live mocks, rule 2`
- [ ] `C-CF-43` `data` The app seeds a created-by actor named for a key in the companies fixture. `src: Core features, live mocks, rule 3`
- [ ] `C-CF-44` `literal` The app renders the board header counts `All opportunities 9`, `Identified 3`, `Qualified 1`. `src: Core features, live mocks, rule 4`
- [ ] `C-CF-45` `literal` The app renders the filtered-table chips `Type is Customer`, `Employees > 500`. `src: Core features, live mocks, rule 5`
- [ ] `C-CF-46` `literal` The app lists the palette action `Export selection as CSV` in the record selection group. `src: Core features, live mocks, rule 6`
- [ ] `C-CF-47` `literal` The app lists the palette chord `G then P` against a go-to-People action. `src: Core features, live mocks, rule 6`
- [ ] `C-CF-48` `capability` The app replays the AI build session as a scripted fixture. `src: Core features, live mocks, rule 7`
- [ ] `C-CF-49` `ui` The app arms each marketing mock when a reader scrolls one into view. `src: Core features, live mocks, rule 9`
- [ ] `C-CF-50` `ui` The app renders every marketing mock in a finished state under a reduced-motion preference. `src: Core features, live mocks, rule 9`
- [ ] `C-CF-51` `literal` The app renders the halftone header line `Idle auto-rotate is active`. `src: Core features, halftone, rule 1`
- [ ] `C-CF-52` `literal` The app renders three halftone control tabs reading `Design`, `Animations`, `Export`. `src: Core features, halftone, rule 2`
- [ ] `C-CF-53` `capability` The app offers fourteen named primitive sources in the halftone source control. `src: Core features, halftone, rule 2`
- [ ] `C-CF-54` `capability` The app updates the halftone render during a control movement. `src: Core features, halftone, rule 3`
- [ ] `C-CF-55` `capability` The app downloads a rendered still from the halftone export tab. `src: Core features, halftone, rule 4`
- [ ] `C-CF-56` `capability` The app produces every site halftone plate at build time. `src: Core features, halftone, rule 6`
- [ ] `C-CF-57` `literal` The app prices the `Pro` plan at `$9` per user per month. `src: Core features, pricing, rule 2`
- [ ] `C-CF-58` `literal` The app prices the `Organization` plan at `$19` per user per month. `src: Core features, pricing, rule 2`
- [ ] `C-CF-59` `literal` The app prices the `Enterprise` plan from `$50k` per year. `src: Core features, pricing, rule 2`
- [ ] `C-CF-60` `capability` The app reprices every plan card by one stored yearly saving on a toggle to Yearly. `src: Core features, pricing, rule 3`
- [ ] `C-CF-61` `ui` The app opens one comparison matrix group at a time. `src: Core features, pricing, rule 5`
- [ ] `C-CF-62` `constraint` The app denies a row rule creation request on a Pro workspace. `src: Core features, pricing, rule 6`
- [ ] `C-CF-63` `constraint` The app writes no row rule for a denied Pro workspace request. `src: Core features, pricing, rule 6`
- [ ] `C-CF-64` `capability` The app offers two-factor enrolment on every plan tier. `src: Core features, pricing, rule 7`
- [ ] `C-CF-65` `capability` The app raises the seat count when an administrator invites a member. `src: Core features, pricing, rule 8`
- [ ] `C-CF-66` `capability` The app retains an above-plan row rule as an inert stored rule after a downgrade. `src: Core features, pricing, rule 9`
- [ ] `C-CF-67` `capability` The app restores an inert row rule to effect when the plan returns. `src: Core features, pricing, rule 9`
- [ ] `C-CF-68` `ui` The app renders a Favorites group in the workspace rail. `src: Core features, shell, rule 1`
- [ ] `C-CF-69` `capability` The app changes the rail for every signed-in member within a second of an object rename. `src: Core features, shell, rule 2`
- [ ] `C-CF-70` `ui` The app renders the view bar record count beside the view name. `src: Core features, shell, rule 3`
- [ ] `C-CF-71` `ui` The app hosts a record preview in the right side panel. `src: Core features, shell, rule 4`
- [ ] `C-CF-72` `capability` The app gives a newly created object a table view with no further step. `src: Core features, metadata engine, rule 1`
- [ ] `C-CF-73` `capability` The app gives a newly created object an addressable resource with no further step. `src: Core features, metadata engine, rule 1`
- [ ] `C-CF-74` `capability` The app offers at least fourteen field types. `src: Core features, metadata engine, rule 2`
- [ ] `C-CF-75` `capability` The app makes a new relation navigable from both paired sides. `src: Core features, metadata engine, rule 3`
- [ ] `C-CF-76` `capability` The app archives both sides of a relation together. `src: Core features, metadata engine, rule 3`
- [ ] `C-CF-77` `capability` The app preserves every stored value through a field rename. `src: Core features, metadata engine, rule 4`
- [ ] `C-CF-78` `constraint` The app refuses a field type change that would lose a value. `src: Core features, metadata engine, rule 5`
- [ ] `C-CF-79` `capability` The app reports the count of rows blocking a refused field type change. `src: Core features, metadata engine, rule 5`
- [ ] `C-CF-80` `constraint` The app changes no value when a field type change is refused. `src: Core features, metadata engine, rule 5`
- [ ] `C-CF-81` `capability` The app keeps a deleted object restorable for thirty days. `src: Core features, metadata engine, rule 6`
- [ ] `C-CF-82` `capability` The app lists every dependent view of a schema change before the change lands. `src: Core features, metadata engine, rule 7`
- [ ] `C-CF-83` `capability` The app lists every dependent workflow trigger of a schema change before the change lands. `src: Core features, metadata engine, rule 7`
- [ ] `C-CF-84` `capability` The app lists every dependent permission rule of a schema change before the change lands. `src: Core features, metadata engine, rule 7`
- [ ] `C-CF-85` `constraint` The app leaves no view pointing at a field that no longer exists. `src: Core features, metadata engine, rule 7`
- [ ] `C-CF-86` `capability` The app accepts exactly one of two simultaneous saves to one piece of metadata. `src: Core features, metadata engine, rule 8`
- [ ] `C-CF-87` `capability` The app tells the losing metadata writer the stored version was stale. `src: Core features, metadata engine, rule 8`
- [ ] `C-CF-88` `capability` The app applies a schema change in place for a member holding an open view. `src: Core features, metadata engine, rule 9`
- [ ] `C-CF-89` `data` The app ships the seven starter objects as seeded metadata rows. `src: Core features, metadata engine, rule 10`
- [ ] `C-CF-90` `ui` The app keeps the table header row in place during a body scroll. `src: Core features, table view, rule 1`
- [ ] `C-CF-91` `ui` The app renders a boolean cell as a mark paired with a word. `src: Core features, table view, rule 2`
- [ ] `C-CF-92` `ui` The app right-aligns a currency cell with thousands separators. `src: Core features, table view, rule 2`
- [ ] `C-CF-93` `capability` The app commits a cell edit on Enter. `src: Core features, table view, rule 3`
- [ ] `C-CF-94` `capability` The app abandons a cell edit on Escape. `src: Core features, table view, rule 3`
- [ ] `C-CF-95` `constraint` The app refuses a non-numeric value at a currency cell before any storage. `src: Core features, table view, rule 3`
- [ ] `C-CF-96` `capability` The app returns the committed cell value after a page reload. `src: Core features, table view, rule 4`
- [ ] `C-CF-97` `capability` The app returns the committed cell value through the keyed interface. `src: Core features, table view, rule 4`
- [ ] `C-CF-98` `capability` The app scrolls ten thousand rows with the header in place. `src: Core features, table view, rule 5`
- [ ] `C-CF-99` `capability` The app persists a per-person column pin across a sign-out. `src: Core features, table view, rule 6`
- [ ] `C-CF-100` `capability` The app records a bulk field edit as one undoable act. `src: Core features, table view, rule 7`
- [ ] `C-CF-101` `capability` The app restores hidden rows when a reader removes a filter chip. `src: Core features, table view, rule 8`
- [ ] `C-CF-102` `capability` The app keeps the caret in place when a remote edit lands on another cell of the same row. `src: Core features, table view, rule 9`
- [ ] `C-CF-103` `capability` The app stores the later of two commits to one cell. `src: Core features, table view, rule 9`
- [ ] `C-CF-104` `capability` The app tells the earlier writer the value was replaced. `src: Core features, table view, rule 9`
- [ ] `C-CF-105` `ui` The app renders a created-by cell for a workflow actor as a workflow chip. `src: Core features, table view, rule 10`
- [ ] `C-CF-106` `capability` The app groups any object carrying a single-select field into lanes. `src: Core features, kanban, rule 1`
- [ ] `C-CF-107` `literal` The app renders a record code in the style of `OPP-1` on a board card. `src: Core features, kanban, rule 2`
- [ ] `C-CF-108` `capability` The app writes the grouped field when a card is dragged into another lane. `src: Core features, kanban, rule 3`
- [ ] `C-CF-109` `capability` The app recounts the source lane total as a dragged card lands. `src: Core features, kanban, rule 3`
- [ ] `C-CF-110` `capability` The app recounts the destination lane total as a dragged card lands. `src: Core features, kanban, rule 3`
- [ ] `C-CF-111` `capability` The app re-dates a record when a calendar entry is dragged to another day. `src: Core features, kanban, rule 5`
- [ ] `C-CF-112` `constraint` The app hides a private view from every other member. `src: Core features, kanban, rule 6`
- [ ] `C-CF-113` `capability` The app pins a favourited view to the rail for one person only. `src: Core features, kanban, rule 7`
- [ ] `C-CF-114` `ui` The app renders relation sections as chips carrying a detach control. `src: Core features, record page, rule 1`
- [ ] `C-CF-115` `ui` The app renders a timeline entry with an actor. `src: Core features, record page, rule 2`
- [ ] `C-CF-116` `capability` The app derives the record timeline from the same event stream the audit trail reads. `src: Core features, record page, rule 3`
- [ ] `C-CF-117` `capability` The app shows a field edit on another person's open record page within a second. `src: Core features, record page, rule 4`
- [ ] `C-CF-118` `capability` The app opens the palette from a keyboard shortcut anywhere in the workspace. `src: Core features, palette, rule 1`
- [ ] `C-CF-119` `constraint` The app fires no navigation chord during typing in a text input. `src: Core features, palette, rule 2`
- [ ] `C-CF-120` `capability` The app offers a date operator reading in future. `src: Core features, palette, rule 3`
- [ ] `C-CF-121` `capability` The app saves a built filter into a view. `src: Core features, palette, rule 3`
- [ ] `C-CF-122` `capability` The app groups full-text search results per object. `src: Core features, palette, rule 4`
- [ ] `C-CF-123` `constraint` The app returns no permission-hidden row in a search result. `src: Core features, palette, rule 5`
- [ ] `C-CF-124` `constraint` The app counts no permission-hidden row in a readable result count. `src: Core features, palette, rule 5`
- [ ] `C-CF-125` `capability` The app offers a schedule trigger node. `src: Core features, workflows, rule 1`
- [ ] `C-CF-126` `capability` The app offers an outbound web request action node carrying a signed payload. `src: Core features, workflows, rule 1`
- [ ] `C-CF-127` `capability` The app records each workflow node input in the run history. `src: Core features, workflows, rule 2`
- [ ] `C-CF-128` `capability` The app records each workflow node outcome in the run history. `src: Core features, workflows, rule 2`
- [ ] `C-CF-129` `capability` The app marks a run failed when a node fails. `src: Core features, workflows, rule 2`
- [ ] `C-CF-130` `capability` The app starts exactly one run per workflow per triggering event. `src: Core features, workflows, rule 3`
- [ ] `C-CF-131` `capability` The app halts a self-triggering workflow chain at a depth limit. `src: Core features, workflows, rule 4`
- [ ] `C-CF-132` `capability` The app writes a halt entry naming why a workflow chain stopped. `src: Core features, workflows, rule 4`
- [ ] `C-CF-133` `capability` The app finishes an in-flight run on the version the run started on. `src: Core features, workflows, rule 5`
- [ ] `C-CF-134` `capability` The app refuses a run attempted past the plan credit allowance. `src: Core features, workflows, rule 6`
- [ ] `C-CF-135` `literal` The app prefixes a workflow message subject with `Workflow:` followed by the workflow name. `src: Core features, workflows, rule 7`
- [ ] `C-CF-136` `constraint` The app sends a workflow message with no carbon copy. `src: Core features, workflows, rule 7`
- [ ] `C-CF-137` `constraint` The app sends a workflow message with no blind carbon copy. `src: Core features, workflows, rule 7`
- [ ] `C-CF-138` `capability` The app names the acted-on record in a workflow message body. `src: Core features, workflows, rule 7`
- [ ] `C-CF-139` `constraint` The app sends no message for a run refused at the credit gate. `src: Core features, workflows, rule 8`
- [ ] `C-CF-140` `constraint` The app sends no message for a run halted by the depth limit. `src: Core features, workflows, rule 8`
- [ ] `C-CF-141` `capability` The app binds rows of an object to a row owner through a permission rule. `src: Core features, permissions, rule 1`
- [ ] `C-CF-142` `capability` The app answers every read path from one permission authority. `src: Core features, permissions, rule 2`
- [ ] `C-CF-143` `capability` The app answers a request for a permission-hidden row as not found. `src: Core features, permissions, rule 3`
- [ ] `C-CF-144` `constraint` The app answers a request for a permission-hidden row as something other than forbidden. `src: Core features, permissions, rule 3`
- [ ] `C-CF-145` `capability` The app computes an aggregate after row filtering. `src: Core features, permissions, rule 4`
- [ ] `C-CF-146` `constraint` The app moves no visible lane total by a permission-hidden row. `src: Core features, permissions, rule 4`
- [ ] `C-CF-147` `capability` The app reconciles a readable total with the rows one member can list. `src: Core features, permissions, rule 4`
- [ ] `C-CF-148` `constraint` The app returns no masked field in a keyed interface response. `src: Core features, permissions, rule 6`
- [ ] `C-CF-149` `constraint` The app returns no masked field in an export file. `src: Core features, permissions, rule 6`
- [ ] `C-CF-150` `capability` The app records a sign-in in the audit trail. `src: Core features, permissions, rule 7`
- [ ] `C-CF-151` `capability` The app records an export in the audit trail. `src: Core features, permissions, rule 7`
- [ ] `C-CF-152` `capability` The app records the value before a record mutation in the audit trail. `src: Core features, permissions, rule 7`
- [ ] `C-CF-153` `constraint` The app deletes no audit entry. `src: Core features, permissions, rule 7`
- [ ] `C-CF-154` `capability` The app filters the audit trail by actor. `src: Core features, permissions, rule 7`
- [ ] `C-CF-155` `capability` The app names the records a chat answer read. `src: Core features, AI surfaces, rule 1`
- [ ] `C-CF-156` `capability` The app refuses a chat question the workspace records cannot answer. `src: Core features, AI surfaces, rule 1`
- [ ] `C-CF-157` `constraint` The app cites no permission-hidden row in a chat answer. `src: Core features, AI surfaces, rule 2`
- [ ] `C-CF-158` `capability` The app marks every scaffolded object as a draft for review. `src: Core features, AI surfaces, rule 3`
- [ ] `C-CF-159` `capability` The app gives an installed app an actor identity of the app's own. `src: Core features, AI surfaces, rule 4`
- [ ] `C-CF-160` `capability` The app archives an uninstalled app's contributions reversibly. `src: Core features, AI surfaces, rule 5`
- [ ] `C-CF-161` `capability` The app previews the landing type of each mapped import column. `src: Core features, import, rule 1`
- [ ] `C-CF-162` `capability` The app flags an import row that would fail with a reason. `src: Core features, import, rule 1`
- [ ] `C-CF-163` `capability` The app offers a duplicate strategy of update on a matched key. `src: Core features, import, rule 2`
- [ ] `C-CF-164` `constraint` The app writes nothing during an import dry run. `src: Core features, import, rule 3`
- [ ] `C-CF-165` `capability` The app removes exactly the rows a committed import created when the batch is undone. `src: Core features, import, rule 4`
- [ ] `C-CF-166` `capability` The app records one audit entry per committed import batch. `src: Core features, import, rule 4`
- [ ] `C-CF-167` `capability` The app completes an import of fifty thousand rows with visible progress. `src: Core features, import, rule 5`
- [ ] `C-CF-168` `constraint` The app adds no hidden row to an exported view file. `src: Core features, import, rule 6`
- [ ] `C-CF-169` `capability` The app shows a key secret once at creation. `src: Core features, import, rule 7`
- [ ] `C-CF-170` `capability` The app refuses a revoked key on the next request. `src: Core features, import, rule 7`
- [ ] `C-CF-171` `capability` The app addresses every object through the keyed interface from the moment of creation. `src: Core features, import, rule 8`
- [ ] `C-CF-172` `capability` The app signs every webhook delivery. `src: Core features, import, rule 9`
- [ ] `C-CF-173` `capability` The app records a webhook retry as a retry. `src: Core features, import, rule 9`
- [ ] `C-CF-174` `capability` The app renders a dashboard widget grid over any object. `src: Core features, dashboards, rule 1`
- [ ] `C-CF-175` `capability` The app rearranges dashboard widgets by dragging. `src: Core features, dashboards, rule 2`
- [ ] `C-CF-176` `capability` The app computes every dashboard widget number after row filtering. `src: Core features, dashboards, rule 3`

## C-UF User flow

- [ ] `C-UF-01` `contract` The app serves a landing page at the root address. `src: User flow, route table row 1`
- [ ] `C-UF-02` `contract` The app serves the positioning essay at `/why-thirty`. `src: User flow, route table`
- [ ] `C-UF-03` `contract` The app serves the halftone tool at `/halftone`. `src: User flow, route table`
- [ ] `C-UF-04` `contract` The app serves the terms page at `/terms`. `src: User flow, route table`
- [ ] `C-UF-05` `contract` The app serves the privacy page at `/privacy-policy`. `src: User flow, route table`
- [ ] `C-UF-06` `contract` The app requires a session for every address under `/workspace`. `src: User flow, route table`
- [ ] `C-UF-07` `contract` The app requires an admin role for the data model studio address. `src: User flow, route table`
- [ ] `C-UF-08` `capability` The app sends an unauthenticated request for a workspace address to the sign-in page. `src: User flow, entry and redirects`
- [ ] `C-UF-09` `capability` The app returns a person to the requested workspace address after a successful sign-in. `src: User flow, entry and redirects`
- [ ] `C-UF-10` `capability` The app stops the old token working immediately on sign-out. `src: User flow, entry and redirects`
- [ ] `C-UF-11` `capability` The app leaves a record unchanged when a token expires part way through an edit. `src: User flow, entry and redirects`
- [ ] `C-UF-12` `ui` The app names what would fill an empty list in every empty state. `src: User flow, states`
- [ ] `C-UF-13` `ui` The app renders a skeleton of rows as the table loading state. `src: User flow, states`
- [ ] `C-UF-14` `ui` The app renders an error in place with a way back. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The app carries meaning on one near-black neutral at several strengths. `src: UI/UX notes, colour para`
- [ ] `C-UX-02` `ui` The app uses one light vivid blue as the only brand hue in the chrome. `src: UI/UX notes, colour para`
- [ ] `C-UX-03` `ui` The app reserves four accent colours for meaning alone. `src: UI/UX notes, colour para`
- [ ] `C-UX-04` `ui` The app sets display headlines in one serif face used nowhere else. `src: UI/UX notes, type para`
- [ ] `C-UX-05` `ui` The app sets navigation labels in an uppercase letterspaced mono face. `src: UI/UX notes, type para`
- [ ] `C-UX-06` `ui` The app gives every control a resting appearance. `src: UI/UX notes, components para`
- [ ] `C-UX-07` `ui` The app gives every control an unavailable appearance signalled by more than colour. `src: UI/UX notes, components para`
- [ ] `C-UX-08` `ui` The app leads every page with exactly one primary action. `src: UI/UX notes, primary action para`
- [ ] `C-UX-09` `ui` The app shares one eased motion character across every transition. `src: UI/UX notes, motion para`
- [ ] `C-UX-10` `ui` The app renders every scene finished under a reduced-motion preference. `src: UI/UX notes, motion para`
- [ ] `C-UX-11` `constraint` The app meets WCAG AA contrast for body text against the background. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-12` `constraint` The app reaches every control by keyboard navigation with a visible focus ring. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-13` `ui` The app overflows nothing sideways at any viewport width. `src: UI/UX notes, responsive para`
- [ ] `C-UX-14` `ui` The app collapses the workspace rail to icons at tablet width. `src: UI/UX notes, responsive para`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app serves the marketing pages with real markup in the first response. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The app builds the server with FastAPI. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The app builds the interface with SolidStart. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` The app reads the database address from `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` The app reads the mail host from `SMTP_HOST`. `src: Technical requirements para 1`
- [ ] `C-TR-06` `contract` The app sends mail to Mailpit over real SMTP. `src: Technical requirements para 1`
- [ ] `C-TR-07` `contract` The app stores data in PostgreSQL. `src: Technical requirements para 1`
- [ ] `C-TR-08` `constraint` The app introduces no second database. `src: Technical requirements para 2`
- [ ] `C-TR-09` `contract` The app returns `200` from `GET /api/health` once ready. `src: Technical requirements para 3`
- [ ] `C-TR-10` `constraint` The app writes no record value into a log line. `src: Technical requirements, logging para`
- [ ] `C-TR-11` `constraint` The app serves no credential in anything the browser downloads. `src: Technical requirements, secrets para`
- [ ] `C-TR-12` `contract` The app gives every public route a document title of the route's own. `src: Technical requirements, meta para`
- [ ] `C-TR-13` `contract` The app gives every public route a description of the route's own. `src: Technical requirements, meta para`
- [ ] `C-TR-14` `contract` The app declares a social preview title on every public route. `src: Technical requirements, meta para`
- [ ] `C-TR-15` `contract` The app serves the social preview image the public routes declare. `src: Technical requirements, meta para`
- [ ] `C-TR-16` `capability` The app renders every object through one view engine. `src: Technical requirements, architecture para`
- [ ] `C-TR-17` `capability` The app delivers a missed change in order to a reconnecting client. `src: Technical requirements, liveness list`
- [ ] `C-TR-18` `capability` The app completes a permission-filtered read of a thousand rows within 1.5 times an unfiltered read. `src: Technical requirements, liveness list`
- [ ] `C-TR-19` `capability` The app opens the seeded workspace interactively within two seconds. `src: Technical requirements, liveness list`
- [ ] `C-TR-20` `capability` The app loads the halftone rendering engine only on the halftone route. `src: Technical requirements, liveness list`
- [ ] `C-TR-21` `capability` The app accepts exactly one of two simultaneous metadata saves. `src: Technical requirements, concurrency para`
- [ ] `C-TR-22` `capability` The app creates no second run when one triggering event is observed twice. `src: Technical requirements, concurrency para`

## C-DM Data model

- [ ] `C-DM-01` `data` The app stores every timestamp in UTC. `src: Data model, opening line`
- [ ] `C-DM-02` `literal` The app accepts the password `deku-demo-pw-2026` at login for every seeded account. `src: Data model, seeded password para`
- [ ] `C-DM-03` `contract` The app writes each seeded account into `/app/USER_README.md`. `src: Data model, seeded password para`
- [ ] `C-DM-04` `data` The app keeps one workspace row per deployment. `src: Data model, workspace entity`
- [ ] `C-DM-05` `data` The app carries the owner role on exactly one membership. `src: Data model, membership entity`
- [ ] `C-DM-06` `data` The app keeps an object label unique across active objects. `src: Data model, object metadata entity`
- [ ] `C-DM-07` `data` The app purges an archived object after thirty days. `src: Data model, object metadata entity`
- [ ] `C-DM-08` `data` The app keeps a field name unique within the field's object. `src: Data model, field metadata entity`
- [ ] `C-DM-09` `data` The app keeps both sides of a relation present together. `src: Data model, relation metadata entity`
- [ ] `C-DM-10` `data` The app refuses a second record write of a value on a field marked unique. `src: Data model, record entity`
- [ ] `C-DM-11` `data` The app updates no event row after creation. `src: Data model, event entity`
- [ ] `C-DM-12` `data` The app pins the workflow version on a run for the run's whole life. `src: Data model, workflow entity`
- [ ] `C-DM-13` `data` The app marks a permission rule inert when the plan does not admit one. `src: Data model, permission rule entity`
- [ ] `C-DM-14` `data` The app stores no key secret in readable form. `src: Data model, key entity`
- [ ] `C-DM-15` `data` The app stores money in integer minor units. `src: Data model, money para`
- [ ] `C-DM-16` `data` The app returns the same integer money value through every read path. `src: Data model, money para`
- [ ] `C-DM-17` `data` The app seeds one dashboard named Sales Dashboard. `src: Data model, seed data para`
- [ ] `C-DM-18` `data` The app seeds one permission rule binding a company row to the account owner. `src: Data model, seed data para`
- [ ] `C-DM-19` `data` The app duplicates no row when the process restarts. `src: Data model, seed data para`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The app names the ground colour token `--surface`. `src: Front-end specification, design tokens`
- [ ] `C-FE-02` `ui` The app names the single brand hue token `--color-blue`. `src: Front-end specification, design tokens`
- [ ] `C-FE-03` `ui` The app names nine grey ladder tokens from chalk down to charcoal. `src: Front-end specification, design tokens`
- [ ] `C-FE-04` `ui` The app reserves the grey ladder for mock surfaces, never for text. `src: Front-end specification, design tokens`
- [ ] `C-FE-05` `ui` The app names four accent tokens for the four meanings. `src: Front-end specification, design tokens`
- [ ] `C-FE-06` `ui` The app moves marketing mocks by shifting rather than by redrawing. `src: Front-end specification, motion`
- [ ] `C-FE-07` `ui` The app plays each marketing band choreography once. `src: Front-end specification, motion`
- [ ] `C-FE-08` `constraint` The app ships no binary asset. `src: Front-end specification, drawn asset system`
- [ ] `C-FE-09` `ui` The app draws every fixture company logo as a monogram tile. `src: Front-end specification, drawn asset system`
- [ ] `C-FE-10` `ui` The app draws every person avatar as a circle carrying seeded initials. `src: Front-end specification, drawn asset system`
- [ ] `C-FE-11` `ui` The app renders the trusted-by bar as ten desaturated text wordmarks. `src: Front-end specification, drawn asset system`
- [ ] `C-FE-12` `ui` The app wraps every product demonstration in a drawn window chrome carrying three dots. `src: Front-end specification, shared furniture`
- [ ] `C-FE-13` `ui` The app renders a key sequence in the mono face at the right edge of a palette row. `src: Front-end specification, command palette`
- [ ] `C-FE-14` `ui` The app renders the AI side panel as a translucent surface over the work behind one. `src: Front-end specification, AI side panel`
- [ ] `C-FE-15` `ui` The app moves focus into an overlay when one opens. `src: Front-end specification, announcements and focus`
- [ ] `C-FE-16` `ui` The app returns focus to the opener when an overlay closes. `src: Front-end specification, announcements and focus`
- [ ] `C-FE-17` `ui` The app announces a row edited by somebody else. `src: Front-end specification, announcements and focus`
- [ ] `C-FE-18` `ui` The app offers a menu equivalent for every drag operation. `src: Front-end specification, responsive behaviour`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app serves one workspace per deployment. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The app reads across no second workspace. `src: Constraints bullet 1`
- [ ] `C-CN-03` `constraint` The app takes no card. `src: Constraints bullet 5`
- [ ] `C-CN-04` `constraint` The app issues no invoice. `src: Constraints bullet 5`
- [ ] `C-CN-05` `constraint` The app generates no chat answer from anything outside the workspace records. `src: Constraints bullet 6`
- [ ] `C-CN-06` `constraint` The app ships no font file. `src: Constraints bullet 7`
- [ ] `C-CN-07` `constraint` The app offers no direct messaging between members. `src: Constraints bullet 9`
- [ ] `C-CN-08` `constraint` The app shares no record publicly outside the workspace. `src: Constraints bullet 9`
- [ ] `C-CN-09` `constraint` The app stays responsive with ten thousand records in one view. `src: Constraints bullet 10`
- [ ] `C-CN-10` `constraint` The app calls no external service at runtime. `src: Constraints bullet 3`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The app listens on container-internal port `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The app reads the outside port from `APP_PUBLIC_PORT`. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The app serves the HTTP API under the `/api` prefix on the same origin. `src: Deployment contract bullet 2`
- [ ] `C-DC-05` `contract` The app answers `GET /api/health` with `200` once ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual step. `src: Deployment contract bullet 4`
- [ ] `C-DC-07` `contract` The app writes login credentials to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-08` `contract` The app leaves a `.browser_screenshots/` directory empty at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `contract` The app leaves a `.downloads/` directory empty at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-10` `contract` The app serves a production build behind a static or preview server. `src: Deployment contract bullet 7`
- [ ] `C-DC-11` `contract` The app keeps the server running after the build session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-12` `contract` The app binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-13` `constraint` The app starts no copy of a named backing service. `src: Deployment contract bullet 10`
- [ ] `C-DC-14` `constraint` The app uses no persistent volume. `src: Deployment contract bullet 12`
- [ ] `C-DC-15` `contract` The app returns a top-level JSON array from a list endpoint. `src: Deployment contract, API shapes`
- [ ] `C-DC-16` `contract` The app requires a bearer token on every endpoint except login, health, webhook receivers. `src: Deployment contract, API shapes`
- [ ] `C-DC-17` `contract` The app rejects a rule-breaking request as a client error carrying a reason. `src: Deployment contract, API shapes`
- [ ] `C-DC-18` `constraint` The app returns no server error for a rule-breaking request. `src: Deployment contract, API shapes`
- [ ] `C-DC-19` `constraint` The app stores no record outside PostgreSQL. `src: Deployment contract, no mocks`
- [ ] `C-DC-20` `constraint` The app records no message as sent without handing one to the mail server. `src: Deployment contract, no mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `owner@example.com` | seeded owner address | C-RL-22 | User roles, seeded accounts table |
| `admin@example.com` | seeded admin address | C-RL-23 | User roles, seeded accounts table |
| `member@example.com` | seeded first member address | C-RL-24 | User roles, seeded accounts table |
| `member2@example.com` | seeded second member address | C-RL-25 | User roles, seeded accounts table |
| `55.9K` | repository count chip | C-CF-09 | Core features, marketing site rule 1 |
| `7.2K` | community count chip | C-CF-10 | Core features, marketing site rule 1 |
| `(C) 2026 - Thirty` | footer copyright line | C-CF-13 | Core features, marketing site rule 2 |
| `Build your Enterprise CRM at AI Speed` | landing headline | C-CF-19 | Core features, marketing site rule 5 |
| `+10k others` | logo bar tail | C-CF-20 | Core features, marketing site rule 6 |
| `npx create-thirty-app` | scaffold command in an FAQ answer | C-CF-27 | Core features, marketing site rule 12 |
| `All` | first marketplace filter chip | C-CF-34 | Core features, marketing site rule 18 |
| `Enrichment` | second marketplace filter chip | C-CF-34 | Core features, marketing site rule 18 |
| `Productivity` | third marketplace filter chip | C-CF-34 | Core features, marketing site rule 18 |
| `Search` | fourth marketplace filter chip | C-CF-34 | Core features, marketing site rule 18 |
| `All Companies - 9` | hero view bar label | C-CF-41 | Core features, live mocks rule 1 |
| `All opportunities 9` | board header total | C-CF-44 | Core features, live mocks rule 4 |
| `Identified 3` | board header lane count | C-CF-44 | Core features, live mocks rule 4 |
| `Qualified 1` | board header lane count | C-CF-44 | Core features, live mocks rule 4 |
| `Type is Customer` | filtered table chip | C-CF-45 | Core features, live mocks rule 5 |
| `Employees > 500` | filtered table chip | C-CF-45 | Core features, live mocks rule 5 |
| `Export selection as CSV` | palette action row | C-CF-46 | Core features, live mocks rule 6 |
| `G then P` | palette navigation chord | C-CF-47 | Core features, live mocks rule 6 |
| `Idle auto-rotate is active` | halftone header line | C-CF-51 | Core features, halftone rule 1 |
| `Design` | first halftone control tab | C-CF-52 | Core features, halftone rule 2 |
| `Animations` | second halftone control tab | C-CF-52 | Core features, halftone rule 2 |
| `Export` | third halftone control tab | C-CF-52 | Core features, halftone rule 2 |
| `Pro` | first plan name | C-CF-57 | Core features, pricing rule 2 |
| `$9` | Pro price per user per month | C-CF-57 | Core features, pricing rule 2 |
| `Organization` | second plan name | C-CF-58 | Core features, pricing rule 2 |
| `$19` | Organization price per user per month | C-CF-58 | Core features, pricing rule 2 |
| `Enterprise` | third plan name | C-CF-59 | Core features, pricing rule 2 |
| `$50k` | Enterprise floor price per year | C-CF-59 | Core features, pricing rule 2 |
| `OPP-1` | board card record code | C-CF-107 | Core features, kanban rule 2 |
| `Workflow:` | workflow message subject prefix | C-CF-135 | Core features, workflows rule 7 |
| `deku-demo-pw-2026` | password for every seeded account | C-DM-02 | Data model, seeded password para |
| `404: This page could not be found.` | not-found copy line | C-CF-37 | Core features, marketing site rule 21 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the four case page addresses | C-CF-30 | named as four cases with no slug given for any one |
| the seeded workflow name behind the message subject | C-CF-119 | the prefix is pinned, the seeded name is named only in the seed paragraph |
| the ten trusted-by wordmark names | C-FE-11 | a count is given with no name for any one |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 4 | 8 |
| User roles | 3 | 27 |
| Core features | 38 | 176 |
| User flow | 8 | 14 |
| UI/UX notes | 4 | 14 |
| Technical requirements | 8 | 22 |
| Data model | 8 | 19 |
| Front-end specification | 5 | 18 |
| Constraints | 1 | 10 |
| Deployment contract | 13 | 20 |
