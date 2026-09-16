# Perpetua Cloud

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser, sign in as a developer, file a
change request that would shorten a namespace's retention window, sign in again as a namespace
admin, approve it, apply it, and see the namespace's retention change and both principals named in
the audit trail, without hitting an error page. A different stranger, signed in as a developer,
must NOT be able to approve or apply their own request by any means, and must NOT be able to reach
another organisation's namespace, including by putting its identifier straight into the address or
calling the API directly. Neither of those can be arranged by hiding a button: the grant rows and
the namespace rows must be unchanged afterwards, and a refusal the app draws for itself does not
count.

## Overview

Perpetua Cloud is the operator console for a durable execution platform, plus the small public
product surface that explains and sells it. A durable execution platform records every step an
application takes as an append-only event history, so that when the process running that code
dies, the history is replayed into a fresh process and execution resumes exactly where it stopped,
once, with no lost progress and no duplicated side effect. The code carrying business logic is a
workflow. The code touching the outside world is an activity, and activities are retried on a
policy until they succeed or the policy gives up. Both run inside customer-operated processes
called workers, which poll the platform over an outbound connection; the platform never dials into
a customer network. Work is routed to workers through named task queues. Every tenant boundary is
a namespace, and a namespace holds its own executions, its own retention window, its own endpoint
and its own certificate trust.

Alongside workflows and activities the platform offers signals, which deliver a named message into
a running execution; queries, which read derived state without changing it; and timers, so that a
workflow can sleep for thirty days and wake to send a reminder without holding a process open.

Two kinds of person use the signed-in half. Platform teams manage namespaces, roles, principals
and workers across regions. Engineers browse running workflow executions, read a failed event
history, and file a namespace change request that a namespace admin reviews, approves and applies.
The public half is a dark, technical product site: it explains workflow orchestration, publishes
the security posture, states what the product stores, and lets a visitor ask for an account.

The information architecture is deliberately flat. Organisations do not nest, and that constraint
has a stated consequence: a company wanting two independent billing relationships has two
organisations sharing no identity between them, and the scope switcher is how a person moves
between them. Between the organisation and the namespace sits an optional grouping called a
project, a named collection of namespaces used for grouping and for scoping grants; a project is a
convenience over a tenancy boundary, never a tenancy boundary itself.

The threat model, in one paragraph: the assets worth protecting are customer payload data,
credentials, the audit trail and the configuration that decides access. The adversary this build
is designed against is an authenticated principal of one organisation reaching for another's
data, and a principal exercising a permission they no longer hold.

This is an enterprise product and five properties make it one, each of them a real behaviour in
this build rather than a claim. There are principals rather than users, and a principal may be a
person or a machine. Membership and access resolve through grants rather than a flag on a person
row. Every change is written to an append-only audit trail that a tenant administrator cannot
edit. Namespaces are pinned to regions and a region is immutable once chosen. And a consequential
change is not a tick box on a row: it is a request with a policy, a set of approvals, an expiry
and an application step.

The genuinely hard part is that authorisation must be re-evaluated immediately before a change
request is applied, not only when it was submitted, so that a request filed by somebody who has
since lost the underlying permission fails at application instead of succeeding because it was
authorised earlier.

Deliberately not built: billing, metering, invoices and any money path; schedules and batch
operations; outbound webhooks; the editorial content platform and the fourteen marketing routes
listed in Constraints; comments, likes, messaging and notifications of any kind.

## User roles

Three roles are seeded. A grant binds a principal to a role at a scope, and the scopes widen in
this order: namespace, then project, then organisation.

| Role | Can read | Can write | Cannot |
|---|---|---|---|
| `developer` | executions, event histories, workers, task queues and namespace settings inside a namespace they hold a grant on | file a change request, withdraw their own change request | **cannot approve any change request, including one they filed themselves**; **cannot apply a change request**; **cannot create, edit or delete a namespace**; **cannot grant a role**; **cannot read any namespace they hold no grant on** |
| `namespace-admin` | everything a `developer` can, across every namespace in their organisation | everything a `developer` can, plus approve, reject and apply a change request, create a namespace, and edit namespace settings directly where the kind is not under review | **cannot approve a change request they filed themselves**; **cannot grant a role at organisation scope**; **cannot delete the organisation**; **cannot read another organisation** |
| `owner` | everything in their organisation, including the audit trail and the identity configuration | everything a `namespace-admin` can, plus grant a role at organisation scope, create a custom role, and countersign a change request whose kind requires two approvals | **cannot approve a change request they filed themselves, even holding every role**; **cannot edit or delete an audit entry**; **cannot read another organisation** |

Three further role names are grantable but not seeded as accounts: `admin`, `read-only` and
`auditor`. A grant carries an effect, which is either allow or deny, and an optional expiry.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `developer` session to any `namespace-admin`-only or
`owner`-only endpoint must be rejected by the server (an unauthorized request is denied, not
served), leaving the protected state unchanged.

Signup is closed. No route creates an account, and the public sign-up route collects an enquiry
rather than provisioning anything. Every principal is seeded in the identity provider described in
Technical requirements. The seeded accounts:

| Account | Role and scope | Organisation |
|---|---|---|
| `developer@example.com` | `developer` at namespace scope on `payments-prod` | Northwind Trading |
| `developer2@example.com` | `developer` at namespace scope on `ledger-prod` | Forgelab |
| `namespace-admin@example.com` | `namespace-admin` at organisation scope | Northwind Trading |
| `namespace-admin2@example.com` | `namespace-admin` at organisation scope | Northwind Trading |
| `owner@example.com` | `owner` at organisation scope, and additionally holds every other built-in role by an explicit grant | Northwind Trading |

`developer2@example.com` exists in a second organisation so that isolation is a real boundary
rather than a filter. `namespace-admin2@example.com` exists so that a kind requiring two approvals
can actually reach two. `owner@example.com` holds every role so that separation of duty can be
shown to survive a principal who nominally outranks the rule.

## Core features

### Auth

Sign-in is through the identity provider named in Technical requirements, reachable at `AUTH_URL`.
The seeded principals and their roles already exist there; the app must not try to create a realm,
a client or a user, and must not require any administrative credential of its own.

1. `POST /api/auth/login` takes `{"email", "password"}` and returns `{"access_token"}` plus the
   signed-in principal's effective roles and scopes. The field is named `access_token` exactly.
   Every account uses the password given in Data model.
2. Every request other than login, `GET /api/health`, and the public routes carries the
   `access_token` as a bearer credential. A request with no token, an unparseable token or an
   expired token is denied.
3. A token minted at login stays usable for at least an hour, so that a long session does not go
   stale part-way through a piece of work.
4. Passwords are never stored by this app and never echoed back by any endpoint or any page.
5. Signing out invalidates the session, and a request replaying the old token afterwards is denied.
6. A sign-in failure never falls back to a weaker authentication method, and the failure message
   does not say whether the address exists.

### 1. The public product surface and the failure-and-recovery demonstrator

The public half is six routes and it reads the control plane for nothing at all.

1. `/` explains durable execution and carries an interactive demonstrator. The demonstrator is a
   real state machine, not a recording: it starts a simulated order workflow, runs four activities
   in sequence, deliberately fails the third, retries it on a policy, recovers, and completes. A
   timeline underneath redraws as it goes.
2. On recovery, no activity bar that had already completed is redrawn or restarted. A build that
   clears the timeline and replays it demonstrates the opposite of what the product claims.
3. The demonstrator fetches no media file and no image file. Every visual part of it is drawn by
   the app.
4. A transcript beside the timeline lists each event as it happens. While the reader has scrolled
   the transcript up, it does not jump back down on the next event.
5. `/product` tours the capabilities: workflows, activities, workers, task queues, namespaces,
   signals, queries, timers and event history, one panel each.
6. `/pricing` states the plan names and what each unlocks as a four-column entitlement matrix. It
   publishes no price and runs no calculator in this build.
7. `/security` states the posture in prose: namespace isolation, a named symmetric cipher at rest
   and transport security in flight, customer-controlled payload encryption, per-namespace
   certificate trust the customer supplies, outbound-only worker connectivity, the retention
   control the customer sets, and a published disclosure address with a scope statement and a
   safe-harbour statement. It links to a compliance evidence portal and a data-processing
   agreement as off-origin destinations, and it reproduces no certification claim of any kind,
   because this build is not certified against anything and must not imply it is. It also links
   to an architecture paper and states the self-hosted considerations: the engine is open source
   and self-hostable, and what a self-hosted deployment does not get is exactly this hosted
   product's regional namespaces, federated identity, role-based access, service accounts, audit
   logging and availability guarantee.
8. `/privacy` is a privacy page, reachable from the footer of every page including every console
   page, and it states what Perpetua Cloud stores about a person, which parts of it survive that
   person's deletion, and how long an event history is kept.
9. `/get-cloud` collects an account enquiry: work address, organisation name, expected region. It
   creates no account and grants nothing.
10. Every form in the build, public or signed-in, rejects invalid input inline and names the
    offending field in its own message rather than in a single banner. A submission that is
    invalid writes nothing at all: no partial row, no enquiry record, no audit entry.
11. An unknown address under any route renders the product's own not-found page with a way back to
    the route it was reached from, and answers as not found rather than as success.
12. Every internal link on every public route resolves. No public route links to an address this
    build does not serve.
13. The site serves a favicon and declares it in the document head.
14. `/sitemap.xml` lists every public route this build serves, and `/robots.txt` points at that
    sitemap.
15. No public route reads the control plane, requires a session, or fails when the signed-in half
    is unavailable.

### 2. Change requests, review and approval

This is the feature the rest of the build exists around. A consequential change is a request with
a subject, a policy, a set of approvals, an expiry and an application step.

1. The reviewable kinds are `grant_org_role`, `create_custom_role`, `change_identity_provider`,
   `disable_enforced_sso`, `change_trust_bundle`, `reduce_retention`, `delete_namespace`,
   `initiate_failover`, `batch_terminate_above_threshold` and `change_billing_owner`. Each kind
   carries whether review is required, how many approvals it needs, which roles may approve, and
   an expiry.
2. Filing opens in a modal from the request queue. It takes `POST /api/change-requests` with
   `{"kind", "subject_ref", "proposed", "reason"}` and returns the created request. On success the
   app navigates to a full-page confirmation showing the filed request, its kind, its subject, its
   policy, its expiry and who may approve it.
3. The lifecycle is a state machine and a request moves through exactly these states, spelled
   exactly this way: `draft`, `pending`, `approved`, `applying`, `applied`, `failed`, `rejected`,
   `expired`, `withdrawn`. A request enters `pending` on submission and leaves it on approval,
   rejection, withdrawal or expiry. It enters `applying` when application begins and leaves it for
   `applied` or `failed`. `applied`, `failed`, `rejected`, `expired` and `withdrawn` are terminal,
   and `failed` carries its reason and offers a re-request action.
4. **The requester may never be the sole approver.** This holds even where the policy nominally
   permits self-approval, and even where the requester holds every role. An approval by the
   requesting principal on their own request is denied and the request stays `pending` with no
   approval recorded. The policy chooses who else must agree, never whether anyone must.
5. **Policy is evaluated twice: when the request is submitted, and again immediately before it is
   applied.** A request submitted by a principal who has since lost the underlying permission must
   move to `failed` at application, with a reason naming the lost permission, and the subject must
   be unchanged. The same holds when an approver's permission is revoked between their approval
   and the application.
6. Applying is idempotent on a caller-supplied request identifier. Two applications of the same
   approved request produce one change to the subject, one `applied` request and one audit entry,
   never two.
7. Two concurrent approvals by different eligible principals on a request needing two approvals
   produce one applied change, not two applications. Exactly one application wins.
8. An application that fails partway leaves the subject in a stated state and the request
   `failed` with the reason. It never leaves the request `applied`.
9. A `developer` may file and may withdraw their own request. An approve, reject or apply call
   from a `developer` session is denied and the request row does not change.
10. The request queue at `/o/<org>/requests` has three views: awaiting my approval, my requests,
    and all, with filters for kind, state and requester, and a count beside the queue's entry in
    the rail.
11. The request detail shows the subject as a before and after comparison of the affected fields,
    with any secret value redacted. **The before side is read when the detail is opened, not
    stored at submission**, and where it has changed since submission the screen says so, so that
    nobody approves against a state that no longer exists.
12. Rejecting requires a reason and the reason is stored and shown. Withdrawing is available only
    to the requester.
13. A request whose expiry passes without the required approvals becomes `expired` and is never
    applicable afterwards.

### 3. Namespaces and regions

1. A namespace belongs to exactly one organisation, is pinned to exactly one region, and is
   addressed by its name within that organisation. Namespace names are unique within an
   organisation and the uniqueness is checked again at commit, not trusted from the check that ran
   while the operator was typing.
2. `POST /api/namespaces` takes `{"name", "region", "retention_days", "capacity_mode"}`. The legal
   regions are `eu-central-1`, `us-east-1` and `ap-southeast-2`. `capacity_mode` is `on-demand` or
   `provisioned`.
3. Creation is a durable operation with a visible state, spelled `requested`, `provisioning`,
   `ready` or `failed`. The console shows the state and does not present the namespace as usable
   until it is `ready`. A creation that fails leaves no half-created namespace in the list.
4. **Region is immutable after creation.** The creation form says so while the operator is
   choosing, and an attempt to change it afterwards is denied.
5. Namespace settings carry retention in days, the codec endpoint, the certificate trust bundle,
   the capacity mode with resource units when provisioned, per-namespace rate limits, the endpoint
   address, and the declared search attributes.
6. Reducing retention deletes history, so the settings screen states how many executions will be
   affected before confirming and requires the operator to type the namespace name. Where the
   organisation has review enabled for that kind, the change is filed as a change request instead
   of being applied directly.
7. Replacing a certificate trust bundle accepts both the old and the new entry for an overlap
   window rather than cutting over at once, and the screen shows every entry's expiry and warns
   as one approaches.
8. **A namespace cannot read, list, signal, query, terminate or otherwise interact with another
   namespace, including one in the same organisation.** The check resolves the namespace from the
   credential, never from a name in the request.
9. A request carrying a valid credential for one organisation and naming a resource in another is
   answered exactly as a request for a resource that does not exist, on every operation, so that
   the refusal cannot be used to discover what exists.
10. Where an organisation has pinned a namespace to a region for residency, no operation moves
    that namespace's data out of that region: an export job runs in region, and a metrics
    aggregate may leave the region while a payload never does.
11. A namespace may be replicated: one region is the primary and accepts writes, and each other
    region is a standby receiving replication and serving no writes. The replication lag is the
    observable delay between them and is shown per standby as a metric.
12. Promotion of a standby is a failover, and an operator-initiated failover is filed as a change
    request because it accepts data loss bounded by the lag. The screen shows the current lag
    beside the control and refuses to proceed silently above a stated threshold: it requires an
    acknowledgement naming the lag. This build files and records the failover request; it does not
    carry out the promotion.

### 4. Workflow executions and the event history

1. An execution is one run of one workflow. It carries a workflow identifier chosen by the caller,
   a run identifier generated by the platform, a type, a task queue, a status, a start time, a
   close time once closed, an optional parent, a search attribute set, and an event history.
2. Statuses are spelled exactly: `running`, `completed`, `failed`, `cancelled`, `terminated`,
   `continued-as-new`, `timed-out`.
3. The workflow identifier is the caller's idempotency key. A start with an identifier already
   running is refused or de-duplicated according to the policy the caller states, and ten
   simultaneous starts of the same identifier produce exactly one execution.
4. The execution list is the busiest screen: a queue of executions, newest first, with columns for
   status, workflow identifier, run identifier, type, task queue, start, close and duration.
5. Above it sit quick filters as chips: running, failed in the last hour, closed today,
   long-running. Selecting a chip writes its query into the query bar rather than applying a
   hidden filter.
6. The query bar accepts a structured query over indexed attributes, not free text: equality,
   inequality, ordering, set membership, a between operator for times, and boolean composition. A
   syntax error is shown inline at the character offset that caused it.
7. Paging is by cursor, never by offset. Rows are inserted constantly, and an adversarial
   insertion between two page fetches must produce no duplicated row and no skipped row. A cursor
   from a differently sorted query is rejected rather than reinterpreted.
8. The execution detail shows a header with the status, both identifiers and the permitted
   actions; three collapsible panels for summary, relationships, and input and results; a timeline
   of activities against the execution's own duration; and the event history.
9. An activity that retried appears as segments within one bar, not as several bars, because an
   activity that retried four times is one activity.
10. The event history table fetches by cursor and never loads a whole history to render one page
    of it. The header and the summary panel render without fetching the history at all.
11. Downloading a history is a queued job with a result reference that is single-use and bound to
    the principal who submitted it, never a synchronous stream.
12. A payload renders in one of exactly five states: decoded and pretty-printed with a copy
    control; decoded with a marker naming the codec that decoded it; the encoding named with the
    failure reason and the raw bytes, with the failure attributed to the codec service rather than
    to the platform; the encoding named with a link to the setting where a codec is configured,
    which is not an error; or the size with a download action when it is too large to render.
13. **Decoding an encrypted payload happens in the operator's browser against the customer's own
    codec endpoint.** No server-side call to a codec endpoint exists anywhere in this build.
14. An execution's state is derived from its event history rather than stored beside it. Status,
    duration and result are projections of the history, and the history is append-only: events are
    added, never modified, never reordered, and never removed before retention expires.
15. Resetting an execution creates a new run from a chosen event and does not modify the old run.
    The old run remains, marked as reset, pointing at its successor.
16. The list is served from a search index that is a projection of the history store, and the
    contract between them is stated: every execution eventually appears; the staleness between
    them is bounded and shown as a metric; the history store is authoritative, so a disagreement
    is a defect in the projection rather than a display quirk; an execution is readable directly
    by identifier from the store without the index; and a reconciliation pass compares the two
    over a moving window and repairs the projection. No operation ever writes to the index. An
    execution started seconds ago may not appear yet, the screen says so, and the empty state
    offers a direct lookup by identifier rather than reporting that nothing was found.
17. `cancel` and `terminate` are never adjacent in the action list, carry different confirmation
    shapes, and `terminate` requires the workflow identifier to be typed and states plainly that
    compensating logic will not run. Every action is idempotent on a caller-supplied request
    identifier, so a retried terminate produces one termination and one audit entry.

### 5. Principals, roles, grants and the policy decision

1. Three kinds of principal exist and every authorisation decision resolves one of them: a person,
   who authenticates through the identity provider; a service account, which authenticates with an
   issued key and is created by a person holding the grant rather than self-registered; and a
   certificate subject, implied by a trust bundle rather than enrolled individually.
2. A principal is not a person row. A service account never receives a password reset.
3. **The decision rule.** For a principal, an action and a resource: collect every grant that
   applies to the resource or to any of its ancestors; if any applicable grant has effect deny,
   deny; otherwise if any grant permits the action, permit; otherwise deny. An explicit deny at
   namespace scope defeats an allow at organisation scope.
4. **An expired grant is not collected.** Expiry is judged at decision time against the request
   clock, never by a job that sweeps expired rows, because a sweeper that is late is an access
   control failure. An expired grant stays visible in the console marked expired and stays in the
   audit trail.
5. A principal may not create a custom role granting a permission they do not themselves hold, and
   may not create a service account exceeding their own grants.
6. There is one policy decision path and every console route has a control-plane operation behind
   it. The rail is filtered by the viewer's effective permissions on the server, and that filtering
   has no security value of its own: it is never the check.
7. The members screen lists people with their status, roles, groups, last seen and provisioning
   source, and offers invite, change roles, suspend and remove.
8. An invitation carries an address, a set of roles, an inviter, an expiry and a single-use token.
   Accepting binds the token and creates the grants in one transaction. An invitation to an address
   already in the organisation is refused with a message naming the existing membership rather
   than creating a second one.
9. Removing a person revokes their grants and invalidates their sessions. It does not delete their
   audit entries and it does not delete what they created.
10. **The last owner cannot be removed, suspended or demoted.** The console refuses it with a
    message saying another owner must be appointed first, and the API refuses it independently.
11. A group is a named set of principals that can hold grants, and a group's grants apply to
    whoever is in it at decision time rather than being copied onto members. A group whose source
    is the directory is read-only in the console, because an edit would be destroyed at the next
    synchronisation.
12. Federated sign-on configuration carries the provider metadata, an attribute map from claims to
    person fields, an optional group-claim map, a just-in-time provisioning switch and an
    enforcement switch. Group claims reconcile membership on every assertion, including removals.
13. **Enforcement cannot be enabled without a verified domain**, because an unverified domain claim
    would let an organisation capture accounts at a company it does not own. A stated number of
    break-glass owner credentials remain exempt from enforcement, their use is audited loudly, and
    every owner is notified.

### 6. Workers, task queues and deployment versions

1. A worker is identified by its identity, its build identifier, its SDK and version, and its
   host. Its state is derived from when it last polled rather than stored as a field.
2. The worker fleet screen lists workers for a namespace with their last poll, and marks a worker
   that has stopped polling within a stated window as unreachable rather than deleting it.
3. Workers dial out and poll. **Nothing in this build opens a connection into a customer network**,
   and no feature may be specified that requires one.
4. A task queue carries a name, a kind and a partition count, and the namespace home shows its
   backlog so that work piling up is visible before it is a problem.
5. A deployment version carries a build identifier and a ramp percentage, and ramping is visible
   as a state rather than inferred from which workers are polling.

### 7. The audit trail

Governance rests on this feature: an audit trail a tenant can edit is not evidence, so the write
path is append-only and tamper-evident.

1. Every mutating operation writes exactly one audit entry recording when it happened, the
   principal that performed it, the principal it was performed on behalf of where there was one,
   the source, the request identifier, the action, the resource kind and identifier, the scope
   path, the outcome, and what changed.
2. **The audit trail is append-only in fact.** No endpoint updates or deletes an audit entry, and
   no screen offers it. An `owner` attempting it is denied.
3. Each entry carries the hash of the previous entry for its organisation as well as its own, so
   that an entry altered directly in the store makes a verification action report the first
   divergence at that entry.
4. **Denied attempts are audited**, with the outcome recorded as denied, because the entries an
   intrusion would generate are precisely the refused ones.
5. Deleting a person leaves their entries intact with a stable pseudonymous attribution rather
   than removing them or blanking them.
6. An applied change request writes one entry naming both the requesting principal and every
   approving principal.
7. The audit screen searches by principal, action, resource kind, outcome and time range, and its
   export is a queued job that runs in the namespace's region.

### 8. Console shell, tables and resilience

1. The console addresses its scope: every route below `/o/<org>` resolves inside one organisation
   and every route below `/o/<org>/ns/<ns>` resolves inside one namespace. The scope is in the
   address, not in a session variable, so any screen can be pasted to a colleague and open where
   the sender was.
2. A breadcrumb trail is the primary wayfinding and names every level from the organisation down
   to the current resource, each level a link to that level's own screen.
3. A scope switcher names the current organisation and namespace and opens a two-pane picker,
   organisations beside that organisation's namespaces, both filterable. Switching scope goes to
   the equivalent screen in the new scope where one exists and to the new scope's home where it
   does not. **It never leaves the viewer on the old scope's screen under the new scope's label.**
4. Every list in the console is one table, and it distinguishes never-had-any from
   none-match-your-filter, offering to clear the filter only in the second case.
5. Selecting the page and selecting the whole result set are separate actions, and the second
   names the count it is about to act on.
6. A failed refresh keeps the last good rows on screen with a banner rather than replacing them
   with an error page. A first load renders placeholder rows at the current row count rather than
   a spinner, so the layout does not jump.
7. Every console screen region fails independently: one region that cannot load leaves the others
   usable and says what is missing.
8. Every long operation is a job with an observable state and a single-use result reference bound
   to its submitter.
9. Retries against any dependency back off exponentially with jitter to a stated ceiling and then
   dead-letter rather than retrying for ever, and they hold to a retry budget, so that a hundred
   simultaneous failures do not retry in lockstep.
10. Exceeding a rate limit is answered distinctly from a validation failure and includes how long
    to wait, because a generic failure teaches every client to retry at once and converts a limit
    into an outage.

## User flow

### Routes

| Route | Purpose | Auth |
|---|---|---|
| `/` | Product home and the failure-and-recovery demonstrator | public |
| `/product` | Capability tour | public |
| `/pricing` | Plans and the entitlement matrix | public |
| `/security` | Isolation, encryption, connectivity, disclosure | public |
| `/privacy` | What the product stores | public |
| `/get-cloud` | Account enquiry | public |
| `/sitemap.xml` | Every public route this build serves | public |
| `/robots.txt` | Points at the sitemap | public |
| `/login` | Sign in | public |
| `/o/<org>` | Organisation home: health, namespaces, recent activity, open requests | `developer` and above |
| `/o/<org>/namespaces` | Namespace list | `developer` and above |
| `/o/<org>/namespaces/new` | Namespace creation | `namespace-admin` and above |
| `/o/<org>/ns/<ns>` | Namespace home | grant on that namespace |
| `/o/<org>/ns/<ns>/workflows` | Execution queue and query bar | grant on that namespace |
| `/o/<org>/ns/<ns>/workflows/<wid>/<rid>` | Execution detail and event history | grant on that namespace |
| `/o/<org>/ns/<ns>/workers` | Worker fleet and task-queue backlog | grant on that namespace |
| `/o/<org>/ns/<ns>/settings` | Retention, codec, certificates, limits, search attributes | `namespace-admin` and above |
| `/o/<org>/members` | People, invitations, grants | `namespace-admin` and above |
| `/o/<org>/requests` | Change request queue, review and approval | `developer` and above |
| `/o/<org>/requests/<id>` | Change request detail, before and after, approvals | `developer` and above |
| `/o/<org>/audit` | Audit search and export | `owner` |

### Entry and redirects

An unauthenticated request for any route under `/o/` goes to `/login` with the requested address
kept, and lands on it after signing in rather than on a generic home. Signing in with no remembered
destination lands on `/o/<org>` for the principal's own organisation, or on an organisation chooser
when they belong to more than one. Signing out returns to `/` and invalidates the session. A token
that expires mid-action leaves the work in progress on screen, says the session ended, and returns
the operator to the same place after signing in again rather than discarding what they had typed.
A principal reaching a route their grants do not cover is refused by the server with the same
answer they would get for a resource that does not exist, and the console shows a not-permitted
state rather than an empty table. A request for an organisation or namespace the principal holds no
grant on is answered identically whether or not it exists.

### Journeys

**File, approve and apply a retention reduction.**
1. Sign in as `developer@example.com` with the corpus password.
2. Follow the breadcrumb to Northwind Trading, then `payments-prod`, then its settings.
3. Change retention from `30` days to `7` days and submit. Because `reduce_retention` is under
   review, the app files a change request rather than applying the change.
4. Land on the full-page confirmation naming the kind `reduce_retention`, the subject
   `payments-prod`, the before value `30`, the after value `7`, the expiry, and who may approve.
5. Open `/o/northwind/requests`, see the request under my requests in state `pending`, and confirm
   there is no approve control.
6. Sign out, sign in as `namespace-admin@example.com`.
7. Open `/o/northwind/requests`, see the request under awaiting my approval, open it, read the
   before and after, and approve with a reason.
8. Apply the request. The request reaches `applied`, `payments-prod` now reports a retention of
   `7` days, and `/o/northwind/audit` carries one entry naming both principals.

**A developer cannot approve their own request.**
1. Sign in as `developer@example.com` and file a `reduce_retention` request on `payments-prod`.
2. Call the approve endpoint for that request from this session.
3. The call is denied, the request is still `pending`, no approval is recorded against it, and
   `payments-prod` still reports its original retention.
4. Sign in as `owner@example.com`, who holds every role, and file a request of the same kind.
5. Approve that request from the same session. The approval is denied and the request stays
   `pending`, because the requester is never the sole approver however many roles they hold.

**Authorisation is re-checked at application.**
1. Sign in as `developer@example.com` and file a `reduce_retention` request on `payments-prod`.
2. Sign in as `namespace-admin@example.com` and approve it, leaving it `approved`.
3. Still as `namespace-admin@example.com`, revoke the filing principal's grant on `payments-prod`
   from `/o/northwind/members`.
4. Apply the request. It moves to `failed` with a reason naming the lost permission, and
   `payments-prod` still reports its original retention.

**Read a failed execution's history.**
1. Sign in as `developer@example.com` and open `/o/northwind/ns/payments-prod/workflows`.
2. Select the chip for failures in the last hour and watch its query appear in the query bar.
3. Open the execution with workflow identifier `subscription-9f21c4d0` and run identifier
   `01J7Y6M2R8`.
4. Read the header and the summary without the history loading, then page the event history by
   cursor and expand the failing event.
5. Open the input panel and see the payload rendered in whichever of the five states applies.

**Isolation holds on a direct call.**
1. Sign in as `developer2@example.com`, whose only grant is on `ledger-prod` in Forgelab.
2. Request `/o/northwind/ns/payments-prod/workflows` and then call the same resource on the API
   directly with this session's token.
3. Both are answered exactly as a resource that does not exist, and no row in Northwind Trading
   changes.

### States

Every list has an empty state that says whether nothing has ever existed or the filter is too
narrow. Every page has a loading state that reserves the space its content will occupy. A failed
fetch keeps the last good data with a banner. A form that fails validation keeps what was typed,
names each offending field beside it, and writes nothing. A request that is denied renders a
not-permitted state rather than a blank screen or a crash. An error anywhere leaves the app usable
and navigable rather than replacing it with a stack trace.

## UI/UX notes

The north star is comprehension under pressure: an operator reading an event history at three in
the morning should understand what happened before they understand the interface. The register is
operational. This is a console and a technical product site, so it reads quiet and
information-dense, built for scanning and for repeated action, and it carries no oversized hero
composition and no marketing atmosphere where the working interface belongs. Density over
decoration; stillness over expression.

The ground is a near-black neutral and the ink on it is a near-white neutral, which is what makes
colour feel rationed and therefore meaningful. A true near-black neutral sits behind the header and
the code panels, one step darker than the page itself. Light panels invert this: a near-white
neutral ground carrying near-black neutral ink, used for the testimonial cards and the enquiry
column and nowhere else. Supporting copy on dark grounds is a light, muted blue; the mid, muted
blue reserved for light panels is the single most likely contrast failure in this build and must
not appear on the dark ground. Raised rows inside dark tables are a deep cool neutral, and table
header rows a slightly deeper cool neutral again.

Colour carries meaning and each meaning has one owner. The primary action is a light, vivid blue
blended into a light, vivid indigo, and nothing that is not a primary action wears that blend.
Failure is a light, vivid red blended into a light, vivid indigo, and it appears nowhere except
where something has gone wrong. Success is a mid, vivid teal blended into a light, vivid lime, and
a success chip is the only thing wearing it. In-progress is a light, vivid amber, warnings a light,
vivid amber ink, and destructive confirmations a light, vivid red. One light, vivid violet blended
into a light, vivid green closes the front page and appears once. A light, soft orange and a
near-white, soft violet are the two remaining accents and each is used once. Every bright thing on
this site is a blend of two hues rather than a flat fill, and the flat exceptions are named: the
eyebrow labels and the demonstrator's success ink take a light, vivid green flat, and the
announcement bar takes a mid, vivid lime flat. Keeping to a closed set of blends is what stops the
product turning into a rainbow. The exact values are yours, so long as each meaning keeps its one
owner and the contrast floors below hold.

Type is two families and one rule: the display family carries everything a person wrote and the
monospace family carries everything a machine said. Eyebrows, buttons, labels, tabs, chips, status
words, identifiers, code and terminal output are all machine utterances and are all monospace.
There is no third family and no italic anywhere. The display family is `Space Grotesk` and the
monospace family is `JetBrains Mono`. The rendered scale is `128px` for the one closing statement,
`68px` on `74.8px` for section headings, `52px` on `57.2px` for route headings at tablet width,
`48px` on `57.6px` for plan card headings, `44px` on `48.4px` for card headings at mobile width,
`32px` on `38.4px` for card and panel headings, `24px` on `38.4px` for pull quotes, `24px` on
`28.8px` for table group headings, `20px` on `28px` for standfirsts, `18px` on `28.8px` for
long-form body, `16px` on `24px` for the default body, `16px` on `28px` for body inside cards,
`15px` on `22.5px` for console controls, `14px` on `20px` for table cells, and `12px` on `16px`
for eyebrows and chips, with `10px` on `15px` for the densest console labels. Weights in use are
`100`, `300`, `400`, `500` and `700`, and the thinnest is a texture confined to monospace at the
two smallest steps rather than a legibility choice. Figures align wherever amounts or counts stack
in a column. Uppercase is applied by the design rather than stored in the copy, so that the strings
themselves stay in sentence case.

The two typefaces are chosen rather than inherited. The display family is a geometric grotesque
with a light weight and a tall x-height, which is what lets a very large heading stay light
without thinning into the background. The monospace family is chosen for a clearly distinguished
zero and a narrow advance, because identifiers and run codes are read character by character.

Shape is a closed radius set: barely rounded on chips and inline code, a little more on inputs,
more again on cards and panels, softest on modal surfaces, and fully capsule on transport
controls, the scenario picker and status dots. One element departs from the set deliberately, the
timeline bar, whose radius is half its own height so that it reads as a capsule rather than
clipping its label, and that departure must not be tidied back onto the nearest token. Depth
is almost absent by design: a hard offset shadow with no blur on light cards over a coloured band,
a real soft shadow following the navigation panel's own shape, and a backdrop blur behind the
navigation panel and the demonstrator's terminal so that colour behind them stays legible as
colour. There is no fourth depth device, and in particular no soft glow under a card on the dark
ground, which reads as a smudge rather than as lift. Hero areas have no background colour at all:
they have a stack, a generated star field over a receding perspective grid over a dark wash, and
the wash is what stops the field competing with the type.

Motion character is mechanical: state changes land promptly and nothing eases in decoratively. The
public site may animate its ambient layers and its demonstrator, and the console may not: no
drifting field, no marquee and no scroll-driven reveal runs anywhere inside the console, because an
operator during an incident does not want a page that moves. The only motion the console keeps is a
state transition on a control, a determinate progress indicator where a real operation has real
progress, and a placeholder shimmer during a first load. Anything ambient stops when the document
is hidden. A reduced-motion preference is respected everywhere: the ambient layers stop, the
marquee becomes a static wrapped grid, and pointer and focus transitions survive at full strength
rather than being switched off, because removing every transition makes an interface feel broken
rather than calm.

Density is compact in the console and comfortable on the public site: console rows sit tight so
that a full execution queue fits one screen, and the console's spacing runs about half the site's.
The layout archetype is a breadcrumbed drill-down: the breadcrumb trail is the primary wayfinding
on every console screen, with the rail as a secondary index that is filtered on the server and
keeps an accessible name on every item even when it collapses to icons.

Responsive behaviour holds at every width between the named breakpoints rather than only at them,
and there are three named tiers: a desktop tier, a tablet tier and a phone tier. The page grid
collapses to a single column below the mid breakpoint with a generous side inset, the rail
collapses first to icons and then to a drawer, and the nine-column console tables become cards
carrying a per-table choice of three fields rather than a sideways-scrolling table. Nothing
overflows sideways at any viewport on any route, and every navigation target stays reachable at
the narrowest viewport.

The accessibility floors are contract, not taste. Body text meets WCAG AA contrast against its
ground, and the hero headline meets it at the narrowest width where the type sits over the densest
part of the generated grid. Full keyboard navigation reaches every control with a visible focus
ring, including the primary action, whose ring is never removed for looking wrong. Touch targets
are comfortably sized. Icon-only controls carry labels. Meaning is never carried by colour alone,
so every status chip pairs its colour with a word. Tab sets are real tab sets with one tab stop and
arrow-key movement, disclosures carry expanded state on the control that toggles them, and facet
groups are labelled checkbox groups. Every chart has a table view reachable beside it. The
gradient-edge device degrades to a real border under forced colours, and an outlined control never
disappears there. The brand mark announces itself with the product name rather than the word logo.

Structure and semantics carry their share: each screen has one main landmark, headings descend
without skipping a level, every table announces its caption, and a status message reaches a
reader through a polite live region rather than only by changing colour. Every dialog in the
build, including the filing modal and the terminate confirmation, traps focus while it is open,
makes the background inert, closes on escape, and restores focus to the control that opened it.
Focus is managed at every point where content is replaced rather than navigated: opening a
dialog, closing one, paging a table, switching a tab, revealing a disclosure, submitting a form
that fails validation, and arriving at a full-page confirmation.

## Technical requirements

The frontend is `Svelte` compiled with `Vite`, served as a production build and talking to the
backend over JSON. The backend is `FastAPI` on Python, serving the HTTP API on the same origin
under the `/api` prefix. The rendering model is a single-page application against a JSON API: the
browser receives an application shell on first paint and every screen after that is composed in the
browser from JSON the API returns, so the first response carries no rendered route content. The
datastore is `PostgreSQL`, read from `DATABASE_URL`. Identity is `Keycloak`, read from `AUTH_URL`,
which holds the seeded principals and their roles. `GET /api/health` returns `200` once the app is
ready. Logs go to standard output as one structured line per request.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing services
available in this environment are `PostgreSQL` and `Keycloak`, and reaching for anything else is a
contract violation.

`PostgreSQL` and `Keycloak` are already running and reachable at those environment variables. Read
every host and port from the environment and never hardcode one. Both hold their seeded state
before this app starts; the app must not download, install, compile or start a copy of either, and
must not create a realm, a client or a user in `Keycloak`.

Every response carries the standard security headers, including a strict transport policy and a
content-type policy that refuses sniffing. No credential, API key, administrative token or secret
appears in anything the browser downloads, in any JSON response, or in any page source.

The control-plane interface is resource-shaped and versioned in its path, with one envelope
everywhere. An error answer carries a stable machine-readable code, a human message, a request
identifier, and a per-field map when a validation failed. A refusal for lack of permission and a
refusal for a resource that does not exist are the same answer. Pagination is by cursor. A field
selection parameter exists so that the console does not fetch payloads it will not render. Rate
limits apply per principal and per operation class and the answer carries the remaining budget and
the reset time. A long operation returns an operation reference rather than blocking. Within a
version, changes are additive only.

Validation rules are declared once per operation and both the server's checking and the browser's
are derived from that one declaration, so that the browser never accepts what the server refuses.

Performance is a requirement rather than an aspiration, and the principle behind every rule here
is that a screen must stay usable on exactly the executions an operator needs it for, which are
the largest ones. The organisation home and the namespace home render their first screen promptly
on a namespace carrying a large execution history, and the execution detail's header and summary
render without reading the history at all. An execution list request answers within a budget that
holds at two hundred thousand events in one history. Heavy surfaces are mounted only when they
are opened: the global search overlay, the scope picker and the payload viewer are deferred rather
than mounted with the screen, so that the first paint does not pay for a panel nobody opened.

Every mutating operation accepts a caller-supplied request identifier and is idempotent on it for a
stated window, so that a retry from a client or a proxy cannot produce a second change, a second
audit entry or a second approval.

## Data model

Fourteen tables. All timestamps are UTC, and calendar-day logic uses server-side UTC today.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

Tables are named in snake case and so are columns. Every table carries `created_at` and
`updated_at` except the append-only ones, which carry `occurred_at` and no `updated_at`.
Identifiers are opaque, sortable and prefixed by kind, so that an identifier in a support ticket
names its own type. Foreign keys are declared and enforced in the store, and every relationship
states what happens when the far end is deleted rather than accepting a default, because a default
cascade is how audit rows get destroyed.

**`person`** - `id`, `email`, `email_verified_at`, `name`, `status`. `email` is unique and
case-folded.

**`organisation`** - `id`, `name`, `slug`, `state`, `primary_region`, `created_by`. `slug` is
globally unique.

**`verified_domain`** - `id`, `organisation_id`, `domain`, `verification_method`, `verified_at`.
Required before sign-on enforcement can be enabled.

**`principal`** - `id`, `kind`, `organisation_id`, `person_id`, `service_account_id`, `status`. One
row per acting subject; `kind` is `person`, `service_account` or `certificate_subject`, and exactly
one of the two references is set.

**`service_account`** - `id`, `organisation_id`, `name`, `description`, `owner_person_id`,
`review_due_at`.

**`group`** - `id`, `organisation_id`, `name`, `source`, `external_id`. `source` is `local` or
`directory`, and membership is read-only where it is `directory`.

**`group_member`** - `group_id`, `principal_id`, `source`.

**`role`** - `id`, `organisation_id`, `name`, `builtin`, `permissions`. `organisation_id` is null
for the built-in roles.

**`grant`** - `id`, `subject_kind`, `subject_id`, `role_id`, `scope_kind`, `scope_id`, `effect`,
`expires_at`, `granted_by`. `effect` is `allow` or `deny`; `subject_kind` is `principal` or
`group`; `scope_kind` is `namespace`, `project` or `organisation`. This is the only place
authorisation is stored: there is no administrator flag on `person` and no role string on
`group_member`, because either would be a second answer to a question the decision path does not
ask it.

**`namespace`** - `id`, `organisation_id`, `name`, `region`, `state`, `retention_days`,
`capacity_mode`, `resource_units`, `endpoint`, `created_by`. `name` is unique within an
organisation. `region` never changes after the row is created. `state` is `requested`,
`provisioning`, `ready` or `failed`.

**`trust_bundle_entry`** - `id`, `namespace_id`, `subject`, `fingerprint`, `not_before`,
`not_after`, `added_by`. Two entries may be valid at once during a rotation overlap.

**`search_attribute`** - `id`, `namespace_id`, `name`, `type`, `state`. `type` is one of `keyword`,
`text`, `integer`, `double`, `boolean`, `datetime` or `keyword_list`. A value placed in a search
attribute is indexed rather than stored as a payload and is therefore readable by the platform,
which the declaration screen says plainly.

**`task_queue`** - `id`, `namespace_id`, `name`, `kind`, `partitions`.

**`worker`** - `id`, `namespace_id`, `identity`, `build_id`, `sdk`, `sdk_version`, `host`,
`first_seen_at`, `last_poll_at`. Reachability is derived from `last_poll_at` on read rather than
stored.

**`execution`** - `namespace_id`, `workflow_id`, `run_id`, `type`, `task_queue`, `status`,
`started_at`, `closed_at`, `parent_run_id`, `search_attributes`. `status`, `closed_at` and duration
are projections of the event history, not independently written fields. The primary key is
`namespace_id` with `workflow_id` and `run_id`.

**`execution_event`** - `namespace_id`, `workflow_id`, `run_id`, `event_id`, `occurred_at`,
`event_type`, `attributes`. Append-only. `event_id` increases monotonically within one execution
and has no gaps. No row here is ever updated, reordered or deleted before retention expires.

**`change_request`** - `id`, `organisation_id`, `kind`, `subject_ref`, `proposed`, `state`,
`requested_by`, `expires_at`, `applied_at`, `failure_reason`. `state` is one of `draft`, `pending`,
`approved`, `applying`, `applied`, `failed`, `rejected`, `expired` or `withdrawn`.

**`change_approval`** - `change_request_id`, `principal_id`, `decision`, `reason`, `decided_at`. A
row whose `principal_id` equals the request's `requested_by` is never the row that satisfies the
policy, and a request with no approval from a principal other than its requester is never
applicable. At most one approval row exists per principal per request.

**`audit_entry`** - `id`, `organisation_id`, `occurred_at`, `principal_id`, `on_behalf_of_id`,
`source`, `request_id`, `action`, `resource_kind`, `resource_id`, `scope_path`, `outcome`,
`changes`, `prev_hash`, `hash`. Append-only: the application never updates or deletes a row here,
and `prev_hash` chains each entry to the previous entry for its organisation so that an alteration
is detectable at the entry where it happened. Deleting a `person` leaves these rows in place with a
stable pseudonymous attribution.

**`job`** - `id`, `organisation_id`, `kind`, `submitted_by`, `state`, `progress`, `result_ref`,
`expires_at`. `result_ref` is single-use and bound to `submitted_by`.

The invariants, each stated as a property of the running system rather than as a construction:

- A change request is never `applied` unless at least one recorded approval belongs to a principal
  other than its requester. Two simultaneous approvals on a request needing two produce exactly
  one application; the other is rejected and no second change to the subject occurs.
- Two simultaneous applications of the same approved request produce exactly one change to the
  subject, one `applied` request and one audit entry. The second is rejected.
- A namespace name is unique within its organisation at all times. Two simultaneous creations of
  the same name in the same organisation produce exactly one namespace; the other is rejected and
  leaves no row behind.
- An execution's `event_id` sequence has no duplicate and no gap. Two simultaneous appends to the
  same execution produce two events with distinct consecutive identifiers, never two with the same
  one.
- Ten simultaneous starts of the same `workflow_id` in one namespace produce exactly one
  `execution` row.
- An `audit_entry` row, once written, is never observed with different content afterwards.
- A failed operation leaves no partial state: no orphaned grant, no namespace stuck in
  `provisioning`, no change request in `applying`.

### Seed data

Two organisations. Northwind Trading with slug `northwind`, primary region `eu-central-1`. Forgelab
with slug `forgelab`, primary region `us-east-1`.

Three namespaces. `payments-prod` in Northwind Trading, region `eu-central-1`, `retention_days`
`30`, capacity mode `on-demand`, state `ready`. `orders-prod` in Northwind Trading, region
`us-east-1`, `retention_days` `14`, capacity mode `provisioned`, state `ready`. `ledger-prod` in
Forgelab, region `us-east-1`, `retention_days` `30`, capacity mode `on-demand`, state `ready`.

Five principals, as listed in User roles, each with the corpus password. `developer@example.com`
holds one `developer` grant at namespace scope on `payments-prod` only.
`developer2@example.com` holds one `developer` grant at namespace scope on `ledger-prod` only, so
that a cross-organisation request from that session is a real boundary crossing.
`namespace-admin@example.com` and `namespace-admin2@example.com` each hold a `namespace-admin`
grant at organisation scope on Northwind Trading. `owner@example.com` holds an `owner` grant at
organisation scope on Northwind Trading plus an explicit allow grant for every other built-in
role, so that a principal holding everything still cannot be the sole approver of their own
request.

One expired grant: `developer@example.com` holds a `developer` grant on `orders-prod` whose
`expires_at` is one day before first start, so that an expired grant is present to be not
collected. One explicit deny grant: `namespace-admin2@example.com` holds a deny at namespace scope
on `orders-prod`, so that a deny defeating a wider allow is present to observe.

Change request policy, seeded per kind: `reduce_retention` requires review and one approval from
`namespace-admin` or `owner`, with an expiry `48` hours after submission. `delete_namespace` and
`grant_org_role` require review and two approvals from `owner`, with the same expiry.
`initiate_failover` requires review and two approvals. The remaining kinds are configured as not
requiring review in this seed, so that the direct path and the reviewed path are both reachable.

One change request already in `pending`: filed by `developer@example.com` against `orders-prod`,
kind `reduce_retention`, proposing `retention_days` `7`, with no approval recorded, so that the
approval queue is not empty on first sign-in. One change request already `applied` against
`orders-prod`, so that the audit trail is not empty and the history of a change is visible.

Three executions in `payments-prod`. Workflow identifier `subscription-9f21c4d0`, run identifier
`01J7Y6M2R8`, type `SubscriptionWorkflow`, task queue `billing-tq`, status `failed`, carrying at
least `40` events including a failed activity with three retry segments, so that the timeline, the
retry rendering and the cursor paging all have something real to show. Workflow identifier
`invoice-7a03b1e2`, run identifier `01J7Y6M3S1`, status `running`, task queue `billing-tq`.
Workflow identifier `payout-4c88d0aa`, run identifier `01J7Y6M4T2`, status `completed`, task queue
`payouts-tq`. One execution in `ledger-prod`, workflow identifier `ledger-close-11f0`, run
identifier `01J7Y6M5U3`, status `running`, so that a cross-organisation read has a real target to
be refused.

Two task queues in `payments-prod`, `billing-tq` and `payouts-tq`, each with a visible backlog.
Two workers in `payments-prod`, one polling recently and one whose last poll is outside the
reachability window so that an unreachable worker is visible. One trust bundle entry on
`payments-prod` expiring within the warning threshold, so that the expiry warning is reachable.
Three declared search attributes on `payments-prod`: `customer_tier` of type `keyword`,
`amount_minor` of type `integer`, and `settled_at` of type `datetime`.

One payload in each of the five render states across the seeded executions, so that all five are
reachable: one plain, one encoded and decodable, one encoded whose decode fails, one encoded with
no codec configured on its namespace, and one too large to render.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual specification in full. It states no rule whose grading depends on
reading it rather than the sections above.

### No binary asset, anywhere

No route fetches an image file, an icon file, a video or an audio file, and no grain overlay or
tinted grid arrives as a file. Every visual element is drawn: the star field, the perspective
grid, the brand mark, every icon, the traffic-light dots on the code panels, the status dots and
the timeline markers. Where a design would ordinarily reach for a binary asset, the substitution
is a generated one, and the guide to generating each is given below rather than left to taste.

The star field is generated. Its points are near-white neutral with roughly one in forty taking a
near-white, muted blue, their brightness is distributed across a range weighted to the dim end
rather than spread evenly, and their placement carries mild clustering from a density field so
that the field reads as a sky rather than as confetti. It tiles seamlessly with no visible seam at
the widest tier and is stable across builds at a fixed seed.

The perspective grid is generated too. Longitudinal lines run evenly spaced at the near edge and
converge on a vanishing point that is horizontally centred; transverse lines are spaced by a
reciprocal progression so they crowd toward the horizon. The lines fade before reaching the
horizon rather than converging into a solid band. A grain and noise texture sits over the
composition at low strength, generated rather than fetched, and the dark wash sits between the
field and the grid.

No synthetic photographic likeness is attached to a named person anywhere in this build. Where
the design calls for a portrait, an abstract generated mark stands in its place.

### The layered background

Hero areas carry a stack rather than a colour, and three compositions appear. Deep space is a star
field over a darkened wash over a perspective grid, used on the home, product and security heroes.
Dusk is a star field over a perspective grid over a dark blended ground, used on the enquiry panel.
Brand grid is a low-alpha grid over a blended ground, used on the section introducing the hosted
platform. The composition changes between routes rather than the colour.

### The gradient-edge device

A secondary button, an outlined card and a framed panel all share one device: the element carries a
transparent edge of a stated width, a flat interior fill of the page ground, and a two-hue blend
visible only in that edge. It must render without a wrapper element and without a second shape
kept in sync with the element's own roundness, and it must not blur at a fractional device pixel
ratio. Rebuilding it as a separate ring shape behind the card is the common wrong turn, because the
two shapes then have to be kept identical forever. The pointer state swaps the interior fill rather
than the edge. Under forced colours it degrades to a real border.

### The scaling rule and the grid

One spacing unit, and every gap, pad and inset is an integer multiple of it, declared once and
derived from rather than hand-tuned per section. Content widths come from a closed set of ten
container sizes and no layout invents an eleventh. The page grid is a named twelve-column grid
above the mid tier, carrying a single-column collapse with a generous side inset below it. The
header reserves the same height at every width and every route, declared once so that anchor
offsets and sticky tops read it rather than repeat it.

### Global chrome

Above the header sits an announcement bar carrying one message, one inline link and three utility
links, on a mid, vivid lime ground. The header exposes five groups: Platform, which opens a panel
carrying Overview, How it works, Hosted platform and Security; Docs, a direct off-origin link;
Pricing, a direct link; Use cases, a panel with three labelled sections for customer stories, by
industry and by audience; and Resources, a panel carrying the library, learning, community, code
exchange, blog and changelog. Three of the five open a panel rather than navigating, and it is the
same panel component in all three. Right of the header sit four controls: a search, a source-forge
link with a live star count fetched at build rather than per visitor, a primary action whose label
changes by route, and a secondary action. The footer carries the status dot, the privacy link, the
terms link and the disclosure address on every page.

### The console shell

A persistent left rail in two tiers, a top bar and a content region. The upper tier is
organisation-scoped and carries home, namespaces, members, audit and requests. The lower tier
appears only when a namespace is selected and carries workflows, workers and settings. The rail
collapses to icons at the mid tier and to a drawer at the narrow tier, and every item keeps an
accessible name in every state. The top bar carries the scope switcher, a global search, an
environment indicator when the console points at anything other than production, and the account
menu. The breadcrumb trail sits above the content region on every screen.

### The shared console table

Sorting is server-side on a single column with the direction in the address. Filtering is
server-side and in the address. Paging is by cursor. A header checkbox selects the page, and
selecting the result set is a separate action naming the count. Bulk actions are unavailable with a
stated reason until a selection exists, and name the selected count in their confirmation. Density
is a two-step toggle remembered per person. Columns are choosable and remembered per person per
table. Export is queued as a job. The empty state distinguishes never-had-any from
none-match-your-filter. An error keeps the last good rows with a banner. Loading renders
placeholder rows at the current row count.

### Iconography

Every icon is drawn on a twenty-four unit square and the set divides into two construction styles
that are never mixed inside one row: filled interface icons drawn as a single closed path with no
stroke, and stroked illustrative icons drawn as open paths inheriting the current colour with no
fill. The inventory is a menu glyph of three bars, a plus, an arrow, a chevron, a terminal prompt, a
book, a calendar, a play triangle, a restart glyph, a search glyph, a diamond activity marker and a
badge, plus six stroked illustrative glyphs pairing with the capability rows: an event-flow glyph, a
branch glyph, a stack glyph, a grid glyph, a cluster glyph and a cloud glyph. Two icons sit on
their own grids, the play triangle and the badge, and that is deliberate. Every icon inherits the
text colour of its container, which is what makes a pointer state work without a second drawing.
The brand mark is a four-pointed star with a concave waist, drawn as a single closed outline
stroked in the text colour and never filled at any size, and its accessible name is the product
name rather than the word logo. The status dot, the code panel's traffic-light dots, the step
meter's dots and the timeline markers are not icons: they are shapes built from the tokens that
take their colour from state.

### The code surface

Code panels sit on the darkest ground with a tab set above them whose active tab carries a blended
underline. Keywords take a light, soft blue. A copy control sits at the top right and confirms in
place rather than by moving the layout. The tab set is a real tab set with one tab stop and
arrow-key movement.

### The demonstrator

Four panes and one event stream: a control pane with a scenario picker and transport controls, a
worker pane, a timeline pane and a terminal transcript. The meter is a labelled progress indicator
that announces each state change once, and the three visual panes are hidden from assistive
technology so that the meter is the accessible surface rather than a duplicate. Under reduced
motion the failure burst does not scale and the timeline bars appear rather than growing. Switching
the scenario mid-run does not restart the run.

### Scroll

Exactly one scroll subscription exists per public route, shared by every effect on it rather than
one listener per effect. The reading rail measures the article body rather than the document. The
hero background changes at two points rather than continuously. Reveal observers stop observing
once they have fired.

### Copy identity

These strings are fixed and appear exactly as written: the announcement bar's utility links are
`About`, `Careers` and `Talk to sales`. The primary action on the public site reads `Get started`
and the secondary reads `Log in`. The Use cases panel's three entries read `AI`,
`Financial services` and `Platform engineering`. The footer's column headings read `Explore` and
`Community`, and its entries include `Join our chat group`, `Find a meetup near you` and
`Contact us`. The customer logo band carries the placeholder marks `Northwind`, `Vanta Bank`,
`Skyward`, `Forgelab`, `Sendwise`, `Cascade Air`, `Braddock`, `Larkspur`, `Kestrel Pay` and
`Orbis`, and no real company name, likeness or trademark appears anywhere in the build. The console's approval actions read `Approve`, `Reject`,
`Withdraw` and `Apply`. The execution actions read `Signal`, `Query`, `Update`, `Reset`, `Cancel`
and `Terminate`. The five payload states are labelled `Decoded`, `Decoded by codec`,
`Decode failed`, `No codec configured` and `Too large to render`. The request queue's three views
read `Awaiting my approval`, `My requests` and `All`. The empty execution list reads
`No executions match this query` when a query is active and `This namespace has no executions yet`
when none has ever existed.

### Degraded behaviour per dependency

When `PostgreSQL` is unreachable the console shows a service-unavailable state per region rather
than a blank screen, and the public routes keep serving. When `Keycloak` is unreachable sign-in
fails with a stated reason and an existing valid session keeps working until it expires. When a
customer codec endpoint is unreachable the payload panel renders the decode-failed state attributed
to the codec service rather than to the platform. When the search index is unreachable the
execution list says so and the direct lookup by identifier still works, because it reads the store
rather than the index.

## Constraints

Single-tenant in the sense that this build serves exactly the two seeded organisations and creates
no new ones; there is no self-service organisation creation and no self-service signup.

Not built, and no route, control or endpoint for any of it: billing, metering, usage buckets,
plans, invoices, credit notes and every other money path; schedules and batch operations; outbound
webhooks, notifications, reminders and escalation; observability dashboards, metrics, service
levels and alert rules; service account key issuance, rotation and revocation screens; region
failover execution beyond filing it as a change request; person erasure propagation; the editorial
content platform and the six content types behind it; and the fourteen public routes this build
does not serve, namely how-it-works, cloud, use cases, the three solutions routes, startup,
partners, resources, code exchange, changelog, blog, events, about, careers and news.

No external network call at runtime. Nothing in this build reaches the public internet while it is
running: no analytics collector, no third-party font, no icon CDN, no map tile, no error reporter,
no customer-relationship endpoint and no mail vendor. The star count and the status figure are
fixed values in this build rather than live fetches.

No native application and no mobile application; the browser is the only client.

No email of any kind is sent. An invitation exists as a record with a single-use token and is
accepted by opening its link within the app; nothing is delivered to an inbox.

No payload is ever parsed, indexed or interpreted by this build beyond rendering it, and no
server-side codec call exists.

The app stays responsive with two organisations, three namespaces, two hundred thousand events in
a single execution history, ten thousand executions in one namespace and five thousand audit
entries in one organisation.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/login` | `{"email", "password"}` | `{"access_token", "principal", "roles", "scopes"}` |
| `POST /api/auth/logout` | none | the session is invalidated |
| `GET /api/health` | none | `200` once ready |
| `GET /api/me` | none | `{"principal", "roles", "scopes", "organisations"}` |
| `GET /api/organisations` | none | a top-level JSON array of the caller's organisations |
| `GET /api/organisations/{slug}/namespaces` | `?region=&state=&cursor=` | `{"items", "next_cursor"}` |
| `POST /api/organisations/{slug}/namespaces` | `{"name", "region", "retention_days", "capacity_mode"}` | the created namespace with its `state` |
| `GET /api/organisations/{slug}/namespaces/{name}` | none | the namespace, or the not-found answer |
| `PATCH /api/organisations/{slug}/namespaces/{name}` | `{"retention_days"}` or `{"capacity_mode"}` or `{"codec_endpoint"}` | the namespace, or a filed change request when the kind is under review |
| `GET /api/organisations/{slug}/namespaces/{name}/executions` | `?query=&cursor=&limit=` | `{"items", "next_cursor"}` |
| `GET /api/organisations/{slug}/namespaces/{name}/executions/{workflow_id}/{run_id}` | none | the execution header and summary, without its history |
| `GET /api/organisations/{slug}/namespaces/{name}/executions/{workflow_id}/{run_id}/history` | `?cursor=&limit=` | `{"items", "next_cursor"}` |
| `POST /api/organisations/{slug}/namespaces/{name}/executions/{workflow_id}/{run_id}/terminate` | `{"request_id", "reason"}` | the execution with status `terminated` |
| `GET /api/organisations/{slug}/namespaces/{name}/workers` | `?cursor=` | `{"items", "next_cursor"}` |
| `GET /api/organisations/{slug}/namespaces/{name}/task-queues` | none | a top-level JSON array of task queues with their backlog |
| `GET /api/organisations/{slug}/members` | `?cursor=` | `{"items", "next_cursor"}` |
| `POST /api/organisations/{slug}/grants` | `{"subject_kind", "subject_id", "role", "scope_kind", "scope_id", "effect", "expires_at"}` | the created grant, or a filed change request at organisation scope |
| `DELETE /api/organisations/{slug}/grants/{id}` | none | the grant is revoked |
| `GET /api/organisations/{slug}/change-requests` | `?view=&kind=&state=&requester=&cursor=` | `{"items", "next_cursor"}` |
| `POST /api/organisations/{slug}/change-requests` | `{"kind", "subject_ref", "proposed", "reason"}` | the created request in state `pending` |
| `GET /api/organisations/{slug}/change-requests/{id}` | none | the request with its policy, approvals, expiry, and a before side read now |
| `POST /api/organisations/{slug}/change-requests/{id}/approve` | `{"reason"}` | the request with the approval recorded |
| `POST /api/organisations/{slug}/change-requests/{id}/reject` | `{"reason"}` | the request in state `rejected` |
| `POST /api/organisations/{slug}/change-requests/{id}/withdraw` | none | the request in state `withdrawn` |
| `POST /api/organisations/{slug}/change-requests/{id}/apply` | `{"request_id"}` | the request in state `applied`, or `failed` with `failure_reason` |
| `GET /api/organisations/{slug}/audit` | `?principal=&action=&resource_kind=&outcome=&from=&to=&cursor=` | `{"items", "next_cursor"}` |
| `POST /api/organisations/{slug}/audit/export` | `{"request_id"}` | a job reference |
| `GET /api/jobs/{id}` | none | `{"state", "progress", "result_ref"}` |
| `POST /api/enquiries` | `{"email", "organisation_name", "region"}` | the recorded enquiry; creates no account |

Field names are exact. A list endpoint that pages returns its rows under `items` with a
`next_cursor`, and a list endpoint that does not page returns a top-level JSON array. A successful
call returns the named resource or shape. An invalid or unauthorized call is rejected as a client
error, never as a server error and never as a silent success, and a refusal for lack of permission
is byte-identical to a refusal for a resource that does not exist. Bearer auth is required on
everything except `POST /api/auth/login`, `GET /api/health` and the public routes.

### No mocks

`PostgreSQL` and `Keycloak` are the facts. A namespace, a grant, a change request, an approval, an
execution event and an audit entry must each exist as a real row in the `PostgreSQL` database at
`DATABASE_URL`, and every seeded principal must exist as a real subject in
`Keycloak` at `AUTH_URL` whose credential the app validates rather than accepts on trust. None of
the following satisfies this brief, however good the interface looks: an in-memory list of change
requests, a hardcoded approval response the app returns to itself, a token the app signs for itself
without reference to `Keycloak`, an audit trail kept in a log file rather than in rows, a seeded
user that exists only in the app's own table, or a retention change that updates a screen without
updating a row. The named provider is the fact - the app's UI and its own tables can only reflect
what lives in the provider, never substitute for it.

## Definition of done

A developer can sign in, read a failed execution's event history, and file a request to shorten a
namespace's retention window. A namespace admin can review that request against the namespace's
current settings, approve it, and apply it, after which the namespace reports the new retention and
the audit trail names both people. A developer who files a request cannot approve or apply it, and
neither can a request's own author however many roles they hold. A request whose author has lost
the underlying permission since filing it fails when applied, and the namespace is unchanged.
