# Kanvo

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, sign in as `editor@example.com`, branch the file `Checkout Redesign`,
get that branch approved by `reviewer@example.com`, and merge it into the main
file, without hitting an error page. The hard part is what happens when the work
changes after the sign-off: an approval belongs to one exact version of a
branch, so a later push to that branch voids it and the merge is refused rather
than warned about. The refusal has to be true of the stored record, not of the
screen: the main file must carry no merge version, and the branch must still be
sitting in review, for anyone who asks the server directly.

## Overview

Kanvo is an organization-wide design workspace. A member signs in, drills down
through their organization to a team, a project and a file, and works on that
file as a board of named frames they can pan, zoom, move and rename. Several
members work on one file at once and see each other's cursors. Frames carry
comment threads. A file's components can be published as a library other files
subscribe to, and a subscriber takes a new version when it chooses to rather
than when the library changes.

The part that makes it an organization's tool rather than a drawing tool is what
sits around the file. Work that needs sign-off is done on a branch, handed to a
named reviewer, approved against a specific version, and merged. Administrators
run members, roles, seats and identity enforcement from a console that is
separate from the workspace, and every governed transition lands in an
append-only audit stream that an administrator can read but nobody can rewrite.

The governance failure this product exists to prevent has one shape: approved,
then quietly changed, then merged. Preventing it is the single hardest guarantee
here, and it is a refusal rather than a warning.

Kanvo deliberately is not a vector drawing tool: a frame is a named rectangle on
the board, not a path editor. It has no billing, no payment processor, no
invoices, no plugins, no embeds, no outbound callbacks, no search index, no
uploaded image bytes and no background job runner.

## User roles

Three organization roles. Every account is seeded; there is no signup route and
no registration form anywhere in the product.

| Role | Can read | Can write |
|---|---|---|
| `editor` | files in projects belonging to teams they are a member of, and those files' comments, branches and reviews | edit frames on those files, start and reply to comment threads, resolve threads, publish a library version from a file they can edit, apply a library update, create a branch, request review on a branch they created. **Cannot approve any branch. Cannot merge any branch. Cannot reach any administration screen or endpoint.** |
| `reviewer` | the same files, plus every branch and review on them | everything an `editor` can do, plus approve, request changes on, and merge a branch whose source file sits in a project of a team they are a member of. **Cannot approve a branch they created themselves. Cannot approve or merge a branch on a file belonging to a team they are not a member of. Cannot reach any administration screen or endpoint.** |
| `org_admin` | the member list, identity settings and the whole audit stream | change a member's organization role, change a member's seat type, invite a member, deactivate a member, set identity enforcement. **Cannot read or edit the contents of a file unless they hold a grant on it through a team. Cannot approve or merge a branch. Cannot delete, edit or reorder an audit record.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from an `editor`
session to any `reviewer`-only or `org_admin`-only endpoint must be rejected by
the server (an unauthorized request is denied, not served), leaving the
protected state unchanged.

Role is not the whole answer. A `reviewer` is scoped by relationship: they may
decide only on branches whose source file sits in a project of a team they
belong to, and a reviewer from a peer team is denied on both the decision and
the merge. An `org_admin` holds no implicit grant on content: administering an
organization and reading its designs are separate powers, and an administrator
who does hold a team grant and opens a file has that open recorded under its own
audit action rather than as an ordinary open.

A file a member may not see and a file that does not exist give the same answer,
down to the same body. An identifier that names no file, however it is formed,
is a file that does not exist. Anything else tells a stranger what the organization is
working on.

**How the answer is reached.** One decision answers "may this member do this to
this thing", and every read and every write asks it before any data is loaded.
The interface asks it too, so that it can hide what the member cannot do, but
the server never believes the interface: performing any action straight through
the API with the interface bypassed must give exactly the answer the interface
would have given. The order is fixed and it is the whole model:

1. collect every grant that applies, across the organization, the team, the
   project and the file;
2. if any explicit deny applies, the answer is denied, and no allow overrides
   it;
3. otherwise take the union of what those grants allow;
4. apply the attribute rules as filters, each of which can only remove a
   capability and never add one;
5. if nothing allowed the action, the answer is denied.

Step four is what keeps the model readable: an attribute that could also grant
would be a second, hidden permission system. The attributes this product reads
are the resource's organization, the member's team memberships, the member's
seat type, and the start and end of any time-bounded grant. A grant that has
expired is powerless the moment it expires, because the question is asked fresh
every time and not because some later cleanup removed the row.

A grant may be direct: one named member given edit or view on one named file
without restructuring the project. There is exactly one way to be stricter
rather than more generous, and it exists because administrators ask for it
constantly: a direct deny on one file for one member, which beats every allow
from every level. A direct deny carries a reason, and both granting and revoking
are recorded.

**Tenant isolation.** Every tenant-scoped row carries its organization
directly, not only through a chain of relationships, and every query is scoped
by it. A read that fails to scope itself returns nothing rather than everything,
so the classic missing filter is an empty list and never another organization's
work.

Seeded accounts, all with the password `deku-demo-pw-2026`:

| Address | Role | Seat | Teams |
|---|---|---|---|
| `editor@example.com` | `editor` | `full` | `Atlas` |
| `editor2@example.com` | `editor` | `full` | `Atlas` |
| `reviewer@example.com` | `reviewer` | `full` | `Atlas` |
| `reviewer2@example.com` | `reviewer` | `full` | `Beacon` |
| `org_admin@example.com` | `org_admin` | `view_only` | none |

A seat is what a member costs and a role is what they may do. They are
independent: `org_admin@example.com` holds the highest role on the cheapest
seat, and that combination is legal and must stay legal.

## Core features

### Branching, review and the approval state machine

This is the feature the rest of the product exists to support.

A branch is a fork of a file that carries its ancestry. It moves through one
state machine, and the same machine serves every review in the product:

```
draft -> in_review -> approved -> applied
  ^         |            |
  |         v            |
  +-- changes_requested  |
  |                      |
  +-- withdrawn <--------+
```

1. Creating a branch on `Checkout Redesign` requires edit access on it, records
   the source file's current version as the branch's base version, and leaves
   the main file untouched. Editing the branch never changes the main file.
2. Requesting review names exactly one reviewer and moves the branch from
   `draft` to `in_review`. A request naming no reviewer, or naming a branch with
   nothing changed on it, is rejected as invalid and the branch stays `draft`.
3. A reviewer may move a branch from `in_review` to `approved`, or to
   `changes_requested`. A `changes_requested` decision requires a comment; a
   decision submitted without one is rejected as invalid and the branch stays
   `in_review`.
4. A branch in `changes_requested` returns to `in_review` when the requester
   pushes any change to it.
5. **An approval binds to a version, not to a branch.** Approving records the
   branch's current version as the approved version, and the review panel shows
   that version beside the recorded approval.
6. **A push to the branch after an approval invalidates that approval.** The
   invalidation happens in the same act that stores the new version, so the
   branch is never left holding a live approval against a version that is no
   longer its latest. The invalidation returns the branch to `in_review`, so a
   fresh approval is needed against the new version. The review panel says the
   approval was invalidated and names the version that superseded it.
7. **A merge is refused unless the branch's current version is the version the
   live approval was bound to.** A merge attempted after the approval was
   invalidated is refused, the main file gains no merge version, and the branch
   stays out of `applied`. This is a refusal, not a warning, and it must be true
   of the stored record: reading the main file and the branch straight from the
   server after the refusal must show the main file unchanged and the branch
   still in review.
8. A member may not approve a branch they created. Self-approval is denied and
   the branch state does not change.
9. A reviewer may decide and merge only on a branch whose source file sits in a
   project of a team they are a member of. `reviewer2@example.com`, who is in
   `Beacon` and not in `Atlas`, is denied on both the decision and the merge for
   a branch on `Checkout Redesign`, and the branch row is not changed.
10. An `editor` is denied on every decision endpoint and on merge, whatever
    their relationship to the branch, and the branch row does not change.
11. A successful merge appends one merge version to the main file, moves the
    branch to `applied`, and records the merged version on the branch. Merging
    the same branch twice produces exactly one merge version: the second attempt
    is refused and no second version exists.
12. A branch may be withdrawn by its creator at any time, from any state other
    than `applied`, by sending the decision `withdrawn`; a withdrawn branch is
    never merged.

Review mail goes out over real SMTP to the mail service at `SMTP_HOST`, which is
Mailpit, already running. Exactly three transitions send mail, each sending
exactly one message to exactly one recipient, with no cc and no bcc:

| Transition | Recipient | Subject |
|---|---|---|
| review requested | the named reviewer | begins with `Review requested: ` followed by the branch name, for example `Review requested: Compact Payment Step` |
| approved | the member who requested the review | begins with `Review approved: ` followed by the branch name |
| merged | the member who requested the review | begins with `Branch merged: ` followed by the branch name |

Every one of those messages has a non-empty body naming the branch and the file
it belongs to. No other transition sends mail: `changes_requested`, a withdrawal
and an invalidated approval send nothing at all.

Mail is one channel; the other is in the product, and the in-product channel
carries everything and is never suppressed. Every review transition appears in
the notification centre of the member who requested the review, including the
transitions that send no mail, and a review request also appears in the named
reviewer's. The centre carries an unread count, and the read position is stored
on the server so the count agrees wherever the member signs in. Notifications
fall into two categories, `review` and `membership`. A member may turn off
`membership` mail; `review` mail addressed to that member cannot be turned off,
because the whole point of a review request is that the reviewer learns about
it.

### Sign in and the workspace shell

Sign-in runs against the organization identity provider, which is Keycloak,
already running at `AUTH_URL`. The sign-in form asks for the address first and
only then for the method the organization's policy resolves for that address,
and the resolution answer must not disclose whether an account exists: it
reports the policy for the domain, never for the address.

1. Signing in with a seeded address and `deku-demo-pw-2026` succeeds and lands
   on `/app`, or on the protected path the visitor originally asked for.
2. Requesting any `/app` or `/admin` route without a session redirects to
   `/signin` carrying the attempted path, and the visitor lands on that path
   after signing in.
3. Signing in with a wrong password is refused, no session is created, and the
   answer does not say whether the address exists.
4. The session is an opaque reference resolved on every request, so a member
   deactivated by an administrator is refused on their very next request rather
   than at some later refresh.
5. Non-browser callers obtain a bearer token from `POST /api/auth/login` with
   the same credentials. The answer carries that token as `access_token`, and
   every endpoint except the login route, the health route and the public
   routes requires it.
6. Sign-in is rate limited per address, whether or not an account exists for
   that address. After `10` failed attempts for one address inside
   `15 minutes`, every further attempt for that address is refused for the rest
   of that window, even with the right password, and the refusal says the
   address is locked rather than repeating the wrong-password answer. Sign-in
   is also limited per source address, far more loosely: `100` failed attempts
   from one source inside `15 minutes` lock that source out, so one person
   mistyping a password never locks out a colleague on the same network.

The shell resolves to exactly one of `boot`, `unauthenticated`, `provisioning`,
`ready`, `degraded` and `evicted`, and the working area renders nothing until
the shell is `ready`. `degraded` is not an error screen: when the live
connection is down, a member still reads every file they had open, the write
controls on the board are disabled, and a banner says plainly that their edits
are not reaching anybody.

Switching the active organization aborts every request in flight for the
previous one, drops every cached list keyed to it rather than marking it stale,
and resets to the new organization's home rather than mapping the current path
across.

### Projects, files and the frame canvas

Work is contained in a hierarchy, and every level of the containment hierarchy
except the last is a permission boundary: an organization holds teams, a team
holds projects, a project holds files, and a file holds frames. A member drills
down through it. A project shows a board of its files. A file opens as a canvas
of named frames that pans and zooms.

1. Opening `Checkout Redesign` shows the frames `Payment Step` and
   `Confirmation`.
2. Moving a frame is visible on the next drawn frame, before any answer comes
   back from the server, and the stored position matches what was shown once the
   save lands.
3. Reloading the file shows every frame at its stored position and size. A
   position that only ever existed on screen is not a saved position.
4. A frame can be added, renamed and deleted. A deleted frame leaves the board
   and does not come back on reload.
5. The scene is a tree and stays a tree: a move that would make a frame its own
   ancestor is refused and the tree is left exactly as it was, never repaired
   into some other shape.
6. Sibling order is total and agreed. Two members adding a frame at the same
   position under the same parent must both end up with their frame present,
   in one order that every later reader of the file sees identically, with
   neither insert lost and neither overwriting the other.
7. A member with read access only sees every tool except comment hidden, and a
   write sent straight to the API from such a session is denied and changes no
   stored frame.
8. When the server declines a write, the canvas returns to the state it recorded
   before the attempt and an inline banner names what was reverted and why.

**Two people changing one frame.** This is the ordinary case, not the exception,
and the rule is per kind of change rather than per frame. Position, size and
name are last writer wins, ordered by the sequence the server assigns and never
by a client's clock, so two members who both move one frame converge on the same
final position and every reader sees it. Order within a parent is not last
writer wins: both inserts survive, per rule 6 above. A deletion beats a
concurrent change to the same frame: a rename that arrives for a frame already
deleted is discarded and the frame is not resurrected, because bringing back
something a colleague deleted on purpose is a worse outcome than a lost rename.

A client whose live connection drops and comes back catches up on everything it
missed and keeps every change it had already committed; nothing it committed
before the drop is lost, and nothing it attempted while disconnected is applied
silently afterwards.

### Presence and live cursors

Presence is what makes this collaboration rather than turn-taking. A member is
present in a file while their client holds it open. A non-browser client takes
part by reading `GET /api/files/{file_id}/presence`: each read counts the
calling member as present in that file for the following `30 seconds`.

1. Two members with the same file open each see the other's cursor, carrying the
   other's display name.
2. A member's cursor colour is derived from their identity, so the same person
   is the same colour in every later session.
3. No two members in one file are shown the same presence colour.
4. Presence is never written down. Closing the tab removes the cursor, and
   nothing about where anybody's pointer was survives the session anywhere.

### Comments on a frame

1. A thread is anchored to a named frame and is listed against that frame, not
   against a point on the page.
2. Replies in a thread are ordered oldest first.
3. The author may edit their own comment for `15 minutes` after posting. After
   that the edit is refused and the panel says a correction is a reply.
4. Only the comment's author may edit it. Another member's edit is denied and
   the stored body does not change.
5. Deleting a comment replaces its body with a tombstone and keeps the thread
   and its replies intact; the thread is never removed with the comment.
6. Resolving a thread records who resolved it and when, hides it from the
   default view, and raises the resolved count.
7. A thread started on a branch travels to the main file when the branch merges,
   and carries a note naming the branch it came from.

### Component libraries

A library is a file whose components have been published for other files to
build with. In a library file every top-level frame is a component, and the
frame's name is the component's name. A frame may be saved with an empty name
while it is still being drawn. Publishing is a versioned, named act.

1. `Atlas Core Kit` is published as the library `Atlas Core`, whose version `1`
   holds the components `Primary Action` and `Field Label`, the two top-level
   frames of `Atlas Core Kit`. A published version
   carries three kinds of object: a named component, a named style, and a named
   variable belonging to a variable collection, where a collection is the unit a
   consumer switches between its modes.
2. Publishing a new version is refused while any component in the file is
   unnamed, and the refusal names the component. Nothing is published.
3. Publishing is refused when two components on one page share a name, and the
   refusal names the collision.
4. Publishing is refused when a component contains an instance of itself. The
   refusal happens at publish, never at render.
5. A successful publish writes the next version number, the changelog line the
   publisher wrote, the publisher and the time, and that version is immutable
   afterwards: a later publish adds a version, it never edits one. The library
   page lists every published version with its number beside the changelog line
   its publisher wrote.
6. `Checkout Redesign` subscribes to `Atlas Core` pinned at version `1`. When
   version `2` is published, `Checkout Redesign` shows an update badge and its
   own content is unchanged until somebody applies the update.
7. Applying an update moves the pin and is one undoable operation, never a
   sequence of separate changes the member has to undo one at a time.

### The organization admin console

A separate routed area only an `org_admin` can reach. Every write in it appends
an audit record.

1. The member list shows each member's address, organization role, seat type,
   team count, status and the date the member was last active. It shows a date,
   never a live online signal: a live presence indicator in an administrative
   list is surveillance rather than administration.
2. Changing a member's organization role, or their seat type, takes effect on
   that member's next request, not on their next sign-in.
3. A bulk role change is previewed before it applies: the preview names how many
   rows will change and how many the actor is not permitted to change. Applying
   it changes only the permitted rows and reports the outcome per row, never as
   a single success.
4. Inviting an address that is already a member returns the existing membership
   and creates no second membership row.
5. An invitation for a malformed address is rejected as invalid, names the
   field, and writes nothing.
6. Deactivating a member releases their seat immediately, and their content is
   retained and surfaced as needing a new owner rather than deleted.
7. Identity enforcement moves between `optional` and `required`. Setting it to
   `required` while no break-glass principal is named is refused, with an
   explanation, rather than warned about: turning federation on with nobody
   holding a password can lock every administrator out of the organization.
8. At most two break-glass principals may be named.
9. Every administration endpoint denies a session that is not an `org_admin`,
   and the denied write leaves the stored row unchanged.

### The audit stream

1. Every governed transition appends one record carrying the time, the acting
   member, the action, the resource, and whether the outcome was allowed or
   denied. A denial carries a reason.
2. The action is drawn from a closed vocabulary and is never a free string:
   `sign_in`, `sign_in_failed`, `member_invited`, `member_role_changed`,
   `member_seat_changed`, `member_deactivated`, `grant_granted`,
   `grant_revoked`, `file_created`, `file_opened`, `file_renamed`,
   `file_trashed`, `admin_content_access`, `library_published`,
   `library_subscription_changed`, `review_requested`, `review_approved`,
   `review_changes_requested`, `approval_invalidated`, `review_withdrawn`,
   `branch_merged`, `identity_policy_changed`, `audit_exported`.
3. An invalidated approval writes its own `approval_invalidated` record naming
   the approval, the version it was bound to, the version that superseded it and
   the member who pushed. That single record is the evidence the whole workflow
   exists to produce.
4. An administrator opening content they hold no team grant on is recorded under
   `admin_content_access`, never as an ordinary `file_opened`.
5. The stream is append-only in the store itself, not by convention: the
   application's own database role holds no update and no delete on it. An
   attempt to change a recorded event fails.
6. Only an `org_admin` may read the stream, and it can be filtered by actor, by
   action and by time range.

### The public surface

1. `/` is a public overview of the product, readable without a session, leading
   with one primary action that reaches `/signin`.
2. Every internal link on every public route resolves. A public route that links
   to an address the app does not serve is a defect.
3. `/access` is a public form by which somebody asks for access to an
   organization. It takes an address and a note, validates the address inline
   without discarding what else was typed, and records the request.
4. The access form carries an unattended field named `company_website` that no
   person ever fills in. A submission that arrives with `company_website`
   non-empty is refused and records nothing at all. The same form submitted
   repeatedly in quick succession from one source, more than `5` times inside
   `1 minute`, is refused the same way, so an automated sender records nothing
   however many times it tries.
5. An address the app does not serve renders Kanvo's own not-found page, which
   answers not-found and carries a way back into the product. There is exactly
   one not-found experience, not a branded one and a bare framework one.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | public overview, one primary action leading to sign-in | public |
| `/access` | public access-request form | public |
| `/signin` | address first, then the method the policy resolves | public |
| `/sitemap.xml` | lists every public route | public |
| `/robots.txt` | points at the sitemap | public |
| `/app` | signed-in home: recent files and the team trail | member |
| `/app/teams/{team_id}` | a team's projects | member of that team |
| `/app/projects/{project_id}` | the file board for a project | member of the owning team |
| `/app/files/{file_id}` | the frame board and the inspector | grant on the file |
| `/app/files/{file_id}/branches/{branch_id}` | a branch's frame board and its review panel | grant on the source file |
| `/app/libraries/{library_id}` | a library, its versions and its components | member of the organization |
| `/admin/members` | members, roles, seats, bulk actions | `org_admin` |
| `/admin/identity` | identity configuration and enforcement | `org_admin` |
| `/admin/audit` | the audit stream, filtered | `org_admin` |

**Entry and redirects.** An unauthenticated request for `/app` or `/admin`
redirects to `/signin` carrying the attempted path, and lands there after
sign-in. Sign-in with no attempted path lands on `/app`. Sign-out returns to `/`
and ends the session at once, and the back button does not restore a signed-in
screen. A session revoked mid-action leaves the current screen in place, shows
the evicted explanation with one action, and does not discard what was typed. An
`editor` who asks for an `/admin` route is denied by the server, and the rail
never showed them the link. A member who asks for a file in a team they do not
belong to gets the same answer as for a file that does not exist.

**Journeys.**

1. *Move a frame.* `editor@example.com` signs in, opens `Atlas`, then
   `Atlas Mobile`, then `Checkout Redesign`. They drag `Payment Step`. It moves
   at once, a banner confirms the save, and a reload shows it at its new place.
2. *Two in one file.* `editor@example.com` and `editor2@example.com` both open
   `Checkout Redesign`. Each sees the other's named cursor in its own colour.
   `editor2@example.com` closes the tab and the cursor disappears leaving
   nothing behind.
3. *Comment.* `editor@example.com` selects `Confirmation`, starts a thread,
   `editor2@example.com` replies, the author edits their own comment inside the
   window, and the thread is resolved.
4. *Publish.* `editor@example.com` opens `Atlas Core Kit`, is refused a publish
   while a component is unnamed, names it, writes a changelog line, and
   publishes version `2`. `Checkout Redesign` shows an update badge and has not
   changed; applying the update moves its pin to version `2`.
5. *The review journey.* `editor@example.com` branches `Checkout Redesign` as
   `Compact Payment Step`, moves `Payment Step` on the branch, and requests
   review from `reviewer@example.com`, who receives one message.
   `reviewer2@example.com` tries to approve and is denied.
   `editor@example.com` tries to approve their own branch and is denied.
   `reviewer@example.com` approves. `editor@example.com` pushes one more change,
   which voids the approval, and the merge is then refused with the main file
   unchanged. `reviewer@example.com` approves again and the merge succeeds,
   appending one merge version and sending one message to
   `editor@example.com`. `org_admin@example.com` opens `/admin/audit` and finds
   every one of those transitions, attributed.
6. *Administer.* `org_admin@example.com` previews a bulk role change, applies
   it to the permitted rows only, re-invites an existing member and gets the
   existing membership back, and is refused when setting enforcement to
   `required` with no break-glass principal named.
7. *Public.* A visitor reads `/`, follows the one primary action to `/signin`,
   submits `/access` with `company_website` filled and is refused, and asks for
   an unknown address and gets Kanvo's own not-found page.

**States.** Every list has an empty state, every screen a loading state, and no
error crashes the app. A loading skeleton matches the geometry of what replaces
it, so nothing jumps when the real content arrives. The file board's empty state
offers create to a member who may write and says so plainly to one who may only
read, and a board emptied by a filter says how many are hidden and offers to
clear it. The frame board shows the last committed still, dimmed, with a
determinate bar, and the toolbar says editing is not yet possible rather than
swallowing a drag it cannot apply. The approval control enters a pending state
and stays disabled until the server answers; on failure it returns to its
previous state and the banner names the reason, most often that the version
moved.

## UI/UX notes

Kanvo reads quiet. The north star is comprehension: somebody opening it should
understand in the first moment what state the work is in and who else is in it.
The register is operational, so the product is dense but organised, built for
scanning and repeated action, with no oversized hero and no marketing
composition where the working interface belongs. Space over dividers; calm over
expressive.

The ground is monochrome and the whole theme is one base colour at a ladder of
strengths rather than a second palette, which is what makes the dark theme a
change of one value. The page ground is a near-white neutral and body and
heading text is a near-black neutral. Secondary text is a mid neutral; hairlines
and control rings are the same text colour at a much lower strength; card and
panel grounds lower still. The primary action carries the near-black neutral
ground with a near-white neutral label and softens slightly under a pointer. The
secondary action has a transparent ground and a ring that strengthens under a
pointer. Fields sit on a near-white neutral ground with mid neutral placeholder
text. Deep neutral steps carry the dark theme's grounds.

Accent colour is reserved for status and for presence, and never touches page
chrome. A mid, vivid cyan is selection and the interactive accent on the board,
and the same colour at low opacity fills a selection. A mid, vivid green means
something succeeded, and a review approved is the only place in the product it
appears. A mid, vivid red means refused or destructive, and it appears nowhere
else. A light, vivid amber means a warning, and an invalidated approval wears
it. A mid, soft red ground with a near-white neutral label is the one opaque
semantic colour in the theme and carries a form error. Collaborator presence
draws from a set including a light, vivid blue, a light, vivid indigo and a
light, vivid magenta, one stable colour per person; a near-white cool neutral
and a near-white neutral are the tint grounds behind an empty-state
illustration. Three rules pin those words: the failure colour appears nowhere
except failure, the success colour nowhere except a completed governed
transition, and no two people in one file share a presence colour. The exact
shades are yours so long as those rules hold and the contrast floors below are
met. Against defaults: no screen dominated by one hue family with no second
signal, no decoration standing in for content, and no meaning carried by colour
alone.

Typography is `Inter` for the interface, with a metric-matched local fallback
ahead of the platform stack, and `JetBrains Mono` for identifiers, version
numbers and audit rows, so figures align wherever values stack. The metric-matched fallback
is required rather than optional: with a swap display strategy an unmatched
fallback reflows every heading on the page when the real face arrives. The scale
is `56px` set solid and `44px` at a leading of `1.1` for the public overview and
major headings at the widest width, dropping to `36px` set solid and `32px` at
`1.1` at the two narrower ones; `30px` at `1.2` and `24px` at `1.3` for lede and
card headings; `22px` at weight `320` and `1.35` for large body; `18px` at
weight `330` and `1.4` as the dominant text style in the product; `18px` at
weight `400` and `1.3` for navigation and dense body; `16px` at `1.45` for body
and the root default; `14px` at `1.45` for small print; `12px` at `1.3` for
captions; and `11px` at about `1.45` as the smallest legal line. Letter spacing is a function of size, tightening as size grows, expressed
as one rule rather than hard-coded per component.

Corner softness is a size relationship rather than one value used everywhere: a
control the height of a table row takes the smallest step, a hero action a
middle one, a full-width closing action the largest, and avatars and presence
chips are pills. Density is comfortable in the administrative tables and on the
board, and compact in the rail and the audit view, where rows sit tight so a
full page of events fits one screen. Elevation is a soft, wide, faint shadow
rather than a hard edge, and a control wears its ring on the inside rather than
as a border so that a pointer changing the ring causes no reflow.

Every control answers five states: resting, pointed-at, pressed, focused and
unavailable, and unavailable is never signalled by colour alone. Escape closes
any slide-over and returns focus to the control that opened it. Destructive
actions confirm first and the confirmation names the thing. Any action that can
take longer than a moment enters a loading state in which the label rises and
fades while an indicator rises into the space it left, and the control keeps its
width so nothing beside it moves. Hover styling applies only where the device
actually hovers, because without that guard a touch device holds the hover state
after a tap and the control reads as stuck.

Motion is eased: what a pointer causes is quick and settles, what a whole
section causes is slower and reads as deliberate. Only transform, opacity and
colour animate, never a layout property, and no control transitions everything
at once. The named moments are a frame settling after a drag, the slide-over
entering from the right, the inline banner arriving above the working area, the
update badge appearing on a subscribing file, and the review control's pending
state. Under a reduced-motion preference those entrances neither translate nor
fade and content is present at its final position from first paint, while the
short control transitions stay, because a ground change under a pointer is not
the motion that preference is about and removing it makes controls feel broken;
the loading indicator becomes static.

Light is the committed default and is designed fully. Dark is required and is
the same design with the base colour swapped and the ladder inverted; the
accents do not invert, each taking a dark variant chosen for contrast, and every
presence colour clears the contrast floor against both grounds. The theme
follows the platform preference, can be overridden, and the override is stored
per member on the server so it follows them between devices.

The arrangement is responsive and holds at every width between the named tiers.
The left rail is persistent at the widest width, collapses to an icon rail that
expands on hover in the middle band, and becomes an overlay drawer at the
narrowest; the inspector goes from persistent to an overlay from the right to a
bottom sheet; administrative tables go from every column, to the four primary
columns with the rest behind a row expander, to one card per row; the toolbar
groups behind an overflow as space runs out. The board stays usable at every
width, at least for reading and commenting, because a design tool that is a
blank screen on a phone fails the reviewer who opens a shared link from a
message. Screen width and pointer type are separate questions: on a coarse
pointer every hit area is at least `44` by `44`, every hover-only affordance has
a tap or focus equivalent, one finger pans the board, two fingers zoom, and a
long press begins a drag so panning is never mistaken for moving a frame. At a
narrow viewport nothing overflows sideways and every navigation target stays
reachable, whether from the rail's overlay drawer or from the toolbar overflow.
The layout stays usable at `200%` browser zoom and at a `200%` platform text
size with no loss of content or function and no sideways scrolling.

Accessibility is WCAG AA on every route and at every width, and these are
contract rather than taste. Every focusable element carries a visible focus
indicator drawn as two rings, an inner one in the ground colour and an outer one
in the foreground colour, so it stays visible on either ground and over an
illustration, and it is never removed. Focus is trapped only inside a slide-over
or dialog, deliberately, and released on close back to the control that opened
it. The skip link is the first focusable element, becomes visible on focus, and
moves focus rather than only scrolling. Focus order follows visual order at
every width. Contrast is verified rather than assumed: the muted secondary
colour is a strength of the text colour and does not carry its ratio with it, so
it is checked at every size it is used at and the product carries two muted
steps rather than one that is wrong at half its usages, every accent used as a
foreground is checked against both grounds, and the focus ring clears `3:1`
against adjacent colours. One main landmark per route, targeted by the skip
link; headings form a real outline; lists are lists; decorative graphics are
hidden from assistive technology; every meaningful icon carries a name. Keyboard
navigation reaches everything: the board is a labelled application region with a
frame tree beside it that is a real tree view and the primary keyboard path into
the document, and every direct manipulation on the board has a keyboard
equivalent. Comments are a feed with each thread a labelled group and new
comments announced politely. Presence is announced on request rather than
continuously, because a live region reporting every cursor move is unusable.
Administrative tables are real tables with header associations, sortable columns
announcing their state, and a caption naming the row count.

Every screen leads with exactly one primary action, visually distinct from every
secondary one: the public overview leads with the action that reaches sign-in, a
project leads with create, a file leads with the branch action, and a review
panel leads with the one decision the viewer is entitled to make. No screen
carries two controls wearing the primary treatment.

## Technical requirements

Each route arrives as server-rendered HTML that is readable before any script
runs, and only the interactive regions hydrate as islands: the frame board, the
comment panel, the review panel and the member table. The frontend is Astro with
islands. The backend is FastAPI on Python 3.12, serving the HTTP API on the same
origin under the `/api` prefix. The datastore is PostgreSQL, already running and
reached at `DATABASE_URL`. Identity is Keycloak, already running and reached at
`AUTH_URL`. Its realm is `deku` and the application's client is `kanvo-app`, a
public client with both the authorization-code flow and the direct password
grant enabled. The realm already holds the five seeded accounts with their
passwords, and the three organization roles `editor`, `reviewer` and `org_admin`
as realm roles on those accounts. Do not create the realm, the client, the roles
or the accounts: read them.
Mail is Mailpit, already running and reached over SMTP at `SMTP_HOST` and
`SMTP_PORT` with `SMTP_USER` and `SMTP_PASS`. `GET /api/health` returns `200`
once the app is ready. Every request writes one structured log line carrying the
method, the path, the status, the duration and a request identifier, and that
same identifier is returned to the client on an error and recorded on the audit
row.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor: the only backing services available in this environment are
PostgreSQL, Keycloak and Mailpit, and reaching for anything else is a contract
violation.

Read every host, port and credential from the environment. Never hardcode one.
The backing services are already running at those variables and must not be
downloaded, installed, compiled or started.

Sessions are an opaque reference carried in a cookie that is `HttpOnly`,
`Secure` and `SameSite=Lax`, scoped to the host and not shared with subdomains.
The reference is resolved on every request, which is what makes a deactivation
true on the member's next request instead of at some later moment. State-
changing requests carry a token bound to the session, and no state-changing
operation is reachable by a safe method.

The identity provider's own subject is the join key onto a member, never their
mail address. Addresses change, and treating one as an identity is how a renamed
employee becomes a second account and a departed one keeps their access.

A sitemap at `/sitemap.xml` lists every public route the app serves, and
`/robots.txt` points at it. Every public route carries its own title.

The schema is migrated as the app starts, so the first request after a cold
start meets a complete schema rather than a partial one, and migrations run once
however many times the app is restarted.

**The interface contract.** Versioning is explicit: the API's version is part of
the response, and a change that would break a caller arrives as a new version
rather than as a changed meaning for an existing field. Pagination is explicit
too: a list endpoint returns at most `500` rows per page as a top-level array,
newest first wherever the rows carry a time, and puts the cursor for the next
page in the `X-Next-Cursor` response header; a page is never unbounded. A write that the outside world could retry
accepts an idempotency key, and a retry carrying a key already seen returns the
first result and repeats no effect. Limits are stated rather than discovered: a
request body is bounded, an invitation carries at most `50` addresses, a
changelog line is bounded, and a request past a limit is rejected as invalid
rather than truncated. Validation is answered at the field: a rejected request
names every field that failed and why, in one answer rather than one field at a
time, keeps the valid fields, and writes nothing at all. A rejection that is
well formed but meaningless for the current state is distinguishable from one
that is malformed.

**Instrumentation.** Every request, every denial and every governed transition
is instrumented: the structured log line carries the outcome, and a denial
carries its reason, so an operator can answer which member was refused what and
when without reading the database.

**Language and localization.** The document declares its language. Timestamps
are stored and returned with their zone, never as a bare local time, and
user-facing copy is stored whole with blanks in it rather than glued together
from pieces, because a concatenated sentence cannot be translated.

**Security.** The session controls above are the product's security boundary,
and the test that matters is an interface bypass: every action driven straight
at the API, with the interface out of the picture entirely, must give exactly
the answer the interface would. A rule that only hides a control is not a rule.

**Performance and evaluation cost.** A permission evaluation for a list is one
question about the whole list, not one question per row; getting that wrong is
invisible on a small team and fatal on a large one. Scroll and animation stay
smooth: nothing reads layout in the same frame it animates in.

**Realtime synchronization and routing.** Changes made by one member reach the
others without either of them reloading the page, ordered by the sequence the
server assigns. Every route in the routing table below is reachable directly by
its address: the information architecture is addressable, so a member can send a
colleague a link to a file or a branch and the colleague lands on that exact
screen after signing in.

**Observability.** The obligation is that an operator can reconstruct what
happened without reading the database: the structured log line and the audit
record together carry it.

These properties must hold of the running system:

- Two members adding a frame at the same position under the same parent both
  end up with their frame stored, in one order every later reader agrees on,
  with neither insert lost. This holds under real simultaneous requests.
- A branch never ends up holding a live approval bound to a version that is not
  its latest, whatever order a push and an approval arrive in.
- Two merges of one branch produce exactly one merge version. The second is
  refused and no second version exists.
- Repeating an invitation for an address that is already a member returns that
  membership and creates no second membership row.
- A failed operation leaves no partial state: no orphaned row, no branch left
  half-merged, no audit record for a transition that did not happen.
- A project screen listing files resolves access for the whole list in one round
  trip rather than asking once per file, and the frame board stays interactive
  with `200` frames on a page.

## Data model

Twenty-two tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account
so a grader can sign in.

**organization** - `id`, `name`, `slug` (unique), `status`
(`active` or `suspended`), `created_at`.

**principal** - `id`, `primary_email` (unique, compared without regard to case),
`display_name`, `external_id` (the identity provider's subject, unique),
`status` (`active` or `deactivated`), `created_at`.

**membership** - `organization_id`, `principal_id` (unique together), `org_role`
(`editor`, `reviewer` or `org_admin`), `seat_type` (`full`, `collaborator`,
`view_only` or `guest`), `status` (`invited`, `active` or `deactivated`),
`source` (`seeded`, `invite` or `provisioned`), `last_active_at`,
`deactivated_at`.

**team** - `id`, `organization_id`, `name`, `created_at`.
**team_member** - `team_id`, `principal_id` (unique together), `team_role`
(`team_admin`, `editor` or `viewer`).

**grant** - the one table every permission is written in. `id`,
`organization_id`, `subject_id` (the member the grant is about),
`resource_kind` (`organization`, `team`, `project` or `file`), `resource_id`,
`capability_set` (the named role the grant carries), `effect`
(`allow` or `deny`, and `deny` is legal only when `resource_kind` is `file`),
`starts_at`, `ends_at` (both nullable, the bounds of a time-bounded grant),
`reason` (required when the effect is `deny`), `created_by`, `created_at`.
Reads come at this table from two directions and both must stay fast: everything
that reaches one resource, and everything one member can reach.

**project** - `id`, `organization_id`, `team_id`, `name`, `status`
(`active` or `trashed`), `created_at`. Two active projects in one team never
share a name, and trashing a project releases its name for reuse.

**file** - `id`, `organization_id`, `project_id`, `name`, `kind`
(`design` or `library`), `is_branch`, `source_file_id`, `status`
(`active` or `trashed`), `created_at`, `updated_at`. Two active files in one
project never share a name, and trashing a file releases its name for reuse.

**file_version** - `id`, `file_id`, `sequence` (rises by one per file, starting
at `1`), `kind` (`autosave`, `named` or `merge`), `label`, `created_by`,
`created_at`. `sequence` is the ordering authority for a file, and restoring an
earlier state appends a new version equal to it rather than rewinding, so
nothing between the two is lost.

**frame** - `id`, `file_id`, `parent_id`, `name`, `order_key`, `x`, `y`,
`width`, `height`, `status` (`active` or `deleted`), `updated_at`. No frame is
ever its own ancestor. Within one parent the order is total and agreed by every
reader, and two frames inserted at the same position under one parent both
survive with a stable relative order rather than one replacing the other.

**branch** - `id`, `source_file_id`, `branch_file_id` (unique),
`base_version_id`, `state` (`draft`, `in_review`, `approved`,
`changes_requested`, `applied` or `withdrawn`), `merged_version_id`,
`created_by`, `created_at`.

**review_request** - `id`, `branch_id`, `requested_by`,
`reviewer_principal_id`, `state` (`open` or `closed`), `created_at`.

**review_decision** - `id`, `review_request_id`, `decision`
(`approved` or `changes_requested`), `target_version_id`, `decided_by`,
`decided_at`, `invalidated_at`, `invalidated_by_version_id`.
`target_version_id` is what makes an approval belong to a version rather than to
a branch. A decision is never deleted; a superseded one is marked invalidated
and keeps its record.

**comment_thread** - `id`, `file_id`, `frame_id`, `resolved`, `resolved_by`,
`resolved_at`, `origin_branch_name`, `created_at`.
**comment** - `id`, `thread_id`, `author_id`, `body`, `edit_deadline`,
`tombstoned`, `created_at`. `edit_deadline` is `15 minutes` after `created_at`
and is stored rather than derived at read time.

**library** - `id`, `organization_id`, `file_id` (unique), `name`, `created_at`.
**library_version** - `id`, `library_id`, `number` (rises by one per library),
`changelog`, `published_by`, `published_at`. Immutable once written.
**library_component** - `id`, `library_version_id`, `name`.
**library_subscription** - `library_id`, `file_id` (unique together),
`pinned_version_id`.

**notification** - `id`, `organization_id`, `recipient_principal_id`,
`category` (`review` or `membership`), `branch_id`, `action` (one of the review
actions in the closed vocabulary), `created_at`, `read_at`. The unread count is
the number of the recipient's rows with no `read_at`.

**access_request** - `id`, `email`, `note`, `created_at`. A refused submission
writes no row.

**audit_event** - `id`, `organization_id`, `occurred_at`, `actor_principal_id`,
`action` (one of the closed vocabulary above), `resource_kind`, `resource_id`,
`outcome` (`allowed`, `denied` or `error`), `reason`, `detail`. The application
reads this table and appends to it and can do nothing else to it: an update or a
delete issued against it by the app's own database role does not succeed.

Derived rather than stored: a member's effective capabilities on a resource, a
file's current version number, a thread's reply count, a library's latest
version number, and whether a branch's live approval is still valid.

**Seed data.** One organization `Harborlight`, slug `harborlight`. Two teams,
`Atlas` and `Beacon`. Two projects, `Atlas Mobile` in `Atlas` and `Beacon Web`
in `Beacon`. Three files: `Checkout Redesign` and `Atlas Core Kit` in
`Atlas Mobile`, and `Beacon Landing` in `Beacon Web`. Two frames in
`Checkout Redesign`, `Payment Step` and `Confirmation`. Two top-level frames in
`Atlas Core Kit`, `Primary Action` and `Field Label`. One library `Atlas Core`,
published from `Atlas Core Kit` at version `1`, holding those two frames as its
components, with `Checkout Redesign`
subscribed and pinned at version `1`. The five accounts in `## User roles`, with
their roles, seats and teams exactly as listed there.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual detail that will not fit above. It adds nothing
the rest of the brief contradicts. Layout, spacing and softness are given as
relationships; the exact values are yours so long as the relationships hold.

**Grid.** Twelve columns with a gutter one spacing step wide and a side margin
that narrows as the window does, capped at a maximum content width. The margin
is widest at the widest tier, a little over half that in the middle band, and
narrower again at the narrowest, where the arrangement drops to four columns
because twelve columns at phone width produce columns narrower than a character.
The column width is a rule, not a rendered number: the available width less the
margins and the gutters, divided by the column count.

**Spacing.** One scale, a zero plus twelve steps expressed against the root font
size, running from a quarter of the root up to seven and a half times it. Steps
sit close together at the small end, so small gaps can be tuned finely, and far
apart at the large end, so large gaps read as deliberate breaks. Two composite
steps set the page rhythm: an ordinary section's vertical padding is five times
the root, and a full-bleed block's is half as much again.

**Corner softness.** Seven steps and a pill, and the step follows the height of
the control rather than one softness applied everywhere. The smallest chips are
barely softened, an ordinary control takes the dominant middle step, a hero
action roughly twice that, and a full-width closing action roughly three times
it. Avatars and presence chips are pills. A control about twice as tall as
another takes about twice its softness; applying one softness everywhere loses
the whole sense of scale.

**Control geometry.** Four sizes that form a scale rather than a set. A
navigation trigger is the shortest and has no ground. A standard action is a
little taller, padded about twice as wide as it is tall, and wears either the
primary ground or a transparent ground with an inset ring. A hero action is
close to twice the standard action's height, and a full-width closing action
spans the whole content box at about three times it. An icon button is square
and slightly shorter than a standard action. The label inside a standard action
sits in its own element with a little horizontal padding and its own transition,
which is what lets it rise out of the way for the loading indicator.

**Elevation.** Two steps, both a soft wide shadow at low opacity rather than an
opaque colour: a near one for a panel and a far one for an overlay. Controls
carry a hairline inset ring rather than a border, so a ring change under a
pointer causes no reflow. The header's bottom hairline and the panel dividers
are the same ring at the same strength.

**Leading and letter spacing.** Two leading ratios are tokens, a loose `1.45`
and a flat `1`. The dominant body text sits at `1.4`, and the largest heading is
set solid on the flat token. Letter spacing tightens in proportion to size, by
roughly a forty-fifth of an em at every size, so large headings tighten visibly,
navigation and control labels only slightly, and body sizes not at all.
Applying the largest heading's tightening to a small label has misread the rule.

**Motion timing.** Two durations carry the product: a fast one for anything a
pointer causes and a slower one for anything a whole section causes. A control
transitions its ground and its ring together on the fast duration while its
label translates independently on the same one. Nothing transitions every
property at once. At most `12` elements animate in one viewport, and an element
animating during a scroll does not read layout in the same frame.

**Shell geometry.** A top bar one toolbar tall carries the organization
switcher, search, create, help, notifications and the avatar menu. A left rail
about a sixth of a wide window carries recents, drafts, shared, favourites and
the team trail, and collapses to an icon strip as narrow as the top bar is
tall. The working area takes the remainder. An inspector a little wider than
the rail appears only inside a file and carries properties, comments, version
history and review. Banners anchor to the top of the working area. The rail
becomes the icon strip in the middle band and an overlay drawer at the
narrowest tier; the inspector becomes a bottom sheet at the narrowest tier.

**Board behaviour.** Zoom runs continuously from far out to far in with no
discrete steps, and is never coupled to document scroll position nor
intercepted by the browser's own zoom. A click selects the topmost frame whose
geometry contains the point, ignoring locked frames; a double click descends one
level; a shift click toggles membership in the selection; a marquee selects
every frame it intersects, or only those fully contained when the alt modifier
is held. A drag snaps to a `1px` grid and to the edges of siblings within `8px`.
An arrow key nudges by `1px` and shift with an arrow by `10px`. A corner handle
scales, preserving aspect ratio when shift is held and scaling about the centre
when alt is held. Rotation snaps to `15` degree increments when shift is held.
Every one of those changes local state first and sends the change second,
carrying the state it replaced so a refusal can be reversed exactly. Undo is per
member and never reverses a colleague's work; the stack holds at most `200`
entries, clears when the file closes, and skips an entry whose target has since
been deleted rather than applying it to nothing.

**Loading the board.** Four steps, and something is on screen after the first:
the frame, the file name and the page tabs with an empty surface; then the last
committed still, which is not yet interactive; then the live frames, at which
point selection becomes possible; then the other members' cursors. Between the
second and third steps the board is explicitly read-only and the toolbar says
so.

**Presence rates.** Cursor position is coalesced to at most `20` updates a
second per member, selection is sent on change, the viewport rectangle is sent
once it settles, and a member is marked idle after `120` seconds without input.
None of it is stored.

## Constraints

- One organization tenancy in the seeded data, but every query is scoped by
  organization and a member of one organization can reach nothing belonging to
  another.
- No signup, no self-registration, no password reset and no magic link. Accounts
  are seeded.
- No vector drawing: a frame is a named rectangle, not a path editor. No pen,
  no boolean operations, no image upload, no object store, no file export.
- No billing, no payment processor, no plans, no seats purchase flow, no
  invoices, no credits, no usage metering.
- No search index, no plugins, no widgets, no embeds, no third-party
  applications, no outbound callbacks, no chat integration.
- No background job runner, no scheduled work, no queue, no retry worker, no
  escalation timer and no delegation of approval authority.
- No data residency regions, no legal hold, no audit export file generation, no
  tamper-evidence digest chain.
- No marketing site beyond the single public overview route, no developer
  documentation site, no help centre, no status page, no blog, no template
  community, no consent banner and no analytics vendor.
- No native, desktop or mobile application, and no offline editing queue.
- No external network calls at runtime. The three backing services named above
  are the only ones that exist.
- The app must stay responsive with `200` frames on a page, `50` files in a
  project and `5,000` audit events in the stream.

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

**API shapes.** Field names exactly as written. A list endpoint returns a
top-level JSON array. A successful call returns the named resource or shape; an
invalid or unauthorized call is rejected as a client error, never as a server
error and never as a silent success. Every endpoint below except
`POST /api/auth/login`, `GET /api/health` and the public routes requires the
session cookie or a bearer token.

| Endpoint | Request body or query | Returns |
|---|---|---|
| `POST /api/auth/login` | `email`, `password` | `access_token`, `principal` |
| `GET /api/health` | none | a small JSON body |
| `GET /api/me` | none | `principal`, `memberships`, `capabilities` |
| `GET /api/teams` | none | array of teams the caller belongs to |
| `GET /api/teams/{team_id}/projects` | none | array of projects in that team |
| `GET /api/projects/{project_id}/files` | none | array of files |
| `GET /api/files/{file_id}/versions` | none | array of versions, each with its `sequence` and `kind` |
| `GET /api/files/{file_id}/frames` | none | array of frames |
| `POST /api/files/{file_id}/frames` | `name`, `parent_id`, `after_frame_id`, `x`, `y`, `width`, `height` | the created frame with its `order_key` |
| `PATCH /api/frames/{frame_id}` | any of `name`, `parent_id`, `x`, `y`, `width`, `height` | the updated frame |
| `DELETE /api/frames/{frame_id}` | none | the frame with `status` `deleted` |
| `GET /api/files/{file_id}/presence` | none | array of members present in the file, each with `primary_email`, `display_name` and `colour`; the read counts the caller as present |
| `GET /api/files/{file_id}/threads` | none | array of threads, each with its `frame_id`, `resolved`, `origin_branch_name` and its `comments` ordered oldest first |
| `POST /api/files/{file_id}/threads` | `frame_id`, `body` | the thread, whose `comments` holds its first comment |
| `POST /api/threads/{thread_id}/comments` | `body` | the created comment |
| `PATCH /api/comments/{comment_id}` | `body` | the updated comment |
| `DELETE /api/comments/{comment_id}` | none | the comment with `tombstoned` true |
| `POST /api/threads/{thread_id}/resolve` | none | the thread with `resolved` true |
| `GET /api/files/{file_id}/libraries` | none | array of libraries published from that file, each with its `id` and `name` |
| `GET /api/files/{file_id}/subscriptions` | none | array of subscriptions, each with its `library_id` and `pinned_version_id` |
| `GET /api/libraries/{library_id}/versions` | none | array of library versions |
| `POST /api/libraries/{library_id}/versions` | `changelog` | the published version |
| `POST /api/files/{file_id}/library-updates/{library_id}` | none | the subscription with its new `pinned_version_id` |
| `POST /api/files/{file_id}/branches` | `name` | the branch with its `id`, `branch_file_id` and `base_version_id` |
| `GET /api/branches/{branch_id}` | none | `id`, `state`, `branch_file_id`, `base_version_id`, `current_version_id`, `merged_version_id`, and `approval`: null, or the latest approval with its `target_version_id`, `decided_by`, `invalidated_at` and `invalidated_by_version_id` |
| `POST /api/branches/{branch_id}/review-requests` | `reviewer_email` | the review request |
| `POST /api/branches/{branch_id}/decisions` | `decision` (`approved`, `changes_requested`, or `withdrawn` from the branch creator), `comment` | the decision with its `target_version_id`, or for `withdrawn` the branch with `state` `withdrawn` |
| `POST /api/branches/{branch_id}/versions` | `frames`, an array of frames each with `name`, `x`, `y`, `width`, `height`, written onto the branch as its next version | the new version with its `id` and `sequence` |
| `POST /api/branches/{branch_id}/merge` | none | the branch with `state` `applied` and its `merged_version_id` |
| `GET /api/admin/members` | optional `role`, `seat`, `status` | array of memberships, each with `principal_id`, `primary_email`, `org_role`, `seat_type`, `status` and `last_active_at` |
| `PATCH /api/admin/members/{principal_id}` | `org_role`, `seat_type` | the updated membership |
| `POST /api/admin/members/bulk` | `principal_ids`, `org_role` | array of per-row outcomes |
| `POST /api/admin/members/invitations` | `email`, `org_role`, `seat_type` | the membership, existing or new |
| `GET /api/admin/identity` | none | `enforcement`, `break_glass_emails` |
| `PATCH /api/admin/identity` | `enforcement`, `break_glass_emails` | the updated settings |
| `GET /api/admin/audit` | optional `actor`, `action`, `from`, `to` | array of audit events, newest first, each with `id`, `occurred_at`, `actor_principal_id`, `action`, `resource_kind`, `resource_id`, `outcome` and `detail` |
| `POST /api/access-requests` | `email`, `note`, `company_website` | the recorded request |

**No mocks.** PostgreSQL, Keycloak and Mailpit are the facts. An in-memory list
of members standing in for rows, a hardcoded success body the app returns to
itself instead of exchanging a code with the identity provider, a review message
appended to a local array instead of sent over SMTP, or an audit list held in
process instead of in the store, are all contract violations however good the
interface looks. The named provider is the fact: the app's UI and its own tables
can only reflect what lives in the provider, never substitute for it.

## Definition of done

A member signs in, opens a shared file, moves a frame, and sees it in the same
place after a reload. They branch that file, ask a colleague to review it, and
the colleague approves. Changing the branch after that approval voids it, and
the merge is refused until the colleague approves the new version, at which
point the branch merges into the main file and the requester is told by mail. An
administrator can read every one of those transitions in a record nobody can
rewrite.
