# Checklist: Girder

Items: 380
Unpinned values flagged: 6
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` The product serves a public marketing surface plus a governed console behind one sign-in. `src: Overview`
- [ ] `C-OV-02` `constraint` The browser never holds a resource credential. `src: Overview`
- [ ] `C-OV-03` `constraint` The browser never composes the statement sent to a resource. `src: Overview`
- [ ] `C-OV-04` `constraint` The browser is never the authority on what a principal may see. `src: Overview`
- [ ] `C-OV-05` `capability` A control hidden in the interface never stands in for a server decision. `src: Overview`
- [ ] `C-OV-06` `constraint` The product carries no scheduler, no webhook receiver, no federated identity provider. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` An `owner` administers members, groups, grants, policies, resources, environments. `src: User roles`
- [ ] `C-RL-02` `role` An `owner` cannot grant an approval the same principal requested. `src: User roles`
- [ ] `C-RL-03` `role` An `owner` cannot alter an audit record. `src: User roles`
- [ ] `C-RL-04` `role` A `builder` authors app drafts, canvas operations, queries, frozen versions. `src: User roles`
- [ ] `C-RL-05` `role` A `builder` cannot administer members, groups, grants, policies. `src: User roles`
- [ ] `C-RL-06` `role` A `builder` cannot read a stored resource credential. `src: User roles`
- [ ] `C-RL-07` `role` A `builder` cannot promote to `production` without an approval granted by another principal. `src: User roles`
- [ ] `C-RL-08` `role` An `operator` runs published apps the groups of that principal grant. `src: User roles`
- [ ] `C-RL-09` `role` An `operator` cannot reach the editor at any address. `src: User roles`
- [ ] `C-RL-10` `role` An `operator` cannot widen a row predicate by editing a request parameter. `src: User roles`
- [ ] `C-RL-11` `role` An `auditor` reads the audit trail, holds no other read anywhere. `src: User roles`
- [ ] `C-RL-12` `role` An `auditor` writes nothing anywhere. `src: User roles`
- [ ] `C-RL-13` `constraint` Signup is closed on the console path: an account exists by seeding, or by invitation. `src: User roles`
- [ ] `C-RL-14` `capability` A lower role calling a higher-role endpoint directly is denied by the server, leaving the protected state unchanged. `src: User roles`
- [ ] `C-RL-15` `literal` The seeded principals are `owner@example.com`, `builder@example.com`, `builder2@example.com`, `operator@example.com`, `operator2@example.com`, `auditor@example.com`. `src: User roles`
- [ ] `C-RL-16` `literal` Every seeded principal signs in with the password `deku-demo-pw-2026`. `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `capability` Sign-in accepts an email plus a password, returning a bearer token carrying the principal email, the principal role. `src: Core features, auth`
- [ ] `C-CF-02` `capability` An unknown address produces the same refusal as a wrong password. `src: Core features, auth`
- [ ] `C-CF-03` `capability` A password field never appears only for addresses the product recognises. `src: Core features, auth`
- [ ] `C-CF-04` `capability` Repeated sign-in failures for one address are refused after a stated number of attempts. `src: Core features, auth`
- [ ] `C-CF-05` `capability` A sign-in lockout appends an authentication event to the audit trail. `src: Core features, auth`
- [ ] `C-CF-06` `capability` A signed-out token is refused on the next request. `src: Core features, auth`
- [ ] `C-CF-07` `capability` A session expiring mid-action leaves the typed work on screen, offering sign-in in place. `src: Core features, auth`
- [ ] `C-CF-08` `capability` The app list returned to a principal contains only apps that principal may open. `src: Core features, workspace`
- [ ] `C-CF-09` `capability` Returning every app in the workspace, hiding the remainder in the browser, is refused as a violation. `src: Core features, workspace`
- [ ] `C-CF-10` `capability` App search runs at the server across names, descriptions the caller may see. `src: Core features, workspace`
- [ ] `C-CF-11` `capability` An app card shows the name, a badge per released environment, the last edit time, the last editor. `src: Core features, workspace`
- [ ] `C-CF-12` `capability` Creating an app opens a dedicated route, takes a name, lands in the editor on a new draft. `src: Core features, workspace`
- [ ] `C-CF-13` `capability` A command palette opens from anywhere in the console, listing only what the caller may reach. `src: Core features, workspace`
- [ ] `C-CF-14` `capability` The command palette stays closed if a text field holds focus. `src: Core features, workspace`
- [ ] `C-CF-15` `capability` Creating a resource takes a name, a kind, a host, a port, a database, a username, a password. `src: Core features, resources`
- [ ] `C-CF-16` `capability` A stored resource secret renders as a set indicator plus a replace action, never as a masked value. `src: Core features, resources`
- [ ] `C-CF-17` `capability` A reachability probe runs at the server, answering `reachable`, or `unreachable` with a failure class. `src: Core features, resources`
- [ ] `C-CF-18` `constraint` A reachability probe returns no host, no port, no username, no database name, no credential fragment. `src: Core features, resources`
- [ ] `C-CF-19` `capability` Deleting a referenced resource is refused, naming the referencing apps, the referencing queries. `src: Core features, resources`
- [ ] `C-CF-20` `capability` Rotating a credential replaces the previous value, appending an audit event carrying no part of either value. `src: Core features, resources`
- [ ] `C-CF-21` `constraint` No credential, token, key appears in any response body, bundled asset, log line, error body, audit record. `src: Core features, resources`
- [ ] `C-CF-22` `capability` Query parameters are bound by the driver, never pasted into the statement text. `src: Core features, queries`
- [ ] `C-CF-23` `capability` A parameter key the query never declared is rejected as invalid. `src: Core features, queries`
- [ ] `C-CF-24` `capability` Authorization resolves per execution, before the statement reaches the resource. `src: Core features, queries`
- [ ] `C-CF-25` `literal` A query run answers exactly one of `ok`, `denied`, `invalid`, `unreachable`, `timeout`, `quota_exceeded`, `failed`. `src: Core features, queries`
- [ ] `C-CF-26` `capability` An `ok` run returns rows, a row count, a duration in milliseconds, a declared type per column. `src: Core features, queries`
- [ ] `C-CF-27` `capability` A refusal stays distinct from an `ok` run returning zero rows, end to end. `src: Core features, queries`
- [ ] `C-CF-28` `capability` A run against a resource whose credentials no longer work answers `unreachable`, naming the resource, naming the failure class. `src: Core features, queries`
- [ ] `C-CF-29` `capability` A statement exceeding the stated bound answers `timeout`, naming the bound exceeded, offering a re-run. `src: Core features, queries`
- [ ] `C-CF-30` `capability` A superseded execution is cancelled at the resource, never merely ignored at the client. `src: Core features, queries`
- [ ] `C-CF-31` `capability` A mutating run carries an idempotency key derived from the logical operation, never from the clock. `src: Core features, queries`
- [ ] `C-CF-32` `capability` A repeated idempotency key returns the first result rather than executing a second time. `src: Core features, queries`
- [ ] `C-CF-33` `data` Each execution appends one query-run record carrying the query, resource, principal, environment, row count, duration, outcome. `src: Core features, queries`
- [ ] `C-CF-34` `constraint` A query-run record never stores the result rows. `src: Core features, queries`
- [ ] `C-CF-35` `ui` The editor holds four regions: a component tree, a canvas, a query panel, an inspector. `src: Core features, canvas`
- [ ] `C-CF-36` `capability` The canvas-to-query-panel split ratio is remembered per builder per app. `src: Core features, canvas`
- [ ] `C-CF-37` `capability` A component occupies a whole number of grid columns by a whole number of grid rows. `src: Core features, canvas`
- [ ] `C-CF-38` `capability` A drop that would collide displaces the resident downward in tree order. `src: Core features, canvas`
- [ ] `C-CF-39` `capability` A displacement counts as one operation for undo. `src: Core features, canvas`
- [ ] `C-CF-40` `capability` Deleting a component leaves the vacated gap in place. `src: Core features, canvas`
- [ ] `C-CF-41` `ui` An invalid drag target is refused visibly rather than accepted, then corrected. `src: Core features, canvas`
- [ ] `C-CF-42` `capability` Escape during a drag returns the component to the origin, leaving nothing on the undo stack. `src: Core features, canvas`
- [ ] `C-CF-43` `ui` Resize handles sit on all eight edges, corners, snapping to the grid, never below one cell per axis. `src: Core features, canvas`
- [ ] `C-CF-44` `capability` A multi-select move counts as one operation with one inverse, undoing in one step. `src: Core features, canvas`
- [ ] `C-CF-45` `literal` A canvas mutation is one of `add`, `remove`, `move`, `resize`, `reparent`, `set-property`, `bind`, `unbind`, `rename`. `src: Core features, canvas`
- [ ] `C-CF-46` `capability` Undo applies the inverse of the last operation, redo re-applies the same operation. `src: Core features, canvas`
- [ ] `C-CF-47` `capability` The operation log survives a reload, so undo depth is not bounded by the session. `src: Core features, canvas`
- [ ] `C-CF-48` `capability` Renaming a component rewrites the bindings referencing that component in the same operation. `src: Core features, canvas`
- [ ] `C-CF-49` `capability` An app carrying four components at non-default positions reopens after a reload with every position, size, parent, binding intact. `src: Core features, canvas`
- [ ] `C-CF-50` `capability` A save whose base version hash is stale is refused, returning the current version, returning the conflicting operations. `src: Core features, canvas`
- [ ] `C-CF-51` `capability` Canvas selection survives a builder moving focus into the inspector. `src: Core features, canvas`
- [ ] `C-CF-52` `capability` Every canvas operation carries a keyboard path stated in the interface. `src: Core features, canvas`
- [ ] `C-CF-53` `capability` Every component exposes the own state of that component under the component name. `src: Core features, components`
- [ ] `C-CF-54` `ui` Every component able to be busy declares a busy state, an empty state, an error state. `src: Core features, components`
- [ ] `C-CF-55` `ui` The inspector groups properties as content, data, appearance, interaction, layout, identity. `src: Core features, components`
- [ ] `C-CF-56` `capability` Any bindable field switches to an expression in place, switching back with the last fixed value retained. `src: Core features, components`
- [ ] `C-CF-57` `capability` The resolved value, the resolved type of a bound field render beneath the field, live. `src: Core features, components`
- [ ] `C-CF-58` `capability` An inspector edit commits on blur, commits on enter, reverting on escape. `src: Core features, components`
- [ ] `C-CF-59` `capability` A multi-selection shows the intersection of properties, marking differing values. `src: Core features, components`
- [ ] `C-CF-60` `constraint` A binding expression reaches queries by name, components by name, the current row, a standard library, nothing else. `src: Core features, components`
- [ ] `C-CF-61` `capability` The binding dependency graph stays acyclic, refusing a cycle with both ends named. `src: Core features, components`
- [ ] `C-CF-62` `capability` Changing one value re-evaluates only the bindings downstream of the change. `src: Core features, components`
- [ ] `C-CF-63` `ui` A binding error surfaces on the component, on the inspector field, carrying the expression, carrying the failure. `src: Core features, components`
- [ ] `C-CF-64` `ui` Losing the server connection raises one global banner rather than a per-component storm. `src: Core features, components`
- [ ] `C-CF-65` `capability` An event handler is a declared action from a closed set, never a script. `src: Core features, components`
- [ ] `C-CF-66` `capability` A failing handler halts the chain, reporting which handler failed. `src: Core features, components`
- [ ] `C-CF-67` `capability` A form validates per field in the browser for feedback, at the server for truth. `src: Core features, components`
- [ ] `C-CF-68` `capability` A second form submission is refused by the idempotency key, not only by a disabled control. `src: Core features, components`
- [ ] `C-CF-69` `capability` A failed submission retains every typed value, attaching the error to the field the server named. `src: Core features, components`
- [ ] `C-CF-70` `capability` A bound select keeps the selected label after the options query re-runs. `src: Core features, components`
- [ ] `C-CF-71` `capability` Grid paging, sorting, filtering, searching, aggregation execute at the resource. `src: Core features, grid`
- [ ] `C-CF-72` `capability` One grid interaction produces one request over the seeded fifty thousand rows. `src: Core features, grid`
- [ ] `C-CF-73` `constraint` No grid response carries the whole seeded table. `src: Core features, grid`
- [ ] `C-CF-74` `capability` Grid selection is held as row keys taken from the data, never as row indices. `src: Core features, grid`
- [ ] `C-CF-75` `ui` The grid header stays attached to the body during scrolling. `src: Core features, grid`
- [ ] `C-CF-76` `data` A currency cell holds integer minor units, never a decimal fraction. `src: Core features, grid`
- [ ] `C-CF-77` `capability` An edited cell stages rather than writes, rendering as staged per row per cell. `src: Core features, grid`
- [ ] `C-CF-78` `capability` Staged changes commit by an explicit action, as one mutation, under one idempotency key. `src: Core features, grid`
- [ ] `C-CF-79` `capability` A failed commit retains the staged values, marking the failed rows with the reason. `src: Core features, grid`
- [ ] `C-CF-80` `capability` A successful commit refetches rather than patching the local copy. `src: Core features, grid`
- [ ] `C-CF-81` `capability` A cell the acting principal may not write is not editable, decided by the permission layer. `src: Core features, grid`
- [ ] `C-CF-82` `ui` The grid distinguishes first loading, subsequent loading, empty unfiltered, empty filtered, denied, error, truncated. `src: Core features, grid`
- [ ] `C-CF-83` `literal` Two environments exist in promotion order: `staging`, then `production`. `src: Core features, releases`
- [ ] `C-CF-84` `data` An app version is immutable, content addressed by a hash never reused. `src: Core features, releases`
- [ ] `C-CF-85` `data` A release is an insert pointing an environment at a version, never an update. `src: Core features, releases`
- [ ] `C-CF-86` `capability` Rolling back is promoting the previous version, available without an edit. `src: Core features, releases`
- [ ] `C-CF-87` `capability` A published app address stays stable across releases. `src: Core features, releases`
- [ ] `C-CF-88` `capability` An operator session continues on the released version until the builder promotes. `src: Core features, releases`
- [ ] `C-CF-89` `capability` Promotion to `production` requires an approval granted by a principal other than the requester. `src: Core features, releases`
- [ ] `C-CF-90` `capability` Self-approval is refused even when the requester holds the approve grant. `src: Core features, releases`
- [ ] `C-CF-91` `capability` An approval binds to the exact version hash requested, lapsing on any further edit. `src: Core features, releases`
- [ ] `C-CF-92` `capability` An approval carries a reason required at request time, lapsing unacted within the window. `src: Core features, releases`
- [ ] `C-CF-93` `capability` The same query run in each environment uses the credential set of that environment. `src: Core features, releases`
- [ ] `C-CF-94` `ui` The environment in force stays visible in the editor at all times. `src: Core features, releases`
- [ ] `C-CF-95` `literal` A permission action is one of `read`, `write`, `execute`, `publish`, `promote`, `administer`, `export`. `src: Core features, permissions`
- [ ] `C-CF-96` `capability` A decision returns a reason on an allow outcome, on a deny outcome alike. `src: Core features, permissions`
- [ ] `C-CF-97` `capability` Grants reaching a principal are collected directly, through group membership, through nested groups, through time-bounded grants. `src: Core features, permissions`
- [ ] `C-CF-98` `capability` A grant whose validity window excludes the request time is discarded. `src: Core features, permissions`
- [ ] `C-CF-99` `capability` A grant whose environment differs from the request environment is discarded. `src: Core features, permissions`
- [ ] `C-CF-100` `capability` An explicit `deny` at any scope in the chain decides the outcome. `src: Core features, permissions`
- [ ] `C-CF-101` `capability` A narrower allow never overcomes a broader deny. `src: Core features, permissions`
- [ ] `C-CF-102` `capability` The default outcome is deny at every scope for every action. `src: Core features, permissions`
- [ ] `C-CF-103` `capability` A cached decision is keyed by principal, action, target, environment, plus the version of every contributing grant. `src: Core features, permissions`
- [ ] `C-CF-104` `capability` A write to a grant, a membership, a policy, a principal status invalidates the cached decision within a stated number of seconds. `src: Core features, permissions`
- [ ] `C-CF-105` `capability` Removing a member from a group takes effect on the next authorised action of that member. `src: Core features, permissions`
- [ ] `C-CF-106` `capability` Grant expiry is enforced at decision time, never by a sweeping job. `src: Core features, permissions`
- [ ] `C-CF-107` `capability` Elevated access is requested with a reason, granted by another principal, bounded, expiring on its own. `src: Core features, permissions`
- [ ] `C-CF-108` `capability` An elevated interval is queryable afterwards as an interval with the approver, with the reason. `src: Core features, permissions`
- [ ] `C-CF-109` `capability` A row predicate composes into the statement at the server before execution. `src: Core features, permissions`
- [ ] `C-CF-110` `capability` Two principals in different groups receive different row sets from the same query. `src: Core features, permissions`
- [ ] `C-CF-111` `capability` A column mask applies at the server on the single result path every reader shares. `src: Core features, permissions`
- [ ] `C-CF-112` `constraint` A masked value never leaves the server. `src: Core features, permissions`
- [ ] `C-CF-113` `capability` Masking binds to the column identity in the result, defeating an alias, an aggregate, a join. `src: Core features, permissions`
- [ ] `C-CF-114` `capability` The `export` action is decided separately from `read`. `src: Core features, permissions`
- [ ] `C-CF-115` `capability` An administrator sees what a principal may reach, who may reach a target, why a decision was made, what changed between two moments. `src: Core features, permissions`
- [ ] `C-CF-116` `data` Grants are versioned rather than updated in place. `src: Core features, permissions`
- [ ] `C-CF-117` `capability` An invitation message reaches the invited address alone, with no cc, with no bcc. `src: Core features, invitations`
- [ ] `C-CF-118` `literal` An invitation subject begins with `Girder invitation: ` followed by the workspace name. `src: Core features, invitations`
- [ ] `C-CF-119` `literal` The seeded invitation subject reads `Girder invitation: Northgate Operations`. `src: Core features, invitations`
- [ ] `C-CF-120` `capability` An invitation body names the workspace, names the inviting principal, carries the acceptance address. `src: Core features, invitations`
- [ ] `C-CF-121` `capability` An invitation token is single use, time limited, bound to the invited address. `src: Core features, invitations`
- [ ] `C-CF-122` `capability` A second acceptance of one token is refused. `src: Core features, invitations`
- [ ] `C-CF-123` `capability` Accepting for an address already holding an account adds a membership, never a second account. `src: Core features, invitations`
- [ ] `C-CF-124` `capability` An expired token offers a fresh invitation, revealing nothing about the workspace. `src: Core features, invitations`
- [ ] `C-CF-125` `ui` An invitee sees the workspace name, the inviting principal, before accepting. `src: Core features, invitations`
- [ ] `C-CF-126` `constraint` Revoking an invitation sends no message. `src: Core features, invitations`
- [ ] `C-CF-127` `constraint` Accepting an invitation sends no message. `src: Core features, invitations`
- [ ] `C-CF-128` `constraint` Inviting an address already holding a membership is refused, sending no message. `src: Core features, invitations`
- [ ] `C-CF-129` `constraint` The audit store is append-only for every principal in the product. `src: Core features, audit`
- [ ] `C-CF-130` `data` Authentication, authorization, execution, editing, release, identity, permission, secret, administration events are recorded. `src: Core features, audit`
- [ ] `C-CF-131` `data` Every audit event carries an identity, a sequence, a time, an actor, an actor kind, a source address, a request identifier, a session identity, a target, an outcome, the preceding hash. `src: Core features, audit`
- [ ] `C-CF-132` `capability` Altering one audit record breaks every hash link after that record. `src: Core features, audit`
- [ ] `C-CF-133` `capability` Audit verification returns the first divergent sequence number rather than a boolean. `src: Core features, audit`
- [ ] `C-CF-134` `capability` An audit event commits on the same transaction as the effect the event records. `src: Core features, audit`
- [ ] `C-CF-135` `capability` The trail is queryable by actor, target, action, outcome, time window in combination. `src: Core features, audit`
- [ ] `C-CF-136` `capability` Exporting an audit result appends an audited event of its own. `src: Core features, audit`
- [ ] `C-CF-137` `data` Audit events, query-run records, drafts, versions each carry a stated retention window. `src: Core features, audit`
- [ ] `C-CF-138` `constraint` Query results are never retained beyond the request. `src: Core features, audit`
- [ ] `C-CF-139` `ui` The home route carries a hero, a feature block, a value block, a results band, two industry blocks, a closing composer, article cards, a footer. `src: Core features, marketing`
- [ ] `C-CF-140` `ui` Four pillar routes render one template, each wearing one accent family. `src: Core features, marketing`
- [ ] `C-CF-141` `capability` Every destination named by the header, by the footer, resolves to a real page. `src: Core features, marketing`
- [ ] `C-CF-142` `ui` Every figure in the results band is attributed to a named customer. `src: Core features, marketing`
- [ ] `C-CF-143` `capability` The announcement banner carries a validity window, removing itself once lapsed. `src: Core features, marketing`
- [ ] `C-CF-144` `capability` An image record without alternative text cannot be published. `src: Core features, marketing`
- [ ] `C-CF-145` `capability` Every route declares a unique title, a meta description, a theme colour, a dark colour scheme, a viewport declaration. `src: Core features, marketing`
- [ ] `C-CF-146` `capability` A favicon is served, drawn from the unit-square icon vocabulary. `src: Core features, marketing`
- [ ] `C-CF-147` `capability` A sitemap lists every published public route, named by a robots file. `src: Core features, marketing`
- [ ] `C-CF-148` `constraint` A sitemap lists no console route, no unpublished article. `src: Core features, marketing`
- [ ] `C-CF-149` `capability` A draft article is unreachable at any public address, through the site search. `src: Core features, marketing`
- [ ] `C-CF-150` `data` The content model carries a page, a band, an article, an author, a category, a customer, a result, a navigation record, an announcement. `src: Core features, marketing`
- [ ] `C-CF-151` `capability` A navigation destination resolving to nothing fails validation at publish time. `src: Core features, marketing`
- [ ] `C-CF-152` `capability` Publishing revalidates only the affected routes. `src: Core features, marketing`
- [ ] `C-CF-153` `ui` Typing an at-sign in the composer opens a source picker filtering as the visitor types. `src: Core features, composer`
- [ ] `C-CF-154` `capability` A composer chip is atomic: one backspace selects the chip, a second removes the chip whole. `src: Core features, composer`
- [ ] `C-CF-155` `capability` The caret never lands inside a composer chip. `src: Core features, composer`
- [ ] `C-CF-156` `capability` A composer chip carries a reference rather than a label, surviving a rename of the source. `src: Core features, composer`
- [ ] `C-CF-157` `capability` Composer chips survive a copy round trip, survive a paste round trip. `src: Core features, composer`
- [ ] `C-CF-158` `capability` The composer placeholder is available as one unbroken sentence for assistive technology. `src: Core features, composer`
- [ ] `C-CF-159` `capability` Submitting the composer carries the sentence, the chips, into the next screen. `src: Core features, composer`
- [ ] `C-CF-160` `constraint` The composer contacts no model, sends nothing to an analytics destination. `src: Core features, composer`
- [ ] `C-CF-161` `capability` The demo form asks for a work email, a reason chosen from three declared options, nothing further. `src: Core features, demo`
- [ ] `C-CF-162` `literal` The demo request answers exactly one of `sent`, `invalid`, `spam`, `failed`. `src: Core features, demo`
- [ ] `C-CF-163` `capability` A failed demo submission keeps every typed value in the form. `src: Core features, demo`
- [ ] `C-CF-164` `ui` The consent line states agreement to the privacy policy, linking the privacy route. `src: Core features, demo`
- [ ] `C-CF-165` `capability` Where a jurisdiction requires affirmative consent the consent line becomes an unchecked box gating submission. `src: Core features, demo`
- [ ] `C-CF-166` `literal` The subscription answers exactly one of `sent`, `invalid`, `already`, `failed`. `src: Core features, demo`
- [ ] `C-CF-167` `capability` Both public forms are limited per address, per source, without relying on a hidden field alone. `src: Core features, demo`
- [ ] `C-CF-168` `constraint` Free text from a public form is stored, rendered as text, never as markup. `src: Core features, demo`
- [ ] `C-CF-169` `capability` Search opens as an overlay from a header control, from a keyboard shortcut working on any route. `src: Core features, search`
- [ ] `C-CF-170` `capability` The search field settles before running rather than firing on every keystroke. `src: Core features, search`
- [ ] `C-CF-171` `capability` Escape, the scrim, the close control each return focus to the control the overlay opened from. `src: Core features, search`
- [ ] `C-CF-172` `constraint` Search indexes published public routes only. `src: Core features, search`
- [ ] `C-CF-173` `literal` Search answers exactly one of `ok`, `invalid`, `failed`. `src: Core features, search`
- [ ] `C-CF-174` `capability` An address resolving to nothing serves the not-found route with the full header, the full footer. `src: Core features, not-found`
- [ ] `C-CF-175` `capability` The not-found message names the requested path, rendered as text. `src: Core features, not-found`
- [ ] `C-CF-176` `ui` The not-found route carries a playable falling-blocks game with a title, a level readout, a match readout, a tally readout. `src: Core features, not-found`
- [ ] `C-CF-177` `ui` The game readouts open at the first level, at a match count of five, at a tally of zero. `src: Core features, not-found`
- [ ] `C-CF-178` `ui` Each game binding renders on screen beside the action of that binding. `src: Core features, not-found`
- [ ] `C-CF-179` `capability` The game releases the arrow keys on blur, capturing nothing until focused. `src: Core features, not-found`
- [ ] `C-CF-180` `capability` The game stops off screen, stops under a reduced-motion preference. `src: Core features, not-found`
- [ ] `C-CF-181` `capability` The game readouts are announced to assistive technology. `src: Core features, not-found`
- [ ] `C-CF-182` `constraint` The game tally stays in the browser of the visitor, sent nowhere. `src: Core features, not-found`

## C-UF User flow

- [ ] `C-UF-01` `contract` An unauthenticated request for a console address lands on the sign-in route with the requested address remembered. `src: User flow`
- [ ] `C-UF-02` `contract` A successful sign-in returns to the remembered address, falling back to the workspace home. `src: User flow`
- [ ] `C-UF-03` `contract` Signing out returns to the public home route, stopping the token immediately. `src: User flow`
- [ ] `C-UF-04` `contract` A principal whose groups grant nothing on a console route is told plainly, never shown an empty version. `src: User flow`
- [ ] `C-UF-05` `contract` An `operator` typing the editor address is refused. `src: User flow`
- [ ] `C-UF-06` `ui` Every list carries an empty state naming what would appear there, distinct from a refusal. `src: User flow`
- [ ] `C-UF-07` `ui` Every route carries a loading state. `src: User flow`
- [ ] `C-UF-08` `ui` A refusal names the action, never the data the action would have returned. `src: User flow`
- [ ] `C-UF-09` `ui` An error carries the request identifier the visitor may quote, never ending the session. `src: User flow`
- [ ] `C-UF-10` `contract` The published app runtime is reached at a run address carrying the app slug. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The public surface renders dark on every route, declaring a dark colour scheme, carrying no light version. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The console renders both a dark theme, a light theme, each designed in full. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Three meaning colours carry failure, success, progress, appearing in no other role. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` A pillar route wears exactly one accent family. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Headings set at the lightest available stroke, tracking tightening as size grows. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Figures align in a column wherever amounts stack. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Exactly one real shadow exists on the public surface, falling below the composer. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` One easing family carries the overwhelming majority of transitions. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Three continuous animations run slowly enough to read as the page being alive. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` A reduced-motion preference stops all three continuous animations entirely rather than shortening. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` The link underline retracts to the trailing edge, re-emerging from the leading edge. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` The console reads compact: rows sit tight so a full queue fits one screen. `src: UI/UX notes`
- [ ] `C-UX-13` `constraint` Contrast meets WCAG AA for text, interface components, the focus indicator, in both console themes. `src: UI/UX notes`
- [ ] `C-UX-14` `constraint` Every interaction is reachable by keyboard navigation with a visible focus ring. `src: UI/UX notes`
- [ ] `C-UX-15` `constraint` Meaning is never carried by colour alone. `src: UI/UX notes`
- [ ] `C-UX-16` `ui` The component tree is the accessible peer of the canvas rather than a fallback. `src: UI/UX notes`
- [ ] `C-UX-17` `ui` The grid announces total rows rather than rendered rows. `src: UI/UX notes`
- [ ] `C-UX-18` `ui` The layout holds at every viewport width between the named tiers. `src: UI/UX notes`
- [ ] `C-UX-19` `ui` The editor refuses a phone layout below the stated minimum width, offering the preview. `src: UI/UX notes`
- [ ] `C-UX-20` `ui` Empty, loading, denied, error, truncated render as five distinguishable states. `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Every horizontal dimension on the public surface derives from one column arithmetic rule. `src: Front-end specification`
- [ ] `C-FE-02` `ui` The content occupies all but two columns, the remaining two splitting either side as the outer gutter. `src: Front-end specification`
- [ ] `C-FE-03` `ui` A hairline border carries cards, table cells, the logo wall, the footer columns. `src: Front-end specification`
- [ ] `C-FE-04` `ui` The colour system carries three layers: raw ladders, semantic surfaces, per-component state sets. `src: Front-end specification`
- [ ] `C-FE-05` `ui` A pressed button takes the label colour to fully transparent, leaving the icon opaque. `src: Front-end specification`
- [ ] `C-FE-06` `ui` A focused text input inverts from transparent-on-dark to a solid pale field with dark type. `src: Front-end specification`
- [ ] `C-FE-07` `ui` Eight accent ladders run darkest to lightest at seven steps each. `src: Front-end specification`
- [ ] `C-FE-08` `ui` Type carries a continuous stroke axis reaching two in-between values no static family reaches. `src: Front-end specification`
- [ ] `C-FE-09` `ui` Corners soften on a short ladder, a circular control staying a semicircle at any height. `src: Front-end specification`
- [ ] `C-FE-10` `ui` Depth ordering places the cursor above the modal layer, the skip link above everything. `src: Front-end specification`
- [ ] `C-FE-11` `ui` Every icon draws as unit squares on a small integer grid, shipping as inline geometry. `src: Front-end specification`
- [ ] `C-FE-12` `ui` The search glyph is the one icon drawn as true geometry rather than unit squares. `src: Front-end specification`
- [ ] `C-FE-13` `ui` The dismiss glyph shares the action arrow path, rotated by the consuming component. `src: Front-end specification`
- [ ] `C-FE-14` `ui` The header renders transparent at rest, acquiring a near-solid dark field once scrolled. `src: Front-end specification`
- [ ] `C-FE-15` `ui` Three header menus open one shared panel spanning the document width, animating as one object. `src: Front-end specification`
- [ ] `C-FE-16` `ui` The high-value conversion control is the quieter of the conversion pair. `src: Front-end specification`
- [ ] `C-FE-17` `ui` Below the tablet tier the header contents scale as one transform rather than being re-typeset. `src: Front-end specification`
- [ ] `C-FE-18` `ui` The footer sets the wordmark large enough to span roughly two thirds of the viewport. `src: Front-end specification`
- [ ] `C-FE-19` `ui` A marquee track duplicates its contents, deriving duration from content width. `src: Front-end specification`
- [ ] `C-FE-20` `ui` A marquee row masks at both edges so items enter through a fade rather than at a hard boundary. `src: Front-end specification`
- [ ] `C-FE-21` `ui` The feature tab timer pauses on hover, on focus within the block, on leaving the viewport. `src: Front-end specification`
- [ ] `C-FE-22` `ui` Selecting a feature tab by hand stops automatic advance for the remainder of the session. `src: Front-end specification`
- [ ] `C-FE-23` `ui` The custom cursor declares four states: default, hover, active, message. `src: Front-end specification`
- [ ] `C-FE-24` `ui` The cursor label follows the pointer under a transition rather than being positioned per frame. `src: Front-end specification`
- [ ] `C-FE-25` `ui` The custom cursor renders nowhere a pointer cannot hover. `src: Front-end specification`
- [ ] `C-FE-26` `ui` The custom cursor leaves text inputs, text selection, native controls their own cursor. `src: Front-end specification`
- [ ] `C-FE-27` `ui` Scroll effects attach locally to the element rather than writing state onto the document root. `src: Front-end specification`
- [ ] `C-FE-28` `ui` The hero frame blur ramps together with opacity, driven continuously by scroll position. `src: Front-end specification`
- [ ] `C-FE-29` `ui` The hero scrim renders as a multi-stop gradient with an accelerating alpha curve. `src: Front-end specification`
- [ ] `C-FE-30` `ui` The decorative vertical rules are the layout column grid made briefly visible. `src: Front-end specification`
- [ ] `C-FE-31` `ui` The composer border renders as a ring of exactly the border width following the corner radius. `src: Front-end specification`
- [ ] `C-FE-32` `ui` The composer placeholder sheen is a travelling hole in a dark overlay rather than a bright streak. `src: Front-end specification`
- [ ] `C-FE-33` `ui` The composer sheen stops on focus. `src: Front-end specification`
- [ ] `C-FE-34` `ui` Customer marks render as monochrome silhouettes on the pale tile, redrawn from unit squares. `src: Front-end specification`
- [ ] `C-FE-35` `ui` No typeface file, photograph, icon file, texture, video, logo file ships. `src: Front-end specification`
- [ ] `C-FE-36` `ui` The hero video frame is filled by a generated field of slow coloured light over fine grain. `src: Front-end specification`
- [ ] `C-FE-37` `ui` Article illustrations generate from a seed derived from the article slug. `src: Front-end specification`
- [ ] `C-FE-38` `ui` Each view declares one main landmark, a banner landmark, a contentinfo landmark, labelled navigation landmarks. `src: Front-end specification`
- [ ] `C-FE-39` `ui` Each view carries exactly one first-level heading, skipping no level below. `src: Front-end specification`
- [ ] `C-FE-40` `ui` Every control carries an accessible name matching the visible label where one exists. `src: Front-end specification`
- [ ] `C-FE-41` `literal` The header conversion controls read `Book a demo`, `Start for free`. `src: Front-end specification`
- [ ] `C-FE-42` `literal` The home headline reads `Secure your vibe-coded apps`. `src: Front-end specification`
- [ ] `C-FE-43` `literal` The skip link reads `Skip to main content`. `src: Front-end specification`
- [ ] `C-FE-44` `literal` The footer copyright reads `(c) Girder 2026`. `src: Front-end specification`
- [ ] `C-FE-45` `literal` The not-found action reads `Go to homepage`. `src: Front-end specification`
- [ ] `C-FE-46` `literal` The game title reads `404 Blocks`. `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The backend runs NestJS on Node 20, serving the JSON API. `src: Technical requirements`
- [ ] `C-TR-02` `contract` The frontend builds with Vue 3 under Vite into a production bundle. `src: Technical requirements`
- [ ] `C-TR-03` `contract` The datastore is PostgreSQL reached at `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-04` `contract` Mail sends over real SMTP to Mailpit at `SMTP_HOST`, `SMTP_PORT`. `src: Technical requirements`
- [ ] `C-TR-05` `contract` Authentication is app-implemented email with password, hashed, issuing bearer tokens. `src: Technical requirements`
- [ ] `C-TR-06` `contract` A health route returns `200` once the app is ready. `src: Technical requirements`
- [ ] `C-TR-07` `constraint` No second database, cache, queue, object store, identity provider, mail vendor is introduced. `src: Technical requirements`
- [ ] `C-TR-08` `constraint` The backing services are already running, never downloaded, never started by the app. `src: Technical requirements`
- [ ] `C-TR-09` `constraint` No host, no port is hardcoded; every one is read from the environment. `src: Technical requirements`
- [ ] `C-TR-10` `contract` Three deployable surfaces ship from one repository: marketing, studio, runtime. `src: Technical requirements`
- [ ] `C-TR-11` `constraint` The runtime bundle carries no editor code. `src: Technical requirements`
- [ ] `C-TR-12` `contract` Dependencies point one way from the design system through the runtime to the editor. `src: Technical requirements`
- [ ] `C-TR-13` `contract` No product state is held in a module-scope singleton. `src: Technical requirements`
- [ ] `C-TR-14` `capability` A client-side permission copy is advisory, used only to hide controls. `src: Technical requirements`
- [ ] `C-TR-15` `capability` Every performance bound is stated against the reference conditions carried in the brief. `src: Technical requirements`
- [ ] `C-TR-16` `capability` Concurrent executions per workspace are bounded, answering `quota_exceeded` beyond the bound. `src: Technical requirements`
- [ ] `C-TR-17` `capability` Rows per result are capped per resource, flagged as truncated in the response. `src: Technical requirements`
- [ ] `C-TR-18` `capability` Resource errors map to a stated outcome before leaving the server. `src: Technical requirements`
- [ ] `C-TR-19` `capability` A resource refusal stays distinct from a platform refusal. `src: Technical requirements`
- [ ] `C-TR-20` `capability` A request identifier generates at the edge, propagating to every log line, returning to the caller on error. `src: Technical requirements`
- [ ] `C-TR-21` `constraint` Parameters are logged by name, by type, never by value. `src: Technical requirements`
- [ ] `C-TR-22` `constraint` Result rows are never logged. `src: Technical requirements`
- [ ] `C-TR-23` `capability` Metrics record rate, error rate, duration distribution, quota consumption per workspace per resource per query. `src: Technical requirements`
- [ ] `C-TR-24` `contract` Every response carries a security header set covering content policy, transport, frame ancestors, referrer, sniffing, permissions. `src: Technical requirements`
- [ ] `C-TR-25` `capability` Every mutating cross-boundary call carries a derived idempotency key retained across the retry window. `src: Technical requirements`
- [ ] `C-TR-26` `contract` A sitemap generates from the published public routes, named by a robots file. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` All timestamps are UTC. `src: Data model`
- [ ] `C-DM-02` `literal` Every seeded account uses the password `deku-demo-pw-2026`, written into `/app/USER_README.md`. `src: Data model`
- [ ] `C-DM-03` `data` Money is held in integer minor units of `usd`, never as a decimal fraction. `src: Data model`
- [ ] `C-DM-04` `data` A principal row carries an identity, an email unique across the table, a role, a password hash, a status. `src: Data model`
- [ ] `C-DM-05` `data` A group row carries a name unique across the table, an optional parent, forming a cycle-checked nesting. `src: Data model`
- [ ] `C-DM-06` `data` A group membership row records the source of the membership. `src: Data model`
- [ ] `C-DM-07` `data` A resource row holds a reference to a credential rather than the secret itself. `src: Data model`
- [ ] `C-DM-08` `data` A credential row exists once per resource per environment, encrypted at rest under a per-workspace key. `src: Data model`
- [ ] `C-DM-09` `data` An app version row is never updated once written. `src: Data model`
- [ ] `C-DM-10` `data` A draft row references a base version hash plus an ordered operation list. `src: Data model`
- [ ] `C-DM-11` `data` A component row carries a name unique within the version, a grid rectangle, a parent, a position. `src: Data model`
- [ ] `C-DM-12` `data` A query row carries a name unique within the version, a resource, a statement, declared parameters. `src: Data model`
- [ ] `C-DM-13` `data` A release row is inserted only, the newest row for an environment being the release in force. `src: Data model`
- [ ] `C-DM-14` `data` An approval row never carries the same principal as requester plus approver. `src: Data model`
- [ ] `C-DM-15` `data` A granted approval is usable only for a release whose version hash equals the approval version hash. `src: Data model`
- [ ] `C-DM-16` `data` Two promotion attempts racing on one approval produce exactly one release. `src: Data model`
- [ ] `C-DM-17` `data` A permission row is an edge carrying a principal, a scope, an action, an effect, a validity window, a version. `src: Data model`
- [ ] `C-DM-18` `data` A policy row carries a row predicate, masked columns, a version, a publish time. `src: Data model`
- [ ] `C-DM-19` `data` An invitation token is usable exactly once, two simultaneous acceptances producing exactly one membership. `src: Data model`
- [ ] `C-DM-20` `data` An audit sequence increases strictly with no gaps within the workspace. `src: Data model`
- [ ] `C-DM-21` `data` An audit event hash covers every other column of the row, the preceding hash among them. `src: Data model`
- [ ] `C-DM-22` `data` The release in force is derived from the newest release row rather than stored as a flag. `src: Data model`
- [ ] `C-DM-23` `data` Effective grants are derived at decision time rather than cached onto the principal row. `src: Data model`
- [ ] `C-DM-24` `data` Seeding is idempotent: restarting the app duplicates no row. `src: Data model`
- [ ] `C-DM-25` `literal` The seeded workspace is `Northgate Operations`. `src: Data model`
- [ ] `C-DM-26` `literal` The seeded resources are `Orders Warehouse`, `Ledger Archive`. `src: Data model`
- [ ] `C-DM-27` `literal` The seeded apps are `Order Desk`, `Refund Desk`. `src: Data model`
- [ ] `C-DM-28` `literal` The seeded queries are `orders_recent`, `order_mark_delayed`. `src: Data model`
- [ ] `C-DM-29` `literal` The seeded groups are `Platform Builders`, `Operations`, `Support Desk`. `src: Data model`
- [ ] `C-DM-30` `literal` The seeded orders table carries `50000` rows. `src: Data model`
- [ ] `C-DM-31` `literal` The named seeded orders are `NG-1001`, `NG-1002`, `NG-1003`. `src: Data model`
- [ ] `C-DM-32` `literal` The named seeded order amounts are `124500`, `98000`, `1000`. `src: Data model`
- [ ] `C-DM-33` `literal` The seeded policy `Support masking` restricts rows to `delayed`, masking `customer_name`. `src: Data model`
- [ ] `C-DM-34` `data` The `Support Desk` group holds an explicit deny on export at the workspace scope. `src: Data model`
- [ ] `C-DM-35` `data` One seeded resource carries a stale credential so a reachability probe answers unreachable. `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` A single workspace exists, with no second tenant, no cross-workspace surface. `src: Constraints`
- [ ] `C-CN-02` `constraint` No workflow scheduler, no run history, no webhook receiver exists. `src: Constraints`
- [ ] `C-CN-03` `constraint` No federated identity provider, no second factor exists. `src: Constraints`
- [ ] `C-CN-04` `constraint` No residency region, no erasure across derived stores exists. `src: Constraints`
- [ ] `C-CN-05` `constraint` No payment, no billing, no subscription, no invoicing exists. `src: Constraints`
- [ ] `C-CN-06` `constraint` No native mobile application exists. `src: Constraints`
- [ ] `C-CN-07` `constraint` No comment, no like, no direct message exists. `src: Constraints`
- [ ] `C-CN-08` `constraint` No collaborative cursor exists. `src: Constraints`
- [ ] `C-CN-09` `constraint` No model call is made from any surface. `src: Constraints`
- [ ] `C-CN-10` `constraint` Only PostgreSQL, Mailpit exist as backing services. `src: Constraints`
- [ ] `C-CN-11` `constraint` Resource kinds beyond the relational kind are declarable, never executed. `src: Constraints`
- [ ] `C-CN-12` `constraint` No external network call is made at runtime. `src: Constraints`
- [ ] `C-CN-13` `constraint` No analytics destination receives any value. `src: Constraints`
- [ ] `C-CN-14` `constraint` No binary asset ships with the build. `src: Constraints`
- [ ] `C-CN-15` `constraint` No mark reproduces a real trademark. `src: Constraints`
- [ ] `C-CN-16` `constraint` No route reflects an unescaped request value into a page. `src: Constraints`
- [ ] `C-CN-17` `constraint` The product stays responsive at fifty thousand seeded rows, two hundred canvas components, thirty queries. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at the public address read from the environment. `src: Deployment contract`
- [ ] `C-DC-02` `contract` The port mapping publishes the container-internal port read from the environment. `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under an api prefix. `src: Deployment contract`
- [ ] `C-DC-04` `contract` The health route returns a success status once the app is ready. `src: Deployment contract`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-06` `contract` Login credentials are written to the readme path at the app root. `src: Deployment contract`
- [ ] `C-DC-07` `contract` Two reserved directories exist at the app root, empty. `src: Deployment contract`
- [ ] `C-DC-08` `contract` A production build is served behind a static server, never a development server. `src: Deployment contract`
- [ ] `C-DC-09` `contract` The server outlives the session, never running as a child of the shell. `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server binds all interfaces rather than loopback. `src: Deployment contract`
- [ ] `C-DC-11` `contract` The named backing services are already running, never started by the app. `src: Deployment contract`
- [ ] `C-DC-12` `contract` No edge function is used. `src: Deployment contract`
- [ ] `C-DC-13` `contract` No persistent volume, no fixed container name, no custom network is declared. `src: Deployment contract`
- [ ] `C-DC-14` `contract` Every list endpoint returns a top-level JSON array. `src: Deployment contract`
- [ ] `C-DC-15` `contract` An invalid request is rejected as a client error rather than a server error. `src: Deployment contract`
- [ ] `C-DC-16` `contract` An unauthorized request is rejected as a client error rather than served. `src: Deployment contract`
- [ ] `C-DC-17` `contract` Bearer auth is carried on every endpoint except sign-in, health, the three public marketing endpoints. `src: Deployment contract`
- [ ] `C-DC-18` `contract` Field names in every graded request body are exact. `src: Deployment contract`
- [ ] `C-DC-19` `contract` An in-memory store standing in for the named provider is refused as a violation. `src: Deployment contract`
- [ ] `C-DC-20` `contract` A reachability answer produced without opening a connection is refused as a violation. `src: Deployment contract`
- [ ] `C-DC-21` `contract` An invitation recorded as sent without handing a message to SMTP is refused as a violation. `src: Deployment contract`
- [ ] `C-DC-22` `contract` An audit chain recomputed on read is refused as a violation. `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `owner@example.com` | a value the brief pins verbatim | `C-RL-15` |
| `builder@example.com` | a value the brief pins verbatim | `C-RL-15` |
| `builder2@example.com` | a value the brief pins verbatim | `C-RL-15` |
| `operator@example.com` | a value the brief pins verbatim | `C-RL-15` |
| `operator2@example.com` | a value the brief pins verbatim | `C-RL-15` |
| `auditor@example.com` | a value the brief pins verbatim | `C-RL-15` |
| `deku-demo-pw-2026` | a value the brief pins verbatim | `C-RL-16` |
| `ok` | a value the brief pins verbatim | `C-CF-25` |
| `denied` | a value the brief pins verbatim | `C-CF-25` |
| `invalid` | a value the brief pins verbatim | `C-CF-25` |
| `unreachable` | a value the brief pins verbatim | `C-CF-25` |
| `timeout` | a value the brief pins verbatim | `C-CF-25` |
| `quota_exceeded` | a value the brief pins verbatim | `C-CF-25` |
| `failed` | a value the brief pins verbatim | `C-CF-25` |
| `add` | a value the brief pins verbatim | `C-CF-45` |
| `remove` | a value the brief pins verbatim | `C-CF-45` |
| `move` | a value the brief pins verbatim | `C-CF-45` |
| `resize` | a value the brief pins verbatim | `C-CF-45` |
| `reparent` | a value the brief pins verbatim | `C-CF-45` |
| `set-property` | a value the brief pins verbatim | `C-CF-45` |
| `bind` | a value the brief pins verbatim | `C-CF-45` |
| `unbind` | a value the brief pins verbatim | `C-CF-45` |
| `rename` | a value the brief pins verbatim | `C-CF-45` |
| `staging` | a value the brief pins verbatim | `C-CF-83` |
| `production` | a value the brief pins verbatim | `C-CF-83` |
| `read` | a value the brief pins verbatim | `C-CF-95` |
| `write` | a value the brief pins verbatim | `C-CF-95` |
| `execute` | a value the brief pins verbatim | `C-CF-95` |
| `publish` | a value the brief pins verbatim | `C-CF-95` |
| `promote` | a value the brief pins verbatim | `C-CF-95` |
| `administer` | a value the brief pins verbatim | `C-CF-95` |
| `export` | a value the brief pins verbatim | `C-CF-95` |
| `Girder invitation: ` | a value the brief pins verbatim | `C-CF-118` |
| `Girder invitation: Northgate Operations` | a value the brief pins verbatim | `C-CF-119` |
| `sent` | a value the brief pins verbatim | `C-CF-162` |
| `spam` | a value the brief pins verbatim | `C-CF-162` |
| `already` | a value the brief pins verbatim | `C-CF-166` |
| `Book a demo` | a value the brief pins verbatim | `C-FE-41` |
| `Start for free` | a value the brief pins verbatim | `C-FE-41` |
| `Secure your vibe-coded apps` | a value the brief pins verbatim | `C-FE-42` |
| `Skip to main content` | a value the brief pins verbatim | `C-FE-43` |
| `(c) Girder 2026` | a value the brief pins verbatim | `C-FE-44` |
| `Go to homepage` | a value the brief pins verbatim | `C-FE-45` |
| `404 Blocks` | a value the brief pins verbatim | `C-FE-46` |
| `/app/USER_README.md` | a value the brief pins verbatim | `C-DM-02` |
| `Northgate Operations` | a value the brief pins verbatim | `C-DM-25` |
| `Orders Warehouse` | a value the brief pins verbatim | `C-DM-26` |
| `Ledger Archive` | a value the brief pins verbatim | `C-DM-26` |
| `Order Desk` | a value the brief pins verbatim | `C-DM-27` |
| `Refund Desk` | a value the brief pins verbatim | `C-DM-27` |
| `orders_recent` | a value the brief pins verbatim | `C-DM-28` |
| `order_mark_delayed` | a value the brief pins verbatim | `C-DM-28` |
| `Platform Builders` | a value the brief pins verbatim | `C-DM-29` |
| `Operations` | a value the brief pins verbatim | `C-DM-29` |
| `Support Desk` | a value the brief pins verbatim | `C-DM-29` |
| `50000` | a value the brief pins verbatim | `C-DM-30` |
| `NG-1001` | a value the brief pins verbatim | `C-DM-31` |
| `NG-1002` | a value the brief pins verbatim | `C-DM-31` |
| `NG-1003` | a value the brief pins verbatim | `C-DM-31` |
| `124500` | a value the brief pins verbatim | `C-DM-32` |
| `98000` | a value the brief pins verbatim | `C-DM-32` |
| `1000` | a value the brief pins verbatim | `C-DM-32` |
| `Support masking` | a value the brief pins verbatim | `C-DM-33` |
| `delayed` | a value the brief pins verbatim | `C-DM-33` |
| `customer_name` | a value the brief pins verbatim | `C-DM-33` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the stated number of sign-in attempts before a lockout | `C-CF-04` |
| the stated number of seconds a decision cache may lag a grant write | `C-CF-110` |
| the option count above which a bound select searches at the server | `C-CF-71` |
| the stated per-resource statement timeout bound | `C-CF-29` |
| the stated minimum width below which the editor refuses a phone layout | `C-UX-19` |
| the stated compressed payload cap for the marketing surface | `C-TR-15` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 4 | 6 |
| User roles | 5 | 16 |
| Core features | 45 | 182 |
| User flow | 3 | 10 |
| UI and UX notes | 4 | 20 |
| Front-end specification | 10 | 46 |
| Technical requirements | 9 | 26 |
| Data model | 10 | 35 |
| Constraints | 2 | 17 |
| Deployment contract | 10 | 22 |
