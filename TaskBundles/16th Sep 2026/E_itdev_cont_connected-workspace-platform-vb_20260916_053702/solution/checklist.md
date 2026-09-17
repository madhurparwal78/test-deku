# Checklist: Meridian Workspace

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract
Sections absent: buildplan
Items: 400
Unpinned values flagged: 1

## C-OV Overview

- [ ] `C-OV-01` `capability` The app keeps documents, tracked records, a public face in one workspace. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app presents a page as an ordered tree of typed blocks. `src: Overview para 2`
- [ ] `C-OV-03` `capability` The app presents a database as a page whose children share a property schema. `src: Overview para 2`
- [ ] `C-OV-04` `capability` The app presents a teamspace as the container carrying the default access a page inherits. `src: Overview para 2`
- [ ] `C-OV-05` `constraint` The app places every page in exactly one teamspace. `src: Overview para 3`
- [ ] `C-OV-06` `data` The app records a membership as a relation carrying a role, a granted time. `src: Overview para 3`
- [ ] `C-OV-07` `constraint` The app omits realtime cursors, presence, comments, mentions from the product. `src: Overview para 5`
- [ ] `C-OV-08` `constraint` The app omits billing, federated sign-in, automations from the product. `src: Overview para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` An admin reads every teamspace in the workspace. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An admin reads the activity record. `src: User roles table row 1`
- [ ] `C-RL-03` `role` An admin changes a teamspace access mode. `src: User roles table row 1`
- [ ] `C-RL-04` `constraint` The app refuses an admin request to modify an activity record row. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A member reads a page in an open teamspace. `src: User roles table row 2`
- [ ] `C-RL-06` `constraint` The app refuses a member request to read a private teamspace. `src: User roles table row 2`
- [ ] `C-RL-07` `constraint` The app refuses a member request to read a page carrying an explicit deny for that member. `src: User roles table row 2`
- [ ] `C-RL-08` `constraint` The app refuses a member request to any admin endpoint. `src: User roles table row 2`
- [ ] `C-RL-09` `constraint` The app refuses a member request to change a grant. `src: User roles table row 2`
- [ ] `C-RL-10` `role` A guest reads only the pages explicitly granted to that guest. `src: User roles table row 3`
- [ ] `C-RL-11` `constraint` The app omits a database property hidden from guests from a guest response. `src: User roles table row 3`
- [ ] `C-RL-12` `constraint` The app enforces authorization server side on every mutating endpoint. `src: User roles, enforcement paragraph`
- [ ] `C-RL-13` `constraint` The app refuses a direct request for a page the calling principal may not read. `src: User roles, enforcement paragraph`
- [ ] `C-RL-14` `constraint` The app refuses a request for a private teamspace the way a non-existent teamspace is refused. `src: User roles, enforcement paragraph`
- [ ] `C-RL-15` `constraint` The app offers no signup surface. `src: User roles para 1`
- [ ] `C-RL-16` `literal` The app seeds the account `admin@example.com` with the role admin. `src: User roles, seeded accounts table`
- [ ] `C-RL-17` `literal` The app seeds the account `member@example.com` with the role member. `src: User roles, seeded accounts table`
- [ ] `C-RL-18` `literal` The app seeds the account `member2@example.com` with the role member. `src: User roles, seeded accounts table`
- [ ] `C-RL-19` `literal` The app seeds the account `guest@example.com` with the role guest. `src: User roles, seeded accounts table`
- [ ] `C-RL-20` `literal` The app names the group `Editors` as a grant subject holding one member. `src: User roles, final paragraph`

## C-CF Core features

- [ ] `C-CF-01` `literal` The app accepts an address at `/api/auth/identify`. `src: Core features, Auth rule 1`
- [ ] `C-CF-02` `constraint` The app returns an identical identify response body for a known address, an unknown address. `src: Core features, Auth rule 1`
- [ ] `C-CF-03` `constraint` The app returns an identical identify response status for a known address, an unknown address. `src: Core features, Auth rule 1`
- [ ] `C-CF-04` `literal` The app accepts email, password at `/api/auth/login`. `src: Core features, Auth rule 2`
- [ ] `C-CF-05` `capability` The app returns a bearer token on a successful login. `src: Core features, Auth rule 2`
- [ ] `C-CF-06` `constraint` The app rejects a wrong password with no hint about whether the address exists. `src: Core features, Auth rule 2`
- [ ] `C-CF-07` `constraint` The app denies a request carrying no bearer token on every endpoint outside the anonymous set. `src: Core features, Auth rule 3`
- [ ] `C-CF-08` `constraint` The app denies a request carrying an unparseable bearer token. `src: Core features, Auth rule 3`
- [ ] `C-CF-09` `data` The app stores every password hashed. `src: Core features, Auth rule 4`
- [ ] `C-CF-10` `literal` The app accepts the password `deku-demo-pw-2026` at login for every seeded account. `src: Core features, Auth rule 4`
- [ ] `C-CF-11` `literal` The app ends a session at `/api/auth/logout`. `src: Core features, Auth rule 5`
- [ ] `C-CF-12` `constraint` The app refuses the bearer token a logout was called with on the next request. `src: Core features, Auth rule 5`
- [ ] `C-CF-13` `constraint` The app exposes no endpoint creating a principal from an unauthenticated request. `src: Core features, Auth rule 6`
- [ ] `C-CF-14` `capability` The app refuses further password attempts for one address after five failures inside a rolling window. `src: Core features, Auth rule 7`
- [ ] `C-CF-15` `capability` The app accepts password attempts for that address again once the window passes. `src: Core features, Auth rule 7`
- [ ] `C-CF-16` `constraint` The app never applies a permanent lockout to an address. `src: Core features, Auth rule 7`
- [ ] `C-CF-17` `capability` The app lets every member discover an open teamspace. `src: Core features, Teamspaces rule 1`
- [ ] `C-CF-18` `capability` The app lets every member read a page in an open teamspace. `src: Core features, Teamspaces rule 1`
- [ ] `C-CF-19` `capability` The app lets every member discover the name of a closed teamspace. `src: Core features, Teamspaces rule 2`
- [ ] `C-CF-20` `constraint` The app denies a read of a page in a closed teamspace to a principal outside its membership. `src: Core features, Teamspaces rule 2`
- [ ] `C-CF-21` `constraint` The app omits a private teamspace from the listing returned to a principal outside its membership. `src: Core features, Teamspaces rule 3`
- [ ] `C-CF-22` `constraint` The app refuses a direct request for a page in a private teamspace the way an unissued identifier is refused. `src: Core features, Teamspaces rule 3`
- [ ] `C-CF-23` `literal` The app returns a top-level JSON array of discoverable teamspaces at `/api/teamspaces`. `src: Core features, Teamspaces rule 4`
- [ ] `C-CF-24` `literal` The app returns `Engineering`, `People Ops` to `member@example.com` from the teamspace listing. `src: Core features, Teamspaces rule 4`
- [ ] `C-CF-25` `literal` The app omits `Board Papers` from the teamspace listing returned to `member@example.com`. `src: Core features, Teamspaces rule 4`
- [ ] `C-CF-26` `constraint` The app denies a teamspace access-mode change requested from a member session. `src: Core features, Teamspaces rule 5`
- [ ] `C-CF-27` `constraint` The app leaves the stored access mode unchanged after a denied access-mode change. `src: Core features, Teamspaces rule 5`
- [ ] `C-CF-28` `capability` The app carries thirteen block types on a page. `src: Core features, Pages rule 1`
- [ ] `C-CF-29` `literal` The app inserts a block at a stated sibling position at `/api/pages/{pageId}/blocks`. `src: Core features, Pages rule 2`
- [ ] `C-CF-30` `literal` The app edits a block text, checked state, colour at `/api/blocks/{blockId}`. `src: Core features, Pages rule 2`
- [ ] `C-CF-31` `literal` The app changes a block position, depth in one operation at `/api/blocks/{blockId}/move`. `src: Core features, Pages rule 2`
- [ ] `C-CF-32` `capability` The app soft deletes a block so a deleted block stops being returned. `src: Core features, Pages rule 2`
- [ ] `C-CF-33` `literal` The app returns a soft-deleted block to its old position at `/api/blocks/{blockId}/restore`. `src: Core features, Pages rule 2`
- [ ] `C-CF-34` `constraint` The app refuses a request indenting a block past depth 5. `src: Core features, Pages rule 3`
- [ ] `C-CF-35` `constraint` The app writes nothing after refusing an over-deep indent. `src: Core features, Pages rule 3`
- [ ] `C-CF-36` `data` The app starts every block version at 1. `src: Core features, Pages rule 4`
- [ ] `C-CF-37` `data` The app advances a block version by exactly one on each accepted write. `src: Core features, Pages rule 4`
- [ ] `C-CF-38` `constraint` The app accepts exactly one of two writes to a block carrying the same version. `src: Core features, Pages rule 4`
- [ ] `C-CF-39` `constraint` The app rejects the losing write of a block version conflict as a conflict. `src: Core features, Pages rule 4`
- [ ] `C-CF-40` `data` The app leaves a contended block at the accepted writer value. `src: Core features, Pages rule 4`
- [ ] `C-CF-41` `data` The app records the writing principal as the block last edited by value. `src: Core features, Pages rule 5`
- [ ] `C-CF-42` `data` The app records the writing principal as the page last edited by value. `src: Core features, Pages rule 5`
- [ ] `C-CF-43` `capability` The app returns the blocks of a page in the order a member dropped them after a reload. `src: Core features, Pages rule 6`
- [ ] `C-CF-44` `ui` The app opens a typed insert menu when a member types a slash at the start of an empty block. `src: Core features, Editing rule 7`
- [ ] `C-CF-45` `ui` The app filters the insert menu as the member keeps typing. `src: Core features, Editing rule 7`
- [ ] `C-CF-46` `ui` The app turns a hash followed by a space into a heading as the member types. `src: Core features, Editing rule 8`
- [ ] `C-CF-47` `ui` The app turns a dash followed by a space into a bulleted list item as the member types. `src: Core features, Editing rule 8`
- [ ] `C-CF-48` `ui` The app undoes a markdown shorthand transformation in one step. `src: Core features, Editing rule 8`
- [ ] `C-CF-49` `ui` The app shows a drag handle to the left of a block on hover. `src: Core features, Editing rule 9`
- [ ] `C-CF-50` `ui` The app shows a drop indicator marking the landing position, the landing depth during a drag. `src: Core features, Editing rule 9`
- [ ] `C-CF-51` `ui` The app applies a block operation to every block in a multi-block selection. `src: Core features, Editing rule 10`
- [ ] `C-CF-52` `capability` The app records undo as a stack of invertible operations. `src: Core features, Editing rule 11`
- [ ] `C-CF-53` `constraint` The app leaves another principal work in place when one principal undoes an operation. `src: Core features, Editing rule 11`
- [ ] `C-CF-54` `data` The app stores a block text as an array of runs carrying annotations. `src: Core features, Rich text rule 13`
- [ ] `C-CF-55` `data` The app carries seven annotation kinds on a run. `src: Core features, Rich text rule 13`
- [ ] `C-CF-56` `capability` The app keeps an annotation on the words the annotation was applied to after surrounding text changes. `src: Core features, Rich text rule 14`
- [ ] `C-CF-57` `capability` The app returns the stored runs, annotations unchanged after a reload. `src: Core features, Rich text rule 15`
- [ ] `C-CF-58` `capability` The app answers one authorization question from every read path, every write path. `src: Core features, authorization opening`
- [ ] `C-CF-59` `constraint` The app denies an action for a deactivated principal. `src: Core features, authorization rule 1`
- [ ] `C-CF-60` `constraint` The app denies an action covered by an expired grant. `src: Core features, authorization rule 1`
- [ ] `C-CF-61` `constraint` The app denies an action when an explicit deny grant covers the resource for the principal. `src: Core features, authorization rule 1`
- [ ] `C-CF-62` `capability` The app allows an admin action, recording the allowance as an administrative access. `src: Core features, authorization rule 1`
- [ ] `C-CF-63` `capability` The app allows an action at the highest level an explicit allow grant carries. `src: Core features, authorization rule 1`
- [ ] `C-CF-64` `capability` The app allows a member read inside an open teamspace at the teamspace default. `src: Core features, authorization rule 1`
- [ ] `C-CF-65` `capability` The app allows an anonymous read of a published page. `src: Core features, authorization rule 1`
- [ ] `C-CF-66` `constraint` The app denies an action no rule allows. `src: Core features, authorization rule 1`
- [ ] `C-CF-67` `constraint` The app lets an explicit deny beat every allow at every level. `src: Core features, authorization rule 2`
- [ ] `C-CF-68` `literal` The app refuses `Onboarding Checklist` to `member2@example.com`. `src: Core features, authorization rule 2`
- [ ] `C-CF-69` `literal` The app serves `Onboarding Checklist` to `member@example.com`. `src: Core features, authorization rule 2`
- [ ] `C-CF-70` `capability` The app gives a page the effective grants of its parent when the page carries no grant set. `src: Core features, authorization rule 3`
- [ ] `C-CF-71` `capability` The app replaces inheritance for a page subtree when the page carries its own grant set. `src: Core features, authorization rule 3`
- [ ] `C-CF-72` `capability` The app returns a page back to inheritance on request. `src: Core features, authorization rule 3`
- [ ] `C-CF-73` `literal` The app returns the level, the grant source per subject at `/api/pages/{pageId}/access`. `src: Core features, authorization rule 4`
- [ ] `C-CF-74` `capability` The app names the grant source as the page, a named ancestor, the teamspace, a named group. `src: Core features, authorization rule 4`
- [ ] `C-CF-75` `data` The app writes an administrative read of a page as an administrative access in the activity record. `src: Core features, authorization rule 5`
- [ ] `C-CF-76` `constraint` The app denies a grant create, change, delete requested from a member session. `src: Core features, authorization rule 6`
- [ ] `C-CF-77` `constraint` The app denies a grant create, change, delete requested from a guest session. `src: Core features, authorization rule 6`
- [ ] `C-CF-78` `data` The app records on every page, block, row the workspace the record belongs to. `src: Core features, authorization rule 7`
- [ ] `C-CF-79` `constraint` The app returns no record belonging to another workspace from any endpoint. `src: Core features, authorization rule 7`
- [ ] `C-CF-80` `constraint` The app caches no authorization decision across principals. `src: Core features, authorization rule 8`
- [ ] `C-CF-81` `constraint` The app keys no cache guarding permissioned content without the principal. `src: Core features, authorization rule 8`
- [ ] `C-CF-82` `constraint` The app denies the next read after a principal leaves a group. `src: Core features, authorization rule 9`
- [ ] `C-CF-83` `constraint` The app denies an action once a grant passes its expiry time. `src: Core features, authorization rule 10`
- [ ] `C-CF-84` `data` The app marks an expired grant expired, retaining the row. `src: Core features, authorization rule 10`
- [ ] `C-CF-85` `capability` The app delegates access only by a grant carrying an optional end date. `src: Core features, authorization rule 11`
- [ ] `C-CF-86` `constraint` The app denies an action under a grant created with an end date already passed. `src: Core features, authorization rule 11`
- [ ] `C-CF-87` `data` The app carries twelve property types on a database. `src: Core features, Databases rule 1`
- [ ] `C-CF-88` `constraint` The app keeps exactly one title property per database. `src: Core features, Databases rule 1`
- [ ] `C-CF-89` `literal` The app issues unique keys reading `ZEN-1`, `ZEN-2` from the seeded database. `src: Core features, Databases rule 1`
- [ ] `C-CF-90` `data` The app stores a number property as an exact decimal string. `src: Core features, Databases rule 2`
- [ ] `C-CF-91` `data` The app stores a filter, a sort, a group property, a visible property list per view. `src: Core features, Databases rule 3`
- [ ] `C-CF-92` `data` The app stores a filter as a nested tree of conditions joined by and, by or. `src: Core features, Databases rule 4`
- [ ] `C-CF-93` `capability` The app returns a saved nested filter tree unchanged after a reload. `src: Core features, Databases rule 4`
- [ ] `C-CF-94` `ui` The app groups a board view by a status property. `src: Core features, Databases rule 5`
- [ ] `C-CF-95` `ui` The app shows the group name, the row count in a board column header. `src: Core features, Databases rule 5`
- [ ] `C-CF-96` `literal` The app ends every board column with an affordance reading `New page`. `src: Core features, Databases rule 5`
- [ ] `C-CF-97` `constraint` The app omits a property the calling principal may not read from the row response. `src: Core features, Databases rule 6`
- [ ] `C-CF-98` `literal` The app omits `Key notes` from a row response served to `guest@example.com`. `src: Core features, Databases rule 6`
- [ ] `C-CF-99` `constraint` The app refuses a filter, a sort, a group on a property hidden from the calling principal. `src: Core features, Databases rule 6`
- [ ] `C-CF-100` `literal` The app returns readable rows at `/api/databases/{dbId}/views/{viewId}/rows` as a top-level JSON array. `src: Core features, Databases rule 8`
- [ ] `C-CF-101` `literal` The app stores uploaded file bytes in the bucket named by `STORAGE_BUCKET`. `src: Core features, Attachments rule 1`
- [ ] `C-CF-102` `literal` The app names an uploaded object `workspaces/{workspace_slug}/pages/{page_id}/{sha256_of_bytes}.{ext}`. `src: Core features, Attachments rule 1`
- [ ] `C-CF-103` `constraint` The app writes no attachment bytes to the container filesystem. `src: Core features, Attachments rule 2`
- [ ] `C-CF-104` `constraint` The app stores no attachment bytes inside a database column. `src: Core features, Attachments rule 2`
- [ ] `C-CF-105` `data` The app records the filename, the content type, the byte size, the digest of an attachment. `src: Core features, Attachments rule 2`
- [ ] `C-CF-106` `literal` The app streams an object to an entitled principal at `/api/attachments/{attachmentId}`. `src: Core features, Attachments rule 3`
- [ ] `C-CF-107` `constraint` The app denies an attachment read to a principal the owning page is denied to. `src: Core features, Attachments rule 3`
- [ ] `C-CF-108` `constraint` The app denies an attachment read to an anonymous caller when the owning page is unpublished. `src: Core features, Attachments rule 3`
- [ ] `C-CF-109` `capability` The app serves an attachment anonymously for as long as the owning page stays published. `src: Core features, Attachments rule 4`
- [ ] `C-CF-110` `literal` The app seeds the attachment `handbook-cover.png` on the page `Engineering Handbook`. `src: Core features, Attachments rule 5`
- [ ] `C-CF-111` `constraint` The app requires full access on a page before publishing the page. `src: Core features, Publishing rule 1`
- [ ] `C-CF-112` `capability` The app states how many pages became public in the publish response. `src: Core features, Publishing rule 1`
- [ ] `C-CF-113` `ui` The app confirms a publish with the child-page count before the call is made. `src: Core features, Publishing rule 1`
- [ ] `C-CF-114` `literal` The app serves a published page anonymously at `/site/{slug}`. `src: Core features, Publishing rule 2`
- [ ] `C-CF-115` `constraint` The app keeps a public slug unique across the workspace. `src: Core features, Publishing rule 2`
- [ ] `C-CF-116` `constraint` The app refuses a publish request asking for a slug already in use. `src: Core features, Publishing rule 2`
- [ ] `C-CF-117` `capability` The app renders the published route on the server. `src: Core features, Publishing rule 3`
- [ ] `C-CF-118` `capability` The app renders the published route readably with scripting disabled. `src: Core features, Publishing rule 3`
- [ ] `C-CF-119` `capability` The app gives a published route its own title, its own description. `src: Core features, Publishing rule 3`
- [ ] `C-CF-120` `capability` The app lists a published page in a sitemap. `src: Core features, Publishing rule 3`
- [ ] `C-CF-121` `capability` The app answers gone at the public address of an unpublished page. `src: Core features, Publishing rule 4`
- [ ] `C-CF-122` `constraint` The app never redirects an unpublished public address into the workspace. `src: Core features, Publishing rule 4`
- [ ] `C-CF-123` `literal` The app seeds `Release Notes` published at the slug `release-notes`. `src: Core features, Publishing rule 6`
- [ ] `C-CF-124` `constraint` The app answers not found for an anonymous request naming an unpublished seeded page. `src: Core features, Publishing rule 6`
- [ ] `C-CF-125` `literal` The app lists every principal with a role, an active flag at `/api/admin/members`. `src: Core features, Admin rule 1`
- [ ] `C-CF-126` `capability` The app deactivates a principal on an admin request. `src: Core features, Admin rule 1`
- [ ] `C-CF-127` `constraint` The app denies the next request of a deactivated principal. `src: Core features, Admin rule 1`
- [ ] `C-CF-128` `capability` The app applies a group addition to the added principal on the next read. `src: Core features, Admin rule 2`
- [ ] `C-CF-129` `literal` The app returns the activity record newest first at `/api/admin/activity`. `src: Core features, Admin rule 3`
- [ ] `C-CF-130` `data` The app names the acting principal, the action, the resource type, the resource identifier, the time on an activity row. `src: Core features, Admin rule 3`
- [ ] `C-CF-131` `data` The app records a publish, an unpublish, a grant change, a page delete, a page restore, an access-mode change, an administrative access. `src: Core features, Admin rule 3`
- [ ] `C-CF-132` `constraint` The app exposes no endpoint updating an activity row. `src: Core features, Admin rule 4`
- [ ] `C-CF-133` `constraint` The app exposes no endpoint deleting an activity row. `src: Core features, Admin rule 4`
- [ ] `C-CF-134` `constraint` The app denies every admin endpoint to a member session, to a guest session. `src: Core features, Admin rule 5`
- [ ] `C-CF-135` `constraint` The app writes nothing after denying an admin endpoint. `src: Core features, Admin rule 5`
- [ ] `C-CF-136` `data` The app names the changed thing in the detail field of an activity row. `src: Core features, Admin rule 6`
- [ ] `C-CF-137` `capability` The app returns the same slug, the same published count on a repeated publish of an already published page. `src: Core features, Admin rule 7`
- [ ] `C-CF-138` `constraint` The app writes no second activity row on a repeated publish. `src: Core features, Admin rule 7`
- [ ] `C-CF-139` `literal` The app returns matching pages as a top-level JSON array at `/api/search`. `src: Core features, Search rule 1`
- [ ] `C-CF-140` `capability` The app matches a search query against a page title, against block text. `src: Core features, Search rule 1`
- [ ] `C-CF-141` `constraint` The app omits a page the calling principal may not read from every search result. `src: Core features, Search rule 2`
- [ ] `C-CF-142` `capability` The app returns an empty array for a search matching nothing. `src: Core features, Search rule 3`
- [ ] `C-CF-143` `constraint` The app scopes every search to one workspace. `src: Core features, Search rule 4`
- [ ] `C-CF-144` `capability` The app keeps a search index current as pages, blocks change. `src: Core features, Search rule 5`
- [ ] `C-CF-145` `constraint` The app drops a page from a principal results at the moment the page leaves that principal grant. `src: Core features, Search rule 5`
- [ ] `C-CF-146` `capability` The app renders its own not-found page at an address the product does not serve. `src: Core features, product surfaces rule 1`
- [ ] `C-CF-147` `capability` The app puts the product name, a line of its own copy, a link back on the not-found page. `src: Core features, product surfaces rule 1`
- [ ] `C-CF-148` `capability` The app answers a not-found status at an address the product does not serve. `src: Core features, product surfaces rule 1`
- [ ] `C-CF-149` `constraint` The app serves no internal link resolving to an address the product answers not-found for. `src: Core features, product surfaces rule 2`
- [ ] `C-CF-150` `capability` The app resolves two disagreeing allow grants at the higher access level. `src: Core features, Edge cases rule 7`

## C-UF User flow

- [ ] `C-UF-01` `literal` The app serves an identifier-first sign in at `/login`. `src: User flow route table row 1`
- [ ] `C-UF-02` `literal` The app serves the workspace home at `/w`. `src: User flow route table row 2`
- [ ] `C-UF-03` `literal` The app serves workspace search at `/w/search`. `src: User flow route table row 3`
- [ ] `C-UF-04` `literal` The app serves a page in the detail pane at `/w/p/{pageId}`. `src: User flow route table row 4`
- [ ] `C-UF-05` `literal` The app serves a database view in the detail pane at `/w/db/{dbId}/{viewId}`. `src: User flow route table row 5`
- [ ] `C-UF-06` `literal` The app serves members, groups to an admin at `/w/admin/members`. `src: User flow route table row 6`
- [ ] `C-UF-07` `literal` The app serves teamspaces, access modes to an admin at `/w/admin/teamspaces`. `src: User flow route table row 7`
- [ ] `C-UF-08` `literal` The app serves the activity record to an admin at `/w/admin/activity`. `src: User flow route table row 8`
- [ ] `C-UF-09` `capability` The app sends an anonymous request for a workspace route to the sign-in route. `src: User flow, entry paragraph`
- [ ] `C-UF-10` `capability` The app continues to the requested address after a successful sign in. `src: User flow, entry paragraph`
- [ ] `C-UF-11` `capability` The app lands a sign in carrying no pending address on the workspace home. `src: User flow, entry paragraph`
- [ ] `C-UF-12` `capability` The app returns to the sign-in route on signout. `src: User flow, entry paragraph`
- [ ] `C-UF-13` `constraint` The app refuses the previous bearer token after a signout. `src: User flow, entry paragraph`
- [ ] `C-UF-14` `capability` The app returns a member to the address the member was on after an expired-token sign in. `src: User flow, entry paragraph`
- [ ] `C-UF-15` `constraint` The app renders no admin table to a member session. `src: User flow, entry paragraph`
- [ ] `C-UF-16` `ui` The app names the role an admin route needs in the refusal shown to a member. `src: User flow, entry paragraph`
- [ ] `C-UF-17` `ui` The app names the filter that emptied a database view in the empty state. `src: User flow, states paragraph`
- [ ] `C-UF-18` `ui` The app offers a clear-filter action in the empty state of a filtered view. `src: User flow, states paragraph`
- [ ] `C-UF-19` `ui` The app renders skeleton sidebar rows at the last known count during a load. `src: User flow, states paragraph`
- [ ] `C-UF-20` `ui` The app renders a database view header, column set before the rows arrive. `src: User flow, states paragraph`
- [ ] `C-UF-21` `ui` The app renders an error as a banner above the content. `src: User flow, states paragraph`
- [ ] `C-UF-22` `ui` The app keeps already loaded content readable under an error banner. `src: User flow, states paragraph`
- [ ] `C-UF-23` `ui` The app shows a create prompt in a teamspace holding no pages. `src: User flow, states paragraph`
- [ ] `C-UF-24` `constraint` The app shows no stack trace anywhere in the interface. `src: User flow, states paragraph`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The app puts the content before the product chrome in what a reader notices first. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The app reads quiet, dense but organised, built for scanning. `src: UI/UX notes para 1`
- [ ] `C-UX-03` `ui` The app puts every working surface on a white page. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-04` `ui` The app renders body text as a near-black neutral softened off pure black. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-05` `ui` The app carries five text weights, each strictly lighter than the one above. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-06` `ui` The app renders the application default text as a deep warm neutral. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-07` `ui` The app carries exactly one saturated colour, a mid vivid cyan blue. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-08` `constraint` The app puts the saturated action colour nowhere that is not interactive. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-09` `ui` The app darkens the action colour one step on hover, one step again on press. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-10` `ui` The app renders hairlines as a near-white neutral at one thickness. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-11` `constraint` The app carries exactly one hover tint strength across the product. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-12` `ui` The app carries three state colours appearing nowhere else. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-13` `ui` The app carries ten block hues as a pale background with a darker foreground of the same family. `src: UI/UX notes, block palette paragraph`
- [ ] `C-UX-14` `literal` The app meets a contrast ratio of at least `4.5 to 1` on every block hue pair at 16px upward. `src: UI/UX notes, block palette paragraph`
- [ ] `C-UX-15` `ui` The app uses one interface sans in a regular face, a medium face, a semibold face. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-16` `literal` The app sets body text at `16px` over a `24px` line in the regular face. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-17` `ui` The app keeps a line-height ratio of 1.5 through the body scale, at the display sizes. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-18` `ui` The app lines figures up in a column wherever amounts stack. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-19` `ui` The app rounds corners at one default softness, a smaller one, a larger one. `src: UI/UX notes, shape paragraph`
- [ ] `C-UX-20` `constraint` The app uses a fully rounded pill only for a menu button, a badge. `src: UI/UX notes, shape paragraph`
- [ ] `C-UX-21` `ui` The app reads comfortable in the reading column, compact in the sidebar. `src: UI/UX notes, shape paragraph`
- [ ] `C-UX-22` `ui` The app builds a shadow from several barely-there stacked layers. `src: UI/UX notes, shape paragraph`
- [ ] `C-UX-23` `ui` The app carries four elevations, no more. `src: UI/UX notes, shape paragraph`
- [ ] `C-UX-24` `ui` The app carries seven named stacking layers, no more. `src: UI/UX notes, shape paragraph`
- [ ] `C-UX-25` `ui` The app carries one main action style, one quieter alternative. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-26` `ui` The app gives each action style resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-27` `constraint` The app signals an unavailable control by more than colour. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-28` `ui` The app closes any open dialog, popover, side peek on Escape. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-29` `ui` The app returns focus to the opening control when a dialog closes. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-30` `ui` The app confirms a destructive action first, naming what will be affected. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-31` `ui` The app collapses the sidebar away entirely with a hover peek. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-32` `literal` The app orders the sidebar sections `Teamspaces`, then `Private`. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-33` `ui` The app remembers whether a sidebar section was left collapsed. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-34` `literal` The app ends each sidebar section with a `More` row expanding in place. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-35` `ui` The app animates a hover, a focus, a pressed state by a transition on a named property. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-36` `constraint` The app transitions no property nobody chose. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-37` `ui` The app moves everything on one family of curves at one of three speeds. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-38` `ui` The app settles a control background into its hover tint as the pointer arrives. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-39` `ui` The app eases the sidebar width open, closed without reflowing the content twice. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-40` `ui` The app shows an optimistically saved row at once, settling when the save lands. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-41` `ui` The app undoes an optimistic row, showing the reason, when the save fails. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-42` `ui` The app turns a spinner for as long as work is happening. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-43` `ui` The app settles a dropped block into its new position rather than jumping. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-44` `constraint` The app removes entrance animations under a reduced-motion preference. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-45` `constraint` The app keeps colour transitions under a reduced-motion preference. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-46` `constraint` The app keeps the spinner turning under a reduced-motion preference. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-47` `literal` The app conforms to `WCAG 2.1` level AA across the product. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-48` `constraint` The app puts muted text only at 18px upward, only on a non-essential label. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-49` `ui` The app makes every interactive control reachable by keyboard navigation alone. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-50` `ui` The app draws the focus ring as a dark ring inside a light ring. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-51` `constraint` The app never removes the focus ring. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-52` `ui` The app follows reading order in focus order. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-53` `ui` The app moves focus to a neighbour after an action removes the focused element. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-54` `ui` The app makes every block operation reachable without a pointer. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-55` `ui` The app gives every drag a keyboard equivalent announcing the new position. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-56` `ui` The app traps focus inside a dialog, returning focus to the trigger on close. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-57` `ui` The app renders a database view as a real table carrying header associations. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-58` `ui` The app gives a database grid arrow-key navigation with a stated way in, a stated way out. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-59` `ui` The app announces save state politely, errors assertively. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-60` `constraint` The app never relies on hue alone for a status, a validation message. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-61` `ui` The app gives an icon-only control an accessible name describing the action. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-62` `ui` The app hides a decorative image from assistive technology. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-63` `ui` The app asks for alternative text when an image is added. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-64` `ui` The app warns when a heading level is skipped. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-65` `ui` The app reflows to a single column at 200 per cent text scale with nothing clipped. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-66` `ui` The app raises its layout floor at each tier from a mobile-first base. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-67` `constraint` The app carries exactly one max-width query. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-68` `ui` The app holds its arrangement at every viewport width between the named tiers. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-69` `ui` The app turns the sidebar into a sheet dismissing on selection at phone width. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-70` `ui` The app hides the tab strip at phone width, opening one page at a time. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-71` `ui` The app scrolls a table view sideways inside its own frame with the title column pinned. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-72` `ui` The app shows one board column at a time with a horizontal pager at phone width. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-73` `ui` The app collapses the sidebar to a toggle at tablet width. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-74` `ui` The app stops the content column growing past the widest breakpoint. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-75` `constraint` The app never scrolls the document sideways. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-76` `literal` The app sizes every coarse-pointer control at least `44px by 44px`. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-77` `ui` The app gives every hover affordance a non-hover equivalent. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-78` `ui` The app breaks a very long unbroken word in a page title rather than overflowing. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-79` `ui` The app closes an open dropdown across a resize. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-80` `ui` The app writes every string in sentence case outside a proper noun. `src: UI/UX notes, copy paragraph`
- [ ] `C-UX-81` `constraint` The app writes no exclamation mark in an interface string. `src: UI/UX notes, copy paragraph`
- [ ] `C-UX-82` `literal` The app displays the strings `Share`, `New`, `New page`, `Syncing` exactly. `src: UI/UX notes, copy paragraph`
- [ ] `C-UX-83` `literal` The app displays the board groups `To-do`, `In progress`, `In review`, `Complete` exactly. `src: UI/UX notes, copy paragraph`
- [ ] `C-UX-84` `literal` The app displays the view names `Company tasks`, `Current sprint` exactly. `src: UI/UX notes, copy paragraph`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The app scrolls only the content pane inside the workspace application. `src: Front-end specification, two surfaces`
- [ ] `C-FE-02` `ui` The app scrolls a published page as an ordinary document. `src: Front-end specification, two surfaces`
- [ ] `C-FE-03` `ui` The app renders the sign-in surface as a single narrow centred column on white. `src: Front-end specification, sign-in surface`
- [ ] `C-FE-04` `literal` The app labels the sign-in address field `Email`. `src: Front-end specification, sign-in surface`
- [ ] `C-FE-05` `literal` The app labels the sign-in primary control `Continue`. `src: Front-end specification, sign-in surface`
- [ ] `C-FE-06` `constraint` The app shows no password field on the sign-in surface. `src: Front-end specification, sign-in surface`
- [ ] `C-FE-07` `ui` The app puts the workspace switcher at the top of the sidebar. `src: Front-end specification, sidebar`
- [ ] `C-FE-08` `ui` The app scrolls the tab strip horizontally, shrinking tabs to a minimum first. `src: Front-end specification, tab strip`
- [ ] `C-FE-09` `ui` The app replaces the active tab when a page is opened from the sidebar. `src: Front-end specification, tab strip`
- [ ] `C-FE-10` `ui` The app survives a reload with the open tab set intact. `src: Front-end specification, tab strip`
- [ ] `C-FE-11` `ui` The app renders a page as one reading column with generous side gutters. `src: Front-end specification, page surface`
- [ ] `C-FE-12` `ui` The app keeps the page header sticky inside the content pane. `src: Front-end specification, page surface`
- [ ] `C-FE-13` `ui` The app pins the title column of a table view. `src: Front-end specification, database surfaces`
- [ ] `C-FE-14` `ui` The app offers a count in a calculation row beneath a table body. `src: Front-end specification, database surfaces`
- [ ] `C-FE-15` `ui` The app puts the title, up to three further properties on a board card. `src: Front-end specification, database surfaces`
- [ ] `C-FE-16` `ui` The app virtualises rows so only the visible window plus a small overscan renders. `src: Front-end specification, database surfaces`
- [ ] `C-FE-17` `ui` The app renders a published page with no sidebar, no tab strip, no action row. `src: Front-end specification, published page`
- [ ] `C-FE-18` `constraint` The app links nothing from a published page back into the workspace. `src: Front-end specification, published page`
- [ ] `C-FE-19` `ui` The app carries one interface typeface in three faces. `src: Front-end specification, typography`
- [ ] `C-FE-20` `ui` The app declares each font family with a fallback stack ending in a generic family. `src: Front-end specification, typography`
- [ ] `C-FE-21` `ui` The app carries four radii, no fifth. `src: Front-end specification, radii`
- [ ] `C-FE-22` `ui` The app declares stacking in seven named bands. `src: Front-end specification, layering`
- [ ] `C-FE-23` `ui` The app draws every icon as inline geometry on one grid at one stroke thickness. `src: Front-end specification, iconography`
- [ ] `C-FE-24` `ui` The app rotates one arrow shape for every direction rather than redrawing. `src: Front-end specification, iconography`
- [ ] `C-FE-25` `ui` The app reduces curves to five roles, no more. `src: Front-end specification, motion inventory`
- [ ] `C-FE-26` `ui` The app reduces durations to three plus a press feedback. `src: Front-end specification, motion inventory`
- [ ] `C-FE-27` `constraint` The app ships no binary file of any kind. `src: Front-end specification, zero-asset`
- [ ] `C-FE-28` `ui` The app draws the wordmark, the page icons, the favicon as geometry. `src: Front-end specification, zero-asset`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app builds its frontend with Lit on Vite. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The app serves its backend with FastAPI on Python. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The app delivers page content as JSON from the same origin under the api prefix. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` The app renders the published site route as HTML on the server. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` The app stores records in PostgreSQL. `src: Technical requirements para 1`
- [ ] `C-TR-06` `contract` The app stores file bytes in minio. `src: Technical requirements para 1`
- [ ] `C-TR-07` `literal` The app answers `GET /api/health` with status 200 once ready. `src: Technical requirements para 1`
- [ ] `C-TR-08` `contract` The app writes one structured log line per request carrying method, path, status. `src: Technical requirements para 1`
- [ ] `C-TR-09` `constraint` The app writes no password, no bearer token, no store credential to a log line. `src: Technical requirements para 1`
- [ ] `C-TR-10` `literal` The app reads its database connection from `DATABASE_URL`. `src: Technical requirements para 3`
- [ ] `C-TR-11` `literal` The app reads its object store address from `STORAGE_ENDPOINT`. `src: Technical requirements para 3`
- [ ] `C-TR-12` `literal` The app reads its bucket name from `STORAGE_BUCKET`. `src: Technical requirements para 3`
- [ ] `C-TR-13` `literal` The app reads its store credentials from `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`. `src: Technical requirements para 3`
- [ ] `C-TR-14` `literal` The app reads its public address from `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`. `src: Technical requirements para 3`
- [ ] `C-TR-15` `constraint` The app hardcodes no service host, no service port. `src: Technical requirements para 3`
- [ ] `C-TR-16` `contract` The app sends standard security headers on every response. `src: Technical requirements para 4`
- [ ] `C-TR-17` `contract` The app sends a strict transport policy header on every response. `src: Technical requirements para 4`
- [ ] `C-TR-18` `contract` The app sends a content-type policy forbidding sniffing on every response. `src: Technical requirements para 4`
- [ ] `C-TR-19` `constraint` The app puts no credential, no key, no token in anything the browser downloads. `src: Technical requirements para 4`
- [ ] `C-TR-20` `contract` The app serves a favicon, declaring the favicon in the document head of every rendered route. `src: Technical requirements para 4`
- [ ] `C-TR-21` `contract` The app executes a search, a filter, a sort, a group in the store. `src: Technical requirements para 5`
- [ ] `C-TR-22` `contract` The app pages a list endpoint by cursor rather than by offset. `src: Technical requirements para 5`

## C-DM Data model

- [ ] `C-DM-01` `data` The app carries eleven tables. `src: Data model para 1`
- [ ] `C-DM-02` `data` The app records every timestamp in UTC. `src: Data model para 1`
- [ ] `C-DM-03` `literal` The app writes the seeded password `deku-demo-pw-2026` into `/app/USER_README.md` beside each account. `src: Data model, password paragraph`
- [ ] `C-DM-04` `data` The app stores a principal email lowercased, unique across principals. `src: Data model, principals`
- [ ] `C-DM-05` `data` The app stores a group name unique across groups. `src: Data model, groups`
- [ ] `C-DM-06` `data` The app stores a teamspace slug unique across teamspaces. `src: Data model, teamspaces`
- [ ] `C-DM-07` `data` The app stores a page public slug unique across pages. `src: Data model, pages`
- [ ] `C-DM-08` `constraint` The app keeps a block on one page, changing position rather than page on a move. `src: Data model, structural invariants`
- [ ] `C-DM-09` `constraint` The app keeps block depth at 5 or lower. `src: Data model, structural invariants`
- [ ] `C-DM-10` `constraint` The app gives every published page a slug. `src: Data model, structural invariants`
- [ ] `C-DM-11` `constraint` The app puts a principal in a group once. `src: Data model, structural invariants`
- [ ] `C-DM-12` `data` The app advances a database unique-id counter by one, never reissuing a number. `src: Data model, uniqueness paragraph`
- [ ] `C-DM-13` `literal` The app keeps `ZEN-3` naming one row for the life of the database. `src: Data model, uniqueness paragraph`
- [ ] `C-DM-14` `data` The app gives two rows created at the same moment two different unique-id keys. `src: Data model, uniqueness paragraph`
- [ ] `C-DM-15` `data` The app derives a board column count rather than storing the count. `src: Data model, derived paragraph`
- [ ] `C-DM-16` `data` The app derives the child-page count a publish confirmation reports. `src: Data model, derived paragraph`
- [ ] `C-DM-17` `literal` The app seeds the teamspace `Engineering` with the access mode open. `src: Data model, seed data`
- [ ] `C-DM-18` `literal` The app seeds the teamspace `People Ops` with the access mode closed. `src: Data model, seed data`
- [ ] `C-DM-19` `literal` The app seeds the teamspace `Board Papers` with the access mode private. `src: Data model, seed data`
- [ ] `C-DM-20` `literal` The app seeds the page `Engineering Handbook` unpublished with four blocks. `src: Data model, seed data`
- [ ] `C-DM-21` `literal` The app seeds the page `Compensation Bands` in the closed teamspace. `src: Data model, seed data`
- [ ] `C-DM-22` `literal` The app seeds the page `Board Minutes` in the private teamspace. `src: Data model, seed data`
- [ ] `C-DM-23` `literal` The app seeds the database `Company Tasks` in the open teamspace with four rows. `src: Data model, seed data`
- [ ] `C-DM-24` `literal` The app seeds the properties `Project`, `Team`, `Date`, `Created by`, `Key notes`, `Status`. `src: Data model, seed data`
- [ ] `C-DM-25` `literal` The app seeds a read grant on `Company Tasks` for `guest@example.com`. `src: Data model, seed data`
- [ ] `C-DM-26` `constraint` The app duplicates no row when the app restarts. `src: Data model, closing line`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app carries one workspace. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The app carries no realtime transport, no presence, no offline store. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` The app carries no comments, no mentions, no page history browser. `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` The app carries no formula, no relation, no rollup property type. `src: Constraints bullet 4`
- [ ] `C-CN-05` `constraint` The app carries no timeline, calendar, gallery, list, chart view. `src: Constraints bullet 4`
- [ ] `C-CN-06` `constraint` The app carries no assistant, no agent, no metered unit. `src: Constraints bullet 5`
- [ ] `C-CN-07` `constraint` The app carries no billing, no seat, no plan, no invoice. `src: Constraints bullet 6`
- [ ] `C-CN-08` `constraint` The app carries no federated sign-in, no passkey, no second factor. `src: Constraints bullet 7`
- [ ] `C-CN-09` `constraint` The app carries no automation, no connector, no webhook. `src: Constraints bullet 8`
- [ ] `C-CN-10` `constraint` The app sends no email, no notification. `src: Constraints bullet 9`
- [ ] `C-CN-11` `constraint` The app carries no custom domain, no certificate management. `src: Constraints bullet 10`
- [ ] `C-CN-12` `constraint` The app carries one locale. `src: Constraints bullet 13`
- [ ] `C-CN-13` `constraint` The app makes no external network call at runtime beyond the two named backing services. `src: Constraints bullet 15`

## C-DC Deployment contract

- [ ] `C-DC-01` `literal` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The app serves on the container-internal port `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The app reads its port from configuration rather than hardcoding a port. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The app serves its HTTP interface under the api prefix on the app origin. `src: Deployment contract bullet 2`
- [ ] `C-DC-05` `contract` The app answers the health route with status 200 once ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual step. `src: Deployment contract bullet 4`
- [ ] `C-DC-07` `literal` The app writes login credentials to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-08` `contract` The app returns a top-level JSON array from a list endpoint. `src: Deployment contract, API shapes`
- [ ] `C-DC-09` `contract` The app rejects an invalid request as a client error rather than a server error. `src: Deployment contract, API shapes`
- [ ] `C-DC-10` `contract` The app returns an opaque identifier a caller never parses. `src: Deployment contract, conventions`
- [ ] `C-DC-11` `contract` The app returns every timestamp as ISO-8601 in UTC with a trailing Z. `src: Deployment contract, conventions`
- [ ] `C-DC-12` `contract` The app refuses a request body carrying an unknown field. `src: Deployment contract, conventions`
- [ ] `C-DC-13` `literal` The app takes `start_cursor`, `page_size` on a paged request. `src: Deployment contract, conventions`
- [ ] `C-DC-14` `literal` The app returns `has_more`, `next_cursor` on a paged response. `src: Deployment contract, conventions`
- [ ] `C-DC-15` `constraint` The app keeps a cursor stable under concurrent row inserts. `src: Deployment contract, conventions`
- [ ] `C-DC-16` `literal` The app answers `unauthorized` when no valid credential was presented. `src: Deployment contract, error catalogue`
- [ ] `C-DC-17` `literal` The app answers `forbidden_permission` when the authorization decision denied the action. `src: Deployment contract, error catalogue`
- [ ] `C-DC-18` `literal` The app answers `not_found` for a resource the caller may not know exists. `src: Deployment contract, error catalogue`
- [ ] `C-DC-19` `literal` The app answers `conflict_version` when the supplied version is not the stored version. `src: Deployment contract, error catalogue`
- [ ] `C-DC-20` `literal` The app answers `conflict_state` when the resource state forbids the action. `src: Deployment contract, error catalogue`
- [ ] `C-DC-21` `literal` The app answers `validation_failed` with a per-field list in `details`. `src: Deployment contract, error catalogue`
- [ ] `C-DC-22` `literal` The app answers `rate_limited` carrying how long until attempts are accepted again. `src: Deployment contract, error catalogue`
- [ ] `C-DC-23` `constraint` The app returns no store error, no stack trace to a caller. `src: Deployment contract, error catalogue`
- [ ] `C-DC-24` `constraint` The app keeps no in-memory stand-in for the object store. `src: Deployment contract, No mocks`
- [ ] `C-DC-25` `constraint` The app returns no self-answered success in place of a store write. `src: Deployment contract, No mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | password for every seeded account | C-CF-10 | Core features, Auth rule 4 |
| `admin@example.com` | seeded admin address | C-RL-16 | User roles, seeded accounts table |
| `member@example.com` | seeded member address | C-RL-17 | User roles, seeded accounts table |
| `member2@example.com` | second seeded member address | C-RL-18 | User roles, seeded accounts table |
| `guest@example.com` | seeded guest address | C-RL-19 | User roles, seeded accounts table |
| `Editors` | the seeded group | C-RL-20 | User roles, final paragraph |
| `/api/auth/identify` | identifier-first endpoint | C-CF-01 | Core features, Auth rule 1 |
| `/api/auth/login` | login endpoint | C-CF-04 | Core features, Auth rule 2 |
| `/api/auth/logout` | logout endpoint | C-CF-11 | Core features, Auth rule 5 |
| `/api/teamspaces` | teamspace listing endpoint | C-CF-23 | Core features, Teamspaces rule 4 |
| `Engineering` | the open teamspace | C-CF-24 | Data model, seed data |
| `People Ops` | the closed teamspace | C-CF-24 | Data model, seed data |
| `Board Papers` | the private teamspace | C-CF-25 | Data model, seed data |
| `/api/pages/{pageId}/blocks` | block insert endpoint | C-CF-29 | Core features, Pages rule 2 |
| `/api/blocks/{blockId}` | block edit endpoint | C-CF-30 | Core features, Pages rule 2 |
| `/api/blocks/{blockId}/move` | block move endpoint | C-CF-31 | Core features, Pages rule 2 |
| `/api/blocks/{blockId}/restore` | block restore endpoint | C-CF-33 | Core features, Pages rule 2 |
| `Onboarding Checklist` | the page carrying an explicit deny | C-CF-68 | Data model, seed data |
| `/api/pages/{pageId}/access` | grant provenance endpoint | C-CF-73 | Core features, authorization rule 4 |
| `ZEN-1` | first seeded unique-id key | C-CF-89 | Core features, Databases rule 1 |
| `ZEN-2` | second seeded unique-id key | C-CF-89 | Core features, Databases rule 1 |
| `New page` | board column create affordance label | C-CF-96 | Core features, Databases rule 5 |
| `Key notes` | the property hidden from a guest | C-CF-98 | Core features, Databases rule 6 |
| `/api/databases/{dbId}/views/{viewId}/rows` | view rows endpoint | C-CF-100 | Core features, Databases rule 8 |
| `STORAGE_BUCKET` | bucket name variable | C-CF-101 | Core features, Attachments rule 1 |
| `workspaces/{workspace_slug}/pages/{page_id}/{sha256_of_bytes}.{ext}` | object key scheme | C-CF-102 | Core features, Attachments rule 1 |
| `/api/attachments/{attachmentId}` | attachment read endpoint | C-CF-106 | Core features, Attachments rule 3 |
| `handbook-cover.png` | the seeded attachment | C-CF-110 | Core features, Attachments rule 5 |
| `/site/{slug}` | published page route | C-CF-114 | Core features, Publishing rule 2 |
| `Release Notes` | the seeded published page | C-CF-123 | Core features, Publishing rule 6 |
| `release-notes` | the seeded public slug | C-CF-123 | Core features, Publishing rule 6 |
| `/api/admin/members` | member listing endpoint | C-CF-125 | Core features, Admin rule 1 |
| `/api/admin/activity` | activity record endpoint | C-CF-129 | Core features, Admin rule 3 |
| `/api/search` | search endpoint | C-CF-139 | Core features, Search rule 1 |
| `/login` | sign-in route | C-UF-01 | User flow route table row 1 |
| `/w` | workspace home route | C-UF-02 | User flow route table row 2 |
| `/w/search` | workspace search route | C-UF-03 | User flow route table row 3 |
| `/w/p/{pageId}` | page route | C-UF-04 | User flow route table row 4 |
| `/w/db/{dbId}/{viewId}` | database view route | C-UF-05 | User flow route table row 5 |
| `/w/admin/members` | admin members route | C-UF-06 | User flow route table row 6 |
| `/w/admin/teamspaces` | admin teamspaces route | C-UF-07 | User flow route table row 7 |
| `/w/admin/activity` | admin activity route | C-UF-08 | User flow route table row 8 |
| `4.5 to 1` | block palette contrast floor | C-UX-14 | UI/UX notes, block palette paragraph |
| `16px` | body text size | C-UX-16 | UI/UX notes, type paragraph |
| `24px` | body line height | C-UX-16 | UI/UX notes, type paragraph |
| `Teamspaces` | first sidebar section label | C-UX-32 | UI/UX notes, components paragraph |
| `Private` | second sidebar section label | C-UX-32 | UI/UX notes, components paragraph |
| `More` | sidebar section expand row label | C-UX-34 | UI/UX notes, components paragraph |
| `WCAG 2.1` | accessibility standard | C-UX-47 | UI/UX notes, accessibility paragraph |
| `44px by 44px` | coarse-pointer target floor | C-UX-76 | UI/UX notes, responsive paragraph |
| `Share` | page action label | C-UX-82 | UI/UX notes, copy paragraph |
| `New` | page action label | C-UX-82 | UI/UX notes, copy paragraph |
| `Syncing` | sync indicator label | C-UX-82 | UI/UX notes, copy paragraph |
| `To-do` | first board group label | C-UX-83 | UI/UX notes, copy paragraph |
| `In progress` | second board group label | C-UX-83 | UI/UX notes, copy paragraph |
| `In review` | third board group label | C-UX-83 | UI/UX notes, copy paragraph |
| `Complete` | fourth board group label | C-UX-83 | UI/UX notes, copy paragraph |
| `Company tasks` | table view name | C-UX-84 | UI/UX notes, copy paragraph |
| `Current sprint` | board view name | C-UX-84 | UI/UX notes, copy paragraph |
| `Email` | sign-in field label | C-FE-04 | Front-end specification, sign-in surface |
| `Continue` | sign-in primary label | C-FE-05 | Front-end specification, sign-in surface |
| `GET /api/health` | health route | C-TR-07 | Technical requirements para 1 |
| `DATABASE_URL` | database connection variable | C-TR-10 | Technical requirements para 3 |
| `STORAGE_ENDPOINT` | object store address variable | C-TR-11 | Technical requirements para 3 |
| `STORAGE_ACCESS_KEY` | object store key variable | C-TR-13 | Technical requirements para 3 |
| `STORAGE_SECRET_KEY` | object store secret variable | C-TR-13 | Technical requirements para 3 |
| `APP_PUBLIC_URL` | public address variable | C-TR-14 | Technical requirements para 3 |
| `APP_PUBLIC_PORT` | public port variable | C-TR-14 | Technical requirements para 3 |
| `/app/USER_README.md` | credential file path | C-DM-03 | Data model, password paragraph |
| `ZEN-3` | a unique-id key never reissued | C-DM-13 | Data model, uniqueness paragraph |
| `Company Tasks` | the seeded database | C-DM-23 | Data model, seed data |
| `Project` | title property name | C-DM-24 | Data model, seed data |
| `Team` | select property name | C-DM-24 | Data model, seed data |
| `Date` | date property name | C-DM-24 | Data model, seed data |
| `Created by` | created-by property name | C-DM-24 | Data model, seed data |
| `Status` | status property name | C-DM-24 | Data model, seed data |
| `Engineering Handbook` | the seeded unpublished page | C-CF-110 | Data model, seed data |
| `Compensation Bands` | the page in the closed teamspace | C-DM-21 | Data model, seed data |
| `Board Minutes` | the page in the private teamspace | C-DM-22 | Data model, seed data |
| `4173` | container-internal port | C-DC-02 | Deployment contract bullet 1 |
| `start_cursor` | paged request cursor field | C-DC-13 | Deployment contract, conventions |
| `page_size` | paged request size field | C-DC-13 | Deployment contract, conventions |
| `has_more` | paged response flag field | C-DC-14 | Deployment contract, conventions |
| `next_cursor` | paged response cursor field | C-DC-14 | Deployment contract, conventions |
| `unauthorized` | no valid credential code | C-DC-16 | Deployment contract, error catalogue |
| `forbidden_permission` | authorization denial code | C-DC-17 | Deployment contract, error catalogue |
| `not_found` | unknown or unknowable resource code | C-DC-18 | Deployment contract, error catalogue |
| `conflict_version` | version mismatch code | C-DC-19 | Deployment contract, error catalogue |
| `conflict_state` | forbidden state code | C-DC-20 | Deployment contract, error catalogue |
| `validation_failed` | malformed request code | C-DC-21 | Deployment contract, error catalogue |
| `details` | per-field validation list field | C-DC-21 | Deployment contract, error catalogue |
| `rate_limited` | too many attempts code | C-DC-22 | Deployment contract, error catalogue |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the workspace slug used in an object key | C-OV-01 | named by scheme with no literal slug stated beside the scheme |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 8 |
| User roles | 1 | 20 |
| Core features | 45 | 150 |
| User flow | 6 | 24 |
| UI and UX notes | 11 | 84 |
| Front-end specification | 6 | 28 |
| Technical requirements | 6 | 22 |
| Data model | 4 | 26 |
| Constraints | 2 | 13 |
| Deployment contract | 11 | 25 |
