# Checklist: Kanvo

Items: 167
Unpinned values flagged: 1
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` A second approval allows the merge to append one version to the shared file `src: Overview`
- [ ] `C-OV-02` `capability` Work needing sign-off is done on a branch whose review is requested from a named reviewer `src: Overview`
## C-RL User roles

- [ ] `C-RL-01` `role` An `editor` moves a frame on a file in a project of a team the `editor` belongs to `src: User roles`
- [ ] `C-RL-02` `role` An `editor` is denied the approve action on the decision endpoint `src: User roles`
- [ ] `C-RL-03` `role` An `editor` is denied on every merge endpoint `src: User roles`
- [ ] `C-RL-04` `role` An `editor` is denied on every administration endpoint `src: User roles`
- [ ] `C-RL-05` `role` A `reviewer` from a peer team is denied the decision on a branch outside that team `src: User roles`
- [ ] `C-RL-06` `role` A self approval by the branch creator is denied `src: User roles`
- [ ] `C-RL-07` `role` A `reviewer` from a peer team is denied on the decision, leaving the branch row unchanged `src: User roles`
- [ ] `C-RL-08` `role` An `org_admin` changes a member's organization role `src: User roles`
- [ ] `C-RL-09` `role` An `org_admin` holds no implicit grant on file contents `src: User roles`
- [ ] `C-RL-10` `contract` Enforcement is server-side, so an `editor` is denied on the decision endpoint whatever the interface shows `src: User roles`
- [ ] `C-RL-11` `contract` A file the caller may not read is denied with the same shape as a file that is not found `src: User roles`
- [ ] `C-RL-12` `contract` Every row is scoped by organization, so a cross-team file read is denied `src: User roles`
- [ ] `C-RL-13` `literal` Five seeded members sign in: `editor@example.com`, `editor2@example.com`, `reviewer@example.com`, `reviewer2@example.com`, `org_admin@example.com` `src: User roles`
- [ ] `C-RL-14` `literal` Every seeded account signs in with `deku-demo-pw-2026` `src: User roles`
- [ ] `C-RL-15` `role` Seat type is stored on the membership row independently of the organization role `src: User roles`
## C-CF Core features

- [ ] `C-CF-01` `capability` A seeded member signs in at the sign-in route, receiving a session `src: Core features`
- [ ] `C-CF-02` `capability` Signing in lands the member on the file first asked for rather than on an error page `src: Core features`
- [ ] `C-CF-03` `capability` An anonymous request for a protected route is denied rather than served `src: Core features`
- [ ] `C-CF-04` `capability` A repeated wrong password at sign-in is refused, creating no session `src: Core features`
- [ ] `C-CF-05` `constraint` Before repeated failures reach the lockout, a wrong password at sign-in answers the same for a seeded address as for an unknown one `src: Core features`
- [ ] `C-CF-06` `capability` A seeded member receives a bearer token that authenticates a non-browser caller `src: Core features`
- [ ] `C-CF-07` `constraint` Repeated failures at sign-in reach a lockout rather than one answer forever `src: Core features`
- [ ] `C-CF-08` `ui` The shell loads the rail trail carrying organization, team, project, file before the working area `src: Core features`
- [ ] `C-CF-09` `data` Opening `Checkout Redesign` shows the frames `Payment Step`, `Confirmation` `src: Core features`
- [ ] `C-CF-10` `capability` A frame drag is shown before the server answers, then persisted across a reload `src: Core features`
- [ ] `C-CF-11` `data` A moved frame keeps its stored position across a reload `src: Core features`
- [ ] `C-CF-12` `capability` A frame can be added, renamed, deleted `src: Core features`
- [ ] `C-CF-13` `constraint` A move that would make a frame its own ancestor is refused, leaving the tree unchanged `src: Core features`
- [ ] `C-CF-14` `contract` Two simultaneous inserts at one position under one parent both survive in one agreed order `src: Core features`
- [ ] `C-CF-15` `role` A read-only member's write sent straight to the API is denied, changing no stored frame `src: Core features`
- [ ] `C-CF-16` `ui` A declined write returns the canvas to its recorded previous state with a banner naming the reason `src: Core features`
- [ ] `C-CF-17` `contract` Two concurrent changes to one frame are both stored in one agreed order `src: Core features`
- [ ] `C-CF-18` `contract` A rename arriving for a deleted frame is discarded, so the removed frame is not stored again `src: Core features`
- [ ] `C-CF-19` `contract` Presence lists the other member in the file by display name `src: Core features`
- [ ] `C-CF-20` `contract` A member's cursor colour is derived from their identity, staying the same in later sessions `src: Core features`
- [ ] `C-CF-21` `contract` No two members in one file are shown the same presence colour `src: Core features`
- [ ] `C-CF-22` `constraint` Presence carries a stable colour for a member across sessions `src: Core features`
- [ ] `C-CF-23` `data` A comment thread is anchored to a named frame `src: Core features`
- [ ] `C-CF-24` `data` A comment thread stored against a frame carries its replies oldest first `src: Core features`
- [ ] `C-CF-25` `role` A comment edit by another member is refused, leaving the stored body unchanged `src: Core features`
- [ ] `C-CF-26` `data` Deleting a comment leaves a tombstone, keeping the thread intact `src: Core features`
- [ ] `C-CF-27` `data` Resolving a thread records the resolver, hiding the thread from the default view `src: Core features`
- [ ] `C-CF-28` `data` A thread started on a branch travels to the main file when the merge appends its version `src: Core features`
- [ ] `C-CF-29` `data` The library `Atlas Core` version `1` holds `Primary Action`, `Field Label` `src: Core features`
- [ ] `C-CF-30` `constraint` A publish is refused when any component is unnamed, naming the component `src: Core features`
- [ ] `C-CF-31` `constraint` A publish is refused when two components on one page share a name `src: Core features`
- [ ] `C-CF-32` `constraint` A publish is refused when a component contains an instance of itself `src: Core features`
- [ ] `C-CF-33` `data` A successful publish writes the next number, the changelog line, the publisher, the time `src: Core features`
- [ ] `C-CF-34` `constraint` A published library version is immutable once written `src: Core features`
- [ ] `C-CF-35` `ui` A subscriber pinned to an older version shows an update badge without changing content `src: Core features`
- [ ] `C-CF-36` `capability` The subscriber pin moves only when the update is applied, as one undoable operation `src: Core features`
- [ ] `C-CF-37` `data` Creating a branch records the source file's current version as the base version `src: Core features`
- [ ] `C-CF-38` `constraint` A branch records its base version, so an edit on the branch never reaches the main file `src: Core features`
- [ ] `C-CF-39` `capability` Requesting review names one reviewer, moving the branch to `in_review` `src: Core features`
- [ ] `C-CF-40` `constraint` A review request naming no reviewer is rejected as invalid, leaving the branch in `draft` `src: Core features`
- [ ] `C-CF-41` `constraint` A `changes_requested` decision without a comment is rejected as invalid `src: Core features`
- [ ] `C-CF-42` `capability` A branch in `changes_requested` returns to `in_review` when the requester pushes a change `src: Core features`
- [ ] `C-CF-43` `data` Approving records the branch's current version as the approved version `src: Core features`
- [ ] `C-CF-44` `contract` A push after an approval invalidates that approval in the act that stores the new version `src: Core features`
- [ ] `C-CF-45` `ui` The review panel names the version that superseded an invalidated approval `src: Core features`
- [ ] `C-CF-46` `contract` A merge is refused unless the branch's current version equals the approved version `src: Core features`
- [ ] `C-CF-47` `contract` A refused merge leaves the main file carrying no merge version `src: Core features`
- [ ] `C-CF-48` `contract` A refused merge leaves the branch out of `applied` `src: Core features`
- [ ] `C-CF-49` `role` Self-approval is denied, leaving the branch state unchanged `src: Core features`
- [ ] `C-CF-50` `role` A reviewer outside the file's team is denied on merge `src: Core features`
- [ ] `C-CF-51` `data` A successful merge appends one merge version, moving the branch to `applied` `src: Core features`
- [ ] `C-CF-52` `contract` Merging one branch twice produces exactly one merge version `src: Core features`
- [ ] `C-CF-53` `capability` A branch withdrawal by its creator is stored from any state `src: Core features`
- [ ] `C-CF-54` `literal` A review request sends one message whose subject begins `Review requested: ` `src: Core features`
- [ ] `C-CF-55` `literal` An approval delivers one mail to the requester whose subject begins `Review approved: ` `src: Core features`
- [ ] `C-CF-56` `literal` A merge sends one message whose subject begins `Branch merged: ` `src: Core features`
- [ ] `C-CF-57` `constraint` A review request delivers one mail to the reviewer alone, carrying no copy address `src: Core features`
- [ ] `C-CF-58` `constraint` A `changes_requested` decision sends no mail `src: Core features`
- [ ] `C-CF-59` `constraint` A withdrawal delivers no mail `src: Core features`
- [ ] `C-CF-60` `constraint` An invalidated approval delivers no mail `src: Core features`
- [ ] `C-CF-61` `data` Every review mail names the branch in its body, naming the file too `src: Core features`
- [ ] `C-CF-62` `ui` A notification centre carries an unread count, read from a server-stored cursor `src: Core features`
- [ ] `C-CF-63` `ui` The member list shows address, organization role, seat type, team count, status `src: Core features`
- [ ] `C-CF-64` `capability` A role change takes effect on the member's next request `src: Core features`
- [ ] `C-CF-65` `ui` A bulk role change is previewed with the permitted count, naming the unpermitted count `src: Core features`
- [ ] `C-CF-66` `capability` A bulk change applies only the permitted rows, reporting per row `src: Core features`
- [ ] `C-CF-67` `contract` Inviting an existing member returns the existing membership, creating no second row `src: Core features`
- [ ] `C-CF-68` `constraint` An invitation carrying a malformed address stores no membership row `src: Core features`
- [ ] `C-CF-69` `data` The audit stream stores every review transition with its actor, naming the outcome `src: Core features`
- [ ] `C-CF-70` `constraint` Every stored audit action is drawn from the closed vocabulary the stream accepts `src: Core features`
- [ ] `C-CF-71` `data` An invalidated approval writes its own `approval_invalidated` record naming both versions `src: Core features`
- [ ] `C-CF-72` `contract` The audit stream is append-only in the store, refusing an update from the application role `src: Core features`
- [ ] `C-CF-73` `role` Only an `org_admin` reads the audit stream `src: Core features`
- [ ] `C-CF-74` `capability` The audit stream filters by actor, by action, by time range `src: Core features`
- [ ] `C-CF-75` `ui` The route `/` is a public overview leading with one primary action reaching `/signin` `src: Core features`
- [ ] `C-CF-76` `contract` Every internal link on every public route resolves `src: Core features`
- [ ] `C-CF-77` `capability` The route `/access` records an access request, validating the address inline `src: Core features`
- [ ] `C-CF-78` `constraint` An access request carrying a filled decoy field is refused, recording nothing `src: Core features`
- [ ] `C-CF-79` `contract` An unknown address answers not-found from the product's own page `src: Core features`
- [ ] `C-CF-80` `contract` A push that invalidates the approval returns the branch to `in_review` `src: Core features`
- [ ] `C-CF-81` `contract` Reading presence counts the calling member as present in the file `src: Core features`
- [ ] `C-CF-82` `constraint` An access request repeated more than five times inside a minute from one source is refused `src: Core features`
- [ ] `C-CF-83` `ui` The requester's notification centre carries a changes-requested decision that sent no mail `src: Core features`
- [ ] `C-CF-84` `ui` A review request appears in the named reviewer's notification centre `src: Core features`
## C-UF User flow

- [ ] `C-UF-01` `ui` Every route drills down from the team to the project to the file by its own address `src: User flow`
- [ ] `C-UF-02` `capability` Signing out returns the editor to the public overview, ending the session at once `src: User flow`
- [ ] `C-UF-03` `ui` A revoked session shows the evicted explanation with one action `src: User flow`
- [ ] `C-UF-04` `role` An `editor` asking for an administration route is denied by the server `src: User flow`
- [ ] `C-UF-05` `ui` The rail shows the editor no entry to the administration area `src: User flow`
- [ ] `C-UF-06` `ui` Every list carries an empty state naming what to do next `src: User flow`
- [ ] `C-UF-07` `ui` The canvas confirms a frame drag with a banner rather than a silent save `src: User flow`
- [ ] `C-UF-08` `ui` An error never crashes the app, leaving the surrounding shell usable `src: User flow`
- [ ] `C-UF-09` `ui` The canvas shows the dimmed still with a determinate bar before live frames arrive `src: User flow`
- [ ] `C-UF-10` `ui` The approve control in the review panel waits for the server before reporting `src: User flow`
- [ ] `C-UF-11` `ui` A failed approval returns the control to its previous state, naming the reason `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The interface reads quiet, dense but organised, built for scanning `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The ground is monochrome, expressed as one base colour at a ladder of strengths `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The failure colour appears nowhere except failure `src: UI/UX notes`
- [ ] `C-UX-04` `ui` The success colour appears nowhere except a completed governed transition `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Typography is `Inter` for the interface, `JetBrains Mono` for identifiers `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Motion is eased, animating only transform, opacity, colour `src: UI/UX notes`
- [ ] `C-UX-07` `ui` A reduced-motion preference removes entrance movement, keeping short control transitions `src: UI/UX notes`
- [ ] `C-UX-08` `ui` A dark theme is required, following the platform preference with a server-stored override `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Body text meets WCAG AA contrast against its background in both themes `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Every focusable element carries a visible two-ring focus indicator `src: UI/UX notes`
- [ ] `C-UX-11` `ui` A frame tree beside the canvas is the primary keyboard path into the document `src: UI/UX notes`
- [ ] `C-UX-12` `ui` Each screen leads with exactly one primary action, visually distinct from every secondary one `src: UI/UX notes`
- [ ] `C-UX-13` `ui` At a narrow viewport nothing overflows sideways, keeping every navigation target reachable `src: UI/UX notes`
- [ ] `C-UX-14` `ui` The review panel presents the approve action to a reviewer entitled to decide `src: UI/UX notes`
- [ ] `C-UX-15` `ui` The review panel marks an approval as superseded once the branch has moved `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` At a narrow viewport the arrangement drops to an overlay drawer with nothing overflowing `src: Front-end specification`
- [ ] `C-FE-02` `ui` Corner softness rises with control height across the stated ladder `src: Front-end specification`
- [ ] `C-FE-03` `ui` A control carries an inset ring rather than a border, so a pointer change causes no reflow `src: Front-end specification`
- [ ] `C-FE-04` `ui` Zoom runs continuously with no discrete steps, uncoupled from document scroll `src: Front-end specification`
- [ ] `C-FE-05` `ui` A drag snaps to the stated grid, snapping also to sibling edges within the stated distance `src: Front-end specification`
- [ ] `C-FE-06` `ui` Undo is per member, never reversing a colleague's change `src: Front-end specification`
- [ ] `C-FE-07` `ui` Loading the canvas runs in four steps, showing something after the first `src: Front-end specification`
- [ ] `C-FE-08` `ui` Presence updates are coalesced to the stated rate, persisted nowhere `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `literal` A frame move is persisted in PostgreSQL, reached at `DATABASE_URL` `src: Technical requirements`
- [ ] `C-TR-02` `literal` A seeded member signs in against Keycloak, reached at `AUTH_URL` `src: Technical requirements`
- [ ] `C-TR-03` `literal` A review request delivers mail through Mailpit, reached at `SMTP_HOST` `src: Technical requirements`
- [ ] `C-TR-04` `contract` The health route answers an anonymous request, unlike every other request, which is denied `src: Technical requirements`
- [ ] `C-TR-05` `contract` `/sitemap.xml` lists every public route the app serves `src: Technical requirements`
- [ ] `C-TR-06` `contract` `/robots.txt` names the sitemap location `src: Technical requirements`
- [ ] `C-TR-07` `contract` Every public route carries its own title, from the overview through to the sign-in route `src: Technical requirements`
- [ ] `C-TR-08` `contract` A repeated invitation returns the first result, storing no second row `src: Technical requirements`
- [ ] `C-TR-09` `contract` A refused review request names the reviewer field that failed, writing nothing `src: Technical requirements`
- [ ] `C-TR-10` `contract` An action driven straight at the decision endpoint denies an `editor` exactly as the interface would `src: Technical requirements`
- [ ] `C-TR-11` `contract` A merge refused over an invalidated approval leaves no partial state `src: Technical requirements`
- [ ] `C-TR-12` `literal` A seeded member signs in through the Keycloak realm `deku` with the client `kanvo-app` `src: Technical requirements`
## C-DM Data model

- [ ] `C-DM-01` `literal` Every seeded member signs in with the password `deku-demo-pw-2026` `src: Data model`
- [ ] `C-DM-02` `data` `file_version.sequence` rises by one per file, starting at one `src: Data model`
- [ ] `C-DM-03` `data` `review_decision.target_version_id` binds an approval to a version `src: Data model`
- [ ] `C-DM-04` `data` A push invalidates the approval, leaving the decision record in place `src: Data model`
- [ ] `C-DM-05` `literal` Signing in reaches the organization `Harborlight` through the team `Atlas` `src: Data model`
- [ ] `C-DM-06` `literal` The project `Atlas Mobile` carries the files `Checkout Redesign`, `Atlas Core Kit` `src: Data model`
- [ ] `C-DM-07` `data` Seeding is idempotent, so a seeded member holds exactly one membership row `src: Data model`
- [ ] `C-DM-08` `literal` The team `Beacon` carries the project `Beacon Web` with the file `Beacon Landing`, read by a member of that team `src: Data model`
## C-CN Constraints

- [ ] `C-CN-01` `constraint` A cross-team file read is denied, so one tenant reaches nothing of another `src: Constraints`
- [ ] `C-CN-02` `constraint` No signup page is served, so an anonymous request for one is denied as not found `src: Constraints`
## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app answers at its public address, so even an unknown address reaches the product `src: Deployment contract`
- [ ] `C-DC-02` `contract` The public routes the sitemap lists are served on the mapped port `src: Deployment contract`
- [ ] `C-DC-03` `contract` A seeded member signs in through the API on the same origin, receiving a token `src: Deployment contract`
- [ ] `C-DC-04` `contract` The app starts from its image, answering at an unknown address with no manual step `src: Deployment contract`
- [ ] `C-DC-05` `contract` The audit stream is read as a top-level array of stored review transitions `src: Deployment contract`
- [ ] `C-DC-06` `contract` An invalid frame move is refused as a client error rather than a server error `src: Deployment contract`
- [ ] `C-DC-07` `contract` An unauthorized call to the merge endpoint is denied rather than served `src: Deployment contract`
- [ ] `C-DC-08` `contract` Every endpoint beyond the health route, the public routes aside, denies an anonymous request `src: Deployment contract`
- [ ] `C-DC-09` `contract` The approval answer carries the branch version field named in the endpoint table `src: Deployment contract`
- [ ] `C-DC-10` `constraint` No in-memory stand-in substitutes for the mail service a review request delivers through `src: Deployment contract`
## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the seeded password | `C-RL-14` |
| `editor@example.com` | the first seeded editor | `C-RL-13` |
| `editor2@example.com` | the second seeded editor | `C-RL-13` |
| `reviewer@example.com` | the in-team reviewer | `C-RL-13` |
| `reviewer2@example.com` | the peer-team reviewer | `C-RL-13` |
| `org_admin@example.com` | the seeded administrator | `C-RL-13` |
| `Review requested: ` | the review-request subject prefix | `C-CF-54` |
| `Review approved: ` | the approval subject prefix | `C-CF-55` |
| `Branch merged: ` | the merge subject prefix | `C-CF-56` |
| `Atlas Core` | the seeded library | `C-CF-29` |
| `Primary Action` | the first seeded component | `C-CF-29` |
| `Field Label` | the second seeded component | `C-CF-29` |
| `1` | the seeded library version number | `C-CF-29` |
| `DATABASE_URL` | the datastore variable | `C-TR-01` |
| `AUTH_URL` | the identity variable | `C-TR-02` |
| `SMTP_HOST` | the mail host variable | `C-TR-03` |
| `deku` | the Keycloak realm | `C-TR-12` |
| `kanvo-app` | the Keycloak client | `C-TR-12` |
| `Harborlight` | the seeded organization | `C-DM-05` |
| `Atlas` | the first seeded team | `C-DM-05` |
| `Beacon` | the second seeded team | `C-DM-08` |
| `Atlas Mobile` | the first seeded project | `C-DM-06` |
| `Beacon Web` | the second seeded project | `C-DM-08` |
| `Checkout Redesign` | the seeded design file | `C-DM-06` |
| `Atlas Core Kit` | the seeded library file | `C-DM-06` |
| `Beacon Landing` | the peer-team file | `C-DM-08` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the name a member types when opening a branch | `C-CF-37` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 0 | 2 |
| User roles | 7 | 15 |
| Core features | 33 | 84 |
| User flow | 8 | 11 |
| UI/UX notes | 2 | 15 |
| Front-end specification | 5 | 8 |
| Technical requirements | 12 | 12 |
| Data model | 5 | 8 |
| Constraints | 2 | 2 |
| Deployment contract | 10 | 10 |

## Declared but ungraded
These obligations are stated in the brief and are the agent's to meet. No
channel this kit runs can observe them, so they are recorded here rather than
carrying a citation nobody earned. Several are proven downstream by the
handoff gates. OPEN-DECISIONS D-H is the standing question this part answers.

| Obligation | why it is ungraded |
|---|---|
| The product offers no vector path editing, no billing, no plugins, no uploaded image bytes | an absence: the kit has no channel that observes a feature the product does not have |
| One decision answers every read before any data is loaded | one decision function is a source property; G10 bars a reward-bearing test from reading the source |
| An attribute rule only removes a capability, never adds one | the attribute filter direction is a source property, observable only by reading the policy module |
| A grant outside its start bound is powerless the moment the bound passes | no grant endpoint is pinned, so a time-bounded grant cannot be created or expired from outside |
| A direct deny on one file for one member carries a reason | the same: a direct deny carries a reason in a record no pinned endpoint exposes |
| Switching organization drops every cached list keyed to the previous one | one organization is seeded, so the switcher has no second tenant to drop a cache for |
| A reconnecting client keeps every change committed before the drop | reconnection needs the live transport, and no realtime slot is declared |
| A `review` notification addressed to a member cannot be turned off | no notification-preference endpoint is pinned, so the non-suppressible category cannot be probed |
| Each route arrives as server-rendered HTML readable before any script runs | the rendering model is observable only as a source property once the page has hydrated |
| Only the interactive regions hydrate as islands | which regions hydrate is a source property |
| Every request writes one structured log line carrying method, path, status, duration, request identifier | the kit has no log channel; the structured line is read by an operator, not a grader |
| No second database, cache, queue, object store, identity provider, mail vendor is introduced | a second datastore would be a source and environment property |
| Every host, port, credential is read from the environment, never hardcoded | reading configuration rather than a literal is a source property |
| The session cookie is `HttpOnly`, `Secure`, `SameSite=Lax`, scoped to the host | the graders authenticate by bearer token, so the browser cookie flags are never on their path |
| The session reference is resolved on every request | resolving the session every request is observable only through a deactivation no pinned endpoint performs |
| A state-changing request carries a token bound to the session | the request-forgery token belongs to the browser session the graders do not use |
| No state-changing operation is reachable by a safe method | reaching a mutating operation by a safe method is a route-shape property no pinned endpoint exposes |
| The identity provider's subject is the join key onto a member, never the mail address | the identity join key is a source property |
| The schema is migrated as the app starts, running once across restarts | migration on start is proven by the handoff gates that boot the image, not by a static gate |
| The API version is part of the response | no endpoint in the pinned table returns the API version |
| A list endpoint takes a cursor, returning the array with the next cursor | no pinned list endpoint carries a cursor argument in the table |
| An invitation carries at most fifty addresses | the fifty-address cap needs a bulk invitation endpoint that the pinned table does not carry |
| A denial is instrumented with its reason on the structured log line | the same log channel as C-TR-07 |
| Every timestamp is stored with its zone, never as a bare local time | no pinned response field is documented as carrying a zone |
| Permission for a list is resolved in one round trip rather than once per row | round-trip count is invisible to a black-box caller |
| A change made by one member reaches the others without either reloading the page | live propagation needs the realtime transport, and no realtime slot is declared |
| The canvas stays interactive with two hundred frames on a page | a frame-count performance bar is not deterministic between two identical runs |
| Fourteen tables carry the model, with every timestamp in UTC | counting tables would couple a reward-bearing check to the schema shape rather than to behaviour |
| The seeded credentials are written into `/app/USER_README.md` | the credentials file is proven by the handoff gates that boot the image |
| No external network call is made at runtime | the absence of an outbound call is not observable from inside the app |
| The app stays responsive at the stated data volumes | a responsiveness bar at a data volume is a performance measurement, not a deterministic check |
| Reserved `.browser_screenshots/`, `.downloads/` directories exist at the app root, empty | the reserved directories are proven by the handoff gates that boot the image |
| A production build is served behind a static or preview server, never a dev server | a production build rather than a dev server is proven at image build, handoff-owned |
| The server keeps running after the session ends, never as a child of the shell | the server outliving the session is exactly what the oracle run proves, handoff-owned |
| The server binds `0.0.0.0`, never `127.0.0.1` | the bind address is proven by the harness reaching the container, handoff-owned |
| No copy of a backing service is downloaded, installed, compiled, started | a downloaded copy of a backing service is a source and environment property |
| No edge function is used | an edge function would be an environment property |
| No persistent volume, no fixed container name, no custom network is declared | volumes, container names and networks are compose properties the handoff gates read |
| A deactivated member is refused on their very next request | no pinned endpoint deactivates a member, so the next-request refusal cannot be exercised |
| Deactivating a member releases their seat immediately, retaining their content | the same: releasing a seat needs a deactivation the pinned table does not carry |
| Enforcement set to required with no break-glass principal named is refused, leaving the stored row unchanged | identity enforcement is written by one pinned endpoint but its break-glass precondition is not readable from outside |
| At most two break-glass principals may be named | the two-principal cap on break-glass sits behind the same unreadable precondition |
| An administrator opening ungranted content is recorded under `admin_content_access` | administrative content access needs an administrator who holds a team grant, and none is seeded |
| A degraded connection keeps reads working, leaving write controls disabled | a dropped live connection cannot be induced from a screenshot-and-click judge, and no realtime slot is declared to observe it deterministically |
| An explicit deny beats every allow, so a denied write changes no row | no pinned endpoint writes a grant, so an explicit deny cannot be set up from outside the app |
| An edit after the stated window is refused | the fifteen-minute edit window cannot elapse inside a bounded grading run |
| The file version sequence rises rather than rewinding, so restoring appends | no pinned endpoint restores an earlier version, so an append-on-restore cannot be exercised |
| A deny grant is legal only on a file, which is where an implicit grant is refused | no pinned endpoint writes a grant row, so the file-only deny rule cannot be exercised |
| Two active files in one project never share a name, as a duplicate name is refused | no pinned endpoint creates or renames a file, so the active-name uniqueness rule cannot be exercised |
