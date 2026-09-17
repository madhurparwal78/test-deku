# Lockleaf

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser,
create an account, write a note, sign out, and sign in again from a fresh browser to
find that note intact and readable, without hitting an error page.

The words of that note must never exist in readable form anywhere except the browser
that is showing them: not in the database, not in the object store, not in any request
the browser sends, and not in the sign-in exchange, which never carries the password.
A different stranger, signed in to a different account, must NOT be able to read, list,
overwrite or delete that note by any means. A note the server encrypts for itself with
a key the server holds does not count as sealed.

## Overview

Lockleaf is a private notes application for people who want a place to write that
nobody else can read. Its defining property is that the company operating it cannot
read the notes. Only you have access to the keys required to decrypt your data: every
note, tag, folder, saved view and attached file is sealed on the device before it is
stored, with keys that are made from the account password and never leave the device
in any form.

A person writes notes of several kinds, organises them with tags and nested folders,
pins, archives, trashes and protects them, keeps saved views, attaches files, steps
back through revision history, and moves between devices while every one of them
stays in step. The free plan is real and generous: unlimited notes, unlimited devices,
the full encryption, offline reading, tags, export and protection of single notes are
never paid for. What a paid plan buys is editing richness, history depth and space for
files. The gate is never on the security.

The server is a synchronising store of sealed items with an account system in front of
it. It learns how many items an account holds, of which kinds, roughly how large they
are and when they change. It never learns a title, a body, a tag name, a file name or a
search query. That is the trade the product makes and it says so plainly rather than
promising more: a breach of the server, an employee with database access or a subpoena
to the operator yields ciphertext and metadata and nothing else, while tampering,
substitution and rollback of a stored item are detected rather than obeyed.

This is deliberately **not** a collaboration tool, a publishing tool or a document
server. There is no sharing of notes between accounts, no comments, no server-side
search, no password reset and no support path that can open a note. A marketing
surface exists, and it is small: a home page, a plans page, two principle essays, a
local demo and the account pages.

The genuinely hard part is that every shortcut an ordinary notes app takes is a defect
here that leaves the interface looking correct: a sign-in form that posts the password,
a sync that asks what changed since a clock time and silently drops one note, a later
save that silently replaces an earlier one, an emptied trash that a returning device
quietly resurrects, and an expired card that locks a person out of their own writing.

## User roles

One role. Every account is a person with a vault of their own, and no account can see
into another.

| Role | Can do |
|---|---|
| Account holder | create, read, change, trash and delete their own notes, tags, folders, saved views, files and revisions; manage their own sessions, password, lock, export, import and subscription; invite accounts to share a `Canopy` subscription they own. **Cannot read, list, change or delete any item, file, revision or session belonging to another account, including an account sharing their subscription.** **Cannot recover a forgotten password.** |

A person who owns a shared subscription sees which accounts are on it and can remove
them. **They never see those accounts' notes**, and nothing in the product suggests
they could.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button
in the UI is not authorization: a direct API call from one account's session to any
endpoint acting on another account's items, files, revisions or sessions must be
rejected by the server (an unauthorized request is denied, not served), leaving the
protected state unchanged. An item that belongs to another account is reported as not
found rather than as forbidden, so a request never confirms that it exists.

**Signup is open.** Anyone may create an account at `/signup` with an email address or
a private username.

Seeded accounts, every one using the password `deku-demo-pw-2026`:

| Account | Plan on record | What it holds |
|---|---|---|
| `user@example.com` | `Canopy`, `active`, expiring `2027-03-01`, owner of the shared subscription | the working vault used for most journeys |
| `user2@example.com` | none of its own; a member of the `Canopy` subscription owned by `user@example.com` | a separate vault the owner can never read |
| `user3@example.com` | `Canopy`, `expired` on `2026-06-30` | work made while paid, kept after the subscription lapsed |

## Core features

### Accounts and the password that never leaves the device

The password produces two independent secrets on the device. One is the root key that
opens the vault and never leaves the device. The other is the **authentication secret**,
which is the only thing sent to sign in. Neither can be computed from the other.

1. Creating an account sends the identifier, the authentication secret and the
   account's **key parameters** (the per-account inputs to the key derivation) to
   `POST /api/accounts`. The password itself is never sent, in any request, in any
   encoding.
2. An identifier is an email address or a private username. It is trimmed and
   lower-cased before comparison, and two accounts can never hold the same identifier.
   Uniqueness is compared after that normalisation, and the enumeration defence below
   applies to usernames identically.
   Creating an account with a taken identifier is rejected as invalid.
3. The server stores a slow, salted password hash of the authentication secret and the
   key parameters. It never stores anything from which the root key can be derived.
4. Before signing in, the device fetches the key parameters with
   `GET /api/auth/params`. For an identifier with no account the server returns
   **synthetic** key parameters that carry the same fields as a real account's, are
   identical on every request for that identifier, and differ from one unknown
   identifier to the next, so the response never reveals whether an account exists.
5. Signing in sends the identifier and the authentication secret to `POST /api/sessions`.
   A wrong secret and an unknown identifier are refused with the same outcome and the
   same response body, so a failed sign-in never names which part was wrong. Response
   timing is levelled by a fixed floor rather than by a random delay.
6. **There is no password reset.** No link, route or message offers to reset, recover or
   email a password, because a forgotten password means the vault cannot be opened by
   anyone. The sign-in page instead offers `Start over with an empty vault`, which opens
   `/start-over`.
7. `/start-over` first lists the two real ways back to your notes: an export file you
   saved earlier, and a device that is still signed in. Only then does it offer to
   delete the account and create a new one under the same identifier. Its button stays
   unavailable until the person types exactly `delete my notes forever`, and it is named
   `Delete my vault and start over`: the confirmation
   requires typing the consequence, never merely clicking a checkbox.
8. The signup form states the consequence once, plainly, at the moment the password is
   chosen: `Nobody can recover your notes if you forget this password.`
9. The signup form refuses a password shorter than `12` characters, and a password
   confirmation that does not match, inline beside the field it concerns, and creates
   no account.
10. Changing the password happens at `/settings/password`. The device re-wraps the
    account's items keys under the new root key and submits the new authentication
    secret, the new key parameters and the re-wrapped items keys to
    `POST /api/account/password` together, authorised by the current authentication
    secret. **Either all of it is stored or none of it is.**
11. A password change rewrites no note: every note keeps the version it had, because
    only the small wrapped keys change.
12. A password change ends every other session of that account at once. The session
    that made the change continues with the fresh token it is given.

### Sessions

1. Signing in returns an access `token`, valid for `60` minutes, and a `refresh_token`,
   valid for `30` days.
2. `POST /api/sessions/refresh` exchanges a refresh token for a new access token and a
   new refresh token. A refresh token works exactly once.
3. **Reuse detection: presenting a refresh token that has already been used invalidates
   the whole chain.** The refresh token that replaced it and its access token stop working
   too, because a reused refresh token means a stolen copy has been caught.
4. `/settings/sessions` lists every session of the account with its device, when it
   started and when it was last used, marks the current one, and ends any other one on
   request. An ended session is refused from that moment.
5. Signing out ends the current session. A call carrying its token afterwards is
   refused.

### The sealed item store

Everything a person makes is an item in one list, told apart only by its type.

1. An item carries a `uuid` generated on the device, a `content_type`, a sealed
   `envelope`, a `version` and a `deleted` flag. The server assigns `version`,
   `created_at` and `updated_at`.
2. `content_type` is one of `note`, `tag`, `items_key`, `file`, `revision`,
   `saved_view` or `preferences`. It is the one deliberate fact the server can read,
   because sync, storage and history rules differ by kind. An item of any other type is
   refused as `invalid_type`, so every stored type is one of the known markers.
3. The `uuid` is random, from a cryptographic source, and never sequential, never
   derived from the content and never derived from the device. It stays the same for
   the life of the item, across edits, type changes and export.
4. The `envelope` is opaque to the server. The title, the body, the note type, the tag
   names, the parent folder, the pinned, archived, trashed and protected flags, file
   names and every timestamp a person sees all live inside it.
5. Every envelope is sealed with an authenticated cipher under a fresh random nonce
   for every save, so saving the same words twice produces two different envelopes.
6. The authentication covers the item's `uuid` and the key it was sealed under as
   well as its contents, so an envelope moved into another item, or an older envelope
   put back in place of a newer one, fails to open rather than opening as the wrong
   note.
7. **An item that cannot be opened is shown, never hidden and never shown empty.** Its
   page reads `This note cannot be opened`, names its `uuid`, offers to export the raw
   envelope, and offers no editor that could save over it. An empty note would read as
   a note the person emptied themselves.
8. Every envelope records, inside its authenticated part, the protocol version that
   produced it. The app reads every protocol version it has ever written, writes only the
   current one, and upgrades an item to the current version when that item is next saved,
   never as a bulk pass. A protocol upgrade therefore never rewrites a whole vault.
9. After a suspected compromise a person can rotate the items key from `/settings`: a new
   items key becomes current, new saves use it, and older items stay readable and are
   re-keyed when next saved. Rotation adds a key and never removes one.
10. An `envelope` longer than `2000000` characters is refused as `too_large` and nothing
   of it is stored. It is never truncated.

### Sync

One exchange carries everything in both directions: `POST /api/items/sync`.

1. The device sends its `cursor`, a `limit`, a `request_id` and the `items` it has
   changed, each with the `version` it last saw (none for a new item).
2. The server answers with the `retrieved_items` changed since the cursor, the
   `saved_items` with their new versions, any `conflicts`, a new `cursor`, and `more`,
   which is `true` while further changes remain.
3. **The cursor is an opaque token over a total order of that account's changes, never
   a clock time.** A device stores it and hands it back without reading it. Every item
   written after a cursor is delivered exactly once to a device that keeps following
   `more`, even when many items are written in the same instant and a page boundary
   falls between them.
4. `limit` defaults to `150` and never exceeds `500`. A request carries at most `500`
   items.
5. Each item in a request is accepted or refused on its own. One refused item never
   fails the others.
6. A request replayed with the same `request_id` returns the same answer and changes
   nothing a second time.
7. A device with no cursor receives the whole vault from the beginning. Losing a cursor
   is an ordinary event, not a failure.
8. A device keeps working with the network off: it reads and edits its own sealed copy,
   queues what it changed, and catches up through the same exchange when the network
   returns. Work that has not reached the server is never shown as synced.
9. Ownership is checked on every item in every operation. Only the account's own items are
   ever sent or received. A `uuid` that belongs to
   another account is refused as `uuid_conflict`, reveals nothing about the other item,
   and changes nothing.

### Conflicts and deletion

Detection happens on the server; resolution happens on the device, because the server can
read neither side of a conflict. Server-side deduplication, diffing or merging is impossible
by design.

1. An item submitted with a `version` older than the stored one is a
   `version_conflict`. The stored item stays exactly as it was and comes back in the
   conflict as `server_item`.
2. **The server never merges and a later save never silently replaces an earlier one.**
   The device that received the conflict keeps both: it saves its own words as a new
   note marked as a conflicted copy of the original, carrying the original's tags and
   folder.
3. A conflicted copy is visibly labelled `Conflicted copy` with the device and the time
   that made it, and sorts directly beside its original rather than at the top of the
   list.
4. A conflicted copy offers a side-by-side comparison with its original, and lets the
   person keep one, keep both, or merge by hand.
5. `/notes` offers `Clear identical copies`, which finds conflicted copies whose words
   match their original exactly and removes them in one action after confirmation.
6. Moving a note to the trash is a flag inside its envelope. A trashed note is still an
   item, still syncs and can be restored.
7. **Emptying the trash writes a tombstone rather than removing the row:** the item
   keeps its `uuid`, its `deleted` flag becomes `true`, its `envelope` becomes empty and
   its `version` increases. The tombstone syncs like any other change, so a device that
   was offline learns of the deletion when it returns.
8. A tombstone is kept for at least `90` days.
9. **A deleted note never comes back.** A device that returns with an older version of a
   tombstoned item receives a `version_conflict` carrying the tombstone, and the note
   stays deleted on every device.

### Notes and note types

A note's type is a property of the note, chosen when it is created and changeable
afterwards. Creating a note opens the dedicated route `/notes/new`.

| Note type | Plan |
|---|---|
| `Plain text` | `Leaf` and above |
| `Markdown` | `Leaf` and above |
| `Rich text` | `Branch` and above |
| `Tasks and todos` | `Branch` and above |
| `Code` | `Branch` and above |
| `Authenticator` | `Branch` and above |

1. `/notes/new` carries a `Note type` chooser, a `Title` field and a `Note body` editor,
   and `Create note` seals and saves the note, then opens it at `/notes/<uuid>`.
2. An unsaved buffer survives a forced quit or a crash: the words are kept on the device as
   a draft before they become a saved note or a revision.
3. A note saves itself as the person writes, settling before it saves rather than on
   every keystroke, and saves at once when the page loses focus or is closed. Its
   status line reads `Saving` while a save is in flight and `All changes saved` once the
   sealed copy is stored on the server.
4. Every note type can render itself as plain text, and that plain rendering is always
   available: in export, on a device without the richer editor, and after a
   subscription lapses.
5. Every editor, including `Tasks and todos` and `Authenticator`, can be driven
   entirely from the keyboard.
6. `Authenticator` notes hold the setup secrets that produce sign-in codes for other
   services. They are protected by default, and a plain export leaves them out unless
   the person confirms their inclusion separately.
7. Changing a note's type first shows what the conversion will lose, then writes a
   revision of the content as it was, and never drops content silently.
8. A person on `Leaf` is offered only the `Leaf` types when creating a note. Notes
   already written in a paid type always open, read and edit in their own editor.

### Tags, folders and saved views

1. A tag is an item with a name and an optional parent tag. **A folder is a tag with a
   parent**; there is no second hierarchy.
2. A note belongs to any number of tags.
3. Two tag names that differ only by letter case or by an equivalent spelling of the same
   characters are the same tag.
4. Nesting a tag under another is a `Branch` feature. A person on `Leaf` can still open
   and move through folders they made while paid, and is told plainly that new nesting
   needs a paid plan.
5. Two devices can each move a folder inside the other while offline. When that loop
   arrives, the app repairs it by lifting one folder back to the top level, and says so.
   It never hangs, spins or hides either folder.
6. Deleting a tag removes the tag, moves its child tags up to its parent, and never
   deletes a note.
7. A saved view is an item holding a query over a closed set of conditions: title
   contains, tag is, note type is, edited within a number of days, and the pinned,
   archived and protected flags. It is evaluated on the device every time it is shown.
8. A saved view that cannot be evaluated shows `This view cannot be evaluated` with its
   reason, never an empty list.

### Pin, archive, trash and protect

Pinning, archiving and protecting are three different things, and all three are flags inside
the sealed envelope, never columns the server can read.

1. A pinned note sorts to the top of every list it appears in.
2. An archived note leaves `/notes`, stays searchable, and is listed at `/archive`.
3. A trashed note leaves every list except `/trash`, and can be restored from there.
4. A protected note shows `This note is protected` in place of its words, and shows
   them only after the account password is entered again.
5. The app says honestly that protection hides a note from someone looking over your
   shoulder and is not a second lock on the data.

### Search

1. Search runs on the device over the words it has already unsealed: titles, bodies, tag
   names and file names.
2. **A search query never leaves the device**, in a URL, a request body, a log line or
   anything else.
3. The search field is labelled `Search notes` and narrows the note list as the person
   types, matching regardless of letter case.
4. The device's own search index is sealed on disk like everything else, and a device
   that is still building it shows its progress and falls back to a slower full scan
   rather than returning wrong results.

### Revision history

1. A revision is an item of type `revision`: a whole sealed copy of a note at a moment,
   never a difference from the one before, so one damaged revision never spoils the
   others. Storing revisions as deltas is not acceptable.
2. The device makes revisions as a person writes, gathering edits that land close
   together into one revision.
3. `/notes/<uuid>/history` lists a note's revisions newest first, each with its time,
   and restoring one saves it as the note's newest content.
4. Revision history differs by plan, and the server enforces what reaches it:

| Plan | History |
|---|---|
| `Leaf` | `Current session only`: revisions live on the device for the current editing session and are not synced. A `revision` item sent from a `Leaf` account is refused as `plan_limit`. |
| `Branch` | `365 days`: revisions sync, and those older than `365 days` are removed. |
| `Canopy` | `Unlimited`: revisions sync and are never removed. |

5. Pruning runs on the device, which alone knows a revision's real time, with the server
   pruning on its own `created_at` as a backstop; the two agree on the boundary so a
   revision never appears on one device and vanishes on another.
6. **Nothing is ever removed from the revision history of an account whose subscription
   has lapsed.** Its existing revisions stay readable indefinitely.

### Encrypted files

1. A file is attached to a note and is sealed on the device in chunks of at most
   `4194304` bytes each, each chunk authenticated together with its position and with
   whether it is the last one, so chunks cannot be reordered, repeated or cut off the end
   without the file failing to open.
2. Uploading happens in two steps. `POST /api/files` records the file as `pending` with
   its `chunk_count`, under the same `uuid` as the file's own item of type `file`; each chunk is sent to `PUT /api/files/<uuid>/chunks/<index>`; and
   `POST /api/files/<uuid>/complete` marks it `complete` only when every chunk from `0`
   to one less than `chunk_count` is stored. A file missing a chunk cannot be completed.
3. Sealed chunks are stored in `minio` in the bucket named by `STORAGE_BUCKET`, under the
   key `vault/<file uuid>/<chunk index>`, for example
   `vault/0f8c2a3e-6b1d-4e7a-9c55-2d7e41b09a13/0`. File bytes are stored nowhere else: not
   on the app's own disk and not in the database.
4. A chunk is readable only by the account that owns the file, through the authenticated
   endpoint `GET /api/files/<uuid>/chunks/<index>`. A request from any other account is
   answered as not found.
5. A dropped upload resumes from the first chunk not yet stored, rather than starting
   again.
6. Downloading is streamed: chunks are fetched and decrypted in sequence and never assembled
   whole in memory. The download shows an image as it opens,
   and stops with a visible error the moment a chunk fails to authenticate.
7. Attaching files is a `Canopy` feature. A request to start an upload from an account
   whose effective plan is not `Canopy` is refused as `plan_limit` and stores nothing.
8. **Storage is counted in sealed bytes**, the bytes actually stored including each
   chunk's overhead. `GET /api/account/storage` reports `used_bytes` and `quota_bytes`,
   and the figure a person is shown is the same figure the limit is enforced against.
9. `Canopy` includes `100 GB` of storage, reported as a `quota_bytes` of `107374182400`. An upload that would pass the quota is refused
   before it starts and again at completion.
10. **An account over its quota, or no longer entitled to files, can always open and
    download every file it already has.** Only new uploads stop.
11. An orphan sweep reaps chunks with no file and pending uploads with no chunks, on a
    schedule, acting only on records older than `90` days so it never races a slow upload.
12. Previews of images are made on the device the first time the file opens and are
    never uploaded.

### Plans, subscriptions and sharing

| Plan | Price | What it adds |
|---|---|---|
| `Leaf` | `Free` | unlimited notes, unlimited devices, full encryption, offline reading, tags, protected notes, full export in sealed or plain form |
| `Branch` | `$36.00` a year, `3600` in integer minor units of `usd` | the `Rich text`, `Tasks and todos`, `Code` and `Authenticator` note types, nested folders, `365 days` of revision history |
| `Canopy` | `$96.00` a year, `9600` in integer minor units of `usd` | everything in `Branch`, `100 GB` of encrypted file storage, `Unlimited` revision history, sharing the subscription with up to `5` accounts in total |

1. `GET /api/account/subscription` reports the account's own `plan`, its `status` of
   `active` or `expired`, its `expires_at`, and its `effective_plan`.
2. The `effective_plan` is the account's own plan while that is `active`; otherwise
   `Canopy` while the account is a member of an `active` shared `Canopy` subscription;
   otherwise `Leaf`.
3. The subscription carries an `entitlement`: a signed token in three dot-separated parts
   whose middle part is the base64url JSON of `identifier`, `plan`, `expires_at` and
   `features`. The entitlement is refreshed before expiry, with a grace window so a network
   problem is never a downgrade. `POST /api/entitlements/verify` answers `valid` `true` for a token the
   product signed and `false` for any token whose parts have been altered.
4. **What costs money is enforced on the server**: file storage, the storage quota and
   revision history. What changes the interface is a courtesy on the device: which note
   types are offered and whether a folder can nest.
5. **Expiry restricts what can be newly done and never removes access to what was already
   made.** After a lapse, notes in paid types still open, read, edit and export; nested
   folders stay and stay navigable; files stay downloadable; revisions stay; and
   `Authenticator` notes keep working, because they hold the codes that open other
   services.
6. The owner of an `active` `Canopy` subscription invites another account by identifier
   with `POST /api/subscription/invitations`. The invitation is `pending` until the
   invited account accepts it, and expires after `7` days.
7. **Sharing shares the subscription and nothing else.** Every member keeps their own
   account, their own password, their own keys and their own sealed vault. The owner
   sees each member's identifier and can remove them, and can never reach a member's
   items, files or revisions by any path.
8. A shared subscription never holds more than `5` accounts including the owner. An
   acceptance that would pass that number is refused.
9. A removed member's effective plan returns to their own plan or to `Leaf`, and they
   keep everything they made.
10. Purchasing is not part of this product: no card is taken and no checkout exists. A
    subscription exists as a recorded plan, status and expiry.

### Lock

1. A person may turn on a lock for the device at `/settings/lock` by choosing a passcode
   of at least `6` digits in the fields `Passcode` and `Confirm passcode` and choosing
   `Turn on lock`.
2. `Lock now` in the sidebar locks the app at once and opens `/locked`.
3. **Locking discards every key and every unsealed note from the page**, rather than
   covering them. While locked, no note title or body is present in the page.
4. Entering the passcode in the `Passcode` field at `/locked` and choosing `Unlock` returns to where the person
   was. A passcode path always exists; nothing about unlocking depends on a fingerprint or
   a face.
5. Locking never interrupts a save that is already under way.

### Export, import and leaving

1. `/settings/export` produces the whole vault as one file, in one of two forms. The sealed
   form holds every envelope exactly as stored. The plain form holds readable notes, tags,
   saved views, preferences and revision history, and opens in any text editor.
2. Choosing the plain form warns once, plainly, that the file is not sealed.
3. The export is one file. When files make it exceed a size threshold, the archive is split
   and the parts are named in sequence.
4. The export format is documented on the export page, versioned and stable, and names
   anything it leaves out.
5. `/settings/import` reads an export file on the device, never on the server. Before
   anything is written it shows how many notes, tags and files the file holds and what
   will not survive.
6. **Importing adds and never overwrites.** Imported items receive new identifiers, and
   items the account already holds with the same words are offered as skippable
   duplicates.
7. Importing a sealed export asks for the password that made it, and says plainly that the
   current password will not open an older file.
8. `/settings/delete` deletes the account after offering the export in the same flow and
   requiring the account password and the typed words `delete my notes forever`. It
   removes every item, revision, file and session, retains only the minimum billing
   records the law requires and names them explicitly in the flow, and ends on its own full-page
   confirmation. The request is `DELETE /api/account`.
9. After deletion, signing in with the old identifier is refused exactly as an unknown
   identifier is, and the identifier is free for a new account.

### The public site and the demo

1. `/` is the home page, `/plans` compares the three plans, `/privacy` carries the essay
   `Stand For Privacy`, `/longevity` carries the essay `Built to Last`, and `/demo` is
   the live demo.
2. The demo runs the real editor, with the same `Title` and `Note body` fields, and the real
   note types on the device with a throwaway key,
   creates nothing on any server, and says `Nothing you write here is saved.` when it
   opens and again when the person leaves it.
3. An address matching no route renders the product's own not-found page, headed
   `We can't find that page.`, with links back to the home page, the plans page, the
   privacy essay and sign in, and answers with a not-found result rather than a success.
4. Every public route carries its own document title and its own meta description, and no
   two public routes share either.
5. Every public route declares a social preview title and a preview image, and the preview
   image address resolves. The image is drawn by the app, never a shipped file.
6. Every internal link on every public route resolves. A link that leaves the site is
   marked as leaving it and opens in a new context.
7. Every form rejects invalid input inline, names the field that is invalid, and writes
   nothing.

## User flow

The information architecture is a public site, then one authenticated app with a
persistent sidebar: `All notes`, `Archive`, `Trash`, the folder tree, `Saved views`,
`Files`, `Settings` and `Lock now`.

| Route | Purpose | Auth |
|---|---|---|
| `/` | home page | public |
| `/plans` | the three plans and the comparison table | public |
| `/privacy` | the essay `Stand For Privacy` | public |
| `/longevity` | the essay `Built to Last` | public |
| `/demo` | the local live demo | public |
| `/signup` | create an account | public |
| `/sign-in` | sign in | public |
| `/start-over` | delete the vault and start again under the same identifier | public |
| `/notes` | every note that is not archived or trashed, as a table | authenticated |
| `/notes/new` | create a note | authenticated |
| `/notes/<uuid>` | read and edit one note | authenticated |
| `/notes/<uuid>/history` | the note's revisions | authenticated |
| `/archive` | archived notes | authenticated |
| `/trash` | trashed notes, restore and empty | authenticated |
| `/tags/<uuid>` | the notes under one tag or folder | authenticated |
| `/views/new` | create a saved view | authenticated |
| `/views/<uuid>` | the notes matching one saved view | authenticated |
| `/files` | every attached file with its sealed size and the storage figure | authenticated |
| `/settings` | the account | authenticated |
| `/settings/sessions` | sessions and ending them | authenticated |
| `/settings/password` | change the password | authenticated |
| `/settings/lock` | turn the lock on or off | authenticated |
| `/settings/subscription` | plan, expiry, sharing and invitations | authenticated |
| `/settings/theme` | choose a theme | authenticated |
| `/settings/export` | export the vault | authenticated |
| `/settings/import` | import an export file | authenticated |
| `/settings/delete` | delete the account | authenticated |
| `/locked` | the lock screen | authenticated |

**Entry and redirects**

An unauthenticated request for an app route goes to `/sign-in`, and after signing in the
requested route opens; with no held route, signing in lands on `/notes`. The sign-in form
carries `Email`, `Password` and a `Sign in` button; the signup form carries `Email`,
`Password`, `Confirm password` and a `Create account` button. `Sign out` sits in the
settings menu, ends the session and returns to `/sign-in`, and going back in the browser
never restores a signed-in screen. An expired access token is renewed with the refresh
token without interrupting the person; when renewal is refused the action writes nothing
and the app returns to `/sign-in`. While the lock is on, every app route opens `/locked`
until it is unlocked. Changing the password, exporting, importing and deleting the account
each end on their own full-page confirmation that says what happened and offers the next
step.

**Journeys**

1. Open `/signup`, create an account, and land on an empty `/notes` that says there are no
   notes yet and offers `New note`. Create a `Plain text` note titled `Harbour lights`, wait
   for `All changes saved`, sign out, sign in again in a fresh browser, and open
   `Harbour lights` to read its words.
2. Sign in as `user@example.com`. The note table lists `Grocery run` first because it is
   pinned. Open the folder `Finance`, then `Taxes`, and open `Quarterly taxes`.
3. Open `Quarterly taxes`, open its history, and read its `3` revisions, newest first.
4. Type `renewal` into `Search notes`: the table narrows to `Passport renewal`. Open the saved
   view `Renewals` and see the same note.
5. Open `Passport renewal`: it shows `This note is protected`. Enter the account password
   and read it.
6. In the note table, find `Packing list` with its `Conflicted copy` directly beside it,
   labelled with the device `Kitchen tablet`, and open the comparison.
7. Move `Old wifi password` from `/trash` to deletion by emptying the trash; it is gone from
   every list.
8. Open `/files`: `lease-scan.pdf` is listed with its sealed size beside the storage figure.
9. Sign in as `user3@example.com`. The subscription page shows `Canopy` expired on
   `2026-06-30`. Open `Loan agreement` in the folder `Legal` inside `Contracts`, read and edit
   it; open `Bank login codes`; try to nest a new folder and be told that new nesting needs a
   paid plan.
10. Sign in as `user@example.com`, open `/settings/subscription`, and see `user2@example.com`
    listed as a member with a statement that members' notes are never shared.
11. Sign in as `user2@example.com` and see `Surprise party plan` and none of
    `user@example.com`'s notes.

**States**

Every list has an empty state that says what is missing and offers the action that fills it:
`/notes`, `/archive`, `/trash`, `/files`, a tag, a saved view and the sessions list. A saved
view that matches nothing says so, and a saved view that cannot be evaluated says that
instead, so the two are never confused. Every page has a loading state, and while a vault is
first unsealing after sign-in the app shows its progress rather than an empty table. A
failed save shows a banner in place, keeps the words on screen and keeps them queued. A
failed sync shows how many changes are waiting. Errors never replace the app with a crash
page.

## UI/UX notes

Somebody arriving should understand at once that this is a quiet, serious place to write,
built by people who take privacy literally. The register is operational inside the app,
where people write and find things again, and editorial on the public pages, where the
argument is made in plain sentences. There is no feeling to manufacture: trust comes from
restraint, plain wording and nothing moving during a decision.

**Palette by role.** Four colours do nearly all the work, and a build that gets them right
is most of the way there. Reading text is a deep cool neutral, and it is what almost every
paragraph wears. Headings take a near-black neutral, the strongest text on any page. The
page ground and every card are a near-white neutral. One mid, vivid blue carries everything
a person can click or that is active, and nothing that cannot be clicked wears it. The
pressed state of that blue is a deep, soft blue.

The page alternates, band after band, between the near-white neutral ground and a paler,
near-white cool neutral band, with a second near-white cool neutral kept for the rare inset.
**A card sits only on the pale band, never on the plain ground**, with a hairline border in a
near-white cool neutral and no shadow. Success is a mid, vivid teal and failure is a light,
vivid red, and each always carries a word or a mark beside its colour.

The one accent is a mid, vivid orange, and it has exactly two jobs: the rule beneath a
navigation link while the pointer is over it, and the rule under the phrase naming the
encryption in the home page's opening sentence. It never colours text, a badge, a warning or
a plan. A light, soft cyan appears only as small decorative dots, and a light, vivid orange
tints one drawn illustration and nothing else. The exact shades are yours so long as those
roles and exclusions hold.

**Type.** One freely licensed geometric grotesque family carries everything, used at four
weights: regular for reading, medium for interface labels, bold for headings and controls,
and the heaviest for the one page title per page. Reading text is set generously but with
tight leading on short lines; any paragraph longer than a few lines relaxes its leading so
the essays read comfortably. Figures line up wherever sizes and dates stack in a column. Every time a person sees is
displayed in the reader's own time zone, from the absolute instant stored inside the envelope.

**Shape and density.** No radius is shared by accident: controls are barely softened, cards and panels a little more, theme
swatches almost square, and every icon sits on a fully round, lightly tinted disc in its own
hue. The app is compact: a full note table reads on one screen. The public pages are
spacious, with sections reading as separate at a glance without a dividing line.

**Motion.** Movement is modest, eased and uniform. Pointer feedback settles in about a fifth
of a second and eases out; a panel swap is a touch quicker; content that arrives because a
person asked for it fades while rising a short distance, once. Nothing animates on scroll,
nothing moves during a decision, and transitions name the property they change rather than
moving everything at once. The theme chooser's demonstration panel changes its ground slowly
on purpose. The one continuous motion is the carousel of uses on the home page, and it pauses
while pointed at or focused. Under a reduced-motion preference every state change still
happens and still completes, but instantly; the carousel stops; disclosures open without
transition; nothing fades or rises.

**Components.** Every control has resting, pointed-at, pressed, focused and unavailable
states, and unavailable is never signalled by colour alone. Links carry no underline at rest
and underline when pointed at. Buttons come filled or outlined, and on any page a filled
button means the one recommended action. Escape closes any overlay. Emptying the trash,
deleting a tag, starting over and deleting the account confirm before acting.

**Mode.** The public site has one light appearance and follows no system preference. The app
offers themes as a deliberate choice: `Paper`, the light default, `Midnight`, a dark theme,
and `Sepia`, a warm reading theme. The chosen theme is a synced, sealed preference. A theme
that fails to load falls back to `Paper` and says so.

**Accessibility floors**, which do not vary with the theme: body text meets the WCAG AA
contrast ratio of `4.5:1` against its ground in every theme; the clickable blue is used for
text only at larger sizes, and smaller text uses the pressed-state blue; every touch target is
at least `44` by `44` pixels; keyboard navigation reaches every control with a visible focus
ring in the brand blue drawn with a gap from the control; every icon-only control carries a
label; meaning is never carried by colour alone; each route has one banner, one main landmark
and one footer; a skip link is the first focusable element and appears on focus; the page
declares its language; and every page stays usable at twice the normal zoom without scrolling
sideways, except the plans comparison table.

**Responsive.** The layout is mobile-first rather than desktop-first, built for the narrow screen first and holds at every width
between the phone, tablet and desktop tiers rather than only at them. On a phone the app's
sidebar folds into a menu and each note table row becomes a stacked card carrying the same
fields with their labels. Nothing overflows sideways at any viewport width, and every
navigation target stays reachable.

**What this must not look like.** Not a page dominated by one hue family with no second
signal, not decoration standing in for content, not a card floating on the plain ground, and
not a lock screen that covers words still sitting in the page.

## Technical requirements

Server-rendered multi-page application. The backend is `Express` with `Nunjucks` templates;
the browser layer is vanilla progressive enhancement: plain scripts and the platform's own
cryptography interface enhance server-rendered pages, with no client framework. Storage is
PostgreSQL, reached at `DATABASE_URL`. File chunks live in `minio`, reached at
`STORAGE_ENDPOINT` in the bucket `STORAGE_BUCKET` with `STORAGE_ACCESS_KEY` and
`STORAGE_SECRET_KEY`. Authentication is app-implemented with bearer tokens.
`GET /api/health` returns `200` once the app is ready. Request lines go to stdout.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing
services available in this environment are PostgreSQL and `minio`, and reaching for anything
else is a contract violation.

PostgreSQL and `minio` are **already running** and reachable at their environment variables.
Do not download, install, compile or start a copy of either.

The observable consequence of the rendering model: every route arrives as complete HTML for
its page structure, headings, navigation and copy, so a public route is fully readable with
scripting turned off. Note words cannot be rendered by the server, because the server holds
nothing readable; the page's own script unseals them on the device and fills them in.

**Where keys live.** No key capable of opening a note, a tag, a view or a file exists outside
the account holder's own device, in any form: not in the database, not in the object store,
not in memory on the server, not in a log, not in a backup and not in any response.

The cryptographic primitives are the builder's choice so long as these properties hold.
The key derivation from the password is memory-hard, with its parameters stored per account
so they can be raised later without breaking older accounts. The password makes a root key;
the root key wraps the account's items keys; the items keys seal every item. Items keys are
themselves items of type `items_key`, and an account may hold several, so an item sealed under
an older key still opens after a newer one becomes current.

Every comparison of a token, a hash or a secret on the server takes the same time whether it
matches or not, and a failed sign-in takes no less time than a successful one.

Randomness for identifiers, nonces and keys comes from the platform's cryptographic source.

No log line, error report or response ever contains a password, an authentication secret, a
token, a key, an envelope's contents, a search query, a note title, a tag name or a file name.
There is no third-party crash reporter and no third-party analytics; any telemetry is
self-hosted, carries no value derived from content, and honours an opt-out everywhere.

Encrypting without authenticating is not acceptable: every seal is authenticated, and
every write-bearing request is safe to replay, which is what idempotency means here.

No secret the server holds, including the storage access key, the storage secret key and the
database password, appears in any page, script or style the browser downloads.

The client refuses to send anything to a host over plain transport unless that host is the
same origin it was served from.

There is no outbound network at run time.

## Data model

Seven tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data,
not a secret. Hash it as normal; the exact literal must work at login, and it must be written
into `/app/USER_README.md` alongside each account so a grader can sign in.

Because that password is fixture data, the seeded vaults may be sealed once at first start by
the same sealing a device performs, using keys made from it. After seeding, nothing readable of
any seeded note, tag, view or file name remains anywhere on the server.

**accounts** - `id`, `identifier` unique after trimming and lower-casing, `auth_hash`,
`key_params`, `created_at`. `key_params` is stored exactly as the device supplied it.

**sessions** - `id`, `account_id`, `device`, `created_at`, `last_used_at`, `revoked_at`
nullable. Token values are never stored in readable form.

**items** - `uuid` unique, `account_id`, `content_type`, `envelope`, `version`, `deleted`,
`created_at`, `updated_at`. No column of this table holds a title, a body, a tag name, a file
name or a flag other than `deleted`; everything a person typed or chose lives in `envelope`.
`content_type` is one of `note`, `tag`, `items_key`, `file`, `revision`, `saved_view` or
`preferences`.

**file_uploads** - `file_uuid` unique, `account_id`, `chunk_count`, `stored_bytes`, `status`,
`created_at`. `status` is `pending` or `complete`.

**subscriptions** - `id`, `owner_account_id`, `plan`, `status`, `expires_at`. `plan` is
`Branch` or `Canopy`; `status` is `active` or `expired`.

**subscription_members** - `subscription_id`, `account_id`, `joined_at`, `removed_at`
nullable.

**invitations** - `id`, `subscription_id`, `identifier`, `status`, `expires_at`. `status` is
`pending`, `accepted` or `expired`.

### Invariants, stated as properties of the running system

- No text, JSON or character column of any table ever contains the words of a note, a tag, a
  saved view or a file name, in plain form or in a reversible encoding of it.
- An item belongs to exactly one account, and nothing about it is ever returned to another.
- Every item written after a cursor is delivered exactly once to a device that follows `more`
  from that cursor.
- A stored item's `version` only increases, and a write carrying an older version changes
  nothing.
- A tombstoned item stays tombstoned: no later write carrying an older version restores it.
- A password change either stores the new authentication secret, key parameters and wrapped
  items keys together or stores none of them, and it changes the version of no note.
- A refresh token is accepted at most once, and a second presentation ends the session it
  belongs to.
- The storage figure an account is shown equals the sum of the sealed bytes stored for its
  files, and it is the figure its quota is enforced against.
- A shared subscription never holds more than `5` accounts.
- An account whose subscription lapsed loses no item, file or revision.

### Seed data

Three accounts as listed under `## User roles`. `user@example.com` owns the `Canopy`
subscription, `active` until `2027-03-01`, and `user2@example.com` is its member.
`user3@example.com` holds a `Canopy` subscription `expired` on `2026-06-30`.

`user@example.com` holds four tags: the folder `Finance`, the folder `Taxes` nested inside
`Finance`, and the flat tags `Errands` and `Documents`. It holds these notes:

| Title | Type | Placement | Words |
|---|---|---|---|
| `Grocery run` | `Plain text` | tag `Errands`, pinned | `Oat milk, lemons, rye bread, coffee filters.` |
| `Quarterly taxes` | `Markdown` | folder `Taxes` | `Estimated payment is due on the fifteenth.` |
| `Passport renewal` | `Rich text` | tag `Documents`, protected | `Book the photo appointment before the form expires.` |
| `Packing list` | `Tasks and todos` | none | `Charger`, `Rain jacket` |
| `Router notes` | `Code` | archived | `admin panel lives on the second port` |
| `Old wifi password` | `Plain text` | trashed | `harbour-guest-2019` |

`Quarterly taxes` has `3` revisions. `Packing list` has one conflicted copy, labelled as made on
the device `Kitchen tablet`, whose tasks are `Charger` and `Passport`. The saved view `Renewals`
matches notes whose title contains `renewal`. The file `lease-scan.pdf` is attached to
`Passport renewal` and stored as `2` chunks.

`user2@example.com` holds one note, `Surprise party plan`, of type `Plain text`, with the words
`Keep the cake order secret until Saturday.`

`user3@example.com` holds the folder `Legal` with the folder `Contracts` nested inside it; the
note `Loan agreement` of type `Rich text` in `Contracts`, with `2` revisions and the words
`Repayments begin in October at the agreed rate.`; the note `Bank login codes` of type
`Authenticator`; and the file `contract-draft.pdf`, attached to `Loan agreement` and stored as
`1` chunk.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

The visual specification the product carries, in full. Values are described rather than given;
the relationships are the requirement.

**Tokens, named by role.** Fifteen colour roles, four radii, four spacing steps and four motion
roles, each named for what it does rather than for its value, so a value can change without its
name lying. Anything a component needs outside that set is a request to extend the set, not a
local value. The palette has no duplicates: one token per role, no two names for one colour, no
two near-identical greys, and no token whose value is a keyword.

**Spacing.** One base unit and a four-step scale built on it. Section padding is generous on a
wide screen and collapses to the smallest comfortable gutter on a phone. Full-bleed bands may run
very wide; text never runs wider than about seventy characters to a line.

**Marks.** A single-glyph mark in a rounded square, stroked rather than filled, in the brand blue,
beside the wordmark `Lockleaf` in the bold weight. No second mark sits in the lock-up.

**Icons.** Twelve line icons drawn as strokes on one small square grid with round caps and round
joins, in the current text colour: a clock for revision history, an envelope, a shield, a folder,
a key, a lock, a check, a chevron, a search glass, a tag, a trash can and a pin. Each sits on the
icon well: a fully round disc in the icon's own hue at low strength, with the icon at full
strength. The well is one component with one colour input, not twelve tinted pictures. Two
further shapes are drawn exactly as simple paths: a small downward dropdown arrow in the reading
text colour, and a five-pointed rating star.

**The hatched motif.** The site's one decorative idea is drawn, never shipped as a file: fine
parallel diagonal hatching in the hairline border colour, clipped to a rotated square (the dashed
diamond), to a disc (the dashed circle, at three sizes, some turned a quarter turn), and to a band
(the dashed separator between sections and between the plan cards). It appears at low emphasis in
page corners and section margins, at higher strength in separator bands, and is accompanied by
two small solid dots in the light, soft cyan placed asymmetrically so the hatched shapes read as a
constellation rather than a texture. The smallest ornaments are dropped on a phone.

**The one shadow.** Cards have borders, not shadows. The single exception is the drawn panel beside
the `Who is Lockleaf?` band on the home page, which carries one very soft, offset drop shadow to lift
it off a flat ground.

**Header.** At the top of a public page: the mark, then `Plans`, `Stand For Privacy`,
`Built to Last`, then `Go to web app` with a trailing arrow. After any scroll a filled
`Start for free` button appears between the links and `Go to web app`; its space is reserved from
the start so the row never shifts when it fades in. The current route's link is underlined. Below
the tablet width the links fold behind a menu button.

**Footer.** The public chrome closes with three columns on a wide screen and three
accordions on a phone: `Product` with `Plans`
and `Try live demo`; `Principles` with `Stand For Privacy` and `Built to Last`; `Account` with
`Sign in` and `Create account`. An accordion announces whether it is open, and a closed panel is
removed from the reading order and from focus. It never collapses by scaling its height to
zero, because a panel squashed that way stays announced while invisible. With every
accordion collapsed, a screen reader announcing the footer reads only the three column titles.

**The home page**, in bands alternating the plain and the pale ground:

| Band | Contents |
|---|---|
| Hero, plain ground | the title `Free your mind.` in the heaviest weight, centred; one claim sentence, `Lockleaf is a free, private notes app with end-to-end encryption and sync across unlimited devices.`, with the words `end-to-end encryption` ruled beneath in the accent; two filled buttons side by side, `Start writing for free` and `Try live demo`; dashed diamonds, dashed circles and two cyan dots in the margins |
| Vault panel, plain ground | a wide drawn panel: a deep blue field, the hatched motif at low strength, and a centred stroked vault glyph in the brand blue, with a blue rule beneath it |
| Security claim, pale ground | heading `A steel vault for your mind.`, the paragraph `Lockleaf protects your notes and files with end-to-end encryption. Only you have access to the keys required to decrypt your data.`, and the link `See the plans` |
| Uses carousel, pale ground | sixteen chips moving in one continuous row, in this order, from the mundane to the most private: `Markdown`, `Rich text documents`, `Budgets and personal finance`, `Tasks and todos`, `Code snippets`, `Passwords and keys`, `Outlining and lists`, `Family records and documents`, `Health records`, `Journaling and diary`, `Secure file storage`, `Passport and ID photos`, `Bank account and credit card numbers`, `Legal contracts and agreements`, `Confidential business contracts and agreements`, `Private photos and videos` |
| Fearless claim, plain ground | heading `Write fearlessly.`, a paragraph saying that notes the company can read can also be read by whoever compels or breaches the company, and the link `Read how we protect your data` to `/privacy` |
| Durability claim, pale ground | heading `Your notes and files, always.` with its first word carrying the accent treatment inside one heading, a paragraph on offline copies and sync, and the link `View our plans` |
| Harms claim, plain ground | heading `Take back your data.`, one paragraph naming leaks, doxing, fraud and identity theft with two phrases in bold, and the link `Read our longevity statement` to `/longevity` |
| Start band, pale ground | heading `Start your vault`, the line `Unlimited notes, unlimited devices, all for free.`, one filled button `Create account`, and the follow-up `Want more?` with the link `Learn about our plans` |
| Who is Lockleaf, plain ground | heading `Who is Lockleaf?`, two short paragraphs on software sustainability and ethical data practice, and the drawn panel carrying the site's one shadow |

The carousel moves at one constant speed at every width, pauses while pointed at or focused,
stops under a reduced-motion preference, and is marked decorative with the same sixteen strings
present as a static list for anyone not seeing it move.

**The plans page.** Title `Plans`. Three cards, staggered so the recommended one stands tallest,
with dashed vertical separators between them:

| Card | Name | Price | Heading above the list | Action |
|---|---|---|---|---|
| 1 | `Leaf` | `Free` | `You'll have` | `Start for free`, outlined |
| 2 | `Branch` | `$36.00 / year` | `Everything in Leaf plus` | `Go Branch`, outlined |
| 3 | `Canopy` | `$96.00 / year` | `Everything in Branch plus` | `Go Canopy`, filled |

The third card carries a filled star before its name and renders its name and price in the brand
blue. **Exactly one button on the page is filled, and it is the recommended plan's.** Feature lines
are prefixed by a check in the icon well. All three actions lead to `/signup`.

Below the cards, `Compare features` begins with a `Plan Summary` row of one sentence per plan:
`Our way of contributing our privacy-preserving solution to society at large.` for `Leaf`,
`Unlocks the full potential of Lockleaf. Ideal if you're not using files.` for `Branch`, and
`Offers 100 GB of encrypted storage for your photos, documents, and videos.` for `Canopy`. Then
five topic groups: `Styling`, `Note types`, `Security`, `Note history` and `Other features`. A cell
is either a check mark or a text value; the `Note history` row reads `Current session only`,
`365 days` and `Unlimited`. A bar carrying the three plan names and prices pins to the top of the
viewport while the table scrolls beneath it, and its three columns stay aligned with the table's
three columns at every width. The table's own header row stays in the table. On a phone the cards
stack one per row, never two across, and the table scrolls sideways inside its own container with
the feature column held in place.

**The principle pages.** Each is built from headings and paragraphs alone: a title of three or four
words with no punctuation, one or two short opening paragraphs stating the belief, one hinge line
introducing a list, four or five items each a bold sentence-long heading followed by a paragraph,
and a closing `Read More` heading with two links. The voice is first person plural, in short
declarative sentences, and at least one item states a limitation rather than a benefit. Inline links
are the same size and weight as the prose around them, in the brand blue, underlined only when
pointed at.

- `/privacy`: title `Stand For Privacy`; opening `We believe the Internet should do a simple thing: Keep your private information private.`; hinge `Here's how we do it:`; item headings `End-to-End Encryption:`, `Independently Audited:`, `Open:`, `No tracking or intrusive analytics.` and `No third-party email services.`
- `/longevity`: title `Built to Last`; opening `We believe in building software that lasts.`; hinge `And this is how our applications will survive the apocalypse.`; item headings include `We are complexity bigots.` and `We say no to most feature requests.`, the second argued for a full paragraph. Its second
  paragraph reads `To us, it is sad to consider that in the Information Age, the chances are that all information will probably not be there tomorrow. The software that enables all of our thoughts and dreams is now built to such a low standard and at such breakneck speeds and aimed at such ludicrous commercial interests, that its very survivability is in question.`
  The first item's paragraph reads `We don't merely hate complexity in software: we detest it. Fussy code decreases its durability. It forces users to alter habits for no reason. Clutter makes code obsolete before it's finished and it makes it impossible to adapt. Complexity creates user problems, it introduces bugs, and decreases performance. It's also expensive. Simplicity is the one and only future.`

**The not-found page** carries the full header and footer, the heading `We can't find that page.`, the
line `You may have mistyped the address, or the page may have moved.`, and four links onward. No
status code appears in the heading.

**Inside the app.** The sidebar sits on the pale ground and the working surface on the plain ground.
The note table carries title, type, tags and last edited, with pinned notes first, a conflicted copy
directly beneath its original, and the `Search notes` field above it. The editor carries the title,
the type, the tags, the status line and the body, with history, protect, pin, archive and trash
reachable from the keyboard. The theme chooser at `/settings/theme` is a radio group named
`Choose a style`, whose swatches each carry a text name; choosing one retints a demonstration panel
first and the app only when confirmed.

**Accessibility contracts by component.** The theme chooser is a radio group with a group name; a
dropdown is a listbox that opens on Enter and Space, moves with the arrow keys and closes on Escape
returning focus to its trigger; a disclosure announces its expanded state and its closed panel is
inert; the carousel is decorative and pauses on hover and focus; the pinned comparison bar is
presentational; a button that navigates is a link.

**Delivery.** Every public route is complete markup before any script runs, and only the carousel,
the dropdowns, the disclosures and the theme chooser need script to come alive. The typeface is
declared with a real fallback stack to the system sans and swaps in when loaded, blocking nothing.
No image file, no icon font and no third-party script or tag loads on any public route.

## Constraints

- One account per person and one vault per account. No organisations, no workspaces and no
  tenancy beyond the account.
- No sharing of notes between accounts, no shared folders, no family folder and no way for a
  subscription owner to see a member's notes.
- No password reset, no account recovery by email, no password hint and no support path that
  can open a vault.
- No server-side search, no server-side index, no server-side preview or thumbnail and no
  server-side import. Import happens on the device.
- No real-time collaboration and no comments.
- No checkout, no card payment and no regional pricing. No payment provider exists.
- No email of any kind: no nightly mail backups, no sign-in notifications by mail and no
  invitations by mail. Invitations appear in the invited account's subscription page.
- No two-factor authentication, no hardware keys and no biometric unlock.
- No spreadsheet note type and no dated journal note type.
- No links between notes and no backlinks.
- No plugins, no custom theme plugins and no web clipper.
- No backups to consumer cloud storage services.
- No self-hosting and no setting to point the app at a different server.
- No help centre, knowledge base, blog, press page, features page, comparison pages or
  testimonials.
- No outbound network calls at run time. No native, desktop or mobile app.
- The app stays responsive with `5000` notes in one account.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`,
  where `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world
  uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
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
error, never as a server error and never as a silent success. Bearer auth is required on everything
except `GET /api/auth/params`, `POST /api/accounts`, `POST /api/sessions`,
`POST /api/sessions/refresh`, `POST /api/entitlements/verify` and `GET /api/health`.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/auth/params` | `identifier` | `identifier`, `key_params` |
| `POST /api/accounts` | `identifier`, `auth_secret`, `key_params` | `token`, `refresh_token`, `account` |
| `POST /api/sessions` | `identifier`, `auth_secret`, `device` | `token`, `refresh_token`, `expires_in` |
| `POST /api/sessions/refresh` | `refresh_token` | `token`, `refresh_token` |
| `GET /api/sessions` | none | array of `id`, `device`, `created_at`, `last_used_at`, `current` |
| `DELETE /api/sessions/<id>` | none | the ended session |
| `DELETE /api/sessions/current` | none | the current session ends |
| `POST /api/account/password` | `current_auth_secret`, `auth_secret`, `key_params`, `items_keys` | `token`, `refresh_token` |
| `DELETE /api/account` | `auth_secret`, `confirmation` | the account is deleted |
| `POST /api/items/sync` | `cursor`, `limit`, `request_id`, `items` of `uuid`, `content_type`, `envelope`, `version`, `deleted` | `retrieved_items`, `saved_items`, `conflicts`, `cursor`, `more` |
| `GET /api/items/<uuid>` | none | `uuid`, `content_type`, `envelope`, `version`, `deleted`, `created_at`, `updated_at` |
| `POST /api/files` | `uuid`, `chunk_count` | `uuid`, `status` |
| `PUT /api/files/<uuid>/chunks/<index>` | the sealed chunk bytes | `index`, `stored_bytes` |
| `POST /api/files/<uuid>/complete` | none | `uuid`, `status` |
| `GET /api/files/<uuid>/chunks/<index>` | none | the sealed chunk bytes |
| `DELETE /api/files/<uuid>` | none | the file and its chunks are removed |
| `GET /api/account/storage` | none | `used_bytes`, `quota_bytes` |
| `GET /api/account/subscription` | none | `plan`, `status`, `expires_at`, `effective_plan`, `shared_by`, `members`, `entitlement` |
| `POST /api/subscription/invitations` | `identifier` | `id`, `identifier`, `status`, `expires_at` |
| `GET /api/subscription/invitations` | none | array of `id`, `identifier`, `status`, `expires_at` addressed to the signed-in account |
| `POST /api/subscription/invitations/<id>/accept` | none | the membership, with the account's new `effective_plan` |
| `DELETE /api/subscription/members/<identifier>` | none | the member is removed |
| `POST /api/entitlements/verify` | `entitlement` | `valid`, `claims` |
| `GET /api/health` | none | `200` once ready |

Each entry in `saved_items` carries `uuid` and `version`. Each entry in `conflicts` carries `uuid`,
`type` and, for a `version_conflict`, `server_item`. A conflict `type` is one of `version_conflict`,
`uuid_conflict`, `plan_limit`, `invalid_type` or `too_large`.

**No mocks.** The sealed items, the tombstones, the sessions and the subscriptions must be rows that
exist in PostgreSQL, and every file chunk must be an object that exists in `minio` under its key. An
in-memory item list, a note list the server renders from readable titles, a sync that answers from a
cache instead of the stored rows, file bytes kept on the app's own disk and a quota figure written by
hand are each a violation of this brief. PostgreSQL and `minio` are the fact: the app's screens and its
own summaries can only reflect what lives there, never substitute for it.

## Definition of done

A person can create an account, write a note, sign out, and sign in from a fresh browser to find the
note intact, while nothing readable of it ever reaches the server and the password never leaves the
browser. A second account can never reach that note. Every change reaches every device exactly once,
two edits of one note both survive, and an emptied trash stays empty when an offline device returns.
When a subscription lapses, every note, folder, file and revision made while paid still opens.
