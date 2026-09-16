# Calder Disclosure Platform

Build and deploy a working web application from this brief. There is no starting codebase. When you
are done, a stranger must be able to open the app in a browser and read a published press release at
its public address, with its lead image, without signing in and without hitting an error page. A
different stranger must NOT be able to reach a release whose embargo instant has not passed, by any
means: not through the archive, not through a direct request for its address, not through the search,
not through the release counter, and not by fetching its lead image. The image bytes must live as a
real object in the `minio` bucket at the key scheme this brief pins; a copy on the app container's
own filesystem does not count, and neither does a database column holding the bytes.

## Overview

Calder Disclosure Platform is the system a multi-entity commodity trading, shipping and investment
group uses to decide what it says in public and then to say it. It is two surfaces over one content
store: a five-division corporate site that anyone on the internet reads, and an editorial console
where communications, legal and compliance staff write every word that site carries.

The group is five public-facing divisions under one holding brand: `Calder Group`, the holding brand
and the shared narrative; `Calder Trading`, physical commodity trading in oil products and metals;
`Calder Capital`, a fund management arm; `Calder Maritime`, the owned and chartered fleet; and
`Kite Energy`, an energy investments venture that trades under its own mark. It runs three offices
in three regulatory regimes: Geneva, Dubai and Singapore.

The organisational graph is shallow and fixed, and its edges are the permission model: the group
holds five divisions, a division holds records, and each of the three offices belongs to one
jurisdiction. A membership is an edge rather than a column, carrying a role, a scope, who granted it
and when it lapses, because a column cannot carry any of those, and the failure that matters is the
former-employee problem: a person who has left whose publish right outlives their employment.

Nothing reaches the public site by being typed. A record is drafted by an author on one division,
submitted, cleared by a legal reviewer, classified and cleared by a compliance officer, and then
released or scheduled by a publisher. Five roles and five divisions mean authority is a pair rather
than a rank: a Trading press officer must not be able to publish under the Capital mark, and a
person who wrote a release must not be able to approve it, however senior they are. An approval is
recorded against the exact words that were approved, so editing those words takes the approval away
again. That is the point of the product, and it is also the part that makes it annoying, so there is
a deliberate and capped shortcut for changes that cannot carry meaning.

The public site is what the group is judged on, and it is a journey rather than a document. The home
route descends through seven chapters, four of them addressable, and most of its height carries no
copy at all, because the empty space is the distance travelled.

It deliberately is not a trading system. No price, position, cargo, vessel movement or counterparty
record enters this platform: the site quotes volumes in prose and the console holds prose about
volumes. It also has no confidential reporting channel, no federated sign-in, no email or
notification delivery, no outbound webhooks, no live three dimensional scene layer, no ambient audio
and one locale.

The genuinely hard part is that an embargoed release does not exist publicly. It is not hidden by a
filter that a query somewhere might forget: it is absent from what the public path can read at all,
its address answers exactly as an address that was never issued answers, its lead image is refused
at its own address, and the release counter does not count it. The same release, to a publisher on
its own division, renders with a banner naming the instant. When that instant passes it publishes
exactly once, even if the process that publishes it restarts across the moment.

## User roles

Signup is closed. Accounts exist only because they are seeded; there is no registration surface, no
invitation flow and no password reset. A principal signs in, and what they may do is decided by the
memberships they hold, each of which names one role on one division.

| Role | Can read | Can write |
|---|---|---|
| `author` | every record on a division they hold, in any state, and every published document | creates and edits drafts on that division, submits them for review, uploads media. **Cannot** approve any stage of any submission, **cannot** approve their own work by any route, **cannot** set a disclosure class, **cannot** publish, schedule or unpublish, **cannot** touch a record on a division they do not hold |
| `legal_reviewer` | every record on a division they hold, in any state | approves or requests changes on the legal stage of a submission on that division. **Cannot** approve the compliance stage of the same submission, **cannot** edit body copy, **cannot** set a disclosure class, **cannot** publish, **cannot** approve a submission they authored |
| `compliance_officer` | every record on a division they hold, in any state | approves or requests changes on the compliance stage, and sets the disclosure class on a record. **Cannot** edit body copy, **cannot** approve a stage another role owns, **cannot** approve a submission they authored, **cannot** approve a stage of a submission they already decided, **cannot** publish |
| `publisher` | every record on a division they hold, in any state | publishes, schedules, cancels a schedule, and unpublishes an approved record on that division. **Cannot** approve any stage, **cannot** edit body copy, **cannot** publish a record that is not `approved`, **cannot** publish a `market_sensitive` record without a scheduled instant |
| `group_admin` | every record's metadata across every division (title, type, state, instants, who acted), the whole audit trail, and the exception report | grants and revokes memberships, and nothing else. **Cannot** read the body of any record that is not published, **cannot** read an embargoed body, **cannot** approve, **cannot** publish, **cannot** edit any record, **cannot** grant a role on a division without recording who granted it |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from an `author` session to any `publisher`-only endpoint must
be rejected by the server (an unauthorized request is denied, not served), leaving the protected
state unchanged.

The same rule governs reads. There is one decision, asked once per request, and it answers deny
unless a rule allows: an unrecognised action denies, an unrecognised resource denies, and an error
while deciding denies rather than falling through. Three denials beat every allow and none of them
can be expressed as the absence of a permission: a principal is denied approval of a submission they
authored, on any stage, under any delegation; a principal is denied a second stage of a submission
they have already decided; and `group_admin` is denied the body of anything not published, which is
the rule products of this shape violate most often. Running the system is not the same permission as
reading what is inside it.

Every content read is scoped by division as well as by role. A request that does not name a division
is a request for the divisions the principal holds and no others, and a direct request for a record
on a division a principal does not hold is refused the way a record identifier that was never issued
is refused, so that a refusal never confirms the record exists.

Seeded accounts, every one of them using the password `deku-demo-pw-2026`:

| Email | Display name | Memberships |
|---|---|---|
| `author@example.com` | `Ines Marchetti` | `author` on `trading`, and `legal_reviewer` on `capital` |
| `author2@example.com` | `Tobias Renner` | `author` on `capital` |
| `legal_reviewer@example.com` | `Priya Raman` | `legal_reviewer` on `trading`, and `compliance_officer` on `trading` |
| `compliance_officer@example.com` | `Yusuf Adeyemi` | `compliance_officer` on `trading` and on `capital` |
| `publisher@example.com` | `Hana Lindqvist` | `publisher` on all five divisions |
| `group_admin@example.com` | `Elena Duarte` | `group_admin`, and no content membership at all |

Two of those rows are deliberate and the product is wrong if either works. `author@example.com`
holds a reviewer role on a second division, so they may clear somebody else's Capital work and must
still be refused their own Trading work. `legal_reviewer@example.com` holds both reviewer roles on
one division, so they may complete one stage of a Trading submission and must be refused the other,
because two stamps from one person is one stamp.

## Core features

### Auth

Email and password, implemented by the app. No external identity provider, no second factor, no
directory sync.

1. `POST /api/auth/login` takes `email` and `password` and returns a bearer token on success, in a
   field named `access_token`. A wrong password is rejected as a client error carrying no hint about
   whether the address exists.
2. Every endpoint except `POST /api/auth/login`, `GET /api/health` and the `GET /api/public/*` and
   `POST /api/public/enquiries` surfaces requires `Authorization: Bearer <token>`. A missing,
   expired or unparseable token is denied, not served.
3. Passwords are hashed at rest. The literal `deku-demo-pw-2026` must work at login for all six
   seeded accounts.
4. `POST /api/auth/logout` ends the session. The bearer token it was called with must be refused on
   the next request.
5. Signup is closed. No endpoint creates a principal from an unauthenticated request, and no
   endpoint resets a password.
6. After five failed password attempts for one address inside a rolling window, further attempts for
   that address are refused with a message stating that too many attempts have been made, and are
   accepted again once the window passes. The refusal is temporary and never a permanent lockout,
   because a permanent lock is a denial of service against the member rather than a defence of the
   account. It carries no hint about whether the address exists.
7. A principal who signs in holding no membership succeeds at signing in and lands on a surface
   stating they have no access and naming who grants it. They are never given a default role: a
   default role is a permission escalation with a friendly name.
8. Deactivating a principal stops their access at once rather than at their next sign in, because
   somebody who has left does not sign in again. Their existing bearer tokens are refused on the
   next request, their memberships stop granting anything, any pending approval assigned to them
   returns to the role group on that division, and any delegation they granted is revoked. Access
   loss on a deactivation is immediate and is never left to a cache to expire; an ordinary
   membership change, by contrast, takes effect within 60 seconds.
9. The consistency expectations are stated rather than left to be discovered as bug reports. A
   console write is readable by its own writer immediately. A publication is public within 30
   seconds and searchable within 30 seconds. A membership change reaches the decision within 60
   seconds. A deactivation reaches it immediately. An audit write is readable immediately.
10. Every instant in the product comes from one synchronised clock. Ordering within the trail uses a
    monotonic sequence rather than a wall-clock reading, because two events in the same millisecond
    are common and a clock adjustment moves backwards.

### Divisions, memberships and the decision

1. Five divisions exist and are seeded: `group` (`Calder Group`), `trading` (`Calder Trading`),
   `capital` (`Calder Capital`), `maritime` (`Calder Maritime`) and `kite-energy` (`Kite Energy`).
   Divisions are created and archived by nobody in this product; the set is fixed.
2. `Kite Energy` is the brand exception and the only one: it trades under its own mark rather than
   under the group mark plus a word. A division record carries its own wordmark and its own primary
   colour, defaulting to the group values, and the division bar renders the division's own label
   rather than composing it from the group name. Publish rights are scoped by division precisely so
   that another division's team cannot apply that mark. If a division's own mark is missing the page
   falls back to the group mark and the console raises a warning; a broken mark never renders.
3. A membership is not a column on a principal. It is a record carrying a principal, a division, a
   role, who granted it, an optional justification and an optional expiry. A principal holds any
   number of memberships, including two roles on one division, and every one of them is listed with
   its provenance at `GET /api/admin/members`.
4. A membership with an expiry stops granting anything the moment it passes, and it is retained
   rather than deleted, so that who could publish last quarter stays answerable.
5. `POST /api/admin/memberships` requires `group_admin` and records the granting principal. A
   membership granted to a single named principal rather than derived from a role group carries a
   mandatory justification and a maximum life of 90 days, and it appears in the exception report.
   The same call from any other session is denied and no membership is created.
6. `group_admin` cannot grant a role they do not themselves hold on a division where doing so would
   give them content access: a `group_admin` who needs to read content asks for a content membership
   from another `group_admin`, which is time bounded, justified, and shows up in the exception
   report.
7. One decision governs every read and every write. Asking whether one principal may read a page of
   50 records costs one decision over the set rather than 50 separate ones, and the answer does not
   change between the count the archive shows and the rows it returns: a paginator that says fifty
   and returns ten has already leaked that forty exist.
8. `GET /api/admin/exceptions` requires `group_admin` and returns everything deliberately outside the
   normal model: individual grants with their justification and expiry, active delegations with their
   parties and end instant, fast-path publications with their counts, and denied authorization
   attempts grouped by principal and action.

### Records, revisions and the two hashes

1. Every content record carries the same envelope whatever its type: an identifier that is never a
   guessable sequence, a type, a division, a slug, a state, the identifier of its current revision,
   the identifier of its published revision, an optional disclosure class, an optional embargo
   instant, a first-publication instant that is never rewritten, and who created and last updated it.
2. `current_revision_id` and `published_revision_id` are two different fields and the public path
   reads only the second. Collapsing them means every autosave is a publication.
3. Nine types exist: `page`, `release`, `product`, `vessel`, `investment`, `person`, `figures`,
   `policy` and `redirect`. The approval chain a type requires is a property of the type, held as
   data and readable, not a branch in code, and changing it does not affect submissions already in
   flight.
4. A revision is immutable. Editing creates a revision; it never rewrites one. A revision carries its
   parent, its author, its instant, the full field set, a hash over the whole canonical field set, and
   a second hash over only the fields in that type's approved set.
5. For a `release` the approved set is the title, the standfirst, the body, the disclosure class and
   the lead image. Everything else, including the image credit, the caption and the related links,
   sits outside it.
6. A body is a structured document, not a string of markup. The permitted block types are exactly
   `paragraph`, `subheading_2`, `subheading_3`, `list_unordered`, `list_ordered`, `quote`, `image`
   and `table`. Anything else is rejected when it is written, not stripped when it is rendered,
   because stripping at render leaves the bad content in the store for the next renderer that
   forgets. No arbitrary markup, no scripts, and no embed from a third-party origin at all: a
   corporate release page that can embed a third-party frame is a stored injection with a review
   process attached to it, and the review does not help, because a reviewer approves the embed and
   the third party changes what it serves afterwards.
7. Every block carries an identifier that is stable across revisions, so a comparison of two
   revisions says a block moved rather than saying one was deleted and another created.
8. `POST /api/content/records` requires `author` on the named division and creates a record in
   `draft`. `PATCH /api/content/records/{id}` edits it and produces a revision. Both are denied for
   any other role, and denied for an `author` on a division they do not hold, and the stored record
   is unchanged.
9. Two edits to the same record carrying the same revision identifier do not both succeed. Exactly
   one is accepted, the record's current revision advances, and the other is rejected as a conflict
   carrying the current value so the editor can see both. This holds under real concurrency.
10. Referential integrity is enforced rather than hoped for. A division holding records cannot be
    archived until they are. A media record in use cannot be deleted, and the console shows every
    record referencing it so the refusal is actionable rather than a dead end. A redirect survives
    the deletion of the record that minted it, with its origin reference emptied. The revisions of a
    record that reached publication are never deleted, because the approval trail points at them.
    Where a reference is found broken it is reported, and a broken reference is never repaired
    automatically, because an automatic repair of a reference is how content quietly changes.
11. Sanitisation happens when a value is written, never when it is rendered, because stripping at
    render leaves the bad value in the store for the next renderer that forgets. A structured body is
    checked against the permitted block list. A plain text field is length bounded, has control
    characters removed and has its edges trimmed. An uploaded file has its type verified by
    inspecting the bytes. A slug is generated rather than accepted, lowercase, from a restricted
    character set. An address or a telephone number is stored both raw and normalised, and the raw
    form is never used to build a request.

### The review chain

1. Ten states exist: `draft`, `in_review`, `legal_review`, `compliance_review`, `changes_requested`,
   `approved`, `embargoed`, `published`, `unpublished` and `archived`. There is no reset: nothing
   returns to `draft` except through the transitions below.
2. `POST /api/workflow/records/{id}/submit` moves a record from `draft` to `in_review`. The actor
   must hold `author` on the division, every required field must be complete, and a record of a type
   that requires a disclosure class must already have one. It opens a submission carrying the record,
   the revision, the chain version in force at that moment, and the submitting principal. At most one
   submission is open per record at a time, and a second concurrent submit is rejected rather than
   creating a second.
3. `in_review` becomes `legal_review` on assignment of a legal reviewer. An author may withdraw their
   own submission from `in_review` back to `draft`; nobody else may.
4. `legal_review` becomes `compliance_review` when a principal holding `legal_reviewer` on the
   division approves the legal stage. `legal_review` becomes `changes_requested` when they request
   changes, and a comment is mandatory on that transition.
5. `compliance_review` becomes `approved` when a principal holding `compliance_officer` on the
   division approves the compliance stage. That transition additionally requires that the actor is
   not the submission's author and **did not perform the legal approval on this submission**. A
   system that lets a dual-hatted officer satisfy both stages has a two stage chain on paper and a
   one stage chain in fact.
6. `changes_requested` returns to `draft` automatically on the next edit, and both stage decisions
   are cleared. Legal and compliance are sequential by default, because compliance reviews the
   legally-cleared text. A type may declare the two stages parallel instead, and when it does both
   must complete before `approved`, either may request changes, and a request for changes returns
   the record to `draft` and voids both.
7. An author may never approve their own submission, on any stage, under any role they hold and
   under any delegation. `author@example.com` submitting a Capital release as its author is refused
   the legal stage on it, although they hold `legal_reviewer` on `capital`, and the refusal is
   recorded with its reason.
8. An approval is recorded against the approved-set hash of the revision it approved. On any
   subsequent edit: if any field in the approved set changed, every approval on the record is void
   and the record returns to `draft`; if only fields outside the approved set changed, the approvals
   stand and the change is recorded. Without the second half, correcting an image credit would
   restart a three day approval chain and people would work around the system rather than in it.
9. `POST /api/workflow/delegations` lets an approver delegate their approval authority. A delegation
   names one role on one division, carries a mandatory end instant no more than 30 days out, may not
   be delegated onward, records both the delegate and the delegator on every decision it produces,
   and is revocable immediately by the delegator or by `group_admin`. A delegate who is the author of
   a submission is still barred from approving it: delegation must not become a route around the
   self-approval bar.
10. The fast path: a change confined to fields outside the approved set, made by a principal holding
    `author` on the division, on a record already in `published`, may be published directly by one
    `publisher` action with no review stage. It is recorded identically. It is capped: three
    fast-path publications on one record within seven days force the next change through the full
    chain, whatever it touches.
11. A published release may be corrected. A correction travels the chain again, and on publication
    the page carries a visible correction notice with its instant. Whether a correction is material
    is set by a `compliance_officer`, never by the author.
12. Transitions are serialised per record. Two simultaneous approvals produce one success and one
    rejection carrying the current state, never two recorded approvals and never a lost one. Every
    transition endpoint takes the state the caller believes the record is in and rejects as a
    conflict if the record has moved.
13. `GET /api/workflow/inbox` returns four queues in this order: submissions awaiting this
    principal's decision, records this principal authored that were sent back, this principal's own
    drafts, and records this principal follows. An empty first queue carries an authored line saying
    there is nothing awaiting a decision, because an empty approval queue is good news and should say
    so.
14. Notifications are shown in the console and nowhere else. A notification carries a title, a
    division, a record type and a link, and never the record body; for a `market_sensitive` record it
    does not carry the record title either, because an unpublished market-sensitive headline sitting
    where it can be read has already leaked. Ten changes to one record inside an hour produce one
    notification, not ten. Non-urgent notifications batch into a digest at a per-principal frequency,
    defaulting to daily, while an approval request, an escalation and anything security-relevant never
    batch. A submission awaiting a decision for 48 hours escalates to the division's other approvers,
    and at 96 hours to `group_admin`. A principal sets their own preferences per event class, with one
    floor: nobody can switch off being told that their own permissions changed.

### Disclosure classification and the policy register

1. Four classes exist: `general`, corporate news with no market or regulatory sensitivity;
   `regulated`, relating to a licensed activity, which appends the regulated disclaimer;
   `market_sensitive`, which could affect the price of a traded instrument; and `restricted`, an
   internal record that never enters the published projection under any state.
2. `POST /api/content/records/{id}/classify` requires `compliance_officer` on the division. The same
   call from an `author`, a `legal_reviewer` or a `publisher` session is denied and the stored class
   is unchanged. An author can never change a class, in any state.
3. A `release`, `investment`, `policy` or `document` record cannot leave `compliance_review` without
   a class.
4. A `market_sensitive` record cannot go from `approved` straight to `published`. It must be
   scheduled, and a publish attempt on it without a scheduled instant is rejected. A company that
   buys and ships oil putting out an unscheduled announcement is how prices move by accident.
5. The policy register is the single place every controlled text lives: the code of conduct, the
   privacy notices, the terms of use, the sustainability policies and the standard disclaimers. A
   register entry carries a reference code, a title, an integer version, an effective-from instant,
   an optional effective-until instant, the accountable role, a review interval in days, the
   divisions it scopes to, the jurisdictions it applies under, whether it is published internally or
   externally or both, a body, and the identifier of the version it supersedes. A reference code and
   a version together are unique.
6. Versions are immutable. Changing an entry creates a version; it never edits one.
7. The disclaimer appended to a regulated page is a register entry referenced by code, resolved at
   publication against the version then in force, and frozen into the published document with that
   version recorded. Updating the disclaimer changes what newly published pages say; it never
   retroactively changes what a page said on the day it was published. That distinction is the whole
   reason the register exists rather than a shared template fragment.
8. An entry whose effective-from instant is in the future is not rendered publicly and is visible in
   the console with its date. A superseded entry shows the current version, and the superseded
   versions are reachable from it with the period each was in force, because a counterparty doing due
   diligence sometimes needs the version that applied on a particular date two years ago.
9. An entry overdue for review is flagged in the console and in the exception report and is still
   rendered publicly, because an overdue policy is still the policy.

### Embargo and scheduled publication

1. `POST /api/workflow/records/{id}/schedule` requires `publisher` on the division, requires the
   record to be `approved`, and takes an instant. It moves the record to `embargoed`.
2. An instant in the past is rejected at the transition, not silently published.
3. An embargoed record does not exist publicly. It is absent from `GET /api/public/releases`, its
   address under `GET /api/public/releases/{slug}` answers exactly as a slug that was never issued
   answers, it is absent from `GET /api/public/search`, its lead image is refused at
   `GET /api/public/media/{mediaId}`, and `GET /api/public/counters` does not count it. A build that
   filters it out of the list and still serves it at its own address has not built this.
4. The same record, requested by a principal holding `publisher` on its division through the console
   surface, renders in full with a persistent banner naming the release instant.
5. The instant is stored in absolute time and shown both as the instant and in the reading
   principal's own local time, because a release timed for market open in Singapore has been set by
   somebody in Geneva.
6. When the instant passes, the record publishes. It publishes exactly once. The publication is a
   conditional move from `embargoed`, so a second attempt finds the record already published and does
   nothing: a scheduler that fires twice, or that restarts across the instant, still produces one
   publication, one projection write and one advance of the counter.
7. A record published more than 60 seconds after its instant records the delay, because a
   market-sensitive announcement going out late is nearly as bad as one going out early.
8. `DELETE /api/workflow/records/{id}/schedule` returns an embargoed record to `approved` and
   requires `publisher`. It is denied for every other role.
9. A publication carrying an idempotency key is executed once. A repeat with the same key and the
   same body returns the original response; a repeat with the same key and a different body is
   rejected as a conflict. Keys are honoured for 24 hours. This matters most on publish, which is
   the call where a double execution announces something twice.

### Media in the object store

1. Media bytes live in the `minio` bucket and nowhere else. `POST /api/content/records/{id}/media`
   takes the bytes plus a filename and `alt_text`, writes the object, and returns the record.
2. The object key scheme is `media/{division_key}/{record_id}/{sha256_of_bytes}.{ext}`, for example
   `media/trading/rel-0004/3f9a2c81d5e0b7461fa2c9d3e8b05147a6c2f9d0e1b3a4578c6d9e0f1a2b3c4d.png`.
   The checksum in the key is what makes the object immutable and permanently cacheable.
3. `alt_text` is required and may not be empty. A media record without alternative text cannot be
   created, which is the only reliable way to get alternative text written.
4. Every media record also carries a focal point, so that the crop at every width keeps the subject
   in frame, plus an optional caption and an optional credit.
5. Embedded metadata is stripped on receipt: no camera model, no location, no author, no revision
   history. The content type is verified by inspecting the bytes, never by trusting the declared type
   or the file extension, and anything not on the permitted list is refused.
6. `GET /api/media/{mediaId}` returns the bytes to a principal who may read the record the media
   belongs to, and denies everybody else. `GET /api/public/media/{mediaId}` returns the bytes only
   when the media belongs to a record that is currently published, and otherwise refuses exactly as
   an identifier that was never issued is refused. An anonymous request for the lead image of a draft
   or embargoed release is refused at that address, not merely absent from the page.
7. Where a record that needs an image has none, the page renders a generated placeholder derived from
   the record's own identifier, so the same record always gets the same placeholder. A placeholder
   keyed on anything that changes between renders makes an archive look broken; keyed on the record
   it looks intentional.

### The public site

1. Ten public routes carry content, plus a search route: `/`, `/trading/`, `/capital/`,
   `/maritime/`, `/kite-energy/`, `/who-we-are/`, `/news/`, `/news/{slug}/`, `/sustainability/`,
   `/contact/`, `/privacy-policy/`, `/terms-of-use/` and `/search`.
2. A public document is produced once, when it is published, and then served. Nothing on a public
   route is assembled while a visitor waits, and the public serving path can read only finished
   documents: it holds no way to reach a draft, a revision, an embargoed body or the audit trail.
   That is the property that makes a bug in the public path unable to leak a draft, because the draft
   is not reachable from where the bug is.
3. Publishing a record that other documents depend on refreshes those documents. Invalidation is by
   declared dependency rather than by naming addresses. Every rendered
   document declares what it depends on: its own record, every record it references, the policy
   versions it carries, the office set and its division. Publishing an office change refreshes every
   document carrying the footer, which is all of them, and that is correct, because the footer
   changed. Refreshing by naming individual addresses is how a departed director lingers on three
   pages nobody remembered.
4. The release counter in the header is the count of published releases across all divisions,
   unfiltered. It is not the count of the current filter and not the count of the current page. It is
   fetched at runtime from `GET /api/public/counters` rather than baked into every document, because
   baking it in means publishing one release refreshes the whole site, and every document ships with
   the last known value as its initial content so the header is never empty and never shifts the
   layout when the value arrives. With 9 seeded published releases it reads `9`.
5. `/news/` is the release archive. Its pagination and its filtering are both address-driven: `?page=2` is a real address rendered by
   the server, and so are `?division=trading` and `?year=2023`, alone or together, both defaulting to
   unfiltered. A page carries 6 cards, and the last page carries whatever remains; with the 9 seeded
   published releases that is 6 on the first page and 3 on the second. Infinite scroll is not permitted here, because a
   journalist needs to be able to link to and cite a page of the archive.
6. A card carries an image, a date and a title. A title longer than the card allows is truncated when
   the document is produced, with a trailing ellipsis inside the text, and the full title is what
   assistive technology announces, because the point of the shortening is to keep the grid tidy, not
   to hide information.
7. A release slug is immutable once the release has been published. Retitling a published release
   mints a redirect record rather than moving the document, and the old address keeps resolving,
   because a release is cited by counterparties and regulators and a broken citation is a compliance
   question rather than a broken link. A redirect chain is collapsed when it is written: minting a
   redirect whose target is itself a redirect rewrites the new one to point at the final target, and
   a chain longer than one hop is rejected.
8. `POST /api/workflow/records/{id}/unpublish` requires `publisher` and a mandatory reason. The
   release's address then answers gone and renders the withdrawal notice carrying the date of
   withdrawal. It does not answer not found and it does not vanish: most systems delete, this one
   withdraws and says so, because a citation that leads to a blank page raises more questions than
   one that leads to an honest notice. An archived release answers the same way and is additionally
   excluded from the archive and from the search.
9. `/trading/` carries two product families, `Oil` and `Metals`, and twelve products across them,
   each a record with a name, a body, a family and an order. Adding a thirteenth is an editorial act.
   A family with no published products is removed from the selector entirely, and if only one family
   remains the selector is not rendered.
10. Every division route except the group home carries a strip of the three most recent releases
    tagged to that division, ordered by publication instant descending, and renders nothing at all if
    there are none. It never falls back to group-wide releases, because a Capital page showing a
    Maritime release implies a relationship that does not exist.
11. `/capital/` is the most legally exposed route on the site. Records on `capital` carry a mandatory
    disclosure class and cannot reach `approved` without one, and the class drives the disclaimer
    block appended to the rendered page from the register.
12. `/maritime/` lists the fleet from vessel records, each carrying a name, a class, a deadweight, a
    year built, a flag, whether it is owned or chartered, and a status of active or disposed. A vessel
    record carries no position, no voyage, no cargo, no charterer and no commercial term of any kind,
    and no route exists by which it could: a fleet page that grows a live position feed has quietly
    become a commercial system with a public front door.
13. `/who-we-are/` carries the group narrative and the leadership block. A person record has a
    publication state of its own, independent of the page, so a director who leaves is unpublished
    from the page without the page being edited, and the change takes effect through the refresh path
    rather than through a rebuild, because a departure is sometimes urgent. A person record carries a
    display-from and a display-until instant, so a departure can be scheduled. If no person record is
    published the leadership block is omitted entirely rather than rendered empty.
14. `/sustainability/` carries the full strategy, the three pillars written out rather than hidden
    behind tabs, the externally published subset of the policy register with each entry's version and
    effective date, and downloadable disclosure documents. Each download is counted, per document per
    day, and no visitor identifier is retained.
15. `/privacy-policy/` and `/terms-of-use/` are register entries rendered as routes, never
    hand-written templates, because a version on the site and a version in the register drift the
    moment somebody edits one. Each carries its title, its version, its effective date and the date
    it was last reviewed, its body, an in-page contents list built from its subheadings, a one
    paragraph summary of what changed since the previous version, and a list of previous versions
    each linkable and each showing the period it was in force.
16. The privacy notice has three variants, one per jurisdiction: `CH`, `AE-DIFC` and `SG`. The
    visitor is served the variant for the jurisdiction their request resolves to, and all three are
    reachable from a selector on the page, because inferring a jurisdiction is not the same as asking
    and a visitor whose location resolves wrongly must not be trapped. The three variants share a
    parent, so a change to the common body propagates and only the jurisdiction-specific sections are
    edited separately.
17. `GET /api/public/search` searches published documents only: published releases, pages, products,
    people and externally published policy entries. It is address-driven at `/search?q=`, rendered by
    the server, and its results are linkable. It is not a live overlay. A query shorter than 2
    characters returns the no-query state rather than an error. The console's own search over records
    in every state shares no index with it, because a public index that could reach a draft is a leak.
18. A withdrawn or unpublished release leaves the public search within 30 seconds of being withdrawn,
    because slow removal from an index is how taken-down material stays findable for a week.
19. Seven authored surfaces exist and none of them is a bare server document: not found, gone,
    forbidden, server error, maintenance, rate limited, and a not-found for an unknown console route.
    Their copy is fixed. Not found reads
    `We cannot find that page. It may have moved, or the address may be mistyped.` Gone reads
    `This release was withdrawn on <date>. It is no longer published.` The server error reads
    `Something went wrong at our end. Please try again. If you need to tell us about this, quote reference <request_id>.`
    Maintenance reads `We are carrying out planned maintenance and expect to be back by <time>.` and
    carries a retry-after value matching the time it names. Rate limited reads
    `Too many requests. Please wait <duration> and try again.` and carries a matching retry-after
    value.
    Each carries the mark, the chrome and a way back. The server error surface displays the request
    identifier as selectable text, because the whole point of it is to be quoted, and it must not be
    an image and must not be a truncated hash. The not-found surface offers the five divisions and
    the release archive. No error surface loads any visual layer, because a page that spends eight
    seconds drawing a mountain before telling you the thing you wanted is missing is worse than a
    bare server document.
20. One rule governs emptiness everywhere: a block with no content is removed, not rendered empty.
    There are exactly three exceptions, where the absence is itself the answer to a question the user
    asked and an authored line is the correct response: the release archive, the console inbox and
    the search results. A home-page chapter with no content record is not rendered at all and the
    chapter numerals renumber, so there is never an empty numbered gap in the middle of the descent.

### The enquiry form and the visitor's own surfaces

1. `POST /api/public/enquiries` takes an enquiry from an anonymous visitor at `/contact/`. Its fields
   are: `subject_area` (one of the five divisions or `general`, and it must be a known value), `name`
   (required, 2 to 120 characters after trimming), `organisation` (optional, up to 200 characters),
   `country` (required, and it decides the jurisdiction), `email` (required, checked for syntax),
   `phone` (optional, permissive, stored both as entered and normalised), `message` (required, 20 to
   4000 characters), and `consent` (required, an explicit choice that is not pre-selected, recorded
   with the version of the privacy notice in force).
2. The validation rules are declared once on the server and executed in two places: the same rules run
   in the browser for immediate feedback, and the server runs them again on submission and never
   trusts the browser's result. A payload that satisfies the browser and violates the server is
   rejected by the server, and nothing is written.
3. Field messages are authored strings held with the content, not generated from the rules.
4. Validation behaviour: a field blurred with a value is checked; a required field blurred empty is
   not flagged yet, because somebody tabbing through has not made a mistake; a submit attempt checks
   everything, moves focus to the first invalid field and announces how many errors there are, once,
   not once per field; after a failed submit a corrected field revalidates as it is typed so the error
   clears the moment it is fixed; and a submit while one is pending is ignored while the control shows
   its pending state.
5. Four anti-abuse layers, in order, and none of them is a visual puzzle: a submission token minted
   per form render, single use, expiring in 30 minutes; a minimum of 3 seconds between the form being
   rendered and being submitted; a limit of 5 submissions per hour from one origin; and only after
   that, a challenge. A visual puzzle is never presented, because the people writing to a group like
   this are frequently not writing in their first language.
6. The country decides the jurisdiction and the jurisdiction decides which office answers:
   Switzerland and the European area resolve to `CH` and Geneva; Gulf states resolve to `AE-DIFC` and
   Dubai; Asia and the Pacific resolve to `SG` and Singapore; anything else resolves to `CH`, as the
   most protective default. The country comes from the visitor, never inferred from the connection,
   because a guess is not a lawful basis for choosing a regime; an inferred country may only
   pre-select the field.
7. The write and the delivery are two different promises and only the one that can be kept is made.
   The submission validates, mints an enquiry record, writes it, and answers. The routing to the
   destination office happens afterwards and its failure never surfaces to the visitor, whose enquiry
   is already recorded. Telling a visitor their enquiry was delivered before it has been is the lie
   this ordering prevents.
8. The confirmation replaces the form in place, without navigating away, and carries a confirmation
   line, the enquiry's public reference, the expected response window and the office that will
   respond. It receives focus and is announced.
9. Every error state preserves what was typed. A rejected validation keeps the values and moves focus
   to the first error; an expired token re-renders the form with a fresh token and every value intact;
   a rate limit states the retry window and keeps the values; a server error states a reference
   identifier, offers the destination office's own address as a fallback route, and offers the typed
   values as a copyable block. A form that loses a four thousand character message will not get a
   second submission.
10. A first-time visitor is asked once whether they accept anything beyond what the site strictly
    needs. Refusing everything is one action, exactly as prominent and exactly as easy as accepting
    everything. The answer is stored first-party, survives a reload and a later visit, is changeable
    from the privacy route, which also shows what was chosen and when and which version of the notice
    was in force at that moment, and takes effect immediately including removing anything already
    stored. Nothing beyond the strictly necessary is stored before an affirmative choice, and a
    browser that already declares a preference not to be tracked is treated as a refusal and not
    prompted. Three exclusion zones carry no measurement of any kind and offer no choice, because
    there is nothing there to choose about: every error surface, the enquiry form while it is being
    filled in, and any surface where somebody is composing a message. Something watching keystrokes
    on a page where a person is typing a complaint is not measurement, it is eavesdropping.
11. What the communications team actually asks is measured on the server from the request path alone:
    document views, download counts and search terms, aggregated to a daily count with no visitor
    identifier retained and no linkage between requests. That measurement survives a visitor refusing
    everything, which is the point of it.

### The audit trail

1. Every mutation, every authorization decision that denied, every sign-in and every read of a
   restricted record is recorded. Reads are recorded only for restricted records, which here means an
   embargoed body and the trail itself; recording every read of every page produces a volume nobody
   queries.
2. An entry carries its instant, the acting principal and, when the action was delegated, the
   principal it was performed on behalf of; the action, from a closed vocabulary and never a free
   string; the resource type, the resource identifier and the division; the hash before and the hash
   after, never the content itself; whether the decision was allow or deny and why it denied; the
   request identifier; and the hash of the previous entry together with its own hash.
3. Storing hashes rather than content is deliberate: the trail must be broadly readable to be useful,
   and the content must not be.
4. The trail is append-only. No endpoint updates an entry and no endpoint deletes one, at any
   privilege level, and `GET /api/admin/audit` is the only way to read it. An entry, once written, is
   never changed.
5. Each entry's stored previous-entry hash equals the preceding entry's own hash, so removing or
   altering one entry breaks the chain visibly.
6. `GET /api/admin/audit` is queryable by actor, resource, action, division, decision and time range.
   Its empty state is an authored line stating no entries match, restating the query, because an
   auditor who sees a blank table needs to know whether the query was wrong or the answer was
   genuinely nothing.
7. Each of these is one query with one answer: who approved this release and when; under whose
   authority, if it was delegated; what exactly they approved, through the after-hash; whether it was
   edited after approval; who granted this person publish rights; and what the decision said when a
   request was denied.

### Edge cases

1. An author edits an approved release before publication: every approval is void, the state returns
   to `draft`, and the approvers are told.
2. An author edits only the image credit on an approved release: the approvals stand and the change
   is recorded.
3. An approver holds both reviewer roles on one division: they complete one stage and are refused the
   other on the same submission.
4. An approver delegates to the release's author: the author is still barred.
5. Two publishers publish the same release at the same moment: one succeeds, one is rejected with a
   conflict, and exactly one publication exists.
6. An embargo instant is set in the past: rejected at the transition.
7. The process that publishes embargoed records restarts across an instant: the release publishes
   once, not twice and not never.
8. A market-sensitive release is submitted with no embargo: it cannot leave `compliance_review`, and
   a publish attempt on it is rejected.
9. The approval chain for a type is changed while a submission is in flight: that submission completes
   under the chain version recorded on it.
10. A slug is changed after publication: a redirect is minted and the original address keeps working.
11. A redirect's target is later redirected: the chain is collapsed when the second is written.
12. A release is published and then found to be wrong: it is unpublished with a reason, its address
    answers gone with the withdrawal date, and the record remains.
13. A record references media that has not been checked for malware: the record cannot be published.
    Unchecked means unpublished, with no exception. If the check cannot be performed, the upload is
    still accepted and held, and the record that references it is still blocked from publishing.
14. A principal is deactivated while holding a pending approval: their tokens stop working at once and
    the approval returns to the role group.
15. A principal is deactivated mid-edit: the save is refused as unauthenticated and the draft is
    preserved for a successor rather than lost.
16. The release archive is filtered to nothing: the filtered empty state renders, the filter chips
    stay visible so the visitor can see what excluded everything, and a control clears them.
17. A release has no lead image: the deterministic placeholder renders, and it is the same placeholder
    every time for that release.
18. `GET /api/public/counters` is unavailable: the last known value ships in the document and stays
    there rather than the header emptying or the layout shifting.
19. A visitor refuses every non-essential choice: every route is fully functional and only the
    measurement is lost.
20. The object store does not answer on a media call: that call is rejected as a dependency failure,
    every other surface keeps working, and authorization is never relaxed because a dependency
    failed. That degradation is stated rather than hoped for, and it is the only one in the product:
    the database is the app's own floor and there is no surface without it.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the group home, a journey of seven chapters with four addressable anchors | anonymous |
| `/trading/` | the trading division, two product families and twelve products | anonymous |
| `/capital/` | the capital division, with its disclaimer from the register | anonymous |
| `/maritime/` | the fleet | anonymous |
| `/kite-energy/` | the energy venture, under its own mark | anonymous |
| `/who-we-are/` | the group narrative, the leadership block and the group figures | anonymous |
| `/news/` | the release archive, paginated and filtered by address | anonymous |
| `/news/{slug}/` | one release | anonymous |
| `/sustainability/` | strategy, pillars, the external policy list, reports | anonymous |
| `/contact/` | offices, the media contact and the enquiry form | anonymous |
| `/privacy-policy/` | the register entry, with a jurisdiction selector | anonymous |
| `/terms-of-use/` | the register entry | anonymous |
| `/search` | the public search over published documents | anonymous |
| `/console/login` | sign in | anonymous |
| `/console` | the inbox, four queues | any membership |
| `/console/divisions/{key}/releases` | the division's records as a table | a membership on that division |
| `/console/releases/new` | the create route | `author` on a division |
| `/console/releases/{id}` | the record: editor, review rail, preview | a membership on that division |
| `/console/releases/{id}/history` | the revision and decision timeline | a membership on that division |
| `/console/policies` | the policy register | any membership |
| `/console/media` | the asset library | any membership |
| `/console/admin/members` | memberships, their provenance and their expiry | `group_admin` |
| `/console/admin/audit` | the audit trail, queryable | `group_admin` |
| `/console/admin/exceptions` | the exception report | `group_admin` |
| any other address | the product's own not-found page | anonymous |

**Entry and redirects.** An anonymous request for any `/console` route lands on `/console/login` and,
after a successful sign in, continues to the address that was asked for. A sign in with no pending
address lands on `/console`. Signing out returns to `/console/login` and the previous token stops
working. A token that has expired mid-action returns to `/console/login` and, once signed in again,
resumes at the address the principal was on. A principal holding no membership signs in and lands on
a surface stating they have no access and naming who grants it. A principal who opens a console route
for a division they hold no membership on is refused by the server, and no record table is rendered
to them. A principal without `group_admin` who opens any `/console/admin` route is refused by the
server and shown a message naming the role the route needs. An anonymous request for `/news/{slug}/`
whose release is embargoed, in draft, or never existed answers not found; one whose release was
withdrawn answers gone and renders the withdrawal notice.

**Journeys.**

1. Sign in at `/console/login` as `author@example.com` with `deku-demo-pw-2026`. The rail lists
   `Calder Trading` and `Calder Capital`, and nothing else. Open `/console/releases/new`, write a
   Trading release, upload a lead image with alternative text, and submit. The review rail moves to
   `legal_review` and the record leaves the drafts queue.
2. Sign in as `legal_reviewer@example.com`. The release is in the first inbox queue. Approve the legal
   stage; the rail moves to `compliance_review`. Then attempt the compliance stage on the same
   submission: it is refused, although this account holds `compliance_officer` on `trading`, and the
   refusal names the reason.
3. Sign in as `compliance_officer@example.com`, set the class to `market_sensitive`, and approve the
   compliance stage. The record is `approved`.
4. Sign in as `publisher@example.com` and attempt to publish it directly: it is rejected, because a
   market-sensitive record must be scheduled. Schedule it for an instant a few seconds ahead. Before
   that instant, open `/news/{slug}/` signed out: not found. Request its lead image at
   `GET /api/public/media/{mediaId}` signed out: refused. After the instant, the same address renders
   the release, the header counter has advanced by one, and the archive lists it first.
5. Sign in as `author@example.com` and edit the body of an approved Trading release: the record
   returns to `draft` and both approvals are gone. Edit only the image credit on another approved
   release: the approvals stand.
6. Sign in as `author@example.com`, open the Capital release they authored, and attempt the legal
   stage on it. It is refused, although this account holds `legal_reviewer` on `capital`.
7. Sign in as `author2@example.com`, who holds `capital` only, and request a Trading draft at its own
   address. The refusal is the one an identifier that was never issued gets.
8. Sign in as `group_admin@example.com`. `/console/admin/members` lists every membership with who
   granted it and when it expires; `/console/admin/audit` carries every action from the journeys
   above, newest first. Request the body of an unpublished release: refused, and the refusal is in the
   trail.
9. Signed out, open `/news/`. Six cards, newest first. Go to `/news/?page=2` by address: the remaining
   three. Filter to `/news/?division=trading`. Open a release, then its division from the eyebrow.
10. Signed out, open `/contact/`, answer the consent question, fill the enquiry form with a country in
    Asia, and submit. The confirmation replaces the form in place with a reference and the Singapore
    office named as the responder. Reload: the consent answer has survived.
11. Sign in as `publisher@example.com`, retitle a published release, and request the old address: it
    still resolves. Unpublish another with a reason, and request its address: gone, with the
    withdrawal date, and it is no longer in the archive or the search.

**States.** Every list has an empty state that names what is missing rather than apologising for
being empty: a filtered archive names the filters that emptied it, keeps the filter chips visible and
offers a control to clear them; an empty inbox queue says there is nothing awaiting a decision. Every
surface has a loading state: the archive renders six card skeletons at the real card dimensions
carrying the placeholder sheen, and a console table renders its header and its column set before the
rows arrive. An error renders as a banner above content that already loaded, which stays readable;
the app never shows a blank screen and never shows a stack trace.

## UI/UX notes

Somebody arriving at the public site should understand within one screen that this is a large,
serious, multi-business group whose word carries weight, and should feel they have begun a journey
rather than opened a page. Somebody arriving at the console should understand within one screen what
is waiting on them and what state it is in. Those are two different first moments and the product
needs both, which is why the two surfaces share a resolved token set and share nothing else.

The public site is corporate-editorial with a point of view: atmosphere is permitted, the subject is
seen before the chrome, and the composition is allowed to be slow. The console is operational: quiet,
dense but organised, built for scanning and repeated action, with no journey, no split text and no
drifting scroll, because it is used for six hours a day and every one of those is hostile at that
length. Space over dividers on the public site. Density over atmosphere in the console. The exact
values below are yours wherever a relationship or an exclusivity rule is stated instead, so long as
every stated relationship and every stated exclusivity holds.

**Mode.** The product commits to a light mode and designs it fully. A dark mode is optional; if one
is built it holds every relationship and every exclusivity stated below, and the light mode stays the
one the product opens in.

**The palette thesis.** One brand blue, a long pale ramp beneath it, and almost nothing else. The
richness of a finished page comes from the imagery behind the type, never from the palette. Read that
as a constraint rather than a summary: a sixth accent added later will look wrong, because there is
no fifth for it to sit next to.

**Palette by role.** The brand colour is a mid, soft cyan. It is the mark, all body copy on light
ground, and every rule and hairline in the product, and it appears in all three of those places and
nowhere else as a fill. The light ground is a near-white neutral, and it is also the colour of all
copy on dark ground; the two swap roles and never blend. Secondary copy on light ground is a light,
muted cyan one step off the brand, and it is the same colour a brand-blue link becomes when it is
pointed at. A second light, muted cyan one step brighter than that is a ground-adjacent tint and a
marker halo, and it never touches type. Dividers on light ground are a near-white cool neutral, and
the palest cool neutral in the product is restricted to rules and dividers and may never carry text
at any size. There is exactly one bright colour, a mid, vivid cyan: it is the border of the one
tertiary control style and appears nowhere else at all. A near-black neutral exists only as the
ground behind a chapter and is never used for type.

Alphas travel with the colour rather than as a separate transparency on a parent, because a
transparency on a parent fades its children too. Six strengths of the light ground carry overlay
fills, secondary copy on dark ground, a disabled control on dark ground, rules inside the overlay
menu, placeholder copy, and the terminal stop of the card sheen, each weaker than the one above it.
Three strengths of the brand carry the focus ring fill, the card hover wash and the pressed state,
strongest first. One strength of the palest cool neutral draws hairlines on dark ground and one of
the bright blue draws the tertiary control's resting border. The exact strengths are yours; their
order is not.

**Type.** Two families and no third. Body and most headings are set in `CalderSans`, a licensed
geometric sans with near-circular bowls, a single-storey `a` and generous letter spacing at display
size, in weights 400 and 700, roman and italic. The largest display size is set in `Josefin Sans`,
an openly licensed humanist geometric with a high waist, in its light weights. Every face loads with
a swap policy so copy is readable before the faces arrive, and the fallback stack is
`"CalderSans", "Century Schoolbook L", "Futura", "Avenir Next", sans-serif`, chosen close enough in
metrics that the swap never reflows a headline by more than one line. Ship only the weights and
styles actually used, subset to the characters the published content needs, and preload the two faces
used above the fold.

The sizes are given exactly in `## Front-end specification`, because a type scale the builder invents
is the fastest way to lose the design's character. The single thing to understand about them is that
the display setting does its work through tracking rather than size: between the two layout states
the largest heading roughly doubles while its letter spacing more than triples, and getting that
relationship wrong produces a headline that reads as a different company. Figures line up in a column
wherever amounts stack.

**The grid and the rhythm.** Four columns on a narrow screen and twenty four above the primary
switch, with a column gap that roughly doubles across the switch and never collapses. Twenty four is
not decoration: the composition places copy off centre, spanning ranges that a twelve column field
forces to round to halves and thirds, and rounding them is what makes a composed layout look centred
and ordinary. Two secondary arrangements exist for enumerated blocks, one of four equal parts for the
pillar row and one of two for paired copy blocks. The page gutter is narrow below the switch and
several times wider above it, and the header's own gutter widens twice as the viewport grows. Full
width scene sections sit outside the padded container while copy sections sit inside it, and both are
real: they coexist rather than one being a mistake.

Vertical rhythm is not a scale. It is measured per section, and the two that recur are a large row
gap between the five division blocks and an even larger run above and below the sustainability
chapter. They are large on purpose: the journey needs empty document to travel through between
chapters, and compressing them turns a descent into a list.

**Shape.** Circles and squares, and one softness between them. Every circular control is a true
circle: the scroll-to-top, the arrow buttons, the marker dots, the chapter chevron. One small
softness belongs to the media tiles and the paginator controls. Everything else is square. There is
no intermediate radius in this product and adding one is the fastest way to make it look generic.

**The token contract.** Every colour, size, spacing step, stacking level and radius resolves from one
named set at the document root and is referenced everywhere else. A literal written inline anywhere
is a defect, because the console renders the same type scale against the same tokens and the two
surfaces must not drift.

**Motion.** Three motion roles and no fourth. One is the workhorse: quick to leave and with a very
long, soft settle, and it does every hover lift, every control and every small positional change. One
gets up to speed so fast the eye never sees it begin, and it belongs to the pointer follower and to
the marker positions, where a visible start would read as a jump. One holds still for a beat and then
arrives decisively, and it is reserved for the chapter-scale reveals, where the hesitation is the
drama. Where a duration needs changing, change the duration: adding a fourth character is a change to
the brand rather than to a component.

There is a fourth ramp and it is flat, and the split is absolute: colour and see-through changes are
always flat and never shaped, and anything that moves is always shaped and never flat. Colour
interpolated on a shaped curve reads as a flicker; position interpolated flat reads as mechanical.
The reference never confuses the two and neither should this.

Durations form a ladder by role rather than a set of values: the shortest for a pointer-entry colour
change and the smallest transforms; a little longer for see-through and background changes; a default
one step above that which covers most of the product and is the base of the ladder; longer again for
positional changes over a distance, including the globe markers; longer still for the larger card
lifts; and longest of all, roughly three times the default, for the chapter-scale reveals, which
always pair with the hesitating character. Nothing uses a duration off that ladder to feel special.

Five reveals are named and each must exist. A card arrives from below and settles, staggered down the
grid. A line of type arrives the same way from half that distance, which is deliberate: a card travels
twice as far as a line, so the grid reads as arriving in blocks rather than as a uniform shimmer. A
navigation label arrives from a fractional offset that is a line-height remainder and must be
preserved exactly rather than rounded. A loading indicator's container arrives from above. Individual
mark paths arrive from below, which is what makes the mark assemble rather than fade.

**The character machine.** This is the most consequential single requirement in the brief. Display
headlines are split so that every character is independently transformable, and body paragraphs are
split so that every visual line is, so that a sentence assembles itself as the reader arrives rather
than fading in whole. The split happens at runtime and only after the faces have loaded, because a
line split computed against a fallback face breaks in the wrong places and never recovers. It is
non-destructive: the original text is restored when the element goes away, the element's accessible
name is the whole string and never the sequence of fragments, the text stays selectable as one
continuous string and copies with no inserted whitespace, and the browser's own find still finds it.
If the splitting technique defeats find, the technique is wrong, and anybody can check that in thirty
seconds. None of this runs in the console.

**Hover.** Roughly half the perceived craft of this site is in states no still image shows, and four
of them are required. A primary bar label rests held back and comes to full strength when pointed at,
while its siblings stay held back. A release card's underline does not appear, it grows sideways from
nothing to full width from a fixed origin. A read-more control's label does not brighten, it slides
downward out of sight while a replacement fills in behind it and its border goes from the
half-strength bright blue to solid light ground. A text link and both of its decorations move together
from the brand colour to the hover colour, never one without the other. Hover is never the only
signal on a link, because the hover colour is lighter than the resting colour: an underline or a
weight change accompanies it.

**The scroll instrument.** The home route is not a page with sections, it is a journey of roughly
twenty screens at a desktop height, most of which deliberately carries no copy at all, and the
scrollbar is its transport control. Native scrolling is replaced by an interpolated driver that keeps
moving for a moment after the reader stops pushing, reports a fractional position every frame,
exposes whether it is in motion or settled as state on the document root that anything on the page can
read, and can be stopped and restarted without losing position. Every visual change on the journey is
a function of that fractional position and of nothing else, which has one consequence that is the test
of whether it was built properly: **scrolling backwards runs the journey exactly backwards.** A
journey that only works downhill has a hidden timeline in it.

**Reduced motion.** Under a reduced-motion preference the journey is stripped, never switched off,
because the journey carries the content and the inertia is what causes harm. Specifically: the visual
layer still tracks the scroll position, with no smoothing and no inertia; the character and line
splits do not run at all and copy renders as whole text; the named reveals resolve immediately at
their resting position; the turning loading indicator is replaced by a static one carrying a text
label; route transitions cut with no cross-fade and no slide; and the pointer follower is not rendered
at all.

**One primary action per view.** Each public chapter and each console surface leads with exactly one
primary action, visually distinct from every secondary one and the only thing on that view carrying
the strongest contrast in the interface. Secondary and tertiary styles exist and are quieter; the
tertiary is the only style wearing the bright blue, on its border. Every action style has resting,
pointed-at, pressed, focused and unavailable states, and unavailable is never signalled by colour
alone.

**The console.** Four regions and no journey. A rail on the left carrying the division switcher and
then the sections this principal may see, the sections filtered rather than shown-and-refused. A bar
across the top carrying the current division, a search field, the count of work pending on this
principal, and the principal menu. The main region carrying the current surface, which is a table
first: a list of records with their state, their division, their type and their instants, dense enough
that a full queue fits one screen without a row becoming hard to hit. A contextual panel on the right
carrying, on a record, the workflow state, the decision history, the pending action and the assigned
reviewers, and on a list, the filter set. A record's preview is a real rendering of the actual public
template against the draft, switchable between the three widths, because a reviewer approves what they
saw and a preview that differs from the published result makes the whole chain worthless. Every record
surface carries one control that opens that record's own trail in place, because a history you have to
travel to is a history nobody reads. A confirmation appears as a transient message at the lower right
which is dismissible and which never carries the only copy of anything: if it matters, it is also on
the surface.

Nothing in the console locks a record. Locks strand records when somebody shuts a laptop and goes
home. Two people editing different fields of one release both succeed, because a release is edited by
a press officer and a lawyer at the same time on purpose; only a second write to the same field is
refused, and it comes back with the current value so the editor can see both. Nothing moves on screen
while an approver is reading a submission.

**Responsive.** The composition changes rather than merely narrowing. The primary switch is the one
consequential boundary in the design, and across it: the grid goes from four columns to twenty four,
the column gap roughly doubles, the page gutter goes from narrow to several times wider, the display
heading roughly doubles while its tracking more than triples, the mark changes from its stacked
lockup to its horizontal one, the primary bar goes from the current division alone to all five, the
scroll cue's copy changes from `Swipe down` to `Scroll down to discover`, and the pointer follower and
every hover behaviour appear. Two further widths adjust the header gutter and the widest layout, and
the arrangement holds at every width between them. Pick one boundary convention and hold it: the
reference used both an inclusive and an exclusive form of the same boundary, which lets one exact
width match both the minimum-width rule and the maximum-width rule and produces a fault visible at
that one width and nowhere else. Avoid that overlap by using the exclusive form throughout.

The mobile home composition is authored rather than derived, and that is expensive and it is what the
product needs: the phone journey is longer than the tablet one despite the phone being less than half
as wide, which is impossible if it is the same composition reflowed. The build must be able to express
a chapter that exists at one width and not at another, and chapters whose order differs by width. A
phone also receives a different instruction rather than a reworded one: `Swipe down` and
`Scroll down to discover` are two strings for two gestures and are never one string reused.

Full-height chapters size against the smallest viewport height rather than the dynamic one, so that a
phone's address bar collapsing does not resize anything mid-journey. On a short viewport, such as a
landscape phone, the opening chapter is not full height, the scroll cue sits inline rather than pinned
to the foot, and the overlay menu scrolls rather than fitting. The document itself never scrolls
sideways; genuinely wide content scrolls inside its own container with a visible affordance. Any
control on a coarse pointer is at least 44px by 44px, and every hover affordance has a non-hover
equivalent, because a phone has no pointer to hover with.

The console is built for 1024px and upward and deliberately not for phones, with exactly one
exception: an approver must be able to read a submission and approve, reject or request changes from a
phone, because approvals hold publication up and approvers travel. That is a dedicated narrow surface,
not the console reflowed.

**Accessibility.** WCAG 2.1 level AA across both surfaces. A site built on a scroll journey and
character-split headlines fails by default, so every rule here is a countermeasure to something above
and none of them is optional.

Body text holds at least 4.5 to 1 against its background and large text at least 3 to 1, in every
state and over every chapter ground: the light ground on the slate chapter, and on every other chapter
ground, varies with the ground and so is not determinable statically, which means a single reading
proves nothing. Each chapter therefore carries a scrim sufficient to hold the ratio against that
chapter's brightest state, established by sampling that chapter rather than by judging one frame by
eye. Three measured failures in the reference are corrected rather than
copied: the palest cool neutral never carries text and is restricted to rules and dividers; secondary
copy on light ground uses the hover colour at 16px and above, or the brand colour at any size; and
link hover is never the only indicator, because it reduces contrast rather than increasing it.

Every visual layer is decorative and carries nothing the copy does not, so it is removed from the
accessibility tree entirely, and any label that appears inside it, such as an office's country beside
its marker, also exists as real document text. Nothing flashes more than three times a second
anywhere, including the loading indicator.

Keyboard scrolling moves the driver, not the document behind it: page up, page down, home, end, space
and the arrow keys all move through the driver, and focusing an element that is out of view scrolls it
into view through the driver too. A native focus jump moves the document without telling the driver,
and the journey then renders the wrong chapter until the next gesture; that is the one that breaks.
The driver interpolates and never prevents or redirects a scroll gesture. A skip link is first in the
document and visible on focus. The chapter index is operable rather than decorative: each numeral is a
control that travels to its chapter, the current chapter is exposed as state, and the set is reachable
by keyboard in document order.

Names describe the destination or the action, never the shape: a circular arrow button is named for
where it goes, taken from the label beside it, rather than "arrow"; the chapter numerals are named for
their chapters rather than their numbers; the release counter is named for what it counts rather than
being a bare numeral; the menu trigger exposes whether it is expanded and that changes; and the mark
is the only non-decorative icon in the product and carries the group name. The sustainability pillars
are a real tab set: the arrow keys move between them, only the current tab is in the tab order, each
panel is labelled by its tab, and the current pillar is reflected in the address so one can be linked.

In the console: complete keyboard operation including block insertion, reordering and link editing;
focus visible at all times and never suppressed, drawn so it reads on any ground; focus order matching
visual order in all three regions; one polite live region for save state and one assertive for errors
and transition results; table headers associated and sortable columns announcing their state; dialogs
trapping focus, closing on escape and returning focus to what opened them; and a session about to
expire warning with an extend control rather than discarding work. Status and validation never rely on
hue alone: each carries an icon, a label or a shape. Every control has a visible persistent label,
never a placeholder standing in for one. At 200 per cent text scale the layout reflows to a single
column with nothing clipped and no sideways scroll.

**Copy.** Sentence case except for proper nouns and the uppercase navigation labels, no exclamation
marks, no first-person plural in an interface string, verbs in the imperative for actions, and empty
and error strings that name the thing that is missing rather than apologising. These strings appear
exactly as written: `Calder Group`, `Calder Trading`, `Calder Capital`, `Calder Maritime`,
`Kite Energy`, `News`, `Menu`, `Contact`, `ESG`, `Privacy policy`, `Terms of use`,
`Scroll down to discover`, `Swipe down`, `Who we are`, `Explore Our`, `Products:`, `Oil`, `Metals`,
`Environmental`, `Social`, `Governance`, `Contact us`, `First`, `Last`, `Geneva, Switzerland`,
`Dubai, UAE`, `Singapore`.

**What it must not look like.** No page dominated by one hue family with no second signal. No second
accent beside the one bright blue. No intermediate corner radius. No decoration standing in for
content. No marketing composition where the console belongs, and no journey, no split text and no
drifting scroll inside it. No chapter rendered as a heading over a void. No error surface that makes
somebody wait for scenery before telling them what went wrong.

## Front-end specification

This section carries the visual detail that does not fit the notes above. Nothing graded lives only
here; this is the specification's long form.

### The type scale, exactly

Thirteen classes, each measured in the two states the primary switch produces. The first value is the
base state, the second is at and above the switch.

| Class | Size | Line height | Letter spacing |
|---|---|---|---|
| `fs-h1` | `2.5rem`, then `5rem` | `1.2` | `.25rem`, then `.5rem` |
| `fs-h2` | `2.25rem`, then `3.125rem` | `1.4` | `.09rem`, then `.14rem` |
| `fs-h3` | `1.75rem`, then `2.5rem` | `1.4` | `.14rem`, then `.1rem` |
| `fs-h4` | `.75rem`, then `1.25rem` | `1.4` | `.03rem`, then `.05rem` |
| `fs-h5` | `1rem` | `1.6` | none |
| `fs-s1` | `1.25rem`, then `1.5rem` | `1.6` | `.03rem` above the switch |
| `fs-s2` | `1.25rem` | `1.6` | `.05rem` |
| `fs-body` | `1rem` | `1.6` | `.08rem` |
| `fs-body-s` | `.75rem` | `1.6` | `.06rem` |
| `fs-cta` | `.75rem` | `1.2` | `.025rem` |
| `fs-cta-s` | `.75rem` | `1.2` | `.03rem` |
| `fs-label` | `.75rem` at weight `700` | `1.4` | `.0375rem` |
| `fs-numerals` | `.5rem` at weight `700` | `1.6` | `.025rem` |

Two further styles are required and are not in the table above, because they were measured in the
rendered output rather than declared. `fs-label-lg` is `14px` at weight `700` over a line height of
`16.8px`, and it is the most-used label variant in the product. `fs-h1-index` is `62px` at weight
`300` in the display face, and it sets the release archive's heading and nothing else.

Rounding `.5rem` of tracking to a pixel value, or collapsing `rem` to `em`, produces a headline that
reads as a different brand. The relationship to hold is the one in the notes: across the switch the
largest heading roughly doubles in size and its tracking more than triples.

### Stacking, in order

Six levels and no more, named by occupant: behind everything, the visual layer; then in-flow chapter
overlays; then the sticky chapter index; then the header and the utility cluster; then the overlay
menu; and above everything including the menu, the pointer follower. The gaps between them are
deliberate, so that a seventh occupant has somewhere to go without renumbering.

### Iconography

Every icon in this product is geometry drawn inline. No icon font, no icon image, no icon sprite,
nothing that arrives as a file. An icon inherits its colour from the copy around it, except the mark
and the pillar set, which declare theirs. An icon inside an interactive control is decorative and the
control carries the name.

The mark exists in two genuinely different drawings and both must be built. The horizontal lockup is
a wide filled drawing used in the light-ground footer and, in a reversed cut, over a chapter ground.
The stacked lockup is a taller compound drawing used in the loading state and on narrow screens, and
its emblem is stroked rather than filled, which is how the emblem survives at the size the loading
state uses it. Substituting one for the other at the wrong size loses the emblem entirely. The emblem
is a stylised tree of dots above the wordmark, and two of its parts move independently: a hairline
vertical trunk, which is the only straight line in the mark, and a single pivot dot.

Four directional icons, all single-path and all inheriting their colour: an arrow pointing right, a
filled arrow pointing up, a downward scroll cue, and a small chevron derived from the cue at a little
over half its scale. Their terminal weights differ, deliberately, each tuned to the size it is used at:
the right arrow is the lightest, the up arrow the heaviest, and the cue sits between them. Normalising
them to one weight is the single most common way this set gets flattened.

The loading indicator is two arcs of one circle laid end to end, each stroked with its own gradient
across four stops, rotating continuously. Building it as one stroked circle with a dashed offset
produces a visibly different object: the two gradient halves are what give the ring its fade, and a
dash cannot reproduce it.

Four pillar marks sit inside circular outlines, rendered in the light ground over the slate chapter:
a leaf drawn as one long curved stroke closed by a short filled tail; three overlapping figures at
three sizes, the leftmost solid, the centre outlined and the right a small solid dot; a monogram
letterform set in a plain geometric; and a ring with a chord and a small solid node at its lower
right, which carries the same small node twice at identical coordinates because one of the two moves
independently. Reproduce both. None of these may be replaced by a font glyph, because each is animated
per part and a glyph has no parts.

### Global chrome

Four elements are present on every route and survive navigation between routes without being rebuilt:
the header, the overlay menu, the pointer follower and the footer.

The header is fixed and has no background at all, which is why its background never changes. What
changes is the colour of its copy, which inverts between the brand colour and the light ground as the
chapter beneath it changes ground. It fades rather than slides, on the flat ramp. It carries three
parts: the division bar, five uppercase labels at the small call-to-action tracking, with the current
division at full strength under a hairline rule and its siblings held back and restored on pointer
entry; the release counter, a numeral in a circular brand-coloured fill with the light ground as its
figure, at weight 700; and the menu trigger. The rule under the current label is measured from the
label's own width rather than set to a fixed length.

The overlay menu is closed by default and occupies the full screen when open. It carries the five
division names, then `Contact`, `ESG`, `Privacy policy` and `Terms of use`. Every label in it appears
twice in the markup, which is the signature of the per-character reveal: one copy is the resting text
and the other the incoming text, offset and clipped. Opening it must lock the document scroll without
shifting the layout, trap focus inside the overlay, return focus to the trigger on close, and close on
the escape key and on a route change.

The pointer follower is three nested pieces. An outer ring trails the pointer with a per-frame
interpolation, so it reads as having weight. A middle dot tracks the pointer exactly with no lag. A dot
between them collapses over an interactive target and springs back from precisely the point it left,
and it collapses by scaling to nothing rather than by fading, which is why it returns from the same
place rather than reappearing wherever the pointer now is. The follower is suppressed entirely wherever
there is no fine pointer with hover, which is the site treating touch as a different product rather
than the same product with the mouse missing.

The footer is four columns on a wide screen: a link column carrying the five divisions then `Contact`,
`ESG`, `Privacy policy` and `Terms of use`; then one column per office carrying the city and country
heading, the address, the telephone and the reception address. Beneath a full-width rule sit the
horizontal mark and the copyright line, right aligned. Office headings are set at `fs-s2` and the
address and contact lines at `fs-body-s`. Telephone and mail lines are real protocol links and they
carry no trailing character after the number or the address: the reference did, and it breaks the dial
action on some handsets.

Routes that carry no visual layer, which is every route except the group home and the five division
routes, must not load the visual layer at all rather than loading it and leaving it empty.

### The journey, chapter by chapter

The group home is a single continuous descent, and these are the states along it in order. There is no
cut between them: each is a position on one path, and the chapter index counts them off in numbered
diamonds at the left margin.

| Fraction | On screen |
|---|---|
| the start | the summit above cloud, the mark centred left in its reversed horizontal cut, the scroll cue at the foot |
| an eighth in | descending into cloud, the opening statement setting line by line, one peak still visible |
| a quarter in | inside cloud, the first two divisions, each with a numbered diamond and a link |
| over a third | out over a dark sea, a vessel under way, the fifth division |
| the midpoint | a lit globe seen from close, with a marker and a country label |
| just past it | the globe from further out, the sustainability statement over it |
| three quarters | the slate ground, the sustainability heading, three pillar tabs and four pillar marks |
| seven eighths | the diversity statement, chapter four, and the corporate responsibility heading rising |
| the end | the footer, on the light ground, the visual layer gone |

Chapter zero carries no headline at all. The mark over the mountain is the headline, and the first
words arrive only when the descent begins. Do not add a hero heading.

Chapter one is the opening statement: a character-split headline at `fs-h1` reading
`Calder is a global commodity trading and asset investment company.`, a line-split paragraph at
`fs-s1` stating that the group trades, refines, stores and transports energy and commodities, invests
in related assets, and provides services with integrity and efficiency to create long-term value for
its clients, and a link block carrying the label `Who we are`, a circular button holding the right
arrow, and a hairline rule beneath both. The paragraph's line breaks are art-directed and are
preserved: it is set one element per visual line, not reflowed. The rule spans wider than the label and is a hover target in its own
right, as well as the label. The anchor is `#WhoWeAre`.

Chapter two is the five divisions, in numbered blocks with a large row gap between them. Each block
carries a numeral in a square outline rotated exactly forty five degrees, an eyebrow in sentence case,
a character-split proposition at `fs-h2`, and a link with the division name in uppercase, the circular
arrow and the hairline. The rotation is composed with a half-unit translation that keeps the outline on
the pixel grid; without it the outline renders visibly heavier on one side. `Calder Group` is block one
and does not link away. The propositions are pinned copy and read, in order:
`Operating Efficiently, Leading with Innovation.` for `Calder Trading`,
`Identify and seize opportunities that maximise value` for `Calder Capital`, a fleet and logistics
line for `Calder Maritime`, and `Energy investments` for `Kite Energy`. The chapter heading above
them is `We provide energy solutions with integrity and efficiency`, and the interlink paragraph
beneath them states that the group's divisions complement each other, providing integrated services
that leverage their combined expertise. The anchor is `#WhatWeDo`.

Chapter three is the globe, under a character-split headline stating that the group is established
in the world's major trade hubs and financial markets with over 15 global offices, connecting and
serving both emerging and mature markets worldwide. It is a lit sphere filling most of the frame,
carrying small circular markers
with uppercase country labels beside them at `fs-label`. A label appears only while its marker is on
the visible hemisphere. The markers are positioned in document space and moved to follow their
projected position each frame, and their movement is smoothed on the second motion character, on
position and on colour together, which is why they glide rather than jitter as the globe turns and is
the only place that character appears in the layout. Markers are content, not code: they come from the
office records, each with a latitude, a longitude and a label, so opening an office is an editorial act
rather than a deployment. The anchor is `#GlobalConnectivity`.

Chapter four changes the ground to a mid cool neutral slate and the visual layer recedes. It carries
the sustainability heading `Delivering sustainable energy solutions` at `fs-h2` in the light ground,
above a statement that the group is committed to integrating its sustainability strategy with its
pursuit of value, powering lives and respecting nature, and recognises the lasting impact its
decisions have on people, communities and the environment; a left column with the strategy paragraph
truncated at six lines with a trailing ellipsis and a circular chevron control beneath it that expands
it by height; a right column with three tabs, labelled `Environmental`, `Social` and `Governance`, and their
panels, the environmental panel opening on the statement that reducing the group's impact on the
environment is paramount to its business; and a row of the four pillar marks in four equal parts,
standing for environment, society, governance and carbon. The current tab is the light ground at weight 700 under a hairline rule of the same
colour; the others are the palest cool neutral under a weaker rule. The anchor is `#Sustainability`.

Chapter five is two paired copy blocks in two equal parts: on the left the statement
`We strive to create an environment where everyone can thrive and contribute to our success.` at
`fs-h3`; on the right the diversity figures paragraph at
`fs-body`; a hairline at the weakest strength of the palest cool neutral spanning the right column; the
fourth chapter numeral in its diamond at the left margin; and the corporate responsibility heading
`Our pledge to corporate social responsibility` at `fs-h2`, held back until it clears the fold. The figures in the right block come from the figures
record, not from the template.

Chapter six is the footer: the visual layer ends, the ground returns to the light neutral.

Each of the four anchors is a real, linkable, shareable address. Arriving at one on a cold load must
render the document with the journey already at that chapter, must not animate the travel from the
start, and must leave the driver settled so the first wheel gesture moves from that point. Arriving at
the same anchor from a link inside the document does animate, on the hesitating character at the
longest duration. The footer links to `/#Sustainability` from every route, so that restore path runs
across documents.

### The scroll cue, the index and the lock

The scroll cue sits at the foot of the opening chapter, reading `Scroll down to discover` above the
primary switch and `Swipe down` below it. It fades out on the first scroll input and never returns,
and the label itself drifts as it goes, on a fine positional scrub above the switch and on a
see-through scrub below it. That difference is authored rather than scaled, and is the clearest single
sign that the touch composition was designed rather than shrunk.

The scroll-to-top control is the filled up arrow in a circular button. It rests invisible, appears after
the first screen, and returns the journey to its start.

Three things lock the scroll and all three use the same mechanism: the overlay menu, any dialog, and
the loading state before first paint. Locking stops the driver rather than setting an overflow on the
document, because setting overflow while the driver holds a fractional position makes the page jump by
the fractional remainder on unlock. That jump is the single most common defect in builds of this shape.

### Loading, and the authored no-layer variant

Loading is four phases and the document must be readable at the end of the second. Phase one is the
document, the fonts and the copy, with the visual area blank. Phase two is the first coarse visual
state, after which the site is usable. Phase three brings the current chapter to full detail. Phase
four prepares the adjacent chapters while the reader is idle. The loading indicator may cover phases
one and two only: blocking the document on phase three is what makes a site like this feel broken on a
hotel connection, and the reference did exactly that on three of its five division routes, which
returned a document and then never painted.

Every route carrying a visual layer also has a complete, authored variant with no visual layer, and it
is not a degraded version of the same page. It carries the same copy, the same headings, the same
links and the same chapter order, over still posters generated from the same procedural sources, and
it passes every accessibility and performance requirement independently. It is served to any device
that fails the capability check, to a visitor who has asked for reduced data, to a visitor under
reduced motion who additionally opts out, and to a crawler. It is not an afterthought: it is the
version most of the world will actually see.

### Gradients, placeholders and the zero-asset substitution rule

Nothing in this build ships as a binary that was downloaded, and every asset class has a
substitution recipe instead of a file. Two gradients exist and only two. The
first is the placeholder sheen a media tile carries before its image resolves, which begins its first
stop at a negative position on purpose, so that the visible band is the tail of a much wider ramp and
a tile of any width gets the same slow wash rather than a compressed one; preserve the negative stop.
The second is a scrim that lifts copy off the lower right of a full-bleed chapter.

Where a record needs an image and has none, the placeholder is generated from a hash of the record's
own identifier, using two colours from the palette, at the aspect ratio of the slot, with the record's
initials set in the brand sans at low contrast. The same record always produces the same placeholder.

Grain, cloud density, terrain break-up and micro surface relief are generated once at startup and
cached, never requested over the network: a fine grain over the whole composed frame, a smooth gradient
noise for cloud, a cellular pattern for surface break-up, and a normal derived from the grain by finite
differences. The four chapter grounds are, in order down the journey, a near-white neutral cloud sheet,
a near-black cool neutral sea, the lit globe under a near-white, soft cyan atmosphere key, and a mid
cool neutral slate. Rock and snow mid tones are three light cool neutrals a step apart from each
other; terrain diffuse mid tones run from a near-white neutral to a mid, muted amber; and the water on
the fleet chapter runs a ramp from a mid, soft cyan through a light, soft teal to a near-white, muted
teal. A marker on the globe carries a glow at one strength of the brighter ground tint. A handful of
near-black greens in the reference's own render layer, a deep, soft green and a deep, muted green
among them, are channel-packing constants rather than colours: a value that never touches the document
is not a brand token, and a build that promotes one of them to a brand green has misread the
evidence.

### The release archive, precisely

The archive heading is set in `fs-h1-index`, left aligned, in the brand colour. The grid is three cards
across on a wide screen, on the twenty four column field. A card carries an image at the small
softness with a fixed aspect and a cover fit, a date at `fs-body-s` in the secondary copy colour, and a
title at `fs-s2` in the brand colour over at most two lines. Dates render as a long month, a day and a
four-digit year, with no comma before the year. A card's underline is a hairline rule hidden at zero
horizontal scale that grows to full width from a fixed origin on pointer entry. Cards reveal from below
and settle, staggered down the grid.

The paginator is five controls, centred, each a rounded rectangle at the small softness with a hairline
border, in this order: `First`, previous, the current page numeral, next, `Last`. On page one the first
two are present and unavailable, rendered at half strength, and they stay in the document and stay
skipped by the keyboard rather than being removed, so the paginator does not change width between
pages. The page numeral is set at weight 700 in the same frame the release counter uses.

### The console shell, precisely

The console loads no visual layer, no scroll driver, no character splitting and no pointer follower.
Its rail carries the division switcher first: a principal holding one division sees the division's name
and no control, and a principal holding none, which `group_admin@example.com` does by design, sees an
explanatory surface and no content. Below it, the sections this principal may see. Its top bar carries
the current division, the search field, the pending-work count and the principal menu. Its record
surface is three panes: the editor with the fields in the order the type declares, the review rail, and
the preview. Its inbox is four queues in the order given in `## Core features`.

## Technical requirements

Frontend: `SolidStart`. Backend: `FastAPI` on Python. The rendering model is server-rendered documents
with interactive islands: a visitor's first paint of any public route is HTML the server produced from
the finished-document store, carrying the copy before any script runs, and the interactive pieces
attach to that HTML afterwards. The console is one of those pieces and is never prerendered. Storage:
`PostgreSQL` for records, `minio` for media bytes. Authentication: app-implemented email and password with
bearer tokens, passwords hashed at rest. There is no external identity provider, so nothing is
trusted from an outside assertion. Health: `GET /api/health` returns `200` once the app is
ready. Logging: one structured line per request to standard output carrying the method, the path, the
status, the request identifier and the principal identifier when there is one, and never a password, a
bearer token, an object-store credential, a visitor's name, a visitor's address or the text of anything
a visitor typed into a form.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database,
cache, queue, object store, identity provider or mail vendor - the only backing services available in
this environment are `PostgreSQL` and `minio`, and reaching for anything else is a contract violation.

The backing services are already running and reachable at these variables, which the app reads from the
environment and never hardcodes: `DATABASE_URL` for `PostgreSQL`; `STORAGE_ENDPOINT`, `STORAGE_BUCKET`,
`STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY` for `minio`; `APP_PUBLIC_URL` and `APP_PUBLIC_PORT` for
the app itself.

Correlation is one identifier end to end. A request identifier is accepted from the caller or minted
for the request, echoed on the response, present in every log line the request produces, written onto
every audit entry it causes, and shown on the server-error surface. One identifier from beginning to
end is the difference between a five minute investigation and a five hour one.

Every response the app serves carries the standard security headers, including a strict transport
policy, a policy that forbids content-type sniffing, a policy denying every frame ancestor, and a
policy denying camera, microphone, geolocation and payment, and a cross-origin opener policy
confined to the same origin. Referrer information is limited to the origin on cross-origin
navigations. Anti-forgery: because the console carries a bearer token rather than an ambient cookie, a
cross-site request forgery has no credential of the visitor's to borrow; even so, no state-changing action is
reachable by a safe method, and a transition triggered by following a link is a defect. Nothing the browser downloads contains a credential, an API key or
an administrative token: not the script bundle, not a stylesheet, not an inline script, and not any
JSON payload served to an anonymous reader.

The app serves a favicon and declares it in the document head of every route it renders. Every public
route declares its own social preview title, description and image, no two public routes share them,
and every declared preview image resolves to a real object rather than to a missing address.

The public search, the archive's filters and the console's record lists are narrowed in the store
rather than by fetching every row and discarding most of them in the browser, and a console list pages
with a cursor rather than an offset, so a page boundary stays stable while records are being written.

Performance is a requirement with a stated budget rather than an aspiration. The largest element to
paint on any public route is text, never a visual layer: if a visual layer is the largest element the
budget cannot be met on a four year old mid-range laptop with integrated graphics, and no optimisation
afterwards recovers it. Asking whether one principal may read a page of 50 records costs one decision
over the set, not 50 separate ones, and the cost does not grow with the number of divisions. The app
answers a public document read, an archive page and a search inside one budget with 20000 content
records across the five divisions and 4000 audit entries.

## Data model

Fourteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**principals** - `id`, `email` (unique, lowercase), `password_hash`, `display_name`, `is_active`,
`created_at`.

**divisions** - `id`, `key` (unique, one of `group`, `trading`, `capital`, `maritime`,
`kite-energy`), `name`, `wordmark`, `primary_colour_role` (`group` or `own`), `is_archived`.

**memberships** - `id`, `principal_id`, `division_id` (nullable, null only for `group_admin`), `role`
(`author`, `legal_reviewer`, `compliance_officer`, `publisher`, `group_admin`),
`granted_by_principal_id`, `justification` (nullable), `granted_at`, `expires_at` (nullable),
`revoked_at` (nullable). A principal holds any number of rows here, including two roles on one
division. A membership is never a column on a principal, because a column cannot carry who granted it
or when it lapses.

**offices** - `id`, `city`, `country`, `jurisdiction` (`CH`, `AE-DIFC` or `SG`), `address_lines`,
`phone_e164`, `phone_display`, `reception_email`, `latitude`, `longitude`, `marker_label`,
`image_media_id` (nullable), `is_data_controller_contact`. Both telephone forms are stored, because
the display form carries spacing that is locally meaningful and the normalised form is what a link
uses. Exactly one office per jurisdiction carries `is_data_controller_contact`.

**content_records** - `id`, `type` (`page`, `release`, `product`, `vessel`, `investment`, `person`,
`figures`, `policy` or `redirect`), `division_id`, `slug`, `state` (one of the ten), `title`,
`current_revision_id`, `published_revision_id` (nullable), `disclosure_class` (nullable, one of
`general`, `regulated`, `market_sensitive`, `restricted`), `embargo_at` (nullable), `published_at`
(nullable, first publication and never rewritten), `unpublished_at` (nullable), `unpublish_reason`
(nullable), `fast_path_count_7d`, `created_by`, `updated_by`, `created_at`, `updated_at`. No two
records of one type share a slug. `current_revision_id` and `published_revision_id` are distinct and
the public path reads only the second.

**content_revisions** - `id`, `record_id`, `parent_revision_id` (nullable), `author_principal_id`,
`created_at`, `fields`, `content_hash`, `approved_field_hash`. A revision is never rewritten.
`content_hash` covers the whole canonical field set; `approved_field_hash` covers only the fields in
the type's approved set, and it is the one an approval is recorded against.

**content_blocks** - `id`, `revision_id`, `stable_block_id`, `position`, `block_type` (one of
`paragraph`, `subheading_2`, `subheading_3`, `list_unordered`, `list_ordered`, `quote`, `image`,
`table`), `payload`. `stable_block_id` is the same value across revisions for the same block.

**submissions** - `id`, `record_id`, `revision_id`, `chain_version`, `submitted_by`, `submitted_at`,
`state`, `completed_at` (nullable). At most one row per record has a null `completed_at`.

**approval_stages** - `id`, `submission_id`, `stage_index`, `role_required`, `state` (`pending`,
`approved` or `changes_requested`), `decided_by` (nullable), `on_behalf_of` (nullable), `decided_at`
(nullable), `comment` (nullable), `revision_hash_at_decision` (nullable). No stage's `decided_by`
equals its submission's `submitted_by`, and no two stages of one submission share a `decided_by`.

**delegations** - `id`, `from_principal_id`, `to_principal_id`, `role`, `division_id`, `granted_at`,
`expires_at` (never more than 30 days after `granted_at`), `revoked_at` (nullable).

**policy_entries** - `id`, `reference_code`, `title`, `version`, `effective_from`, `effective_until`
(nullable), `owner_role`, `review_interval_days`, `scope_division_ids`, `jurisdictions`, `publication`
(`internal`, `external` or `both`), `body_revision_id`, `supersedes_id` (nullable), `reviewed_at`. A
reference code and a version together are unique.

**disclosure_bindings** - `published_revision_id`, `policy_reference_code`, `policy_version`. What a
published document actually carried, recorded at publication and never rewritten afterwards.

**media** - `id`, `division_id`, `record_id`, `object_key`, `content_type`, `byte_size`, `sha256`,
`width`, `height`, `focal_x`, `focal_y`, `alt_text` (never empty), `caption` (nullable), `credit`
(nullable), `scan_state`, `uploaded_by`, `uploaded_at`. The bytes are in the bucket; this table records
where they are.

**published_documents** - `route_path`, `locale`, `jurisdiction_variant` (nullable), `record_id`,
`revision_id`, `rendered_at`, `etag`, `payload`, `policy_versions`, `depends_on_tags`. The public
serving path reads this table and no other.

**enquiries** - `id`, `public_reference`, `subject_area`, `name`, `organisation` (nullable), `country`,
`jurisdiction`, `email`, `phone_raw` (nullable), `phone_e164` (nullable), `message`,
`consent_policy_version`, `consent_at`, `received_at`, `routed_office_id` (nullable), `delivery_state`
(`pending`, `routed` or `failed`).

**audit_entries** - `id`, `occurred_at`, `actor_principal_id`, `on_behalf_of_principal_id` (nullable),
`action` (a closed vocabulary, never a free string), `resource_type`, `resource_id`, `division_id`
(nullable), `before_hash` (nullable), `after_hash` (nullable), `decision` (`allow` or `deny`),
`deny_reason` (nullable), `request_id`, `prev_entry_hash`, `entry_hash`. Rows are added and read and
never changed: no endpoint updates one and no endpoint deletes one.

There is no mass-deletion path anywhere in this product, and its absence is structural rather than
careful: no transition removes a content record, the withdrawal path is a state rather than a
deletion, and the trail cannot be deleted at all, so an accidental mass deletion is prevented rather
than merely recoverable. An archived record stays recoverable indefinitely.

Derived rather than stored: the release counter; whether a policy entry is currently in force; the
archive's page count; the number of documents a publication refreshed; a chapter's numeral once an
unpublished chapter has renumbered the set; and the effective decision for one principal on one
resource.

The structural invariants, stated together. A record in `published` has a non-null
`published_revision_id`. A record in `embargoed` had an `embargo_at` in the future at the moment it
was scheduled. A record whose `disclosure_class` is `market_sensitive` never moves from `approved`
directly to `published`. At most one submission per record is open. Every decided stage records the
revision hash it approved. No stage is decided by its submission's author, and no two stages of one
submission are decided by the same principal. Every published document names the policy versions in
force when it was rendered. Every media row has non-empty `alt_text`. A redirect chain is one hop.
Each audit entry's `prev_entry_hash` equals the previous entry's `entry_hash`. A published record's
slug never changes.

Two transitions on one record from the same starting state do not both succeed. Exactly one is
accepted, the record advances, and the other is rejected as a conflict carrying the state the record
is actually in. The same holds for two edits to one record from the same revision, and for two
publications of one embargoed record at its instant: exactly one publication exists. This holds under
real concurrency.

**Seed data.** Six principals as listed in `## User roles`, with the memberships listed there. Five
divisions with the keys listed above; `kite-energy` carries its own wordmark and
`primary_colour_role` of `own`, and the other four carry `group`. Three offices, each rendered on the contact route under the headings `Geneva, Switzerland`,
`Dubai, UAE` and `Singapore`. Geneva: jurisdiction `CH`, address `12 Quai des Bergues, 1201 Geneva`,
telephone `+41225550118` displayed as `P : +41 22 555 0118`, reception `gva@calder.example.com`, the data
controller contact for `CH`, marker label `SWITZERLAND`. Dubai: jurisdiction `AE-DIFC`, address
`Level 14, Gate Village 7, DIFC, Dubai`, telephone `+97145550142` displayed as `P : +971 4 555 0142`,
reception `dxb@calder.example.com`, the data controller contact for `AE-DIFC`, marker label `UAE`.
Singapore: jurisdiction `SG`, address `8 Marina View, Asia Square Tower 1, Singapore`, telephone
`+6562550173` displayed as `P : +65 6255 0173`, reception `sgp@calder.example.com`, the data controller
contact for `SG`, marker label `SINGAPORE`. The media enquiries line reads
`For any media enquiries, please contact` above the address `media@calder.example.com`.

Nine published releases, newest first:

| Date | Title | Division |
|---|---|---|
| `December 15 2023` | `Calder joins Energy LEAP for Operational Excellence` | `group` |
| `December 1 2023` | `Calder participates in Cargo Day 2023` | `group` |
| `September 4 2023` | `Calder Trading expands its Fujairah blending capacity` | `trading` |
| `May 31 2023` | `Calder and the Private Office of Sheikh Ahmed...` | `group` |
| `April 18 2023` | `Calder Capital appoints its first investment committee` | `capital` |
| `February 16 2023` | `Calder and the Private Office of Sheikh Ahmed...` | `group` |
| `December 7 2022` | `Calder enters South African energy market with New Ag...` | `group` |
| `October 3 2022` | `Calder Maritime charters two medium range tankers` | `maritime` |
| `August 12 2022` | `Calder Maritime acquires its first vessel` | `maritime` |

The ellipsis inside three of those titles is the truncation applied when the document was produced;
the full title is stored on the record and is what assistive technology announces.

Five further releases, one in each of the states that matter: one `draft` on `trading`; one
`compliance_review` on `capital`, whose legal stage was decided by `legal_reviewer@example.com`; one
`approved` on `capital` classified `general`; one `embargoed` on `trading` classified
`market_sensitive`, titled `Calder Trading agrees a multi-year naphtha supply arrangement`, with an
embargo instant 30 days after the app first starts and a lead image already in the bucket; and one
`unpublished` on `group`, titled `Calder restates its 2022 throughput figures`, withdrawn with the
reason `Superseded by a corrected statement`.

Twelve `product` records on `trading`, in two families, each carrying a name, a family, an order and
a body whose substance is fixed. `Oil` carries: `Crude oil`, the movement of crude from producing
countries to international markets in support of external refineries; `Marine Fuels`, bunkering in
Fujairah, the third largest bunkering market in the world, through a network of bunker barges;
`Gasoline`, gasoline and its components, with storage and a blending hub; `LPG (Liquefied Petroleum
Gas)`, very large gas carriers from the United States and the Arabian Gulf to Far East Asia, and
pressurised cargoes to local markets in Asia and Africa; `Power and Gas`, trading licences in Turkey;
`Fuel Oil`, blending for the bunker barges and utility-grade supply to power plants; `Downstream`,
storage and downstream infrastructure, with over one million metric tons moved into East and Southern
Africa; `Naphtha`, petrochemical grades and gasoline blending grades; and `Renewables`, developing
relationships in the renewable and low-carbon space. `Metals` carries: `Ferroalloys`, which are vital
in steelmaking for strength and corrosion resistance, comprising ferromolybdenum, ferroniobium,
ferrotungsten, ferromanganese and ferrosilicon; `Dry Bulk`, pet coke and bauxite; and `Base Metals`,
copper, aluminium, zinc, nickel, lead and tin, valued for durability and conductivity across
construction, manufacturing, electronics and transportation. The family's own introduction states
that the metals, minerals and dry bulk division operates globally, managing transportation, storage
and supply from source to end consumers. `Renewables` carries a body and no image, which is its
expected state. Three `vessel` records on `maritime`, two owned and
one chartered. Two `investment` records on `kite-energy`. Eight `person` records on `group`, of which
six are published, one is scheduled to stop displaying and one is unpublished.

One `figures` record on `group`, carrying an office count of `15`, a nationality count of `27`, a
female share of the global team of `35`, a female share of management of `22`, and an `as_at` date,
because these numbers appear in regulated disclosures and a stale one is a misstatement rather than a
stale cache. The diversity paragraph on the home route renders from this record and not from the
template.

Six `policy` register entries: `POL-CONDUCT` at version 2, `POL-PRIVACY-CH`, `POL-PRIVACY-AE` and
`POL-PRIVACY-SG` all at version 3 and sharing a parent, `POL-TERMS` at version 1, and `POL-DISC-REG`
at version 4, which is the regulated disclaimer the capital route carries. `POL-CONDUCT` version 1 is
retained as a superseded version with the period it was in force. All six are published externally
except `POL-DISC-REG`, which is published as both.

The copyright line is derived from the latest publication instant or from the build instant, never
authored: the reference hard-coded a year two years stale on a site carrying current releases.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Constraints

- No confidential reporting channel, no anonymous case intake, no claim codes and no break-glass
  access. The helpline block on the contact route is replaced by the published media address.
- No live three dimensional scene layer: no mesh loading, no texture transcoding, no per-frame
  lighting, no camera path through geometry. The journey, its chapters, its anchors, its scroll
  binding and its authored no-layer variant are all required; what sits behind them is a generated
  visual layer rather than a loaded world.
- No ambient audio layer, no audio meter and no sound control.
- No federated sign-in, no directory provisioning, no second factor, no step-up assurance, no
  service or integration credentials, no passkeys and no recovery codes.
- No email and no notification delivery of any kind. Notifications exist inside the console only.
- No outbound webhooks, no event subscribers, no inbound hooks and no third-party integrations.
- No third-party script of any kind, no tag manager, no external analytics and no external consent
  platform. Measurement is server-side only.
- The app does not work with the network off. A visitor who loses their connection gets their
  browser's own failure rather than a cached copy of a route they visited before, and nothing the
  app holds survives a reload with the network down.
- No data residency choice, no per-region keys, no retention policy engine, no erasure workflow and
  no subject access export.
- Internationalisation is out of scope, and it is scoped out on the record rather than forgotten.
  One locale, English: no translation workflow, no locale negotiation, no per-locale number or date
  formatting, no translated interface strings and no right-to-left mirroring. The two scroll-cue
  strings stay two strings and are never one string reused.
- No trading, position, cargo, vessel movement, price or counterparty data enters this platform, and
  no credential or network path to any system holding it exists. This is a control, not a scoping
  note: a public website holding a key into a commodity trading system is a target with an unusually
  attractive payoff, and the safest way to protect that key is not to have one.
- No external network calls at runtime beyond the two backing services named in this brief.
- No native application and no packaged desktop build.
- The app must stay responsive with 20000 content records across the five divisions and 4000 audit
  entries.

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
identifier is an opaque string and is never parsed for meaning; a timestamp is ISO-8601 in UTC with a
trailing `Z`; a rejected request carries a machine-readable `code`, a human-readable `message` and the
`request_id`; and an unknown field in a request body is refused rather than ignored. Console list
endpoints page by cursor: a paged request takes `cursor` and `page_size` and the response carries
`has_more` and `next_cursor`, the cursor is opaque, and it stays stable while records are being
written. Every write takes an optional `Idempotency-Key`, honoured for 24 hours. Bearer auth is
required on everything except `POST /api/auth/login`, `GET /api/health`, every `GET /api/public/*`
address and `POST /api/public/enquiries`.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/login` | `{ "email", "password" }` | `{ "access_token", "principal_id", "display_name" }` |
| `POST /api/auth/logout` | none | `{ "ok" }` |
| `GET /api/me` | none | `{ "principal_id", "email", "display_name", "memberships" }` |
| `GET /api/health` | none | `{ "status" }` |
| `GET /api/content/records` | optional `division`, `type`, `state`, `cursor`, `page_size` | array of `{ "id", "type", "division_key", "slug", "state", "title", "disclosure_class", "embargo_at", "published_at", "updated_at" }` |
| `POST /api/content/records` | `{ "type", "division_key", "title", "slug", "blocks" }` | the record |
| `GET /api/content/records/{id}` | none | the record plus `{ "current_revision", "published_revision" }` |
| `PATCH /api/content/records/{id}` | `{ "title", "standfirst", "blocks", "credit", "caption", "expected_revision_id" }` | the record, with `current_revision_id` advanced |
| `GET /api/content/records/{id}/revisions` | optional `cursor` | array of `{ "id", "author_principal_id", "created_at", "content_hash", "approved_field_hash" }` |
| `POST /api/content/records/{id}/classify` | `{ "disclosure_class" }` | the record |
| `POST /api/content/records/{id}/media` | the bytes, plus `filename` and `alt_text` | `{ "id", "object_key", "content_type", "byte_size", "sha256", "alt_text" }` |
| `GET /api/media/{mediaId}` | none | the object bytes, to a principal entitled to the record |
| `POST /api/workflow/records/{id}/submit` | `{ "expected_state" }` | `{ "record_id", "state", "submission_id" }` |
| `POST /api/workflow/records/{id}/transition` | `{ "to", "expected_state", "comment" }` | `{ "record_id", "state", "stages" }` |
| `POST /api/workflow/records/{id}/schedule` | `{ "embargo_at", "expected_state" }` | `{ "record_id", "state", "embargo_at" }` |
| `DELETE /api/workflow/records/{id}/schedule` | none | `{ "record_id", "state" }` |
| `POST /api/workflow/records/{id}/publish` | `{ "expected_state" }` | `{ "record_id", "state", "published_at", "route_path" }` |
| `POST /api/workflow/records/{id}/unpublish` | `{ "reason" }` | `{ "record_id", "state", "unpublished_at" }` |
| `GET /api/workflow/inbox` | none | `{ "awaiting_my_decision", "changes_requested_on_my_work", "my_drafts", "watching" }`, each an array |
| `POST /api/workflow/delegations` | `{ "to_principal_id", "role", "division_key", "expires_at" }` | the delegation |
| `DELETE /api/workflow/delegations/{id}` | none | `{ "ok" }` |
| `GET /api/policy/entries` | optional `publication`, `jurisdiction` | array of `{ "id", "reference_code", "title", "version", "effective_from", "effective_until", "publication" }` |
| `GET /api/admin/members` | none | array of `{ "principal_id", "email", "display_name", "is_active", "memberships" }` |
| `POST /api/admin/memberships` | `{ "principal_id", "division_key", "role", "justification", "expires_at" }` | the membership |
| `DELETE /api/admin/memberships/{id}` | none | `{ "ok" }` |
| `GET /api/admin/audit` | optional `actor`, `resource_id`, `action`, `division`, `decision`, `since`, `until`, `cursor` | array of `{ "id", "occurred_at", "actor_principal_id", "on_behalf_of_principal_id", "action", "resource_type", "resource_id", "division_id", "before_hash", "after_hash", "decision", "deny_reason", "request_id", "prev_entry_hash", "entry_hash" }` |
| `GET /api/admin/exceptions` | none | `{ "individual_grants", "active_delegations", "fast_path_publications", "denied_attempts" }` |
| `GET /api/public/counters` | none | `{ "published_releases" }` |
| `GET /api/public/releases` | optional `page`, `division`, `year` | `{ "items", "page", "page_size", "total_pages" }` |
| `GET /api/public/releases/{slug}` | none | `{ "slug", "title", "standfirst", "division_key", "published_at", "blocks", "lead_media_id", "disclaimer", "related" }`, for a published release only |
| `GET /api/public/media/{mediaId}` | none | the object bytes, for media on a published record only |
| `GET /api/public/policies` | optional `jurisdiction` | array of `{ "reference_code", "title", "version", "effective_from" }` |
| `GET /api/public/policies/{referenceCode}` | optional `jurisdiction` | `{ "reference_code", "title", "version", "effective_from", "reviewed_at", "blocks", "change_summary", "previous_versions" }` |
| `GET /api/public/search` | `q` | array of `{ "type", "title", "route_path", "division_key", "published_at", "excerpt" }` |
| `GET /api/public/divisions` | none | array of `{ "key", "name", "wordmark", "primary_colour_role" }` |
| `GET /api/public/offices` | none | array of `{ "city", "country", "jurisdiction", "address_lines", "phone_e164", "phone_display", "reception_email", "latitude", "longitude", "marker_label" }` |
| `GET /api/public/figures` | none | `{ "office_count", "nationality_count", "female_share_global", "female_share_management", "as_at" }` |
| `POST /api/public/enquiries` | `{ "subject_area", "name", "organisation", "country", "email", "phone", "message", "consent", "form_token" }` | `{ "public_reference", "responding_office", "response_window" }` |

**The error catalogue.** A rejected request carries one of these exact `code` values and no other,
because a caller branches on the code rather than on the message:

| `code` | Meaning |
|---|---|
| `unauthorized` | no valid credential was presented |
| `forbidden_permission` | the decision denied the action |
| `not_found` | the resource does not exist, or the caller may not know that it does |
| `gone` | the resource existed and was withdrawn |
| `conflict_version` | the revision or state supplied is not the one stored |
| `conflict_state` | the resource is in a state that forbids this action |
| `validation_failed` | the request is malformed, carrying a per-field list in `details` |
| `rate_limited` | too many attempts, carrying how long until they are accepted again |
| `dependency_unavailable` | a backing service this call needs did not answer |

`not_found` covering "exists, but you may not know that" is deliberate: a distinct denial for a
resource whose very existence is confidential is an enumeration oracle. A request for an embargoed
release's slug, a request for a record on a division the caller does not hold, and a request for a
slug that was never issued all answer `not_found`. `gone` is different and is used only where the
absence is itself the public statement: a withdrawn release. A store error and a stack trace never
reach a caller.

**No mocks.** `PostgreSQL` and `minio` are the fact. An in-memory list of media, a hardcoded object
key the app never writes, a file written to the app container's own filesystem, a data address held in
a block payload, or a `{"ok": true}` response the app returns to itself are each a contract violation
however good the interface looks. The named provider is the fact - the app's UI and its own tables can
only reflect what lives in the provider, never substitute for it.

## Definition of done

A press officer drafts a release, a legal reviewer clears it, a different officer classifies and
clears it, and a publisher schedules it. Until the scheduled instant passes the release is
unreachable at its own address, in the archive, in the search and through its lead image; after the
instant a signed-out stranger reads it with its image served from the bucket. Editing an approved
release's words takes the approvals away again, and nobody approves their own work by holding a
second role or by handing their authority to somebody else.
