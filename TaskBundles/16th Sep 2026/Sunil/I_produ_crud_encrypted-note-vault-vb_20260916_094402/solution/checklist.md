# Checklist: Lockleaf

Items: 212
Unpinned values flagged: 0
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-1` `capability` The company operating Lockleaf cannot read the notes. `src: Overview para 1`
- [ ] `C-OV-2` `constraint` Keys made from the account password never leave the device in any form. `src: Overview para 1`
- [ ] `C-OV-3` `capability` The free plan never charges for encryption, unlimited devices, offline reading, tags, export or note protection. `src: Overview para 2`
- [ ] `C-OV-4` `constraint` The server never learns a title, a body, a tag name, a file name or a search query. `src: Overview para 3`
- [ ] `C-OV-5` `constraint` Lockleaf offers no sharing of notes between accounts. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-1` `role` An account holder changes or deletes only notes the account holder owns. `src: User roles table row 1`
- [ ] `C-RL-2` `role` An account holder cannot read an item, file, revision or session of another account. `src: User roles table row 1`
- [ ] `C-RL-3` `role` An account holder cannot recover a forgotten password. `src: User roles table row 1`
- [ ] `C-RL-4` `role` A subscription owner sees which accounts share the subscription. `src: User roles para 2`
- [ ] `C-RL-5` `role` A subscription owner never reaches the notes of a member account. `src: User roles para 2`
- [ ] `C-RL-6` `contract` A direct API call acting on another account's items is rejected by the server. `src: User roles para 3`
- [ ] `C-RL-7` `contract` A rejected call leaves the protected state unchanged. `src: User roles para 3`
- [ ] `C-RL-8` `contract` An item belonging to another account is reported as not found rather than as forbidden. `src: User roles para 3`
- [ ] `C-RL-9` `literal` Signup is open at `/signup`. `src: User roles para 4`
- [ ] `C-RL-10` `capability` Signup accepts an email address or a private username as the identifier. `src: User roles para 4`
- [ ] `C-RL-11` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles seeded accounts`
- [ ] `C-RL-12` `literal` The seeded account `user@example.com` holds an `active` `Canopy` subscription. `src: User roles seeded accounts table row 1`
- [ ] `C-RL-13` `literal` The seeded account `user2@example.com` is a member of the subscription owned by `user@example.com`. `src: User roles seeded accounts table row 2`
- [ ] `C-RL-14` `literal` The seeded account `user3@example.com` holds a `Canopy` subscription `expired` on `2026-06-30`. `src: User roles seeded accounts table row 3`

## C-CF Core features

- [ ] `C-CF-1` `contract` Creating an account sends the identifier, the authentication secret, the key parameters to POST /api/accounts. `src: Core features, Accounts rule 1`
- [ ] `C-CF-2` `constraint` No request ever carries the password in any encoding. `src: Core features, Accounts rule 1`
- [ ] `C-CF-3` `constraint` The server refuses a second account under an identifier differing only by letter case or surrounding spaces. `src: Core features, Accounts rule 2`
- [ ] `C-CF-4` `constraint` The server stores nothing from which the root key can be derived. `src: Core features, Accounts rule 3`
- [ ] `C-CF-5` `capability` GET /api/auth/params returns synthetic key parameters for an identifier with no account. `src: Core features, Accounts rule 4`
- [ ] `C-CF-6` `capability` Synthetic key parameters carry the same fields as the key parameters of a real account. `src: Core features, Accounts rule 4`
- [ ] `C-CF-7` `capability` Synthetic key parameters stay identical across requests for one identifier. `src: Core features, Accounts rule 4`
- [ ] `C-CF-8` `capability` Synthetic key parameters differ between two unknown identifiers. `src: Core features, Accounts rule 4`
- [ ] `C-CF-9` `contract` Signing in sends the identifier with the authentication secret to POST /api/sessions. `src: Core features, Accounts rule 5`
- [ ] `C-CF-10` `constraint` A wrong secret is refused with the same outcome as an unknown identifier. `src: Core features, Accounts rule 5`
- [ ] `C-CF-11` `constraint` A wrong secret receives the same response body as an unknown identifier. `src: Core features, Accounts rule 5`
- [ ] `C-CF-12` `constraint` No link, route or message offers to reset, recover or email a password. `src: Core features, Accounts rule 6`
- [ ] `C-CF-13` `ui` The sign-in page offers the link `Start over with an empty vault`, which opens `/start-over`. `src: Core features, Accounts rule 6`
- [ ] `C-CF-14` `ui` The start-over page lists an export file saved earlier as a way back to the notes. `src: Core features, Accounts rule 7`
- [ ] `C-CF-15` `ui` The start-over page lists a device still signed in as a way back to the notes. `src: Core features, Accounts rule 7`
- [ ] `C-CF-16` `ui` The start-over button stays unavailable until the person types `delete my notes forever`. `src: Core features, Accounts rule 7`
- [ ] `C-CF-17` `ui` The signup form states that nobody can recover the notes behind a forgotten password. `src: Core features, Accounts rule 8`
- [ ] `C-CF-18` `ui` The signup form refuses a password shorter than `12` characters beside the password field. `src: Core features, Accounts rule 9`
- [ ] `C-CF-19` `ui` The signup form refuses a password confirmation that does not match, beside the confirmation field. `src: Core features, Accounts rule 9`
- [ ] `C-CF-20` `capability` A password change submits the new authentication secret, new key parameters, re-wrapped items keys to POST /api/account/password. `src: Core features, Accounts rule 10`
- [ ] `C-CF-21` `constraint` A password change stores everything submitted or stores none of the submission. `src: Core features, Accounts rule 10`
- [ ] `C-CF-22` `constraint` A password change rewrites no note. `src: Core features, Accounts rule 11`
- [ ] `C-CF-23` `capability` A password change ends every other session of the account at once. `src: Core features, Accounts rule 12`
- [ ] `C-CF-24` `capability` The session making a password change continues with a fresh token. `src: Core features, Accounts rule 12`
- [ ] `C-CF-25` `capability` POST /api/sessions/refresh exchanges a refresh token for a new access token with a new refresh token. `src: Core features, Sessions rule 2`
- [ ] `C-CF-26` `constraint` A refresh token works exactly once. `src: Core features, Sessions rule 2`
- [ ] `C-CF-27` `constraint` Presenting a used refresh token invalidates the refresh token that replaced the used one. `src: Core features, Sessions rule 3`
- [ ] `C-CF-28` `constraint` Presenting a used refresh token ends the access token of that session. `src: Core features, Sessions rule 3`
- [ ] `C-CF-29` `ui` The sessions page lists every session with the device, the start time, the last use. `src: Core features, Sessions rule 4`
- [ ] `C-CF-30` `ui` The sessions page marks the current session. `src: Core features, Sessions rule 4`
- [ ] `C-CF-31` `capability` An ended session is refused from the moment the session ends. `src: Core features, Sessions rule 4`
- [ ] `C-CF-32` `data` An item carries `uuid`, `content_type`, `envelope`, `version`, `deleted`. `src: Core features, The sealed item store rule 1`
- [ ] `C-CF-33` `literal` The content type is one of `note`, `tag`, `items_key`, `file`, `revision`, `saved_view` or `preferences`. `src: Core features, The sealed item store rule 2`
- [ ] `C-CF-34` `constraint` An item of any other content type is refused as `invalid_type`. `src: Core features, The sealed item store rule 2`
- [ ] `C-CF-35` `constraint` Titles, bodies, tag names, flags, file names live only inside the envelope. `src: Core features, The sealed item store rule 4`
- [ ] `C-CF-36` `capability` Saving the same words twice produces two different envelopes. `src: Core features, The sealed item store rule 5`
- [ ] `C-CF-37` `capability` An item that cannot be opened shows a heading saying the note cannot be opened. `src: Core features, The sealed item store rule 7`
- [ ] `C-CF-38` `capability` The page of an unopenable item names the item uuid. `src: Core features, The sealed item store rule 7`
- [ ] `C-CF-39` `constraint` The page of an unopenable item offers no editor that could save over the item. `src: Core features, The sealed item store rule 7`
- [ ] `C-CF-40` `constraint` An envelope longer than `2000000` characters is refused as `too_large`. `src: Core features, The sealed item store rule 10`
- [ ] `C-CF-41` `constraint` An oversized envelope is never truncated into storage. `src: Core features, The sealed item store rule 10`
- [ ] `C-CF-42` `contract` Sync runs through POST /api/items/sync. `src: Core features, Sync para 1`
- [ ] `C-CF-43` `capability` The sync reply carries `retrieved_items`, `saved_items`, `conflicts`, `cursor`, `more`. `src: Core features, Sync rule 2`
- [ ] `C-CF-44` `capability` Every item written after a cursor is delivered exactly once to a device following `more`. `src: Core features, Sync rule 3`
- [ ] `C-CF-45` `constraint` One refused item in a sync request never fails the other items. `src: Core features, Sync rule 5`
- [ ] `C-CF-46` `capability` A sync replayed with the same `request_id` returns the same answer. `src: Core features, Sync rule 6`
- [ ] `C-CF-47` `constraint` A replayed sync changes nothing a second time. `src: Core features, Sync rule 6`
- [ ] `C-CF-48` `capability` A device with no cursor receives the whole vault from the beginning. `src: Core features, Sync rule 7`
- [ ] `C-CF-49` `constraint` A uuid belonging to another account is refused as `uuid_conflict`. `src: Core features, Sync rule 9`
- [ ] `C-CF-50` `constraint` A uuid conflict reveals nothing about the item of the other account. `src: Core features, Sync rule 9`
- [ ] `C-CF-51` `constraint` Sync sends or receives only the items of the signed-in account. `src: Core features, Sync rule 9`
- [ ] `C-CF-52` `capability` An item submitted with an older version is a `version_conflict`. `src: Core features, Conflicts and deletion rule 1`
- [ ] `C-CF-53` `constraint` A stale write leaves the stored item unchanged. `src: Core features, Conflicts and deletion rule 1`
- [ ] `C-CF-54` `capability` A version conflict returns the stored item as `server_item`. `src: Core features, Conflicts and deletion rule 1`
- [ ] `C-CF-55` `ui` A conflicted copy is labelled `Conflicted copy` with the device that made the copy. `src: Core features, Conflicts and deletion rule 3`
- [ ] `C-CF-56` `ui` A conflicted copy sorts directly beside the original note. `src: Core features, Conflicts and deletion rule 3`
- [ ] `C-CF-57` `ui` A conflicted copy offers a side-by-side comparison with the original note. `src: Core features, Conflicts and deletion rule 4`
- [ ] `C-CF-58` `ui` The note list offers `Clear identical copies`, removing matching conflicted copies after confirmation. `src: Core features, Conflicts and deletion rule 5`
- [ ] `C-CF-59` `capability` Emptying the trash writes a tombstone whose `deleted` flag is `true`. `src: Core features, Conflicts and deletion rule 7`
- [ ] `C-CF-60` `capability` A tombstone carries an empty envelope with a higher version. `src: Core features, Conflicts and deletion rule 7`
- [ ] `C-CF-61` `capability` A tombstone reaches a device that was offline through sync. `src: Core features, Conflicts and deletion rule 7`
- [ ] `C-CF-62` `constraint` An older copy of a tombstoned item receives a version conflict carrying the tombstone. `src: Core features, Conflicts and deletion rule 9`
- [ ] `C-CF-63` `constraint` A deleted note never comes back. `src: Core features, Conflicts and deletion rule 9`
- [ ] `C-CF-64` `ui` A trashed note can be restored from the trash. `src: Core features, Pin, archive, trash and protect rule 3`
- [ ] `C-CF-65` `ui` Emptying the trash removes the trashed note from every list. `src: Core features, Conflicts and deletion rule 7`
- [ ] `C-CF-66` `ui` The new note route carries a `Note type` chooser, a `Title` field, a `Note body` editor. `src: Core features, Notes and note types rule 1`
- [ ] `C-CF-67` `capability` Choosing `Create note` saves the note, then opens the note at its own route. `src: Core features, Notes and note types rule 1`
- [ ] `C-CF-68` `ui` The note status line reads `All changes saved` once the sealed copy is stored. `src: Core features, Notes and note types rule 3`
- [ ] `C-CF-69` `ui` The note status line reads `Saving` during a save in flight. `src: Core features, Notes and note types rule 3`
- [ ] `C-CF-70` `capability` A note written in one browser opens with the same words after signing in again. `src: Core features, Notes and note types rule 3`
- [ ] `C-CF-71` `ui` Every note editor can be driven entirely from the keyboard. `src: Core features, Notes and note types rule 5`
- [ ] `C-CF-72` `ui` A person on `Leaf` is offered only the Leaf note types when creating a note. `src: Core features, Notes and note types rule 8`
- [ ] `C-CF-73` `ui` Changing a note type first shows what the conversion will lose. `src: Core features, Notes and note types rule 7`
- [ ] `C-CF-74` `ui` A folder is a tag nested inside another tag in the folder tree. `src: Core features, Tags, folders and saved views rule 1`
- [ ] `C-CF-75` `ui` A person on `Leaf` is told that new nesting needs a paid plan. `src: Core features, Tags, folders and saved views rule 4`
- [ ] `C-CF-76` `ui` A person on `Leaf` still opens folders made on a paid plan. `src: Core features, Tags, folders and saved views rule 4`
- [ ] `C-CF-77` `ui` A saved view that cannot be evaluated shows a message saying so, with the reason. `src: Core features, Tags, folders and saved views rule 8`
- [ ] `C-CF-78` `ui` The saved view `Renewals` lists notes whose title contains `renewal`. `src: Core features, Tags, folders and saved views rule 7`
- [ ] `C-CF-79` `ui` A pinned note sorts to the top of the note table. `src: Core features, Pin, archive, trash and protect rule 1`
- [ ] `C-CF-80` `ui` An archived note is listed on the archive page. `src: Core features, Pin, archive, trash and protect rule 2`
- [ ] `C-CF-81` `ui` A protected note shows a notice saying the note is protected until the account password is entered again. `src: Core features, Pin, archive, trash and protect rule 4`
- [ ] `C-CF-82` `ui` The app says protection hides a note from someone looking over your shoulder. `src: Core features, Pin, archive, trash and protect rule 5`
- [ ] `C-CF-83` `constraint` A search query never leaves the device. `src: Core features, Search rule 2`
- [ ] `C-CF-84` `ui` The field `Search notes` narrows the note list as the person types. `src: Core features, Search rule 3`
- [ ] `C-CF-85` `ui` The history page lists revisions newest first with their times. `src: Core features, Revision history rule 3`
- [ ] `C-CF-86` `constraint` A revision item sent from a `Leaf` account is refused as `plan_limit`. `src: Core features, Revision history table row 1`
- [ ] `C-CF-87` `constraint` An account whose subscription lapsed keeps every revision. `src: Core features, Revision history rule 6`
- [ ] `C-CF-88` `capability` POST /api/files records a file as `pending` with the file chunk count. `src: Core features, Encrypted files rule 2`
- [ ] `C-CF-89` `capability` Each chunk is sent to the chunk endpoint of the file. `src: Core features, Encrypted files rule 2`
- [ ] `C-CF-90` `constraint` A file missing a chunk cannot be completed. `src: Core features, Encrypted files rule 2`
- [ ] `C-CF-91` `capability` Completing a fully stored file marks the file `complete`. `src: Core features, Encrypted files rule 2`
- [ ] `C-CF-92` `data` Sealed chunks are stored in minio under the key vault, file uuid, chunk index. `src: Core features, Encrypted files rule 3`
- [ ] `C-CF-93` `constraint` A chunk is readable only by the account owning the file. `src: Core features, Encrypted files rule 4`
- [ ] `C-CF-94` `constraint` An upload from an account whose effective plan is not `Canopy` is refused. `src: Core features, Encrypted files rule 7`
- [ ] `C-CF-95` `capability` The storage endpoint reports `used_bytes` equal to the sealed bytes stored. `src: Core features, Encrypted files rule 8`
- [ ] `C-CF-96` `literal` A `Canopy` account reports a `quota_bytes` of `107374182400`. `src: Core features, Encrypted files rule 9`
- [ ] `C-CF-97` `capability` An account no longer entitled to files downloads every file the account already has. `src: Core features, Encrypted files rule 10`
- [ ] `C-CF-98` `ui` The files page lists each file with the sealed size beside the storage figure. `src: Core features, Encrypted files rule 8`
- [ ] `C-CF-99` `capability` The subscription endpoint reports `plan`, `status`, `expires_at`, `effective_plan`. `src: Core features, Plans, subscriptions and sharing rule 1`
- [ ] `C-CF-100` `capability` A member of an active shared `Canopy` subscription has the effective plan `Canopy`. `src: Core features, Plans, subscriptions and sharing rule 2`
- [ ] `C-CF-101` `capability` A lapsed account has the effective plan `Leaf`. `src: Core features, Plans, subscriptions and sharing rule 2`
- [ ] `C-CF-102` `capability` The entitlement endpoint answers valid for an entitlement the product signed. `src: Core features, Plans, subscriptions and sharing rule 3`
- [ ] `C-CF-103` `constraint` The entitlement endpoint answers invalid for an altered entitlement. `src: Core features, Plans, subscriptions and sharing rule 3`
- [ ] `C-CF-104` `data` The entitlement middle part holds `identifier`, `plan`, `expires_at`, `features` as base64url JSON. `src: Core features, Plans, subscriptions and sharing rule 3`
- [ ] `C-CF-105` `ui` After a lapse a note in a paid type still opens, reads, edits. `src: Core features, Plans, subscriptions and sharing rule 5`
- [ ] `C-CF-106` `ui` After a lapse an `Authenticator` note keeps working. `src: Core features, Plans, subscriptions and sharing rule 5`
- [ ] `C-CF-107` `ui` The subscription page lists the identifier of each member. `src: Core features, Plans, subscriptions and sharing rule 7`
- [ ] `C-CF-108` `ui` The subscription page states that members' notes are never shared. `src: Core features, Plans, subscriptions and sharing rule 7`
- [ ] `C-CF-109` `capability` An accepted invitation gives the invited account the effective plan `Canopy`. `src: Core features, Plans, subscriptions and sharing rule 6`
- [ ] `C-CF-110` `capability` A removed member keeps everything the member made. `src: Core features, Plans, subscriptions and sharing rule 9`
- [ ] `C-CF-111` `ui` Choosing `Lock now` in the sidebar locks the app, then opens `/locked`. `src: Core features, Lock rule 2`
- [ ] `C-CF-112` `constraint` A locked page holds no note title or body. `src: Core features, Lock rule 3`
- [ ] `C-CF-113` `ui` Entering the passcode on the locked page, then choosing `Unlock`, returns to the notes. `src: Core features, Lock rule 4`
- [ ] `C-CF-114` `ui` Choosing the plain export form warns once that the file is not sealed. `src: Core features, Export, import and leaving rule 2`
- [ ] `C-CF-115` `ui` The import page shows how many notes, tags, files an export file holds before writing anything. `src: Core features, Export, import and leaving rule 5`
- [ ] `C-CF-116` `ui` The delete page offers the export in the same flow before deleting the account. `src: Core features, Export, import and leaving rule 8`
- [ ] `C-CF-117` `capability` Deleting an account removes every item of the account. `src: Core features, Export, import and leaving rule 8`
- [ ] `C-CF-118` `capability` After deletion a sign-in with the old identifier is refused exactly as an unknown identifier is. `src: Core features, Export, import and leaving rule 9`
- [ ] `C-CF-119` `capability` After deletion the identifier is free for a new account. `src: Core features, Export, import and leaving rule 9`
- [ ] `C-CF-120` `ui` The demo says `Nothing you write here is saved.` when the demo opens. `src: Core features, The public site and the demo rule 2`
- [ ] `C-CF-121` `capability` The demo creates nothing on any server. `src: Core features, The public site and the demo rule 2`
- [ ] `C-CF-122` `capability` An unknown address answers with a not-found result. `src: Core features, The public site and the demo rule 3`
- [ ] `C-CF-123` `ui` The not-found page is headed `We can't find that page.` `src: Core features, The public site and the demo rule 3`
- [ ] `C-CF-124` `capability` The not-found page links back to the home page, the plans page, the privacy essay, sign in. `src: Core features, The public site and the demo rule 3`
- [ ] `C-CF-125` `capability` Every public route carries a document title no other public route shares. `src: Core features, The public site and the demo rule 4`
- [ ] `C-CF-126` `capability` Every public route carries a meta description no other public route shares. `src: Core features, The public site and the demo rule 4`
- [ ] `C-CF-127` `capability` Every public route declares a social preview title. `src: Core features, The public site and the demo rule 5`
- [ ] `C-CF-128` `capability` Every public route declares a preview image whose address resolves. `src: Core features, The public site and the demo rule 5`
- [ ] `C-CF-129` `capability` Every internal link on every public route resolves. `src: Core features, The public site and the demo rule 6`
- [ ] `C-CF-130` `capability` A form rejects invalid input inline, naming the invalid field. `src: Core features, The public site and the demo rule 7`
- [ ] `C-CF-131` `constraint` A form rejecting invalid input writes nothing. `src: Core features, The public site and the demo rule 7`

## C-UF User flow

- [ ] `C-UF-1` `contract` An unauthenticated request for an app route goes to `/sign-in`. `src: User flow, Entry and redirects`
- [ ] `C-UF-2` `ui` The sign-in form carries `Email`, `Password`, a `Sign in` button. `src: User flow, Entry and redirects`
- [ ] `C-UF-3` `ui` The signup form carries `Email`, `Password`, `Confirm password`, a `Create account` button. `src: User flow, Entry and redirects`
- [ ] `C-UF-4` `capability` Signing in with no held route lands on `/notes`. `src: User flow, Entry and redirects`
- [ ] `C-UF-5` `ui` An empty note list says there are no notes yet, offering `New note`. `src: User flow, Journeys 1`
- [ ] `C-UF-6` `ui` Choosing `Sign out` in the settings menu ends the session, returning to `/sign-in`. `src: User flow, Entry and redirects`
- [ ] `C-UF-7` `ui` Every list has an empty state that says what is missing, offering the action that fills the list. `src: User flow, States`
- [ ] `C-UF-8` `ui` Changing the password ends on a full-page confirmation saying what happened. `src: User flow, Entry and redirects`
- [ ] `C-UF-9` `ui` During the first unsealing after sign-in the app shows progress rather than an empty table. `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-1` `ui` Reading text is a deep cool neutral, headings a near-black neutral, the page ground a near-white neutral. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-2` `ui` The mid, vivid blue appears only on things a person can click or that are active. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-3` `ui` A card sits only on the pale band, never on the plain ground. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-4` `ui` The mid, vivid orange accent appears only under a navigation link being pointed at or under the encryption phrase on the home page. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-5` `ui` Success wears a mid, vivid teal with a word or a mark beside the colour. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-6` `ui` Nothing animates on scroll. `src: UI/UX notes, Motion`
- [ ] `C-UX-7` `ui` Under a reduced-motion preference the carousel stops. `src: UI/UX notes, Motion`
- [ ] `C-UX-8` `ui` Every control has resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes, Components`
- [ ] `C-UX-9` `ui` The app offers the themes `Paper`, `Midnight`, `Sepia`. `src: UI/UX notes, Mode`
- [ ] `C-UX-10` `ui` Keyboard navigation reaches every control with a visible focus ring. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-11` `ui` Body text meets the WCAG AA contrast ratio of `4.5:1` in every theme. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-12` `ui` A skip link is the first focusable element, appearing on focus. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-13` `ui` On a phone each note table row becomes a stacked card carrying the same fields with labels. `src: UI/UX notes, Responsive`
- [ ] `C-UX-14` `ui` Nothing overflows sideways at any viewport width. `src: UI/UX notes, Responsive`

## C-TR Technical requirements

- [ ] `C-TR-1` `contract` The app keeps its rows in PostgreSQL reached at `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-2` `contract` The app keeps file chunks in minio reached at `STORAGE_ENDPOINT` in the bucket `STORAGE_BUCKET`. `src: Technical requirements para 1`
- [ ] `C-TR-3` `constraint` No page, script or style the browser downloads carries the storage keys or the database password. `src: Technical requirements, secrets para`

## C-DM Data model

- [ ] `C-DM-1` `data` The accounts table holds an `identifier` unique after trimming or lower-casing. `src: Data model, accounts`
- [ ] `C-DM-2` `data` The items table holds `uuid`, `account_id`, `content_type`, `envelope`, `version`, `deleted`, `created_at`, `updated_at`. `src: Data model, items`
- [ ] `C-DM-3` `constraint` No column of the items table holds a title, body, tag name, file name or flag other than `deleted`. `src: Data model, items`
- [ ] `C-DM-4` `data` The file_uploads table holds a `status` of `pending` or `complete`. `src: Data model, file_uploads`
- [ ] `C-DM-5` `constraint` No text column of any table holds the words of a note in plain form. `src: Data model, Invariants bullet 1`
- [ ] `C-DM-6` `constraint` No text column of any table holds a reversible encoding of the words of a note. `src: Data model, Invariants bullet 1`
- [ ] `C-DM-7` `literal` The seeded account `user2@example.com` holds the note `Surprise party plan`. `src: Data model, Seed data`
- [ ] `C-DM-8` `literal` The seeded account `user@example.com` holds the pinned note `Grocery run` with the words `Oat milk, lemons, rye bread, coffee filters.` `src: Data model, Seed data table row 1`
- [ ] `C-DM-9` `literal` The seeded note `Quarterly taxes` has `3` revisions. `src: Data model, Seed data`
- [ ] `C-DM-10` `literal` The seeded note `Packing list` has one conflicted copy made on the device `Kitchen tablet`. `src: Data model, Seed data`
- [ ] `C-DM-11` `literal` The seeded note `Loan agreement` of `user3@example.com` has `2` revisions. `src: Data model, Seed data`
- [ ] `C-DM-12` `literal` The seeded account `user3@example.com` holds the file `contract-draft.pdf`. `src: Data model, Seed data`
- [ ] `C-DM-13` `literal` The seeded file `lease-scan.pdf` is attached to `Passport renewal`. `src: Data model, Seed data`
- [ ] `C-DM-14` `literal` The seeded note `Passport renewal` is protected. `src: Data model, Seed data table row 3`
- [ ] `C-DM-15` `constraint` A stored item version only increases with each accepted save. `src: Data model, Invariants bullet 4`

## C-FE Front-end specification

- [ ] `C-FE-1` `ui` The home page hero reads `Free your mind.` above the buttons `Start writing for free`, `Try live demo`. `src: Front-end specification, The home page table row 1`
- [ ] `C-FE-2` `ui` The home page carousel shows sixteen chips, beginning with `Markdown`, ending with private photos. `src: Front-end specification, The home page table row 4`
- [ ] `C-FE-3` `ui` The carousel pauses on pointer hover or keyboard focus. `src: Front-end specification, The home page`
- [ ] `C-FE-4` `ui` The plans page shows the `Leaf`, `Branch`, `Canopy` cards priced `Free`, `$36.00 / year`, `$96.00 / year`. `src: Front-end specification, The plans page table`
- [ ] `C-FE-5` `ui` Exactly one button on the plans page is filled, belonging to `Canopy`. `src: Front-end specification, The plans page`
- [ ] `C-FE-6` `ui` A bar carrying the three plan names pins above the scrolling comparison table. `src: Front-end specification, The plans page`
- [ ] `C-FE-7` `ui` The `Note history` row reads `Current session only`, `365 days`, `Unlimited`. `src: Front-end specification, The plans page`
- [ ] `C-FE-8` `ui` The privacy essay `Stand For Privacy` is built from headings with paragraphs alone. `src: Front-end specification, The principle pages`
- [ ] `C-FE-9` `ui` The longevity essay `Built to Last` carries the heading `We say no to most feature requests.` `src: Front-end specification, The principle pages`
- [ ] `C-FE-10` `ui` A closed footer accordion is removed from the reading order. `src: Front-end specification, Footer`
- [ ] `C-FE-11` `ui` The filled `Start for free` header button fades in after scroll without shifting the row. `src: Front-end specification, Header`
- [ ] `C-FE-12` `ui` The hatched diamonds, circles, separators are drawn rather than shipped as files. `src: Front-end specification, The hatched motif`
- [ ] `C-FE-13` `ui` The `Canopy` card carries a filled star before the plan name. `src: Front-end specification, The plans page`

## C-CN Constraints

- [ ] `C-CN-1` `constraint` Lockleaf has no password reset flow. `src: Constraints bullet 3`
- [ ] `C-CN-2` `constraint` Lockleaf runs no server-side search. `src: Constraints bullet 4`

## C-DC Deployment contract

- [ ] `C-DC-1` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-2` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-3` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-4` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes`
- [ ] `C-DC-5` `contract` An invalid call is rejected as a client error, never as a server error. `src: Deployment contract, API shapes`
- [ ] `C-DC-6` `contract` Bearer auth is required on item reads. `src: Deployment contract, API shapes`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `/signup` | a pinned value in the brief | `C-RL-9` | instruction.md |
| `deku-demo-pw-2026` | a pinned value in the brief | `C-RL-11` | instruction.md |
| `user@example.com` | a pinned value in the brief | `C-RL-12` | instruction.md |
| `active` | a pinned value in the brief | `C-RL-12` | instruction.md |
| `Canopy` | a pinned value in the brief | `C-RL-12` | instruction.md |
| `user2@example.com` | a pinned value in the brief | `C-RL-13` | instruction.md |
| `user3@example.com` | a pinned value in the brief | `C-RL-14` | instruction.md |
| `expired` | a pinned value in the brief | `C-RL-14` | instruction.md |
| `2026-06-30` | a pinned value in the brief | `C-RL-14` | instruction.md |
| `note` | a pinned value in the brief | `C-CF-33` | instruction.md |
| `tag` | a pinned value in the brief | `C-CF-33` | instruction.md |
| `items_key` | a pinned value in the brief | `C-CF-33` | instruction.md |
| `file` | a pinned value in the brief | `C-CF-33` | instruction.md |
| `revision` | a pinned value in the brief | `C-CF-33` | instruction.md |
| `saved_view` | a pinned value in the brief | `C-CF-33` | instruction.md |
| `preferences` | a pinned value in the brief | `C-CF-33` | instruction.md |
| `quota_bytes` | a pinned value in the brief | `C-CF-96` | instruction.md |
| `107374182400` | a pinned value in the brief | `C-CF-96` | instruction.md |
| `Surprise party plan` | a pinned value in the brief | `C-DM-7` | instruction.md |
| `Grocery run` | a pinned value in the brief | `C-DM-8` | instruction.md |
| `Oat milk, lemons, rye bread, coffee filters.` | a pinned value in the brief | `C-DM-8` | instruction.md |
| `Quarterly taxes` | a pinned value in the brief | `C-DM-9` | instruction.md |
| `3` | a pinned value in the brief | `C-DM-9` | instruction.md |
| `Packing list` | a pinned value in the brief | `C-DM-10` | instruction.md |
| `Kitchen tablet` | a pinned value in the brief | `C-DM-10` | instruction.md |
| `Loan agreement` | a pinned value in the brief | `C-DM-11` | instruction.md |
| `2` | a pinned value in the brief | `C-DM-11` | instruction.md |
| `contract-draft.pdf` | a pinned value in the brief | `C-DM-12` | instruction.md |
| `lease-scan.pdf` | a pinned value in the brief | `C-DM-13` | instruction.md |
| `Passport renewal` | a pinned value in the brief | `C-DM-13` | instruction.md |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 1 | 5 |
| User roles | 1 | 14 |
| Core features | 30 | 131 |
| User flow | 8 | 9 |
| UI and UX notes | 2 | 14 |
| Technical requirements | 3 | 3 |
| Data model | 5 | 15 |
| Front-end specification | 3 | 13 |
| Constraints | 0 | 2 |
| Deployment contract | 6 | 6 |

Where a section states more obligation-bearing sentences than items, the remainder is
rationale, a restatement of an item already listed, or an obligation declared below as
one no channel can observe.

## Declared but ungraded

Obligations `instruction.md` states that no channel can observe. Recorded here rather than
given a fabricated citation or dropped in silence (stage-3-checklist.md, OPEN-DECISIONS D-H).
Each stays a requirement of the product; none moves the score.

| Obligation | why: |
|---|---|
| An access token stays valid for `60` minutes, a refresh token for `30` days. | a lifetime is asserted only by waiting it out, and J.5 bars a wall-clock wait |
| The key derivation from the password is memory-hard with per-account parameters. | the derivation runs inside the browser and its cost is invisible to any HTTP, database or page observation |
| Token, hash and secret comparisons take the same time whether they match. | a timing property; J.5 bars an assertion whose outcome differs between two identical runs |
| Identifiers, nonces and keys come from the platform's cryptographic source. | the randomness source is code, and G10 holds the source out of every reward-bearing check |
| No log line, error report or response carries a secret, a query, a title or a file name. | logs live inside the app container, which no channel opens |
| There is no third-party crash reporter and no third-party analytics. | the runtime has no outbound network, so the absence is enforced rather than observed |
| The client refuses plain transport to any host but its own origin. | the environment serves one origin only, so no second host exists to refuse |
| A device keeps working offline and catches up through sync. | the browser channel cannot cut the network, and pytest drives no offline client |
| An unsaved buffer survives a forced quit or a crash. | killing the browser mid-edit is outside what the browser grader can do (reference/N) |
| Tag names differing only by case or equivalent characters are one tag; folder loops repair; deleting a tag reparents its children. | tag names and parents live inside sealed envelopes the grader cannot open |
| Edits landing close together gather into one revision; `Branch` revisions older than `365 days` are removed. | gathering is client behaviour inside sealed items, and pruning needs a year of elapsed time |
| Tombstones are kept at least `90` days; an orphan sweep acts only on records older than `90` days. | a retention floor is observed only by waiting it out |
| Chunks are at most `4194304` bytes, authenticated with their position and a last-chunk marker. | sealing happens in the browser and the server sees opaque chunk bytes |
| A dropped upload resumes from the first missing chunk; downloads stream chunk by chunk; previews are never uploaded. | resumption and streaming are client behaviour under network failure, which no channel can induce |
| An envelope records its protocol version; items upgrade on next save; items keys rotate without removing old keys. | all three live inside sealed envelopes the grader cannot open |
| A shared subscription never holds more than `5` accounts; an invitation expires after `7` days. | the seeded subscription's seats are read by the browser journeys, and expiry needs a week of elapsed time |
| The entitlement refreshes before expiry with a grace window. | a refresh schedule is observed only by waiting for an expiry |
| The export is one sealed or plain file, documented and versioned, split into named parts above a size threshold. | the browser grader cannot read a downloaded file back (reference/N) |
| Importing reads the file on the device, adds with new identifiers and offers duplicates as skippable. | the browser grader cannot choose a local file to upload (reference/N) |
| Account deletion retains only the minimum billing records the law requires, named in the flow. | no billing records exist in this environment to retain |
| Every time a person sees is displayed in the reader's own time zone. | the grader runs in one time zone, so a correct and an incorrect zone read identically |
| Public routes are fully readable with scripting turned off. | the browser grader runs with scripting on and cannot turn it off |
| Locking never interrupts a save already under way. | the race needs a lock pressed during an in-flight save, which no channel can time |
| The stack is `Express` with `Nunjucks` and vanilla progressive enhancement, using only the named libraries. | G10 bars any reward-bearing check from reading the agent's source |
| PostgreSQL and `minio` are never downloaded, installed or started by the app. | the grader reaches the same services either way, so a self-started copy is indistinguishable |
| Login credentials are written to `/app/USER_README.md`; `.browser_screenshots/` and `.downloads/` exist at the app root. | a path on the agent container filesystem, which no black-box channel opens under the separate verifier |
| A production build is served; the server outlives the session and binds `0.0.0.0`. | a process property the harness observes by reaching the app at all, not a separate assertion |
| No edge functions; no persistent volumes, fixed container names or custom networks. | a deployment-topology absence validated by G2 against task.toml, not by a runtime channel |
| The app stays responsive with `5000` notes in one account. | a load characteristic; J.5 bars an assertion whose outcome differs between two identical runs |
| No checkout, no email, no two-factor, no spreadsheet or journal type, no note links, no plugins, no cloud backups, no self-hosting, no help centre or blog. | an absence of features with no route to probe |
| A failed save shows a banner in place and keeps the words queued. | a save failure cannot be induced from outside the running app |
