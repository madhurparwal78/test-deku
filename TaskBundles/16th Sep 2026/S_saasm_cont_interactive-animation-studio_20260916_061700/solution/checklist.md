# Checklist: Mote Interactive Animation Studio

Items: 319
Unpinned values flagged: 4
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-CN, C-TR, C-DM, C-FE, C-DC

## C-OV Overview

- [ ] `C-OV-1` `capability` The application serves a browser workspace for building interactive graphics. `src: Overview`
- [ ] `C-OV-2` `data` A workspace contains folders; a folder contains documents. `src: Overview`
- [ ] `C-OV-3` `data` A document carries artboards, one named animation, one state machine. `src: Overview`
- [ ] `C-OV-4` `capability` Every edit is recorded as an operation on an append-only log. `src: Overview`
- [ ] `C-OV-5` `capability` A revision is materialised from the operation log as a content addressed binary. `src: Overview`
- [ ] `C-OV-6` `capability` A publish freezes one revision into an immutable build. `src: Overview`
- [ ] `C-OV-7` `constraint` The marketplace shows published work to anybody. `src: Overview`
- [ ] `C-OV-8` `constraint` The marketplace shows unpublished work to nobody. `src: Overview`

## C-RL User roles

- [ ] `C-RL-1` `role` The application has exactly two roles, `editor` plus `viewer`. `src: User roles`
- [ ] `C-RL-2` `role` An `editor` may read every folder in the workspace. `src: User roles table row 1`
- [ ] `C-RL-3` `role` An `editor` may create folders, documents, operations, revisions. `src: User roles table row 1`
- [ ] `C-RL-4` `role` An `editor` may publish, roll back, unpublish. `src: User roles table row 1`
- [ ] `C-RL-5` `role` An `editor` may invite a member, may change a member role. `src: User roles table row 1`
- [ ] `C-RL-6` `role` A `viewer` reads only documents granted to them. `src: User roles table row 2`
- [ ] `C-RL-7` `role` A `viewer` reads only folders on the path to a granted document. `src: User roles table row 2`
- [ ] `C-RL-8` `role` A `viewer` cannot create, edit, materialise, restore, publish, roll back, unpublish, invite, change a role. `src: User roles table row 2`
- [ ] `C-RL-9` `role` A `viewer` cannot learn the name of a folder off the granted path. `src: User roles table row 2`
- [ ] `C-RL-10` `contract` Authorization is enforced server-side on every mutating endpoint. `src: User roles`
- [ ] `C-RL-11` `contract` A direct API call from a `viewer` session to an `editor`-only endpoint is denied by the server. `src: User roles`
- [ ] `C-RL-12` `contract` A denied call from a `viewer` session leaves the protected state unchanged. `src: User roles`
- [ ] `C-RL-13` `capability` Signup is open to anybody. `src: User roles`
- [ ] `C-RL-14` `capability` A new account receives its own empty workspace. `src: User roles`
- [ ] `C-RL-15` `literal` The seeded editors are `editor@example.com`, `editor2@example.com`, `editor3@example.com`. `src: User roles`
- [ ] `C-RL-16` `literal` The seeded viewer is `viewer@example.com`, granted read on `Broadcast` alone. `src: User roles`
- [ ] `C-RL-17` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles`

## C-CF Core features

- [ ] `C-CF-1` `capability` Each edit is submitted as one operation carrying a client-minted `op_id`. `src: Core features, The operation log`
- [ ] `C-CF-2` `contract` The service assigns `seq`, strictly increasing per document. `src: Core features, The operation log rule 1`
- [ ] `C-CF-3` `contract` Two clients appending at the same moment receive two different `seq` values. `src: Core features, The operation log rule 1`
- [ ] `C-CF-4` `contract` No operation is lost when two clients append at the same moment. `src: Core features, The operation log rule 1`
- [ ] `C-CF-5` `contract` Two operations on different properties of one node both apply with outcome `applied`. `src: Core features, The operation log rule 2`
- [ ] `C-CF-6` `contract` Two operations on one property of one node resolve to the higher `seq`. `src: Core features, The operation log rule 2`
- [ ] `C-CF-7` `contract` The losing operation on one property is recorded with outcome `superseded`. `src: Core features, The operation log rule 2`
- [ ] `C-CF-8` `contract` An operation against a node an earlier operation deleted is recorded with outcome `discarded`. `src: Core features, The operation log rule 3`
- [ ] `C-CF-9` `contract` The response to a discarded operation names the member who deleted the node. `src: Core features, The operation log rule 3`
- [ ] `C-CF-10` `contract` A discarded operation is never silently dropped. `src: Core features, The operation log rule 3`
- [ ] `C-CF-11` `contract` Re-posting a known `op_id` returns the original `seq`. `src: Core features, The operation log rule 4`
- [ ] `C-CF-12` `contract` Re-posting a known `op_id` writes no second operation row. `src: Core features, The operation log rule 4`
- [ ] `C-CF-13` `contract` Re-posting a known `op_id` does not change the stored state a second time. `src: Core features, The operation log rule 4`
- [ ] `C-CF-14` `capability` A publish freezes one revision into an immutable build. `src: Core features, Publish and rollback rule 1`
- [ ] `C-CF-15` `capability` A publish renders a poster frame for the build. `src: Core features, Publish and rollback rule 1`
- [ ] `C-CF-16` `capability` A publish repoints the named channel at the new build. `src: Core features, Publish and rollback rule 1`
- [ ] `C-CF-17` `capability` A publish creates a public listing for the build. `src: Core features, Publish and rollback rule 1`
- [ ] `C-CF-18` `constraint` No build column changes after insert. `src: Core features, Publish and rollback rule 1`
- [ ] `C-CF-19` `constraint` A channel refers to exactly one current build, or to none. `src: Core features, Publish and rollback rule 2`
- [ ] `C-CF-20` `constraint` Two simultaneous publishes of one document to one channel do not both become current. `src: Core features, Publish and rollback rule 2`
- [ ] `C-CF-21` `constraint` The losing simultaneous publish is rejected. `src: Core features, Publish and rollback rule 2`
- [ ] `C-CF-22` `constraint` A rejected simultaneous publish leaves no orphaned build row. `src: Core features, Publish and rollback rule 2`
- [ ] `C-CF-23` `constraint` The single-current-build rule holds at the database level, never in application logic alone. `src: Core features, Publish and rollback rule 2`
- [ ] `C-CF-24` `capability` A rollback repoints the channel at an earlier build. `src: Core features, Publish and rollback rule 3`
- [ ] `C-CF-25` `contract` A rollback reaches every reader within ten seconds. `src: Core features, Publish and rollback rule 3`
- [ ] `C-CF-26` `capability` Unpublishing removes delivery within ten seconds. `src: Core features, Publish and rollback rule 3`
- [ ] `C-CF-27` `capability` Unpublishing removes the listing within ten seconds. `src: Core features, Publish and rollback rule 3`
- [ ] `C-CF-28` `constraint` Unpublishing never deletes the build. `src: Core features, Publish and rollback rule 3`
- [ ] `C-CF-29` `contract` `GET /api/runtime/{slug}` requires no credential. `src: Core features, The runtime address rule 1`
- [ ] `C-CF-30` `contract` `GET /api/runtime/{slug}` serves the exact bytes of the channel's current build. `src: Core features, The runtime address rule 1`
- [ ] `C-CF-31` `constraint` A channel with no current build is not served. `src: Core features, The runtime address rule 1`
- [ ] `C-CF-32` `literal` The seeded document `Menu Transition` has never been published. `src: Core features, The runtime address rule 2`
- [ ] `C-CF-33` `constraint` The revision bytes of an unpublished document sit in the object store. `src: Core features, The runtime address rule 2`
- [ ] `C-CF-34` `constraint` No unauthenticated route reaches the revision bytes of an unpublished document. `src: Core features, The runtime address rule 2`
- [ ] `C-CF-35` `constraint` `GET /api/listings` never returns an unpublished document in any ordering. `src: Core features, The runtime address rule 3`
- [ ] `C-CF-36` `constraint` `GET /api/listings` never returns an unpublished document for any search term. `src: Core features, The runtime address rule 3`
- [ ] `C-CF-37` `constraint` The unpublished-document exclusion holds for a signed-in caller, also for a signed-out one. `src: Core features, The runtime address rule 3`
- [ ] `C-CF-38` `role` An `editor` holds a seat. `src: Core features, Seats`
- [ ] `C-CF-39` `role` A `viewer` holds no seat; a pending invitation holds no seat. `src: Core features, Seats`
- [ ] `C-CF-40` `contract` The seat count is derived from the grants on read, never stored. `src: Core features, Seats`
- [ ] `C-CF-41` `literal` The workspace `Northlight Studio` caps seats at `3`. `src: Core features, Seats`
- [ ] `C-CF-42` `constraint` Accepting an invitation that would exceed the seat cap is refused. `src: Core features, Seats`
- [ ] `C-CF-43` `constraint` A refused acceptance holds the invitation at state `seat_blocked`. `src: Core features, Seats`
- [ ] `C-CF-44` `constraint` A refused acceptance writes no member row. `src: Core features, Seats`
- [ ] `C-CF-45` `constraint` A refused acceptance leaves the derived seat count unmoved. `src: Core features, Seats`
- [ ] `C-CF-46` `capability` A `viewer` invitation accepted at a full seat cap succeeds. `src: Core features, Seats`

## C-UF User flow

- [ ] `C-UF-1` `ui` The route `/m` serves the marketplace grid plus search, unauthenticated. `src: User flow route table`
- [ ] `C-UF-2` `ui` The route `/m/<handle>/<slug>` serves one playing listing, unauthenticated. `src: User flow route table`
- [ ] `C-UF-3` `ui` The route `/signup` serves open signup, unauthenticated. `src: User flow route table`
- [ ] `C-UF-4` `ui` The route `/login` serves sign-in, unauthenticated. `src: User flow route table`
- [ ] `C-UF-5` `ui` The route `/w` redirects to a readable folder. `src: User flow route table`
- [ ] `C-UF-6` `ui` The route `/w/files/<folder_id>` serves folders, documents, detail. `src: User flow route table`
- [ ] `C-UF-7` `ui` The route `/w/documents/new` creates a document, `editor` only. `src: User flow route table`
- [ ] `C-UF-8` `ui` The route `/w/d/<document_id>` serves artboards, timeline, states. `src: User flow route table`
- [ ] `C-UF-9` `ui` The route `/w/d/<document_id>/history` serves revisions plus restore. `src: User flow route table`
- [ ] `C-UF-10` `ui` The route `/w/d/<document_id>/publish` serves publish, rollback, unpublish, `editor` only. `src: User flow route table`
- [ ] `C-UF-11` `ui` The route `/w/members` serves members, roles, seats, invites, `editor` only. `src: User flow route table`
- [ ] `C-UF-12` `contract` A signed-out request for a `/w` route redirects to `/login`. `src: User flow, Entry and redirects`
- [ ] `C-UF-13` `contract` After sign-in the member lands on the route originally asked for. `src: User flow, Entry and redirects`
- [ ] `C-UF-14` `contract` Sign-in with no stored destination lands on `/w`. `src: User flow, Entry and redirects`
- [ ] `C-UF-15` `contract` Sign-out returns the member to `/m`. `src: User flow, Entry and redirects`
- [ ] `C-UF-16` `ui` A token expiring mid-action keeps the typed values on the page. `src: User flow, Entry and redirects`
- [ ] `C-UF-17` `ui` A token expiring mid-action offers a fresh sign-in. `src: User flow, Entry and redirects`
- [ ] `C-UF-18` `contract` A `viewer` reaching an `editor` route is refused, leaving state unchanged. `src: User flow, Entry and redirects`
- [ ] `C-UF-19` `ui` Searching `menu` on `/m` returns nothing. `src: User flow, Journeys journey 1`
- [ ] `C-UF-20` `ui` The listing route `/m/rae/loader-ring` opens for a signed-out visitor. `src: User flow, Journeys journey 1`
- [ ] `C-UF-21` `ui` A fresh signup lands the new member on an empty workspace. `src: User flow, Journeys journey 1`
- [ ] `C-UF-22` `ui` Creating the document `Hover Chip` in `Product UI` succeeds for `editor@example.com`. `src: User flow, Journeys journey 2`
- [ ] `C-UF-23` `ui` Two editors changing one property of one node both end on the higher `seq` value. `src: User flow, Journeys journey 3`
- [ ] `C-UF-24` `ui` The superseded editor is told which member won. `src: User flow, Journeys journey 3`
- [ ] `C-UF-25` `ui` Publishing the head revision to `loader-ring` makes the bytes readable signed out. `src: User flow, Journeys journey 4`
- [ ] `C-UF-26` `ui` A rollback surfaces the earlier bytes inside ten seconds. `src: User flow, Journeys journey 4`
- [ ] `C-UF-27` `ui` Inviting `editor4@example.com` as an `editor` at a full cap is refused. `src: User flow, Journeys journey 5`
- [ ] `C-UF-28` `ui` Every list surface carries an empty state naming the next action. `src: User flow, States`
- [ ] `C-UF-29` `ui` Every route carries a loading state. `src: User flow, States`
- [ ] `C-UF-30` `ui` A refusal raises an inline banner above the surface that raised the refusal. `src: User flow, States`
- [ ] `C-UF-31` `ui` The inline banner names what was refused, also why. `src: User flow, States`
- [ ] `C-UF-32` `ui` No page is replaced by an error page. `src: User flow, States`
- [ ] `C-UF-33` `ui` A document surface shows one of `draft`, `published`, `unshared changes`. `src: User flow, States`
- [ ] `C-UF-34` `ui` A listing tile shows a poster frame before the document loads. `src: User flow, States`

## C-UX UI/UX notes

- [ ] `C-UX-1` `ui` The interface reads as command-line: high contrast, technical, instrument-like. `src: UI/UX notes`
- [ ] `C-UX-2` `ui` The register is operational: quiet, built for scanning, no hero. `src: UI/UX notes`
- [ ] `C-UX-3` `ui` Type is monospace everywhere, with no proportional face. `src: UI/UX notes`
- [ ] `C-UX-4` `ui` A display voice sets capitals tracked open. `src: UI/UX notes`
- [ ] `C-UX-5` `ui` A body voice sets an ordinary stroke tracked normal. `src: UI/UX notes`
- [ ] `C-UX-6` `ui` The two type voices stay distinguishable at the smallest label size. `src: UI/UX notes`
- [ ] `C-UX-7` `ui` Motion character is instant, so a state change lands immediately. `src: UI/UX notes`
- [ ] `C-UX-8` `ui` Only the focus ring carries a duration. `src: UI/UX notes`
- [ ] `C-UX-9` `ui` Every transition names the properties animated. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Hover is a colour change, never a transform. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` Density is compact, so a full folder fits one screen. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` Panels separate by small luminance steps rather than by a border. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Saturated colour is confined to the product graphics, one primary action, three state colours. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` Contrast meets WCAG AA. `src: UI/UX notes`
- [ ] `C-UX-15` `ui` Every command has a keyboard route carrying a visible focus ring. `src: UI/UX notes`
- [ ] `C-UX-16` `ui` Icon-only controls carry labels. `src: UI/UX notes`
- [ ] `C-UX-17` `ui` Meaning is never carried by colour alone. `src: UI/UX notes`
- [ ] `C-UX-18` `ui` Every playing graphic carries a text alternative travelling with the document. `src: UI/UX notes`
- [ ] `C-UX-19` `ui` The layout holds at every width between the named tiers. `src: UI/UX notes`
- [ ] `C-UX-20` `ui` No route is twice as tall on a phone as on a desktop. `src: UI/UX notes`
- [ ] `C-UX-21` `ui` The product commits to dark, designing dark fully. `src: UI/UX notes`
- [ ] `C-UX-22` `ui` A light mode stays optional, never the default surface. `src: UI/UX notes`
- [ ] `C-UX-23` `ui` Every control carries resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes`
- [ ] `C-UX-24` `ui` An input shows a label plus an error in one fixed place. `src: UI/UX notes`
- [ ] `C-UX-25` `ui` A destructive action confirms before proceeding. `src: UI/UX notes`

## C-CN Constraints

- [ ] `C-CN-1` `constraint` One workspace per account. `src: Constraints`
- [ ] `C-CN-2` `constraint` A member never reads another workspace's rows. `src: Constraints`
- [ ] `C-CN-3` `constraint` No marketing route is built. `src: Constraints`
- [ ] `C-CN-4` `constraint` No desktop application, installer, download channel is built. `src: Constraints`
- [ ] `C-CN-5` `constraint` No plan, price, invoice, proration, metering, dunning is built. `src: Constraints`
- [ ] `C-CN-6` `constraint` No federated identity, no second factor is built. `src: Constraints`
- [ ] `C-CN-7` `constraint` No render pipeline, no batch export, no background job queue is built. `src: Constraints`
- [ ] `C-CN-8` `constraint` No customer-owned bucket, no data residency is built. `src: Constraints`
- [ ] `C-CN-9` `constraint` No assistant, no execution of member-supplied code is built. `src: Constraints`
- [ ] `C-CN-10` `constraint` No newsletter, no contact form, no outbound email is built. `src: Constraints`
- [ ] `C-CN-11` `constraint` No comment, direct message, notification, shared library is built. `src: Constraints`
- [ ] `C-CN-12` `constraint` No staged erasure, audit ledger, tracing, metrics pipeline is built. `src: Constraints`
- [ ] `C-CN-13` `constraint` No native mobile application is built. `src: Constraints`
- [ ] `C-CN-14` `constraint` No money appears anywhere in the product. `src: Constraints`
- [ ] `C-CN-15` `constraint` The application makes no external network call at run time beyond PostgreSQL, MinIO. `src: Constraints`
- [ ] `C-CN-16` `constraint` The application stays responsive at `2000` documents across `50` folders. `src: Constraints`
- [ ] `C-CN-17` `constraint` The application stays responsive at `200` revisions on one document. `src: Constraints`
- [ ] `C-CN-18` `constraint` The application stays responsive at `500` public listings. `src: Constraints`

## C-TR Technical requirements

- [ ] `C-TR-1` `contract` Every page's HTML is produced on the server, complete on first paint. `src: Technical requirements`
- [ ] `C-TR-2` `contract` A member with scripting disabled still reads folders, documents, revisions, members, marketplace. `src: Technical requirements`
- [ ] `C-TR-3` `contract` A member with scripting disabled can still follow every link. `src: Technical requirements`
- [ ] `C-TR-4` `contract` The JSON API is served on the same origin under `/api`. `src: Technical requirements`
- [ ] `C-TR-5` `contract` The front end is vanilla progressive enhancement, with no single-page application. `src: Technical requirements`
- [ ] `C-TR-6` `contract` Authentication is app-implemented email plus password with bearer tokens. `src: Technical requirements`
- [ ] `C-TR-7` `contract` `GET /api/health` returns `200` with no credential once seeding has finished. `src: Technical requirements`
- [ ] `C-TR-8` `literal` PostgreSQL is reached at `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-9` `literal` MinIO is reached at `STORAGE_ENDPOINT` with `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`. `src: Technical requirements`
- [ ] `C-TR-10` `contract` Paging on `GET /api/listings` uses an opaque cursor, never an offset. `src: Technical requirements`
- [ ] `C-TR-11` `contract` A page holds at most `24` items. `src: Technical requirements`
- [ ] `C-TR-12` `contract` The cursor returns in the `X-Next-Cursor` response header, absent on the last page. `src: Technical requirements`
- [ ] `C-TR-13` `contract` The featured ordering is snapshotted at the first page of a paging session. `src: Technical requirements`
- [ ] `C-TR-14` `contract` A paging reader never sees one listing on two pages, never skips one. `src: Technical requirements`
- [ ] `C-TR-15` `contract` `GET /api/listings?order=` accepts `featured`, `latest`, `for-hire`. `src: Technical requirements`
- [ ] `C-TR-16` `contract` The `latest` ordering sorts by `published_at` descending. `src: Technical requirements`
- [ ] `C-TR-17` `contract` The `for-hire` ordering restricts to authors whose `for_hire` is true. `src: Technical requirements`
- [ ] `C-TR-18` `contract` The featured ordering caps consecutive listings from one `handle` at one. `src: Technical requirements`
- [ ] `C-TR-19` `contract` Search covers title, handle, tags, server side, reflected in the address. `src: Technical requirements`
- [ ] `C-TR-20` `contract` A second like from one member leaves `like_count` where the first put the count. `src: Technical requirements`
- [ ] `C-TR-21` `contract` `like_count` moves in the same transaction as the like row. `src: Technical requirements`
- [ ] `C-TR-22` `contract` `GET /api/runtime/{slug}` answers with `Cache-Control: max-age=10`. `src: Technical requirements`
- [ ] `C-TR-23` `constraint` A failed publish leaves no orphaned build row, no listing without a build, no dangling channel. `src: Technical requirements`
- [ ] `C-TR-24` `contract` A client learns other members' operations from `GET /api/documents/{id}/operations?since=<seq>`. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-1` `data` All timestamps are UTC. `src: Data model`
- [ ] `C-DM-2` `literal` Every seeded account logs in with the literal password `deku-demo-pw-2026`. `src: Data model`
- [ ] `C-DM-3` `contract` The password literal is written into `/app/USER_README.md` beside each account. `src: Data model`
- [ ] `C-DM-4` `data` `workspace` carries `id`, `name`, `slug`, `seat_cap`, `created_at`, with `slug` unique. `src: Data model`
- [ ] `C-DM-5` `data` `member` carries `email`, `display_name`, `handle`, `password_hash`, `status`, `for_hire`. `src: Data model`
- [ ] `C-DM-6` `constraint` `member.email` is unique; `member.handle` is unique. `src: Data model`
- [ ] `C-DM-7` `constraint` A `handle` never changes once a listing carries the handle. `src: Data model`
- [ ] `C-DM-8` `contract` An explicit `deny` grant at any level defeats an allow at every level. `src: Data model`
- [ ] `C-DM-9` `contract` The most specific grant wins, so a document grant beats a folder grant. `src: Data model`
- [ ] `C-DM-10` `data` `invitation.state` takes `invited`, `accepted`, `seat_blocked`, `expired`, `revoked`. `src: Data model`
- [ ] `C-DM-11` `data` `animation.frame_count` is an integer count of frames, never a duration in seconds. `src: Data model`
- [ ] `C-DM-12` `data` `transition.index` is the declaration order deciding which transition wins. `src: Data model`
- [ ] `C-DM-13` `constraint` `operation.seq` is unique per document, strictly increasing. `src: Data model`
- [ ] `C-DM-14` `constraint` `operation.op_id` is unique per document. `src: Data model`
- [ ] `C-DM-15` `data` `operation.outcome` takes `applied`, `superseded`, `discarded`. `src: Data model`
- [ ] `C-DM-16` `constraint` `revision.content_hash` is the lowercase SHA-256 hex of the bytes at `object_key`. `src: Data model`
- [ ] `C-DM-17` `constraint` Materialising a revision whose hash equals the head's creates no revision. `src: Data model`
- [ ] `C-DM-18` `constraint` No `revision_parent` row is ever deleted, nor rewritten. `src: Data model`
- [ ] `C-DM-19` `capability` A restore inserts a new revision carrying two parent rows. `src: Data model`
- [ ] `C-DM-20` `constraint` Every revision made after a restored revision stays reachable. `src: Data model`
- [ ] `C-DM-21` `constraint` A `build` row is immutable after insert. `src: Data model`
- [ ] `C-DM-22` `constraint` `channel.slug` is unique; `channel.state` takes `live` or `unpublished`. `src: Data model`
- [ ] `C-DM-23` `constraint` `listing.visibility` is `public` only during a `live` channel state. `src: Data model`
- [ ] `C-DM-24` `constraint` `listing_like` is unique on the listing plus member pair. `src: Data model`
- [ ] `C-DM-25` `capability` A soft-deleted document sets `deleted_at`, staying recoverable from a trash surface. `src: Data model`
- [ ] `C-DM-26` `capability` A recovered document returns to the original folder where the folder still exists. `src: Data model`
- [ ] `C-DM-27` `constraint` A revision is never deleted. `src: Data model`
- [ ] `C-DM-28` `constraint` A build is never deleted during a channel reference. `src: Data model`
- [ ] `C-DM-29` `constraint` A member who authored a revision is deactivated rather than deleted. `src: Data model`
- [ ] `C-DM-30` `contract` The seat count is the number of distinct `active` members holding an `editor` grant, computed on read. `src: Data model`
- [ ] `C-DM-31` `contract` The `unshared changes` state compares a document head revision against the channel's current build. `src: Data model`
- [ ] `C-DM-32` `literal` A revision's bytes live at `documents/{document_id}/{sha256_of_bytes}.mot`. `src: Data model`
- [ ] `C-DM-33` `literal` A poster frame lives at `posters/{build_id}/{sha256_of_bytes}.svg`. `src: Data model`
- [ ] `C-DM-34` `constraint` A document's bytes exist nowhere but the object store. `src: Data model`
- [ ] `C-DM-35` `constraint` No stored object exceeds `10485760` bytes. `src: Data model`
- [ ] `C-DM-36` `literal` The seeded workspace is `Northlight Studio`, slug `northlight`, `seat_cap` `3`. `src: Data model`
- [ ] `C-DM-37` `literal` The seeded folders are `Product UI`, `Game UI`, `Broadcast`. `src: Data model`
- [ ] `C-DM-38` `literal` The seeded published documents are `Loader Ring`, `Match Ticker`. `src: Data model`
- [ ] `C-DM-39` `literal` The seeded artboards are `Ring`, `Ring Compact`, `Menu`, `Ticker`. `src: Data model`
- [ ] `C-DM-40` `literal` The seeded animations are `Spin` at `120` frames, `Slide` at `45` frames, `Crawl` at `600` frames. `src: Data model`
- [ ] `C-DM-41` `literal` The seeded state machine carries states `Idle`, `Loading`, `Done`. `src: Data model`
- [ ] `C-DM-42` `literal` The seeded inputs are `progress`, `complete`, `tap`. `src: Data model`
- [ ] `C-DM-43` `literal` The seeded listings hold `like_count` `23` for `loader-ring`, `623` for `match-ticker`. `src: Data model`
- [ ] `C-DM-44` `constraint` Seeding is idempotent, so restarting duplicates no row. `src: Data model`
- [ ] `C-DM-45` `constraint` The seat contradiction in the source is resolved rather than reproduced. `src: Data model`

## C-FE Front-end specification

- [ ] `C-FE-1` `ui` Navigation is a top-nav of four items: Files, Marketplace, Members, account. `src: Front-end specification, Information architecture`
- [ ] `C-FE-2` `ui` A searchable command palette opens on a keyboard shortcut, reaching every command. `src: Front-end specification, Information architecture`
- [ ] `C-FE-3` `ui` The work surface is a split detail pane: tree plus list left, detail right. `src: Front-end specification, Information architecture`
- [ ] `C-FE-4` `ui` Creating a document is a dedicated route rather than a layer. `src: Front-end specification, Information architecture`
- [ ] `C-FE-5` `ui` Feedback is an inline banner above the raising surface, never a toast. `src: Front-end specification, Information architecture`
- [ ] `C-FE-6` `literal` The ground ramp runs `#000000`, `#0b0b0b`, `#0f0f0f`, `#111111`, `#1b1b1b`, `#1d1d1d`, `#222222`, `#242424`, `#282828`, `#303030`, `#323232`. `src: Front-end specification, Colour: the ground`
- [ ] `C-FE-7` `constraint` No component adds a border to compensate for a subtle luminance step. `src: Front-end specification, Colour: the ground`
- [ ] `C-FE-8` `literal` The text ramp runs `#ffffff`, `#f1f1f1`, `#dddddd`, `#cccccc`, `#aaaaaa`, `#8c8c8c`, `#888888`, `#666666`, `#444444`. `src: Front-end specification, Colour: text`
- [ ] `C-FE-9` `literal` The accent set is `rgb(255, 164, 28)`, `#f6c566`, `#57a5e0`, `#33a7ff`, `#4cbe9c`, `#ff3b58`. `src: Front-end specification, Colour: accent and semantic`
- [ ] `C-FE-10` `ui` One saturated fill appears per viewport, never two. `src: Front-end specification, Colour: accent and semantic`
- [ ] `C-FE-11` `constraint` `#666666` is never a body-text colour on `#0b0b0b`. `src: Front-end specification, Contrast`
- [ ] `C-FE-12` `constraint` `#444444` is correct for disabled controls alone. `src: Front-end specification, Contrast`
- [ ] `C-FE-13` `ui` The spectrum sweep interpolates in a perceptual colour space, never a linear one. `src: Front-end specification, The spectrum sweep`
- [ ] `C-FE-14` `ui` The spectrum gradient translates across the text rather than recolouring the text. `src: Front-end specification, The spectrum sweep`
- [ ] `C-FE-15` `ui` Published work is shown on a transparency checkerboard at `12px` radius. `src: Front-end specification, The checkerboard and depth`
- [ ] `C-FE-16` `ui` The type scale runs `micro` through `heading` at the pinned sizes, weights, line-heights. `src: Front-end specification, Typefaces and the type scale`
- [ ] `C-FE-17` `ui` The wordmark plus eyebrow are tracked open at roughly four times the natural advance. `src: Front-end specification, Letter-spacing`
- [ ] `C-FE-18` `ui` Body copy is never tracked. `src: Front-end specification, Letter-spacing`
- [ ] `C-FE-19` `ui` Five radius values cover the product: `8px`, `10px`, `5px`, `4px`, `3px`. `src: Front-end specification, Radius, spacing and density`
- [ ] `C-FE-20` `ui` The chevron is the path `M5.5 6.5L7.5 8.5L9.5 6.5` in a `0 0 15 15` box. `src: Front-end specification, Iconography`
- [ ] `C-FE-21` `ui` Three control styles exist: primary, ghost, pill. `src: Front-end specification, Chrome and controls`
- [ ] `C-FE-22` `ui` The ghost control's ring brightens further than the ghost control's fill. `src: Front-end specification, Chrome and controls`
- [ ] `C-FE-23` `ui` The in-content link moves text plus both pseudo-elements together. `src: Front-end specification, Chrome and controls`
- [ ] `C-FE-24` `ui` The underline is drawn across rather than switched on. `src: Front-end specification, Chrome and controls`
- [ ] `C-FE-25` `ui` `Escape` closes any layer, returning focus to the trigger. `src: Front-end specification, Chrome and controls`
- [ ] `C-FE-26` `ui` The header scrolls away with the page, never returning on scroll up. `src: Front-end specification, Chrome and controls`
- [ ] `C-FE-27` `ui` Four easing curves cover the product; a fifth is never invented. `src: Front-end specification, Motion`
- [ ] `C-FE-28` `constraint` `transition: all` is never declared. `src: Front-end specification, Motion`
- [ ] `C-FE-29` `constraint` Every hover state sits inside a fine-pointer hover query. `src: Front-end specification, Motion`
- [ ] `C-FE-30` `constraint` Every continuous animation sits inside `(prefers-reduced-motion: no-preference)`. `src: Front-end specification, Motion`
- [ ] `C-FE-31` `constraint` Nothing plays an entrance on scroll, nor is scrubbed against scroll position. `src: Front-end specification, Motion`
- [ ] `C-FE-32` `contract` One player component draws every playing document on a surface. `src: Front-end specification, The playback surface`
- [ ] `C-FE-33` `contract` The same document plus start state plus timestamped inputs produce byte-identical frames. `src: Front-end specification, The playback surface`
- [ ] `C-FE-34` `contract` The player advances by a supplied elapsed time, never reading a clock. `src: Front-end specification, The playback surface`
- [ ] `C-FE-35` `contract` Artwork is rasterised at the device pixel ratio, re-rasterised on ratio change. `src: Front-end specification, The playback surface`
- [ ] `C-FE-36` `contract` A document outside the viewport is suspended, resuming at the held state. `src: Front-end specification, The playback surface`
- [ ] `C-FE-37` `contract` Exceeding the frame budget drops documents furthest from the viewport centre first. `src: Front-end specification, The playback surface`
- [ ] `C-FE-38` `contract` Every embedding shows a poster frame, so nothing is ever a blank rectangle. `src: Front-end specification, The playback surface`
- [ ] `C-FE-39` `contract` Transition conditions are evaluated in declaration order; the first satisfied one wins. `src: Front-end specification, The state machine at runtime`
- [ ] `C-FE-40` `contract` A trigger input is consumed by exactly one evaluation, then cleared. `src: Front-end specification, The state machine at runtime`
- [ ] `C-FE-41` `contract` A transition cannot be taken before the exit time fraction. `src: Front-end specification, The state machine at runtime`
- [ ] `C-FE-42` `contract` Setting an input is queued, applied at the next advance. `src: Front-end specification, The state machine at runtime`
- [ ] `C-FE-43` `contract` A missing bound property falls back to the authored value. `src: Front-end specification, The state machine at runtime`
- [ ] `C-FE-44` `ui` The document surface carries five resizable regions persisted per member per document. `src: Front-end specification, The document surface`
- [ ] `C-FE-45` `ui` The Design mode edits a resting value; the Animate mode writes a keyframe at the playhead. `src: Front-end specification, The document surface`
- [ ] `C-FE-46` `ui` The canvas carries an unmistakable visual treatment during Animate mode. `src: Front-end specification, The document surface`
- [ ] `C-FE-47` `ui` The hierarchy tree is virtualised, scrolling ten thousand nodes at the display rate. `src: Front-end specification, The document surface`
- [ ] `C-FE-48` `ui` Canvas handles hold a constant screen size regardless of zoom. `src: Front-end specification, The document surface`
- [ ] `C-FE-49` `ui` Selection hit-tests rendered geometry rather than a bounding box. `src: Front-end specification, The document surface`
- [ ] `C-FE-50` `ui` A whole scrub gesture produces one undo entry. `src: Front-end specification, The document surface`
- [ ] `C-FE-51` `contract` Undo reverses the member's own most recent un-undone operation, never another member's. `src: Front-end specification, The document surface`
- [ ] `C-FE-52` `contract` An undo whose target no longer exists is refused with a reason. `src: Front-end specification, The document surface`
- [ ] `C-FE-53` `ui` A document tile shows poster, title, edited-at meta, state chip. `src: Front-end specification, The workspace surface`
- [ ] `C-FE-54` `ui` The document list sorts by edited-at descending by default, persisted per member. `src: Front-end specification, The workspace surface`
- [ ] `C-FE-55` `constraint` A breadcrumb elides folders above a member's grant, leaking no name. `src: Front-end specification, The workspace surface`
- [ ] `C-FE-56` `ui` The marketplace carries a search field, three tabs, one pill control. `src: Front-end specification, The marketplace surface`
- [ ] `C-FE-57` `ui` The marketplace footer carries a copyright line computed rather than typed. `src: Front-end specification, The marketplace surface`
- [ ] `C-FE-58` `ui` A marketplace tile is a link with a real address covering the whole tile. `src: Front-end specification, The marketplace surface`
- [ ] `C-FE-59` `ui` Like counts render as integers to `999`, then one decimal with a thousands suffix. `src: Front-end specification, The marketplace surface`
- [ ] `C-FE-60` `constraint` The `document` module depends on no renderer, no transport, no service layer. `src: Front-end specification, Module boundaries`
- [ ] `C-FE-61` `constraint` The public surface shares no bundle with the workspace surface. `src: Front-end specification, Module boundaries`
- [ ] `C-FE-62` `ui` Three breakpoints carry the layout at `600px`, `800px`, `1024px`. `src: Front-end specification, Responsive behaviour`
- [ ] `C-FE-63` `ui` The layout sets a floor below `375px`, capping the container above `2200px`. `src: Front-end specification, Responsive behaviour`
- [ ] `C-FE-64` `constraint` Nothing drags the page sideways at any width. `src: Front-end specification, Responsive behaviour`
- [ ] `C-FE-65` `ui` A `2px` focus outline at `#ffffff` offset `2px` is the focus indicator. `src: Front-end specification, Accessibility`
- [ ] `C-FE-66` `ui` Focus order follows reading order on every route. `src: Front-end specification, Accessibility`
- [ ] `C-FE-67` `ui` A decorative document is marked as such, skipped entirely. `src: Front-end specification, Accessibility`
- [ ] `C-FE-68` `constraint` Duplicated markup is never used to produce a visual effect. `src: Front-end specification, Accessibility`
- [ ] `C-FE-69` `constraint` The renderer module never blocks a route's first paint. `src: Front-end specification, Performance`
- [ ] `C-FE-70` `constraint` A document failing to load leaves the poster frame in place permanently. `src: Front-end specification, Performance`
- [ ] `C-FE-71` `constraint` No video ships with the build. `src: Front-end specification, Performance`
- [ ] `C-FE-72` `constraint` No photograph, typeface file, icon file, animation document ships with the build. `src: Front-end specification, Zero assets`
- [ ] `C-FE-73` `ui` Component classes follow `mote-<component>`; custom properties follow `--mote-<token>`. `src: Front-end specification, Naming conventions`
- [ ] `C-FE-74` `ui` A separator inside a heading is typographic, never pictographic. `src: Front-end specification, The marketplace surface`
- [ ] `C-FE-75` `constraint` No asset manifest ships, nor a reference to an asset file. `src: Front-end specification, Zero assets`

## C-DC Deployment contract

- [ ] `C-DC-1` `contract` The application is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-2` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract`
- [ ] `C-DC-3` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-4` `contract` `GET /api/health` returns `200` once the application is ready. `src: Deployment contract`
- [ ] `C-DC-5` `contract` The application starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-6` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-7` `contract` Reserved `.browser_screenshots/` plus `.downloads/` directories exist at the app root, empty. `src: Deployment contract`
- [ ] `C-DC-8` `contract` A production build is served behind a static or preview server, never a dev server. `src: Deployment contract`
- [ ] `C-DC-9` `contract` The server keeps running after the session ends, never as a child of the shell. `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server binds `0.0.0.0`, never `127.0.0.1`, never `localhost`. `src: Deployment contract`
- [ ] `C-DC-11` `constraint` The backing services are already running, so nothing downloads, installs, compiles, starts a copy. `src: Deployment contract`
- [ ] `C-DC-12` `constraint` No edge function is used. `src: Deployment contract`
- [ ] `C-DC-13` `constraint` No persistent volume, no fixed container name, no custom network is used. `src: Deployment contract`
- [ ] `C-DC-14` `contract` `POST /api/auth/signup` accepts `email`, `password`, `display_name`, `handle`. `src: Deployment contract, API shapes`
- [ ] `C-DC-15` `contract` `POST /api/auth/login` returns `token` plus `member_id`. `src: Deployment contract, API shapes`
- [ ] `C-DC-16` `contract` `POST /api/documents/{id}/operations` returns `seq`, `outcome`, `discarded_by`. `src: Deployment contract, API shapes`
- [ ] `C-DC-17` `contract` `POST /api/documents/{id}/revisions` returns `id`, `content_hash`, `object_key`, `parent_revision_ids`, `created`. `src: Deployment contract, API shapes`
- [ ] `C-DC-18` `contract` `POST /api/documents/{id}/publish` returns `build_id`, `channel_slug`, `content_hash`, `object_key`, `poster_key`, `listing_id`. `src: Deployment contract, API shapes`
- [ ] `C-DC-19` `contract` `POST /api/channels/{slug}/rollback` returns `channel_slug` plus `current_build_id`. `src: Deployment contract, API shapes`
- [ ] `C-DC-20` `contract` `GET /api/listings` returns a top-level array carrying `X-Next-Cursor`. `src: Deployment contract, API shapes`
- [ ] `C-DC-21` `contract` `POST /api/invitations/{token}/accept` returns `state` plus `member_id`. `src: Deployment contract, API shapes`
- [ ] `C-DC-22` `contract` Every list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes`
- [ ] `C-DC-23` `contract` Bearer auth is required everywhere except health, signup, login, listings, runtime. `src: Deployment contract, API shapes`
- [ ] `C-DC-24` `contract` An invalid or unauthorized call is rejected as a client error, never a `5xx`, never a silent success. `src: Deployment contract, API shapes`
- [ ] `C-DC-25` `constraint` An in-memory dictionary standing in for stored documents is a contract violation. `src: Deployment contract, No mocks`
- [ ] `C-DC-26` `constraint` Document bytes written to the app container filesystem are a contract violation. `src: Deployment contract, No mocks`
- [ ] `C-DC-27` `constraint` A listing feed served from a fixture file is a contract violation. `src: Deployment contract, No mocks`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the corpus password | `C-DM-2` |
| `editor@example.com` | the first seeded editor | `C-RL-15` |
| `editor2@example.com` | the second seeded editor | `C-RL-15` |
| `editor3@example.com` | the third seeded editor | `C-RL-15` |
| `viewer@example.com` | the seeded viewer | `C-RL-16` |
| `Broadcast` | the folder granted to the viewer | `C-RL-16` |
| `Menu Transition` | the never-published document | `C-CF-32` |
| `Northlight Studio` | the seeded workspace | `C-CF-41` |
| `3` | the seat cap | `C-CF-41` |
| `DATABASE_URL` | the PostgreSQL connection variable | `C-TR-8` |
| `STORAGE_ENDPOINT` | the object store endpoint variable | `C-TR-9` |
| `STORAGE_BUCKET` | the object store bucket variable | `C-TR-9` |
| `STORAGE_ACCESS_KEY` | the object store access key variable | `C-TR-9` |
| `STORAGE_SECRET_KEY` | the object store secret key variable | `C-TR-9` |
| `APP_PUBLIC_URL` | the application address variable | `C-TR-15` |
| `APP_PUBLIC_PORT` | the outside port variable | `C-TR-15` |
| `documents/{document_id}/{sha256_of_bytes}.mot` | the revision object key scheme | `C-DM-32` |
| `posters/{build_id}/{sha256_of_bytes}.svg` | the poster object key scheme | `C-DM-33` |
| `10485760` | the object size cap in bytes | `C-DM-35` |
| `northlight` | the workspace slug | `C-DM-36` |
| `seat_cap` | the seat cap column | `C-DM-36` |
| `Product UI` | the first seeded folder | `C-DM-37` |
| `Game UI` | the second seeded folder | `C-DM-37` |
| `Loader Ring` | the first published document | `C-DM-38` |
| `Match Ticker` | the second published document | `C-DM-38` |
| `Ring` | the first seeded artboard | `C-DM-39` |
| `Ring Compact` | the second seeded artboard | `C-DM-39` |
| `Menu` | the third seeded artboard | `C-DM-39` |
| `Ticker` | the fourth seeded artboard | `C-DM-39` |
| `Spin` | the animation on `Ring` | `C-DM-40` |
| `120` | the frame count of `Spin` | `C-DM-40` |
| `Slide` | the animation on `Menu` | `C-DM-40` |
| `45` | the frame count of `Slide` | `C-DM-40` |
| `Crawl` | the animation on `Ticker` | `C-DM-40` |
| `600` | the frame count of `Crawl` | `C-DM-40` |
| `Idle` | the first state machine node | `C-DM-41` |
| `Loading` | the second state machine node | `C-DM-41` |
| `Done` | the third state machine node | `C-DM-41` |
| `progress` | the number input | `C-DM-42` |
| `complete` | the boolean input | `C-DM-42` |
| `tap` | the trigger input | `C-DM-42` |
| `like_count` | the materialised like total | `C-DM-43` |
| `23` | the seeded like total for `loader-ring` | `C-DM-43` |
| `loader-ring` | the channel slug of `Loader Ring` | `C-DM-43` |
| `623` | the seeded like total for `match-ticker` | `C-DM-43` |
| `match-ticker` | the channel slug of `Match Ticker` | `C-DM-43` |
| `2000` | the document volume target | `C-CN-16` |
| `50` | the folder volume target | `C-CN-16` |
| `200` | the revision volume target | `C-CN-17` |
| `500` | the listing volume target | `C-CN-18` |
| `24` | the marketplace page size | `C-TR-11` |
| `X-Next-Cursor` | the cursor response header | `C-TR-12` |
| `featured` | the editorial ordering | `C-TR-15` |
| `latest` | the recency ordering | `C-TR-15` |
| `for-hire` | the commissions ordering | `C-TR-15` |
| `published_at` | the listing publication timestamp | `C-TR-16` |
| `for_hire` | the member commissions flag | `C-TR-17` |
| `handle` | the author handle column | `C-TR-18` |
| `Cache-Control: max-age=10` | the runtime cache directive | `C-TR-22` |
| `200` | the health status | `C-TR-7` |
| `/api` | the API prefix | `C-TR-4` |
| `#000000` | the void step | `C-FE-6` |
| `#0b0b0b` | the ground step | `C-FE-6` |
| `#0f0f0f` | the alternating band step | `C-FE-6` |
| `#111111` | the raised panel step | `C-FE-6` |
| `#1b1b1b` | the card step | `C-FE-6` |
| `#1d1d1d` | the field step | `C-FE-6` |
| `#222222` | the field hover step | `C-FE-6` |
| `#242424` | the pressed row step | `C-FE-6` |
| `#282828` | the checkerboard step | `C-FE-6` |
| `#303030` | the focus edge step | `C-FE-6` |
| `#323232` | the divider step | `C-FE-6` |
| `#ffffff` | the primary text value | `C-FE-8` |
| `#f1f1f1` | the light text value | `C-FE-8` |
| `#dddddd` | the strong text value | `C-FE-8` |
| `#cccccc` | the numeric text value | `C-FE-8` |
| `#aaaaaa` | the muted text value | `C-FE-8` |
| `#8c8c8c` | the dim text value | `C-FE-8` |
| `#888888` | the default text value | `C-FE-8` |
| `#666666` | the faint text value | `C-FE-8` |
| `#444444` | the disabled text value | `C-FE-8` |
| `rgb(255, 164, 28)` | the primary call-to-action fill | `C-FE-9` |
| `#f6c566` | the eyebrow mark colour | `C-FE-9` |
| `#57a5e0` | the in-content link colour | `C-FE-9` |
| `#33a7ff` | the workspace primary colour | `C-FE-9` |
| `#4cbe9c` | the affirmative colour | `C-FE-9` |
| `#ff3b58` | the negative colour | `C-FE-9` |
| `12px` | the tile radius | `C-FE-15` |
| `8px` | the dominant radius | `C-FE-19` |
| `10px` | the media panel radius | `C-FE-19` |
| `5px` | the small control radius | `C-FE-19` |
| `4px` | the input radius | `C-FE-19` |
| `3px` | the placeholder radius | `C-FE-19` |
| `M5.5 6.5L7.5 8.5L9.5 6.5` | the chevron path | `C-FE-20` |
| `0 0 15 15` | the chevron box | `C-FE-20` |
| `transition: all` | the banned transition shorthand | `C-FE-28` |
| `(hover:hover) and (pointer:fine)` | the pointer query | `C-FE-29` |
| `(prefers-reduced-motion: no-preference)` | the motion query | `C-FE-30` |
| `999` | the like count formatting threshold | `C-FE-59` |
| `600px` | the two-column breakpoint | `C-FE-62` |
| `800px` | the primary desktop breakpoint | `C-FE-62` |
| `1024px` | the three-column breakpoint | `C-FE-62` |
| `375px` | the layout floor | `C-FE-63` |
| `2200px` | the container cap | `C-FE-63` |
| `2px` | the focus outline width | `C-FE-65` |
| `mote-<component>` | the component class convention | `C-FE-73` |
| `--mote-<token>` | the custom property convention | `C-FE-73` |
| `${APP_PUBLIC_PORT}:4173` | the port mapping | `C-DC-2` |
| `/app/USER_README.md` | the credentials file | `C-DC-6` |
| `.browser_screenshots/` | the reserved screenshot directory | `C-DC-7` |
| `.downloads/` | the reserved download directory | `C-DC-7` |
| `0.0.0.0` | the bind address | `C-DC-10` |
| `127.0.0.1` | the forbidden loopback address | `C-DC-10` |
| `localhost` | the forbidden loopback name | `C-DC-10` |
| `email` | the signup address field | `C-DC-14` |
| `password` | the signup secret field | `C-DC-14` |
| `display_name` | the signup name field | `C-DC-14` |
| `token` | the login bearer field | `C-DC-15` |
| `member_id` | the login member field | `C-DC-15` |
| `seq` | the operation sequence field | `C-DC-16` |
| `outcome` | the operation outcome field | `C-DC-16` |
| `discarded_by` | the deleting member field | `C-DC-16` |
| `id` | the revision identifier field | `C-DC-17` |
| `content_hash` | the revision hash field | `C-DC-17` |
| `object_key` | the revision object field | `C-DC-17` |
| `parent_revision_ids` | the revision parents field | `C-DC-17` |
| `created` | the revision creation flag | `C-DC-17` |
| `build_id` | the publish build field | `C-DC-18` |
| `channel_slug` | the publish channel field | `C-DC-18` |
| `poster_key` | the publish poster field | `C-DC-18` |
| `listing_id` | the publish listing field | `C-DC-18` |
| `current_build_id` | the channel current build field | `C-DC-19` |
| `state` | the invitation state field | `C-DC-21` |
| `5xx` | the forbidden server error class | `C-DC-24` |
| `op_id` | the client operation identifier | `C-CF-1` |
| `applied` | the accepted operation outcome | `C-CF-5` |
| `superseded` | the losing operation outcome | `C-CF-7` |
| `discarded` | the deleted-target operation outcome | `C-CF-8` |
| `seat_blocked` | the held invitation state | `C-CF-43` |
| `editor` | the writing role | `C-RL-1` |
| `viewer` | the reading role | `C-RL-1` |
| `GET /api/runtime/{slug}` | the runtime address | `C-CF-29` |
| `GET /api/listings` | the marketplace feed | `C-CF-35` |
| `deny` | the refusing grant flag | `C-DM-8` |
| `invited` | the pending invitation state | `C-DM-10` |
| `accepted` | the joined invitation state | `C-DM-10` |
| `expired` | the lapsed invitation state | `C-DM-10` |
| `revoked` | the withdrawn invitation state | `C-DM-10` |
| `live` | the serving channel state | `C-DM-22` |
| `unpublished` | the withdrawn channel state | `C-DM-22` |
| `public` | the visible listing state | `C-DM-23` |
| `active` | the joined member status | `C-DM-30` |
| `unshared changes` | the drifted document chip | `C-DM-31` |
| `deleted_at` | the soft deletion column | `C-DM-25` |
| `/m` | the marketplace route | `C-UF-1` |
| `/m/<handle>/<slug>` | the listing route | `C-UF-2` |
| `/signup` | the signup route | `C-UF-3` |
| `/login` | the sign-in route | `C-UF-4` |
| `/w` | the workspace root route | `C-UF-5` |
| `/w/files/<folder_id>` | the file browser route | `C-UF-6` |
| `/w/documents/new` | the document create route | `C-UF-7` |
| `/w/d/<document_id>` | the document surface route | `C-UF-8` |
| `/w/d/<document_id>/history` | the revision route | `C-UF-9` |
| `/w/d/<document_id>/publish` | the publish route | `C-UF-10` |
| `/w/members` | the members route | `C-UF-11` |
| `menu` | the search term returning nothing | `C-UF-19` |
| `/m/rae/loader-ring` | the seeded listing address | `C-UF-20` |
| `Hover Chip` | the document created in journey 2 | `C-UF-22` |
| `editor4@example.com` | the invitation address refused at the cap | `C-UF-27` |
| `draft` | the unpublished document chip | `C-UF-33` |
| `published` | the published document chip | `C-UF-33` |
| `GET /api/health` | the health endpoint | `C-TR-7` |
| `X` | the inspector horizontal field | `C-FE-44` |
| `Y` | the inspector vertical field | `C-FE-44` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the bearer token lifetime | `C-TR-6` |
| the recovery window for a soft-deleted document | `C-DM-25` |
| the frame budget per page | `C-FE-37` |
| the command palette keyboard shortcut | `C-FE-2` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 1 | 8 |
| User roles | 1 | 17 |
| Core features | 6 | 46 |
| User flow | 6 | 34 |
| UI/UX notes | 1 | 25 |
| Constraints | 0 | 18 |
| Technical requirements | 5 | 24 |
| Data model | 6 | 45 |
| Front-end specification | 13 | 75 |
| Deployment contract | 10 | 27 |
