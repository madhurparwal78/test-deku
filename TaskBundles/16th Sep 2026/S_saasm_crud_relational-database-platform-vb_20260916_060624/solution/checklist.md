# Checklist: Relational Database Platform

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, deployment
Sections absent: buildplan
Items: 236
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The product holds workspaces that each hold bases. `src: Overview para 1`
- [ ] `C-OV-02` `capability` A base holds tables of records. `src: Overview para 1`
- [ ] `C-OV-03` `capability` A view is a live query over one table rather than a saved copy. `src: Overview para 1`
- [ ] `C-OV-04` `capability` Computed fields resolve through a dependency graph across tables. `src: Overview para 2`
- [ ] `C-OV-05` `capability` An append-only operation log sits beneath every write. `src: Overview para 2`
- [ ] `C-OV-06` `capability` Record history is derived from the operation log. `src: Overview para 2`
- [ ] `C-OV-07` `constraint` The product accepts no uploaded file. `src: Overview para 3`
- [ ] `C-OV-08` `constraint` The product sends no notification of any kind. `src: Overview para 3`
- [ ] `C-OV-09` `constraint` The product carries no comment on any record. `src: Overview para 3`

## C-RL User roles

- [ ] `C-RL-01` `role` An owner grants membership in the workspace of that owner. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An owner changes the role held by a member. `src: User roles table row 1`
- [ ] `C-RL-03` `role` An owner creates a base. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An owner creates a guard. `src: User roles table row 1`
- [ ] `C-RL-05` `role` An owner locks a view. `src: User roles table row 1`
- [ ] `C-RL-06` `role` A creator creates a table. `src: User roles table row 2`
- [ ] `C-RL-07` `role` A creator changes the type of a field. `src: User roles table row 2`
- [ ] `C-RL-08` `role` A creator is denied granting membership. `src: User roles table row 2`
- [ ] `C-RL-09` `role` A creator is denied creating a guard. `src: User roles table row 2`
- [ ] `C-RL-10` `role` An editor changes a cell value. `src: User roles table row 3`
- [ ] `C-RL-11` `role` An editor is denied creating a field. `src: User roles table row 3`
- [ ] `C-RL-12` `role` An editor creates a collaborative view. `src: User roles table row 3`
- [ ] `C-RL-13` `role` A commenter is denied changing any cell value. `src: User roles table row 4`
- [ ] `C-RL-14` `role` A commenter configures a personal view. `src: User roles table row 4`
- [ ] `C-RL-15` `role` A reader writes nothing anywhere in the workspace. `src: User roles table row 5`
- [ ] `C-RL-16` `contract` The server enforces authorization on every mutating endpoint. `src: User roles para 2`
- [ ] `C-RL-17` `role` The more permissive of the two grant paths decides the effective role. `src: User roles para 3`
- [ ] `C-RL-18` `role` A base grant never lowers a member below the inherited workspace role. `src: User roles para 3`
- [ ] `C-RL-19` `role` A member holding no grant reaches nothing in the workspace. `src: User roles para 3`
- [ ] `C-RL-20` `contract` Signup is open to a new account. `src: User roles para 4`
- [ ] `C-RL-21` `role` A new account holds no membership until one is granted. `src: User roles para 4`
- [ ] `C-RL-22` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles para 4`

## C-CF Core features

- [ ] `C-CF-01` `capability` A record is created through the records endpoint. `src: Core features records rule 1`
- [ ] `C-CF-02` `capability` A cell value is changed through the record endpoint. `src: Core features records rule 1`
- [ ] `C-CF-03` `capability` A record is removed through the record endpoint. `src: Core features records rule 1`
- [ ] `C-CF-04` `data` The records endpoint returns a top-level JSON array. `src: Core features records rule 1`
- [ ] `C-CF-05` `data` A returned record carries the current value of every computed field on that row. `src: Core features records rule 1`
- [ ] `C-CF-06` `data` A cell written through the grid re-reads identically after a reload. `src: Core features records rule 2`
- [ ] `C-CF-07` `data` The value shown by the interface equals the value returned by the record endpoint. `src: Core features records rule 2`
- [ ] `C-CF-08` `data` Deleting a record removes both sides of every link naming that record. `src: Core features records rule 3`
- [ ] `C-CF-09` `constraint` A base holds at most 50000 records. `src: Core features records rule 4`
- [ ] `C-CF-10` `data` No two records in one table carry the same auto number. `src: Core features records rule 5`
- [ ] `C-CF-11` `data` A field name of 200 characters breaks no layout. `src: Core features records rule 6`
- [ ] `C-CF-12` `contract` Login returns a bearer token. `src: Core features Auth`
- [ ] `C-CF-13` `contract` An expired token reads as not signed in. `src: Core features Auth`
- [ ] `C-CF-14` `contract` A password is stored hashed. `src: Core features Auth`
- [ ] `C-CF-15` `contract` A plaintext password is returned in no response. `src: Core features Auth`
- [ ] `C-CF-16` `data` The workspaces endpoint returns only the workspaces the caller holds a grant in. `src: Core features workspaces rule 1`
- [ ] `C-CF-17` `constraint` A workspace holds at most 1000 bases. `src: Core features workspaces rule 3`
- [ ] `C-CF-18` `constraint` A base holds at most 100 tables. `src: Core features workspaces rule 3`
- [ ] `C-CF-19` `role` A creator is denied creating a base. `src: Core features workspaces rule 4`
- [ ] `C-CF-20` `data` A request naming a base in a workspace the caller has no grant in answers as though no such base exists. `src: Core features workspaces rule 5`
- [ ] `C-CF-21` `literal` An object identifier carries exactly `17` characters. `src: Core features Identifiers`
- [ ] `C-CF-22` `literal` A record identifier begins with the prefix `rec`. `src: Core features Identifiers`
- [ ] `C-CF-23` `data` An object identifier is never reused once issued. `src: Core features Identifiers`
- [ ] `C-CF-24` `constraint` A table holds at most 500 fields. `src: Core features fields rule 1`
- [ ] `C-CF-25` `data` A field name is unique within the table of that field. `src: Core features fields rule 1`
- [ ] `C-CF-26` `data` The primary field of a table is never a computed type. `src: Core features fields rule 2`
- [ ] `C-CF-27` `data` Every table carries at least one grid view. `src: Core features fields rule 3`
- [ ] `C-CF-28` `data` The field-types endpoint returns all nineteen field types. `src: Core features fields rule 4`
- [ ] `C-CF-29` `data` A select choice carries a colour name drawn from a palette of ten. `src: Core features fields rule 5`
- [ ] `C-CF-30` `data` A computed field refuses a written value. `src: Core features fields rule 6`
- [ ] `C-CF-31` `data` Precision changes what a number displays rather than what a number stores. `src: Core features fields rule 7`
- [ ] `C-CF-32` `literal` A duration of ninety minutes stores `5400`. `src: Core features fields rule 8`
- [ ] `C-CF-33` `data` A date-and-time field resolves against the timezone configured on that field. `src: Core features fields rule 9`
- [ ] `C-CF-34` `data` A link field displays a linked record by the primary field of the linked table. `src: Core features links rule 1`
- [ ] `C-CF-35` `data` Creating a link writes the mirrored reference under the inverse field. `src: Core features links rule 2`
- [ ] `C-CF-36` `data` The single-link preference restricts the picker rather than the store. `src: Core features links rule 3`
- [ ] `C-CF-37` `data` A lookup traverses exactly one hop. `src: Core features links rule 5`
- [ ] `C-CF-38` `data` An invalid lookup configuration blanks every cell of that field. `src: Core features links rule 7`
- [ ] `C-CF-39` `data` A rollup offers all sixteen aggregations. `src: Core features links rule 8`
- [ ] `C-CF-40` `literal` `COUNT` returns `2` over the worked example. `src: Core features links rule 9`
- [ ] `C-CF-41` `literal` `COUNTA` returns `3` over the worked example. `src: Core features links rule 9`
- [ ] `C-CF-42` `literal` `COUNTALL` returns `4` over the worked example. `src: Core features links rule 9`
- [ ] `C-CF-43` `literal` `SUM` returns `12` over the worked example. `src: Core features links rule 9`
- [ ] `C-CF-44` `data` A formula offers all twelve named functions. `src: Core features formula rule 1`
- [ ] `C-CF-45` `literal` `FIND` distinguishes upper case from lower case. `src: Core features formula rule 2`
- [ ] `C-CF-46` `literal` `SEARCH` ignores the case of the text sought. `src: Core features formula rule 2`
- [ ] `C-CF-47` `data` One cell change recomputes only the computed fields reached from that cell. `src: Core features formula rule 4`
- [ ] `C-CF-48` `data` A field reached by two dependency paths recomputes once for one change. `src: Core features formula rule 5`
- [ ] `C-CF-49` `data` Moving a link invalidates the computed fields of both records. `src: Core features formula rule 6`
- [ ] `C-CF-50` `data` A formula whose referenced field was retyped is marked invalid. `src: Core features formula rule 7`
- [ ] `C-CF-51` `data` A configuration making a computed field depend on itself is refused at save. `src: Core features formula rule 8`
- [ ] `C-CF-52` `literal` `ROUND` rounds half away from zero. `src: Core features formula rule 9`
- [ ] `C-CF-53` `data` Adding one tenth to two tenths gives three tenths exactly. `src: Core features formula rule 10`
- [ ] `C-CF-54` `data` A formula evaluation writes nothing. `src: Core features formula rule 11`
- [ ] `C-CF-55` `data` A view belongs to exactly one table. `src: Core features views rule 1`
- [ ] `C-CF-56` `constraint` A table holds at most 1000 views. `src: Core features views rule 2`
- [ ] `C-CF-57` `data` A kanban view stacks records by exactly one single-select field. `src: Core features views rule 5`
- [ ] `C-CF-58` `constraint` A view carries at most 49 filter conditions. `src: Core features views rule 6`
- [ ] `C-CF-59` `constraint` Filter nesting reaches three levels at most. `src: Core features views rule 6`
- [ ] `C-CF-60` `data` One level of a condition group carries exactly one conjunction. `src: Core features views rule 6`
- [ ] `C-CF-61` `constraint` A view carries at most ten sort levels. `src: Core features views rule 7`
- [ ] `C-CF-62` `data` A select field sorts by the configured order of the choices of that field. `src: Core features views rule 7`
- [ ] `C-CF-63` `constraint` Grouping reaches three levels at most. `src: Core features views rule 8`
- [ ] `C-CF-64` `data` A record is refused direct creation into a group formed on a computed field. `src: Core features views rule 8`
- [ ] `C-CF-65` `data` A personal view refuses configuration from another account. `src: Core features views rule 9`
- [ ] `C-CF-66` `data` A locked view refuses configuration from every account until unlocked. `src: Core features views rule 9`
- [ ] `C-CF-67` `data` A locked view still accepts a cell edit from a member who may edit cells. `src: Core features views rule 9`
- [ ] `C-CF-68` `data` Every write appends exactly one operation to the log of the base. `src: Core features operation log rule 1`
- [ ] `C-CF-69` `data` An operation is never updated once written. `src: Core features operation log rule 1`
- [ ] `C-CF-70` `data` An operation is never deleted once written. `src: Core features operation log rule 1`
- [ ] `C-CF-71` `data` An operation carries the account that caused the change. `src: Core features operation log rule 2`
- [ ] `C-CF-72` `data` A sequence within one base starts at 1. `src: Core features operation log rule 3`
- [ ] `C-CF-73` `data` Two simultaneous writes to one base produce two different sequence numbers. `src: Core features operation log rule 3`
- [ ] `C-CF-74` `data` A transaction is atomic across every operation inside that transaction. `src: Core features operation log rule 4`
- [ ] `C-CF-75` `data` The operations endpoint accepts a since parameter. `src: Core features operation log rule 5`
- [ ] `C-CF-76` `data` Record history is a reading of the log rather than a second table. `src: Core features operation log rule 6`
- [ ] `C-CF-77` `data` A historical read recomputes computed fields from the rebuilt values. `src: Core features operation log rule 7`
- [ ] `C-CF-78` `data` A historical read refuses every change. `src: Core features operation log rule 8`
- [ ] `C-CF-79` `data` A historical read applies the permissions of today. `src: Core features operation log rule 9`
- [ ] `C-CF-80` `data` Replay verification names the first sequence where the log parts from the stored data. `src: Core features operation log rule 10`
- [ ] `C-CF-81` `data` A guard names the table watched by that guard. `src: Core features guards rule 1`
- [ ] `C-CF-82` `literal` A guard message is shown exactly as authored. `src: Core features guards rule 2`
- [ ] `C-CF-83` `data` A guard is evaluated after computed fields have been recomputed. `src: Core features guards rule 3`
- [ ] `C-CF-84` `data` A blocking guard leaves no cell row behind. `src: Core features guards rule 4`
- [ ] `C-CF-85` `data` A blocking guard appends no operation. `src: Core features guards rule 4`
- [ ] `C-CF-86` `data` An advisory guard allows the write. `src: Core features guards rule 5`
- [ ] `C-CF-87` `data` An advisory guard records a violation until the data stops violating. `src: Core features guards rule 5`
- [ ] `C-CF-88` `data` A guard refuses a direct request exactly as a guard refuses a typed cell. `src: Core features guards rule 6`
- [ ] `C-CF-89` `constraint` A base holds at most 200 guards. `src: Core features guards rule 7`
- [ ] `C-CF-90` `literal` The seeded blocking guard reads `A deliverable cannot be marked Done with an empty estimate.` `src: Core features guards rule 8`
- [ ] `C-CF-91` `literal` The seeded advisory guard reads `A campaign over 40 hours of tasks usually needs a second owner.` `src: Core features guards rule 8`
- [ ] `C-CF-92` `contract` A refusal names what was refused. `src: Core features Refusals`
- [ ] `C-CF-93` `contract` A refusal leaves no partial write behind. `src: Core features Refusals`
- [ ] `C-CF-94` `ui` The privacy page is reachable from the footer of every page. `src: Core features A privacy page`
- [ ] `C-CF-95` `data` The privacy page is readable without signing in. `src: Core features A privacy page`
- [ ] `C-CF-96` `data` The privacy page names how long each stored value is kept. `src: Core features A privacy page`
- [ ] `C-CF-97` `ui` Every internal link on every route resolves. `src: Core features Every internal link resolves`
- [ ] `C-CF-98` `data` An unknown address answers as not found. `src: Core features Every internal link resolves`
- [ ] `C-CF-99` `ui` The not-found page carries a way back to the workspaces route. `src: Core features Every internal link resolves`

## C-UF User flow

- [ ] `C-UF-01` `contract` The root route redirects a signed-in account to the workspaces route. `src: User flow route table row 1`
- [ ] `C-UF-02` `contract` The root route redirects an unknown visitor to the login route. `src: User flow route table row 1`
- [ ] `C-UF-03` `ui` The workspaces route lists the workspaces the account holds a role in. `src: User flow route table row 5`
- [ ] `C-UF-04` `ui` The base editor route opens the first view of the first table. `src: User flow route table row 7`
- [ ] `C-UF-05` `ui` The guards panel route lists the guards of the base. `src: User flow route table row 10`
- [ ] `C-UF-06` `ui` The history route lists the operation log newest first. `src: User flow route table row 11`
- [ ] `C-UF-07` `contract` An unauthenticated request for a required route lands on the login route. `src: User flow entry para 1`
- [ ] `C-UF-08` `contract` Signing in returns the visitor to the route originally requested. `src: User flow entry para 1`
- [ ] `C-UF-09` `contract` Signing out stops the old bearer token working. `src: User flow entry para 1`
- [ ] `C-UF-10` `contract` A token expiring part-way through an action writes nothing. `src: User flow entry para 1`
- [ ] `C-UF-11` `ui` A cell edit survives a reload of the grid. `src: User flow journey 1`
- [ ] `C-UF-12` `ui` Changing the minutes of a task changes the hours of the deliverable. `src: User flow journey 2`
- [ ] `C-UF-13` `ui` A blocked write shows the guard message in an inline banner. `src: User flow journey 3`
- [ ] `C-UF-14` `ui` A commenter finds no editable cell in the grid. `src: User flow journey 4`
- [ ] `C-UF-15` `ui` A historical read shows a full-width band naming the mode. `src: User flow journey 6`
- [ ] `C-UF-16` `ui` The record route lists the history of that record newest first. `src: User flow journey 7`
- [ ] `C-UF-17` `ui` An active filter shows a count beside the filter control. `src: User flow journey 8`
- [ ] `C-UF-18` `ui` A new record appears at the bottom of the grid. `src: User flow journey 9`
- [ ] `C-UF-19` `ui` Every list carries a written empty state. `src: User flow states`
- [ ] `C-UF-20` `ui` Being filtered to nothing names the filter responsible. `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The palette is nearly colourless across ground, surfaces, rules, text. `src: UI/UX notes para 2`
- [ ] `C-UX-02` `ui` One accent colour carries every interactive affordance. `src: UI/UX notes para 2`
- [ ] `C-UX-03` `ui` The accent colour appears on no non-interactive surface. `src: UI/UX notes para 2`
- [ ] `C-UX-04` `ui` Three meaning colours each carry exactly one meaning. `src: UI/UX notes para 3`
- [ ] `C-UX-05` `ui` The historical read band sits outside the accent family. `src: UI/UX notes para 3`
- [ ] `C-UX-06` `ui` No state is carried by colour alone. `src: UI/UX notes para 3`
- [ ] `C-UX-07` `ui` The interface face is IBM Plex Sans. `src: UI/UX notes para 4`
- [ ] `C-UX-08` `ui` Record identifiers are set in IBM Plex Mono. `src: UI/UX notes para 4`
- [ ] `C-UX-09` `ui` The privacy page is set in IBM Plex Serif. `src: UI/UX notes para 4`
- [ ] `C-UX-10` `ui` Numeric columns set their figures on tabular numerals. `src: UI/UX notes para 4`
- [ ] `C-UX-11` `ui` Rows sit tight so a full table fits one screen. `src: UI/UX notes para 5`
- [ ] `C-UX-12` `ui` The work surface is a split pane showing list beside detail. `src: UI/UX notes para 5`
- [ ] `C-UX-13` `ui` Creating anything opens a slide-over panel over the current surface. `src: UI/UX notes para 5`
- [ ] `C-UX-14` `ui` Feedback is an inline banner that stays until dismissed. `src: UI/UX notes para 5`
- [ ] `C-UX-15` `ui` Motion is mechanical, short, linear, with no easing curve. `src: UI/UX notes para 6`
- [ ] `C-UX-16` `ui` A committed cell carries no transition of any kind. `src: UI/UX notes para 6`
- [ ] `C-UX-17` `ui` Entering a historical read is the most noticeable movement in the product. `src: UI/UX notes para 6`
- [ ] `C-UX-18` `ui` Reduced motion suppresses every transition described. `src: UI/UX notes para 6`
- [ ] `C-UX-19` `ui` Each page leads with exactly one primary action. `src: UI/UX notes para 7`
- [ ] `C-UX-20` `ui` Body text meets WCAG 2.1 AA contrast. `src: UI/UX notes para 8`
- [ ] `C-UX-21` `ui` A visible focus ring reaches 3:1 against its own background. `src: UI/UX notes para 8`
- [ ] `C-UX-22` `ui` Touch targets reach 44 by 44 CSS pixels. `src: UI/UX notes para 8`
- [ ] `C-UX-23` `ui` Keyboard navigation moves the grid selection with the arrow keys. `src: UI/UX notes para 8`
- [ ] `C-UX-24` `ui` The grid reads as a semantic table to assistive technology. `src: UI/UX notes para 8`
- [ ] `C-UX-25` `ui` The page body never scrolls sideways at any width. `src: UI/UX notes para 9`
- [ ] `C-UX-26` `ui` The grid scrolls in both directions inside its own container. `src: UI/UX notes para 9`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The table bar scrolls on overflow rather than wrapping. `src: Front-end specification base editor`
- [ ] `C-FE-02` `ui` A toolbar control shows a count beside the name of that control when active. `src: Front-end specification base editor`
- [ ] `C-FE-03` `ui` The grid header row stays put as the body scrolls. `src: Front-end specification grid`
- [ ] `C-FE-04` `ui` The primary column stays put as the body scrolls sideways. `src: Front-end specification grid`
- [ ] `C-FE-05` `ui` A summary row is pinned at the bottom of the grid. `src: Front-end specification grid`
- [ ] `C-FE-06` `ui` A group header carries its value, its record count, its collapse state. `src: Front-end specification grid`
- [ ] `C-FE-07` `ui` The record detail carries the history of that record newest first. `src: Front-end specification record detail`
- [ ] `C-FE-08` `ui` Every editing affordance is gone from a historical read. `src: Front-end specification mode chrome`
- [ ] `C-FE-09` `ui` The command palette matches workspaces, bases, tables, views, records by name. `src: Front-end specification command palette`
- [ ] `C-FE-10` `ui` A destructive action asks for confirmation naming what will be removed. `src: Front-end specification components`
- [ ] `C-FE-11` `data` The record surface carries the attribute `data-view`. `src: Front-end specification hooks`
- [ ] `C-FE-12` `data` The base editor root carries the attribute `data-mode`. `src: Front-end specification hooks`
- [ ] `C-FE-13` `data` A column header carries the attribute `data-field-type`. `src: Front-end specification hooks`
- [ ] `C-FE-14` `data` A grid row carries the attribute `data-record-id`. `src: Front-end specification hooks`
- [ ] `C-FE-15` `data` A guard refusal banner carries the attribute `data-guard-mode`. `src: Front-end specification hooks`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The front end is Nuxt 3. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The HTTP API is Fastify. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` Storage is PostgreSQL. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` The browser receives complete HTML for a route on first paint. `src: Technical requirements para 1`
- [ ] `C-TR-05` `constraint` No second database is introduced. `src: Technical requirements para 2`
- [ ] `C-TR-06` `contract` The database is reached at `DATABASE_URL` read from the environment. `src: Technical requirements para 3`
- [ ] `C-TR-07` `constraint` No host is hardcoded anywhere in the application. `src: Technical requirements para 3`
- [ ] `C-TR-08` `data` The application serves a favicon declared in the document head. `src: Technical requirements para 6`
- [ ] `C-TR-09` `data` Every public route declares its own social preview title. `src: Technical requirements para 6`
- [ ] `C-TR-10` `data` Every social preview image resolves over HTTP. `src: Technical requirements para 6`
- [ ] `C-TR-11` `data` No credential appears in anything the browser downloads. `src: Technical requirements para 6`

## C-DM Data model

- [ ] `C-DM-01` `data` All timestamps are UTC. `src: Data model para 1`
- [ ] `C-DM-02` `literal` The seeded password `deku-demo-pw-2026` works at login. `src: Data model para 2`
- [ ] `C-DM-03` `contract` The seeded credentials are written to `/app/USER_README.md`. `src: Data model para 2`
- [ ] `C-DM-04` `data` An email is unique across accounts, compared without case. `src: Data model accounts`
- [ ] `C-DM-05` `data` A membership is unique per account per workspace. `src: Data model memberships`
- [ ] `C-DM-06` `data` A computed value is stored nowhere. `src: Data model cells`
- [ ] `C-DM-07` `data` Operation sequence numbers are unique within their base. `src: Data model invariants`
- [ ] `C-DM-08` `data` An operation row is never changed once written. `src: Data model invariants`
- [ ] `C-DM-09` `data` Auto numbers are unique within their table. `src: Data model invariants`
- [ ] `C-DM-10` `data` Six accounts are seeded. `src: Data model seed data`
- [ ] `C-DM-11` `data` Two workspaces are seeded. `src: Data model seed data`
- [ ] `C-DM-12` `data` The Campaign Planning base carries three tables. `src: Data model seed data`
- [ ] `C-DM-13` `data` One seeded formula field is invalid because the referenced field was retyped. `src: Data model seed data`
- [ ] `C-DM-14` `data` Seeding is idempotent across a restart. `src: Data model seed data`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No file upload exists anywhere in the product. `src: Constraints bullet 2`
- [ ] `C-CN-02` `constraint` No email is sent by the product. `src: Constraints bullet 3`
- [ ] `C-CN-03` `constraint` No payment surface exists in the product. `src: Constraints bullet 4`
- [ ] `C-CN-04` `constraint` No realtime push reaches a client. `src: Constraints bullet 5`
- [ ] `C-CN-05` `constraint` No automation runs anywhere in the product. `src: Constraints bullet 6`
- [ ] `C-CN-06` `constraint` No external network call is made at run time. `src: Constraints bullet 13`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The container-internal port is `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served under the `/api` prefix on the same origin. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` The health endpoint returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` The reserved `.browser_screenshots/` directory exists at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` The reserved `.downloads/` directory exists at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-10` `contract` The server binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-11` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract API shapes`
- [ ] `C-DC-12` `contract` An invalid call is rejected as a client error. `src: Deployment contract API shapes`
- [ ] `C-DC-13` `contract` Bearer auth is carried on every endpoint except login, signup, health. `src: Deployment contract API shapes`
- [ ] `C-DC-14` `constraint` An in-memory records array is a contract violation. `src: Deployment contract No mocks`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the seeded account password | `C-RL-22` |
| `17` | the character count of an object identifier | `C-CF-21` |
| `rec` | the record identifier prefix | `C-CF-22` |
| `5400` | ninety minutes as whole seconds | `C-CF-32` |
| `COUNT` | the rollup counting numeric values | `C-CF-40` |
| `2` | the worked-example COUNT result | `C-CF-40` |
| `COUNTA` | the rollup counting non-empty values | `C-CF-41` |
| `3` | the worked-example COUNTA result | `C-CF-41` |
| `COUNTALL` | the rollup counting linked records | `C-CF-42` |
| `4` | the worked-example COUNTALL result | `C-CF-42` |
| `SUM` | the rollup totalling numeric values | `C-CF-43` |
| `12` | the worked-example SUM result | `C-CF-43` |
| `FIND` | the case-sensitive text locator | `C-CF-45` |
| `SEARCH` | the case-insensitive text locator | `C-CF-46` |
| `ROUND` | the rounding function | `C-CF-52` |
| `A deliverable cannot be marked Done with an empty estimate.` | the seeded blocking guard message | `C-CF-90` |
| `A campaign over 40 hours of tasks usually needs a second owner.` | the seeded advisory guard message | `C-CF-91` |
| `data-view` | the record-surface view hook | `` |
| `data-mode` | the base-editor mode hook | `` |
| `data-field-type` | the column-header type hook | `` |
| `data-record-id` | the grid-row identifier hook | `` |
| `data-guard-mode` | the guard refusal banner hook | `` |
| `DATABASE_URL` | the database environment variable | `` |
| `/app/USER_README.md` | the credentials file path | `` |
| `APP_PUBLIC_URL` | the public address environment variable | `` |
| `4173` | the container-internal port | `` |
| `/api` | the HTTP API prefix | `` |
| `200` | the ready answer of the health endpoint | `` |
| `.browser_screenshots/` | the reserved screenshots directory | `` |
| `.downloads/` | the reserved downloads directory | `` |
| `0.0.0.0` | the bind address | `` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact shade of each palette role | `C-UX-01` |
| the exact row height of short, medium, tall | `C-UX-11` |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| overview | 3 | 9 |
| user roles | 8 | 22 |
| core features | 42 | 99 |
| user flow | 9 | 20 |
| ui and ux notes | 5 | 26 |
| front-end specification | 3 | 15 |
| technical requirements | 4 | 11 |
| data model | 4 | 14 |
| constraints | 2 | 6 |
| deployment contract | 10 | 14 |

