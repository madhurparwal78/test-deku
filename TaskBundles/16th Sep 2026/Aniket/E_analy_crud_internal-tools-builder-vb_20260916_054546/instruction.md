# Girder

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser and, signed in as a builder, connect a database resource, bind a table and a form to a query on a canvas, publish that app to a permission group, and watch a support operator run it against production records without hitting an error page. A different stranger, signed in as that support operator, must NOT be able to change a record the operator's group is denied, by any means, including calling the API directly with a valid token. A refusal is a refusal: the record must be unchanged afterwards, and the refusal must be a distinct answer from an empty result. A green tick the app returns to itself does not count.

## Overview

Girder is a platform for building internal software. Engineers and operations staff maintain a company's own databases and need governed screens over them. A developer connects a database, drags a table and a form onto a canvas, binds them to a query, restricts the app to one permission group, and publishes an immutable release that support staff run against production records. The platform's claim is not that building is possible. It is that building is possible without the security team saying no, and every part of the product is arranged around defending that claim.

The product has two surfaces and both are the product. A public marketing site sells the promise to two audiences at once, the engineer who will build with it and the manager who has to approve it, and takes demo requests and self-serve signups. A governed console behind the sign-in keeps the promise: resources, apps, queries, components, permission groups, environments, releases and an append-only audit trail.

One sentence generates most of the rules below. The browser never holds a credential, never composes a statement, and is never the authority on what a principal may see. Every screen may hide a control it believes is disallowed, purely so the interface is not a field of dead buttons, and that hiding is never the enforcement.

Girder deliberately is not a great many things. There is no workflow scheduler, no inbound webhook receiver, no federated identity provider, no second factor, no data residency region, no erasure across derived stores, no payment, no billing, no native mobile application, no comments, no likes and no messaging. The genuinely hard part is that every refusal has to be a refusal: decided by the server, distinguishable from an empty result, and recorded in a trail nobody can quietly edit afterwards.

## User roles

Four roles. Signup is closed on the governed path: an account exists because it was seeded or because somebody was invited. The public site's self-serve control and prompt composer both lead to the demo and signup capture of the marketing surface, never to a new console account.

| Role | Can read | Can write |
|---|---|---|
| `owner` | every app, resource, group, grant, policy, environment and the audit trail in the workspace | members, invitations, groups, grants, policies, resources, credentials, environments, and approval decisions. **Cannot approve an approval the owner requested, and cannot alter or delete an audit record.** |
| `builder` | apps and queries the builder's groups grant, resource names, kinds and last test results | app drafts, canvas operations, queries, frozen versions, promotion requests, and promotions to an unprotected environment. **Cannot administer members, groups, grants or policies, cannot read a stored credential, cannot promote to `production` without an approval granted by somebody else, and cannot approve its own request.** |
| `operator` | published apps the operator's groups grant, in the environments those groups grant, with row predicates and column masks already applied | only what a published app's own mutating query allows for that group. **Cannot open the editor at any address, cannot see an app no group grants, cannot widen a row predicate by editing a request parameter, and cannot export where an explicit deny exists.** |
| `auditor` | the audit trail, and nothing else anywhere | nothing, anywhere. **Cannot read an app, a resource, a query result or a member record, and cannot alter the trail it reads.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a `operator` session to any `owner`-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Permission is scoped by relationship as well as by role. An `operator` reaches an app because a group the operator belongs to holds an `allow` on that app in that environment, not because the role is `operator`. A `builder` reaches an app the same way. Two operators in different groups opening the same app must receive different row sets from the same query.

Seeded accounts, every one of them using the corpus password:

| Email | Role | Groups |
|---|---|---|
| `owner@example.com` | `owner` | `Platform Builders` |
| `builder@example.com` | `builder` | `Platform Builders` |
| `builder2@example.com` | `builder` | `Platform Builders` |
| `operator@example.com` | `operator` | `Operations` |
| `operator2@example.com` | `operator` | `Support Desk` |
| `auditor@example.com` | `auditor` | none |

## Core features

### Auth and sessions

Sign-in takes an email and a password and returns an `access_token` the client sends as a bearer token on every request except sign-in itself, the health route and the three unauthenticated marketing endpoints. Passwords are stored hashed. There is no public registration on the console path.

1. A correct email with a correct password signs in and returns a token that carries the principal's email and role.
2. An unknown address and a wrong password produce the **same** refusal message, the same outcome, and neither response nor any part of the page reveals which of the two happened. A sign-in screen that shows a password field only for addresses it recognises has disclosed the same fact by a different route and is wrong.
3. Repeated failures for one address are refused after a stated number of attempts, and the lockout is itself written to the audit trail as an authentication event.
4. Signing out stops the token working immediately. A request carrying a signed-out token is refused, not served from a cache.
5. A token that expires mid-action leaves the typed work on screen, says the session has ended, and offers sign-in in place rather than discarding the work.

### The workspace and its app catalog

The console opens on the workspace home, a card grid of apps.

1. The app list contains only apps the calling principal may open, decided at the server. Returning every app in the workspace and hiding the rest in the browser is a contract violation: it puts the whole catalogue of an organisation's internal tooling one glance at the network panel away.
2. Apps group into folders, and a folder carries its own grants.
3. Search across app names and descriptions runs at the server and searches only what the caller may see.
4. Each card shows the app name, a badge per environment it is released to, the time of the last edit and the email of the last editor.
5. Creating an app opens a dedicated route at `/console/apps/new`, takes a name, and lands in the editor on a new draft with no released version.
6. Recents and favourites are per principal and never make an unentitled app visible.
7. A command palette opens from anywhere in the console with the platform modifier and `K`, and from a visible control that carries the same hint. It is the console's primary way to reach an app, a resource, an administration screen or a query, and it lists only what the caller may reach. It does not open while a text field has focus.

### Resources and credentials

A resource is a named, typed connection the platform owns. The catalog accepts the kinds `postgres`, `http_api`, `object_store`, `queue`, `warehouse` and `model_provider`; only `postgres` executes statements in this environment, and the other kinds are declarable, listable and deletable but never executed.

1. Creating a resource takes `name`, `kind`, `host`, `port`, `database`, `username` and `password`, per environment. The stored secret is write-only: the interface shows a set indicator and a replace action, never a masked value a client-side toggle could reveal.
2. A test connection runs at the server and answers `reachable` or `unreachable` with a failure class. It never returns the host, the port, the username, the database name or any fragment of the credential, and it never passes the driver's own error text through when that text can carry them.
3. Deleting a resource is refused while any app or query references it, and the refusal names the referencing apps and queries rather than cascading.
4. Rotating a credential replaces the previous value rather than versioning it, and writes its own audit event that carries no part of either value.
5. No credential, connection string, bearer token or private key appears in any response body, any bundled asset, any log line, any error body or any audit record, on any screen, at any point. This holds across every other feature in this brief, not only on the resource form.

### Queries and the query contract

A query is a named, parameterised, resource-bound statement stored against an app version and executed by the server on behalf of a principal.

1. Parameters are bound by the driver. Building a statement by pasting a parameter value into its text is a contract violation however the value was escaped.
2. Every parameter the caller sends must be declared by the query. An undeclared key is rejected as invalid rather than ignored.
3. Authorization is resolved per execution, before the statement is sent, and the resource's own database user is never the authority on what the principal may see.
4. A run answers with exactly one state from this closed set, spelled exactly: `ok`, `denied`, `invalid`, `unreachable`, `timeout`, `quota_exceeded`, `failed`.
5. An `ok` run returns the rows, the row count, the duration in milliseconds, and a declared type per column, so a date that arrived as text is visible as text.
6. `denied` and an `ok` run that returned zero rows are different answers and must stay different end to end, in the response, in the bound component and on the screen. Collapsing a refusal into an empty result is a contract violation: it is how a permission defect stays invisible for a year.
7. A run against a resource whose credentials no longer work answers `unreachable`, names the resource, names the failure class, and shows no stack trace, no host name and no credential fragment.
8. A statement that exceeds the resource's stated bound answers `timeout`, names the bound that was exceeded, offers a re-run, and returns the connection to its pool. The workspace stays responsive for every other principal while a slow statement runs.
9. A superseded execution is cancelled at the resource rather than ignored at the client, and a result that arrives after the request that asked for it has been replaced is discarded rather than rendered.
10. Every mutating run carries an `idempotency_key` derived from the logical operation, never from the clock and never from a value generated at send time. A repeated key returns the first result rather than executing a second time.
11. Each execution appends one query-run record carrying the query, the resource, the principal, the environment, the row count, the duration and the outcome, and **never** the result rows.

### The builder canvas and the operation log

The editor has four regions with draggable dividers: a component tree on the leading rail, the canvas above the centre, the query panel below it, and the inspector on the trailing rail. The three rails collapse; the canvas does not. The split ratio between canvas and query panel is remembered per builder and per app, not globally.

1. The canvas is a grid with a fixed column count across its width and a fixed row unit, so a layout is resolution independent. A component occupies a whole number of columns by a whole number of rows.
2. Two components may never occupy the same cell. A drop that would collide displaces the resident downward in tree order, and the displacement is one operation for undo.
3. Deleting a component leaves its gap where it was. Closing the gap automatically is a contract violation here: a builder who deletes one thing and watches the layout jump has lost their place.
4. Dragging from the library shows a ghost following the pointer and outlines the target cells. An invalid target is refused visibly rather than accepted and corrected afterwards. Escape during a drag returns the component to its origin and leaves nothing on the undo stack.
5. Resize handles sit on all eight edges and corners, snap to the grid, show a live outline, and never take a component below one cell in either axis.
6. A rubber band on empty canvas and a modified click both build a multi-select, and a multi-select move is **one** operation with **one** inverse, so it undoes in one step.
7. Every canvas mutation is an operation with a type, a payload and an inverse, from the closed set `add`, `remove`, `move`, `resize`, `reparent`, `set-property`, `bind`, `unbind`, `rename`. Undo applies the inverse; redo re-applies it.
8. The operation log survives a reload. Reopening an app replays it, so undo depth is not bounded by the session and twenty operations undone after a reload produce the same result as twenty operations undone before one.
9. Renaming a component rewrites the bindings that referenced it as part of the same operation, so undoing the rename restores the bindings too. A rename that leaves a binding pointing at a name that no longer exists is a contract violation.
10. **The persistence rule, and the one to get exactly right.** An app carrying at least four components at non-default positions is saved, the browser is closed, and the app reopens with every position, every size, every parent and every binding exactly as they were left. An app that reopens looking right and doing nothing, because positions were stored and bindings were not, fails this rule as completely as one that reopens empty.
11. Two builders in one app is an expected state. Presence is shown. A save whose base version hash is no longer current is refused, the current version and the conflicting operations are returned, and the losing builder is told what happened and shown the difference. Silently replacing the earlier save with the later one is a contract violation even when nothing is lost by luck.
12. Selection is not focus. A builder tabbing into the inspector keeps the canvas selection.
13. Every canvas operation has a keyboard path, and that path is stated in the interface rather than only in a help page. Selection moves by arrow key and resizes by modified arrow key.

### Components, the inspector and bindings

The library is grouped, searchable and keyboard reachable. Every entry declares its default size in grid units, its bindable properties with their types, its events, and the state it exposes to other components.

Groups and members: **Data** carries table, list, key-value, chart and statistic. **Input** carries text, number, date, select, multiselect, checkbox, switch, slider, file and rich text. **Layout** carries container, tabs, stack, modal, drawer, form, divider and spacer. **Action** carries button, icon button, menu and link. **Display** carries text, image, icon, badge, progress, avatar and timeline. **Navigation** carries breadcrumb, pagination, steps and sidebar.

1. Every component exposes its own state under its own name, so any other component can bind to it. A table exposes its selected row, its page, its sort and its filter. A form exposes its values, its validity and its submission state.
2. Every component that can be busy declares a busy state, an empty state and an error state. A grid with no empty state ships an empty grid that looks broken.
3. The inspector groups the current selection's properties in a fixed order: content, then data, then appearance, then interaction, then layout, then identity.
4. Every bindable field switches to an expression in place, with no dialog, and switches back with the last fixed value retained.
5. The resolved value and the resolved type of every bound field are shown under it, live. A builder must never have to run the app to find out what an expression evaluates to.
6. An inspector edit commits on blur and on enter, and reverts on escape. Committing on every keystroke fills the operation log with noise and makes undo useless.
7. A multi-selection shows the intersection of properties, marks the ones whose values differ, and applies an edit to all of them.
8. A binding is an expression evaluated against a scope of the app's queries by name, its components by name, the current row in a repeated context, and a small standard library. It reaches nothing else: not the host page, not the network, not browser storage.
9. The dependency graph between bindings is maintained, is acyclic, and is checked when the binding is made. A cycle is refused with both ends named. Changing one value re-evaluates only what depends on it. Re-evaluating the whole graph on every keystroke gives the same answers and makes the editor unusable at two hundred components.
10. A binding error surfaces on the component and in the inspector field that produced it, carrying the expression and the failure, never as a blank value.
11. Errors are told apart at three levels: an authoring error appears on the field, on the component badge and on a badge on every ancestor in the tree; a runtime error appears in the bound component's own error state and in the query panel; and losing the connection to the server puts up **one** global banner. Forty component-level error states for one connection loss have told the builder nothing and hidden the one real error that was already there.
12. An event handler is a declared action from a closed set, never a script: run query, set component property, navigate, open or close overlay, show notification, copy to clipboard, download, and trigger workflow. Handlers run in declaration order.
13. A failing handler halts the chain and reports which handler failed. Continuing the chain and then showing a success notification is a contract violation, and it is what a naive implementation does by default.
14. A form validates per field in the browser for feedback and at the server for truth. Submission is disabled while the request is in flight, driven by the request state and not by a timer, and a second submission is refused by the idempotency key rather than only by the disabled control.
15. A failed submission retains every value the user typed and attaches the error to the field the server identified. Navigating away from a dirty form warns, and the warning is reachable by keyboard.
16. A select bound to a query fetches asynchronously, searches at the server above a stated option count, settles before it searches rather than firing on every keystroke, keeps the selected value's label even when that value is not in the current page of options, and **does not lose the selection when the query re-runs**.

### The data grid

The table is the component the product is bought for, and every hard property of this build shows up in it.

1. Paging, sorting, filtering, searching and aggregation are executed by the resource. Fetching every row and doing the work in the browser is a contract violation. Over the seeded table of fifty thousand orders, one interaction produces one request, and no response ever carries the whole table.
2. Paging is by cursor where the resource supports it and by offset otherwise. No list endpoint anywhere in the product is unbounded.
3. Selection is held as row keys taken from the data, never as row indices, so a selection survives a refetch.
4. Rows and columns both render only what is needed to stay smooth at fifty thousand rows, the header never detaches from the body while scrolling, and a row's identity comes from the data rather than its position.
5. Columns resize per column, remember their width per principal per app, and offer a fit-to-content action. Leading columns pin, and the pinned region scrolls vertically in lock with the body.
6. Cell types and their treatment: text truncates with its full value available and wraps only when asked; number aligns to the trailing edge with thousands separated and its precision declared; **currency aligns to the trailing edge and is held as integer minor units, never as a decimal fraction**; date and time render in the viewer's zone with the zone shown where it matters; boolean is a checkbox, three-state where the column is nullable; an enumerated value is a badge with a declared tone per value; a link truncates with its target shown; JSON collapses to a summary and expands in place; an image is a thumbnail from a signed, expiring, single-object address; and an action cell is permission gated per row.
7. An edited cell is staged, not written. Staged changes are visible as staged, per row and per cell.
8. Staged changes commit by an explicit action, as one mutation, under one idempotency key. A failed commit retains the staged values and marks the failed rows with the reason.
9. A successful commit refetches rather than patching the local copy, because the resource may have applied defaults or rules of its own. Patching locally is faster and it is how the grid starts disagreeing with the database, silently.
10. A cell the acting principal may not write is not editable, and that refusal is decided by the permission layer rather than by a flag in the app definition.
11. The grid's states are distinct and all of them are specified: first loading shows skeleton rows at the configured page size with the header already correct; a subsequent load keeps the existing rows dimmed with progress shown in the header; empty with no filter explains what would appear there; empty with a filter names the filter and offers to clear it; denied states the refusal; an error shows the mapped failure with a retry that reuses the same parameters; and a truncated result carries an explicit banner naming the row cap that was hit.

### Versions, releases and environments

Two environments exist, ordered for promotion: `staging`, then `production`. `production` is protected.

1. An app version is immutable and content addressed. Saving edits a draft. Freezing a draft writes a new version with a `version_hash` that never changes and is never reused.
2. A release is an insert that points an environment at a version, carrying the promoter and the time. Nothing about a release is a boolean, and a release row is never updated or deleted.
3. Rolling back is promoting the previous version. It is the same operation, and it must be available without an edit.
4. A published app has a stable address that does not change across releases. A link an operator bookmarked survives every promotion.
5. While a builder edits a published app, an operator's running session continues to be served the released version. The operator sees the change only after the builder promotes it.
6. Promotion to `production` requires an approval granted by a principal other than the requester. Self-approval is refused even when the requester holds the grant to approve.
7. An approval is bound to the exact `version_hash` it was requested for. Any further edit produces a new hash and invalidates the approval; there is no such thing as an approval of an app.
8. An approval carries the reason given at request time, which is a required field, and it lapses if it is not acted on within its window rather than waiting indefinitely.
9. The same query run against `staging` and against `production` uses that environment's own credential set and returns that environment's own rows. The environment in force is visible in the editor at all times.
10. A principal may only execute in an environment its groups reach. A `builder` may promote freely to `staging` and never to `production` without an approval.

### Permission groups, grants and policies

Authorization is a layer with a single entry point. Feature code asks it a question and obeys the answer. Feature code does not contain the rule.

The one call, everywhere: a decision takes the acting principal with its type, its groups and its active grants; an action from the closed set `read`, `write`, `execute`, `publish`, `promote`, `administer`, `export`; the target object with its whole scope chain of workspace, app, environment and where relevant the column; and a context carrying the environment, the time, the source address and the request identifier. It answers `allow` or `deny`, **and a reason, on both**.

The resolution order is fixed and is not configurable:

1. Collect every grant reaching the principal: held directly, held through group membership, held through a nested group, or held through a time-bounded grant.
2. Discard every grant whose validity window does not contain the time of the request.
3. Discard every grant whose environment does not match the environment of the request.
4. If any surviving grant is an explicit `deny` for this action at **any** scope in the chain, the decision is `deny`. Deny always wins, and a narrower `allow` never overcomes it.
5. If any surviving grant is an `allow` for this action at any scope in the chain, the decision is `allow`.
6. Otherwise the decision is `deny`. The default is deny, at every scope, for every action.

Rule four before rule five is the whole design. A system where a narrow allow can overcome a broad deny cannot express "this group may never export", which is the first sentence every compliance review asks for.

Further rules the layer must hold:

1. A decision may be cached. The cache is keyed by principal, action, target and environment **and** by the version of every grant and policy that contributed to it, and it is invalidated by any write to a grant, a group membership, a policy or a principal's status, taking effect within a stated number of seconds. A session-lifetime authorization cache is a contract violation: it is how a removed member keeps access.
2. Removing a member from a group takes effect on that member's **next authorised action**, not on their next sign-in. A session already open loses the app it no longer reaches.
3. Every membership and every grant may carry a validity window, and expiry is enforced when the decision is made. A background sweep is a tidiness measure and never the mechanism, because a sweep that stops running leaves access open.
4. Elevated access is requested with a stated reason, granted by somebody other than the requester, bounded at grant time, and expires on its own. The elevated period is queryable afterwards as an interval: who, what, from when, to when, on whose approval, for what reason.
5. A row predicate is composed into the statement at the server before execution. Two principals in different groups running the same query receive different row sets, and neither can widen the set by editing a request parameter.
6. A column mask is applied at the server, on the single result path every reader shares: the rendered app, the raw result pane, a download, and any exported file. The masked value never leaves the server. Sending the value and starring it in the browser is a leak wearing a costume.
7. Masking is bound to the column's identity in the result, not to its name in the statement, so aliasing it, aggregating it or joining around it recovers nothing.
8. `export` is a separate action decided separately from `read`. A principal that may read may not thereby download.
9. An administrator can ask four questions and get an answer without reading code: what can this principal reach, who can reach this target, why was this decision made, and what changed in the matrix between two points in time. The answer to the third is the ordered rules that fired, ending on the one that decided, with the grant chain each came from.
10. Grants are versioned rather than updated in place, because "who could see this in March" is a question asked after an incident and a mutable table cannot answer it.

### Members and invitations

Inviting a member sends a real message over SMTP to Mailpit at `SMTP_HOST` and `SMTP_PORT`, using `SMTP_USER` and `SMTP_PASS`. This is the only message the product sends.

1. An invitation is addressed to the invited address and to nobody else: no cc, no bcc, one recipient.
2. The subject begins with `Girder invitation: ` followed by a space and the workspace name. For the seeded workspace the subject is exactly `Girder invitation: Northgate Operations`.
3. The body is not empty and names the workspace, the email of the inviting principal, and the acceptance address.
4. The invitation token is single use, time limited, bound to the invited address, and invalidated both when it is used and when the invitation is revoked. A second acceptance of the same token is refused.
5. Accepting an invitation for an address that already has an account adds a membership. It never creates a second account for the same address.
6. An expired token offers to request a fresh invitation and does not reveal whether the workspace exists.
7. Before accepting, the invitee sees the workspace name and the inviting principal.
8. After accepting, the member sees exactly the apps their group grants and no others.
9. The non-transition rule: revoking an invitation sends no message, accepting an invitation sends no message, changing a group's grants sends no message, and inviting an address that already holds a membership is refused and sends no message. Exactly one message exists per successful invitation.

### The audit trail

The trail exists so that a person who does not trust the operator can establish, later, what happened. It is not the engineering log, and the two are kept apart.

1. The store is append-only. No principal in the product holds update or delete on it, including the `owner`.
2. Recorded event classes, each on every occurrence: authentication, meaning sign-in, sign-out, failure and lockout; authorization, meaning every deny and every allow on a target carrying a policy, with the decision reason; query execution, meaning every execution against a resource carrying a policy and every mutating execution, with the query, the resource, the row count, the duration and the outcome and never the result; editing, meaning an app version created, a component changed, a query changed, a resource created or edited, with the version hash before and after; release, meaning a promotion, a rollback, and an approval requested, granted, refused or lapsed, with the environment, the version hash and the approver; identity, meaning a member invited, accepted or removed and a group membership changed, with the source of the change; permission, meaning a grant created, edited, revoked or expired and a policy version published, with the difference; secret, meaning a credential set, rotated, deleted or tested, carrying no part of the value; and administration, meaning a setting changed or a key issued or revoked, with the previous and the new value.
3. Every event carries the same envelope: an event identity, a sequence number that increases monotonically within the workspace, the time, the acting principal and its type, the source address, the request identifier, the session identity, the target object and its version, the outcome, and the hash of the preceding event.
4. The trail is tamper evident. Each event carries the hash of its predecessor, so altering or deleting one record breaks every link after it, and the break is evidence that something was altered rather than a suspicion. The chain head is anchored on a stated interval to a record the product itself cannot rewrite, so replacing the whole chain is detectable as well.
5. Verification is an operation an auditor runs and it returns the **first divergent sequence number**, not a boolean. A record altered directly in the store is detectable by that verification.
6. An event is written on the same transaction as the effect it records. An effect that commits without its event, and an event that commits without its effect, are both contract violations. This is the line between an audit trail and a log of things the application remembered to mention.
7. The trail is queryable by actor, by target object, by action, by outcome and by time window, in combination, with paging, and the export of a query result is itself an audited action.
8. An auditor session is read-only by construction. The `auditor` role holds read on the audit scope and nothing anywhere else, so an auditor cannot alter what it audits even by accident.
9. Retention is stated per class: audit events are kept for the configured compliance window and that window has a floor the operator cannot lower; query-run records are kept on a shorter, operational window; query results are not retained at all and no result cache outlives the request; and drafts and versions are kept per app with a configurable ceiling and a floor of the currently released version plus its predecessor.

### The public marketing surface

The public site is the argument for the product. It is dark on every route, declares itself dark so browser furniture matches, and has no light version.

1. The home route carries, in order: a hero with the headline, the announcement pill, the prompt composer, the import and connector strips and the video frame; a feature block of three pillars under one heading with a tab system; a value block of three columns under a second heading; a logo wall and result cards; two industry blocks; a second composer; three article cards; and the footer.
2. The four platform pillar routes are one template with different content. Each selects one of the eight accent families and wears it throughout, and the accent is the only thing that differs between them.
3. Every destination the header and the footer name resolves to a real page. A navigation promising forty-one destinations and delivering five is the defect this rule exists to prevent, and the not-found route is not an acceptable answer for a link the site itself renders.
4. Every figure quoted in the results band is attributed to a named customer. An unattributed claim about money saved is the most legally exposed element on a page like this.
5. The announcement banner carries a validity window and removes itself when it lapses.
6. Every image reference carries **alternative text** as a required field of the content record, not as an optional one filled in later. An image with no alternative text cannot be published.
7. Every route declares a unique title leading with the page and ending with the product, a meta **description**, a theme colour matching the page field, a dark colour scheme and a viewport declaration. The not-found route declares them too.
8. A `favicon` is served, and it is drawn from the same unit-square vocabulary as the icons.
9. A `sitemap.xml` lists every public route and a `robots.txt` names it. Neither lists a console route and neither lists an unpublished article.
10. An article in draft state is unreachable at any public address, by direct address and through the site search, and that is enforced where the data is read rather than by filtering a list afterwards.
11. Content is separated from presentation by a model of nine types: a page with a slug, a title, a description, a theme accent and an ordered band list; a band, which is one of the declared band shapes; an article with a slug, a title, an excerpt, a body, an author reference, a category reference, a published state, a published time and an illustration reference; an author with a name, a role, a biography and a portrait reference; a category with a slug, a name and a preview media list; a customer with a name, a mark reference, an industry and an ordered result list; a result with a figure, a claim, a customer reference and a link; a navigation record of ordered groups each carrying a label and ordered destinations; and an announcement with text, a link and an active window.
12. Navigation is content rather than code, and a destination resolving to nothing fails validation when it is published rather than when it is requested.
13. Publishing revalidates only the affected routes.

### The prompt composer

A large field at the centre of the hero, into which a visitor types a sentence describing an application they want. It is the site's primary self-serve funnel and its most expensive piece of interaction design.

1. Typing an at-sign opens a picker of data sources. The picker filters as the visitor keeps typing after the at-sign, is navigable by keyboard, and closes on escape without removing the at-sign already typed.
2. Choosing a source inserts a chip, and the chip is atomic. One press of backspace at its trailing edge selects it, a second removes it whole, and the caret can never land inside it.
3. A chip carries a reference, not a label. Renaming the source it points at changes how the chip renders and does not change the value the composer submits.
4. Chips survive a copy and paste round trip as chips.
5. The placeholder is also available as one unbroken sentence for assistive technology, because the visible sentence is broken into three elements by the chip.
6. Starter prompts are a menu of pre-written sentences that replace the field's contents.
7. Submitting the composer from the public site is a signup capture, not a build. The sentence and its chips are carried through and are the first thing the visitor sees on the next screen, so the promise the front page makes is kept by the screen behind it.
8. The composer never contacts a model from the public page and never sends its contents to an analytics destination.

### Demo request, subscription and search

1. The demo request form asks for exactly two things: a work email, validated as an address, and a reason chosen from three declared options. A consumer mail domain is accepted and recorded as one.
2. It answers with exactly one state from `sent`, `invalid`, `spam`, `failed`. On `sent` the confirmation replaces the form block. On `invalid` the field-level messages appear and the form is kept. On `spam` a distinct message appears and the form is kept. On `failed` a retry message appears and **every value the visitor typed is still in the box**. Losing a serious enquiry to a transient error is the worst thing this half of the product can do.
3. The consent line beneath the control states that submitting agrees to the privacy policy and consents to marketing communications, and it links the privacy route. Where the visitor's jurisdiction requires affirmative consent, the same line becomes an unchecked box and the submit stays unavailable until it is checked. Both forms exist in the build.
4. The newsletter subscription answers with exactly one state from `sent`, `invalid`, `already`, `failed`.
5. Both of these are limited per address and per source, and neither relies on a hidden field alone to refuse a machine that submits repeatedly.
6. Free text from either is stored and rendered as text and never as markup, everywhere it is later read.
7. Site search opens as an overlay from a header control and from the platform modifier with `K`, working from any route and not while a text field has focus. The header control carries the shortcut hint at zero opacity, revealed when the control is hovered or focused.
8. The search field settles before it runs rather than firing on every keystroke, cancels superseded requests, groups results by type, is navigable by keyboard with the active result always scrolled into view, and names what was searched for when there is nothing to show.
9. Escape, the scrim and the close control all close the overlay and return focus to the control it was opened from. The page beneath does not scroll while it is open.
10. Search indexes published public routes only. An index that can be made to return a draft is a content leak.
11. Search answers with exactly one state from `ok`, `invalid`, `failed`.

### The not-found route

1. Any address that resolves to nothing serves the not-found route with the full header and footer and the same document metadata as every other route.
2. The message names the path that was requested and then offers somewhere better. The interpolated path is rendered as text. A not-found page that reflects an unescaped path back into the page is a cross-site scripting vector and is the most commonly shipped one on the web.
3. The route carries a playable falling-blocks game with a title, a level readout starting at `1`, a match readout starting at `5` and a score readout starting at `0`.
4. The bindings are displayed on screen beside their action, not hidden in a help panel: `r` restarts, the left arrow moves left, the right arrow moves right, the down arrow drops and the up arrow rotates.
5. The same actions are available by touch on visible controls.
6. The game does not capture the arrow keys until it has focus and releases them on blur, so it never takes the scroll keys from somebody trying to reach the footer.
7. It stops when it is off screen and when reduced motion is preferred, and it never plays sound without an explicit control.
8. Its readouts are announced, so the score is available to somebody who cannot see the board.
9. The score is per session and stays in the visitor's own browser. It is not sent anywhere.

## User flow

### Routes

| Route | Purpose | Auth |
|---|---|---|
| `/` | home, the whole argument | none |
| `/platform/build` `/platform/launch` `/platform/scale` `/platform/govern` | one pillar template, one accent each | none |
| `/blog` and `/blog/:slug` | article index and article | none |
| `/demo` | demo request | none |
| `/search` | search results for a query string | none |
| `/pricing` `/use-cases` `/app-gallery` `/integrations` `/templates` `/utilities` `/customer-stories` `/videos` `/resource-hub` `/interactive-tour` | the Discover destinations | none |
| `/docs` `/community` `/university` `/api-reference` `/rpc-reference` `/cli-reference` `/hire-a-developer` | the Developers destinations | none |
| `/about` `/careers` `/partners` `/support` `/newsroom` | the Company destinations | none |
| `/terms` `/privacy` `/security` `/trust-center` `/changelog` `/status` `/site-map` | the Legal and trust destinations | none |
| `/capabilities/:slug` `/teams/:slug` `/industries/:slug` `/segments/:slug` | the Capabilities, Team, Industry and Type destinations | none |
| `/robots.txt` and `/sitemap.xml` | the crawler contract | none |
| `/signin` | sign in | none |
| `/invite/:token` | invitation acceptance | the token |
| `/console` | workspace home, the app card grid | any signed-in principal |
| `/console/apps/new` | create an app | `builder`, `owner` |
| `/console/apps/:appId/edit` | the four-region editor | `builder`, `owner` |
| `/console/resources` and `/console/resources/new` | the resource catalog | `owner` writes, `builder` reads |
| `/console/admin/members` | members, invitations, removal | `owner` |
| `/console/admin/groups` | groups, nesting, membership sources | `owner` |
| `/console/admin/permissions` | the grant matrix | `owner` |
| `/console/admin/policies` | row predicates and column masks | `owner` |
| `/console/admin/environments` | order, protection, approval requirement | `owner` |
| `/console/admin/audit` | the queryable trail and its verification | `owner`, `auditor` |
| `/console/admin/decide` | the permission answer for a chosen principal and target | `owner` |
| `/run/:appId` | a published app at its own address | any principal a group grants |
| anything else | the not-found route | none |

### Entry and redirects

An unauthenticated request for a console route or a run address lands on `/signin` with the requested address remembered, and a successful sign-in returns there. A sign-in with nothing remembered lands on `/console`. Signing out returns to `/` and the token stops working immediately. A token that expires mid-action leaves the work on screen, says the session ended and offers sign-in in place. A principal whose groups grant nothing on a console route is told plainly that the route is not theirs, and is never shown an empty version of it. An `operator` who reaches `/console/apps/:appId/edit` by typing it is refused: there is no route by which an operator reaches the editor.

### Journeys

1. Sign in as `owner@example.com`, open `/console/resources/new`, create a `postgres` resource named `Ledger Archive` from a host, a port, a database, a user and a password, run the test, and see it listed with its kind and the time it was last tested.
2. Sign in as `builder@example.com`, open `Order Desk` in the editor, author a read query named `orders_recent` against `Orders Warehouse`, run it, and read the rows, the row count and the duration in the result pane.
3. In the same editor, drag a table onto the canvas, bind it to `orders_recent`, drag a form beside it, bind it to `order_mark_delayed`, move and resize both, save, close the browser, reopen the app, and find every position, size and binding intact.
4. Submit the form with order `NG-1002`, watch the bound table refresh without a page reload, and find the changed row still changed after a hard reload.
5. As `builder@example.com`, freeze the draft into a version, request approval to promote it to `production` with a reason, try to approve it as the same principal and be refused, then sign in as `owner@example.com`, grant the approval, and promote.
6. Sign in as `operator@example.com`, open `/run/order-desk`, filter the orders table to `delayed`, sort by the placed time, page forward twice, and submit the form, seeing a toast confirm the write.
7. Sign in as `operator2@example.com`, open the same published app, and see a different, narrower set of rows from the same query, with `customer_name` masked, and no way to widen either by editing a parameter.
8. As `owner@example.com`, invite `newcomer@example.com` into `Support Desk`, then open the invitation from the mailbox, accept it, and see exactly the apps `Support Desk` grants.
9. As `owner@example.com`, remove `operator@example.com` from `Operations` while that operator has a session open, and watch the operator's next action on `Order Desk` be refused rather than served.
10. Sign in as `auditor@example.com`, open the trail, filter to the denials for `operator@example.com` in the last hour, run the verification, and read that the chain is intact from the first sequence number onward.

### States

Every list has an empty state that names what would appear there, and that state is visually and textually distinct from a refusal. Every route has a loading state; the console's loading state keeps the chrome and the header already correct. A refusal names the action and never the data it would have returned. An error carries the request identifier the visitor can quote and never ends the session or blanks the page. A form that fails keeps everything typed into it.

## UI/UX notes

The north star for the public surface: somebody arriving should understand within one screen that this is enterprise infrastructure built by people who value restraint, and should feel the thing is engineered rather than arranged. The north star for the console is plainer and it is comprehension: what this row is, who may touch it, and what has happened to it.

Two registers in one product, held apart deliberately. The public surface is a heavy-aesthetic marketing surface with a point of view and may carry atmosphere. The console is an operational tool: quiet, dense but organised, restrained, predictable, built for scanning and repeated action, with no oversized heroes, no editorial composition and no decoration standing in for content. Comprehension over atmosphere inside the console; conviction over neutrality outside it.

The public field is one near-black neutral with warm near-white type, and there is no light version of any public route. The console carries both a dark and a light theme and both are designed in full. Panels sit a shade above the field, recessed wells a shade below, and a hovered panel a shade above again, so a panel reads as separate from the page without needing a border. Two text tones below the primary carry secondary copy and unavailable copy, and unavailable is never signalled by colour alone.

Three colours carry meaning and appear nowhere else: one for something that has gone wrong, one for something that worked, and one for something still in progress. A state that is none of the three may not borrow any of them. Eight accent families exist as ladders from darkest to lightest, one each of blue, teal, orange, violet, indigo, red, amber and a yellow-green, and a pillar route wears exactly one of them and no other. A cyan-leaning tone is reserved for an expression inside the composer and appears in no other role. The exact shades are yours, so long as they hold those rules and the contrast floors below.

Type carries real contrast between voice and body. Headings are set at the lightest weight the family has, at large sizes, tracking tightening as size grows and opening as size shrinks, so a heading reads as a title rather than as loud body copy. Setting the headline voice any heavier is the single change that would most damage the register. Body sits a step heavier than the headline voice and there is almost nothing between the two. Two in-between weights exist that no static family can reach, one just above regular for small headings and one just below semibold for titles, so interface type never reads as either regular or bold. Figures line up in a column wherever amounts stack. A transitional serif with true italics is available for accents and a monospace family for identifiers and expressions.

Corners are softened on a short ladder rather than chosen per component, and a circular control expresses its radius as a value large enough to guarantee a semicircle at any height, so a pill never degrades into a rounded rectangle when its content wraps. There is almost no shadow: exactly one real shadow exists on the public surface, large and soft and falling a long way below the composer, which is what lifts it off a near-black page where a conventional shadow would be invisible. Everything else that must float is blurred behind instead.

Motion is one family reflected rather than nine curves chosen, and one of them carries the overwhelming majority of every transition, so the whole site moves like one object. Almost every state change lands faster than a reader perceives as motion; visible motion is reserved for a small number of named moments. Transform, scale and rotate animate as one group with one character, so a component never snaps under one interaction and eases under another. Three things move continuously and none is fast enough to read as an animation: a light creeps around the composer's border, a sheen crosses the placeholder text, and a strip of customer marks slides past. Speeding any of them to a normal animation speed would immediately cheapen the page. The signature moment is the link underline, which retracts to the trailing edge until it is gone, jumps its origin to the leading edge while invisible, and grows back out, so the link reads as being replaced rather than merely highlighted. Media arrives very slightly oversized and settles to its true size. A preference for reduced motion stops all three continuous animations entirely rather than shortening them, removes scroll-driven transforms and entrance animations, and preserves every state change as an instantaneous one.

Density is the register's tell. The public surface is spacious, with the gap between bands several times the gap beneath a heading and roughly halving on a narrow screen, every gap a multiple of one base unit that is yours to choose. The console is compact: rows sit tight so a full queue fits one screen, hit areas stay large, positions stay stable between loads, and chrome stays minimal because the same person does the same action forty times a day.

Accessibility is a floor, not a preference. Contrast meets WCAG AA for text, for interface components and for the focus indicator, in both console themes. Touch targets are comfortably sized. Every interaction is reachable by keyboard navigation with a visible focus ring that survives a high-contrast setting, every icon-only control carries an accessible name, and meaning is never carried by colour alone. Four surfaces need their own answer and get one: the canvas, whose accessible peer is the component tree rather than a fallback; the grid, which announces total rows rather than rendered rows; overlays, which move focus in, trap it and return it; and live regions announcing query completion, save state, validation failure and permission refusal.

Responsive behaviour is two problems, not one. The public surface is responsive in the ordinary sense across a phone tier, a tablet tier and a desktop tier, and the layout holds at every viewport width between them rather than only at the named breakpoint values; the header scales as one piece below the tablet tier rather than being re-typeset, so its proportions stay identical. The editor is a desktop instrument and says so: below its stated minimum width it refuses a phone layout in plain words and offers the fully usable preview instead, because a four-region editor crammed into a phone looks usable and is not. A published app is where the responsive work happens, because it is read on a phone in a warehouse.

Empty, loading, denied, error and truncated are five different states and they look different. An empty table and a table the principal may not see must never render the same way: "there are no orders" and "you may not view orders" are different facts, and merging them is how a permission defect hides for a year.

## Front-end specification

This section carries the visual specification in full. Nothing here restates a rule stated above; where a rule appears above it is not repeated here.

### The scaling rule

Every horizontal dimension on the public surface derives from one arithmetic rule over a single column count and a single base width, expressed as declarations rather than as their evaluated results. Two of the derived widths are themselves expressions over the other two. The content occupies all but two of the columns and the remaining two are split either side as the outer gutter. A site maximum width caps the field. Flattening the arithmetic to fixed values produces a layout that is correct at one width and wrong everywhere else, and it is the first thing to build because everything else derives from it. The column count, the base width and the ceiling are yours; deriving every horizontal measure from them is not.

Vertical rhythm is a multiple of one spacing unit. A hairline, narrower than one device pixel at ordinary densities, is a design decision rather than a rounding artefact: it is the border on cards, on table cells, on the logo wall and on the footer columns, and it is what stops a page of boxes reading as a page of boxes.

### The colour system, three layers

Layer one is the raw ladders. Two neutral ladders, one running from black up through near-black to a mid grey and one running from white down through a warm near-white to a muted grey, each at six stops. Eight accent ladders at seven steps each, in the order darkest, darker, dark, primary, light, lighter, lightest. A grey accent at five steps rather than seven. Two alpha ladders, one per neutral, at six and seven stops, and they are what every scrim, hairline and muted rule on the site is made of.

Layer two is the semantic surfaces, each named for its job rather than for its colour: the page field, a raised panel, a recessed well, a hovered or focused panel, primary text, muted text, unavailable text, inverted text, the expression colour inside the composer, a panel stroke, rules and dividers, the pale tile behind a customer mark, a text-selection background and its text, a lightbox scrim and a lightbox at rest. Three semantic state roles, critical, warning and success, at four steps each.

Layer three is the per-component state sets, and it is the layer that makes the interface read as considered. Every interactive component declares its full set rather than deriving hover from opacity. Two consequences are the reason the layer exists and both must be reproduced. The pressed state of every button takes its **text** colour to fully transparent while leaving its **icon** opaque, so a press reads as the label being punched out rather than the button dimming. And a text input inverts completely on focus, from transparent-on-dark with pale text to a solid pale field with dark text, which is a far larger state change than a focus ring and is the most recognisable interaction on the forms.

The components carrying a full state set are at minimum: the primary button, the tertiary button, the secondary button once per accent family, the navigation item with a default, hover, active and inactive state, and the text input with a default, hover and focused state. An icon inside a button takes the button's own icon colour and not its text colour, which is what makes the pressed state work.

The public surface declares itself dark, including its theme colour, so browser chrome, form controls and scrollbars match rather than rendering light widgets on a near-black page. The console redefines layer two per theme and leaves layers one and three untouched, which is the whole reason the layers are separated.

### Typography

Four roles. A grotesque with a continuous weight axis reaching from the very lightest to bold carries display and interface. The same family at two body weights carries running copy. A transitional serif with true italics carries accents. A monospace family carries identifiers, expressions and tabular figures. No licensed typeface ships. Where no open family with a continuous weight axis is available, round to the nearest available weight and record it as a known deviation rather than substituting silently.

The rendered scale has a small number of distinct steps and each one has a job: body copy as the default, a caption and label step, a small-caps eyebrow step set lighter than the caption, a card-heading step, a dense-interface step, a section-heading step at the lightest weight, a subheading step, a display step, a mobile display step, and a legal footnote step. Line height is generous at body sizes, tight at caption sizes and exactly the type size itself at display sizes. Tracking tightens as size grows and opens as size shrinks.

Every typeface declares a swap behaviour, the first-render faces are preloaded and subset, and the fallback stack is metrically matched so the swap does not move the layout.

### Radii, elevation and depth ordering

Corners run on a six-step ladder from barely softened to generously rounded. Beyond the ladder, in use: a small radius on logo tiles and badges, a slightly larger one on inline thumbnails, a medium one on secondary controls, a larger one on filter chips, a large one on the bordered promo box, a larger one still on the gradient-bordered composer, a pill radius on badges, and a hero video frame that is square at the top where it meets the header and heavily rounded at the bottom.

Three shadows exist in the whole public surface: a one-step spread ring on the logo tile, a very small offset shadow plus a half-step pale ring on the cursor label, and the one real shadow on the feature card and the composer, which falls a long way down with a great deal of blur at roughly a third opacity. Depth is otherwise carried by backdrop blur at four strengths: strongest on badges, medium on floating controls, lighter on one button, and lightest on the cursor label and the background figures.

Depth ordering, from the back: base, then raised, then sticky content, then overlay, then navigation, then frame, then modal, then the cursor, then the skip link. The cursor sits **above** the modal, which is the kind of ordering only ever discovered by opening a dialog and watching the cursor disappear behind it, and the skip link sits above everything, which is the only way a skip link works.

### Document structure for assistive technology

Structure is specified, not left to fall out of the markup. Each view declares one main landmark, a banner landmark, a contentinfo landmark, and navigation landmarks labelled individually where there is more than one. Each view carries exactly one first-level heading and skips no heading level below it. Every control carries an accessible name, and where the control has a visible label the accessible name matches it. The document declares its language, and any element whose language differs declares its own. Every route carries a unique title, leading with the specific page and ending with the product name.

### Breakpoints and capability queries

Named tiers, from large phone up through small tablet, tablet, small desktop, desktop, wide and very wide, with the tablet tier carrying by far the most declarations, plus a small number of narrow overrides below phone, below tablet and below small desktop. Two height queries also carry layout and they govern the hero, which fits itself to the viewport rather than to a fixed height.

The reference branches on **pointer capability** rather than on width for its hover treatments, and so does this build: a hover treatment is applied where a pointer can hover and is not applied where one cannot. A reduced-motion preference is a real branch in the stylesheet rather than an afterthought, and it has a stated behaviour in both its reduce and its no-preference forms.

### Iconography

Every icon is drawn as one-unit squares on a small integer grid rather than as curves, and every icon ships as inline geometry rather than as a file. This is the strongest single identity signal after the colour, it costs nothing, and an off-the-shelf icon set would quietly undo more of the character than any other substitution.

The set is small. A caret, drawn as a staircase of seven squares and deliberately open at its point, so it reads as a chevron of two diagonal arms rather than as a filled triangle; it is used on every navigation item with a submenu and rotated for direction, and rotated a quarter turn in the mobile back control. An action arrow, the most-used icon on the site, drawn as a staircase in two-unit steps, appearing inline after every link that leads somewhere, sitting optically on the text baseline rather than on the box baseline, and the only icon that moves. A search glyph, drawn as a true circle with a tail, which is the one legitimate exception to the square-drawing rule because a circle that small cannot be built from unit squares without looking like a mistake. A dismiss glyph that shares the action arrow's path exactly, rotated by the consuming component and shipped as one asset rather than two. A forty-two-square ornament tracing a diagonal of single steps with two squares repeated at each end of the run, which thickens the terminals without a second element, taking the current text colour so it inherits its card's. And the wordmark, a stepped mark in the same square vocabulary set to the leading side of the word, redrawn rather than reproduced, normative in its ratio and in the mark's position relative to the word.

Icon sizing by context: small in header navigation, larger inline in a link where it takes the current colour, small in the mobile menu at a muted alpha, largest as the feature card ornament, and small inside buttons where it takes the button's icon colour.

### Global chrome

**The header** is fixed to the top of every route at the full document width, transparent at rest so the hero video reads as full bleed, and acquiring a near-solid dark field once the page scrolls or once a menu opens, with the change carried by the site's default transition. Its height is a token, and a variant of that token adds the banner height so a route with a banner and a route without place their content identically relative to the header.

Header contents, leading to trailing: a skip link, visually hidden until focused and then pinned above everything; the wordmark linking home; three menus, `Solution`, `Audience` and `Resources`; two direct links, `Use cases` and `Pricing`; a search control labelled `Search` carrying its keyboard hint; a `Sign in` link; and the conversion pair.

**The expanded menu panel** is one shared panel, not three dropdowns. All three menus open it, it is positioned at the header's own height, spans the document width and animates as one object. Its content is three column groups whose headings are set in the small-caps eyebrow. The group labels are `Platform`, `Capabilities`, `Team`, `Industry`, `Type`, `Discover`, `Developers` and `Company`. The navigation shell is clipped slightly larger than itself in every direction, so the panel's own shadow and border escape the clip while its content does not; clipping at exactly the shell's bounds looks identical until the panel opens.

**The conversion pair** sits at the trailing end in tertiary and primary treatments, and the pairing is normative: `Book a demo` is the high-value action and is the **quieter**, darker of the two; `Start for free` is the low-friction action and is the loud pale one. Reversing them changes the funnel.

**The mobile header** collapses the three menus into a single full-height sheet below the tablet tier. The whole header's contents are scaled as one transform rather than re-typeset at a second set of sizes, which is why the phone header is proportionally identical to the desktop one rather than merely smaller. The sheet carries a `Back` control using the rotated caret, so a submenu is a push rather than an expand.

**The footer** carries five link columns, then the conversion pair, then a social row, then a legal row, then the copyright, then the display wordmark. Columns in order: `Platform`, `Capabilities`, `Audience`, `Resources`, `Company`, their headings in the small-caps eyebrow, separated by hairline rules. The display wordmark occupies the full width beneath all of it, set large enough that the word alone spans roughly two thirds of the viewport with the mark to its leading side. It is the last thing on every page and it is the signature.

**The banner** is a short strip above the header carrying one announcement and a link.

**Buttons** come in four treatments sharing one geometry and differing only in their colour set: primary, the site's one loud action; secondary, which exists once per accent family and is used on pillar routes; tertiary, the quiet companion to primary; and text with an arrow, which is inline in copy and is the most common of the four. Every treatment carries resting, pointed-at, pressed, focused and unavailable states, and every pressed state takes its label transparent.

### Motion, in detail

The easing family is one curve authored once and reflected, with an in-out form, an in form, an out form, three overshoot forms that push one control point past its bound, three softened forms, a sine form and a linear form. One of them, the in-out form, carries the overwhelming majority of declared transitions; if one decision in this section has to be right, it is that one curve applied everywhere.

Durations cluster at two poles. The overwhelming majority of state changes, colour and border on interactive elements, happen faster than a reader perceives as motion. A much smaller group, the transform group, is the site's one standard visible move. Between them sit a small-state-change duration, a paired transform-and-opacity duration and a large-element opacity duration. The distribution is the point: the site does almost all of its state change invisibly and reserves visible motion for a handful of moves.

Five transition groups are declared and reused: a default carrying colour and border on interactive elements; a fade carrying opacity on large elements; a move-and-fade pairing transform with opacity at one duration; a quick fade; and a colour set carrying text colour, background colour, border colour and outline colour together at one duration.

The three continuous animations, each infinite and linear: a gradient border travelling around the composer, a shimmer crossing the composer's placeholder, and a logo marquee. Their relative speeds matter more than their absolute ones: the marquee takes many times longer to complete one lap than the border takes to travel once around, and the shimmer sits between them.

The named moments, each of which must exist and none of which needs a number: a fade-in-up entrance that fades while rising a short distance, once, then stays arrived; a plain fade-in; a settle-in where media arrives very slightly oversized and relaxes to its true size, which is the cheapest expensive-looking thing in the set; a small horizontal bounce on pillar tab links; a progress bar that fills by scaling from nothing to full, with a paused counterpart expressed as an animation that goes nowhere rather than as a removed animation, so the element's animation state is identical in both cases and nothing reflows on pause; a gradient shift on badges and a longer-travel variant of it; a two-tone pulse on the critical badge; and four marquee variants, one for image strips, one for the logo grid, one for a partner strip travelling forward and one for its partner travelling back.

**The link underline is the one interaction to build carefully.** Both the link body and the underline carry the same shape: at the start the underline is at full width anchored to its trailing edge; at the midpoint it has collapsed to zero width against that trailing edge; a hair past the midpoint its anchor jumps to the leading edge while it is still invisible; and by the end it has grown back out to full width from the leading edge. That hair past the midpoint is the mechanism and it must survive: interpolating between the two anchors, or collapsing the two midpoints into one, produces a symmetric wipe that reads as nothing. The result is an underline that retracts to the trailing edge and re-emerges from the leading edge, so the link reads as being replaced rather than merely highlighted. The underline is drawn as a hairline-tall image in the primary text tone, with a muted variant in the secondary tone, and the arrow translates under the transform group at the same time.

The entire hover vocabulary of the public site is two treatments: an icon-bearing link drops slightly in opacity, and a text link moves its colour and its border colour from the primary text tone to the muted one. Both pseudo-elements, the arrow and the underline, shift with the parent; colouring only the anchor leaves the arrow at full brightness while the text dims, which is the defect this note exists to prevent.

### The scroll system

Far less responds to scroll than a reader expects, and the restraint is the design: roughly a dozen selectors on the home route at desktop, fewer at tablet and fewer again at phone. Everything else is simply there.

Scroll effects are implemented **locally**, against the element's own intersection with the viewport, and never by writing a scroll state onto the document element. There is no scrolled class, no menu-open class and no scroll-direction class on the root, and adding one invents a mechanism the design does not have and produces different behaviour the moment two effects disagree. The document does carry a scroll padding equal to the header height token, so an in-page anchor lands below the fixed header rather than behind it, and it is derived from that token rather than duplicated.

**The hero video ramp** is the most elaborate effect and the one worth building carefully. Blur and opacity ramp together and continuously with scroll position, from perfectly sharp at full opacity to heavily blurred at low opacity, driven by position rather than by a stepped set of classes. Its frame is square at the top where it meets the header and heavily rounded at the bottom, and the video inside it is masked by a vertical gradient at the top so it dissolves into the header rather than ending at a line. The only element continuously scrubbed by scroll rather than played once on entry is a bobbing glass illustration, which drifts as the reader moves.

**Three masking families** are reused. A vertical soft edge on scrolling panels, fading in at the top and out at the bottom over a short distance. A horizontal soft edge on marquee rows. And a wide horizontal edge on a full-width marquee. The horizontal masks push their opaque region **beyond** the element's own bounds, which produces a fade wider than the element that therefore begins outside it, and the distance is derived from the element rather than authored; the fade width is carried as a custom property so one declaration serves every width.

**The vertical scrim** over the hero is a multi-stop gradient with an accelerating alpha curve, from fully transparent to solid in roughly nineteen stops, and it is a hand-tuned approximation of a perceptual fade rather than a linear one. A two-stop linear gradient in its place produces a visible band across the hero, which is exactly the artefact the many stops exist to remove. A second instance of the same construction exists over a pale field.

**The grid lines** drawn across some sections are a decorative figure of vertical rules at three densities in the teal accent primary, and the two fractional spacings are the column grid evaluated at two viewport widths. The rules are the layout grid briefly made visible rather than an unrelated pattern, and the same construction exists in the vertical direction.

### The prompt composer, treatment

A generous radius, the page field as its background, the muted text tone for its placeholder, and the one real shadow on the site. Its border is a moving gradient **constrained to the border region**, produced by compositing two masks so that only a ring of exactly the border width survives, following the corner radius, through which the gradient shows. Drawing the gradient on a parent and covering its middle with an opaque child works until the card sits over anything other than a flat colour, which on this page it does. The border is not interactive.

The placeholder shimmer is authored backwards from the obvious way: the travelling band is a **hole in a dark overlay** in the page's own colour rather than a bright streak, so on a near-black page it reads as the words quietly brightening and dimming rather than as a glare passing over them. It stops on focus, because a sheen crossing text somebody is typing is a nuisance rather than a flourish.

The chip renders the at-sign as its own element so it can be styled apart from the name, the name in the composer's expression colour and underlined, and the source's mark inside a fully circular container. Below the composer sit a starter-prompts menu, a circular submit control at the trailing edge at pill radius, an import strip and a connector strip. Both strips render a horizontal cluster of overlapping source marks to the leading side of their label, each at a small radius with the leading one on top.

### Marquee and logo systems

Horizontal infinite scrolling is one design-system component with several instantiations, not six separate implementations. The track's contents are duplicated so the wrap point is invisible, the track measures itself and writes its own travel distance to a custom property with a fallback that covers the exactly-duplicated case, the animation is applied to the **track** and never to each item, and the row is masked at both edges by the horizontal soft edge so items enter and leave through a fade rather than at a hard boundary. Duration is derived from content width so rows of different lengths travel at the same apparent speed; giving two rows the same duration at different widths makes one of them visibly race, and that is the defect this rule prevents. Under reduced motion the animation stops entirely and the row becomes a horizontally scrollable region so its content is still reachable.

The instantiations are the home route's customer wall, a second denser logo grid, image strips on pillar routes, blog category previews, an app gallery row which is the slowest on the site, and a pair of partner strips travelling in opposite directions at the same duration. The paired strips are deliberate: two rows in opposition read as depth with nothing actually three dimensional.

The logo tile carries a small radius, the pale tile background, a one-step spread ring and a hairline border. Customer marks are monochrome silhouettes on the pale tile rather than full-colour logos, and every mark is redrawn from between six and fourteen unit squares on the icon grid, with the density varied between marks so the wall does not read as one repeated shape. No mark ships as a file and no mark reproduces a real trademark.

**The feature tab system** on the home route has a vertical tab list on the leading side, a progress bar per tab that fills by scaling, automatic advance on completion, and a cross-fading panel on the trailing side. Its manners are normative: the timer pauses on hover, on focus anywhere within the block, and while the block is out of the viewport; selecting a tab by hand stops the automatic advance for the rest of the session rather than resuming after the current interval; the tab list is a real tab list for keyboard and assistive technology while the progress bars are decorative rather than announced; and the paused state is an animation that does not progress rather than a removed one.

### The cursor system

The pointer is replaced by a drawn cursor carrying a contextual label, in four named states each declared as a full colour set: default, hover, active and message. The active state is the one to read carefully: its cursor stroke goes to the same value as its fill, so the drawn cursor loses its outline and becomes a solid pale shape at the moment of pressing, while its label **gains** a stroke. The emphasis moves from the pointer to the label.

The drawn shape is offset slightly in both axes so it centres on the true pointer position, and the outer ring is parked far off the element when idle rather than hidden by a display change. The label carries a light backdrop blur, a small radius, a tiny offset shadow plus a half-step pale ring, and, crucially, it **follows the pointer under a transition rather than being positioned per frame**. That fraction of a second of lag is the entire effect: a label pinned exactly to the pointer feels glued to the mouse, and a label arriving a beat late feels like it has weight.

What the cursor must not break: it is enhancement only and does not render at all where the pointer cannot hover; the real cursor is hidden only over regions the custom cursor covers, so text inputs, text selection and native controls keep their own; it never renders during a text selection drag; it sits above the modal layer; it is not focusable, is hidden from assistive technology, and carries no information that is not also available another way, because a label that exists only inside the cursor is information a keyboard user cannot reach; and under reduced motion it stops following, so the label snaps rather than lagging.

### Route compositions

**Home** is the longest page on the site by an order of magnitude and is the argument in full; every other public route is a chapter of it. Its hero carries the headline at display size on one line at desktop, the announcement pill, the composer, the strips and the video frame, with a pause control at the frame's leading edge and a film link at its foot carrying two-tone copy. The hero sizes itself to the viewport through height queries rather than to a fixed height. The video is decorative, muted, looping and carries a visible pause control; it does not autoplay on a metered connection or under reduced motion, its poster frame is generated rather than shipped, and a pause persists for the session. The announcement badge is a pill carrying a wide-gamut gradient at half opacity over the page with a backdrop blur, animated by a slow gradient shift, which is why it reads as a tinted pane rather than as a coloured pill; it is authored in the wide space with an explicit narrower fallback declared after it. A second, flat badge treatment in a deep teal carries the `New` marker in the navigation. The feature block pins three pillars against a media panel that cross-fades with the active pillar. The results band is a logo wall of six customer marks in a hairline-ruled grid followed by result cards, each a large figure, a claim and a link carrying the arrow, plus media cards at a small radius with the tile ring. Two industry blocks of identical shape follow. The closing band carries a second composer pre-filled with a different sentence and a newsletter control, and it sits at the foot of a very long page on purpose: it catches the reader who read the whole argument. Three article cards close it, the first set larger than the other two in an asymmetric grid.

**The pillar template** carries a hero with an eyebrow, a headline, a paragraph and the conversion pair; a capability grid; a media strip; an integration wall; customer proof; a conversion band; and the footer.

**The blog index** carries a horizontal category strip with a preview marquee, one featured article at larger scale, and the remainder in a hairline-ruled grid, each card an illustration, a headline and a byline in the small-caps eyebrow, with cursor-based pagination.

**The demo route** places the form beside a proof rail carrying two customer results and a claim about the number of companies using the product, under the same attribution rule as the results band. A return control at the foot of the route scrolls back to the form, carrying an upward arrow, and appears only once the form has left the viewport.

**The search overlay** sits over a scrim with a raised panel background and a panel stroke, above the modal layer, its field inverting on focus exactly as every other input does.

**The not-found route** carries the full header and footer and the same metadata as every other route, and the game board's cells reuse the unit-square vocabulary in the accent ladders.

### The copy deck

These strings are content facts and are reproduced exactly.

| Slot | String |
|---|---|
| Skip link | `Skip to main content` |
| Mobile back | `Back` |
| Menu 1 | `Solution` |
| Menu 2 | `Audience` |
| Menu 3 | `Resources` |
| Link | `Use cases` |
| Link | `Pricing` |
| Search control | `Search` |
| Link | `Sign in` |
| Tertiary button | `Book a demo` |
| Primary button | `Start for free` |
| Home headline | `Secure your vibe-coded apps` |
| Announcement badge | `New` |
| Announcement | `Explore the new Girder app builder for free` |
| Composer placeholder, first part | `Build an order management tool that tracks all orders from the order management` |
| Composer chip | `@Girder Database` |
| Composer placeholder, second part | `and flags an order if it is delayed by more than 3 days.` |
| Composer menu | `Starter prompts` |
| Import strip | `Import apps built in other platforms` |
| Connector strip | `Build via MCP` |
| Film link, muted half | `See what's new.` |
| Film link, bright half | `Watch the film` |
| Feature heading | `Apps that mean business` |
| Feature link | `View app gallery` |
| Pillar heading | `Build powerful apps from anywhere` |
| Pillar 1 title | `Girder app builder` |
| Pillar 1 body | `Describe what you want and get a full, production-ready app with enterprise security and governance built in.` |
| Pillar 1 link | `Learn about the app builder` |
| Pillar 2 title | `MCP server` |
| Pillar 2 body | `Build an app from your favorite AI coding agent and deploy it here within your governed Girder environment.` |
| Pillar 2 link | `Read the MCP server docs` |
| Pillar 3 title | `Import React code` |
| Pillar 3 body | `Deploy apps built in Beacon, Loom, and other platforms. Upload a ZIP file or sync with Quarry.` |
| Pillar 3 link | `Read the app import docs` |
| Second heading | `Securely connect to your production data` |
| Second body | `Every app you build connects directly to your production data sources. Access is governed by your existing permissions, no extra configuration required.` |
| Second link | `See the full list of integrations` |
| Third heading | `Ship safely, with governance built in` |
| Third body | `Deploy with auth, access controls, and audit logging already in place. Fast to production, without sacrificing security.` |
| Third link | `Learn about security and governance` |
| Value heading | `Why enterprises choose Girder` |
| Column 1 title | `Production-ready from day one` |
| Column 1 body | `Don't choose between moving fast or shipping something that'll actually pass a security review. What you build in Girder is enterprise-grade from the start, no rebuild, no audit scramble, no IT veto.` |
| Column 2 title | `From one great app to operational excellence` |
| Column 2 body | `Point solutions help you build apps. You change how your business operates with Girder. One platform to manage, orchestrate, and scale everything you build.` |
| Column 3 title | `More teams building, no new risk` |
| Column 3 body | `Business teams move fast, IT keeps full visibility, and governance is centralized. That's the foundation that makes app generation actually work.` |
| Logo wall heading | `Trusted by 10,000+ teams to generate production-ready AI applications` |
| Result 1 | `Northgate saved $8M and 20,000+ hours` |
| Result 2 | `10x reduction in dev time across 1600 studios` |
| Result 3 | `10x increase in patients treated` |
| Result 4 | `Bellweather saved $6M and 36,000+ hours` |
| Result 5 | `$3M+ profit generated and 80% faster development` |
| Result link | `Read story` |
| Industry 1 title | `For supply chain solutions` |
| Industry 1 body | `The leading manufacturers and logistics companies use Girder to modernize operations across warehouses, fulfillment centers, and global supply networks.` |
| Industry 2 title | `For financial services solutions` |
| Industry 2 body | `The leading banks and fintech companies use Girder to modernize operations without compromising compliance.` |
| Closing heading | `Start today` |
| Closing composer placeholder | `Build me a revenue dashboard that visualizes sales trends across product categories using my @Ledgerline data` |
| Newsletter heading | `Get the latest from Girder` |
| Article 1 | `Ship vibe-coded apps to production` |
| Article 1 byline | `By Dana Whitfield` |
| Article 2 | `What happens after AI builds your prototype?` |
| Article 2 byline | `By Sam Okonjo` |
| Article 3 | `3 questions that tell you whether you're actually governing AI` |
| Article 3 byline | `By Riley Vance` |
| Demo heading | `Book a Girder demo` |
| Demo body | `New to Girder? Schedule a 1:1 session with an expert from our team to learn more.` |
| Demo field label | `Work Email` |
| Demo field label | `Reason for demo` |
| Demo select placeholder | `Select reason` |
| Demo option 1 | `Explore Girder Enterprise` |
| Demo option 2 | `Explore a Girder Use Case` |
| Demo option 3 | `Professional Services` |
| Demo submit | `Book a demo` |
| Consent, first part | `By submitting this form, you agree to our` |
| Consent, link | `privacy policy` |
| Consent, second part | `and consent to receiving marketing communications from Girder.` |
| Demo proof 1 | `Develops 50x faster with Girder` |
| Demo proof 2 | `Saved $8M and increased efficiency by 20%` |
| Demo proof 3 | `Over 10,000 companies from startups to the Fortune 500 use Girder to run their business.` |
| Demo return control | `Return to form` |
| Not-found action | `Go to homepage` |
| Game title | `404 Blocks` |
| Game readout | `Level: 1` |
| Game readout | `Match: 5` |
| Game readout | `Score: 0` |
| Game control | `Restart` |
| Game control | `Move Left` |
| Game control | `Move Right` |
| Game control | `Drop` |
| Game control | `Rotate` |
| Footer copyright | `(c) Girder 2026` |

The not-found message names the requested path and then offers somewhere better, in the shape `The page "/404" wasn't found... Let's find a better place.` with the requested path interpolated and rendered as text.

Navigation group members, reproduced as content: `Featured` carries `AI app security`. `Platform` carries `Build`, `Launch`, `Scale`, `Govern`. `Capabilities` carries `Agents`, `App builder`, `AI primitives`, `Workflows`, `Database`, `External apps`, `Mobile apps`, `Self-hosting`, `AppGen`. `Team` carries `Data`, `Engineering`, `Operations`. `Industry` carries `Financial services`, `Manufacturing`. `Type` carries `Enterprise`, `Startups`. `Discover` carries `App gallery`, `Integrations`, `Templates`, `Utilities`, `Blog`, `Customer stories`, `Videos`, `Resource hub`, `Interactive tour`. `Developers` carries `Documentation`, `Community`, `Girder University`, `API reference`, `RPC reference`, `CLI reference`, `Hire a developer`. `Company` carries `About`, `Careers`, `Partners`, `Support`, `Newsroom`. `Legal` carries `Terms of use`, `Privacy policy`, `Security`, `Trust Center`, `Changelog`, `Status`, `Site map`. The `App gallery` entry carries the `New` badge. The footer's `Capabilities` column carries `AI app security` as a tenth entry and orders the column differently from the header's; both are reproduced as given and the difference is not an error to normalise.

Each pillar link is rendered in two elements so its final word cannot wrap away from its arrow, breaking after `app`, after `server` and after `import` respectively. That is art direction, not an accident.

The six customer names are `Northgate`, `Bellweather`, `Halcyon`, `Trestle`, `Vantage` and `Ironwood`. The three article authors are `Dana Whitfield`, `Sam Okonjo` and `Riley Vance`. The five partner products named in the strips are `Beacon`, `Loom`, `Quarry`, `Pilot` and `Anchor`. The payment provider named inside the closing composer's sample sentence is `Ledgerline`.

### Generated assets

No typeface file, photograph, icon file, texture, video or logo file ships. Everything is generated or drawn.

The hero video frame is filled by a generated animation in four layers: the multi-stop vertical scrim as the ground; two radial gradients at the lower corners, one cool and one warm, authored in a wide colour space with a narrower fallback declared after; a slow drift of both radial centres at a period no shorter than the gradient border's lap, so it reads as light rather than as animation; and a fine tiling noise at low opacity over it. The poster frame is the first frame of that, rendered once. Do not reconstruct a product screenshot: a generated field of slow coloured light in the site's own palette is closer to the intended effect than a poor imitation of an interface.

The grain is a tiling noise texture produced as an inline filter, fine rather than coarse, with several octaves for tonal variation and its saturation removed so there is no colour speckle.

Article and category illustrations are generated placeholders keyed by a seed derived from the article's slug, composed from two accent ladders so the grid of cards reads as one family, with their dimensions declared in the markup so nothing shifts when they render.

## Technical requirements

The browser receives a static production bundle on first paint and every subsequent fact arrives as JSON from the same origin under `/api`. The backend is **NestJS** on Node 20, serving that JSON API. The frontend is **Vue 3** built by **Vite** into the production bundle. The datastore is **PostgreSQL**, reached at `DATABASE_URL`. Mail is **Mailpit**, reached over real SMTP at `SMTP_HOST` and `SMTP_PORT` with `SMTP_USER` and `SMTP_PASS`. Authentication is implemented by the app itself: email and password, hashed passwords, bearer tokens on every request except sign-in, `GET /api/health` and the three unauthenticated marketing endpoints. `GET /api/health` returns `200` once the app is ready.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor: the only backing services available in this environment are PostgreSQL and Mailpit, and reaching for anything else is a contract violation.

The backing services above are **already running** at those environment variables. They must not be downloaded, installed, compiled or started. Never hardcode a host or a port; read every one of them from the environment, including `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`.

**Module architecture: three bundles, one repository.** The marketing surface, the authoring studio and the published-app runtime are three deployable surfaces and the boundary between them is a requirement rather than a preference. An end user's session must not receive editor code: a principal who only runs published apps downloads nothing from the authoring surface. It is partly a weight argument and mostly a surface argument, because code that was never sent cannot be driven.

The layering is four layers deep and dependencies point one way only. The design system holds tokens, primitives and icons and has no product knowledge. The runtime holds components, bindings and the query client and has no editor knowledge. The editor holds the canvas, the inspector and the operation log and depends on the runtime. The server holds the API, the authorization layer, the resources and the audit trail and knows nothing about any client. The build fails on an upward import rather than documenting the layering rule in a readme.

A small number of primitives are worth naming because each one must exist exactly once rather than being reimplemented per screen: a token provider exposing the design tokens and resolving the theme; a reveal primitive carrying the scroll-triggered entrance, one implementation used everywhere; a query client owning execution, cancellation, de-duplication, retry policy and cache keying; a binding primitive owning parsing, dependency registration, sandboxed evaluation and a typed result; an operation log owning append, invert, replay and rebase; an advisory decision primitive mirroring the server's answer for the sole purpose of hiding controls, named advisory where it lives so no later contributor reaches for it as a guard; an audited-action wrapper binding a mutation and its audit event to one transaction boundary; and a row and column windower for the grid.

**State placement.** Server state is refetched and never treated as durable in the browser. An app definition lives on the server as immutable versions. Draft edits live in the synchronised operation log and survive a reload. A component's runtime state is keyed by component name and survives a route change within the app. Editor view state is local per principal per app. The session is carried by a bearer token. No product state is held in a module-scope singleton: the runtime must be able to mount two apps in one document, for the editor's preview and for an embedded case, without them sharing state.

**Advisory client decisions.** The client may hold a copy of a permission decision for the sole purpose of hiding a control the principal cannot use, so the interface is not a field of dead buttons. That copy is advisory, is named as advisory where it lives, and is never enforcement. Every consequential action is decided again at the server.

**Performance bounds and their reference conditions.** The marketing surface and the product are measured against different things on purpose, because one budget for both is how a product gets optimised for a page score while the grid stays slow. Every performance bound below is stated against a four-year-old mid-range laptop, a deliberately slowed connection, an app of two hundred components and thirty queries, and a table of fifty thousand rows. A bound without its conditions is a wish.

- The marketing surface is measured on time to first meaningful paint and on the absence of layout shift after it from anything the build controls. The initial compressed payload has a stated cap and the cap is enforced in the build. Media below the fold is deferred with its dimensions declared. Anything third-party loads after interaction or after consent and never blocks first paint.
- The editor is measured on interaction latency. Dragging and resizing track the pointer without dropping frames. A selection change repaints only the previously and newly selected subtrees. Only the downstream part of the dependency graph re-evaluates. The tree renders only the rows in view. A save transmits operations rather than the document, so its cost is proportional to what changed. The canvas is interactive before every query has returned, and a query still in flight renders its component in a loading state rather than blocking the canvas.
- The runtime is measured on the time from entering a route to the first useful row, and the resource's own duration is reported separately from the platform's, so a slow customer database is never mistaken for a slow product.
- Memory stays bounded across a long editing session. An operation log that grows without compaction is a leak with a good excuse.
- Server-side, the permission decision is bounded and is never made per row; a per-row permission check is the named anti-pattern here. Every list endpoint pages by cursor and none is unbounded. An audit write happens on the transaction of the effect and is bounded.

**Quota and fair share.** Concurrent executions per workspace are bounded, and beyond the bound a request queues and then answers `quota_exceeded` with the time the bound resets. Executions per principal per minute are bounded the same way and the principal is named in the audit event. Rows per result are capped per resource and a capped result is flagged as truncated in the response rather than silently shortened. Request and response payload sizes are bounded and are rejected at the edge before parsing. Scheduling between workspaces is fair share rather than first come: one workspace saturating its own bound must not degrade another's latency or success rate.

**Error mapping.** A resource's errors are mapped before they leave the server, and the mapping is part of the build. An authentication failure at the resource maps to `unreachable`, telling the actor the resource name and that its credentials were refused. A host resolution or network failure maps to `unreachable` with the resource name. A statement syntax error maps to `failed`, with host, port, user and database elided from the message. A constraint violation maps to `failed`, carrying the constraint's human name where the schema provides one. A statement timeout maps to `timeout` with the bound that was exceeded. A permission refusal inside the resource itself maps to `failed` and stays distinct from the platform refusing, because "your database said no" and "we said no" are different facts and merging them makes both permission systems undebuggable.

**Observability, which is not the audit trail.** A request identifier is generated at the edge, propagated across every boundary, attached to every log line and returned to the caller on every error so a person can quote it. Logs are structured and isolated per workspace. Personal data never appears in a log line: parameters are logged by name and type, never by value, and result rows are never logged. Metrics are recorded per workspace, per resource and per query, covering rate, error rate, duration distribution and quota consumption, with high cardinality on workspace and resource treated as a requirement rather than an accident. Alerting is bound to stated objectives on the query path and the editor save path, because an outage of those two is what an outage of this product means. Query cost is attributable to a workspace, a folder and an app. The trail answers who did this and is kept for years; this answers why this is slow and is kept for weeks, and merging them produces a system too noisy to audit and too expensive to keep.

**Response headers.** Every response carries a **security header** set: a content security policy that forbids inline script, a strict transport policy, a frame-ancestors refusal, a referrer policy, a nosniff declaration and a permissions policy. Free text that reaches a page is rendered as text.

**Idempotency.** Every mutating call that crosses a boundary carries an idempotency key derived from the logical operation, never from the clock and never from a value generated at send time, because both defeat the retry they exist to protect. Keys are retained at least as long as the longest retry window, and a repeated key returns the first result rather than executing again.

**Crawler contract.** `sitemap.xml` is generated from the published public routes, `robots.txt` names it, a `favicon` is served, and every route carries a title and a meta `description`.

## Data model

Roughly two dozen tables. All timestamps are UTC, and calendar-day logic uses server-side UTC "today".

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

Money is held and computed in **integer minor units** of `usd`, never as a decimal fraction. `amount_minor` is a count of cents: `$1,245.00` is `124500`, not `1245.00` and not `1245`. A total that is a penny out in front of a finance team ends the tool's credibility.

### principals

`id`, `email` unique, `role` one of `owner`, `builder`, `operator`, `auditor`, `password_hash`, `status` one of `active`, `removed`, `created_at`. The wider principal model the platform reasons about carries six types, `user`, `group`, `service_account`, `agent`, `workflow` and `installation`, and a principal's type is recorded on every grant and every audit event. Two rules hold whatever the type: an `agent` never holds a grant its delegating `user` does not hold, checked when the grant is resolved rather than when it is assigned, because the delegator's rights can shrink afterwards; and a `service_account` is never a member of a group whose grants were authored for interactive users, so a human-facing permission change cannot silently widen a machine's reach.

### groups, group_members

`groups`: `id`, `name` unique, `parent_id` nullable and self-referential, `created_at`. Nesting is depth limited and checked for cycles when it is written. `group_members`: `group_id`, `principal_id`, `source` one of `manual`, `invitation`. The source of every membership is shown wherever membership is shown.

### environments

`id`, `name` unique and one of `staging`, `production`, `position` which fixes the promotion order, `protected` boolean. `production` is protected.

### resources, credentials

`resources`: `id`, `name` unique, `kind`, `host`, `port`, `database`, `username`, `created_by`, `created_at`. A resource holds **no** secret; it holds a reference to one. `credentials`: `id`, `resource_id`, `environment_id`, the stored secret, `set_at`. One credential set per resource per environment, and the `production` set is permissioned independently of the `staging` one. The stored secret is encrypted at rest under a per-workspace key, and the key that encrypts it is not the key that opens the database, so a database copy alone yields nothing. A credential field is derived for display as a set indicator and a replace action; its value is never a field of any response.

### apps, app_versions, app_drafts, components, queries

`apps`: `id`, `name` unique, `slug` unique, `folder`, `created_by`, `created_at`. An app is a container, not a version.

`app_versions`: `id`, `app_id`, `version_hash` unique, `definition`, `created_by`, `created_at`. A row here is never updated. `version_hash` is derived from the definition's content, so two identical definitions produce one hash and any edit produces a different one.

`app_drafts`: `app_id`, `base_version_hash`, the ordered operations, `updated_by`, `updated_at`. A draft is a mutable pointer at a chain of operations; a version is the frozen result of that chain. Autosave writes a draft and never a release.

`components`: `id`, `app_version_id`, `name` unique within its version, `kind`, `column_start`, `row_start`, `column_span`, `row_span`, `properties`, `parent_id`, `position`. Every span is a whole number of grid units.

`queries`: `id`, `app_version_id`, `name` unique within its version, `resource_id`, `statement`, the declared `parameters` with their types, `mutating` boolean.

### query_runs

`id`, `query_id`, `principal_id`, `environment_id`, `row_count`, `duration_ms`, `outcome`, `idempotency_key` nullable, `started_at`. It records that the run happened, who ran it, against what, for how long and with what outcome. It **never** stores the result, because storing results turns the run log into a shadow copy of the customer's database with none of its access controls.

### releases, approvals

`releases`: `id`, `app_id`, `app_version_id`, `environment_id`, `promoted_by`, `approval_id` nullable, `promoted_at`. Inserted only. The release in force for an environment is the newest row for it, so rollback is another insert.

`approvals`: `id`, `app_id`, `version_hash`, `environment_id`, `requester_id`, `approver_id` nullable, `reason` required, `decision` one of `pending`, `granted`, `refused`, `lapsed`, `decided_at` nullable, `expires_at`. The invariant: no row may carry the same value in `requester_id` and `approver_id`, and a `granted` row is only usable for a release whose `app_version.version_hash` equals the approval's `version_hash`. Both must hold under concurrent requests, so two promotion attempts racing on one approval produce exactly one release and the other is refused with the state unchanged.

### permissions, policies

`permissions`: `id`, `principal_kind`, `principal_id`, `scope_kind` one of `workspace`, `folder`, `app`, `environment`, `column`, `scope_id`, `action`, `effect` one of `allow`, `deny`, `valid_from`, `valid_until` nullable, `version`. A grant is an edge with an effect, never a role string on a principal. A row is superseded by a new version rather than updated in place, so the matrix as it stood at any past moment is recoverable.

`policies`: `id`, `name`, `resource_id`, `group_id`, `row_predicate`, `masked_columns`, `version`, `published_at`. Versioned and published, with a preview against a chosen principal available before publishing.

### invitations

`id`, `email`, `group_id`, the stored token, `invited_by`, `expires_at`, `accepted_at` nullable, `revoked_at` nullable. One unaccepted invitation per address at a time; a second request for an address that already holds a live invitation or a membership is refused. A token is usable exactly once: two simultaneous acceptances of one token produce exactly one membership and the other is refused, with no partial state left behind.

### audit_events

`id`, `sequence`, `actor_id`, `actor_kind`, `action`, `target_kind`, `target_id`, `outcome`, `reason`, `request_id`, `source_address`, `session_id`, `occurred_at`, `previous_hash`, `event_hash`. Append only. `sequence` increases strictly with no gaps within the workspace, and `previous_hash` equals the immediately preceding row's `event_hash`. `event_hash` covers every other column in the row including `previous_hash`, so one altered column breaks every link after it and verification returns the first sequence number at which the chain diverges. The chain head is anchored on a stated interval to a record the application itself cannot rewrite, so replacing the whole chain is detectable too. The row and its effect commit together.

### The marketing content tables

`articles`, `authors`, `categories`, `customers`, `results`, `pages`, `bands`, `nav_groups`, `announcements`, `demo_requests`, `subscriptions`, `page_views`. An article carries a `published` state and a `published_at`, and an unpublished row is unreachable at the data layer rather than filtered afterwards. Every media reference carries a required `alt_text` field and a row with an empty one cannot be published. `demo_requests` carries `work_email`, `reason`, `state` and `created_at`. `subscriptions` carries `email`, `source_route` and `created_at`. `page_views` carries the route and the time and no principal, and it is what the usage figures are computed from.

### Derived rather than stored

The release in force for an app and an environment is derived from the newest `releases` row, never stored as a flag on the app. A principal's effective grants are derived at decision time from the surviving grant set, never cached onto the principal row. The row count and the duration on a result are computed for that execution. A group's inherited membership is derived from the nesting, never denormalised. Usage against a quota is derived from the run records for the current window.

### Seed data

One workspace, `Northgate Operations`. Two environments, `staging` then `production`.

Six accounts as listed in `## User roles`, all using the corpus password.

Three groups. `Platform Builders` holds `allow` on `read`, `write` and `publish` at the workspace scope. `Operations` holds `allow` on `read` and `execute` on app `Order Desk` in `production`. `Support Desk` holds `allow` on `read` on app `Order Desk` in `production` and an explicit `deny` on `export` at the workspace scope, so no allow anywhere can give that group an export.

Two resources. `Orders Warehouse`, kind `postgres`, reachable, credentials valid in both environments. `Ledger Archive`, kind `postgres`, whose stored credential no longer works, so a test connection on it answers `unreachable` with a failure class and no credential fragment.

Two apps. `Order Desk`, slug `order-desk`, with one frozen version released to `staging` and to `production`, carrying a table bound to `orders_recent` and a form bound to `order_mark_delayed`. `Refund Desk`, slug `refund-desk`, a draft with no frozen version and no release.

Two queries on `Order Desk`. `orders_recent`, not mutating, declaring the parameters `status` and `limit`. `order_mark_delayed`, mutating, declaring the parameter `order_ref`.

One orders table on `Orders Warehouse` seeded with exactly `50000` rows, each carrying `order_ref`, `customer_name`, `amount_minor`, `status` from `open`, `delayed`, `settled`, and `placed_at`. Three of them are named so they can be matched exactly: `NG-1001` for `Northgate` at `124500` in `delayed`, `NG-1002` for `Bellweather` at `98000` in `open`, and `NG-1003` for `Halcyon` at `1000` in `settled`.

One policy, `Support masking`, attached to group `Support Desk` on resource `Orders Warehouse`, carrying a row predicate restricting results to `status` of `delayed` and masking the column `customer_name`. `Operations` carries no policy, so the two operator accounts see different row sets and different columns from the same query.

Three articles, one per seeded author, one of them unpublished. Six customers, `Northgate`, `Bellweather`, `Halcyon`, `Trestle`, `Vantage` and `Ironwood`, each with at least one result. One announcement whose active window contains the first start.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

Single workspace, `Northgate Operations`. No second tenant and no cross-workspace surface.

Absent features: no workflow scheduler, no scheduled run history, no inbound webhook receiver, no federated identity provider, no second factor, no data residency region, no erasure across derived stores, no break-glass hardware token, no payment, no billing, no subscription, no invoicing, no native mobile application, no comments, no likes, no direct messaging, no real-time collaborative cursors, no AI model call of any kind from any surface.

Absent identity plumbing: no identity federation, no directory provisioning, no claim mapping, and no revocation driven from an external directory. Membership changes are made in the product and take effect in the product.

Absent orchestration: there is no multi-step workflow, so nothing resumes at a failed step and nothing is partially re-run. A mutating query is one step and its idempotency key is what makes a repeat safe.

Absent integrations: only PostgreSQL and Mailpit exist as backing services. Resource kinds beyond `postgres` are declarable, listable and deletable, and never execute. No external network call at runtime, and no analytics destination.

Zero-asset build. No binary asset ships: no typeface file, no photograph, no icon file, no texture, no video, no customer logo file. Everything is generated, drawn inline or rendered procedurally, by the substitution recipes in the front-end specification. No mark reproduces a real trademark.

The reference this product is drawn from shipped roughly forty-two megabytes of binary across six classes, and this build ships none of those bytes: typeface files in woff2, video in mp4, raster imagery in webp, raster icons and marks in png, animated marks in gif, and vector svg. Each class has a recipe instead. Icons and marks are inline geometry. Typefaces are open families matched to the required shape. The hero video and its poster are generated. Article and category illustrations are generated from a seed. Grain is a generated texture. No origin is contacted to fetch an uploaded image or a video, because none is uploaded and none is fetched.

No route reflects an unescaped request value into a page. No credential value reaches any surface.

The product must stay responsive at fifty thousand rows in the seeded orders table, two hundred components on one canvas and thirty queries in one app.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

Field names are exact. A list endpoint returns a top-level JSON array. A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as a client error, never as a server error and never as a silent success. Bearer auth is carried on everything except `POST /api/auth/login`, `GET /api/health`, `POST /api/demo-requests`, `POST /api/subscriptions` and `GET /api/search`.

| Endpoint | Request body or query | Returns |
|---|---|---|
| `POST /api/auth/login` | `email`, `password` | `access_token`, `principal` with `email` and `role` |
| `POST /api/auth/logout` | none | empty on success |
| `GET /api/me` | none | `email`, `role`, `groups` |
| `GET /api/resources` | none | array of `id`, `name`, `kind`, `environments`, `last_test_state`, `last_tested_at` |
| `POST /api/resources` | `name`, `kind`, `host`, `port`, `database`, `username`, `password`, `environment` | the created resource, with no credential field |
| `POST /api/resources/{id}/test` | `environment` | `state` of `reachable` or `unreachable`, and `failure_class` |
| `DELETE /api/resources/{id}` | none | on refusal, `references` naming the apps and queries |
| `GET /api/apps` | optional `search` | array of `id`, `name`, `slug`, `folder`, `released_environments`, `last_edited_at`, `last_edited_by` |
| `POST /api/apps` | `name` | the created app with its `slug` |
| `GET /api/apps/{id}` | none | the app, its draft `base_version_hash` and its releases |
| `POST /api/apps/{id}/operations` | `base_version_hash`, `operations` | on conflict, `current_version_hash` and `conflicting_operations` |
| `POST /api/apps/{id}/versions` | none | `version_hash` |
| `GET /api/apps/{id}/versions` | none | array of `version_hash`, `created_by`, `created_at` |
| `POST /api/approvals` | `app_id`, `version_hash`, `environment`, `reason` | the approval with `decision` of `pending` |
| `POST /api/approvals/{id}/decision` | `decision` of `granted` or `refused` | the decided approval |
| `POST /api/releases` | `app_id`, `version_hash`, `environment`, optional `approval_id` | the release with `promoted_by` and `promoted_at` |
| `GET /api/releases` | `app_id` | array of releases, newest first |
| `POST /api/query-runs` | `app_version`, `query`, `parameters`, `environment`, `idempotency_key` for a mutating query | `state`, and on `ok` also `rows`, `row_count`, `duration_ms`, `columns` with a `name` and a `type` each, and `truncated` |
| `GET /api/groups` | none | array of `id`, `name`, `parent`, `members` with their `source` |
| `POST /api/grants` | `principal_kind`, `principal`, `scope_kind`, `scope`, `action`, `effect`, optional `valid_until` | the created grant |
| `GET /api/decide` | `principal`, `action`, `target`, `environment` | `decision`, `reason`, and `chain` as an ordered list of the rules that fired |
| `POST /api/invitations` | `email`, `group` | the invitation with its `expires_at` and no token |
| `POST /api/invitations/accept` | `token` | the accepted membership |
| `DELETE /api/invitations/{id}` | none | empty on success |
| `DELETE /api/group-members/{group}/{principal}` | none | empty on success |
| `GET /api/audit` | optional `actor`, `action`, `outcome`, `target`, `from`, `to`, `cursor` | array of events and a `next_cursor` |
| `GET /api/audit/verify` | none | `state` of `intact` or `broken`, and `first_divergent_sequence` |
| `POST /api/demo-requests` | `work_email`, `reason` | `state` of `sent`, `invalid`, `spam` or `failed` |
| `POST /api/subscriptions` | `email`, `source_route` | `state` of `sent`, `invalid`, `already` or `failed` |
| `GET /api/search` | `q`, optional `cursor` | `state` of `ok`, `invalid` or `failed`, and on `ok` the grouped `results` |
| `GET /api/health` | none | `200` once ready |

### No mocks

PostgreSQL and Mailpit are the facts. Any of the following is a contract violation however good the interface looks: an in-memory array of apps, releases, grants or audit events that the process rebuilds at start; a resource test that returns `reachable` without opening a connection; an invitation the app records as sent without handing a message to SMTP; a message written to a file or to a log line instead of being sent; a query result the app composes itself instead of executing the statement; and an audit chain recomputed on read so that it is intact by construction. The named provider is the fact: the app's interface and its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A builder signs in, connects a database, binds a table and a form to a query on a canvas, and the app reopens after a reload with every position, size and binding exactly as it was left. A support operator opens the published release at its own address, sees only the rows their group allows with the masked column masked, and is refused at the server when they attempt a change their group denies, leaving the record unchanged. An invited colleague receives one real message, accepts it once, and sees exactly the apps their group grants. An auditor reads the trail, runs its verification, and finds the chain unbroken.
