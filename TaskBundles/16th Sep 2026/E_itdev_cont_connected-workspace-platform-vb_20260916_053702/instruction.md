# Meridian Workspace

Build and deploy a working web application from this brief. There is no starting codebase. When you
are done, a stranger must be able to open the app in a browser and read a published page at its
public address without signing in and without hitting an error page. A different stranger, signed in
as a member of this workspace, must NOT be able to open a page inside a private teamspace, or a page
carrying an explicit deny for them, by any means: not through the interface, not through a direct
HTTP request for its address, not through a search result, and not by fetching its attachment. The
attachment bytes must live as a real object in the `minio` bucket at the key scheme this brief pins;
a copy on the app container's own filesystem does not count, and neither does a row in the database
holding the bytes.

## Overview

Meridian Workspace is where an organisation keeps the things it writes and the work it tracks in the
same place, under one permission model. A member opens a shared database view, edits a page block by
block, and publishes the result to everyone entitled to see it.

There are only three artefacts. A **page** is an ordered tree of blocks, each block a typed row. A
**database** is a page whose children are pages sharing a property schema, presented through named
views. A **teamspace** is the container a page belongs to, and it carries the default access every
page under it inherits. Everything else in the product is one of those three seen through a
different lens: a wiki is pages, a tracker is a database with a status property and a board view, a
published site is a page tree rendered to anonymous readers. Building the three well is the whole
job; building them as separate features is the failure mode.

The containment hierarchy is fixed and shallow, and the whole information architecture follows from
it: one workspace holds teamspaces, a teamspace holds a tree of pages, and a page holds a tree of
blocks. A page belongs to exactly one teamspace and is never in two, which is what stops the
structure turning into a maze. Membership is a relation carrying its own attributes, a role and the
time it was granted, rather than a boolean column on the principal.

Four people use it. An administrator manages members, groups and teamspace access, and reads the
activity record. Two members write pages, file them in a teamspace and run a view. A guest is
granted one teamspace and sees nothing else.

It deliberately is not: no realtime cursors, no presence, no comments, no mentions, no notifications,
no email, no AI assistant, no agents, no billing or seats or plans, no federated sign-in, no
automations or webhooks, no custom domains, no offline store, no formulas, no relations, no rollups,
no calendar or timeline or chart view, no page history browser, no marketing site.

The genuinely hard part is that authorization is a single question asked on the server for every
read and every write, and it must come out right for a page that inherits from a teamspace, a page
that overrides that inheritance, and a page carrying an explicit deny for one principal inside a
teamspace everybody else can read.

## User roles

Signup is closed. Accounts exist only because they are seeded; there is no registration surface and
no invitation flow.

| Role | Can read | Can write |
|---|---|---|
| `admin` | every teamspace and every page in the workspace, including private ones, and the activity record | teamspaces, their access modes, members, groups and grants; every page. **Cannot** modify or delete an activity record row |
| `member` | pages in an open teamspace, and any page or teamspace explicitly granted to them or to a group they belong to | pages they hold `edit` or `full_access` on. **Cannot** read a private teamspace, **cannot** read a page carrying an explicit deny for them, **cannot** open any admin surface, **cannot** change a grant |
| `guest` | only the pages and teamspaces explicitly granted to them, and only the database properties marked visible to a guest | pages they hold `edit` on. **Cannot** list teamspaces they were not granted, **cannot** read a property hidden from guests or filter, sort or group by it, **cannot** open any admin surface |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `member` session to any `admin`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected state
unchanged.

The same rule governs reads. A page a principal may not read is refused on a direct request for its
address, and a teamspace whose access mode is `private` is refused in the way a teamspace that does
not exist is refused, so that a refusal never confirms the teamspace exists.

Seeded accounts, every one of them using the password `deku-demo-pw-2026`:

| Email | Display name | Role |
|---|---|---|
| `admin@example.com` | `Priya Raman` | `admin` |
| `member@example.com` | `Tomas Vidal` | `member` |
| `member2@example.com` | `Nadia Okafor` | `member` |
| `guest@example.com` | `Ellis Byrne` | `guest` |

One group, `Editors`, contains `member@example.com` and nobody else. A group is a grant subject: a
grant made to `Editors` applies to every principal in it.

## Core features

### Auth

Email and password, implemented by the app. No external identity provider.

1. `POST /api/auth/identify` takes an address and returns the sign-in method to use next. Its
   response body and its status are **identical** for an address that exists and one that does not.
   A difference between the two is an account enumeration oracle, and it is the reason this step
   exists separately from the password step.
2. `POST /api/auth/login` takes `email` and `password` and returns a bearer token on success, in a
   field named `access_token`. A wrong password is rejected as a client error with no hint about
   whether the address exists.
3. Every endpoint except `POST /api/auth/identify`, `POST /api/auth/login`, `GET /api/health` and
   the two anonymous published-page endpoints requires `Authorization: Bearer <token>`. A missing or
   unparseable token is denied, not served.
4. Passwords are hashed at rest. The literal `deku-demo-pw-2026` must work at login for all four
   seeded accounts.
5. `POST /api/auth/logout` ends the session. The bearer token it was called with must be refused on
   the next request.
6. Signup is closed. There is no endpoint that creates a principal from an unauthenticated request.
7. Anti-enumeration and anti-abuse are one rule with two halves. The first half is the identify
   response above. The second is rate limiting: after five failed password attempts for one address
   inside a rolling window, further attempts for that address are refused with a message stating
   that too many attempts have been made, and they are accepted again once the window passes. The
   refusal is temporary and never a permanent lockout, because a permanent lock is a denial of
   service against the member rather than a defence of the account. The refusal carries no hint
   about whether the address exists.

### Teamspaces and groups

A teamspace has one of three access modes, and the three differ in exactly two observable ways:
whether a non-member can discover it, and whether a non-member can read its pages.

1. `open`: every member discovers it and reads its pages.
2. `closed`: every member discovers its name and its description, and no principal outside its
   membership reads any page in it.
3. `private`: a principal outside its membership does not discover it at all. It is absent from
   `GET /api/teamspaces`, and a direct request for it or for any page in it is refused exactly as a
   teamspace identifier that was never issued is refused. A build that ships only `open` and
   `closed` has not built this feature.
4. `GET /api/teamspaces` returns a top-level JSON array of exactly the teamspaces the calling
   principal may discover. For `member@example.com` that array contains `Engineering` and
   `People Ops` and does not contain `Board Papers`. For `admin@example.com` it contains all three.
5. Only an `admin` changes a teamspace's access mode. The same call from a `member` session is
   denied and the stored access mode is unchanged.

### Pages and blocks

A page is an ordered tree of blocks. A block is a row, not a fragment of markup, and every block
type is stored with the same shape, so adding a type never adds a table.

1. Block types the product carries: `paragraph`, `heading_1`, `heading_2`, `heading_3`,
   `bulleted_list_item`, `numbered_list_item`, `to_do`, `toggle`, `quote`, `callout`, `code`,
   `divider`, `image`.
2. `POST /api/pages/{pageId}/blocks` inserts a block at a stated position among its siblings.
   `PATCH /api/blocks/{blockId}` edits its text, its checked state or its colour.
   `POST /api/blocks/{blockId}/move` changes its position and its depth in one operation, so a move
   is never a delete followed by an insert. `DELETE /api/blocks/{blockId}` is a soft delete: the
   block stops being returned and `POST /api/blocks/{blockId}/restore` brings it back at its old
   position.
3. Block depth is bounded at 5. A request to indent a block past that bound is refused as invalid by
   the server, not merely disabled in the editor, and nothing is written.
4. Every block carries an integer `version` that starts at 1 and advances by exactly one on each
   accepted write. `PATCH /api/blocks/{blockId}` carries the `version` the writer last saw. Two
   writes to the same block from the same `version` must not both succeed: exactly one is accepted
   and the other is rejected as a conflict, the block ends at the accepted writer's value, and the
   rejected writer is told. This must hold under real concurrency.
5. A block edit is attributed: the page's `last_edited_by` and the block's `last_edited_by` become
   the writing principal, and `last_edited_at` advances.
6. Reordering is persistent. The order a member drops a block into is the order the page returns
   after a reload, for that member and for every other principal who can read the page.

**Editing a page.** The editing affordances are part of the feature, not decoration.

7. Typing a slash at the start of an empty block opens a typed insert menu, filtered as the member
   keeps typing and driven entirely from the keyboard.
8. Markdown shorthand transforms as it is typed: a hash and a space becomes a heading, a dash and a
   space a bulleted list item, a right angle bracket and a space a quote, and square brackets and a
   space a to-do. Each transformation is undone in one step.
9. A drag handle appears to the left of a block when it is pointed at, and dragging shows a drop
   indicator marking both the position and the depth the block will land at.
10. Several blocks can be selected at once, and every block operation works on the selection as it
    works on one block.
11. Undo is a stack of invertible operations rather than a saved snapshot of the page. Undoing one
    principal's last operation must not remove another principal's work from the same page.
12. Pasting plain text containing line breaks produces one block per line, by structure, rather than
    one block containing the whole paste.

**Rich text inside a block.** A block's text is an array of runs, each run a plain string carrying a
list of annotations, rather than a string of wrapped markup.

13. The annotations are `bold`, `italic`, `strikethrough`, `underline`, `code`, a `colour` naming
    one of the ten palette hues as either a foreground or a background, and a `link` carrying an
    internal or external target. Nothing else is an annotation.
14. An annotation is a range over the runs. Editing the text around an annotated range keeps the
    annotation on the words it was applied to rather than losing it or spreading it, which is what
    keeps a highlight attached to the right words after the sentence around it is rewritten.
15. Rich text survives a reload byte for byte: the runs and their annotations come back exactly as
    they were stored.

### The authorization decision

The principle: authorization is a service that is asked a question, not a set of conditions
scattered through the product. One server-side decision, asked the same way from every read path and
every write path, answering whether a principal may take an action on a resource. There is no path
that assumes, adding a resource type changes one place, and the decision is settleable on its own
against a table of cases.

1. The decision is evaluated in this order and the first terminal result wins: the principal is
   deactivated or the grant has expired, deny; an explicit `deny` grant exists on the resource or an
   ancestor for this principal or a group containing it, deny; the principal holds `admin`, allow
   and record it as an administrative access; an explicit `allow` grant exists on the resource or an
   ancestor for this principal or a group containing it, allow at the highest level found; the
   resource is in an `open` teamspace and the principal is a `member`, allow at the teamspace
   default; the page is published and the action is read, allow as anonymous; otherwise deny.
2. An explicit `deny` beats every `allow`, at any level. This is what lets exactly one principal be
   excluded from exactly one page inside a teamspace everybody else reads, without the page being
   moved. `Onboarding Checklist` carries such a grant for `member2@example.com`: that principal is
   refused, and `member@example.com` and `admin@example.com` are not.
3. A page inherits the effective grants of its parent unless it carries its own grant set, which
   replaces inheritance for that page and its subtree. Returning a page to inheritance is an
   available action and the interface states what will change before it happens.
4. `GET /api/pages/{pageId}/access` returns, for each principal or group with access, the level and
   **where the grant came from**: this page, a named ancestor page, the teamspace, or a named group.
   "Why can this person see this?" is the question an administrator asks under pressure, and the
   product answers it rather than being worked around.
5. An administrative read of a page the administrator holds no other grant on is written to the
   activity record as an administrative access, distinct from an ordinary read.
6. No grant may be created, changed or deleted by a `member` or a `guest` session. The call is
   denied and the stored grants are unchanged.
7. Isolation holds on every read path. Every page, block and row records the workspace it belongs
   to, and that tenant predicate is carried on the record rather than recomputed by walking the
   tree, so a scope that was left out is a caught error rather than a silent leak. No response from
   any endpoint, search results, published pages and attachment reads included, ever contains a
   record belonging to another workspace.
8. A decision is never cached across principals, and no cache key that guards permissioned content
   omits the principal it was decided for. Two principals asking for the same page get two
   decisions, however close together they ask.
9. Removing a principal from a group denies their next read. There is no window in which a removed
   member is still allowed, and there is no stale answer left behind by the removal.
10. A grant that has passed its `expires_at` is inert from that moment: the next decision for it
    denies, and the grant row is marked expired and kept rather than deleted, so that who could see
    a page last quarter stays answerable.
11. Delegation is by time-bounded grant and nothing else. An administrator hands a member access by
    creating a grant, optionally with an end date, and that time-bounded grant is the whole
    mechanism: there is no separate impersonation, no "act as", and no role a principal can assume
    temporarily. A grant created with an end date already in the past denies from the moment it is
    written.

### Databases and views

A database is not a table component. It is a property schema, a set of stored queries, and a set of
renderers over the same rows. A row is a page: it opens as a full page with its own blocks and its
own permissions.

1. Property types carried: `title` (exactly one per database, never deleted), `text`, `number`,
   `select`, `status`, `date`, `person`, `checkbox`, `url`, `created_time`, `created_by`, and
   `unique_id`. `unique_id` is an incrementing integer with a per-database prefix, never reused; the
   seeded database issues keys reading `ZEN-1`, `ZEN-2` and so on.
2. A `number` property is stored and returned as an exact decimal string. No floating-point type
   appears in any numeric property path.
3. A view stores, independently of the database and of every other view: its filter, its sort, its
   group property, and its ordered list of visible properties. Two views over one database with
   different filters both hold their own.
4. A filter is a **tree** of conditions joined by `and` and `or` and nested, not a flat list joined
   by one operator. A nested filter round-trips through storage unchanged: saving
   `Status is In progress` or `Status is In review`, and within that `Team is Platform`, and
   reloading the view returns the same tree and the same rows.
5. A `board` view groups by a `status` property. Each column header shows the group name and the
   count of rows in it, the columns follow the option order, and each column ends with an affordance
   reading `New page` rather than a bare plus.
6. Property-level permission: a property a principal may not read is **absent** from the response,
   not present and blank. A blank value still leaks that the property exists, its type, and often
   its cardinality. `Key notes` is hidden from `guest@example.com`: it is absent from that
   principal's row responses, and a request that filters, sorts or groups by it is refused as
   invalid. Otherwise a guest can binary-search a hidden value by filtering on it.
7. Deleting a `select` or `status` option leaves the rows carrying a tombstone rendered as the old
   name rather than blanking them, and renaming an option changes the label while the rows keep the
   option identifier.
8. `GET /api/databases/{dbId}/views/{viewId}/rows` returns a top-level JSON array containing only
   rows the calling principal may read, with the filter, sort and group applied. Filtering and
   sorting happen in the store, not by returning every row and narrowing it afterwards.

### Attachments

1. `POST /api/pages/{pageId}/attachments` accepts a file and stores its bytes in the `minio` bucket
   named by `STORAGE_BUCKET`. The object key follows this scheme exactly:
   `workspaces/{workspace_slug}/pages/{page_id}/{sha256_of_bytes}.{ext}`. A worked example, for a
   PNG uploaded to page `7` in the workspace `meridian`:
   `workspaces/meridian/pages/7/9f2a1c7d4e5b6a8f0c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b.png`.
2. The bytes exist in the bucket and nowhere else. They are never written to the app container's
   filesystem and never stored inside a database column. The response records the filename, the
   content type, the byte size and the digest, and the app's own tables can only reflect what lives
   in the bucket.
3. `GET /api/attachments/{attachmentId}` streams the object back to a principal who may read the
   page it belongs to, and denies every other caller, anonymous callers included.
4. The one exception is a published page: an attachment on a published page is readable
   anonymously, and only for as long as the page stays published. Unpublishing the page makes the
   attachment address deny again.
5. The seeded attachment is `handbook-cover.png` on `Engineering Handbook`. Because that page is
   unpublished, an anonymous request for it is denied.

### Publishing a page to the web

1. `POST /api/pages/{pageId}/publish` requires `full_access` on the page. Its request body states
   whether the subtree is included, and its response states **how many pages became public**,
   because the commonest publishing accident is a member publishing a page whose subtree they had
   not looked at. The interface confirms with that count before the call is made.
2. A published page is reachable at `/site/{slug}` by an anonymous reader. The slug is unique across
   the workspace, editable at publish time, and a second page asking for a slug already in use is
   refused as invalid.
3. The published route is rendered on the server and must be readable with scripting disabled. It
   carries its own title and description, and it lists itself in a sitemap.
4. `DELETE /api/pages/{pageId}/publish` unpublishes. The address then answers gone; it is never a
   redirect into the workspace, and it never renders the page.
5. A link on a published page that points at a page which is not published renders as plain text,
   never as a route into the workspace.
6. `Release Notes` is seeded published at the slug `release-notes`. Every other seeded page is
   unpublished, and an anonymous request for any of them answers not found.

### Admin console and the activity record

1. `GET /api/admin/members` lists every principal with its role and whether it is active.
   `POST /api/admin/members/{id}/deactivate` deactivates one. A deactivated principal's next request
   is denied and its existing bearer token stops working.
2. `GET /api/admin/groups` and the group membership calls manage `Editors`. Adding a principal to a
   group takes effect on that principal's next read; removing one denies the next read, with no
   window in which a removed member is still allowed.
3. `GET /api/admin/activity` returns the activity record, newest first, each row naming the acting
   principal, the action, the resource type, the resource identifier and the time. Publishing,
   unpublishing, a grant change, a page delete, a page restore, a teamspace access-mode change and
   an administrative access are each recorded.
4. The record is append-only. There is no endpoint that updates a row and no endpoint that deletes
   one, and no call by any principal, `admin` included, changes a row once written.
5. Every `/api/admin/*` endpoint is `admin` only. The same call from a `member` or `guest` session is
   denied and nothing is written.
6. The activity record is this workspace's audit trail, and it is the governance surface an
   administrator answers questions from. Its structure is one row per mutation, and a row's `detail`
   names what changed rather than repeating the resource identifier.
7. Publishing a page that is already published at the same slug is idempotent: the call returns the
   same slug and the same published count, and it writes no second activity row.

### Edge cases

These are the critical cases the product is expected to get right, and each has a stated behaviour.

1. A page is deleted while a member has it open: the page becomes read-only in place with a banner
   and a restore action, rather than vanishing under the reader.
2. A `select` option is deleted while rows carry it: the rows keep a tombstone rendered as the old
   name, and a repair action assigns a replacement.
3. A property is deleted while a view filters on it: the filter is marked broken and disabled, the
   view still renders its remaining rows, and the member is offered a repair.
4. A page is moved into a teamspace the mover cannot read: the move is rejected before it happens,
   not after.
5. An ancestor page is deleted: the subtree keeps its own grants, the inherited grants from the
   deleted ancestor are dropped, and the actor is warned that access may narrow before the delete.
6. A guest is granted a page whose parent they cannot see: the grant holds, and the breadcrumb
   renders only the parts they can see.
7. Two grants at different levels disagree: the higher access level wins among allows, and any
   explicit deny beats every allow.
8. A published page is requested after being unpublished: the address answers gone, and a request
   for any attachment on it is denied again.
9. `minio` is unreachable: only attachment upload and attachment read degrade, each answering
   `dependency_unavailable` with a message naming what is unavailable. Pages, blocks, views, search
   and the activity record keep working. That is the whole degradation ladder: a dependency failure
   sheds the feature that needs it and nothing else, and authorization is never a rung on the
   ladder, so it is never shed. Resilience is per dependency; one failure does not take the product
   down.
10. The same publish call arrives twice because a member double-clicked: idempotency is the answer,
    not a second page. The second call returns the same slug and the same published count and writes
    no second activity row.

### Workspace search

1. `GET /api/search?q=` returns a top-level JSON array of pages whose title or block text matches,
   scoped to this one workspace.
2. Results are filtered by the same decision the page endpoints use. A page a principal may not read
   never appears in that principal's results, whatever the query. Searching for `Onboarding` as
   `member2@example.com` returns nothing for that page; the same search as `member@example.com`
   returns it.
3. An empty result set is an empty array and a state in the interface that names what was searched
   for, not an error.
4. The scope is one workspace and nothing wider. There is no cross-workspace search, because the
   decision that filters the results is itself scoped to one workspace.
5. Search reads an index that is kept current as pages and blocks change, rather than scanning every
   block on every query, and the indexing carries the same scope the read path carries. A page that
   leaves a principal's grant leaves that principal's results at the same moment, with no window in
   which the index still answers for it.
6. Ranking is stated rather than incidental: a match on a page title ranks above a match in block
   text, and between two matches of the same kind the more recently edited page ranks higher.

### The product's own surfaces

1. An address the product does not serve renders the product's own not-found page, carrying the
   product name, a short line of its own copy, and a link back to the workspace home, and the
   response is a not-found status. It is never a blank page, a framework default, or a redirect.
2. Every internal link on every route resolves. No link on any page the product serves leads to an
   address the product answers not-found for.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/login` | identifier-first sign in | anonymous |
| `/w` | workspace home: the sidebar and a recently visited list | member |
| `/w/search` | workspace search | member |
| `/w/p/{pageId}` | a page and its block tree in the detail pane | member |
| `/w/db/{dbId}/{viewId}` | a database view in the detail pane | member |
| `/w/admin/members` | members and groups | admin |
| `/w/admin/teamspaces` | teamspaces and their access modes | admin |
| `/w/admin/activity` | the activity record | admin |
| `/site/{slug}` | a published page, server-rendered | anonymous |
| any other address | the product's own not-found page | anonymous |

**Entry and redirects.** An anonymous request for any `/w` route lands on `/login` and, after a
successful sign in, continues to the address that was asked for. A sign in with no pending address
lands on `/w`. Signing out returns to `/login` and the previous token stops working. A request whose
token has expired mid-action returns to `/login` and, once signed in again, resumes at the address
the member was on. A `member` who opens an `/w/admin` route is refused by the server and shown a
message naming the role the route needs; no admin table is ever rendered to a member. An anonymous
request for `/site/{slug}` whose slug is not published answers not found rather than redirecting
into the workspace.

**Journeys.**

1. Sign in at `/login` as `member@example.com` with `deku-demo-pw-2026`. The sidebar lists
   `Engineering` and `People Ops` under `Teamspaces`. Open `Engineering Handbook`. Click at the end
   of the page and type a paragraph: the block appears at once and settles when the save lands. Drag
   the to-do block above the paragraph; a drop indicator shows the target depth. Reload: the order is
   the order it was dropped in.
2. Still as `member@example.com`, open `Engineering Handbook`, choose `Share`, choose to publish. The
   confirmation names how many child pages become public. Confirm, then open `/site/engineering-handbook`
   in a signed-out browser: the page renders. Unpublish it, and the same address answers gone.
3. Sign in as `member2@example.com`. `Engineering` is open, so `Engineering Handbook` and
   `Release Notes` both open. `Onboarding Checklist` is refused, in the sidebar and on a direct
   request for `/w/p/{pageId}`.
4. Sign in as `member@example.com` and look at the sidebar. `Board Papers` is absent. Request its
   teamspace address directly: the refusal is the same one an identifier that was never issued gets.
5. Sign in as `member@example.com` and open `Company Tasks`, the `Current sprint` board. The columns
   are `To-do`, `In progress`, `In review` and `Complete`, each header carrying its count, each
   column ending in `New page`. Switch to the `Company tasks` table view, save a nested filter, and
   reload: the same tree and the same rows come back.
6. Sign in as `guest@example.com` and open the `Company tasks` view. The `Key notes` column is
   absent, not blank. A request that sorts by it is refused.
7. Sign in as `member@example.com`, open `Engineering Handbook`, insert an image block and upload a
   file. The attachment is in the bucket under the key scheme. Signed out, requesting the attachment
   address is denied while the page is unpublished.
8. Sign in as `admin@example.com` and open `/w/admin/activity`. Every publish, unpublish, grant
   change and delete from the journeys above is present, newest first, each naming the principal,
   the action, the resource and the time.

**States.** Every list has an empty state that names what is missing rather than apologising for
being empty: a filtered database view returning nothing names the filter that emptied it and offers
to clear it, and a teamspace with no pages shows a create prompt. Every surface has a loading state:
the sidebar renders skeleton rows at its last known count, and a database view renders its header and
column set before the rows arrive. An error renders as a banner above the content while the content
already loaded stays readable; the app never shows a blank screen and never shows a stack trace.

## UI/UX notes

Somebody opening this should understand at once that it is a place to read and write for a whole
working day, and should notice the content before they notice the product. The register is
operational: quiet, dense but organised, built for scanning and repeated action. A workspace is
looked at for eight hours, and chrome that competes with content fails, so the restraint here is a
requirement rather than a style note. Content over chrome. Space over dividers. The exact values in
every paragraph below are yours, so long as each stated relationship and each stated exclusivity
holds.

**Mode.** The product commits to a light mode and designs it fully. A dark mode is optional; if
one is built it holds every relationship and every exclusivity stated below, and the light mode
stays the one the product opens in.

**Palette by role.** The page is white and every working surface sits on it. Body text is a
near-black neutral, softened very slightly off pure black so it does not glare; strong text is
darker than body, secondary text lighter, muted text lighter again, and disabled or placeholder text
is the lightest text on the page. Five text weights, each strictly lighter than the one above, and
no sixth. The application's own default text is a deep warm neutral rather than a flat grey, which
is what gives the reading surface its paper cast. There is exactly one saturated colour in the
product, a mid, vivid cyan blue: it means "you can act on this" and it appears nowhere that is not
interactive, one step darker when pointed at and one step darker again when pressed. Links wear that
same blue. Hairlines are a near-white neutral at one weight only, with a single stronger hairline
reserved for the increased-contrast preference. Hovering a plain control tints it with the faintest
possible wash of black and nothing more, and there is exactly one hover weight in the product: do
not invent a second. Three further colours carry state and appear nowhere else, one for something
gone wrong, one for something that worked, one for something still in progress; a state that is none
of the three borrows none of them.

**The block palette.** Ten hues carry meaning on tags, callouts, page icons and text highlights,
each a pale background with a darker foreground of the same family: grey is a mid warm neutral on a
near-white neutral; brown a mid, muted orange on a near-white neutral; orange a mid, vivid orange on
a near-white warm neutral; yellow a mid, vivid orange on a near-white warm neutral; green a mid,
muted green on a near-white neutral; blue a mid, soft cyan on a near-white cool neutral; purple a
mid, muted indigo on a near-white neutral; pink a mid, soft magenta on a near-white warm neutral;
red a mid, vivid red on a near-white warm neutral; and default the body text colour on white. Every
one of those ten pairs must meet a contrast ratio of at least 4.5 to 1 at 16px and above. A palette
regenerated by eye fails that on yellow.

**Type.** One interface sans across the whole product at weights 400, 500 and 600, with a serif
reserved for a pull quote and nowhere else, and no monospace outside a code block or an identifier.
The sizes are given exactly because a scale the builder invents loses the design's character: body
is 16px over a 24px line at 400 and is the default for every reading surface including the page
editor; an interface label is 14px over 20px at 500; secondary body is 14px over 20px at 400; a lead
paragraph is 20px over 30px at 400; a caption is 12px over 16px at 500; an eyebrow is 12px over 16px
at 600; a section subheading is 24px at 500; a dialog title is 20px over 28px at 600; a dense list
row is 17px over 25.5px at 500; and the display size is 48px over 72px at 400 on a wide screen and
40px over 60px at 400 on a tablet. The 1.5 line-height ratio holds through the body scale and is
kept at exactly 1.5 at the display sizes too, which is unusual and deliberate. Figures line up in a
column wherever amounts stack.

**Shape, density and elevation.** Corners are gently rounded at one default softness for cards,
inputs and popovers, a smaller one for navigation rows and small icon frames, and a larger one for
dialogs and the widest cards; the only fully rounded shape is the pill used for menu buttons and
badges. Density is comfortable in the reading column and compact in the sidebar and in a table row,
so a full view fits one screen without a row becoming hard to hit. A shadow here is several
barely-there layers stacked rather than one grey blur, which is the difference between something
that looks printed and something that looks cheap; four elevations exist and no more, for a card, a
floating surface, a tooltip and a menu, while a text input carries an inset hairline instead and
gains a ring in the action blue when focused. Seven named stacking layers and no more: below, flow,
sticky, chrome, overlay, dialog, toast.

**Components and their states.** One main action style and one quieter alternative; the main one
carries the strongest contrast in the interface and is the only thing on a screen wearing the action
blue as a fill. Each screen leads with one clear primary action, visually distinct from every
secondary one. Both action styles have resting, pointed-at, pressed, focused and unavailable states,
and unavailable is never signalled by colour alone. Escape closes any open dialog, popover or side
peek and returns focus to the control that opened it; a destructive action confirms first and the
confirmation names what will be affected. The sign-in surface is one centred column on white with no
navigation and no footer beyond a language control and a help control: wordmark, heading, muted
subheading, a labelled address field, a hint, a full-width filled primary, then the legal line. The
workspace frame is three regions of which only the third scrolls independently: a collapsible left
sidebar, a tab strip above the content, and the content pane with a sticky page header. The sidebar
is resizable between a narrow and a wide bound and collapses away entirely with a hover peek, and it
carries, in order, the workspace switcher, a row of icon buttons, then `Teamspaces` and then
`Private`, each section collapsible, each remembering whether it was left collapsed, each ending in
a `More` row that expands in place rather than navigating.

**Motion.** Two mechanisms only: a declared transition on a named property for hover, focus and
pressed states, and a short prepared keyframe sequence for something arriving. The shorthand that
transitions every property at once is used nowhere, because it will animate properties nobody chose,
including layout properties. The character is eased, a considered entrance and exit that reads as a
designed interface rather than as a machine, and everything in the product moves on one family of
curves at one of three speeds chosen by role: the quickest for a state change on a control, a middle
one for a colour change, the longest for a change of size or position, plus a near-instant press
feedback. Nothing uses a different speed to feel special. Five moments are named and each must
exist: a control's background settles into its hover tint as the pointer arrives and leaves faster
than it arrived; the sidebar's width eases open and closed while the content beside it does not
reflow twice; a row saved optimistically appears at once and settles when the save lands, and is
undone with its reason shown if the save fails; a spinner turns for as long as work is happening;
and a block dropped into a new position settles into it rather than jumping. Under a reduced-motion
preference, entrance animations are removed rather than shortened, colour and background transitions
are kept because they carry meaning about state and removing them makes controls feel dead, and the
spinner keeps turning because it says work is happening.

**Accessibility.** WCAG 2.1 level AA across the whole product, and the page editor is held to the
same standard rather than excused as complex. Muted text is permitted only at 18px and above or for
a non-essential label, never at body size. Every interactive control is reachable and operable by
keyboard navigation alone, with a focus ring drawn as a dark ring inside a light ring so it reads on
any ground, never removed and never replaced by a colour change alone; focus order follows reading
order, nothing reachable is invisible, and after an action that removes the focused element focus
moves to a sensible neighbour rather than to the document body. Every block operation is reachable
without a pointer, including insert, move up, move down, indent, outdent, delete and the insert
menu, and every drag has a keyboard equivalent that announces the move and the new position, because
a board whose cards move only by dragging cannot be used at all by a keyboard user. A dialog traps
focus and returns it to its trigger on close; a database view is a real table with header
associations and arrow-key navigation, with a stated way in and a stated way out so the grid is not
a trap. Save state and validation are announced politely and errors assertively. Status and
validation never rely on hue alone: each carries an icon, a label or a shape. An icon-only control
carries an accessible name describing the action rather than the icon; a decorative image is hidden
from assistive technology and a content image carries alternative text, and the editor asks for a
description when an image is added and warns when a heading level is skipped. At 200 per cent text
scale the layout reflows to a single column with nothing clipped and no sideways scroll.

**Responsive.** The layout is mobile-first and additive, raising its floor at each tier rather than
lowering a ceiling, with exactly one max-width query in the whole system. Three named tiers, phone,
tablet and desktop, and the arrangement holds at every viewport width between them. On a phone the
product is a single column: the sidebar becomes a sheet over the content that dismisses on
selection, the tab strip is hidden and one page is open at a time, block handles give way to a
long-press menu, the table view scrolls sideways inside its own frame with the title column pinned,
and the board shows one column at a time with a horizontal pager. On a tablet the sidebar collapses
to a toggle while the content keeps its two-region arrangement. On a desktop all three regions show
at once, and past the widest breakpoint the content column stops growing while the gutters absorb
the remainder. The document itself never scrolls sideways; genuinely wide content scrolls inside its
own container with a visible affordance. Any control on a coarse pointer is at least 44px by 44px,
including every row action, and every hover affordance has a non-hover equivalent because a phone
has no pointer to hover with. A very long unbroken word in a page title breaks anywhere rather than
overflowing, and a dropdown open across a resize closes rather than reflowing into a broken
position.

**Copy.** Sentence case everywhere except proper nouns, no exclamation marks, no first-person plural
in an interface string, verbs in the imperative for actions, and empty and error strings that name
the thing that is missing rather than apologising. These strings appear exactly as written:
`Teamspaces`, `Private`, `More`, `Share`, `New`, `New page`, `To-do`, `In progress`, `In review`,
`Complete`, `Company tasks`, `Current sprint`, `Syncing`.

**What it must not look like.** No page dominated by one hue family with no second signal. No
decoration standing in for content. No marketing composition where the working interface belongs. No
board or table borrowed from a template with no relationship to a workspace.

## Front-end specification

This section carries the visual detail that does not fit the notes above. Nothing graded lives only
here; it expands what is already stated.

**Two surfaces, one brand.** The workspace application is client-rendered over a JSON interface and
does not scroll as a document: only its content pane scrolls. The published page is server-rendered
and scrolls normally. They are different arrangements on purpose, and a member who moves between
them should feel the difference rather than be surprised by it.

**The sign-in surface.** A single narrow centred column, roughly a third of a laptop screen wide, on
white. In order: the wordmark as a small square mark, a heading, a muted subheading, a field label
reading `Email`, the field itself with a placeholder inviting an address, a hint line explaining
that an organisation address collaborates with teammates, the full-width filled primary reading
`Continue`, and the legal line. The field's focus state is a ring in the action blue, inset and
outset, and nothing else changes. There is no password field on this screen: the address is
submitted first and the system decides what to ask for next.

**The sidebar, in order.** The workspace switcher carries a workspace mark, the workspace name and a
disclosure chevron, with a compose control at the far right. Below it a row of small icon buttons for
home and search. Then the section `Teamspaces`, its rows each an icon and a name, ending in a `More`
row. Then the section `Private`, the same shape. Each section header is collapsible and its state
persists for that member. At the bottom sits the page-creation control.

**The tab strip.** Tabs sit above the content pane and scroll horizontally, shrinking to a minimum
width before scrolling begins. Opening a page from the sidebar replaces the active tab. The open set
survives a reload and belongs to the device rather than to the account. Past a soft cap the oldest
inactive tab closes with an undo offered.

**The page surface.** A single reading column with generous side gutters, the page header sticky
within the content pane, and a per-page action row at its top right carrying `Share` and `New`. A
block reveals a drag handle to its left on hover, and a drop indicator during a drag shows both the
position and the depth the block will land at. A page carries an icon and, optionally, a cover image
with an adjustable crop offset. A full-width flag and a small-text flag are per-page.

**The database surfaces.** The table view is a real table: a header row, a pinned title column, rows
at a compact height, and a calculation row beneath the body offering a count. The board view is a
row of columns, each headed by its group name and its count, each ending in `New page`, cards
carrying the title and up to three further properties. A view tab strip sits above both, naming
`Company tasks` and `Current sprint`. Rows are virtualised so only the visible window plus a small
overscan is in the tree, and the view stays usable as the row count grows rather than fetching
everything and narrowing it in the browser.

**The published page.** The same reading column, the same type scale, no sidebar, no tab strip and
no action row. A title, an optional table of contents, the block tree, and nothing that links back
into the workspace. It must render with scripting disabled.

**The not-found page.** The product's own: the wordmark, a short line in the product's voice naming
what was not found, and one link back to the workspace home. It is the only decorative illustration
in the product, drawn as geometry rather than loaded as a file.

**Typography, stated once more as a system.** The product's typography is one interface typeface at
three weights, and the scale in the notes above is the whole scale: a size that is not in it does not
appear. Because no licensed typeface ships with this product, each family is declared with a
fallback stack ending in a generic family, so the product renders correctly on a machine that has
none of the preferred faces installed. Figures are tabular wherever numbers stack in a column, so a
count in a board header and a count in a calculation row line up rather than dance.

**Radii, as a named scale.** Four radii and no fifth: a default softness on cards, inputs and
popovers; a smaller one on navigation rows and small icon frames; a larger one on dialogs and the
widest cards; and a fully rounded pill, which is the only fully rounded shape in the product and
belongs to menu buttons and badges alone. Media that meets a fold is rounded on its top corners only
and square at the bottom.

**Layering, as seven bands.** Stacking is declared in seven named bands and nothing sits outside
them: below for a decorative background, flow for in-page layering, sticky for a sticky table header
and the sticky page header, chrome for the top bar, overlay for a dropdown or a popover, dialog for a
modal, and toast for a transient message. A layering value chosen ad hoc, and in particular an
enormous one chosen to win an argument with another component, is not permitted; an element that
needs to escape its neighbours is given its own stacking context instead.

**Iconography.** Every icon is geometry drawn inline on one grid at one stroke weight, never a font
and never a binary file. Strokes are rounded at their ends and joins, and an icon that carries
meaning on its own also carries an accessible name. The arrow is the one glyph worth naming
separately: one arrow shape is used for every direction, rotated rather than redrawn, so a
disclosure chevron, a sort direction and a link-out marker are visibly the same family. In a
right-to-left reading order the arrow would mirror, and since this product ships one
left-to-right locale it never does.

**The motion inventory, reduced.** Curves are reduced to five roles and no more, and each role is
named by what it is for rather than by its shape: a standard curve for most property changes, a
decelerating one for something arriving, an accelerating one for something leaving and for every
colour change, an emphasised one for the sidebar collapse, and a single overshoot reserved for a
control that snaps into place. Durations are reduced to three plus a press: the quickest for a state
change on a control, a middle one for a colour change, the longest for a change of size or position,
and a near-instant press feedback. That inventory is closed; a sixth curve or a fourth duration
means the system has been abandoned rather than extended.

**Zero-asset substitution.** This product must build with no binary file of any kind, so there is no
reference asset manifest to fetch and every asset class has a procedural substitute. Typefaces are
system and generic families behind a fallback stack rather than downloaded font files. A page cover
and the not-found illustration are drawn as geometry. Where the reference product would carry a
photograph, a logo wall of customer marks, a hero video or a decorative noise or paper texture, this
product carries nothing in its place rather than a placeholder image: the surface stays plain, which
is what the operational register asks for anyway. The wordmark, the page icons and the favicon are
all drawn the same way. An uploaded attachment is the only binary in the product, and it comes from
a member.

## Technical requirements

Frontend: `Lit + Vite`, built to static assets. Backend: `FastAPI` on Python. The rendering model is
a single-page application over a JSON interface: the browser receives an application shell on first
paint and the page content arrives as JSON from the same origin under `/api`. The one exception is
`/site/{slug}`, which the server renders as HTML. Storage: `PostgreSQL` for records, `minio` for
file bytes. Auth: app-implemented email and password with bearer tokens, passwords hashed at rest.
Health: `GET /api/health` returns `200` once the app is ready. Logging: one structured line per
request to standard output carrying the method, the path, the status and the principal identifier
when there is one, and never a password, a bearer token or an object-store credential.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing services
available in this environment are `PostgreSQL` and `minio`, and reaching for anything else is a
contract violation.

The backing services are already running and reachable at these variables, which the app reads from
the environment and never hardcodes: `DATABASE_URL` for `PostgreSQL`; `STORAGE_ENDPOINT`,
`STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY` for `minio`; `APP_PUBLIC_URL` and
`APP_PUBLIC_PORT` for the app itself.

Every response the app serves carries the standard security headers, including a strict transport
policy and a content-type policy that forbids sniffing. Nothing the browser downloads contains a
credential, an API key or an administrative token: not the JavaScript bundle, not a stylesheet, not
an inline script, and not a JSON payload served to an anonymous reader. The app serves a favicon and
declares it in the document head of every route it renders.

The search, the filter, the sort and the group are executed in the store rather than by fetching
every row and narrowing it in the browser, and a list endpoint pages with a cursor rather than an
offset so the page boundary stays stable while rows are being inserted.

Performance is a requirement with a stated budget rather than an aspiration. Asking whether one
principal may read one hundred rows costs one decision over the set, not one hundred separate ones,
and the cost does not grow with the depth of the page tree. A database view stays usable as its row
count grows because only the visible window of rows is materialised for the browser. A workspace
carrying 10000 blocks across 500 pages and 5000 rows in one database answers a page read, a view
read and a search inside the same budget as an empty one.

## Data model

Eleven tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**principals** - `id`, `email` (unique, lowercase), `password_hash`, `display_name`, `kind`
(`member` or `guest`), `workspace_role` (`admin`, `member` or `guest`), `is_active`, `created_at`.

**groups** - `id`, `name` (unique), `created_at`. **group_members** - `group_id`, `principal_id`. A
principal appears at most once per group.

**teamspaces** - `id`, `name`, `slug` (unique), `access_mode` (`open`, `closed` or `private`),
`description`, `created_at`. **teamspace_members** - `teamspace_id`, `principal_id`, `role`
(`teamspace_owner` or `teamspace_member`).

**pages** - `id`, `teamspace_id`, `parent_page_id` (nullable), `title`, `icon`, `position`,
`is_database`, `database_id` (nullable, set when the page is a database row), `published`,
`public_slug` (nullable, unique), `alive`, `created_by`, `last_edited_by`, `created_at`,
`last_edited_at`, `version`. A page belongs to exactly one teamspace and is never in two.

**blocks** - `id`, `page_id`, `parent_block_id` (nullable), `type`, `text`, `checked` (nullable),
`colour` (nullable, one of the ten palette names), `position`, `depth`, `alive`, `created_by`,
`last_edited_by`, `created_at`, `last_edited_at`, `version`. Every block type shares this one shape.
`depth` never exceeds 5, and that bound holds for a request that arrives at the API directly.

**databases** - `id`, `page_id`, `name`, `created_at`. **database_properties** - `id`,
`database_id`, `name`, `type`, `position`, `is_title`, `visible_to_guests`, `options`. Exactly one
property per database carries `is_title`, and it cannot be deleted.

**row_values** - `row_page_id`, `property_id`, `value`. A numeric value is held as an exact decimal
string, never as a floating-point type.

**views** - `id`, `database_id`, `name`, `kind` (`table` or `board`), `filter`, `sort`, `group_by`,
`visible_properties`, `position`. `filter` holds a nested tree of conditions joined by `and` and
`or`, and it survives a save and a reload unchanged. A `board` view always carries `group_by`.

**grants** - `id`, `resource_type` (`page` or `teamspace`), `resource_id`, `subject_type`
(`principal` or `group`), `subject_id`, `level` (`full_access`, `edit`, `comment` or `read`),
`effect` (`allow` or `deny`), `granted_by`, `granted_at`, `expires_at` (nullable). An expired grant
is marked expired and retained, never deleted, so that who could see a page last quarter stays
answerable.

**attachments** - `id`, `page_id`, `filename`, `content_type`, `byte_size`, `sha256`, `object_key`,
`uploaded_by`, `created_at`. The bytes are in the bucket. This table records where they are.

**activity** - `id`, `actor_principal_id`, `action`, `resource_type`, `resource_id`, `at`, `detail`.
Append-only: a row, once written, is never updated and never removed.

Derived rather than stored: a board column's count, a page's effective grant set, the child-page
count a publish confirmation reports, and a `unique_id` property's rendered key, which is its
per-database prefix joined to its integer.

Uniqueness and counters. The counter behind a `unique_id` property belongs to its database, advances
by one on each new row and never goes backwards and never reissues a number, so `ZEN-3` names one
row for the life of the database even after that row is deleted. Two rows created at the same moment
receive two different keys.

The structural invariants, stated together: a page sits in exactly one teamspace; a block sits on
exactly one page and a move changes its position, never its page; block depth never exceeds 5; a
published page always carries a slug and the slug is unique; every principal in a group appears in
it once; and an activity row, once written, is never changed.

Two writes to the same block carrying the same `version` do not both succeed. Exactly one is
accepted, the block's `version` advances by one, and the other is rejected as a conflict with the
block left at the accepted writer's value. This holds under real concurrency.

**Seed data.** Four principals as listed in User roles. One group, `Editors`, containing
`member@example.com`. Three teamspaces: `Engineering` (slug `engineering`, `open`, with `admin`,
`member` and `member2` as members), `People Ops` (slug `people-ops`, `closed`, with `admin`), and
`Board Papers` (slug `board-papers`, `private`, with `admin`). Five pages: `Engineering Handbook` in
`Engineering`, unpublished, carrying a heading block, a paragraph block, a to-do block and a callout
block; `Release Notes` in `Engineering`, published at the slug `release-notes`, carrying two blocks;
`Onboarding Checklist` in `Engineering`, unpublished, carrying one grant of effect `deny` for
`member2@example.com`; `Compensation Bands` in `People Ops`, unpublished; and `Board Minutes` in
`Board Papers`, unpublished. One database, `Company Tasks`, whose page sits in `Engineering`, with
the properties `Project` (title), `Team` (select), `Date` (date), `Created by` (created by),
`Key notes` (text, not visible to a guest) and `Status` (status, with the options `To-do`,
`In progress`, `In review` and `Complete`), a `unique_id` prefix of `ZEN`, four rows one in each
status, and two views named `Company tasks` (table) and `Current sprint` (board grouped by
`Status`). One attachment, `handbook-cover.png`, already in the bucket on `Engineering Handbook`.
The guest `guest@example.com` holds one `read` grant on `Company Tasks` and nothing else.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Constraints

- One workspace. There is no workspace switcher that switches to a second workspace, no
  organization above it, and no consolidation between workspaces.
- No realtime transport, no presence, no cursors, no typing indicators, no offline store.
- No comments, no mentions, no backlinks, no synced blocks, no templates, no page history browser.
- No formulas, no relations, no rollups. No timeline, calendar, gallery, list or chart view.
- No AI assistant, no agents, no autofill, no meeting notes, no metered units.
- No billing, no seats, no plans, no invoices, no payment provider.
- No federated sign-in, no directory provisioning, no domain verification, no passkeys, no second
  factor, no recovery codes.
- No automations, no connectors, no calendar integration, no buttons that call out, no inbound or
  outbound webhooks, no public developer interface.
- No email and no notification delivery of any kind, and no inbox.
- No custom domains and no certificate management. Published pages are served by this app under its
  own origin.
- No data-loss prevention, no security event streaming, no retention policy engine, no erasure
  workflow, no residency choice, no key management.
- No marketing site, no pricing page, no comparison matrix, no question accordion, no contact form.
- One locale, English. Internationalisation is out of scope: no locale negotiation, no per-locale
  number, date or currency formatting, no translated interface strings, and no right-to-left
  mirroring.
- No external network calls at runtime beyond the two backing services named in this brief.
- No native application and no packaged desktop build.
- The app must stay responsive with 10000 blocks across 500 pages in one teamspace and 5000 rows in
  one database.

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

**API shapes.** Field names are exact. A list endpoint returns a top-level JSON array. A successful
call returns the named resource or shape; an invalid or unauthorized call is rejected as a client
error, never a `5xx` and never a silent success. The conventions hold across every endpoint: an
identifier is an opaque string and is never parsed for meaning; a timestamp is ISO-8601 in UTC with
a trailing `Z`; a rejected request carries a machine-readable `code` and a human-readable `message`;
and an unknown field in a request body is refused rather than ignored. Pagination is by cursor: a
paged request takes `start_cursor` and `page_size` and the response carries `has_more` and
`next_cursor`, the cursor is opaque, and it stays stable while rows are inserted. Bearer auth is
required on everything except
`POST /api/auth/identify`, `POST /api/auth/login`, `GET /api/health`, `GET /api/public/pages/{slug}`
and `GET /api/public/attachments/{attachmentId}`.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/identify` | `{ "email" }` | `{ "method" }`, identical for a known and an unknown address |
| `POST /api/auth/login` | `{ "email", "password" }` | `{ "access_token", "principal_id", "workspace_role" }` |
| `POST /api/auth/logout` | none | `{ "ok" }` |
| `GET /api/me` | none | `{ "principal_id", "email", "display_name", "workspace_role" }` |
| `GET /api/health` | none | `{ "status" }` |
| `GET /api/teamspaces` | none | array of `{ "id", "name", "slug", "access_mode", "description" }` |
| `PATCH /api/teamspaces/{id}` | `{ "access_mode" }` | the teamspace |
| `GET /api/pages/{pageId}` | none | `{ "id", "title", "icon", "teamspace_id", "parent_page_id", "published", "public_slug", "version" }` |
| `POST /api/pages` | `{ "teamspace_id", "title", "parent_page_id" }` | the page |
| `PATCH /api/pages/{pageId}` | `{ "title", "icon" }` | the page |
| `DELETE /api/pages/{pageId}` | none | `{ "ok" }` |
| `GET /api/pages/{pageId}/blocks` | none | array of `{ "id", "type", "text", "checked", "colour", "position", "depth", "version" }` |
| `POST /api/pages/{pageId}/blocks` | `{ "type", "text", "position", "depth" }` | the block |
| `PATCH /api/blocks/{blockId}` | `{ "text", "checked", "colour", "version" }` | the block, with `version` advanced |
| `POST /api/blocks/{blockId}/move` | `{ "position", "depth" }` | the block |
| `DELETE /api/blocks/{blockId}` | none | `{ "ok" }` |
| `POST /api/blocks/{blockId}/restore` | none | the block |
| `GET /api/pages/{pageId}/access` | none | array of `{ "subject_type", "subject_id", "subject_name", "level", "effect", "source" }` |
| `POST /api/grants` | `{ "resource_type", "resource_id", "subject_type", "subject_id", "level", "effect" }` | the grant |
| `DELETE /api/grants/{grantId}` | none | `{ "ok" }` |
| `GET /api/databases/{dbId}` | none | `{ "id", "name", "properties", "views" }` |
| `GET /api/databases/{dbId}/views/{viewId}/rows` | optional `cursor` | array of row objects keyed by property name |
| `PATCH /api/views/{viewId}` | `{ "filter", "sort", "group_by", "visible_properties" }` | the view |
| `PATCH /api/rows/{rowPageId}` | `{ "<property name>": value }` | the row |
| `POST /api/pages/{pageId}/attachments` | the file, plus `filename` | `{ "id", "filename", "content_type", "byte_size", "sha256", "object_key" }` |
| `GET /api/attachments/{attachmentId}` | none | the object bytes |
| `POST /api/pages/{pageId}/publish` | `{ "slug", "include_subtree" }` | `{ "slug", "pages_published" }` |
| `DELETE /api/pages/{pageId}/publish` | none | `{ "ok" }` |
| `GET /api/public/pages/{slug}` | none | `{ "title", "blocks" }` for a published page only |
| `GET /api/public/attachments/{attachmentId}` | none | the object bytes, for an attachment on a published page only |
| `GET /api/search` | `q` | array of `{ "page_id", "title", "teamspace_id", "excerpt" }` |
| `GET /api/admin/members` | none | array of `{ "id", "email", "display_name", "workspace_role", "is_active" }` |
| `POST /api/admin/members/{id}/deactivate` | none | the principal |
| `GET /api/admin/groups` | none | array of `{ "id", "name", "members" }` |
| `POST /api/admin/groups/{id}/members` | `{ "principal_id" }` | the group |
| `DELETE /api/admin/groups/{id}/members/{principalId}` | none | `{ "ok" }` |
| `GET /api/admin/activity` | optional `cursor` | array of `{ "id", "actor_principal_id", "action", "resource_type", "resource_id", "at", "detail" }` |

**The error catalogue.** A rejected request carries one of these exact `code` values and no other,
because a caller branches on the code rather than on the message:

| `code` | Meaning |
|---|---|
| `unauthorized` | no valid credential was presented |
| `forbidden_permission` | the authorization decision denied the action |
| `not_found` | the resource does not exist, or the caller may not know that it does |
| `conflict_version` | the `version` supplied is not the version stored |
| `conflict_state` | the resource is in a state that forbids this action |
| `validation_failed` | the request is malformed, carrying a per-field list in `details` |
| `rate_limited` | too many attempts, carrying how long until they are accepted again |
| `dependency_unavailable` | a backing service this call needs did not answer |

`not_found` covering "exists, but you may not know that" is deliberate and is the same principle as
the identify response: a distinct denial for a resource whose very existence is confidential is an
enumeration oracle. A request for a page inside a private teamspace, and a request for a page
identifier that was never issued, both answer `not_found`. A store error and a stack trace never
reach a caller.

**No mocks.** `PostgreSQL` and `minio` are the fact. An in-memory list of attachments, a hardcoded
object key the app never writes, a file written to the app container's own filesystem, a data URI
held in a database column, or a `{"ok": true}` response the app returns to itself are each a
contract violation however good the interface looks. The named provider is the fact - the app's UI
and its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A member signs in, edits a page block by block, files it in a teamspace and publishes it, and a
signed-out stranger reads it at its public address. A page inside a private teamspace, or one
carrying an explicit deny, stays unreadable to the member it excludes through every surface the
product has, including a direct request and a search result. An uploaded attachment exists as a real
object in the bucket at its key, and its address denies a reader the page itself would deny.
