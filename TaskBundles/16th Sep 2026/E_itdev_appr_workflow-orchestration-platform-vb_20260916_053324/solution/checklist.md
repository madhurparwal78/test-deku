# Checklist: workflow-orchestration-platform-vb

Items: 246
Unpinned values flagged: 6
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

---

## C-OV Overview

- [ ] `C-OV-01` `capability` A public marketing site of thirteen routes is served without any session `src: Overview paragraph 2`
- [ ] `C-OV-02` `capability` A workflow orchestration engine walks a drawn graph of steps `src: Overview paragraph 3`
- [ ] `C-OV-03` `capability` A run pauses where a person has to approve, then resumes on a decision `src: Overview paragraph 3`
- [ ] `C-OV-04` `constraint` A run that is paused holds no worker at all `src: Overview paragraph 3`
- [ ] `C-OV-05` `constraint` No marketing route renders a live run `src: Overview non-goals`
- [ ] `C-OV-06` `capability` The engine writes down where a run reached, releases its worker, then resumes from that point on a different worker `src: Overview final paragraph`

## C-RL User roles

- [ ] `C-RL-01` `role` An `operator` creates workflows, saves versions, starts manual runs, reads runs inside any project holding that `operator` as a member `src: User roles table`
- [ ] `C-RL-02` `role` An `operator` is refused when deciding an approval `src: User roles bullet 1`
- [ ] `C-RL-03` `role` An `operator` is refused when creating a credential `src: User roles bullet 1`
- [ ] `C-RL-04` `role` An `operator` is refused when reading the audit stream `src: User roles bullet 1`
- [ ] `C-RL-05` `role` An `approver` decides a run that is waiting inside any project holding that `approver` as a member `src: User roles table`
- [ ] `C-RL-06` `role` An `approver` is refused when deciding a run in a project holding no membership for that `approver` `src: User roles bullet 2`
- [ ] `C-RL-07` `role` An `owner` creates credentials, changes membership, reads the audit stream `src: User roles table`
- [ ] `C-RL-08` `role` Nobody at any privilege reads a stored credential value `src: User roles bullet 3`
- [ ] `C-RL-09` `role` Nobody reads or writes anything inside a project holding no membership for the caller `src: User roles bullet 4`
- [ ] `C-RL-10` `contract` Authorization is enforced server-side on every mutating endpoint `src: User roles closing paragraph`
- [ ] `C-RL-11` `contract` A direct call from a lower-role session to a higher-role endpoint is denied, leaving the protected state unchanged `src: User roles closing paragraph`
- [ ] `C-RL-12` `literal` Five accounts are seeded: `owner@example.com`, `approver@example.com`, `approver2@example.com`, `operator@example.com`, `operator2@example.com` `src: User roles seeded table`
- [ ] `C-RL-13` `literal` Every seeded account signs in with `deku-demo-pw-2026` `src: User roles signup paragraph`
- [ ] `C-RL-14` `constraint` Signup is closed, so no route creates an account `src: User roles signup paragraph`

## C-CF Core features

- [ ] `C-CF-01` `capability` Sign-in takes an email with a password, returning a bearer token `src: Core features Auth`
- [ ] `C-CF-02` `contract` Passwords are stored hashed, never in the clear `src: Core features Auth`
- [ ] `C-CF-03` `contract` Role is resolved from the session, never read from a request body `src: Core features Auth`
- [ ] `C-CF-04` `capability` A sign-in with a wrong password is denied, returning no token `src: Core features rule 2`
- [ ] `C-CF-05` `capability` A console request carrying no bearer token is denied `src: Core features rule 3`
- [ ] `C-CF-06` `capability` Repeated failed sign-ins for one address are refused for a period `src: Core features rule 4`
- [ ] `C-CF-07` `capability` A person sees exactly the projects holding a membership for that person `src: Core features rule 6`
- [ ] `C-CF-08` `capability` A request for a project the caller does not belong to is denied `src: Core features rule 7`
- [ ] `C-CF-09` `capability` Only an `owner` changes membership, with every change recorded in the audit stream `src: Core features rule 8`
- [ ] `C-CF-10` `ui` A workflow opens with its steps on a dotted ground joined by curved edges, with the step list beside the canvas `src: Core features rule 9`
- [ ] `C-CF-11` `ui` A step is added as a new row at the end of the step list, never in a modal `src: Core features rule 9`
- [ ] `C-CF-12` `data` A step carries a name unique within its workflow `src: Core features rule 10`
- [ ] `C-CF-13` `data` A connection carries a source step, a source output index, a target step, a target input index, a type `src: Core features rule 11`
- [ ] `C-CF-14` `capability` Saving produces a new immutable version whose number increments on the canvas header `src: Core features rule 12`
- [ ] `C-CF-15` `capability` A workflow whose graph is invalid is refused at save time, with nothing written `src: Core features rule 13`
- [ ] `C-CF-16` `capability` Comparing two versions reports a step that only moved separately from a step whose behaviour changed `src: Core features rule 14`
- [ ] `C-CF-17` `capability` A workflow that calls itself through any chain is refused rather than exhausting the call stack `src: Core features rule 15`
- [ ] `C-CF-18` `capability` A sub-workflow run is a first-class run with its own identifier, linked to its parent `src: Core features rule 16`
- [ ] `C-CF-19` `capability` Deleting a workflow is a soft-delete, with runs pruned on the ordinary retention schedule `src: Core features rule 17`
- [ ] `C-CF-20` `contract` No endpoint returns a stored credential value to any actor at any privilege `src: Core features rule 19`
- [ ] `C-CF-21` `capability` Testing a credential is the server making a probe call, never the value reaching the browser `src: Core features rule 20`
- [ ] `C-CF-22` `capability` Binding a credential to a step is an `owner` action recorded in the audit stream `src: Core features rule 21`
- [ ] `C-CF-23` `capability` Revoking a credential an active workflow depends on warns first, naming every workflow that breaks `src: Core features rule 22`
- [ ] `C-CF-24` `capability` Starting a run creates the run at status `new`, placing the run on the queue `src: Core features rule 23`
- [ ] `C-CF-25` `capability` A worker claims a run, sets status `running`, records the worker identifier, keeps a heartbeat `src: Core features rule 24`
- [ ] `C-CF-26` `capability` Two simultaneous claims of one queued run leave exactly one winner, with the worker identifier unchanged for the loser `src: Core features rule 25`
- [ ] `C-CF-27` `capability` A step on an untaken branch is marked `skipped` rather than left `pending` `src: Core features rule 27`
- [ ] `C-CF-28` `capability` Each attempt at a step is recorded as its own row `src: Core features rule 28`
- [ ] `C-CF-29` `capability` A step set to `continue_error_output` routes its failure to a second visible output `src: Core features rule 29`
- [ ] `C-CF-30` `capability` A loop past its iteration ceiling fails the run with an error naming the cycle `src: Core features rule 30`
- [ ] `C-CF-31` `capability` An expression referring to an earlier step resolves to the correct ancestor item `src: Core features rule 31`
- [ ] `C-CF-32` `capability` Data pinned to a step is used on a manual run, refused on a production run `src: Core features rule 33`
- [ ] `C-CF-33` `capability` Cancelling a run keeps every attempt produced up to that moment `src: Core features rule 34`
- [ ] `C-CF-34` `data` A run records the workflow version executed against `src: Core features rule 36`
- [ ] `C-CF-35` `capability` An approval step sets the run status to `waiting`, releasing the worker `src: Core features rule 37`
- [ ] `C-CF-36` `constraint` A run at `waiting` holds no worker identifier `src: Core features rule 37`
- [ ] `C-CF-37` `capability` The approval step mints one approve address plus one reject address, each unguessable, each single use `src: Core features rule 38`
- [ ] `C-CF-38` `capability` Approve, reject, expire are three distinct outcomes routing differently `src: Core features rule 39`
- [ ] `C-CF-39` `capability` Only an `approver` or an `owner` belonging to the run's project decides that run `src: Core features rule 40`
- [ ] `C-CF-40` `contract` A decision request from an `operator` session is denied, with the run still `waiting`, no approval decision recorded `src: Core features rule 40`
- [ ] `C-CF-41` `contract` A decision request from an `approver` of another project is denied, with that run unchanged `src: Core features rule 41`
- [ ] `C-CF-42` `data` A decision records the person deciding, plus the moment of the decision `src: Core features rule 42`
- [ ] `C-CF-43` `capability` Presenting the same single-use address a second time is refused, with the recorded decision unchanged `src: Core features rule 43`
- [ ] `C-CF-44` `capability` An approved run is re-queued, resumes on a possibly different worker, reaches `succeeded` `src: Core features rule 44`
- [ ] `C-CF-45` `capability` A rejected run reaches `failed`, with the steps after the approval step marked `skipped` `src: Core features rule 45`
- [ ] `C-CF-46` `capability` Every approval decision is an audit event `src: Core features rule 46`
- [ ] `C-CF-47` `capability` A path already held by another active workflow is refused at activation, naming the other workflow `src: Core features rule 48`
- [ ] `C-CF-48` `capability` Every workflow has two separate inbound addresses, one for production, one for the editor `src: Core features rule 49`
- [ ] `C-CF-49` `capability` A repeat carrying the same idempotency key returns the original run identifier, starting no second run `src: Core features rule 50`
- [ ] `C-CF-50` `capability` A schedule is stored with its own timezone, not the server's `src: Core features rule 51`
- [ ] `C-CF-51` `capability` A run whose worker stops heartbeating is marked `crashed`, keeping every attempt produced `src: Core features rule 54`
- [ ] `C-CF-52` `constraint` A crashed run is never re-run by the engine on its own `src: Core features rule 54`
- [ ] `C-CF-53` `constraint` A queue job carries the run identifier only, never the run's data `src: Core features rule 56`
- [ ] `C-CF-54` `capability` A job failing repeatedly is given up on after a bounded number of attempts, marked `crashed` `src: Core features rule 58`
- [ ] `C-CF-55` `capability` A per-workflow limit of simultaneous runs may be set as low as one `src: Core features rule 60`
- [ ] `C-CF-56` `capability` Exactly one coordinating process owns the schedule at any moment `src: Core features rule 62`
- [ ] `C-CF-57` `capability` An agent calls only the tools wired to that agent on the canvas `src: Core features rule 67`
- [ ] `C-CF-58` `capability` Memory is keyed by a session identifier drawn from the input `src: Core features rule 70`
- [ ] `C-CF-59` `capability` Thirteen public routes render `src: Core features rule 73`
- [ ] `C-CF-60` `contract` Every public route carries its own title plus its own description, with no two routes sharing either `src: Core features rule 74`
- [ ] `C-CF-61` `contract` The site serves a favicon, declaring the favicon in the document head `src: Core features rule 75`
- [ ] `C-CF-62` `ui` Each page leads with one clear primary action, visually distinct from every secondary one `src: Core features rule 76`
- [ ] `C-CF-63` `capability` An unknown address renders the product's own not-found page, answering not found `src: Core features rule 77`
- [ ] `C-CF-64` `capability` Every internal link on every public route resolves `src: Core features rule 78`
- [ ] `C-CF-65` `capability` The repository star count renders a stale value rather than blanking when its source is unreachable `src: Core features rule 79`
- [ ] `C-CF-66` `literal` Four plans render in order: `Starter`, `Pro`, `Business`, `Enterprise` `src: Core features rule 80`
- [ ] `C-CF-67` `ui` A billing switch defaults to annual, rewriting every price with no route change `src: Core features rule 81`
- [ ] `C-CF-68` `literal` Starter is `2900` monthly, `2400` annually `src: Core features rule 82`
- [ ] `C-CF-69` `literal` Pro is `7200` monthly, `6000` annually `src: Core features rule 82`
- [ ] `C-CF-70` `literal` Business is `80000` monthly, `66700` annually `src: Core features rule 82`
- [ ] `C-CF-71` `literal` Included executions are `2500` for Starter, `10000` for Pro, `40000` for Business `src: Core features rule 83`
- [ ] `C-CF-72` `capability` Changing one column's volume changes that column's price, no other column's `src: Core features rule 83`
- [ ] `C-CF-73` `literal` The fourth column reads `Contact Sales` where a price would be `src: Core features rule 84`
- [ ] `C-CF-74` `capability` Catalogue free text matches name plus description, case insensitively `src: Core features rule 89`
- [ ] `C-CF-75` `ui` A segmented control narrows by type across four options `src: Core features rule 90`
- [ ] `C-CF-76` `ui` A sort control defaults to `Popularity` `src: Core features rule 91`
- [ ] `C-CF-77` `ui` A count above the grid reads the number of matches followed by `integrations` `src: Core features rule 92`
- [ ] `C-CF-78` `capability` The query, the facets, the sort, the page all live in the address `src: Core features rule 93`
- [ ] `C-CF-79` `capability` Facet counts reflect the other active filters rather than the whole corpus `src: Core features rule 94`
- [ ] `C-CF-80` `literal` The catalogue pages at `24` results by default, `60` at most `src: Core features rule 95`
- [ ] `C-CF-81` `capability` A page past the last page returns an empty result set with the correct total `src: Core features rule 95`
- [ ] `C-CF-82` `ui` A result set of zero renders an explicit empty state, never an empty grid `src: Core features rule 96`
- [ ] `C-CF-83` `ui` The case-study card sets the metric alone bold, not the whole sentence `src: Core features rule 98`
- [ ] `C-CF-84` `capability` Every form field is validated again on the server, with invalid input rejected inline naming the field `src: Core features rule 102`
- [ ] `C-CF-85` `constraint` Nothing is written when a form submission is rejected `src: Core features rule 102`
- [ ] `C-CF-86` `data` The consent value is stored with a timestamp plus the exact wording shown `src: Core features rule 103`
- [ ] `C-CF-87` `data` Three campaign fields are filled from the query string, stored with the request `src: Core features rule 104`
- [ ] `C-CF-88` `capability` A submission is refused when an unattended decoy field arrives filled `src: Core features rule 105`
- [ ] `C-CF-89` `capability` A form submitted repeatedly in quick succession from one address is refused `src: Core features rule 105`
- [ ] `C-CF-90` `capability` A first-time visitor is asked once about non-essential cookies, with the answer surviving a reload `src: Core features rule 107`
- [ ] `C-CF-91` `ui` Declining consent is one press at the same size, the same prominence, as accepting `src: Core features rule 108`
- [ ] `C-CF-92` `capability` A privacy page reachable from every footer states what Flowmark records `src: Core features rule 110`
- [ ] `C-CF-93` `capability` Opening a run shows every step with a status, an output summary, an attempt count `src: Core features rule 111`
- [ ] `C-CF-94` `constraint` The audit stream is append-only, readable only by an `owner` `src: Core features rule 112`
- [ ] `C-CF-95` `capability` Health answers separately for liveness, for readiness `src: Core features rule 113`

## C-UF User flow

- [ ] `C-UF-01` `contract` An unauthenticated request for a console route redirects to sign-in, landing afterwards on the route asked for `src: User flow entry bullet 1`
- [ ] `C-UF-02` `contract` A successful sign-in with no pending destination lands on the project list `src: User flow entry bullet 2`
- [ ] `C-UF-03` `contract` Signing out returns to the home route, with later console requests redirected `src: User flow entry bullet 3`
- [ ] `C-UF-04` `contract` An expired token leaves the action unapplied, preserving the destination `src: User flow entry bullet 4`
- [ ] `C-UF-05` `contract` A person outside the project named in the path is refused, shown the console's not-found page `src: User flow entry bullet 5`
- [ ] `C-UF-06` `contract` An `operator` requesting a credentials, members, audit route is refused, staying signed in `src: User flow entry bullet 6`
- [ ] `C-UF-07` `ui` Console navigation is a drill-down with a breadcrumb `src: User flow routes paragraph`
- [ ] `C-UF-08` `ui` The public site carries a top navigation bar of six entries, four opening a panel `src: User flow routes paragraph`
- [ ] `C-UF-09` `ui` The run board shows a queued run moving through running to waiting for approval `src: User flow journey 2`
- [ ] `C-UF-10` `ui` An approval decision lands on a confirmation page carrying the run identifier plus the decision `src: User flow journey 3`
- [ ] `C-UF-11` `ui` Every list has an empty state saying what is missing, never a bare empty grid `src: User flow states bullet 1`
- [ ] `C-UF-12` `ui` A route loading indicator sits collapsed at rest, reaching an intermediate width, then completing `src: User flow states bullet 2`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The product is dark only, with no theme toggle `src: UI/UX notes Mode`
- [ ] `C-UX-02` `ui` The palette is declared once as custom properties on the document root, consumed by name `src: UI/UX notes Palette by role`
- [ ] `C-UX-03` `ui` Body text is a near-white neutral rather than pure white `src: UI/UX notes Palette by role`
- [ ] `C-UX-04` `ui` The call-to-action gradient runs from a light, vivid orange into a mid, vivid red, worn by nothing else `src: UI/UX notes Palette by role`
- [ ] `C-UX-05` `ui` Success is a mid, soft teal, failure the accent red, in progress a mid, vivid cyan, waiting a light, vivid orange `src: UI/UX notes Palette by role`
- [ ] `C-UX-06` `ui` The conference family is quarantined to the announcement bar `src: UI/UX notes Palette by role`
- [ ] `C-UX-07` `ui` A card carries a hairline inset ring with a warm second inset along its top edge only `src: UI/UX notes The signature`
- [ ] `C-UX-08` `literal` Type is `Geomanist` with `Geomanist Book`, falling back to `geomanist, ui-sans-serif, system-ui, sans-serif` `src: UI/UX notes Type`
- [ ] `C-UX-09` `ui` Colour moves faster than geometry, so colour arrives before the movement finishes `src: UI/UX notes Motion`
- [ ] `C-UX-10` `ui` Two marquee rows run at cycle lengths with no common factor, so the rows never align `src: UI/UX notes Motion`
- [ ] `C-UX-11` `ui` Pointing at the primary action raises a white veil, swinging the gradient direction, with colour stops unmoved `src: UI/UX notes Motion`
- [ ] `C-UX-12` `constraint` No card lifts, grows, bounces when pointed at `src: UI/UX notes Motion`
- [ ] `C-UX-13` `ui` Under reduced motion the marquees stop, the drift stops, reveals render in final state `src: UI/UX notes Motion`
- [ ] `C-UX-14` `ui` A selected tab is marked by a glowing rail down its left side, never an underline `src: UI/UX notes Selection and focus`
- [ ] `C-UX-15` `ui` The focus indicator is a real outline, distinct from hover `src: UI/UX notes Selection and focus`
- [ ] `C-UX-16` `ui` One breakpoint is the real switch, multi-column above, a single stack below `src: UI/UX notes Responsive`
- [ ] `C-UX-17` `ui` At a narrow viewport nothing overflows sideways, every navigation target staying reachable `src: UI/UX notes Responsive`
- [ ] `C-UX-18` `contract` Body text meets WCAG AA contrast against its background `src: UI/UX notes Accessibility`
- [ ] `C-UX-19` `contract` Every icon-only control carries a text alternative `src: UI/UX notes Accessibility`
- [ ] `C-UX-20` `ui` Keyboard navigation reaches every control, with a visible focus ring `src: UI/UX notes Accessibility`
- [ ] `C-UX-21` `contract` Every content image carries alternative text, with decorative images declaring themselves decorative `src: UI/UX notes Accessibility`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The frontend is Preact built with Vite into a production bundle `src: Technical requirements paragraph 1`
- [ ] `C-TR-02` `contract` The backend is Litestar serving JSON on the same origin under the `/api` prefix `src: Technical requirements paragraph 1`
- [ ] `C-TR-03` `literal` Storage is PostgreSQL, read from `DATABASE_URL` `src: Technical requirements paragraph 1`
- [ ] `C-TR-04` `literal` Identity is Keycloak, read from `AUTH_ISSUER_URL`, `AUTH_CLIENT_ID`, `AUTH_CLIENT_SECRET` `src: Technical requirements paragraph 1`
- [ ] `C-TR-05` `literal` The approval deadline in seconds is read from `APPROVAL_DEADLINE_SEC` `src: Technical requirements paragraph 1`
- [ ] `C-TR-06` `literal` The app's address, its port, are read from `APP_PUBLIC_URL`, `APP_PUBLIC_PORT` `src: Technical requirements paragraph 1`
- [ ] `C-TR-07` `constraint` No host, no port, no deadline is hardcoded `src: Technical requirements paragraph 1`
- [ ] `C-TR-08` `constraint` No second database, cache, queue, object store, identity provider, mail vendor is introduced `src: Technical requirements paragraph 2`
- [ ] `C-TR-09` `constraint` Neither backing service is downloaded, installed, compiled, started by the app `src: Technical requirements paragraph 2`
- [ ] `C-TR-10` `contract` `GET /api/health` returns `200` once the app is ready `src: Technical requirements health paragraph`
- [ ] `C-TR-11` `contract` Liveness answers separately from readiness `src: Technical requirements health paragraph`
- [ ] `C-TR-12` `contract` Passwords are stored with a memory-hard hash `src: Technical requirements auth paragraph`
- [ ] `C-TR-13` `contract` Session tokens are invalidated on sign-out, on a role change `src: Technical requirements auth paragraph`
- [ ] `C-TR-14` `contract` Every log record is structured, carrying the run, workflow, project, correlation identifiers `src: Technical requirements logging`
- [ ] `C-TR-15` `constraint` No credential value, no resolved secret, no full step payload appears in a log record `src: Technical requirements logging`
- [ ] `C-TR-16` `capability` Metrics are exposed for scraping across queue depth, worker count, run status counts, durations `src: Technical requirements metrics`
- [ ] `C-TR-17` `capability` Usage insights are accumulated into buckets as runs finish, surviving the pruning of run output `src: Technical requirements insights`
- [ ] `C-TR-18` `contract` Every save produces an immutable version carrying an identifier, an author, a timestamp `src: Technical requirements versioning`
- [ ] `C-TR-19` `capability` Step output is written as steps complete rather than flushed at the end `src: Technical requirements run output`
- [ ] `C-TR-20` `capability` A per-run ceiling on step output fails that one run with a named error `src: Technical requirements run output`
- [ ] `C-TR-21` `capability` Retention is configurable by age, by count, separately for successful, failed runs `src: Technical requirements run output`
- [ ] `C-TR-22` `constraint` Audit records sit outside retention entirely `src: Technical requirements run output`
- [ ] `C-TR-23` `constraint` Binary payloads never enter the database, never enter the queue `src: Technical requirements binary payloads`
- [ ] `C-TR-24` `contract` Operator code runs where the host globals, filesystem, environment, network stack are all out of reach `src: Technical requirements sandbox`
- [ ] `C-TR-25` `contract` Operator code cannot reach the credential store, nor another run's data `src: Technical requirements sandbox`
- [ ] `C-TR-26` `contract` Operator code is bounded by a wall-clock limit, a memory ceiling, enforced from outside `src: Technical requirements sandbox`
- [ ] `C-TR-27` `contract` Operator code receives its input deep-copied rather than shared `src: Technical requirements sandbox`
- [ ] `C-TR-28` `contract` Every outbound request refuses internal address ranges `src: Technical requirements egress`
- [ ] `C-TR-29` `contract` The address is refused after resolution, then again on every redirect `src: Technical requirements egress`
- [ ] `C-TR-30` `contract` Expressions resolve immediately before the step runs, once per item `src: Technical requirements expressions`
- [ ] `C-TR-31` `contract` The run's start instant is fixed for the whole run `src: Technical requirements expressions`
- [ ] `C-TR-32` `contract` An expression error names the step, the field, the expression `src: Technical requirements expressions`
- [ ] `C-TR-33` `contract` Each credential payload is encrypted under its own data key, wrapped by a key-encryption key outside the database `src: Technical requirements credential storage`
- [ ] `C-TR-34` `contract` A ciphertext moved to another credential's row fails to decrypt `src: Technical requirements credential storage`
- [ ] `C-TR-35` `contract` Credential plaintext never reaches run output, logs, the queue `src: Technical requirements credential storage`
- [ ] `C-TR-36` `contract` A workflow definition is validated when saved rather than discovered broken by a run `src: Technical requirements input validation`
- [ ] `C-TR-37` `contract` Every response carries the standard security headers `src: Technical requirements transport`
- [ ] `C-TR-38` `constraint` No credential, interface key, admin token appears in anything the browser downloads `src: Technical requirements isolation`
- [ ] `C-TR-39` `contract` Every query is scoped by project where data is fetched `src: Technical requirements isolation`
- [ ] `C-TR-40` `contract` No binary asset ships: no image file, no video file, no font file is fetched `src: Technical requirements zero-asset`

## C-DM Data model

- [ ] `C-DM-01` `data` All timestamps are UTC `src: Data model opening`
- [ ] `C-DM-02` `literal` Every seeded account uses `deku-demo-pw-2026`, written into `/app/USER_README.md` `src: Data model password paragraph`
- [ ] `C-DM-03` `data` `users` carries `id`, `email` unique, `display_name`, `instance_role`, `created_at` `src: Data model users`
- [ ] `C-DM-04` `data` `runs` carries `status`, `worker_id`, `heartbeat_at`, `idempotency_key`, `workflow_version_id` `src: Data model runs`
- [ ] `C-DM-05` `data` `approvals` carries `decision`, `decided_by_id`, `decided_at`, `deadline_at`, `approve_token`, `reject_token`, `token_used` `src: Data model approvals`
- [ ] `C-DM-06` `data` `audit_events` rows are appended, never changed, never removed `src: Data model audit_events`
- [ ] `C-DM-07` `data` `run_steps` counts `attempt` from `1`, appending a row per retry `src: Data model run_steps`
- [ ] `C-DM-08` `data` A plan's displayed price is derived from the billing period plus the volume tier `src: Data model derived`
- [ ] `C-DM-09` `data` An approval is `expired` when read past its deadline with no decision, derived at read time `src: Data model derived`
- [ ] `C-DM-10` `literal` `runs.status` takes `new`, `running`, `waiting`, `succeeded`, `failed`, `cancelled`, `crashed` `src: Data model values`
- [ ] `C-DM-11` `literal` `approvals.decision` takes `pending`, `approved`, `rejected`, `expired` `src: Data model values`
- [ ] `C-DM-12` `literal` `users.instance_role` takes `operator`, `approver`, `owner` `src: Data model values`
- [ ] `C-DM-13` `constraint` A run carries at most one approval row for a given step name `src: Data model invariants`
- [ ] `C-DM-14` `constraint` A denied mutation leaves the target row byte-for-byte unchanged `src: Data model invariants`
- [ ] `C-DM-15` `constraint` Seeding is idempotent, so restarting the app duplicates no rows `src: Data model seed data`
- [ ] `C-DM-16` `literal` Two projects are seeded: `platform-ops`, `revenue-ops` `src: Data model seed data`
- [ ] `C-DM-17` `literal` Three workflows are seeded: `Incident triage`, `Nightly backup sweep`, `Lead handoff` `src: Data model seed data`
- [ ] `C-DM-18` `literal` `Incident triage` version `1` carries `Webhook trigger`, `Fetch incident`, `Classify impact`, `Wait for approval`, `Post to channel` `src: Data model seed data`
- [ ] `C-DM-19` `data` One seeded run of `Incident triage` sits at `waiting` with a `pending` approval row `src: Data model seed data`
- [ ] `C-DM-20` `data` Thirty connectors are seeded across eight categories `src: Data model seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The announcement bar is a card whose bottom corners are rounded, whose top corners are square `src: Front-end specification announcement bar`
- [ ] `C-FE-02` `literal` The announcement copy reads `Convergence 2026, Lisbon, October 14. Early bird tickets are now on sale.` `src: Front-end specification announcement bar`
- [ ] `C-FE-03` `ui` The header is fixed, changing nothing at all on scroll `src: Front-end specification header`
- [ ] `C-FE-04` `literal` The six navigation entries read `Product`, `Use cases`, `Docs`, `Community`, `Enterprise`, `Pricing` `src: Front-end specification header`
- [ ] `C-FE-05` `ui` A panel opens on pointer with intent, on click, on Enter, closing on Escape `src: Front-end specification header`
- [ ] `C-FE-06` `ui` The footer glow is masked at its top edge, reaching full strength a fifth of the way down `src: Front-end specification footer`
- [ ] `C-FE-07` `literal` The footer tagline reads `Automate without limits` `src: Front-end specification footer`
- [ ] `C-FE-08` `ui` Every icon is geometry drawn inline, never a font, never a fetched file `src: Front-end specification iconography`
- [ ] `C-FE-09` `ui` One card component carries eight background variants `src: Front-end specification components`
- [ ] `C-FE-10` `ui` The button has three gradient variants, each carrying a transparent veil layer at rest `src: Front-end specification components`
- [ ] `C-FE-11` `ui` The home hero headline runs over two lines, the first naming the product's subject, the second naming the control a reader keeps `src: Front-end specification home hero`
- [ ] `C-FE-12` `ui` The home hero sets its first line light, its second normal `src: Front-end specification home hero`
- [ ] `C-FE-13` `literal` The catalogue search placeholder reads `Search for workflows, nodes, tasks...` `src: Front-end specification catalogue`
- [ ] `C-FE-14` `ui` The enterprise route offers no trial action `src: Front-end specification enterprise`
- [ ] `C-FE-15` `ui` The not-found route renders with no announcement bar, no header, no footer `src: Front-end specification not found`
- [ ] `C-FE-16` `literal` The not-found headline reads `Ooops...` followed by `error 404` `src: Front-end specification not found`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` There is no organisation above a project, no cross-installation federation `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` There is no public signup, no password reset, no email of any kind `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` The plan table sells without charging, so no payment capture exists `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` No third-party analytics, consent vendor, error reporter, flag service is called at run time `src: Constraints bullet 4`
- [ ] `C-CN-05` `constraint` No file upload from the browser exists `src: Constraints bullet 8`
- [ ] `C-CN-06` `constraint` The app stays responsive at two projects, three workflows, thirty connectors, five hundred runs `src: Constraints final bullet`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`, read from the environment `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on that same origin under the `/api` prefix `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps `src: Deployment contract bullet 4`
- [ ] `C-DC-05` `contract` Login credentials are written to `/app/USER_README.md` `src: Deployment contract bullet 5`
- [ ] `C-DC-06` `contract` Reserved `.browser_screenshots/`, `.downloads/` directories exist at the app root, empty `src: Deployment contract bullet 6`
- [ ] `C-DC-07` `contract` A production build is served behind a static or preview server, never a dev server `src: Deployment contract bullet 7`
- [ ] `C-DC-08` `contract` The server keeps running after the session ends, never as a child of the shell `src: Deployment contract bullet 8`
- [ ] `C-DC-09` `contract` The server binds `0.0.0.0`, never `127.0.0.1` `src: Deployment contract bullet 9`
- [ ] `C-DC-10` `constraint` No persistent volumes, no fixed container names, no custom networks are used `src: Deployment contract bullet 12`
- [ ] `C-DC-11` `contract` `POST /api/auth/login` takes an email with a password, returning `access_token` `src: Deployment contract API shapes`
- [ ] `C-DC-12` `contract` `POST /api/approvals/<id>/decision` records a decision of `approved` or `rejected` `src: Deployment contract API shapes`
- [ ] `C-DC-13` `contract` `GET /api/connectors` returns a total, a page, a page size, results, facets `src: Deployment contract API shapes`
- [ ] `C-DC-14` `contract` List endpoints marked as such return a top-level JSON array `src: Deployment contract API shapes`
- [ ] `C-DC-15` `contract` An invalid or unauthorized call is rejected as a client error, never as a server error `src: Deployment contract API shapes`
- [ ] `C-DC-16` `constraint` An in-memory list of runs, a hardcoded approvals payload, a module-level workflow dictionary are contract violations `src: Deployment contract No mocks`

---

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `owner@example.com` | the seeded owner account | `C-RL-12` |
| `approver@example.com` | the seeded approver in Platform Ops | `C-RL-12` |
| `approver2@example.com` | the seeded approver in Revenue Ops | `C-RL-12` |
| `operator@example.com` | the seeded operator in Platform Ops | `C-RL-12` |
| `operator2@example.com` | the seeded operator in Revenue Ops | `C-RL-12` |
| `deku-demo-pw-2026` | the corpus password | `C-RL-13` |
| `Starter` | the first plan | `C-CF-66` |
| `Pro` | the second plan | `C-CF-66` |
| `Business` | the third plan | `C-CF-66` |
| `Enterprise` | the fourth plan | `C-CF-66` |
| `2900` | Starter monthly, minor units | `C-CF-68` |
| `2400` | Starter annual, minor units | `C-CF-68` |
| `7200` | Pro monthly, minor units | `C-CF-69` |
| `6000` | Pro annual, minor units | `C-CF-69` |
| `80000` | Business monthly, minor units | `C-CF-70` |
| `66700` | Business annual, minor units | `C-CF-70` |
| `2500` | Starter included executions | `C-CF-71` |
| `10000` | Pro included executions | `C-CF-71` |
| `40000` | Business included executions | `C-CF-71` |
| `Contact Sales` | the fourth column's price slot | `C-CF-73` |
| `24` | the catalogue default page size | `C-CF-80` |
| `60` | the catalogue maximum page size | `C-CF-80` |
| `integrations` | the word after the catalogue count | `C-CF-77` |
| `Popularity` | the default catalogue sort | `C-CF-76` |
| `Geomanist` | the interface typeface | `C-UX-08` |
| `Geomanist Book` | the second face | `C-UX-08` |
| `geomanist, ui-sans-serif, system-ui, sans-serif` | the fallback stack | `C-UX-08` |
| `DATABASE_URL` | the datastore address | `C-TR-03` |
| `AUTH_ISSUER_URL` | the identity issuer | `C-TR-04` |
| `AUTH_CLIENT_ID` | the identity client | `C-TR-04` |
| `AUTH_CLIENT_SECRET` | the identity client secret | `C-TR-04` |
| `APPROVAL_DEADLINE_SEC` | the approval deadline in seconds | `C-TR-05` |
| `APP_PUBLIC_URL` | the app's public address | `C-TR-06` |
| `APP_PUBLIC_PORT` | the app's public port | `C-TR-06` |
| `/app/USER_README.md` | the credential file | `C-DM-02` |
| `new` | a run just created | `C-DM-10` |
| `running` | a run a worker holds | `C-DM-10` |
| `waiting` | a run paused for a person | `C-DM-10` |
| `succeeded` | a run that finished cleanly | `C-DM-10` |
| `failed` | a run that did not | `C-DM-10` |
| `cancelled` | a run stopped by a person | `C-DM-10` |
| `crashed` | a run whose worker went away | `C-DM-10` |
| `pending` | an approval nobody decided yet | `C-DM-11` |
| `approved` | an approval allowed | `C-DM-11` |
| `rejected` | an approval refused | `C-DM-11` |
| `expired` | an approval past its deadline | `C-DM-11` |
| `operator` | the lowest role | `C-DM-12` |
| `approver` | the deciding role | `C-DM-12` |
| `owner` | the administering role | `C-DM-12` |
| `platform-ops` | the first seeded project | `C-DM-16` |
| `revenue-ops` | the second seeded project | `C-DM-16` |
| `Incident triage` | the seeded workflow carrying an approval step | `C-DM-17` |
| `Nightly backup sweep` | the inactive seeded workflow | `C-DM-17` |
| `Lead handoff` | the Revenue Ops workflow | `C-DM-17` |
| `1` | the seeded workflow version number | `C-DM-18` |
| `Webhook trigger` | the first seeded step | `C-DM-18` |
| `Fetch incident` | the second seeded step | `C-DM-18` |
| `Classify impact` | the third seeded step | `C-DM-18` |
| `Wait for approval` | the approval step | `C-DM-18` |
| `Post to channel` | the final seeded step | `C-DM-18` |
| `Convergence 2026, Lisbon, October 14. Early bird tickets are now on sale.` | the announcement copy | `C-FE-02` |
| `Product` | the first navigation entry | `C-FE-04` |
| `Use cases` | the second navigation entry | `C-FE-04` |
| `Docs` | the third navigation entry | `C-FE-04` |
| `Community` | the fourth navigation entry | `C-FE-04` |
| `Automate without limits` | the footer tagline | `C-FE-07` |
| `AI agents and workflows` | the hero's first line | `C-FE-11` |
| `you can see and control` | the hero's second line | `C-FE-11` |
| `Search for workflows, nodes, tasks...` | the catalogue placeholder | `C-FE-13` |
| `Ooops...` | the not-found headline | `C-FE-16` |
| `error 404` | the not-found headline's second half | `C-FE-16` |
| `${APP_PUBLIC_PORT}:4173` | the port mapping | `C-DC-02` |
| `/api` | the interface prefix | `C-DC-03` |
| `.browser_screenshots/` | the reserved screenshot directory | `C-DC-06` |
| `.downloads/` | the reserved download directory | `C-DC-06` |
| `0.0.0.0` | the bind address | `C-DC-09` |
| `127.0.0.1` | the address never bound | `C-DC-09` |
| `200` | the health response | `C-TR-10` |
| `continue_error_output` | the on-error value routing to a second output | `C-CF-29` |
| `skipped` | a step on an untaken branch | `C-CF-27` |
| `runs.status` | the run state column | `C-DM-10` |
| `approvals.decision` | the approval outcome column | `C-DM-11` |
| `users.instance_role` | the role column | `C-DM-12` |
| `Pricing` | the sixth navigation entry | `C-FE-04` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the loop iteration ceiling | `C-CF-30` |
| the maximum run duration | `C-CF-33` |
| the heartbeat threshold before a run is marked crashed | `C-CF-51` |
| the bounded redelivery count | `C-CF-54` |
| the agent iteration, token, duration ceilings | `C-CF-57` |
| the per-run step-output ceiling | `C-TR-20` |

---

## Coverage ledger

| Section | Obligation sentences | Items |
|---|---|---|
| Overview | 5 | 6 |
| User roles | 4 | 14 |
| Core features | 22 | 95 |
| User flow | 8 | 12 |
| UI and UX notes | 8 | 21 |
| Technical requirements | 26 | 40 |
| Data model | 11 | 20 |
| Front-end specification | 9 | 16 |
| Constraints | 2 | 6 |
| Deployment contract | 10 | 16 |
