# Vireo Console

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, sign in as a developer, open a running app and read its live container
health, file a production deploy request against it, and then sign in as a
second member holding the operator role and watch that request be approved and
applied so the new version goes live, without hitting an error page. The
requester may never decide their own request, and a developer may never decide
anybody's: a separate verifier reads the database directly, so a control hidden
in the interface does not count as a refusal.

---

## Overview

Vireo is a serverless compute platform. A workspace runs inference, training,
batch jobs and untrusted code sandboxes on hardware it does not own, and pays
for it by the second. This build is the governed operator console for that
platform, and the public product site that sits over it.

The console has one job, and it is not administration. It answers the question a
member is asking at the moment they open it, which is one of exactly four: is my
thing running, why did it fail, what is it costing me, and who is allowed to
touch it. Every route answers one of those four.

One flow decides whether the build is correct. A developer opens an app, reads
its live container health, and files a request to promote a version to the
production environment. Because the workspace has the two-person rule enabled,
that request must be decided by a second member holding the operator role, who
is not the requester. Approval alone changes nothing: a separate apply step
makes the change, and its failure is a visible state rather than a silently
unapplied approval. A build that renders every chart beautifully and lets a
developer promote their own version to production has not built this product.

---

## User roles

Six roles are stored. Three of them act in the graded flow, and they form a
ladder: `developer`, then `operator`, then `owner`.

| Role | Holds | Cannot |
|---|---|---|
| `owner` | everything, including billing, quotas, workspace settings, the two-person rule, and deciding any request | nothing. At least one must exist |
| `administrator` | members, roles, grants, environments, integrations and quotas, in every environment | change billing, delete the workspace |
| `developer` | deploy, stop and invoke in a development environment, read logs and metrics, manage secrets, images and schedules, and file a request for anything in production | decide any request, act directly in a production environment, change members or roles, read billing detail |
| `operator` | deploy and roll back in production, terminate containers, change scaling settings, decide a deploy request, and read everything | manage members, manage billing, decide a request they filed themselves |
| `billing` | usage, invoices, budgets, quota requests, and nothing else | anything touching code, logs, volume contents or secret metadata |
| `read-only` | read apps, functions, containers, metrics and their own audit entries | any mutation, any log body, any volume browse |

`read-only` deliberately excludes log bodies and volume contents. Auditors and
stakeholders are the usual holders of that role, and log lines routinely carry
customer data the role was never meant to convey.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a `developer`
session against any `operator`-only endpoint must be rejected with `401` or
`403`.

Signup is closed. There is no public registration form. Accounts exist because
they were seeded or invited, and a member is deactivated, never deleted, because
audit entries reference them and a deleted member turns a year of history into
unattributable rows. The last owner of a workspace cannot be demoted or
deactivated, and the interface explains that at the point of the attempt.

Navigation items are hidden, not disabled, where the member's role grants no
permission on them. A disabled item advertises a capability the member cannot
have. The audit route is the exception: it is visible to every member and
readable by every member for their own actions, because a member who cannot see
their own audit trail cannot dispute it.

---

## Core features

Every rule below has a negative case and an exact rejection status.

1. **Sign in and session.** A seeded principal signs in with an email and a
   password and lands on the workspace overview for their default environment.
   A wrong password is rejected with `401` and a message that does not say which
   half was wrong. A request to any console endpoint without a session is
   rejected with `401`.

2. **Workspace and environment in the route.** Every console route carries the
   workspace and the environment in the path, in that order, before the
   resource. A link pasted into a chat resolves to the same resource for the
   person who receives it, or to a clear permission error, and never silently to
   a different workspace's resource of the same name. A request for a resource
   in a workspace the principal is not a live member of is rejected with `404`,
   so that the existence of another workspace's resource is not disclosed. A
   request for a resource in an environment the member may not read is rejected
   with `403`.

3. **The apps list and the app detail.** The apps list shows name, state, current
   version, function count, live container count, error rate over the last hour,
   spend rate and last deploy with who deployed it. State is one of `live`,
   `stopped`, `deploying`, `failed` or `ephemeral-running`. The app detail route
   carries tabs for overview, functions, deployments, logs, containers and
   settings, each a route of its own so it is linkable. An empty list states what
   would be here, why it is not, and the one action that would change it.

4. **Live container health.** The containers surface lists each container with
   its identifier and a copy control, its function and version, its state from
   `starting`, `ready`, `running`, `idle`, `draining`, `terminated` or `failed`,
   its age, its accelerator class and count, its memory and processor with live
   utilisation, and the count of tasks it has served against its configured
   concurrency limit. A terminated container shows an exit reason drawn from a
   closed vocabulary and from nowhere else: `completed`, `idle-scaledown`,
   `deploy-superseded`, `customer-terminated`, `customer-code-error`,
   `out-of-memory`, `timeout`, `preempted`, `worker-lost`, `platform-error`,
   `quota-exceeded`, `policy-denied`. A write that sets any other exit reason is
   rejected with `422`. `out-of-memory` shows the memory limit beside the
   observed peak, and `timeout` shows the configured timeout beside the elapsed
   time. `worker-lost` and `platform-error` are marked as the platform's own and
   are excluded from the customer error rate, because an error rate that
   includes the platform's failures is a number a customer cannot act on.

5. **Filing a production deploy request.** A `developer` opens an app, chooses a
   version, and files a request to promote it to the production environment. The
   request is created in `draft`, moves to `submitted` when it is filed with a
   reason, and to `in-review` when it is routed to its approvers. A request filed
   with an empty reason is rejected with `422` and the field is named. A
   `developer` who calls the promote endpoint directly, without filing a request,
   is rejected with `403` and the app's live version is unchanged.

6. **Deciding a request, and the two-person rule.** A request in `in-review` is
   decided by a member holding `operator` or `owner`, with a reason that is
   required on every decision and is shown to the requester. The state machine is
   closed: `draft` to `submitted` to `in-review`, then to `approved`, `rejected`,
   `withdrawn` or `expired`; `approved` moves to `applied` only after the change
   is actually made, and `failed-to-apply` is a distinct terminal state. These
   rules each have an exact refusal:
   - A `developer` calling the decide endpoint is rejected with `403`, and the
     request row is untouched: its state, its decider and its decision reason are
     exactly what they were before the call.
   - The requester calling the decide endpoint on their own request is rejected
     with `403` even when they hold `operator` or `owner`, and the row is
     untouched. A requester may never approve their own request.
   - A decision on a request that is not in `in-review` is rejected with `409`
     and names the state it is actually in.
   - Two approvers deciding at once produce one transition. The second is
     rejected with `409` and told the request has already moved.
   - A transition to a state the machine does not allow is rejected with `422`.

7. **Approved is not applied.** Approval changes no app. A separate apply step
   promotes the version, and only then does the request reach `applied` and the
   app's live version change. If the apply fails, the request reaches
   `failed-to-apply` and says why, and the previous version stays live.
   Conflating approved and applied produces the worst outcome in this workflow,
   which is a change everybody believes was made and was not.

8. **Rollback.** Rolling a production app back is one action from the deployments
   list, requires a recorded reason, and is itself a deploy: it creates a new
   version pointing at the previous artifact rather than mutating history. A
   rollback with no reason is rejected with `422`. A rollback that erased the
   record of the bad version would destroy the evidence needed to understand the
   incident, so the superseded version and its health remain readable. The deploy
   state machine is shown as a state rather than a spinner: `requested`,
   `building`, `built`, `switching`, `live`, with `failed` from any state and
   `rolled-back` from `live`.

9. **What the stateful objects have in common.** Secrets, images and
   environments are each scoped to a workspace and an environment, each carries
   an owner and a last-modified record visible in the list rather than only on
   the detail route, and each lists the functions that use it, computed from the
   live deployment rather than from a stored note. Deleting any of them checks
   live usage first, names what depends on it, and refuses rather than warns
   where something live depends on it, because the question a member actually
   asks before deleting something is what will break. A resource used by an app
   the member cannot see is shown as used by one app they do not have access to,
   never as unused: hiding a dependency is how somebody deletes a live secret.
   Retention for logs and build output is stated on the surface that carries
   them rather than buried in settings.

10. **Secrets are written, never read back.** A secret is created with a name, a
   description and key and value pairs, and is granted to an app, a function or
   an environment, never to a person. After creation no interface returns a
   value: the console shows key names and value lengths and nothing else, and
   there is no endpoint, of any role, that returns a secret value. Updating a
   secret creates a new version; containers already running keep the value they
   started with and containers started afterwards get the new one, and the
   interface states that at the moment of the update rather than letting it be
   discovered later. Deleting a secret a live deployment references is refused
   with `409` and the referencing functions are named. The most requested feature
   on this surface is showing a value back to the person who typed it, and the
   answer is rotation, and rotation is safe because both versions stay valid
   during an overlap window, so replacing a value is a changeover rather than an
   outage.

11. **Machine tokens.** A token is created with a name and a scope set and is
    bound to one environment. The secret is shown exactly once, with a copy
    control and an explicit acknowledgement before the dialog is dismissed, and
    is never shown again by any route. Token state is one of `live`,
    `superseded`, `expired`, `revoked` or `disabled`. Revoking is permitted to an
    `owner`; a `developer` calling revoke on a token they did not create is
    rejected with `403`. Tokens created by a deactivated principal are listed
    prominently and disabled rather than deleted, so that the question asked
    after every departure, what could this person still do, has an answer on one
    screen. A token is rotated with an overlap window rather than replaced
    outright, and its creator is warned as the expiry approaches.

12. **Logs and the queue.** Log search is bounded by default to the current
    environment and the last hour; an unbounded query is refused with `422` and
    the narrowing that would make it acceptable. Every line carries its task,
    container, function, app, environment and source, and secret values are
    scrubbed from bodies. Lines dropped by the per-container rate limit are
    marked in the stream with the count and the window, because a silent gap is
    the worst possible outcome. Lines are ordered within one container by that
    container's own clock and merged across containers by arrival, and the
    surface states that it is doing so, because pretending to a global order
    across machines is a lie that costs a debugging session. A member holding `read-only` requesting a log
    body is rejected with `403`. The queue surface names, for every waiting task,
    a reason from a closed list: no capacity in region, workspace concurrency
    limit reached, accelerator quota reached, function maximum containers
    reached, cold start in progress, or workspace on hold, and beside each reason
    the specific action that would fix it.

13. **Usage, quotas and spend.** Every metered quantity is an integer in a base
    unit, recorded per task and per container: accelerator time in device
    milliseconds per accelerator class, processor time in core milliseconds,
    memory time in mebibyte seconds, container idle time, storage in byte days,
    network egress bytes, build time, request count and reserved capacity. Idle
    time is shown as its own line beside serving time rather than folded into the
    total, because it is the charge customers are most often surprised by. Every
    figure on the usage route links through to the tasks that produced it. Every
    quota shows consumption against its limit with the request-increase path
    linked. Crossing a quota threshold raises a task on the overview and
    notifies the billing role and every owner. A budget threshold that is
    crossed is stated plainly, and a hard cap refuses new work while allowing
    running work to finish, because cancelling a half-finished training run to
    save the last part of a budget is a worse outcome than the overshoot, and
    the cap is described honestly as accurate within a bounded overshoot rather
    than as an exact cut-off.

14. **Audit.** Every transition above is recorded with its principal, its action,
    its resource, its before and after values and a request identifier, and the
    record is append-only: an attempt to update or delete an audit entry through
    any endpoint is rejected with `403`, and the stored row is unchanged.

15. **Every surface reaches every other, already filtered.** One principle
    governs every observation surface, and these interaction conventions hold on
    every console route without being restated on each. A task links to
    its container, its log lines and its metrics window; a container links to
    its tasks; a log line links to the task that emitted it and the container
    that ran it; every figure on the overview links to the filtered list that
    produced it. A member never copies an identifier out of one screen to paste
    it into a filter on another. Pagination is by cursor rather than by an offset
    page count, filtering is consistent across every list, sort stably, and carry a visible total where it is cheap and an
    approximate marker where it is not. Filters are encoded in the route, so a
    filtered view is a shareable link and the browser back control works. Live
    regions stream; list regions refresh on a stated interval with a visible
    last-updated time and a manual refresh. Multi-select offers a bulk action
    bar that states how many rows it will affect and names the destructive ones.
    A destructive confirmation names the exact resource, and in a production
    environment it requires the name to be typed.

16. **A privacy page.** A privacy page, reachable from the footer of every public
    page, states what the platform records about a workspace, what it does with
    customer payloads and log bodies, and how long each is kept.

17. **A custom not-found page.** An unknown address renders Vireo's own
    not-found page, with the wordmark, an explanation and a way back into the
    console, and answers with `404`.

18. **Forms reject invalid input inline.** Every form validates on blur and on
    submit, names the field that is wrong and the fix, and writes nothing when it
    refuses. A refused form leaves the record exactly as it was.

---

## User flow

Navigation is a breadcrumbed drill-down: the workspace, then the environment,
then the resource, then the tab, each segment a link back to its own level. The
work surface is a split detail pane, so selecting a row opens it beside the list
rather than replacing it. Creating anything opens a modal over the current
route. Feedback is an inline banner at the top of the affected region, never a
notification that disappears before it is read.

**Routes.**

| Route | Who reaches it |
|---|---|
| `/` | anybody. The public product page |
| `/privacy` | anybody |
| `/login` | anybody |
| `/w/:workspace/:environment/overview` | any member |
| `/w/:workspace/:environment/apps` | any member |
| `/w/:workspace/:environment/apps/:app` | any member, with tabs for overview, functions, deployments, logs, containers and settings |
| `/w/:workspace/:environment/containers` | any member |
| `/w/:workspace/:environment/logs` | any member except `read-only`, which is refused the body |
| `/w/:workspace/:environment/requests` | any member |
| `/w/:workspace/:environment/requests/:id` | any member |
| `/w/:workspace/:environment/secrets` | `developer`, `operator`, `administrator`, `owner` |
| `/w/:workspace/:environment/tokens` | `developer`, `operator`, `administrator`, `owner` |
| `/w/:workspace/:environment/usage` | `billing`, `owner` |
| `/w/:workspace/:environment/team` | `administrator`, `owner` |
| `/w/:workspace/:environment/audit` | any member, scoped to their own actions unless they hold `administrator` or `owner` |
| any unknown address | the not-found page |

**The graded journey.** `developer@example.com` signs in, drills workspace to
environment to `Nova Inference`, and reads the app overview: the live version,
the running containers with their states and ages, the error rate for the last
hour and the spend rate. They open the deployments tab, choose the newest built
version, and the promote control opens a modal naming the source environment,
the target environment and the artifact digest. They type a reason and file it.
The modal closes and an inline banner on the app route says the request is in
review and links to it. The app's live version has not changed.

`operator2@example.com` signs in, opens the requests route, and sees the request
in `in-review` with the requester, the reason, the app, both versions and the
time it was filed. The detail pane carries approve and reject, each demanding a
reason. They approve. The request moves to `approved` and the pane shows the
apply step as the remaining work. They apply. The request moves to `applied`,
the app's live version becomes the requested one, the previous version becomes
`superseded`, and the audit route carries both transitions.

**The refusals, in the same journey.** `developer@example.com` opening their own
request sees the decision controls absent, and a direct call to the decide
endpoint is refused with `403` while the request stays exactly as it was.
`developer2@example.com`, a different member of the same role, is refused the
same way. `operator@example.com` filing a request of their own and then trying
to decide it is refused with `403` for the separation rule, not for the role.

**States.** A suspended workspace keeps its reads and its exports working while
every mutating control is disabled behind one explanation, because the boundary
of a suspension is that a member can always retrieve their own data. The shell
renders immediately from the session and each region
skeletons independently; the left rail never skeletons. An empty workspace shows the
first-deploy path rather than nine empty charts. A permission denial names the
missing permission and the role that holds it, never an individual, and offers
the request path. Navigating away from a dirty form warns. A link into a
production resource opened while the development environment is active switches
environment with a confirmation rather than showing not-found. Every error
surface shows its request identifier with a copy control.

---

## UI/UX notes

Dark by default, and there is no light theme. The page ground is a near-black
neutral; cards, the top bar and the detail pane sit on a deep neutral; inset
regions on a deep neutral one step lighter; separators and skeletons on a mid
neutral. Body copy on those grounds is a near-white green rather than white, and
the pale bands of the public page invert to that same near-white green as a
ground with near-black type on it.

One accent, a vivid green, and it is spent only on the primary action, a
highlighted word in a headline, an icon that must be found, and the live
indicator on a running container. De-emphasis is the reference's most
distinctive decision and must be reproduced: secondary and tertiary copy fade
along a green axis toward a muted green, never toward grey. That is what makes
these dark surfaces read as warm rather than as slate.

Status is never colour alone. Every state carries an icon and a word as well as
its hue, and the hues come from four ramps, each running from a deep ground step
to a light top step: a soft red for failure, a soft amber for warning, a vivid
orange for degraded, and a soft blue for information, with a light magenta
reserved for the platform's own faults so that `worker-lost` and
`platform-error` are visibly not the customer's. Charts use a categorical set of
eight that stays distinguishable at small sizes: a light green, a soft orange, a
light magenta, a mid teal, a soft amber, a mid green, a soft blue and a deep
red, with a near-white muted violet and a light soft cyan for the two annotation
layers.

Hover on a dark control is a low white overlay, never a lighter opaque grey: an
opaque hover breaks the moment the control sits on a different surface.

Type is `Inter Variable` for all body copy and for the whole console, set at a
default weight of medium rather than regular, and `Fira Mono` for eyebrow
labels, code, keyboard hints and every number in a table, so that figures align
in a column. Marketing headlines and card titles take the display face.

Motion is two easings and no more. Everything that changes in place, colour,
ground, border and opacity, eases in and out. Everything that arrives, a panel
opening or a banner entering, eases out. There is one signature moment and it is
applied to a property almost nobody animates: the corner radius of a pill
control changes shape as it is pressed, with a slight overshoot and a visible
settle. Four speeds and no others: a dense table control state, an ordinary
control state, a transform, and the radius signature, each longer than the last.
A wait under the perceptual floor shows nothing at all, because a skeleton that
flashes is worse than a still frame. Reduced motion is honoured everywhere, with
two documented exceptions: the loader keeps spinning and the pulsing skeleton
keeps pulsing, because a progress indicator that does not move is a broken
progress indicator.

Density is operator-facing: rows sit tight so a full container list fits one
screen, and figures are monospaced, thousands separated, and always carry their
currency where they are money. Times are absolute in the member's zone with the
zone named, with relative times only as a secondary label, and durations carry
explicit units. Identifiers are shown in full with a copy control, never
truncated without a way to get the whole value.

Accessibility is a contract, not a preference: WCAG AA contrast for body text
against its ground, comfortably sized touch targets, full keyboard operation
with a visible focus ring on every interactive element, labels on icon-only
controls, and meaning never carried by colour alone. Every content image carries
alternative text and decorative images declare themselves decorative. The page
is one landmark structure with a banner, a navigation region, a main region and
a footer, its headings descend in order without skipping a level, and a skip
control jumps past the chrome to the main region. A modal traps focus while it
is open and returns focus to the control that opened it. A region that updates
without a page change announces itself, so that a member using a screen reader
learns that a request moved state or that a banner appeared. A form that is
refused names the fields that failed in a summary at the top of the form as well
as beside each field.

The narrow arrangement is the same tree rearranged, never a second tree built
beside the first, so that every interaction and every piece of content exists at
one width exactly as it does at another. At a narrow viewport the left rail
collapses to icons carrying tooltips, the detail
pane becomes a full-height sheet over the list, tables scroll inside their own
container, and nothing overflows sideways at any width. Every navigation target
stays reachable at any orientation, portrait or landscape, and the layout holds
at a short viewport as well as a narrow one. Nothing is hidden behind a hover alone,
because a hover does not exist on a touch surface.

---

## Technical requirements

The stack is server-rendered with interactive islands. Nuxt 3 renders every
route on the server and hydrates only the regions that stream or update: the
container list, the log tail and the request detail pane. FastAPI serves the
HTTP API on the same origin under the `/api` prefix.

PostgreSQL is the datastore and is reachable at `DATABASE_URL` and at `DB_URL`,
which carry the same value. Keycloak is the identity provider and is reachable
at `AUTH_URL`. Both of these backing services are **already running** and
reachable at those environment variables. Do not download, install, compile or
start a copy of either of them.

Session is by bearer token issued on sign-in. Authorisation is a single decision
point with a single entry point that every handler calls, taking a principal, an
action, a resource reference and a context, and returning allow or deny together
with the rule that decided. The default is deny, and an explicit deny wins over
every allow. The permission vocabulary is the resource types and actions named
in the data model, and `secret.read-value` is not among them and must not exist:
a console that can display a secret has converted every account compromise into
a credential compromise.

The same policy is answered twice: once before the call proceeds, and once again
over the rows themselves, so that a read path that forgets to scope by workspace
returns nothing rather than everything. The row-level answer takes the workspace
from the authenticated principal at the start of the transaction, never from a
parameter the handler chose, and background work, exports and any cache the app
warms run under the same scoped principal rather than a privileged one. A single
check is one forgotten condition away from a cross-tenant leak, and that is the
defining defect of this class of system. That isolation is the security
boundary the whole governance model rests on, and it is answered per row rather
than per query.

Consistency and idempotency are stated obligations, not accidents. Seeding runs
again without duplicating a row, filing the same request twice from a
double-submitted form produces one request, and applying an already-applied
request changes nothing and says so.

The decision has states of its own and each is distinguishable. A request whose
grant has expired is denied on the next decision and the interface refreshes and
explains rather than showing a broken screen; a grant that expires while work is
already running does not stop that work, because the decision is taken at
admission. An entitlement revoked while a request is in flight lets that request
complete and denies the next. A denial for a missing elevation is a distinct
response from a plain denial, so the client can prompt for elevation rather than
showing a dead end. A denial never names an individual: it names the permission
that is missing and the role that holds it.

No credential, API key, admin token or secret value appears in anything the
browser downloads: not in the rendered markup, not in the client bundle, not in
a JSON payload, and not in an inline script. Configuration the client needs is
limited to public origins.

Every public route carries its own title and description and declares a social
preview title and a social preview image, and that preview image resolves.

`GET /api/health` returns `200` once the app is ready.

**The HTTP surface.** Every console endpoint carries the workspace, then the
environment, before the resource, exactly as the browser routes do.

| Method and path | What it does |
|---|---|
| `POST /api/auth/login` | exchanges an email address and a password for a bearer token |
| `GET /api/health` | reports readiness |
| `GET /api/w/{workspace}/{environment}/apps` | lists the apps in that environment |
| `GET /api/w/{workspace}/{environment}/apps/{app}` | reads one app with its versions and live counts |
| `POST /api/w/{workspace}/{environment}/apps/{app}/promote` | promotes a version directly, permitted outside production only |
| `POST /api/w/{workspace}/{environment}/apps/{app}/rollback` | rolls an app back, carrying a reason |
| `GET /api/w/{workspace}/{environment}/containers` | lists containers with state, age, utilisation and exit reason |
| `POST /api/w/{workspace}/{environment}/containers` | records a container lifecycle event |
| `GET /api/w/{workspace}/{environment}/requests` | lists promotion requests |
| `POST /api/w/{workspace}/{environment}/requests` | files a promotion request, carrying a reason |
| `GET /api/w/{workspace}/{environment}/requests/{id}` | reads one promotion request |
| `POST /api/w/{workspace}/{environment}/requests/{id}/decision` | records an approval or a rejection, carrying a reason |
| `POST /api/w/{workspace}/{environment}/requests/{id}/apply` | applies an approved request |
| `GET /api/w/{workspace}/{environment}/secrets` | lists secrets by name, key names and value lengths |
| `POST /api/w/{workspace}/{environment}/secrets` | creates or versions a secret |
| `DELETE /api/w/{workspace}/{environment}/secrets/{id}` | deletes a secret no live deployment references |
| `GET /api/w/{workspace}/{environment}/tokens` | lists machine tokens by name and prefix |
| `POST /api/w/{workspace}/{environment}/tokens` | creates a machine token, returning the secret once |
| `POST /api/w/{workspace}/{environment}/tokens/{id}/revoke` | revokes a machine token |
| `GET /api/w/{workspace}/{environment}/logs` | reads log lines within a bounded range |
| `GET /api/w/{workspace}/{environment}/team` | lists members with their roles |
| `GET /api/w/{workspace}/{environment}/audit` | reads audit entries |
| `PATCH /api/w/{workspace}/{environment}/audit/{id}` | refused, always |
| `DELETE /api/w/{workspace}/{environment}/audit/{id}` | refused, always |
| `GET /api/w/{workspace}/{environment}/usage` | reads metered quantities with their drill-through |

The seeded workspace slug is `vireo-research`, so a production console path reads
`/api/w/vireo-research/production/apps`.

---

## Data model

Rows, their ownership and the invariants that hold over them.

| Entity | Fields |
|---|---|
| `principal` | email, display name, status: `active`, `invited` or `deactivated` |
| `workspace` | name, slug, default environment, two-person rule on or off |
| `membership` | principal, workspace, role, status |
| `environment` | workspace, name, kind: `development`, `staging` or `production` |
| `app` | workspace, environment, name, state, live version |
| `app_version` | app, ordinal, artifact digest, status: `live`, `superseded`, `failed` or `rolled-back`, deployed by, created at |
| `function` | app version, name, accelerator class, timeout, minimum and maximum containers |
| `container` | function, state, exit reason, worker, region, started at, ended at, tasks served |
| `deploy_request` | workspace, source environment, target environment, app, requested version, requester, state, reason, decided by, decided at, decision reason, applied version, created at, updated at, row version |
| `secret` | workspace, environment, name, description, version, created by, last rotated at. The value is write-only and is held where no read path reaches it |
| `secret_grant` | secret, and the app, function or environment it is granted to |
| `machine_token` | workspace, environment, name, public prefix, scopes, created by, state, last used at, expires at |
| `usage_event` | workspace, environment, app, function, container, quantity, unit, rate version, occurred at |
| `quota` | workspace, kind, limit, consumed |
| `audit_entry` | workspace, principal, action, resource, before, after, request identifier, occurred at |
| `log_line` | container, source, level, body, emitted at |

**Ownership.** Every row above carries its workspace, and every row below the
environment level carries its environment. A read answering for one workspace
never returns a row belonging to another, and that holds for background work and
for exports as well as for interactive reads.

**Derived rather than stored.** These are computed on read and never carried in
a column of their own, so they cannot drift from the rows they summarise: an
app's live container count, its error rate for the last hour, its spend rate,
the list of functions a secret is granted to, the environments a member may act
in, and period-to-date spend on the usage route. No counter column stands in for
a count over rows.

**Invariants.**

- A production `app_version` becomes live only through an applied
  `deploy_request`.
- `approved` and `applied` are distinct states, and the second is reached only
  after the change is made.
- `deploy_request.requester` is never equal to `deploy_request.decided_by`.
- Only a membership whose role is `operator` or `owner` may be recorded as
  `decided_by`.
- A `deploy_request` carries a row version that changes on every transition, so
  that two decisions arriving together produce one transition and the second is
  told the row has moved.
- `audit_entry` rows are inserted and never updated or deleted.
- No read path returns a secret value.
- A `principal` is deactivated, never removed, and a workspace always has at
  least one `active` membership whose role is `owner`.
- The exit reason of a terminated `container` is one of the twelve named values.

**Roles.** The stored role set is `owner`, `administrator`, `developer`,
`operator`, `billing` and `read-only`. Six is deliberate: more produces a matrix
nobody maintains, and fewer forces every real need through the administrator
role, which is worse.

**Permission vocabulary.** Resource types and their actions: workspace read,
update, delete and transfer; member read, invite, update-role and deactivate;
role and grant read, create and revoke; environment read, create, update, delete
and promote; app read, deploy, stop, delete and rollback; function read, invoke,
update-settings and shell; container read, terminate and exec; log read and
export; metric read; secret read-metadata, create, update-value, grant and
delete; machine token read, create and revoke; quota read, request-increase and
set; billing read and download-invoice; audit read and export; request read,
create, decide and apply.

**Seed data, and seeding is idempotent.** Restarting must not duplicate rows.

One workspace, `Vireo Research`, slug `vireo-research`, with the two-person rule
on, and two environments, `development` and `production`. Six principals, every
one with the password `deku-demo-pw-2026`:

| Email | Role |
|---|---|
| `owner@example.com` | `owner` |
| `operator@example.com` | `operator` |
| `operator2@example.com` | `operator` |
| `developer@example.com` | `developer` |
| `developer2@example.com` | `developer` |
| `readonly@example.com` | `read-only` |

Those six addresses and the password `deku-demo-pw-2026` are written to
`/app/USER_README.md` so a reader can sign in without opening the seed.

Two apps in each environment, `Nova Inference` and `Atlas Batch`, with functions
`embed`, `rerank` and `nightly-rollup`. `Nova Inference` in production carries
three versions, the second of which is live, and the third built and awaiting
promotion. Containers exist against the live version in a spread of states
including two terminated ones, one with exit reason `out-of-memory` and one with
`worker-lost`. Money is recorded in integer minor units in `usd`, and every time
is UTC.

---

## Front-end specification

This section carries the visual detail in full. It states no rule that the
product's behaviour depends on.

**The token layer.** The palette is authored in two layers: a raw layer naming
the physical ramps by hue and lightness step, and a semantic layer naming them
by job. Components reference the semantic layer only, because a component that
reaches for a raw token has hard-coded a decision the semantic layer exists to
hold, and re-theming then means editing components.

**The neutral ramp** is fifteen steps and it is the ground of the entire
product. The low end is where almost everything sits. Five of those steps sit
below the mid neutral used for separators, because a dense table on a dark
ground needs to separate rows, headers, hover states and selection without any
of them reading as a border.

**The green ramps are three, with three jobs**, and substituting one for another
looks wrong in a way nobody can name. The accent ramp carries every call to
action and nothing else. The pale ramp carries body copy on dark grounds. The
muted green neighbours carry secondary and tertiary copy.

**Surfaces.** The page ground, the raised surface for cards and the top bar, the
muted surface for inset regions, and the secondary surface for separators and
skeletons. Two of the surface tokens are transparent rather than opaque, and
they are the correct way to build a hover and a pressed state on a dark ground:
a low white overlay for hover, a slightly stronger one for pressed. There is a
tinted transparent ground under a positive state and another under an error
state, both derived from the accent and the red rather than from a new hue.

**Shape.** Seven radius steps, from a hairline on a dense control through to a
generous one on a card, plus a fully rounded pill for the chrome controls and
the tags. Five blur steps, used only behind the translucent overlay ground.

**Type scale.** `Inter Variable` for the interface, at a default weight of 500
rather than 400, so that the interface is set in medium and regular is reserved
for long prose. `Fira Mono` at weights 400, 500 and 700, with font display swap,
for eyebrow labels, code, keyboard hints and every figure in a table. The
display face carries marketing headlines and card titles, with a system sans
stack behind it. The sizes are fixed, as size and line-height pairs:

| Step | Size | Line height | Weight | Use |
|---|---|---|---|---|
| display-lg | 56px | 60px | 500 | the marketing hero headline |
| display-sm | 40px | 44px | 500 | a band headline |
| title-lg | 28px | 34px | 500 | a route title |
| title-sm | 20px | 26px | 500 | a card title or a tab title |
| body | 16px | 24px | 400 | long-form prose, the privacy page |
| ui | 14px | 20px | 500 | console body, labels, buttons |
| ui-sm | 13px | 18px | 500 | table rows, dense controls |
| eyebrow | 12px | 16px | 500 | mono eyebrow labels, keyboard hints |
| figure | 13px | 18px | 500 | mono tabular figures in a table |

**Breakpoints.** Four, at the small, medium, large and extra-large steps, with a
single spacing unit that every gap is a multiple of.

**Motion detail.** The in-place easing carries colour, ground, border, outline
and opacity. The arrival easing carries a panel opening and a banner entering.
The signature easing overshoots and is carried on the corner radius alone. The
named transitions the interface uses are a fade in and a fade out, a slide from
each of the four edges and back to them, a scale in and a scale out, a spin for
the loader, a pulse for the skeleton, and a progress sweep for an indeterminate
bar.

**Loading.** Where the shape of the incoming content is known, a skeleton in
that shape on the secondary surface, pulsing. Where it is not, the loader,
centred. Under the perceptual floor, nothing at all. Past ten seconds, a message
naming what is slow and offering a cancel. A region inside a loaded page
skeletons alone, and the chrome and the left rail never skeleton. An action in flight
shows its state on its own control while the rest of the page stays interactive.

**The production marker.** When the active environment is a production one the
top bar carries a persistent, non-dismissible marker, and the same marker
appears on every destructive confirmation. It is a shape and a label as well as
a colour, because the switch between the practice environment and the live one
is the most dangerous control in the product and everything looks identical in
both.

---

## Build plan

1. Schema, idempotent seed and `GET /api/health`. Exit: the endpoint returns
   `200` and every seeded principal signs in.
2. Session and the single decision point. Exit: a `developer` session against an
   `operator`-only endpoint is refused with `403`.
3. The console shell, the breadcrumbed routes, the environment switcher and the
   production marker. Exit: every console route carries workspace and
   environment before the resource.
4. Apps, versions, containers and the closed exit vocabulary. Exit: a terminated
   container shows a reason from the twelve, and a thirteenth is refused with
   `422`.
5. Deploy requests and the state machine. Exit: a filed request reaches
   `in-review`, a decision moves it to `approved`, and a separate apply moves it
   to `applied` and changes the app's live version.
6. Separation of duties and the role gate. Exit: a `developer` deciding is
   refused with `403` and the row is untouched; a requester deciding their own
   request is refused with `403` and the row is untouched.
7. Rollback, secrets, tokens, logs, the queue, usage, quotas and audit. Exit: no
   read path returns a secret value, and an audit entry cannot be edited.
8. The public page, the privacy page, the not-found page, inline form validation
   and the social preview. Exit: an unknown address renders the product's own
   not-found page and answers `404`.

---

## Constraints

Build the console and the public product page over it. The following belong to
the wider platform and are deliberately out of scope here: the documentation
application and its search, the client library and the command line, the worker
fleet and the scheduler's internals, image building and the layer store, volume
file browsing, distributed filesystem semantics, sandboxes as a separate
surface, schedules, dictionaries and queues as first-class routes, traces,
webhooks and third-party integrations, single sign-on and directory
provisioning, the payment provider and hosted checkout, invoices and credit
notes, the status surface, and the marketing site's dimensional layer,
marquee and carousel.

Where the console describes one of those systems, the console surface is still
built: machine tokens, usage and quotas, the queue's wait reasons and the
container exit vocabulary are all part of this build. What is not built is the
system behind them.

Use only the backing services named in this brief. There is no public signup.
There is no light theme. No number in this brief is a suggestion: the closed
vocabularies are closed, and a value outside one is refused rather than stored.

---

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written
  to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the
  app root, empty.
- Serve a production build behind a static or preview server, never a dev
  server.
- The server must keep running after this session ends and must not be a child
  of the shell. An ordinary background job dies with its shell, and the app will
  not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy
  of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

---

## Definition of done

A developer signs in, reads live container health on a production app, and files
a deploy request that a second member holding the operator role approves and
then applies, moving the live version. The hardest guarantee is the refusal: a
developer calling the decision endpoint, and a requester calling it on their own
request, are both rejected with `403`, and the stored request row is exactly
what it was before the call.
