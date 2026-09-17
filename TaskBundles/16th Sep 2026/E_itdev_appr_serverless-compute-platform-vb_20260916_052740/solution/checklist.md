# Checklist: Vireo Console

Items: 225
Unpinned values flagged: 3
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-BP, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` The product presents a governed operator console for a serverless compute platform, with a public product page over the console. `src: Overview`
- [ ] `C-OV-02` `capability` A member opens an app, reads live container health, files a request to promote a version to the production environment. `src: Overview`
- [ ] `C-OV-03` `constraint` A request to promote a version to production is decided by a second member who is not the requester. `src: Overview`
- [ ] `C-OV-04` `constraint` Approval of a promotion request changes no app until a separate apply step runs. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` The stored role set is `owner`, `administrator`, `developer`, `operator`, `billing`, `read-only`. `src: User roles`
- [ ] `C-RL-02` `role` A member holding `owner` reaches billing, quotas, workspace settings, the two-person rule setting. `src: User roles`
- [ ] `C-RL-03` `role` A member holding `administrator` manages members, roles, grants, environments, quotas. `src: User roles`
- [ ] `C-RL-04` `role` A member holding `developer` deploys in a development environment, files a request for any production change. `src: User roles`
- [ ] `C-RL-05` `role` A member holding `operator` decides a promotion request, rolls back in production, terminates a container. `src: User roles`
- [ ] `C-RL-06` `role` A member holding `billing` reaches usage, budgets, quota requests, nothing touching code. `src: User roles`
- [ ] `C-RL-07` `role` A member holding `read-only` reads apps, functions, containers, metrics, own audit entries. `src: User roles`
- [ ] `C-RL-08` `constraint` A member holding `read-only` requesting a log body receives `403`. `src: User roles`
- [ ] `C-RL-09` `contract` Authorization is enforced server-side on every mutating endpoint. `src: User roles`
- [ ] `C-RL-10` `contract` A direct API call from a `developer` session against an `operator`-only endpoint receives `401` or `403`. `src: User roles`
- [ ] `C-RL-11` `constraint` No public registration form exists on any route. `src: User roles`
- [ ] `C-RL-12` `data` A member is deactivated rather than removed from storage. `src: User roles`
- [ ] `C-RL-13` `constraint` The last member holding `owner` in a workspace cannot be demoted. `src: User roles`
- [ ] `C-RL-14` `constraint` The last member holding `owner` in a workspace cannot be deactivated. `src: User roles`
- [ ] `C-RL-15` `ui` A navigation item a member has no permission on is hidden rather than disabled. `src: User roles`
- [ ] `C-RL-16` `ui` The audit route is visible to every member for their own actions. `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `capability` A seeded principal signs in with an email address, a password, reaching the workspace overview. `src: Core features 1`
- [ ] `C-CF-02` `contract` A sign-in with a wrong password receives `401`. `src: Core features 1`
- [ ] `C-CF-03` `contract` A sign-in failure message does not disclose which half of the pair was wrong. `src: Core features 1`
- [ ] `C-CF-04` `contract` A console endpoint called with no session receives `401`. `src: Core features 1`
- [ ] `C-CF-05` `contract` Every console route carries the workspace before the environment, the environment before the resource. `src: Core features 2`
- [ ] `C-CF-06` `contract` A resource requested in a workspace the principal is not a live member of receives `404`. `src: Core features 2`
- [ ] `C-CF-07` `contract` A resource requested in an environment the member may not read receives `403`. `src: Core features 2`
- [ ] `C-CF-08` `ui` The apps list shows name, state, current version, function count, live container count, error rate, spend rate, last deploy. `src: Core features 3`
- [ ] `C-CF-09` `data` An app state is one of `live`, `stopped`, `deploying`, `failed`, `ephemeral-running`. `src: Core features 3`
- [ ] `C-CF-10` `ui` The app detail route carries a separate linkable route per tab for overview, functions, deployments, logs, containers, settings. `src: Core features 3`
- [ ] `C-CF-11` `ui` An empty apps list states what would appear, why nothing appears, the one action that would change the state. `src: Core features 3`
- [ ] `C-CF-12` `ui` The containers surface lists identifier, function, version, state, age, accelerator class, memory, processor, utilisation, tasks served. `src: Core features 4`
- [ ] `C-CF-13` `data` A container state is one of `starting`, `ready`, `running`, `idle`, `draining`, `terminated`, `failed`. `src: Core features 4`
- [ ] `C-CF-14` `literal` A terminated container carries an exit reason from the closed set `completed`, `idle-scaledown`, `deploy-superseded`, `customer-terminated`, `customer-code-error`, `out-of-memory`, `timeout`, `preempted`, `worker-lost`, `platform-error`, `quota-exceeded`, `policy-denied`. `src: Core features 4`
- [ ] `C-CF-15` `contract` A write setting a container exit reason outside the closed set receives `422`. `src: Core features 4`
- [ ] `C-CF-16` `ui` A container whose exit reason is `out-of-memory` shows the memory limit beside the observed peak. `src: Core features 4`
- [ ] `C-CF-17` `ui` A container whose exit reason is `timeout` shows the configured timeout beside the elapsed time. `src: Core features 4`
- [ ] `C-CF-18` `data` A container whose exit reason is `worker-lost` is excluded from the customer error rate. `src: Core features 4`
- [ ] `C-CF-19` `data` A container whose exit reason is `platform-error` is excluded from the customer error rate. `src: Core features 4`
- [ ] `C-CF-20` `capability` A member holding `developer` files a request to promote a chosen version to the production environment. `src: Core features 5`
- [ ] `C-CF-21` `data` A promotion request is created in `draft`, moves to `submitted` on filing, moves to `in-review` on routing. `src: Core features 5`
- [ ] `C-CF-22` `contract` A promotion request filed with an empty reason receives `422`, naming the field. `src: Core features 5`
- [ ] `C-CF-23` `contract` A member holding `developer` calling the promote endpoint directly receives `403`. `src: Core features 5`
- [ ] `C-CF-24` `data` A refused direct promote leaves the live version of the app unchanged. `src: Core features 5`
- [ ] `C-CF-25` `capability` A member holding `operator` decides a promotion request that sits in `in-review`, supplying a reason. `src: Core features 6`
- [ ] `C-CF-26` `contract` A decision recorded with an empty reason receives `422`. `src: Core features 6`
- [ ] `C-CF-27` `ui` The decision reason is shown to the requester on the request detail route. `src: Core features 6`
- [ ] `C-CF-28` `data` A promotion request state is one of `draft`, `submitted`, `in-review`, `approved`, `rejected`, `withdrawn`, `expired`, `applied`, `failed-to-apply`. `src: Core features 6`
- [ ] `C-CF-29` `contract` A member holding `developer` calling the decide endpoint receives `403`. `src: Core features 6`
- [ ] `C-CF-30` `data` A promotion request refused for role carries the same state, decider, decision reason after the refusal. `src: Core features 6`
- [ ] `C-CF-31` `contract` The requester calling the decide endpoint on their own request receives `403`. `src: Core features 6`
- [ ] `C-CF-32` `data` A promotion request refused for separation of duties carries the same state, decider, decision reason after the refusal. `src: Core features 6`
- [ ] `C-CF-33` `contract` A decision on a promotion request outside `in-review` receives `409`, naming the current state. `src: Core features 6`
- [ ] `C-CF-34` `contract` A second decision arriving against an already decided promotion request receives `409`. `src: Core features 6`
- [ ] `C-CF-35` `contract` A transition the promotion state machine does not allow receives `422`. `src: Core features 6`
- [ ] `C-CF-36` `contract` Approval of a promotion request changes no app version. `src: Core features 7`
- [ ] `C-CF-37` `capability` A separate apply step promotes the requested version, moving the request to `applied`. `src: Core features 7`
- [ ] `C-CF-38` `data` An applied promotion request changes the live version of the app to the requested version. `src: Core features 7`
- [ ] `C-CF-39` `data` A promotion request whose apply fails reaches `failed-to-apply`, stating a reason. `src: Core features 7`
- [ ] `C-CF-40` `data` A promotion request whose apply fails leaves the previous version live. `src: Core features 7`
- [ ] `C-CF-41` `capability` A member holding `operator` rolls a production app back from the deployments list, supplying a reason. `src: Core features 8`
- [ ] `C-CF-42` `contract` A rollback recorded with no reason receives `422`. `src: Core features 8`
- [ ] `C-CF-43` `data` A rollback creates a new version pointing at the previous artifact. `src: Core features 8`
- [ ] `C-CF-44` `data` A superseded version remains readable after a rollback, with the health of the version. `src: Core features 8`
- [ ] `C-CF-45` `data` A deploy state is one of `requested`, `building`, `built`, `switching`, `live`, `failed`, `rolled-back`. `src: Core features 8`
- [ ] `C-CF-46` `capability` A secret is created with a name, a description, key pairs, value pairs. `src: Core features 10`
- [ ] `C-CF-47` `data` A secret is granted to an app, a function, an environment, never to a principal. `src: Core features 10`
- [ ] `C-CF-48` `constraint` No endpoint, for any role, returns a secret value. `src: Core features 10`
- [ ] `C-CF-49` `ui` The secrets surface shows key names, value lengths, nothing further. `src: Core features 10`
- [ ] `C-CF-50` `data` Updating a secret creates a new version, leaving running containers on the version started with. `src: Core features 10`
- [ ] `C-CF-51` `contract` Deleting a secret a live deployment references receives `409`, naming the referencing functions. `src: Core features 10`
- [ ] `C-CF-52` `capability` A machine token is created with a name, a scope set, a binding to one environment. `src: Core features 11`
- [ ] `C-CF-53` `ui` The token secret is shown exactly once, behind an explicit acknowledgement. `src: Core features 11`
- [ ] `C-CF-54` `constraint` No route returns a token secret after the creation dialog closes. `src: Core features 11`
- [ ] `C-CF-55` `data` A machine token state is one of `live`, `superseded`, `expired`, `revoked`, `disabled`. `src: Core features 11`
- [ ] `C-CF-56` `contract` A member holding `developer` revoking a token created by another principal receives `403`. `src: Core features 11`
- [ ] `C-CF-57` `data` A machine token created by a deactivated principal is disabled rather than removed. `src: Core features 11`
- [ ] `C-CF-58` `contract` A log query with no bound receives `422`, stating the narrowing that would be accepted. `src: Core features 12`
- [ ] `C-CF-59` `data` Log search defaults to the current environment, to the last hour. `src: Core features 12`
- [ ] `C-CF-60` `data` Every log line carries task, container, function, app, environment, source. `src: Core features 12`
- [ ] `C-CF-61` `constraint` A secret value is scrubbed from a log body. `src: Core features 12`
- [ ] `C-CF-62` `ui` Lines dropped by a rate limit are marked in the stream with the count, the window. `src: Core features 12`
- [ ] `C-CF-63` `literal` A waiting task carries a reason from the closed set `no capacity in region`, `workspace concurrency limit reached`, `accelerator quota reached`, `function maximum containers reached`, `cold start in progress`, `workspace on hold`. `src: Core features 12`
- [ ] `C-CF-64` `ui` Each waiting reason is shown beside the specific action that would resolve the wait. `src: Core features 12`
- [ ] `C-CF-65` `data` Every metered quantity is stored as an integer in a base unit, per task, per container. `src: Core features 13`
- [ ] `C-CF-66` `ui` Container idle time is shown as a separate line beside serving time. `src: Core features 13`
- [ ] `C-CF-67` `ui` Every figure on the usage route links through to the tasks behind the figure. `src: Core features 13`
- [ ] `C-CF-68` `ui` Every quota shows consumption against a limit, with a request-increase path linked. `src: Core features 13`
- [ ] `C-CF-69` `data` A hard spend cap refuses new work, allowing running work to finish. `src: Core features 13`
- [ ] `C-CF-70` `data` Every state transition is recorded with principal, action, resource, before value, after value, request identifier. `src: Core features 14`
- [ ] `C-CF-71` `contract` An update against a stored audit entry receives `403`. `src: Core features 14`
- [ ] `C-CF-72` `contract` A delete against a stored audit entry receives `403`. `src: Core features 14`
- [ ] `C-CF-73` `data` A stored audit entry is unchanged after a refused update. `src: Core features 14`
- [ ] `C-CF-74` `ui` A task links to the container of the task, to the log lines of the task, to the metrics window of the task. `src: Core features 15`
- [ ] `C-CF-75` `ui` Every figure on the overview links to the filtered list behind the figure. `src: Core features 15`
- [ ] `C-CF-76` `ui` A list filter is encoded in the route, making a filtered view a shareable link. `src: Core features 15`
- [ ] `C-CF-77` `ui` A destructive confirmation names the exact resource, requiring the name typed in a production environment. `src: Core features 15`
- [ ] `C-CF-78` `capability` A privacy page is reachable from the footer of every public page. `src: Core features 16`
- [ ] `C-CF-79` `ui` The privacy page states what the platform records about a workspace, how long each record is kept. `src: Core features 16`
- [ ] `C-CF-80` `capability` An unknown address renders the product's own not-found page, carrying a way back. `src: Core features 17`
- [ ] `C-CF-81` `contract` An unknown address responds with `404`. `src: Core features 17`
- [ ] `C-CF-82` `ui` Every form validates on blur, naming the field at fault, naming the fix. `src: Core features 18`
- [ ] `C-CF-83` `data` A refused form writes nothing, leaving the stored record unchanged. `src: Core features 18`

## C-UF User flow

- [ ] `C-UF-01` `ui` Navigation is a breadcrumbed drill-down from workspace, to environment, to resource, to tab. `src: User flow`
- [ ] `C-UF-02` `ui` Selecting a row opens a detail pane beside the list rather than replacing the list. `src: User flow`
- [ ] `C-UF-03` `ui` Creating a record opens a modal over the current route. `src: User flow`
- [ ] `C-UF-04` `ui` Feedback appears as an inline banner at the top of the affected region. `src: User flow`
- [ ] `C-UF-05` `capability` The route `/login` is reachable without a session. `src: User flow`
- [ ] `C-UF-06` `capability` The route `/privacy` is reachable without a session. `src: User flow`
- [ ] `C-UF-07` `ui` A member holding `developer` viewing their own promotion request sees no decision control. `src: User flow`
- [ ] `C-UF-08` `ui` A suspended workspace keeps reads working, disabling every mutating control behind one explanation. `src: User flow`
- [ ] `C-UF-09` `ui` A permission denial names the missing permission, names the role holding the permission, naming no individual. `src: User flow`
- [ ] `C-UF-10` `ui` Each region of the shell skeletons independently, leaving the rail rendered. `src: User flow`
- [ ] `C-UF-11` `ui` An empty workspace shows the first-deploy path rather than empty charts. `src: User flow`
- [ ] `C-UF-12` `ui` Navigating away from a dirty form raises a warning. `src: User flow`
- [ ] `C-UF-13` `ui` Every error surface shows a request identifier with a copy control. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The interface is dark by default, carrying no light theme. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The page ground is a near-black neutral, with cards on a deep neutral, separators on a mid neutral. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Body copy on a dark ground is a near-white green rather than white. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` One vivid green accent is spent on the primary action, a highlighted headline word, an icon that must be found, a live indicator. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Secondary copy fades along a green axis toward a muted green rather than toward grey. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Every state carries an icon, a word, beside the hue of the state. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Status hues run from a soft red, a soft amber, a vivid orange, a soft blue, with a light magenta reserved for platform faults. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Charts use a categorical set of a light green, a soft orange, a light magenta, a mid teal, a soft amber, a mid green, a soft blue, a deep red. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Annotation layers use a near-white muted violet, a light soft cyan. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Hover on a dark control is a low white overlay rather than a lighter opaque grey. `src: UI/UX notes`
- [ ] `C-UX-11` `literal` Body copy across the console is set in `Inter Variable`. `src: UI/UX notes`
- [ ] `C-UX-12` `literal` Eyebrow labels, code, keyboard hints, every figure in a table are set in `Fira Mono`. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Motion uses one easing for a change in place, one easing for an arrival. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` The corner radius of a pill control changes shape on press, overshooting, settling visibly. `src: UI/UX notes`
- [ ] `C-UX-15` `ui` Reduced motion is honoured on every effect, leaving the loader spinning, leaving the pulsing skeleton pulsing. `src: UI/UX notes`
- [ ] `C-UX-16` `ui` Body text meets WCAG AA contrast against the ground of the text. `src: UI/UX notes`
- [ ] `C-UX-17` `ui` Every interactive element carries a visible focus ring under keyboard operation. `src: UI/UX notes`
- [ ] `C-UX-18` `ui` An icon-only control carries a label. `src: UI/UX notes`
- [ ] `C-UX-19` `ui` Meaning is never carried by colour alone. `src: UI/UX notes`
- [ ] `C-UX-20` `ui` Every content image carries alternative text, with a decorative image declaring the decorative role. `src: UI/UX notes`
- [ ] `C-UX-21` `ui` The page carries a banner landmark, a navigation landmark, a main landmark, a footer landmark. `src: UI/UX notes`
- [ ] `C-UX-22` `ui` Headings descend in order without skipping a level. `src: UI/UX notes`
- [ ] `C-UX-23` `ui` A modal traps focus, returning focus to the control that opened the modal. `src: UI/UX notes`
- [ ] `C-UX-24` `ui` At a narrow viewport the rail collapses to icons carrying tooltips. `src: UI/UX notes`
- [ ] `C-UX-25` `ui` At a narrow viewport nothing overflows sideways, leaving every navigation target reachable. `src: UI/UX notes`
- [ ] `C-UX-26` `ui` Figures in a table are monospaced, thousands separated, carrying a currency where money. `src: UI/UX notes`
- [ ] `C-UX-27` `ui` Times are absolute in the member zone with the zone named, with a relative time as a secondary label. `src: UI/UX notes`
- [ ] `C-UX-28` `ui` An identifier is shown in full with a copy control. `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `capability` Every route is rendered on the server, with interactive islands hydrating the streaming regions. `src: Technical requirements`
- [ ] `C-TR-02` `contract` The HTTP API is served on the app origin under the `/api` prefix. `src: Technical requirements`
- [ ] `C-TR-03` `literal` The datastore is reachable at `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-04` `literal` The datastore is reachable at `DB_URL`, carrying the value of `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-05` `literal` The identity provider is reachable at `AUTH_URL`. `src: Technical requirements`
- [ ] `C-TR-06` `constraint` No backing service named in the brief is downloaded, installed, compiled, started by the build. `src: Technical requirements`
- [ ] `C-TR-07` `capability` A session is carried by a bearer token issued on sign-in. `src: Technical requirements`
- [ ] `C-TR-08` `contract` Authorisation is answered by one decision point taking principal, action, resource reference, context. `src: Technical requirements`
- [ ] `C-TR-09` `contract` The authorisation default is deny, with an explicit deny beating every allow. `src: Technical requirements`
- [ ] `C-TR-10` `constraint` No permission returning a secret value exists in the permission vocabulary. `src: Technical requirements`
- [ ] `C-TR-11` `contract` A read path scoped by no workspace returns no row rather than every row. `src: Technical requirements`
- [ ] `C-TR-12` `contract` The workspace of a read is taken from the authenticated principal rather than from a caller parameter. `src: Technical requirements`
- [ ] `C-TR-13` `data` A decision denied for a lapsed grant leaves running work running. `src: Technical requirements`
- [ ] `C-TR-14` `contract` A denial for missing elevation is distinguishable from a plain denial. `src: Technical requirements`
- [ ] `C-TR-15` `constraint` No credential appears in rendered markup, in a client bundle, in a JSON payload, in an inline script. `src: Technical requirements`
- [ ] `C-TR-16` `contract` Every public route carries an own title, an own description. `src: Technical requirements`
- [ ] `C-TR-17` `contract` Every public route declares a social preview title, a social preview image that resolves. `src: Technical requirements`
- [ ] `C-TR-18` `contract` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements`
- [ ] `C-TR-19` `data` Filing the same promotion request twice from a double submission produces one request. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` A `principal` carries email, display name, status of `active`, `invited`, `deactivated`. `src: Data model`
- [ ] `C-DM-02` `data` A `workspace` carries name, slug, default environment, a two-person rule setting. `src: Data model`
- [ ] `C-DM-03` `data` An `environment` carries a kind of `development`, `staging`, `production`. `src: Data model`
- [ ] `C-DM-04` `data` A `deploy_request` carries workspace, source environment, target environment, app, requested version, requester, state, reason, decider, decision time, decision reason, applied version, row version. `src: Data model`
- [ ] `C-DM-05` `data` Every row carries the workspace of the row. `src: Data model`
- [ ] `C-DM-06` `constraint` A read answering for one workspace returns no row belonging to another workspace. `src: Data model`
- [ ] `C-DM-07` `constraint` A production `app_version` becomes live only through an applied `deploy_request`. `src: Data model`
- [ ] `C-DM-08` `constraint` A `deploy_request` requester is never equal to the decider of the same request. `src: Data model`
- [ ] `C-DM-09` `constraint` Only a membership whose role is `operator` or `owner` is recorded as a decider. `src: Data model`
- [ ] `C-DM-10` `data` A `deploy_request` row version changes on every transition. `src: Data model`
- [ ] `C-DM-11` `constraint` An `audit_entry` row is inserted, never updated, never removed. `src: Data model`
- [ ] `C-DM-12` `constraint` A workspace always carries at least one active membership whose role is `owner`. `src: Data model`
- [ ] `C-DM-13` `data` Seeding runs again without duplicating a row. `src: Data model`
- [ ] `C-DM-14` `literal` The seeded workspace is named `Vireo Research`, with slug `vireo-research`. `src: Data model`
- [ ] `C-DM-15` `literal` The seeded environments are `development`, `production`. `src: Data model`
- [ ] `C-DM-16` `literal` The seeded principal `owner@example.com` holds the role `owner`. `src: Data model`
- [ ] `C-DM-17` `literal` The seeded principal `operator@example.com` holds the role `operator`. `src: Data model`
- [ ] `C-DM-18` `literal` The seeded principal `operator2@example.com` holds the role `operator`. `src: Data model`
- [ ] `C-DM-19` `literal` The seeded principal `developer@example.com` holds the role `developer`. `src: Data model`
- [ ] `C-DM-20` `literal` The seeded principal `developer2@example.com` holds the role `developer`. `src: Data model`
- [ ] `C-DM-21` `literal` The seeded principal `readonly@example.com` holds the role `read-only`. `src: Data model`
- [ ] `C-DM-22` `literal` Every seeded principal signs in with the password `deku-demo-pw-2026`. `src: Data model`
- [ ] `C-DM-23` `literal` The seeded apps are named `Nova Inference`, `Atlas Batch`. `src: Data model`
- [ ] `C-DM-24` `literal` The seeded functions are named `embed`, `rerank`, `nightly-rollup`. `src: Data model`
- [ ] `C-DM-25` `data` The seeded app `Nova Inference` in production carries three versions, with the second live, the third built. `src: Data model`
- [ ] `C-DM-26` `data` Seeded containers exist against the live version, with two terminated, one carrying `out-of-memory`, one carrying `worker-lost`. `src: Data model`
- [ ] `C-DM-27` `literal` Money is recorded in integer minor units in `usd`. `src: Data model`
- [ ] `C-DM-28` `data` Every stored time is UTC. `src: Data model`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The palette is authored as a raw layer naming physical ramps, a semantic layer naming ramps by job. `src: Front-end specification`
- [ ] `C-FE-02` `ui` A component references the semantic layer rather than a raw token. `src: Front-end specification`
- [ ] `C-FE-03` `ui` The neutral ramp carries fifteen steps, with five below the mid neutral used for separators. `src: Front-end specification`
- [ ] `C-FE-04` `ui` Three green ramps carry three jobs: accent, body copy on dark grounds, de-emphasis. `src: Front-end specification`
- [ ] `C-FE-05` `ui` Hover on a dark ground uses a transparent white overlay, with a stronger overlay for a pressed state. `src: Front-end specification`
- [ ] `C-FE-06` `ui` A tinted transparent ground sits under a positive state, another under an error state. `src: Front-end specification`
- [ ] `C-FE-07` `ui` Seven radius steps run from a hairline on a dense control to a generous step on a card, with a pill for chrome controls. `src: Front-end specification`
- [ ] `C-FE-08` `ui` The interface is set in medium by default, reserving regular for long prose. `src: Front-end specification`
- [ ] `C-FE-09` `ui` Four breakpoints run at small, medium, large, extra-large, with one spacing unit every gap is a multiple of. `src: Front-end specification`
- [ ] `C-FE-10` `ui` A wait under the perceptual floor renders nothing rather than a skeleton. `src: Front-end specification`
- [ ] `C-FE-11` `ui` A production environment carries a persistent non-dismissible marker in the top bar. `src: Front-end specification`
- [ ] `C-FE-12` `ui` The production marker is a shape, a label, beside a colour. `src: Front-end specification`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No light theme is built. `src: Constraints`
- [ ] `C-CN-02` `constraint` A value outside a closed vocabulary is refused rather than stored. `src: Constraints`
- [ ] `C-CN-03` `constraint` The documentation application, the client library, the command line are not built. `src: Constraints`
- [ ] `C-CN-04` `constraint` Single sign-on, directory provisioning, the payment provider are not built. `src: Constraints`

## C-BP Build plan

- [ ] `C-BP-01` `capability` Schema, seed, `GET /api/health` land before any console route. `src: Build plan`
- [ ] `C-BP-02` `capability` Session, the single decision point land before the console shell. `src: Build plan`
- [ ] `C-BP-03` `capability` The console shell, breadcrumbed routes, the environment switcher land before apps. `src: Build plan`
- [ ] `C-BP-04` `capability` Apps, versions, containers, the closed exit vocabulary land before promotion requests. `src: Build plan`
- [ ] `C-BP-05` `capability` Promotion requests, the state machine land before separation of duties. `src: Build plan`
- [ ] `C-BP-06` `capability` Separation of duties, the role gate land before the remaining surfaces. `src: Build plan`
- [ ] `C-BP-07` `capability` Rollback, secrets, tokens, logs, usage, quotas, audit land before the public page. `src: Build plan`
- [ ] `C-BP-08` `capability` The public page, the privacy page, the not-found page, form validation, the social preview land last. `src: Build plan`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract`
- [ ] `C-DC-03` `contract` The container-internal port is `4173`, read from the environment rather than hardcoded. `src: Deployment contract`
- [ ] `C-DC-04` `contract` The HTTP API is served on the app origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-05` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-07` `contract` A production build is served behind a static server or a preview server. `src: Deployment contract`
- [ ] `C-DC-08` `contract` The server keeps running after the session ends, running outside the shell as a non-child process. `src: Deployment contract`
- [ ] `C-DC-09` `contract` The server binds `0.0.0.0` rather than `127.0.0.1` or `localhost`. `src: Deployment contract`
- [ ] `C-DC-10` `contract` The backing services named in the brief are already running, reachable at the environment variables of the services. `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `completed` | Core features 4 | `C-CF-14` |
| `idle-scaledown` | Core features 4 | `C-CF-14` |
| `deploy-superseded` | Core features 4 | `C-CF-14` |
| `customer-terminated` | Core features 4 | `C-CF-14` |
| `customer-code-error` | Core features 4 | `C-CF-14` |
| `out-of-memory` | Core features 4 | `C-CF-14` |
| `timeout` | Core features 4 | `C-CF-14` |
| `preempted` | Core features 4 | `C-CF-14` |
| `worker-lost` | Core features 4 | `C-CF-14` |
| `platform-error` | Core features 4 | `C-CF-14` |
| `quota-exceeded` | Core features 4 | `C-CF-14` |
| `policy-denied` | Core features 4 | `C-CF-14` |
| `no capacity in region` | Core features 12 | `C-CF-63` |
| `workspace concurrency limit reached` | Core features 12 | `C-CF-63` |
| `accelerator quota reached` | Core features 12 | `C-CF-63` |
| `function maximum containers reached` | Core features 12 | `C-CF-63` |
| `cold start in progress` | Core features 12 | `C-CF-63` |
| `workspace on hold` | Core features 12 | `C-CF-63` |
| `Inter Variable` | UI/UX notes | `C-UX-11` |
| `Fira Mono` | UI/UX notes | `C-UX-12` |
| `DATABASE_URL` | Technical requirements | `C-TR-03` |
| `DB_URL` | Technical requirements | `C-TR-04` |
| `AUTH_URL` | Technical requirements | `C-TR-05` |
| `Vireo Research` | Data model | `C-DM-14` |
| `vireo-research` | Data model | `C-DM-14` |
| `development` | Data model | `C-DM-15` |
| `production` | Data model | `C-DM-15` |
| `owner@example.com` | Data model | `C-DM-16` |
| `owner` | Data model | `C-DM-16` |
| `operator@example.com` | Data model | `C-DM-17` |
| `operator` | Data model | `C-DM-17` |
| `operator2@example.com` | Data model | `C-DM-18` |
| `developer@example.com` | Data model | `C-DM-19` |
| `developer` | Data model | `C-DM-19` |
| `developer2@example.com` | Data model | `C-DM-20` |
| `readonly@example.com` | Data model | `C-DM-21` |
| `read-only` | Data model | `C-DM-21` |
| `deku-demo-pw-2026` | Data model | `C-DM-22` |
| `Nova Inference` | Data model | `C-DM-23` |
| `Atlas Batch` | Data model | `C-DM-23` |
| `embed` | Data model | `C-DM-24` |
| `rerank` | Data model | `C-DM-24` |
| `nightly-rollup` | Data model | `C-DM-24` |
| `usd` | Data model | `C-DM-27` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the accelerator classes a function may declare | `C-CF-12` |
| the per-container log line rate limit | `C-CF-64` |
| the spend budget threshold values | `C-CF-69` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 1 | 4 |
| User roles | 2 | 16 |
| Core features | 17 | 83 |
| User flow | 4 | 13 |
| UI and UX notes | 4 | 28 |
| Technical requirements | 7 | 19 |
| Data model | 4 | 28 |
| Front-end specification | 2 | 12 |
| Constraints | 1 | 4 |
| Build plan | 3 | 8 |
| Deployment contract | 6 | 10 |

