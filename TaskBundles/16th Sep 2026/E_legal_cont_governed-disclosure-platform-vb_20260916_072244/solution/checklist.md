# Checklist: Calder Disclosure Platform

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract
Sections absent: buildplan
Items: 1007
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public corporate site, an editorial console, from one content store. `src: Overview para 1`
- [ ] `C-OV-02` `data` The app carries five divisions: `group`, `trading`, `capital`, `maritime`, `kite-energy`. `src: Overview para 2`
- [ ] `C-OV-03` `data` The app carries three offices in three regulatory regimes: Geneva, Dubai, Singapore. `src: Overview para 2`
- [ ] `C-OV-04` `constraint` The app places every content record in exactly one division. `src: Overview para 3`
- [ ] `C-OV-05` `data` The app records a membership as an edge carrying a role, a division, a granting principal, an expiry. `src: Overview para 3`
- [ ] `C-OV-06` `constraint` The app refuses any route by which a record reaches the public site without passing the review chain. `src: Overview para 4`
- [ ] `C-OV-07` `constraint` The app refuses an approval of a record by the principal who authored the record. `src: Overview para 4`
- [ ] `C-OV-08` `capability` The app voids an approval when the approved words of the record change. `src: Overview para 4`
- [ ] `C-OV-09` `capability` The app offers a capped shortcut for changes that cannot carry meaning. `src: Overview para 4`
- [ ] `C-OV-10` `constraint` The app omits a confidential reporting channel, a federated sign-in, an email delivery path from the product. `src: Overview para 6`
- [ ] `C-OV-11` `constraint` The app omits a price, a position, a cargo, a vessel movement, a counterparty record from the product. `src: Overview para 6`
- [ ] `C-OV-12` `constraint` The app keeps an embargoed release absent from everything the public path can read. `src: Overview para 7`
- [ ] `C-OV-13` `capability` The app renders an embargoed release to a publisher on the record's own division under a banner naming the instant. `src: Overview para 7`
- [ ] `C-OV-14` `constraint` The app publishes an embargoed release exactly once at the embargo instant. `src: Overview para 7`

## C-RL User roles

- [ ] `C-RL-01` `constraint` The app offers no registration surface. `src: User roles para 1`
- [ ] `C-RL-02` `constraint` The app offers no password reset surface. `src: User roles para 1`
- [ ] `C-RL-03` `role` An author creates a draft on a division the author holds. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An author submits a draft for review. `src: User roles table row 1`
- [ ] `C-RL-05` `role` An author uploads media on a division the author holds. `src: User roles table row 1`
- [ ] `C-RL-06` `constraint` The app refuses an author request to approve any stage of any submission. `src: User roles table row 1`
- [ ] `C-RL-07` `constraint` The app refuses an author request to set a disclosure class. `src: User roles table row 1`
- [ ] `C-RL-08` `constraint` The app refuses an author request to publish a record. `src: User roles table row 1`
- [ ] `C-RL-09` `constraint` The app refuses an author request touching a record on a division the author does not hold. `src: User roles table row 1`
- [ ] `C-RL-10` `role` A legal reviewer approves the legal stage of a submission on a division the reviewer holds. `src: User roles table row 2`
- [ ] `C-RL-11` `role` A legal reviewer requests changes on the legal stage. `src: User roles table row 2`
- [ ] `C-RL-12` `constraint` The app refuses a legal reviewer request to approve the compliance stage of the same submission. `src: User roles table row 2`
- [ ] `C-RL-13` `constraint` The app refuses a legal reviewer request to edit body copy. `src: User roles table row 2`
- [ ] `C-RL-14` `constraint` The app refuses a legal reviewer request to approve a submission the reviewer authored. `src: User roles table row 2`
- [ ] `C-RL-15` `role` A compliance officer approves the compliance stage of a submission on a division the officer holds. `src: User roles table row 3`
- [ ] `C-RL-16` `role` A compliance officer sets the disclosure class on a record. `src: User roles table row 3`
- [ ] `C-RL-17` `constraint` The app refuses a compliance officer request to edit body copy. `src: User roles table row 3`
- [ ] `C-RL-18` `constraint` The app refuses a compliance officer request to approve a stage another role owns. `src: User roles table row 3`
- [ ] `C-RL-19` `constraint` The app refuses a compliance officer request to approve a second stage of a submission the officer already decided. `src: User roles table row 3`
- [ ] `C-RL-20` `constraint` The app refuses a compliance officer request to publish a record. `src: User roles table row 3`
- [ ] `C-RL-21` `role` A publisher publishes an approved record on a division the publisher holds. `src: User roles table row 4`
- [ ] `C-RL-22` `role` A publisher schedules an approved record for an embargo instant. `src: User roles table row 4`
- [ ] `C-RL-23` `role` A publisher cancels a schedule on an embargoed record. `src: User roles table row 4`
- [ ] `C-RL-24` `role` A publisher unpublishes a published record. `src: User roles table row 4`
- [ ] `C-RL-25` `constraint` The app refuses a publisher request to approve any stage. `src: User roles table row 4`
- [ ] `C-RL-26` `constraint` The app refuses a publisher request to publish a record that is not `approved`. `src: User roles table row 4`
- [ ] `C-RL-27` `constraint` The app refuses a publisher request to publish a `market_sensitive` record carrying no scheduled instant. `src: User roles table row 4`
- [ ] `C-RL-28` `role` A group admin reads the title, the type, the state, the instants of every record across every division. `src: User roles table row 5`
- [ ] `C-RL-29` `role` A group admin reads the whole audit trail. `src: User roles table row 5`
- [ ] `C-RL-30` `role` A group admin reads the exception report. `src: User roles table row 5`
- [ ] `C-RL-31` `role` A group admin grants a membership. `src: User roles table row 5`
- [ ] `C-RL-32` `role` A group admin revokes a membership. `src: User roles table row 5`
- [ ] `C-RL-33` `constraint` The app refuses a group admin request for the body of a record that is not published. `src: User roles table row 5`
- [ ] `C-RL-34` `constraint` The app refuses a group admin request to approve a stage. `src: User roles table row 5`
- [ ] `C-RL-35` `constraint` The app refuses a group admin request to publish a record. `src: User roles table row 5`
- [ ] `C-RL-36` `constraint` The app refuses a group admin request to edit a record. `src: User roles table row 5`
- [ ] `C-RL-37` `constraint` The app enforces authorization server side on every mutating endpoint. `src: User roles, enforcement paragraph`
- [ ] `C-RL-38` `constraint` The app leaves protected state unchanged after a denied request. `src: User roles, enforcement paragraph`
- [ ] `C-RL-39` `constraint` The app answers deny on an unrecognised action. `src: User roles, decision paragraph`
- [ ] `C-RL-40` `constraint` The app answers deny on an unrecognised resource. `src: User roles, decision paragraph`
- [ ] `C-RL-41` `constraint` The app answers deny when an error occurs during a decision. `src: User roles, decision paragraph`
- [ ] `C-RL-42` `constraint` The app refuses a request for a record on a division the caller does not hold, as an identifier never issued is refused. `src: User roles, scoping paragraph`
- [ ] `C-RL-43` `literal` The app seeds the account `author@example.com` holding `author` on `trading`. `src: User roles, seeded accounts table`
- [ ] `C-RL-44` `literal` The app seeds the account `author@example.com` holding `legal_reviewer` on `capital`. `src: User roles, seeded accounts table`
- [ ] `C-RL-45` `literal` The app seeds the account `author2@example.com` holding `author` on `capital`. `src: User roles, seeded accounts table`
- [ ] `C-RL-46` `literal` The app seeds the account `legal_reviewer@example.com` holding both reviewer roles on `trading`. `src: User roles, seeded accounts table`
- [ ] `C-RL-47` `literal` The app seeds the account `compliance_officer@example.com` holding `compliance_officer` on two divisions. `src: User roles, seeded accounts table`
- [ ] `C-RL-48` `literal` The app seeds the account `publisher@example.com` holding `publisher` on all five divisions. `src: User roles, seeded accounts table`
- [ ] `C-RL-49` `literal` The app seeds the account `group_admin@example.com` holding no content membership. `src: User roles, seeded accounts table`
- [ ] `C-RL-50` `literal` The app accepts the password `deku-demo-pw-2026` at login for every seeded account. `src: User roles, seeded accounts table`

## C-CF Core features

- [ ] `C-CF-01` `literal` The app accepts an email, a password at `POST /api/auth/login`. `src: Core features, Auth rule 1`
- [ ] `C-CF-02` `literal` The app returns a bearer token in a field named `access_token` on a successful login. `src: Core features, Auth rule 1`
- [ ] `C-CF-03` `constraint` The app rejects a wrong password carrying no hint about whether the address exists. `src: Core features, Auth rule 1`
- [ ] `C-CF-04` `constraint` The app denies a request carrying no bearer token on every endpoint outside the anonymous set. `src: Core features, Auth rule 2`
- [ ] `C-CF-05` `constraint` The app denies a request carrying an expired bearer token. `src: Core features, Auth rule 2`
- [ ] `C-CF-06` `constraint` The app denies a request carrying an unparseable bearer token. `src: Core features, Auth rule 2`
- [ ] `C-CF-07` `data` The app stores every password hashed. `src: Core features, Auth rule 3`
- [ ] `C-CF-08` `literal` The app ends a session at `POST /api/auth/logout`. `src: Core features, Auth rule 4`
- [ ] `C-CF-09` `constraint` The app refuses the bearer token a logout was called with on the next request. `src: Core features, Auth rule 4`
- [ ] `C-CF-10` `constraint` The app exposes no endpoint creating a principal from an unauthenticated request. `src: Core features, Auth rule 5`
- [ ] `C-CF-11` `constraint` The app exposes no endpoint resetting a password. `src: Core features, Auth rule 5`
- [ ] `C-CF-12` `capability` The app refuses further password attempts for one address after five failures inside a rolling window. `src: Core features, Auth rule 6`
- [ ] `C-CF-13` `capability` The app accepts password attempts for that address again once the window passes. `src: Core features, Auth rule 6`
- [ ] `C-CF-14` `constraint` The app never applies a permanent lockout to an address. `src: Core features, Auth rule 6`
- [ ] `C-CF-15` `constraint` The app carries no hint about whether an address exists in a rate-limit refusal. `src: Core features, Auth rule 6`
- [ ] `C-CF-16` `capability` The app signs in a principal holding no membership. `src: Core features, Auth rule 7`
- [ ] `C-CF-17` `ui` The app shows a principal holding no membership a surface stating the principal has no access, naming who grants access. `src: Core features, Auth rule 7`
- [ ] `C-CF-18` `constraint` The app gives a newly seen principal no default role. `src: Core features, Auth rule 7`
- [ ] `C-CF-19` `capability` The app refuses a deactivated principal's existing bearer token on the next request. `src: Core features, Auth rule 8`
- [ ] `C-CF-20` `capability` The app stops a deactivated principal's memberships granting anything. `src: Core features, Auth rule 8`
- [ ] `C-CF-21` `capability` The app returns a deactivated principal's pending approval to the role group on the division. `src: Core features, Auth rule 8`
- [ ] `C-CF-22` `capability` The app revokes a delegation granted by a deactivated principal. `src: Core features, Auth rule 8`
- [ ] `C-CF-23` `contract` The app applies an access loss on a deactivation immediately. `src: Core features, Auth rule 8`
- [ ] `C-CF-24` `contract` The app applies an ordinary membership change within 60 seconds. `src: Core features, Auth rule 8`
- [ ] `C-CF-25` `contract` The app makes a console write readable by the writer immediately. `src: Core features, Auth rule 9`
- [ ] `C-CF-26` `contract` The app makes a publication public within 30 seconds. `src: Core features, Auth rule 9`
- [ ] `C-CF-27` `contract` The app makes a publication searchable within 30 seconds. `src: Core features, Auth rule 9`
- [ ] `C-CF-28` `contract` The app makes an audit write readable immediately. `src: Core features, Auth rule 9`
- [ ] `C-CF-29` `data` The app draws every instant from one synchronised clock. `src: Core features, Auth rule 10`
- [ ] `C-CF-30` `data` The app orders the trail by a monotonic sequence rather than by a wall-clock reading. `src: Core features, Auth rule 10`
- [ ] `C-CF-31` `literal` The app seeds the division key `group` named `Calder Group`. `src: Core features, Divisions rule 1`
- [ ] `C-CF-32` `literal` The app seeds the division key `trading` named `Calder Trading`. `src: Core features, Divisions rule 1`
- [ ] `C-CF-33` `literal` The app seeds the division key `capital` named `Calder Capital`. `src: Core features, Divisions rule 1`
- [ ] `C-CF-34` `literal` The app seeds the division key `maritime` named `Calder Maritime`. `src: Core features, Divisions rule 1`
- [ ] `C-CF-35` `literal` The app seeds the division key `kite-energy` named `Kite Energy`. `src: Core features, Divisions rule 1`
- [ ] `C-CF-36` `constraint` The app fixes the division set at five. `src: Core features, Divisions rule 1`
- [ ] `C-CF-37` `data` The app carries a wordmark on a division record, defaulting to the group wordmark. `src: Core features, Divisions rule 2`
- [ ] `C-CF-38` `data` The app carries a primary colour role on a division record, defaulting to the group value. `src: Core features, Divisions rule 2`
- [ ] `C-CF-39` `ui` The app renders the division bar label from the division's own name rather than composing the label from the group name. `src: Core features, Divisions rule 2`
- [ ] `C-CF-40` `constraint` The app scopes publish rights so another division's team cannot apply the `kite-energy` mark. `src: Core features, Divisions rule 2`
- [ ] `C-CF-41` `capability` The app falls back to the group mark when a division mark is missing. `src: Core features, Divisions rule 2`
- [ ] `C-CF-42` `constraint` The app never renders a broken mark. `src: Core features, Divisions rule 2`
- [ ] `C-CF-43` `data` The app records a membership as a row carrying a principal, a division, a role, a granting principal, an optional justification, an optional expiry. `src: Core features, Divisions rule 3`
- [ ] `C-CF-44` `capability` The app allows one principal to hold two roles on one division. `src: Core features, Divisions rule 3`
- [ ] `C-CF-45` `literal` The app lists every membership with the membership's provenance at `GET /api/admin/members`. `src: Core features, Divisions rule 3`
- [ ] `C-CF-46` `capability` The app stops a membership granting anything the moment the expiry passes. `src: Core features, Divisions rule 4`
- [ ] `C-CF-47` `data` The app retains an expired membership rather than deleting the membership. `src: Core features, Divisions rule 4`
- [ ] `C-CF-48` `literal` The app requires `group_admin` at `POST /api/admin/memberships`. `src: Core features, Divisions rule 5`
- [ ] `C-CF-49` `data` The app records the granting principal on every membership created. `src: Core features, Divisions rule 5`
- [ ] `C-CF-50` `constraint` The app requires a justification on a membership granted to a single named principal. `src: Core features, Divisions rule 5`
- [ ] `C-CF-51` `constraint` The app caps an individually granted membership at 90 days. `src: Core features, Divisions rule 5`
- [ ] `C-CF-52` `capability` The app lists an individually granted membership in the exception report. `src: Core features, Divisions rule 5`
- [ ] `C-CF-53` `constraint` The app creates no membership on a grant attempt from a session holding no `group_admin`. `src: Core features, Divisions rule 5`
- [ ] `C-CF-54` `constraint` The app records a content membership granted to a group admin as time bounded, justified. `src: Core features, Divisions rule 6`
- [ ] `C-CF-55` `contract` The app costs one decision over a page of 50 records rather than 50 separate decisions. `src: Core features, Divisions rule 7`
- [ ] `C-CF-56` `constraint` The app returns a count matching the rows the same caller may read. `src: Core features, Divisions rule 7`
- [ ] `C-CF-57` `literal` The app requires `group_admin` at `GET /api/admin/exceptions`. `src: Core features, Divisions rule 8`
- [ ] `C-CF-58` `capability` The app returns individual grants carrying a justification, an expiry, in the exception report. `src: Core features, Divisions rule 8`
- [ ] `C-CF-59` `capability` The app returns active delegations carrying both parties, an end instant, in the exception report. `src: Core features, Divisions rule 8`
- [ ] `C-CF-60` `capability` The app returns fast-path publications carrying counts in the exception report. `src: Core features, Divisions rule 8`
- [ ] `C-CF-61` `capability` The app returns denied authorization attempts grouped by principal, by action, in the exception report. `src: Core features, Divisions rule 8`
- [ ] `C-CF-62` `data` The app carries one envelope on every content record whatever the record's type. `src: Core features, Records rule 1`
- [ ] `C-CF-63` `data` The app issues a record identifier that is never a guessable sequence. `src: Core features, Records rule 1`
- [ ] `C-CF-64` `data` The app never rewrites a record's first-publication instant. `src: Core features, Records rule 1`
- [ ] `C-CF-65` `data` The app holds `current_revision_id`, `published_revision_id` as two distinct fields. `src: Core features, Records rule 2`
- [ ] `C-CF-66` `constraint` The app reads only `published_revision_id` on the public path. `src: Core features, Records rule 2`
- [ ] `C-CF-67` `data` The app carries nine record types: `page`, `release`, `product`, `vessel`, `investment`, `person`, `figures`, `policy`, `redirect`. `src: Core features, Records rule 3`
- [ ] `C-CF-68` `data` The app holds the approval chain a type requires as readable data rather than as a branch in code. `src: Core features, Records rule 3`
- [ ] `C-CF-69` `constraint` The app leaves a submission already in flight unaffected by a change to the chain. `src: Core features, Records rule 3`
- [ ] `C-CF-70` `constraint` The app never rewrites a revision. `src: Core features, Records rule 4`
- [ ] `C-CF-71` `data` The app carries a parent, an author, an instant, the full field set on every revision. `src: Core features, Records rule 4`
- [ ] `C-CF-72` `data` The app carries a hash over the whole canonical field set on every revision. `src: Core features, Records rule 4`
- [ ] `C-CF-73` `data` The app carries a second hash over only the approved set of the record's type. `src: Core features, Records rule 4`
- [ ] `C-CF-74` `data` The app puts the title, the standfirst, the body, the disclosure class, the lead image in a release's approved set. `src: Core features, Records rule 5`
- [ ] `C-CF-75` `data` The app leaves the image credit, the caption, the related links outside a release's approved set. `src: Core features, Records rule 5`
- [ ] `C-CF-76` `literal` The app permits exactly the block types `paragraph`, `subheading_2`, `subheading_3`, `list_unordered`, `list_ordered`, `quote`, `image`, `table`. `src: Core features, Records rule 6`
- [ ] `C-CF-77` `constraint` The app rejects a block type outside the permitted set when the block is written. `src: Core features, Records rule 6`
- [ ] `C-CF-78` `constraint` The app never strips a rejected block at render instead of rejecting the block at write. `src: Core features, Records rule 6`
- [ ] `C-CF-79` `constraint` The app refuses arbitrary markup in a body. `src: Core features, Records rule 6`
- [ ] `C-CF-80` `constraint` The app refuses an embed from a third-party origin in a body. `src: Core features, Records rule 6`
- [ ] `C-CF-81` `data` The app carries a block identifier that stays the same across revisions. `src: Core features, Records rule 7`
- [ ] `C-CF-82` `capability` The app reports a moved block as moved rather than as one deletion, one creation. `src: Core features, Records rule 7`
- [ ] `C-CF-83` `literal` The app creates a record in `draft` at `POST /api/content/records`. `src: Core features, Records rule 8`
- [ ] `C-CF-84` `constraint` The app requires `author` on the named division to create a record. `src: Core features, Records rule 8`
- [ ] `C-CF-85` `literal` The app edits a record at `PATCH /api/content/records/{id}`, producing a revision. `src: Core features, Records rule 8`
- [ ] `C-CF-86` `constraint` The app leaves the stored record unchanged after a denied create attempt. `src: Core features, Records rule 8`
- [ ] `C-CF-87` `constraint` The app leaves the stored record unchanged after a denied edit attempt. `src: Core features, Records rule 8`
- [ ] `C-CF-88` `constraint` The app accepts exactly one of two edits carrying the same revision identifier. `src: Core features, Records rule 9`
- [ ] `C-CF-89` `capability` The app advances the record's current revision on the accepted edit. `src: Core features, Records rule 9`
- [ ] `C-CF-90` `capability` The app rejects the losing edit as a conflict carrying the current value. `src: Core features, Records rule 9`
- [ ] `C-CF-91` `constraint` The app holds the one-accepted-edit rule under real concurrency. `src: Core features, Records rule 9`
- [ ] `C-CF-92` `constraint` The app refuses to archive a division holding records. `src: Core features, Records rule 10`
- [ ] `C-CF-93` `constraint` The app refuses to delete a media record in use. `src: Core features, Records rule 10`
- [ ] `C-CF-94` `ui` The app shows every record referencing a media record so a refusal to delete names a cause. `src: Core features, Records rule 10`
- [ ] `C-CF-95` `capability` The app empties the origin reference on a redirect whose minting record is deleted. `src: Core features, Records rule 10`
- [ ] `C-CF-96` `constraint` The app never deletes the revisions of a record that reached publication. `src: Core features, Records rule 10`
- [ ] `C-CF-97` `constraint` The app never repairs a broken reference automatically. `src: Core features, Records rule 10`
- [ ] `C-CF-98` `constraint` The app sanitises a value when the value is written rather than when the value is rendered. `src: Core features, Records rule 11`
- [ ] `C-CF-99` `constraint` The app bounds the length of every plain text field. `src: Core features, Records rule 11`
- [ ] `C-CF-100` `constraint` The app removes control characters from a plain text field. `src: Core features, Records rule 11`
- [ ] `C-CF-101` `constraint` The app trims the edges of a plain text field. `src: Core features, Records rule 11`
- [ ] `C-CF-102` `constraint` The app verifies an uploaded file's type by inspecting the bytes. `src: Core features, Records rule 11`
- [ ] `C-CF-103` `constraint` The app generates a slug rather than accepting a supplied slug. `src: Core features, Records rule 11`
- [ ] `C-CF-104` `data` The app stores a telephone number both raw, normalised. `src: Core features, Records rule 11`
- [ ] `C-CF-105` `constraint` The app never uses the raw form of an address to build a request. `src: Core features, Records rule 11`
- [ ] `C-CF-106` `literal` The app carries ten states: `draft`, `in_review`, `legal_review`, `compliance_review`, `changes_requested`, `approved`, `embargoed`, `published`, `unpublished`, `archived`. `src: Core features, chain rule 1`
- [ ] `C-CF-107` `constraint` The app offers no reset returning a record to `draft` outside the stated transitions. `src: Core features, chain rule 1`
- [ ] `C-CF-108` `literal` The app moves a record from `draft` to `in_review` at `POST /api/workflow/records/{id}/submit`. `src: Core features, chain rule 2`
- [ ] `C-CF-109` `constraint` The app requires `author` on the division to submit a record. `src: Core features, chain rule 2`
- [ ] `C-CF-110` `constraint` The app refuses a submit on a record missing a required field. `src: Core features, chain rule 2`
- [ ] `C-CF-111` `constraint` The app refuses a submit on a record whose type requires a disclosure class the record lacks. `src: Core features, chain rule 2`
- [ ] `C-CF-112` `data` The app opens a submission carrying the record, the revision, the chain version in force, the submitting principal. `src: Core features, chain rule 2`
- [ ] `C-CF-113` `constraint` The app keeps at most one submission open per record. `src: Core features, chain rule 2`
- [ ] `C-CF-114` `constraint` The app rejects a second concurrent submit rather than opening a second submission. `src: Core features, chain rule 2`
- [ ] `C-CF-115` `capability` The app moves a record from `in_review` to `legal_review` on assignment of a legal reviewer. `src: Core features, chain rule 3`
- [ ] `C-CF-116` `capability` The app lets an author withdraw the author's own submission from `in_review` to `draft`. `src: Core features, chain rule 3`
- [ ] `C-CF-117` `constraint` The app refuses a withdrawal from `in_review` by a principal who is not the author. `src: Core features, chain rule 3`
- [ ] `C-CF-118` `capability` The app moves a record from `legal_review` to `compliance_review` on a legal approval. `src: Core features, chain rule 4`
- [ ] `C-CF-119` `constraint` The app requires `legal_reviewer` on the division for a legal approval. `src: Core features, chain rule 4`
- [ ] `C-CF-120` `capability` The app moves a record from `legal_review` to `changes_requested` on a legal rejection. `src: Core features, chain rule 4`
- [ ] `C-CF-121` `constraint` The app requires a comment on a changes-requested transition. `src: Core features, chain rule 4`
- [ ] `C-CF-122` `capability` The app moves a record from `compliance_review` to `approved` on a compliance approval. `src: Core features, chain rule 5`
- [ ] `C-CF-123` `constraint` The app requires `compliance_officer` on the division for a compliance approval. `src: Core features, chain rule 5`
- [ ] `C-CF-124` `constraint` The app refuses a compliance approval by the submission's author. `src: Core features, chain rule 5`
- [ ] `C-CF-125` `constraint` The app refuses a compliance approval by the principal who performed the legal approval on the same submission. `src: Core features, chain rule 5`
- [ ] `C-CF-126` `capability` The app returns a record from `changes_requested` to `draft` on the next edit. `src: Core features, chain rule 6`
- [ ] `C-CF-127` `capability` The app clears both stage decisions when a record returns to `draft`. `src: Core features, chain rule 6`
- [ ] `C-CF-128` `data` The app runs the legal stage before the compliance stage by default. `src: Core features, chain rule 6`
- [ ] `C-CF-129` `capability` The app allows a type to declare the two stages parallel. `src: Core features, chain rule 6`
- [ ] `C-CF-130` `constraint` The app requires both parallel stages to complete before `approved`. `src: Core features, chain rule 6`
- [ ] `C-CF-131` `capability` The app voids both parallel stages on a changes-requested transition. `src: Core features, chain rule 6`
- [ ] `C-CF-132` `constraint` The app refuses an approval of a submission by the submission's author on any stage. `src: Core features, chain rule 7`
- [ ] `C-CF-133` `constraint` The app refuses an approval of a submission by the author under any delegation. `src: Core features, chain rule 7`
- [ ] `C-CF-134` `data` The app records a refused self-approval carrying a reason. `src: Core features, chain rule 7`
- [ ] `C-CF-135` `data` The app records an approval against the approved-set hash of the revision approved. `src: Core features, chain rule 8`
- [ ] `C-CF-136` `capability` The app voids every approval on a record when a field in the approved set changes. `src: Core features, chain rule 8`
- [ ] `C-CF-137` `capability` The app returns a record to `draft` when a field in the approved set changes. `src: Core features, chain rule 8`
- [ ] `C-CF-138` `capability` The app leaves approvals standing when only fields outside the approved set change. `src: Core features, chain rule 8`
- [ ] `C-CF-139` `data` The app records a change outside the approved set. `src: Core features, chain rule 8`
- [ ] `C-CF-140` `literal` The app creates a delegation at `POST /api/workflow/delegations`. `src: Core features, chain rule 9`
- [ ] `C-CF-141` `constraint` The app scopes a delegation to one role on one division. `src: Core features, chain rule 9`
- [ ] `C-CF-142` `constraint` The app requires an end instant on a delegation no more than 30 days out. `src: Core features, chain rule 9`
- [ ] `C-CF-143` `constraint` The app refuses a delegation created by a delegate. `src: Core features, chain rule 9`
- [ ] `C-CF-144` `data` The app records both the delegate, the delegator on a decision produced under a delegation. `src: Core features, chain rule 9`
- [ ] `C-CF-145` `capability` The app revokes a delegation immediately on the delegator's request. `src: Core features, chain rule 9`
- [ ] `C-CF-146` `capability` The app revokes a delegation immediately on a group admin's request. `src: Core features, chain rule 9`
- [ ] `C-CF-147` `constraint` The app refuses an approval by a delegate who authored the submission. `src: Core features, chain rule 9`
- [ ] `C-CF-148` `capability` The app publishes a change confined to fields outside the approved set by one publisher action with no review stage. `src: Core features, chain rule 10`
- [ ] `C-CF-149` `constraint` The app requires the record to be in `published` for a fast-path publication. `src: Core features, chain rule 10`
- [ ] `C-CF-150` `constraint` The app requires `author` on the division for a fast-path change. `src: Core features, chain rule 10`
- [ ] `C-CF-151` `data` The app records a fast-path publication identically to an ordinary publication. `src: Core features, chain rule 10`
- [ ] `C-CF-152` `constraint` The app forces the next change through the full chain after three fast-path publications on one record within seven days. `src: Core features, chain rule 10`
- [ ] `C-CF-153` `capability` The app sends a correction of a published release through the chain again. `src: Core features, chain rule 11`
- [ ] `C-CF-154` `ui` The app renders a correction notice carrying an instant on the corrected page. `src: Core features, chain rule 11`
- [ ] `C-CF-155` `constraint` The app allows only a compliance officer to set whether a correction is material. `src: Core features, chain rule 11`
- [ ] `C-CF-156` `constraint` The app serialises transitions per record. `src: Core features, chain rule 12`
- [ ] `C-CF-157` `constraint` The app accepts exactly one of two simultaneous approvals. `src: Core features, chain rule 12`
- [ ] `C-CF-158` `capability` The app rejects the losing approval carrying the current state. `src: Core features, chain rule 12`
- [ ] `C-CF-159` `constraint` The app records no second approval after a rejected simultaneous approval. `src: Core features, chain rule 12`
- [ ] `C-CF-160` `constraint` The app takes the state the caller believes the record holds on every transition endpoint. `src: Core features, chain rule 12`
- [ ] `C-CF-161` `capability` The app rejects a transition as a conflict when the record has moved. `src: Core features, chain rule 12`
- [ ] `C-CF-162` `literal` The app returns four queues at `GET /api/workflow/inbox`. `src: Core features, chain rule 13`
- [ ] `C-CF-163` `data` The app orders the inbox queues as awaiting a decision, sent back, own drafts, watching. `src: Core features, chain rule 13`
- [ ] `C-CF-164` `ui` The app renders an authored line stating nothing awaits a decision when the first inbox queue is empty. `src: Core features, chain rule 13`
- [ ] `C-CF-165` `constraint` The app shows a notification inside the console only. `src: Core features, chain rule 14`
- [ ] `C-CF-166` `data` The app carries a title, a division, a record type, a link on a notification. `src: Core features, chain rule 14`
- [ ] `C-CF-167` `constraint` The app never carries a record body on a notification. `src: Core features, chain rule 14`
- [ ] `C-CF-168` `constraint` The app never carries the title of a `market_sensitive` record on a notification. `src: Core features, chain rule 14`
- [ ] `C-CF-169` `capability` The app produces one notification for ten changes to one record inside an hour. `src: Core features, chain rule 14`
- [ ] `C-CF-170` `capability` The app batches a non-urgent notification into a digest at a per-principal frequency defaulting to daily. `src: Core features, chain rule 14`
- [ ] `C-CF-171` `constraint` The app never batches an approval request, an escalation, a security-relevant notification. `src: Core features, chain rule 14`
- [ ] `C-CF-172` `capability` The app escalates a submission awaiting a decision for 48 hours to the division's other approvers. `src: Core features, chain rule 14`
- [ ] `C-CF-173` `capability` The app escalates a submission awaiting a decision for 96 hours to `group_admin`. `src: Core features, chain rule 14`
- [ ] `C-CF-174` `constraint` The app refuses to switch off telling a principal that the principal's own permissions changed. `src: Core features, chain rule 14`
- [ ] `C-CF-175` `literal` The app carries four disclosure classes: `general`, `regulated`, `market_sensitive`, `restricted`. `src: Core features, classification rule 1`
- [ ] `C-CF-176` `capability` The app appends the regulated disclaimer to a `regulated` record's page. `src: Core features, classification rule 1`
- [ ] `C-CF-177` `constraint` The app keeps a `restricted` record out of the published projection under every state. `src: Core features, classification rule 1`
- [ ] `C-CF-178` `literal` The app sets a disclosure class at `POST /api/content/records/{id}/classify`. `src: Core features, classification rule 2`
- [ ] `C-CF-179` `constraint` The app requires `compliance_officer` on the division to set a disclosure class. `src: Core features, classification rule 2`
- [ ] `C-CF-180` `constraint` The app leaves the stored class unchanged after a classify attempt from an author session. `src: Core features, classification rule 2`
- [ ] `C-CF-181` `constraint` The app leaves the stored class unchanged after a classify attempt from a publisher session. `src: Core features, classification rule 2`
- [ ] `C-CF-182` `constraint` The app refuses a move out of `compliance_review` on a record carrying no class. `src: Core features, classification rule 3`
- [ ] `C-CF-183` `constraint` The app refuses a move from `approved` straight to `published` on a `market_sensitive` record. `src: Core features, classification rule 4`
- [ ] `C-CF-184` `constraint` The app rejects a publish attempt on a `market_sensitive` record carrying no scheduled instant. `src: Core features, classification rule 4`
- [ ] `C-CF-185` `data` The app holds every controlled text in the policy register. `src: Core features, classification rule 5`
- [ ] `C-CF-186` `data` The app carries a reference code, a title, an integer version, an effective-from instant on a register entry. `src: Core features, classification rule 5`
- [ ] `C-CF-187` `data` The app carries an accountable role, a review interval in days on a register entry. `src: Core features, classification rule 5`
- [ ] `C-CF-188` `data` The app carries the scoped divisions, the applicable jurisdictions on a register entry. `src: Core features, classification rule 5`
- [ ] `C-CF-189` `data` The app carries whether a register entry is published internally, externally, both. `src: Core features, classification rule 5`
- [ ] `C-CF-190` `constraint` The app keeps a reference code paired with a version unique. `src: Core features, classification rule 5`
- [ ] `C-CF-191` `constraint` The app creates a version rather than editing a version on a register change. `src: Core features, classification rule 6`
- [ ] `C-CF-192` `capability` The app resolves a disclaimer at publication against the register version then in force. `src: Core features, classification rule 7`
- [ ] `C-CF-193` `data` The app freezes the resolved disclaimer version into the published document. `src: Core features, classification rule 7`
- [ ] `C-CF-194` `constraint` The app never changes what an already published page said when a disclaimer is updated. `src: Core features, classification rule 7`
- [ ] `C-CF-195` `constraint` The app renders no register entry whose effective-from instant lies in the future. `src: Core features, classification rule 8`
- [ ] `C-CF-196` `ui` The app shows a future register entry in the console carrying the entry's date. `src: Core features, classification rule 8`
- [ ] `C-CF-197` `capability` The app makes a superseded register version reachable from the current version carrying the period the version applied. `src: Core features, classification rule 8`
- [ ] `C-CF-198` `ui` The app flags a register entry overdue for review in the console. `src: Core features, classification rule 9`
- [ ] `C-CF-199` `capability` The app lists a register entry overdue for review in the exception report. `src: Core features, classification rule 9`
- [ ] `C-CF-200` `constraint` The app keeps rendering a register entry overdue for review. `src: Core features, classification rule 9`
- [ ] `C-CF-201` `literal` The app schedules an approved record at `POST /api/workflow/records/{id}/schedule`. `src: Core features, embargo rule 1`
- [ ] `C-CF-202` `constraint` The app requires `publisher` on the division to schedule a record. `src: Core features, embargo rule 1`
- [ ] `C-CF-203` `constraint` The app requires the record to be `approved` to schedule the record. `src: Core features, embargo rule 1`
- [ ] `C-CF-204` `capability` The app moves a scheduled record to `embargoed`. `src: Core features, embargo rule 1`
- [ ] `C-CF-205` `constraint` The app rejects an embargo instant lying in the past at the transition. `src: Core features, embargo rule 2`
- [ ] `C-CF-206` `constraint` The app never silently publishes a record scheduled for a past instant. `src: Core features, embargo rule 2`
- [ ] `C-CF-207` `constraint` The app omits an embargoed release from `GET /api/public/releases`. `src: Core features, embargo rule 3`
- [ ] `C-CF-208` `constraint` The app answers an embargoed release's public slug as a slug never issued is answered. `src: Core features, embargo rule 3`
- [ ] `C-CF-209` `constraint` The app omits an embargoed release from `GET /api/public/search`. `src: Core features, embargo rule 3`
- [ ] `C-CF-210` `constraint` The app refuses an embargoed release's lead image at `GET /api/public/media/{mediaId}`. `src: Core features, embargo rule 3`
- [ ] `C-CF-211` `constraint` The app omits an embargoed release from the count at `GET /api/public/counters`. `src: Core features, embargo rule 3`
- [ ] `C-CF-212` `ui` The app renders an embargoed record in full to a publisher on the record's division under a persistent banner naming the release instant. `src: Core features, embargo rule 4`
- [ ] `C-CF-213` `data` The app stores an embargo instant in absolute time. `src: Core features, embargo rule 5`
- [ ] `C-CF-214` `ui` The app shows an embargo instant both as the instant, in the reading principal's local time. `src: Core features, embargo rule 5`
- [ ] `C-CF-215` `capability` The app publishes an embargoed record when the instant passes. `src: Core features, embargo rule 6`
- [ ] `C-CF-216` `constraint` The app publishes an embargoed record exactly once. `src: Core features, embargo rule 6`
- [ ] `C-CF-217` `constraint` The app makes the publication a conditional move from `embargoed`. `src: Core features, embargo rule 6`
- [ ] `C-CF-218` `constraint` The app writes one projection row for one embargoed record reaching the instant. `src: Core features, embargo rule 6`
- [ ] `C-CF-219` `constraint` The app advances the counter once for one embargoed record reaching the instant. `src: Core features, embargo rule 6`
- [ ] `C-CF-220` `constraint` The app still publishes exactly once after a restart across the embargo instant. `src: Core features, embargo rule 6`
- [ ] `C-CF-221` `data` The app records the delay on a record published more than 60 seconds after the record's instant. `src: Core features, embargo rule 7`
- [ ] `C-CF-222` `literal` The app returns an embargoed record to `approved` at `DELETE /api/workflow/records/{id}/schedule`. `src: Core features, embargo rule 8`
- [ ] `C-CF-223` `constraint` The app requires `publisher` to cancel a schedule. `src: Core features, embargo rule 8`
- [ ] `C-CF-224` `constraint` The app leaves an embargoed record unchanged after a cancel attempt from a non-publisher session. `src: Core features, embargo rule 8`
- [ ] `C-CF-225` `contract` The app executes a write carrying an idempotency key once. `src: Core features, embargo rule 9`
- [ ] `C-CF-226` `contract` The app returns the original response to a repeat carrying the same key, the same body. `src: Core features, embargo rule 9`
- [ ] `C-CF-227` `contract` The app rejects a repeat carrying the same key, a different body, as a conflict. `src: Core features, embargo rule 9`
- [ ] `C-CF-228` `contract` The app honours an idempotency key for 24 hours. `src: Core features, embargo rule 9`
- [ ] `C-CF-229` `constraint` The app writes media bytes to the `minio` bucket, nowhere else. `src: Core features, Media rule 1`
- [ ] `C-CF-230` `literal` The app accepts bytes, a filename, an `alt_text` at `POST /api/content/records/{id}/media`. `src: Core features, Media rule 1`
- [ ] `C-CF-231` `literal` The app writes every object under the key scheme `media/{division_key}/{record_id}/{sha256_of_bytes}.{ext}`. `src: Core features, Media rule 2`
- [ ] `C-CF-232` `data` The app puts the checksum of the bytes in the object key. `src: Core features, Media rule 2`
- [ ] `C-CF-233` `constraint` The app refuses a media record carrying an empty `alt_text`. `src: Core features, Media rule 3`
- [ ] `C-CF-234` `data` The app carries a focal point on every media record. `src: Core features, Media rule 4`
- [ ] `C-CF-235` `data` The app carries an optional caption, an optional credit on a media record. `src: Core features, Media rule 4`
- [ ] `C-CF-236` `constraint` The app strips embedded metadata from an uploaded image on receipt. `src: Core features, Media rule 5`
- [ ] `C-CF-237` `constraint` The app refuses an upload whose inspected type sits outside the permitted list. `src: Core features, Media rule 5`
- [ ] `C-CF-238` `literal` The app returns bytes at `GET /api/media/{mediaId}` to a principal entitled to the owning record. `src: Core features, Media rule 6`
- [ ] `C-CF-239` `constraint` The app denies a media request from a principal not entitled to the owning record. `src: Core features, Media rule 6`
- [ ] `C-CF-240` `constraint` The app returns bytes at `GET /api/public/media/{mediaId}` only when the owning record is published. `src: Core features, Media rule 6`
- [ ] `C-CF-241` `constraint` The app refuses an anonymous request for the lead image of a draft release. `src: Core features, Media rule 6`
- [ ] `C-CF-242` `ui` The app renders a generated placeholder derived from the record identifier where a record needing an image has none. `src: Core features, Media rule 7`
- [ ] `C-CF-243` `constraint` The app renders the same placeholder for the same record on every render. `src: Core features, Media rule 7`
- [ ] `C-CF-244` `literal` The app serves the public routes `/`, `/trading/`, `/capital/`, `/maritime/`, `/kite-energy/`, `/who-we-are/`, `/news/`, `/news/{slug}/`, `/sustainability/`, `/contact/`, `/privacy-policy/`, `/terms-of-use/`, `/search`. `src: Core features, public site rule 1`
- [ ] `C-CF-245` `constraint` The app produces a public document once, at publication. `src: Core features, public site rule 2`
- [ ] `C-CF-246` `constraint` The app assembles nothing on a public route during a visitor's wait. `src: Core features, public site rule 2`
- [ ] `C-CF-247` `constraint` The app gives the public serving path no way to reach a draft, a revision, an embargoed body, the audit trail. `src: Core features, public site rule 2`
- [ ] `C-CF-248` `data` The app declares on every rendered document the record, the referenced records, the policy versions, the office set, the division the document depends on. `src: Core features, public site rule 3`
- [ ] `C-CF-249` `capability` The app refreshes every document carrying the footer when an office record is published. `src: Core features, public site rule 3`
- [ ] `C-CF-250` `capability` The app counts published releases across all divisions at `GET /api/public/counters`. `src: Core features, public site rule 4`
- [ ] `C-CF-251` `constraint` The app excludes the current filter from the counter value. `src: Core features, public site rule 4`
- [ ] `C-CF-252` `constraint` The app excludes the current page from the counter value. `src: Core features, public site rule 4`
- [ ] `C-CF-253` `ui` The app ships the last known counter value as a document's initial content. `src: Core features, public site rule 4`
- [ ] `C-CF-254` `literal` The app reads the counter `9` with nine seeded published releases. `src: Core features, public site rule 4`
- [ ] `C-CF-255` `literal` The app renders page two of the archive at the address `/news/?page=2`. `src: Core features, public site rule 5`
- [ ] `C-CF-256` `literal` The app filters the archive by division at the address `/news/?division=trading`. `src: Core features, public site rule 5`
- [ ] `C-CF-257` `literal` The app filters the archive by year at the address `/news/?year=2023`. `src: Core features, public site rule 5`
- [ ] `C-CF-258` `constraint` The app defaults the archive to unfiltered. `src: Core features, public site rule 5`
- [ ] `C-CF-259` `literal` The app renders at most `6` cards on one archive page. `src: Core features, public site rule 5`
- [ ] `C-CF-260` `constraint` The app offers no infinite scroll on the archive. `src: Core features, public site rule 5`
- [ ] `C-CF-261` `ui` The app renders an image, a date, a title on an archive card. `src: Core features, public site rule 6`
- [ ] `C-CF-262` `capability` The app truncates an over-long card title when the document is produced. `src: Core features, public site rule 6`
- [ ] `C-CF-263` `ui` The app exposes the full title as the accessible name of a truncated card title. `src: Core features, public site rule 6`
- [ ] `C-CF-264` `constraint` The app keeps a release slug unchanged once the release has been published. `src: Core features, public site rule 7`
- [ ] `C-CF-265` `capability` The app mints a redirect record when a published release is retitled. `src: Core features, public site rule 7`
- [ ] `C-CF-266` `capability` The app keeps the old address resolving after a redirect is minted. `src: Core features, public site rule 7`
- [ ] `C-CF-267` `capability` The app rewrites a new redirect to the final target when the target is itself a redirect. `src: Core features, public site rule 7`
- [ ] `C-CF-268` `constraint` The app rejects a redirect chain longer than one hop. `src: Core features, public site rule 7`
- [ ] `C-CF-269` `literal` The app unpublishes a record at `POST /api/workflow/records/{id}/unpublish`. `src: Core features, public site rule 8`
- [ ] `C-CF-270` `constraint` The app requires `publisher` to unpublish a record. `src: Core features, public site rule 8`
- [ ] `C-CF-271` `constraint` The app requires a reason on an unpublish. `src: Core features, public site rule 8`
- [ ] `C-CF-272` `ui` The app answers a withdrawn release's address as gone, rendering a withdrawal notice carrying the date. `src: Core features, public site rule 8`
- [ ] `C-CF-273` `constraint` The app keeps a withdrawn release's record rather than deleting the record. `src: Core features, public site rule 8`
- [ ] `C-CF-274` `constraint` The app excludes an archived release from the archive, from the search. `src: Core features, public site rule 8`
- [ ] `C-CF-275` `literal` The app carries two product families named `Oil`, `Metals` on `/trading/`. `src: Core features, public site rule 9`
- [ ] `C-CF-276` `data` The app carries twelve products each holding a name, a body, a family, an order. `src: Core features, public site rule 9`
- [ ] `C-CF-277` `capability` The app removes a family holding no published product from the selector. `src: Core features, public site rule 9`
- [ ] `C-CF-278` `capability` The app renders no selector when only one family remains. `src: Core features, public site rule 9`
- [ ] `C-CF-279` `capability` The app renders the three most recent releases tagged to a division on that division's route. `src: Core features, public site rule 10`
- [ ] `C-CF-280` `data` The app orders a division release strip by publication instant descending. `src: Core features, public site rule 10`
- [ ] `C-CF-281` `capability` The app renders nothing where a division has no tagged release. `src: Core features, public site rule 10`
- [ ] `C-CF-282` `constraint` The app never falls back to a group-wide release on a division strip. `src: Core features, public site rule 10`
- [ ] `C-CF-283` `constraint` The app refuses a move to `approved` on a `capital` record carrying no disclosure class. `src: Core features, public site rule 11`
- [ ] `C-CF-284` `capability` The app appends the disclaimer named by a `capital` record's class from the register. `src: Core features, public site rule 11`
- [ ] `C-CF-285` `data` The app carries a name, a class, a deadweight, a year built, a flag, an ownership, a status on a vessel record. `src: Core features, public site rule 12`
- [ ] `C-CF-286` `constraint` The app carries no position, no voyage, no cargo, no charterer, no commercial term on a vessel record. `src: Core features, public site rule 12`
- [ ] `C-CF-287` `data` The app carries a publication state on a person record independent of the page. `src: Core features, public site rule 13`
- [ ] `C-CF-288` `capability` The app removes an unpublished person from `/who-we-are/` without the page being edited. `src: Core features, public site rule 13`
- [ ] `C-CF-289` `data` The app carries a display-from instant, a display-until instant on a person record. `src: Core features, public site rule 13`
- [ ] `C-CF-290` `capability` The app omits the leadership block entirely where no person record is published. `src: Core features, public site rule 13`
- [ ] `C-CF-291` `capability` The app renders the externally published register entries on `/sustainability/` each carrying a version, an effective date. `src: Core features, public site rule 14`
- [ ] `C-CF-292` `capability` The app counts each disclosure document download per document per day. `src: Core features, public site rule 14`
- [ ] `C-CF-293` `constraint` The app retains no visitor identifier against a download count. `src: Core features, public site rule 14`
- [ ] `C-CF-294` `constraint` The app renders `/privacy-policy/` from a register entry rather than from a template. `src: Core features, public site rule 15`
- [ ] `C-CF-295` `constraint` The app renders `/terms-of-use/` from a register entry rather than from a template. `src: Core features, public site rule 15`
- [ ] `C-CF-296` `ui` The app renders a policy route carrying a title, a version, an effective date, a last-reviewed date. `src: Core features, public site rule 15`
- [ ] `C-CF-297` `ui` The app renders a policy route carrying an in-page contents list built from the entry's subheadings. `src: Core features, public site rule 15`
- [ ] `C-CF-298` `ui` The app renders a policy route carrying one paragraph summarising what changed since the previous version. `src: Core features, public site rule 15`
- [ ] `C-CF-299` `ui` The app renders a policy route carrying a list of previous versions, each linkable, each naming the period the version applied. `src: Core features, public site rule 15`
- [ ] `C-CF-300` `literal` The app carries three privacy notice variants for the jurisdictions `CH`, `AE-DIFC`, `SG`. `src: Core features, public site rule 16`
- [ ] `C-CF-301` `ui` The app offers a selector reaching all three privacy notice variants from the page. `src: Core features, public site rule 16`
- [ ] `C-CF-302` `capability` The app propagates a change to the shared parent body across all three privacy notice variants. `src: Core features, public site rule 16`
- [ ] `C-CF-303` `literal` The app searches published documents at `GET /api/public/search`. `src: Core features, public site rule 17`
- [ ] `C-CF-304` `constraint` The app searches only published releases, pages, products, people, externally published register entries. `src: Core features, public site rule 17`
- [ ] `C-CF-305` `literal` The app renders the public search at the address `/search?q=`. `src: Core features, public site rule 17`
- [ ] `C-CF-306` `capability` The app returns the no-query state for a query shorter than 2 characters. `src: Core features, public site rule 17`
- [ ] `C-CF-307` `constraint` The app shares no index between the public search, the console search. `src: Core features, public site rule 17`
- [ ] `C-CF-308` `capability` The app removes a withdrawn release from the public search within 30 seconds. `src: Core features, public site rule 18`
- [ ] `C-CF-309` `ui` The app renders seven authored surfaces: not found, gone, forbidden, server error, maintenance, rate limited, an unknown console route. `src: Core features, public site rule 19`
- [ ] `C-CF-310` `ui` The app renders the mark, the chrome, a way back on every authored error surface. `src: Core features, public site rule 19`
- [ ] `C-CF-311` `ui` The app displays the request identifier as selectable text on the server error surface. `src: Core features, public site rule 19`
- [ ] `C-CF-312` `ui` The app offers the five divisions, the release archive on the not-found surface. `src: Core features, public site rule 19`
- [ ] `C-CF-313` `constraint` The app loads no visual layer on any error surface. `src: Core features, public site rule 19`
- [ ] `C-CF-314` `ui` The app renders the not-found line exactly as the brief pins the line, naming a possible move, a possible mistype. `src: Core features, public site rule 19`
- [ ] `C-CF-315` `ui` The app renders the gone line exactly as the brief pins the line, naming the withdrawal date. `src: Core features, public site rule 19`
- [ ] `C-CF-316` `ui` The app renders the server error line exactly as the brief pins the line, quoting a reference. `src: Core features, public site rule 19`
- [ ] `C-CF-317` `ui` The app renders the maintenance line exactly as the brief pins the line, naming an expected return time. `src: Core features, public site rule 19`
- [ ] `C-CF-318` `ui` The app renders the rate-limited line exactly as the brief pins the line, naming a wait duration. `src: Core features, public site rule 19`
- [ ] `C-CF-319` `ui` The app removes a block holding no content rather than rendering the block empty. `src: Core features, public site rule 20`
- [ ] `C-CF-320` `ui` The app renders an authored line on an empty release archive, an empty console inbox, an empty search result. `src: Core features, public site rule 20`
- [ ] `C-CF-321` `capability` The app renders no home chapter holding no content record. `src: Core features, public site rule 20`
- [ ] `C-CF-322` `capability` The app renumbers the chapter numerals when a chapter is not rendered. `src: Core features, public site rule 20`
- [ ] `C-CF-323` `literal` The app accepts an enquiry at `POST /api/public/enquiries` from an anonymous visitor. `src: Core features, enquiry rule 1`
- [ ] `C-CF-324` `literal` The app requires a `subject_area` naming one of the five divisions or `general`. `src: Core features, enquiry rule 1`
- [ ] `C-CF-325` `constraint` The app requires a name between 2 characters, 120 characters after trimming. `src: Core features, enquiry rule 1`
- [ ] `C-CF-326` `constraint` The app bounds an organisation at 200 characters. `src: Core features, enquiry rule 1`
- [ ] `C-CF-327` `constraint` The app requires a country on an enquiry. `src: Core features, enquiry rule 1`
- [ ] `C-CF-328` `constraint` The app requires an email whose syntax is checked on an enquiry. `src: Core features, enquiry rule 1`
- [ ] `C-CF-329` `constraint` The app requires a message between 20 characters, 4000 characters. `src: Core features, enquiry rule 1`
- [ ] `C-CF-330` `constraint` The app requires an explicit consent choice that is not pre-selected. `src: Core features, enquiry rule 1`
- [ ] `C-CF-331` `data` The app records the version of the privacy notice in force with a consent choice. `src: Core features, enquiry rule 1`
- [ ] `C-CF-332` `constraint` The app declares the validation rules once on the server. `src: Core features, enquiry rule 2`
- [ ] `C-CF-333` `capability` The app runs the same rules in the browser for immediate feedback. `src: Core features, enquiry rule 2`
- [ ] `C-CF-334` `constraint` The app runs the rules again on the server at submission. `src: Core features, enquiry rule 2`
- [ ] `C-CF-335` `constraint` The app rejects a payload satisfying the browser rules, violating the server rules. `src: Core features, enquiry rule 2`
- [ ] `C-CF-336` `constraint` The app writes nothing on a rejected enquiry. `src: Core features, enquiry rule 2`
- [ ] `C-CF-337` `data` The app holds field messages as authored strings rather than generating the messages from the rules. `src: Core features, enquiry rule 3`
- [ ] `C-CF-338` `ui` The app checks a field blurred carrying a value. `src: Core features, enquiry rule 4`
- [ ] `C-CF-339` `ui` The app flags no required field blurred empty before a submit attempt. `src: Core features, enquiry rule 4`
- [ ] `C-CF-340` `ui` The app moves focus to the first invalid field on a submit attempt. `src: Core features, enquiry rule 4`
- [ ] `C-CF-341` `ui` The app announces the number of errors once on a submit attempt. `src: Core features, enquiry rule 4`
- [ ] `C-CF-342` `ui` The app clears a field error as the corrected value is typed after a failed submit. `src: Core features, enquiry rule 4`
- [ ] `C-CF-343` `ui` The app ignores a submit made during a pending submit. `src: Core features, enquiry rule 4`
- [ ] `C-CF-344` `constraint` The app mints a submission token per form render, single use, expiring in 30 minutes. `src: Core features, enquiry rule 5`
- [ ] `C-CF-345` `constraint` The app requires 3 seconds between the form being rendered, the form being submitted. `src: Core features, enquiry rule 5`
- [ ] `C-CF-346` `constraint` The app limits one origin to 5 enquiry submissions per hour. `src: Core features, enquiry rule 5`
- [ ] `C-CF-347` `constraint` The app presents no visual puzzle on the enquiry form. `src: Core features, enquiry rule 5`
- [ ] `C-CF-348` `literal` The app resolves a Swiss country or a European country to the jurisdiction `CH`, answered from Geneva. `src: Core features, enquiry rule 6`
- [ ] `C-CF-349` `literal` The app resolves a Gulf country to the jurisdiction `AE-DIFC`, answered from Dubai. `src: Core features, enquiry rule 6`
- [ ] `C-CF-350` `literal` The app resolves an Asian or Pacific country to the jurisdiction `SG`, answered from Singapore. `src: Core features, enquiry rule 6`
- [ ] `C-CF-351` `constraint` The app resolves any other country to `CH` as the most protective default. `src: Core features, enquiry rule 6`
- [ ] `C-CF-352` `constraint` The app never infers the jurisdiction from the connection. `src: Core features, enquiry rule 6`
- [ ] `C-CF-353` `capability` The app writes the enquiry record before answering the visitor. `src: Core features, enquiry rule 7`
- [ ] `C-CF-354` `constraint` The app routes the enquiry to the destination office after answering the visitor. `src: Core features, enquiry rule 7`
- [ ] `C-CF-355` `constraint` The app never surfaces a routing failure to the visitor. `src: Core features, enquiry rule 7`
- [ ] `C-CF-356` `ui` The app replaces the form in place with the confirmation without navigating away. `src: Core features, enquiry rule 8`
- [ ] `C-CF-357` `ui` The app carries a confirmation line, a public reference, a response window, the responding office on the confirmation. `src: Core features, enquiry rule 8`
- [ ] `C-CF-358` `ui` The app moves focus to the confirmation, announcing the confirmation. `src: Core features, enquiry rule 8`
- [ ] `C-CF-359` `ui` The app preserves every typed value on a rejected validation. `src: Core features, enquiry rule 9`
- [ ] `C-CF-360` `ui` The app re-renders the form carrying a fresh token, every typed value, on an expired token. `src: Core features, enquiry rule 9`
- [ ] `C-CF-361` `ui` The app states the retry window, preserving typed values, on a rate limit. `src: Core features, enquiry rule 9`
- [ ] `C-CF-362` `ui` The app offers the destination office address, the typed values as a copyable block, on a server error. `src: Core features, enquiry rule 9`
- [ ] `C-CF-363` `ui` The app asks a first-time visitor once about anything beyond the strictly necessary. `src: Core features, enquiry rule 10`
- [ ] `C-CF-364` `ui` The app makes refusing everything one action, exactly as prominent as accepting everything. `src: Core features, enquiry rule 10`
- [ ] `C-CF-365` `capability` The app stores the consent answer first-party, surviving a reload. `src: Core features, enquiry rule 10`
- [ ] `C-CF-366` `capability` The app stores the consent answer surviving a later visit. `src: Core features, enquiry rule 10`
- [ ] `C-CF-367` `ui` The app shows on the privacy route what was chosen, when, which notice version was in force. `src: Core features, enquiry rule 10`
- [ ] `C-CF-368` `capability` The app removes anything already stored when consent is withdrawn. `src: Core features, enquiry rule 10`
- [ ] `C-CF-369` `constraint` The app stores nothing beyond the strictly necessary before an affirmative choice. `src: Core features, enquiry rule 10`
- [ ] `C-CF-370` `capability` The app treats a browser preference not to be tracked as a refusal, prompting nobody. `src: Core features, enquiry rule 10`
- [ ] `C-CF-371` `constraint` The app offers no consent choice on an error surface, on a form being filled in, on a message being composed. `src: Core features, enquiry rule 10`
- [ ] `C-CF-372` `capability` The app measures document views, download counts, search terms on the server from the request path. `src: Core features, enquiry rule 11`
- [ ] `C-CF-373` `constraint` The app retains no visitor identifier in the measurement. `src: Core features, enquiry rule 11`
- [ ] `C-CF-374` `constraint` The app links no two requests in the measurement. `src: Core features, enquiry rule 11`
- [ ] `C-CF-375` `capability` The app records every mutation in the audit trail. `src: Core features, audit rule 1`
- [ ] `C-CF-376` `capability` The app records every authorization decision that denied. `src: Core features, audit rule 1`
- [ ] `C-CF-377` `capability` The app records every sign-in. `src: Core features, audit rule 1`
- [ ] `C-CF-378` `constraint` The app records a read only for an embargoed body, for the trail itself. `src: Core features, audit rule 1`
- [ ] `C-CF-379` `data` The app carries an instant, the acting principal on an audit entry. `src: Core features, audit rule 2`
- [ ] `C-CF-380` `data` The app carries the principal an action was performed on behalf of where the action was delegated. `src: Core features, audit rule 2`
- [ ] `C-CF-381` `data` The app carries an action from a closed vocabulary rather than a free string. `src: Core features, audit rule 2`
- [ ] `C-CF-382` `data` The app carries the resource type, the resource identifier, the division on an audit entry. `src: Core features, audit rule 2`
- [ ] `C-CF-383` `data` The app carries the hash before, the hash after on an audit entry. `src: Core features, audit rule 2`
- [ ] `C-CF-384` `constraint` The app carries no record content on an audit entry. `src: Core features, audit rule 2`
- [ ] `C-CF-385` `data` The app carries whether a decision allowed or denied, with a reason on a denial. `src: Core features, audit rule 2`
- [ ] `C-CF-386` `data` The app carries the request identifier on an audit entry. `src: Core features, audit rule 2`
- [ ] `C-CF-387` `data` The app carries the previous entry's hash together with the entry's own hash. `src: Core features, audit rule 2`
- [ ] `C-CF-388` `constraint` The app exposes no endpoint updating an audit entry. `src: Core features, audit rule 4`
- [ ] `C-CF-389` `constraint` The app exposes no endpoint deleting an audit entry. `src: Core features, audit rule 4`
- [ ] `C-CF-390` `literal` The app reads the audit trail at `GET /api/admin/audit`. `src: Core features, audit rule 4`
- [ ] `C-CF-391` `constraint` The app keeps every stored entry's previous-entry hash equal to the preceding entry's own hash. `src: Core features, audit rule 5`
- [ ] `C-CF-392` `capability` The app queries the trail by actor, by resource, by action, by division, by decision, by time range. `src: Core features, audit rule 6`
- [ ] `C-CF-393` `ui` The app renders an authored line restating the query where an audit query matches nothing. `src: Core features, audit rule 6`
- [ ] `C-CF-394` `capability` The app answers who approved a release, when, in one query. `src: Core features, audit rule 7`
- [ ] `C-CF-395` `capability` The app answers under whose authority a delegated approval was made, in one query. `src: Core features, audit rule 7`
- [ ] `C-CF-396` `capability` The app answers what exactly was approved through the after-hash. `src: Core features, audit rule 7`
- [ ] `C-CF-397` `capability` The app answers whether a record was edited after approval, in one query. `src: Core features, audit rule 7`
- [ ] `C-CF-398` `capability` The app answers who granted a principal publish rights, in one query. `src: Core features, audit rule 7`
- [ ] `C-CF-399` `capability` The app answers what the decision said when a request was denied. `src: Core features, audit rule 7`
- [ ] `C-CF-400` `constraint` The app offers no mass-deletion path. `src: Data model, mass deletion paragraph`
- [ ] `C-CF-401` `constraint` The app keeps an archived record recoverable indefinitely. `src: Data model, mass deletion paragraph`
- [ ] `C-CF-402` `capability` The app voids approvals, returns the record to `draft`, tells the approvers, when an author edits an approved release before publication. `src: Core features, Edge case 1`
- [ ] `C-CF-403` `capability` The app leaves approvals standing, recording the change, when an author edits only the image credit. `src: Core features, Edge case 2`
- [ ] `C-CF-404` `constraint` The app lets a principal holding both reviewer roles complete one stage, refusing the other on the same submission. `src: Core features, Edge case 3`
- [ ] `C-CF-405` `constraint` The app bars the author from approving after an approver delegates to the author. `src: Core features, Edge case 4`
- [ ] `C-CF-406` `constraint` The app accepts one of two simultaneous publications of one release, rejecting the other with a conflict. `src: Core features, Edge case 5`
- [ ] `C-CF-407` `constraint` The app records exactly one publication for two simultaneous publish attempts. `src: Core features, Edge case 5`
- [ ] `C-CF-408` `constraint` The app refuses a `market_sensitive` release leaving `compliance_review` without an embargo. `src: Core features, Edge case 8`
- [ ] `C-CF-409` `capability` The app completes a submission in flight under the chain version recorded on the submission. `src: Core features, Edge case 9`
- [ ] `C-CF-410` `capability` The app collapses a redirect chain when the second redirect is written. `src: Core features, Edge case 11`
- [ ] `C-CF-411` `constraint` The app blocks publication of a record referencing media not checked for malware. `src: Core features, Edge case 13`
- [ ] `C-CF-412` `capability` The app accepts an upload, holding the upload, where the malware check cannot be performed. `src: Core features, Edge case 13`
- [ ] `C-CF-413` `capability` The app preserves a draft for a successor when a principal is deactivated mid-edit. `src: Core features, Edge case 15`
- [ ] `C-CF-414` `ui` The app keeps the filter chips visible, offering a control that clears the chips, on an archive filtered to nothing. `src: Core features, Edge case 16`
- [ ] `C-CF-415` `capability` The app keeps the last known counter value in place where `GET /api/public/counters` is unavailable. `src: Core features, Edge case 18`
- [ ] `C-CF-416` `constraint` The app keeps every route fully functional where a visitor refuses every non-essential choice. `src: Core features, Edge case 19`
- [ ] `C-CF-417` `literal` The app rejects a media call as `dependency_unavailable` where the object store does not answer. `src: Core features, Edge case 20`
- [ ] `C-CF-418` `constraint` The app keeps every other surface working where the object store does not answer. `src: Core features, Edge case 20`
- [ ] `C-CF-419` `constraint` The app never relaxes authorization because a dependency failed. `src: Core features, Edge case 20`

## C-UF User flow

- [ ] `C-UF-01` `contract` The app serves `/` as the group home, anonymous. `src: User flow, route table`
- [ ] `C-UF-02` `contract` The app serves `/news/` as the release archive, anonymous. `src: User flow, route table`
- [ ] `C-UF-03` `contract` The app serves `/news/{slug}/` as one release, anonymous. `src: User flow, route table`
- [ ] `C-UF-04` `contract` The app serves `/contact/` carrying offices, a media contact, the enquiry form, anonymous. `src: User flow, route table`
- [ ] `C-UF-05` `contract` The app serves `/console/login` to an anonymous visitor. `src: User flow, route table`
- [ ] `C-UF-06` `contract` The app serves `/console` as the inbox to any principal holding a membership. `src: User flow, route table`
- [ ] `C-UF-07` `contract` The app serves `/console/divisions/{key}/releases` to a principal holding a membership on that division. `src: User flow, route table`
- [ ] `C-UF-08` `contract` The app serves `/console/releases/new` to a principal holding `author` on a division. `src: User flow, route table`
- [ ] `C-UF-09` `contract` The app serves `/console/releases/{id}` to a principal holding a membership on that division. `src: User flow, route table`
- [ ] `C-UF-10` `contract` The app serves `/console/admin/members` to a principal holding `group_admin`. `src: User flow, route table`
- [ ] `C-UF-11` `contract` The app serves `/console/admin/audit` to a principal holding `group_admin`. `src: User flow, route table`
- [ ] `C-UF-12` `contract` The app serves `/console/admin/exceptions` to a principal holding `group_admin`. `src: User flow, route table`
- [ ] `C-UF-13` `ui` The app renders the product's own not-found page at any other address. `src: User flow, route table`
- [ ] `C-UF-14` `capability` The app lands an anonymous request for a `/console` route on `/console/login`. `src: User flow, entry and redirects`
- [ ] `C-UF-15` `capability` The app continues to the address asked for after a successful sign in. `src: User flow, entry and redirects`
- [ ] `C-UF-16` `capability` The app lands a sign in carrying no pending address on `/console`. `src: User flow, entry and redirects`
- [ ] `C-UF-17` `capability` The app returns a sign out to `/console/login`, stopping the previous token working. `src: User flow, entry and redirects`
- [ ] `C-UF-18` `capability` The app returns an expired token mid-action to `/console/login`, resuming at the address the principal was on. `src: User flow, entry and redirects`
- [ ] `C-UF-19` `ui` The app renders no record table to a principal refused a division's console route. `src: User flow, entry and redirects`
- [ ] `C-UF-20` `ui` The app names the role a `/console/admin` route needs in the refusal shown to a principal holding no `group_admin`. `src: User flow, entry and redirects`
- [ ] `C-UF-21` `constraint` The app answers `/news/{slug}/` as not found where the release is embargoed, in draft, never created. `src: User flow, entry and redirects`
- [ ] `C-UF-22` `ui` The app answers `/news/{slug}/` as gone, rendering the withdrawal notice, where the release was withdrawn. `src: User flow, entry and redirects`
- [ ] `C-UF-23` `ui` The app lists `Calder Trading`, `Calder Capital` in the rail for `author@example.com`. `src: User flow, journey 1`
- [ ] `C-UF-24` `ui` The app moves the review rail to `legal_review` after a submit. `src: User flow, journey 1`
- [ ] `C-UF-25` `ui` The app removes a submitted record from the drafts queue. `src: User flow, journey 1`
- [ ] `C-UF-26` `ui` The app shows a submitted release in the first inbox queue of a legal reviewer. `src: User flow, journey 2`
- [ ] `C-UF-27` `ui` The app names the reason in the refusal shown to a reviewer attempting a second stage. `src: User flow, journey 2`
- [ ] `C-UF-28` `capability` The app moves a record to `approved` after a compliance approval. `src: User flow, journey 3`
- [ ] `C-UF-29` `capability` The app advances the header counter by one after an embargo instant passes. `src: User flow, journey 4`
- [ ] `C-UF-30` `capability` The app lists a newly published release first in the archive. `src: User flow, journey 4`
- [ ] `C-UF-31` `ui` The app renders the remaining three cards at `/news/?page=2` with nine published releases. `src: User flow, journey 9`
- [ ] `C-UF-32` `ui` The app names the Singapore office as the responder on a confirmation for an Asian country. `src: User flow, journey 10`
- [ ] `C-UF-33` `ui` The app keeps the consent answer after a reload of `/contact/`. `src: User flow, journey 10`
- [ ] `C-UF-34` `capability` The app resolves the old address of a retitled published release. `src: User flow, journey 11`
- [ ] `C-UF-35` `ui` The app names the filters that emptied a filtered archive. `src: User flow, states`
- [ ] `C-UF-36` `ui` The app renders six card skeletons at the real card dimensions on a loading archive. `src: User flow, states`
- [ ] `C-UF-37` `ui` The app renders a console table's header, the column set, before the rows arrive. `src: User flow, states`
- [ ] `C-UF-38` `ui` The app renders an error as a banner above content already loaded. `src: User flow, states`
- [ ] `C-UF-39` `ui` The app never renders a blank screen. `src: User flow, states`
- [ ] `C-UF-40` `ui` The app never renders a stack trace. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The app reads on the public site as a large, serious, multi-business group whose word carries authority. `src: UI/UX notes, north star`
- [ ] `C-UX-02` `ui` The app opens the public site as a journey rather than as a page. `src: UI/UX notes, north star`
- [ ] `C-UX-03` `ui` The app shows a console arrival what is waiting on the arriving principal, in what state. `src: UI/UX notes, north star`
- [ ] `C-UX-04` `ui` The app resolves one token set shared by the public site, the console. `src: UI/UX notes, north star`
- [ ] `C-UX-05` `ui` The app reads the public site as corporate-editorial: atmosphere permitted, the subject seen before the chrome. `src: UI/UX notes, register`
- [ ] `C-UX-06` `ui` The app reads the console as operational: quiet, dense but organised, built for scanning. `src: UI/UX notes, register`
- [ ] `C-UX-07` `ui` The app carries no journey, no split text, no drifting scroll inside the console. `src: UI/UX notes, register`
- [ ] `C-UX-08` `ui` The app favours space over dividers on the public site. `src: UI/UX notes, register`
- [ ] `C-UX-09` `ui` The app favours density over atmosphere in the console. `src: UI/UX notes, register`
- [ ] `C-UX-10` `ui` The app commits to a light mode, designing the light mode fully. `src: UI/UX notes, mode`
- [ ] `C-UX-11` `ui` The app opens in light mode where a dark mode also exists. `src: UI/UX notes, mode`
- [ ] `C-UX-12` `ui` The app draws the palette from one brand blue, a long pale ramp beneath the blue, almost nothing else. `src: UI/UX notes, palette thesis`
- [ ] `C-UX-13` `ui` The app draws the richness of a finished page from the imagery behind the type rather than from the palette. `src: UI/UX notes, palette thesis`
- [ ] `C-UX-14` `ui` The app adds no further accent beside the one bright colour. `src: UI/UX notes, palette thesis`
- [ ] `C-UX-15` `ui` The app renders the brand colour as a mid, soft cyan. `src: UI/UX notes, palette by role`
- [ ] `C-UX-16` `ui` The app uses the brand colour for the mark, for body copy on light ground, for every rule. `src: UI/UX notes, palette by role`
- [ ] `C-UX-17` `ui` The app renders the light ground as a near-white neutral. `src: UI/UX notes, palette by role`
- [ ] `C-UX-18` `ui` The app renders copy on dark ground in the same near-white neutral as the light ground. `src: UI/UX notes, palette by role`
- [ ] `C-UX-19` `ui` The app renders secondary copy on light ground as a light, muted cyan one step off the brand. `src: UI/UX notes, palette by role`
- [ ] `C-UX-20` `ui` The app renders a pointed-at brand-blue link in that same secondary colour. `src: UI/UX notes, palette by role`
- [ ] `C-UX-21` `ui` The app keeps the brighter ground-adjacent tint off type entirely. `src: UI/UX notes, palette by role`
- [ ] `C-UX-22` `ui` The app renders dividers on light ground as a near-white cool neutral. `src: UI/UX notes, palette by role`
- [ ] `C-UX-23` `ui` The app restricts the palest cool neutral to rules, to dividers. `src: UI/UX notes, palette by role`
- [ ] `C-UX-24` `ui` The app carries exactly one bright colour, a mid, vivid cyan, on the tertiary control border alone. `src: UI/UX notes, palette by role`
- [ ] `C-UX-25` `ui` The app uses a near-black neutral only as a chapter ground, never for type. `src: UI/UX notes, palette by role`
- [ ] `C-UX-26` `ui` The app carries an alpha with the colour rather than as a transparency on a parent. `src: UI/UX notes, alpha`
- [ ] `C-UX-27` `ui` The app carries six strengths of the light ground, each weaker than the one above. `src: UI/UX notes, alpha`
- [ ] `C-UX-28` `ui` The app carries three strengths of the brand for the focus ring fill, the card hover wash, the pressed state. `src: UI/UX notes, alpha`
- [ ] `C-UX-29` `ui` The app sets body copy in `CalderSans`. `src: UI/UX notes, type`
- [ ] `C-UX-30` `ui` The app sets the largest display size in `Josefin Sans`. `src: UI/UX notes, type`
- [ ] `C-UX-31` `ui` The app carries `CalderSans` in the regular cut, the heavy cut, roman, italic. `src: UI/UX notes, type`
- [ ] `C-UX-32` `ui` The app loads every face with a swap policy so copy reads before the faces arrive. `src: UI/UX notes, type`
- [ ] `C-UX-33` `literal` The app declares the fallback stack `"CalderSans", "Century Schoolbook L", "Futura", "Avenir Next", sans-serif`. `src: UI/UX notes, type`
- [ ] `C-UX-34` `ui` The app keeps a face swap from reflowing a headline by more than one line. `src: UI/UX notes, type`
- [ ] `C-UX-35` `ui` The app ships only the cuts actually used, subset to the characters the published content needs. `src: UI/UX notes, type`
- [ ] `C-UX-36` `ui` The app preloads the two faces used above the fold. `src: UI/UX notes, type`
- [ ] `C-UX-37` `ui` The app roughly doubles the largest heading across the primary switch, more than tripling the letter spacing. `src: UI/UX notes, type`
- [ ] `C-UX-38` `ui` The app lines figures up in a column wherever amounts stack. `src: UI/UX notes, type`
- [ ] `C-UX-39` `ui` The app renders four columns on a narrow screen, twenty four above the primary switch. `src: UI/UX notes, grid`
- [ ] `C-UX-40` `ui` The app roughly doubles the column gap across the primary switch. `src: UI/UX notes, grid`
- [ ] `C-UX-41` `ui` The app never collapses the column gap. `src: UI/UX notes, grid`
- [ ] `C-UX-42` `ui` The app places copy off centre on spans a twelve column field would force to halves, to thirds. `src: UI/UX notes, grid`
- [ ] `C-UX-43` `ui` The app carries one secondary arrangement of four equal parts for the pillar row. `src: UI/UX notes, grid`
- [ ] `C-UX-44` `ui` The app carries one secondary arrangement of two equal parts for paired copy blocks. `src: UI/UX notes, grid`
- [ ] `C-UX-45` `ui` The app keeps the page gutter narrow below the primary switch, several times wider above. `src: UI/UX notes, rhythm`
- [ ] `C-UX-46` `ui` The app widens the header gutter twice as the viewport grows. `src: UI/UX notes, rhythm`
- [ ] `C-UX-47` `ui` The app places full width chapter sections outside the padded container, copy sections inside. `src: UI/UX notes, rhythm`
- [ ] `C-UX-48` `ui` The app carries a large row gap between the five division blocks. `src: UI/UX notes, rhythm`
- [ ] `C-UX-49` `ui` The app carries a larger run above, below the sustainability chapter. `src: UI/UX notes, rhythm`
- [ ] `C-UX-50` `ui` The app renders every circular control as a true circle. `src: UI/UX notes, shape`
- [ ] `C-UX-51` `ui` The app renders the media tiles, the paginator controls at one small softness. `src: UI/UX notes, shape`
- [ ] `C-UX-52` `ui` The app renders everything else square. `src: UI/UX notes, shape`
- [ ] `C-UX-53` `ui` The app carries no intermediate corner radius. `src: UI/UX notes, shape`
- [ ] `C-UX-54` `ui` The app resolves every colour, size, spacing step, stacking level, radius from one named set at the document root. `src: UI/UX notes, token contract`
- [ ] `C-UX-55` `ui` The app writes no literal value inline anywhere. `src: UI/UX notes, token contract`
- [ ] `C-UX-56` `ui` The app carries three motion roles, no fourth. `src: UI/UX notes, motion`
- [ ] `C-UX-57` `ui` The app moves every hover lift, every control, every small positional change on the quick-to-leave, long-settle role. `src: UI/UX notes, motion`
- [ ] `C-UX-58` `ui` The app moves the pointer follower, the globe markers on the role whose start the eye never sees. `src: UI/UX notes, motion`
- [ ] `C-UX-59` `ui` The app reserves the hesitating role for the chapter-scale reveals. `src: UI/UX notes, motion`
- [ ] `C-UX-60` `ui` The app runs every colour change, every see-through change flat rather than shaped. `src: UI/UX notes, motion`
- [ ] `C-UX-61` `ui` The app runs everything that moves on a shaped ramp rather than flat. `src: UI/UX notes, motion`
- [ ] `C-UX-62` `ui` The app runs the shortest duration on a pointer-entry colour change, on the smallest transforms. `src: UI/UX notes, motion`
- [ ] `C-UX-63` `ui` The app runs the longest duration, roughly three times the default, on the chapter-scale reveals. `src: UI/UX notes, motion`
- [ ] `C-UX-64` `ui` The app uses no duration off the stated ladder to make one moment feel special. `src: UI/UX notes, motion`
- [ ] `C-UX-65` `ui` The app arrives a card from below, settling, staggered down the grid. `src: UI/UX notes, reveals`
- [ ] `C-UX-66` `ui` The app arrives a line of type from half a card's distance. `src: UI/UX notes, reveals`
- [ ] `C-UX-67` `ui` The app arrives a navigation label from a fractional offset preserved exactly rather than rounded. `src: UI/UX notes, reveals`
- [ ] `C-UX-68` `ui` The app arrives a loading indicator's container from above. `src: UI/UX notes, reveals`
- [ ] `C-UX-69` `ui` The app arrives individual mark paths from below so the mark assembles rather than fading. `src: UI/UX notes, reveals`
- [ ] `C-UX-70` `ui` The app splits a display headline so every character is independently transformable. `src: UI/UX notes, character machine`
- [ ] `C-UX-71` `ui` The app splits a body paragraph so every visual line is independently transformable. `src: UI/UX notes, character machine`
- [ ] `C-UX-72` `ui` The app runs the split only after the faces have loaded. `src: UI/UX notes, character machine`
- [ ] `C-UX-73` `ui` The app restores the original text when a split element goes away. `src: UI/UX notes, character machine`
- [ ] `C-UX-74` `ui` The app exposes the whole string as the accessible name of a split headline. `src: UI/UX notes, character machine`
- [ ] `C-UX-75` `ui` The app keeps a split headline selectable as one continuous string. `src: UI/UX notes, character machine`
- [ ] `C-UX-76` `ui` The app copies a split headline with no inserted whitespace. `src: UI/UX notes, character machine`
- [ ] `C-UX-77` `ui` The app leaves a split headline findable by the browser's own find. `src: UI/UX notes, character machine`
- [ ] `C-UX-78` `ui` The app runs no split inside the console. `src: UI/UX notes, character machine`
- [ ] `C-UX-79` `ui` The app holds a primary bar label back at rest, bringing the label to full strength when pointed at. `src: UI/UX notes, hover`
- [ ] `C-UX-80` `ui` The app grows a release card's underline sideways from nothing to full width from a fixed origin. `src: UI/UX notes, hover`
- [ ] `C-UX-81` `ui` The app slides a read-more control's label downward out of sight, filling a replacement in behind. `src: UI/UX notes, hover`
- [ ] `C-UX-82` `ui` The app moves a text link together with both of the link's decorations from the brand colour to the hover colour. `src: UI/UX notes, hover`
- [ ] `C-UX-83` `ui` The app never leaves hover as the only signal on a link. `src: UI/UX notes, hover`
- [ ] `C-UX-84` `ui` The app runs the home route roughly twenty screens tall at a desktop height, most carrying no copy. `src: UI/UX notes, scroll instrument`
- [ ] `C-UX-85` `ui` The app keeps moving for a moment after the reader stops pushing. `src: UI/UX notes, scroll instrument`
- [ ] `C-UX-86` `ui` The app reports a fractional scroll position every frame. `src: UI/UX notes, scroll instrument`
- [ ] `C-UX-87` `ui` The app exposes whether the scroll is in motion or settled as state on the document root. `src: UI/UX notes, scroll instrument`
- [ ] `C-UX-88` `ui` The app stops, restarts the scroll driver without losing position. `src: UI/UX notes, scroll instrument`
- [ ] `C-UX-89` `ui` The app makes every visual change on the journey a function of the fractional position alone. `src: UI/UX notes, scroll instrument`
- [ ] `C-UX-90` `ui` The app runs the journey exactly backwards when the reader scrolls backwards. `src: UI/UX notes, scroll instrument`
- [ ] `C-UX-91` `ui` The app strips the journey of smoothing, of inertia, under a reduced-motion preference. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-92` `ui` The app runs no character split, no line split, under a reduced-motion preference. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-93` `ui` The app resolves every named reveal immediately at the resting position under a reduced-motion preference. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-94` `ui` The app replaces the turning loading indicator with a static one carrying a text label under a reduced-motion preference. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-95` `ui` The app cuts route transitions with no cross-fade, no slide, under a reduced-motion preference. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-96` `ui` The app renders no pointer follower under a reduced-motion preference. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-97` `ui` The app leads each public chapter, each console surface with exactly one primary action. `src: UI/UX notes, primary action`
- [ ] `C-UX-98` `ui` The app makes the primary action the only thing on a view carrying the strongest contrast. `src: UI/UX notes, primary action`
- [ ] `C-UX-99` `ui` The app renders the primary action visually distinct from every secondary one. `src: UI/UX notes, primary action`
- [ ] `C-UX-100` `ui` The app carries resting, pointed-at, pressed, focused, unavailable states on every action style. `src: UI/UX notes, primary action`
- [ ] `C-UX-101` `ui` The app never signals unavailable by colour alone. `src: UI/UX notes, primary action`
- [ ] `C-UX-102` `ui` The app loads no visual layer, no scroll driver, no split, no pointer follower in the console. `src: UI/UX notes, console`
- [ ] `C-UX-103` `ui` The app renders a console rail carrying the division switcher, then the sections the principal may see. `src: UI/UX notes, console`
- [ ] `C-UX-104` `ui` The app filters the console rail sections rather than showing a section then refusing the section. `src: UI/UX notes, console`
- [ ] `C-UX-105` `ui` The app renders a console top bar carrying the current division, a search field, the pending-work count, the principal menu. `src: UI/UX notes, console`
- [ ] `C-UX-106` `ui` The app renders the console main region table first, dense enough for a full queue to fit one screen. `src: UI/UX notes, console`
- [ ] `C-UX-107` `ui` The app renders a contextual right panel carrying the workflow state, the decision history, the pending action, the assigned reviewers on a record. `src: UI/UX notes, console`
- [ ] `C-UX-108` `ui` The app renders a record preview from the actual public template against the draft. `src: UI/UX notes, console`
- [ ] `C-UX-109` `ui` The app switches the record preview between the three widths. `src: UI/UX notes, console`
- [ ] `C-UX-110` `ui` The app carries one control on every record surface opening that record's own trail in place. `src: UI/UX notes, console`
- [ ] `C-UX-111` `ui` The app renders a confirmation as a dismissible transient message at the lower right. `src: UI/UX notes, console`
- [ ] `C-UX-112` `ui` The app never leaves the only copy of anything in a transient message. `src: UI/UX notes, console`
- [ ] `C-UX-113` `constraint` The app locks no record in the console. `src: UI/UX notes, console`
- [ ] `C-UX-114` `capability` The app accepts two edits to different fields of one release from two principals. `src: UI/UX notes, console`
- [ ] `C-UX-115` `ui` The app moves nothing on screen during an approver's reading of a submission. `src: UI/UX notes, console`
- [ ] `C-UX-116` `ui` The app changes the grid, the gap, the gutter, the display heading, the mark, the primary bar, the scroll cue copy across the primary switch. `src: UI/UX notes, responsive`
- [ ] `C-UX-117` `ui` The app shows the pointer follower, every hover behaviour only above the primary switch. `src: UI/UX notes, responsive`
- [ ] `C-UX-118` `ui` The app holds the arrangement at every width between the named tiers. `src: UI/UX notes, responsive`
- [ ] `C-UX-119` `ui` The app authors the mobile home composition rather than deriving the composition from the desktop one. `src: UI/UX notes, responsive`
- [ ] `C-UX-120` `ui` The app expresses a chapter existing at one width, absent at another. `src: UI/UX notes, responsive`
- [ ] `C-UX-121` `ui` The app expresses chapters whose order differs by width. `src: UI/UX notes, responsive`
- [ ] `C-UX-122` `ui` The app sizes a full-height chapter against the smallest viewport height rather than the dynamic one. `src: UI/UX notes, responsive`
- [ ] `C-UX-123` `ui` The app renders the opening chapter less than full height on a short viewport. `src: UI/UX notes, responsive`
- [ ] `C-UX-124` `ui` The app places the scroll cue inline rather than pinned to the foot on a short viewport. `src: UI/UX notes, responsive`
- [ ] `C-UX-125` `ui` The app scrolls the overlay menu rather than fitting the menu on a short viewport. `src: UI/UX notes, responsive`
- [ ] `C-UX-126` `ui` The app never scrolls the document sideways. `src: UI/UX notes, responsive`
- [ ] `C-UX-127` `ui` The app scrolls genuinely wide content inside the content's own container carrying a visible affordance. `src: UI/UX notes, responsive`
- [ ] `C-UX-128` `ui` The app sizes any control on a coarse pointer at least 44px by 44px. `src: UI/UX notes, responsive`
- [ ] `C-UX-129` `ui` The app gives every hover affordance a non-hover equivalent. `src: UI/UX notes, responsive`
- [ ] `C-UX-130` `ui` The app builds the console for 1024px upward. `src: UI/UX notes, responsive`
- [ ] `C-UX-131` `ui` The app offers a dedicated narrow surface where an approver reads a submission, deciding, from a phone. `src: UI/UX notes, responsive`
- [ ] `C-UX-132` `ui` The app meets WCAG 2.1 level AA across the public site, the console. `src: UI/UX notes, accessibility`
- [ ] `C-UX-133` `ui` The app holds body text at least 4.5 to 1 against the text's background in every state. `src: UI/UX notes, accessibility`
- [ ] `C-UX-134` `ui` The app holds large text at least 3 to 1 against the text's background. `src: UI/UX notes, accessibility`
- [ ] `C-UX-135` `ui` The app carries a scrim on each chapter sufficient to hold the ratio against that chapter's brightest state. `src: UI/UX notes, accessibility`
- [ ] `C-UX-136` `ui` The app renders secondary copy on light ground in the hover colour at 16px upward, or the brand colour at any size. `src: UI/UX notes, accessibility`
- [ ] `C-UX-137` `ui` The app removes every visual layer from the accessibility tree. `src: UI/UX notes, accessibility`
- [ ] `C-UX-138` `ui` The app renders any label appearing inside a visual layer as real document text too. `src: UI/UX notes, accessibility`
- [ ] `C-UX-139` `ui` The app flashes nothing more than three times a second anywhere. `src: UI/UX notes, accessibility`
- [ ] `C-UX-140` `ui` The app moves the scroll driver on page up, page down, home, end, space, the arrow keys. `src: UI/UX notes, accessibility`
- [ ] `C-UX-141` `ui` The app scrolls a focused out-of-view element into view through the driver. `src: UI/UX notes, accessibility`
- [ ] `C-UX-142` `ui` The app never prevents or redirects a scroll gesture. `src: UI/UX notes, accessibility`
- [ ] `C-UX-143` `ui` The app places a skip link first in the document, visible on focus. `src: UI/UX notes, accessibility`
- [ ] `C-UX-144` `ui` The app makes each chapter numeral a control travelling to that chapter. `src: UI/UX notes, accessibility`
- [ ] `C-UX-145` `ui` The app exposes the current chapter as state. `src: UI/UX notes, accessibility`
- [ ] `C-UX-146` `ui` The app names a circular arrow button for the button's destination rather than for the arrow. `src: UI/UX notes, accessibility`
- [ ] `C-UX-147` `ui` The app names a chapter numeral for the chapter rather than for the number. `src: UI/UX notes, accessibility`
- [ ] `C-UX-148` `ui` The app names the release counter for what the counter counts. `src: UI/UX notes, accessibility`
- [ ] `C-UX-149` `ui` The app exposes whether the menu trigger is expanded, changing the exposed value. `src: UI/UX notes, accessibility`
- [ ] `C-UX-150` `ui` The app names the mark with the group name as the only non-decorative icon. `src: UI/UX notes, accessibility`
- [ ] `C-UX-151` `ui` The app moves between the sustainability pillar tabs with the arrow keys. `src: UI/UX notes, accessibility`
- [ ] `C-UX-152` `ui` The app places only the current pillar tab in the tab order. `src: UI/UX notes, accessibility`
- [ ] `C-UX-153` `ui` The app labels each pillar panel by the panel's tab. `src: UI/UX notes, accessibility`
- [ ] `C-UX-154` `ui` The app reflects the current pillar in the address. `src: UI/UX notes, accessibility`
- [ ] `C-UX-155` `ui` The app operates the console entirely from the keyboard. `src: UI/UX notes, accessibility`
- [ ] `C-UX-156` `ui` The app keeps focus visible at all times, never suppressed. `src: UI/UX notes, accessibility`
- [ ] `C-UX-157` `ui` The app matches focus order to visual order in all three console regions. `src: UI/UX notes, accessibility`
- [ ] `C-UX-158` `ui` The app carries one polite live region for save state, one assertive for errors. `src: UI/UX notes, accessibility`
- [ ] `C-UX-159` `ui` The app associates table headers, announcing a sortable column's state. `src: UI/UX notes, accessibility`
- [ ] `C-UX-160` `ui` The app traps focus in a dialog, closing on escape, returning focus to the opening control. `src: UI/UX notes, accessibility`
- [ ] `C-UX-161` `ui` The app warns before a session expires, offering an extend control. `src: UI/UX notes, accessibility`
- [ ] `C-UX-162` `ui` The app carries an icon, a label, or a shape on every status signal rather than relying on hue alone. `src: UI/UX notes, accessibility`
- [ ] `C-UX-163` `ui` The app carries a visible persistent label on every control. `src: UI/UX notes, accessibility`
- [ ] `C-UX-164` `ui` The app reflows to a single column with nothing clipped, no sideways scroll, at 200 per cent text scale. `src: UI/UX notes, accessibility`
- [ ] `C-UX-165` `ui` The app writes sentence case except for proper nouns, for the uppercase navigation labels. `src: UI/UX notes, copy`
- [ ] `C-UX-166` `ui` The app writes no exclamation mark in an interface string. `src: UI/UX notes, copy`
- [ ] `C-UX-167` `ui` The app writes no first-person plural in an interface string. `src: UI/UX notes, copy`
- [ ] `C-UX-168` `ui` The app writes actions as imperative verbs. `src: UI/UX notes, copy`
- [ ] `C-UX-169` `ui` The app names the missing thing in every empty string rather than apologising. `src: UI/UX notes, copy`
- [ ] `C-UX-170` `literal` The app renders the exact strings `Calder Group`, `Calder Trading`, `Calder Capital`, `Calder Maritime`, `Kite Energy`. `src: UI/UX notes, copy`
- [ ] `C-UX-171` `literal` The app renders the exact strings `News`, `Menu`, `Contact`, `ESG`, `Privacy policy`, `Terms of use`. `src: UI/UX notes, copy`
- [ ] `C-UX-172` `literal` The app renders the exact strings `Scroll down to discover`, `Swipe down`, `Who we are`. `src: UI/UX notes, copy`
- [ ] `C-UX-173` `literal` The app renders the exact strings `Explore Our`, `Products:`, `Oil`, `Metals`. `src: UI/UX notes, copy`
- [ ] `C-UX-174` `literal` The app renders the exact strings `Environmental`, `Social`, `Governance`, `Contact us`, `First`, `Last`. `src: UI/UX notes, copy`
- [ ] `C-UX-175` `literal` The app renders the exact strings `Geneva, Switzerland`, `Dubai, UAE`, `Singapore`. `src: UI/UX notes, copy`
- [ ] `C-UX-176` `ui` The app avoids a page dominated by one hue family carrying no second signal. `src: UI/UX notes, what it must not look like`
- [ ] `C-UX-177` `ui` The app avoids decoration standing in for content. `src: UI/UX notes, what it must not look like`
- [ ] `C-UX-178` `ui` The app avoids a marketing composition where the console belongs. `src: UI/UX notes, what it must not look like`
- [ ] `C-UX-179` `ui` The app avoids a chapter rendered as a heading over a void. `src: UI/UX notes, what it must not look like`
- [ ] `C-UX-180` `ui` The app avoids an error surface making somebody wait for scenery. `src: UI/UX notes, what it must not look like`

## C-FE Front-end specification

- [ ] `C-FE-01` `literal` The app sets `fs-h1` at `2.5rem`, then `5rem` above the switch, over a line height of `1.2`. `src: Front-end specification, type scale`
- [ ] `C-FE-02` `literal` The app tracks `fs-h1` at `.25rem`, then `.5rem` above the switch. `src: Front-end specification, type scale`
- [ ] `C-FE-03` `literal` The app sets `fs-h2` at `2.25rem`, then `3.125rem`, over a line height of `1.4`. `src: Front-end specification, type scale`
- [ ] `C-FE-04` `literal` The app sets `fs-h3` at `1.75rem`, then `2.5rem`, over a line height of `1.4`. `src: Front-end specification, type scale`
- [ ] `C-FE-05` `literal` The app sets `fs-h4` at `.75rem`, then `1.25rem`, over a line height of `1.4`. `src: Front-end specification, type scale`
- [ ] `C-FE-06` `literal` The app sets `fs-h5` at `1rem` over a line height of `1.6`. `src: Front-end specification, type scale`
- [ ] `C-FE-07` `literal` The app sets `fs-s1` at `1.25rem`, then `1.5rem`, over a line height of `1.6`. `src: Front-end specification, type scale`
- [ ] `C-FE-08` `literal` The app sets `fs-s2` at `1.25rem` over a line height of `1.6`. `src: Front-end specification, type scale`
- [ ] `C-FE-09` `literal` The app sets `fs-body` at `1rem` over a line height of `1.6`, tracked at `.08rem`. `src: Front-end specification, type scale`
- [ ] `C-FE-10` `literal` The app sets `fs-body-s` at `.75rem` over a line height of `1.6`, tracked at `.06rem`. `src: Front-end specification, type scale`
- [ ] `C-FE-11` `literal` The app sets `fs-cta` at `.75rem` over a line height of `1.2`, tracked at `.025rem`. `src: Front-end specification, type scale`
- [ ] `C-FE-12` `literal` The app sets `fs-cta-s` at `.75rem` over a line height of `1.2`, tracked at `.03rem`. `src: Front-end specification, type scale`
- [ ] `C-FE-13` `literal` The app sets `fs-label` at `.75rem` in the heavy cut over a line height of `1.4`. `src: Front-end specification, type scale`
- [ ] `C-FE-14` `literal` The app sets `fs-numerals` at `.5rem` in the heavy cut over a line height of `1.6`. `src: Front-end specification, type scale`
- [ ] `C-FE-15` `literal` The app sets `fs-label-lg` at `14px` in the heavy cut over a line height of `16.8px`. `src: Front-end specification, type scale`
- [ ] `C-FE-16` `literal` The app sets `fs-h1-index` at `62px` in the light display cut. `src: Front-end specification, type scale`
- [ ] `C-FE-17` `ui` The app carries six stacking levels: the visual layer behind everything, in-flow chapter overlays, the chapter index, the header, the overlay menu, the pointer follower. `src: Front-end specification, stacking`
- [ ] `C-FE-18` `ui` The app draws every icon as inline geometry. `src: Front-end specification, iconography`
- [ ] `C-FE-19` `constraint` The app ships no icon font, no icon image, no icon sprite. `src: Front-end specification, iconography`
- [ ] `C-FE-20` `ui` The app inherits an icon's colour from the surrounding copy except on the mark, on the pillar set. `src: Front-end specification, iconography`
- [ ] `C-FE-21` `ui` The app marks an icon inside an interactive control decorative, naming the control. `src: Front-end specification, iconography`
- [ ] `C-FE-22` `ui` The app builds two mark lockups: a wide horizontal drawing, a taller stacked drawing. `src: Front-end specification, iconography`
- [ ] `C-FE-23` `ui` The app strokes the stacked lockup's emblem rather than filling the emblem. `src: Front-end specification, iconography`
- [ ] `C-FE-24` `ui` The app draws the emblem as a stylised tree of dots above the wordmark. `src: Front-end specification, iconography`
- [ ] `C-FE-25` `ui` The app moves the emblem's hairline vertical trunk, the emblem's pivot dot independently. `src: Front-end specification, iconography`
- [ ] `C-FE-26` `ui` The app draws four directional icons: a right arrow, a filled up arrow, a downward scroll cue, a small chevron. `src: Front-end specification, iconography`
- [ ] `C-FE-27` `ui` The app draws the three arrows at three different terminal strokes, each tuned to the arrow's size. `src: Front-end specification, iconography`
- [ ] `C-FE-28` `ui` The app draws the loading indicator as two arcs of one circle laid end to end, each stroked with the arc's own gradient. `src: Front-end specification, iconography`
- [ ] `C-FE-29` `constraint` The app builds the loading indicator from two gradient arcs rather than from one dashed circle. `src: Front-end specification, iconography`
- [ ] `C-FE-30` `ui` The app draws four pillar marks inside circular outlines over the slate chapter. `src: Front-end specification, iconography`
- [ ] `C-FE-31` `ui` The app draws the carbon pillar's small node twice at identical coordinates so one of the two moves independently. `src: Front-end specification, iconography`
- [ ] `C-FE-32` `constraint` The app replaces no icon by a font glyph. `src: Front-end specification, iconography`
- [ ] `C-FE-33` `ui` The app keeps the header, the overlay menu, the pointer follower, the footer present on every route without rebuilding them. `src: Front-end specification, global chrome`
- [ ] `C-FE-34` `ui` The app gives the header no background at all. `src: Front-end specification, global chrome`
- [ ] `C-FE-35` `ui` The app inverts the header copy colour between the brand colour, the light ground, as the chapter ground changes. `src: Front-end specification, global chrome`
- [ ] `C-FE-36` `ui` The app fades the header rather than sliding the header, on the flat ramp. `src: Front-end specification, global chrome`
- [ ] `C-FE-37` `ui` The app renders five uppercase division labels at the small call-to-action tracking in the division bar. `src: Front-end specification, global chrome`
- [ ] `C-FE-38` `ui` The app renders the current division at full strength under a hairline rule, siblings held back. `src: Front-end specification, global chrome`
- [ ] `C-FE-39` `ui` The app restores a held-back sibling label on pointer entry. `src: Front-end specification, global chrome`
- [ ] `C-FE-40` `ui` The app renders the release counter as a numeral in a circular brand-coloured fill. `src: Front-end specification, global chrome`
- [ ] `C-FE-41` `ui` The app measures the rule under the current label from the label's own width. `src: Front-end specification, global chrome`
- [ ] `C-FE-42` `ui` The app closes the overlay menu by default, occupying the full screen when open. `src: Front-end specification, global chrome`
- [ ] `C-FE-43` `ui` The app carries the five division names, then `Contact`, `ESG`, `Privacy policy`, `Terms of use` in the overlay menu. `src: Front-end specification, global chrome`
- [ ] `C-FE-44` `ui` The app locks the document scroll without shifting the layout when the overlay menu opens. `src: Front-end specification, global chrome`
- [ ] `C-FE-45` `ui` The app traps focus inside the overlay menu. `src: Front-end specification, global chrome`
- [ ] `C-FE-46` `ui` The app returns focus to the trigger when the overlay menu closes. `src: Front-end specification, global chrome`
- [ ] `C-FE-47` `ui` The app closes the overlay menu on the escape key, on a route change. `src: Front-end specification, global chrome`
- [ ] `C-FE-48` `ui` The app builds the pointer follower from three nested pieces. `src: Front-end specification, global chrome`
- [ ] `C-FE-49` `ui` The app trails the outer ring behind the pointer with a per-frame interpolation. `src: Front-end specification, global chrome`
- [ ] `C-FE-50` `ui` The app tracks the middle dot to the pointer with no lag. `src: Front-end specification, global chrome`
- [ ] `C-FE-51` `ui` The app collapses the follower's dot by scaling to nothing over an interactive target, springing back from the same point. `src: Front-end specification, global chrome`
- [ ] `C-FE-52` `ui` The app suppresses the pointer follower entirely where there is no fine pointer with hover. `src: Front-end specification, global chrome`
- [ ] `C-FE-53` `ui` The app renders four footer columns on a wide screen: a link column, then one column per office. `src: Front-end specification, global chrome`
- [ ] `C-FE-54` `ui` The app renders the horizontal mark, the copyright line right aligned beneath a full-width rule. `src: Front-end specification, global chrome`
- [ ] `C-FE-55` `ui` The app sets office headings at `fs-s2`, address lines at `fs-body-s`. `src: Front-end specification, global chrome`
- [ ] `C-FE-56` `constraint` The app writes no trailing character after a telephone link, after a mail link. `src: Front-end specification, global chrome`
- [ ] `C-FE-57` `constraint` The app loads no visual layer on a route declaring none. `src: Front-end specification, global chrome`
- [ ] `C-FE-58` `ui` The app opens the journey at the summit above cloud, the mark centred left, the scroll cue at the foot. `src: Front-end specification, journey`
- [ ] `C-FE-59` `ui` The app renders no headline in the opening chapter. `src: Front-end specification, journey`
- [ ] `C-FE-60` `ui` The app descends into cloud with the opening statement setting line by line. `src: Front-end specification, journey`
- [ ] `C-FE-61` `ui` The app renders the first two divisions inside cloud, each with a numbered diamond, a link. `src: Front-end specification, journey`
- [ ] `C-FE-62` `ui` The app renders a dark sea carrying a vessel under way at the journey's low point. `src: Front-end specification, journey`
- [ ] `C-FE-63` `ui` The app renders a lit globe at the journey's midpoint carrying a marker, a country label. `src: Front-end specification, journey`
- [ ] `C-FE-64` `ui` The app renders the slate ground, the sustainability heading, three pillar tabs, four pillar marks three quarters down. `src: Front-end specification, journey`
- [ ] `C-FE-65` `ui` The app ends the journey at the footer on the light ground with the visual layer gone. `src: Front-end specification, journey`
- [ ] `C-FE-66` `ui` The app sets the chapter one headline exactly as the brief pins the headline, describing the group in one sentence. `src: Front-end specification, journey`
- [ ] `C-FE-67` `ui` The app preserves the art-directed line breaks of the opening paragraph, one element per visual line. `src: Front-end specification, journey`
- [ ] `C-FE-68` `ui` The app sets the chapter two heading exactly as the brief pins the heading. `src: Front-end specification, journey`
- [ ] `C-FE-69` `literal` The app sets the trading proposition `Operating Efficiently, Leading with Innovation.` `src: Front-end specification, journey`
- [ ] `C-FE-70` `ui` The app sets the capital proposition exactly as the brief pins the proposition. `src: Front-end specification, journey`
- [ ] `C-FE-71` `literal` The app sets the venture proposition `Energy investments`. `src: Front-end specification, journey`
- [ ] `C-FE-72` `ui` The app renders a numeral in a square outline rotated exactly forty five degrees on each division block. `src: Front-end specification, journey`
- [ ] `C-FE-73` `ui` The app composes the diamond rotation with a half-unit translation keeping the outline on the pixel grid. `src: Front-end specification, journey`
- [ ] `C-FE-74` `ui` The app renders `Calder Group` as block one, linking nowhere. `src: Front-end specification, journey`
- [ ] `C-FE-75` `ui` The app renders a globe marker's label only when the marker is on the visible hemisphere. `src: Front-end specification, journey`
- [ ] `C-FE-76` `ui` The app positions globe markers in document space, moving them to follow the projected position each frame. `src: Front-end specification, journey`
- [ ] `C-FE-77` `ui` The app smooths marker movement on position, on colour together. `src: Front-end specification, journey`
- [ ] `C-FE-78` `data` The app draws globe markers from the office records, each carrying a latitude, a longitude, a label. `src: Front-end specification, journey`
- [ ] `C-FE-79` `literal` The app sets the sustainability heading `Delivering sustainable energy solutions`. `src: Front-end specification, journey`
- [ ] `C-FE-80` `ui` The app truncates the strategy paragraph at six lines with a trailing ellipsis, a circular chevron control beneath. `src: Front-end specification, journey`
- [ ] `C-FE-81` `ui` The app expands the truncated strategy paragraph by height. `src: Front-end specification, journey`
- [ ] `C-FE-82` `ui` The app renders the current pillar tab in the light ground under a hairline rule, the others in the palest cool neutral under a weaker rule. `src: Front-end specification, journey`
- [ ] `C-FE-83` `ui` The app sets the people statement exactly as the brief pins the statement. `src: Front-end specification, journey`
- [ ] `C-FE-84` `literal` The app sets the corporate responsibility heading `Our pledge to corporate social responsibility`. `src: Front-end specification, journey`
- [ ] `C-FE-85` `capability` The app makes each of the four anchors a real, linkable, shareable address. `src: Front-end specification, journey`
- [ ] `C-FE-86` `literal` The app carries the anchors `#WhoWeAre`, `#WhatWeDo`, `#GlobalConnectivity`, `#Sustainability`. `src: Front-end specification, journey`
- [ ] `C-FE-87` `capability` The app renders a cold load at an anchor with the journey already at that chapter. `src: Front-end specification, journey`
- [ ] `C-FE-88` `constraint` The app animates no travel from the start on a cold load at an anchor. `src: Front-end specification, journey`
- [ ] `C-FE-89` `capability` The app leaves the driver settled after a cold load at an anchor. `src: Front-end specification, journey`
- [ ] `C-FE-90` `capability` The app animates travel to an anchor reached from a link inside the document. `src: Front-end specification, journey`
- [ ] `C-FE-91` `literal` The app links `/#Sustainability` from the footer of every route. `src: Front-end specification, journey`
- [ ] `C-FE-92` `literal` The app renders the scroll cue `Scroll down to discover` above the primary switch. `src: Front-end specification, scroll cue`
- [ ] `C-FE-93` `literal` The app renders the scroll cue `Swipe down` below the primary switch. `src: Front-end specification, scroll cue`
- [ ] `C-FE-94` `ui` The app fades the scroll cue out on the first scroll input, never returning the cue. `src: Front-end specification, scroll cue`
- [ ] `C-FE-95` `ui` The app drifts the scroll cue label on a positional scrub above the switch, a see-through scrub below. `src: Front-end specification, scroll cue`
- [ ] `C-FE-96` `ui` The app rests the scroll-to-top control invisible, showing the control after the first screen. `src: Front-end specification, scroll cue`
- [ ] `C-FE-97` `ui` The app returns the journey to the start on the scroll-to-top control. `src: Front-end specification, scroll cue`
- [ ] `C-FE-98` `ui` The app locks the scroll by stopping the driver rather than by setting an overflow on the document. `src: Front-end specification, scroll lock`
- [ ] `C-FE-99` `constraint` The app jumps by no fractional remainder when a scroll lock is released. `src: Front-end specification, scroll lock`
- [ ] `C-FE-100` `ui` The app uses one lock mechanism for the overlay menu, for a dialog, for the loading state. `src: Front-end specification, scroll lock`
- [ ] `C-FE-101` `ui` The app loads in four phases, the document readable at the end of the second. `src: Front-end specification, loading`
- [ ] `C-FE-102` `ui` The app shows the loading indicator over the first two phases only. `src: Front-end specification, loading`
- [ ] `C-FE-103` `capability` The app carries a complete authored variant with no visual layer on every route carrying one. `src: Front-end specification, no-layer variant`
- [ ] `C-FE-104` `constraint` The app carries the same copy, headings, links, chapter order in the no-layer variant. `src: Front-end specification, no-layer variant`
- [ ] `C-FE-105` `capability` The app serves the no-layer variant to a device failing the capability check, to a visitor asking for reduced data, to a crawler. `src: Front-end specification, no-layer variant`
- [ ] `C-FE-106` `constraint` The app ships no binary that was downloaded. `src: Front-end specification, zero-asset`
- [ ] `C-FE-107` `ui` The app carries two gradients: the placeholder sheen, the corner scrim. `src: Front-end specification, zero-asset`
- [ ] `C-FE-108` `ui` The app starts the placeholder sheen's first stop at a negative position. `src: Front-end specification, zero-asset`
- [ ] `C-FE-109` `ui` The app derives a missing image's placeholder from a hash of the record identifier, using two palette colours, at the slot's aspect ratio. `src: Front-end specification, zero-asset`
- [ ] `C-FE-110` `ui` The app sets the record's initials in the brand sans at low contrast on a generated placeholder. `src: Front-end specification, zero-asset`
- [ ] `C-FE-111` `ui` The app generates grain, cloud density, terrain break-up, micro surface relief once at startup. `src: Front-end specification, zero-asset`
- [ ] `C-FE-112` `constraint` The app requests no generated texture over the network. `src: Front-end specification, zero-asset`
- [ ] `C-FE-113` `ui` The app renders the archive heading in `fs-h1-index`, left aligned, in the brand colour. `src: Front-end specification, archive`
- [ ] `C-FE-114` `ui` The app renders three archive cards across on a wide screen. `src: Front-end specification, archive`
- [ ] `C-FE-115` `ui` The app renders a card image at the small softness with a fixed aspect, a cover fit. `src: Front-end specification, archive`
- [ ] `C-FE-116` `ui` The app renders a card date at `fs-body-s` in the secondary copy colour. `src: Front-end specification, archive`
- [ ] `C-FE-117` `ui` The app renders a card title at `fs-s2` in the brand colour over at most two lines. `src: Front-end specification, archive`
- [ ] `C-FE-118` `ui` The app renders a card date as a long month, a day, a four-digit year, with no comma before the year. `src: Front-end specification, archive`
- [ ] `C-FE-119` `ui` The app hides a card's underline at zero horizontal scale, growing the underline to full width from a fixed origin on pointer entry. `src: Front-end specification, archive`
- [ ] `C-FE-120` `ui` The app reveals archive cards from below, staggered down the grid. `src: Front-end specification, archive`
- [ ] `C-FE-121` `ui` The app renders five centred paginator controls in the order `First`, previous, the current page numeral, next, `Last`. `src: Front-end specification, paginator`
- [ ] `C-FE-122` `ui` The app renders each paginator control as a rounded rectangle at the small softness with a hairline border. `src: Front-end specification, paginator`
- [ ] `C-FE-123` `ui` The app renders the first two paginator controls unavailable at half strength on page one. `src: Front-end specification, paginator`
- [ ] `C-FE-124` `ui` The app keeps an unavailable paginator control in the document, skipped by the keyboard. `src: Front-end specification, paginator`
- [ ] `C-FE-125` `ui` The app keeps the paginator the same width between pages. `src: Front-end specification, paginator`
- [ ] `C-FE-126` `ui` The app shows a principal holding one division that division's name with no switcher control. `src: Front-end specification, console shell`
- [ ] `C-FE-127` `ui` The app shows a principal holding no division an explanatory surface with no content. `src: Front-end specification, console shell`
- [ ] `C-FE-128` `ui` The app renders the console record surface as three panes: the editor, the review rail, the preview. `src: Front-end specification, console shell`
- [ ] `C-FE-129` `ui` The app orders the editor's fields in the order the record's type declares. `src: Front-end specification, console shell`

## C-TR Technical requirements

- [ ] `C-TR-01` `literal` The app is built with the frontend `SolidStart`. `src: Technical requirements para 1`
- [ ] `C-TR-02` `literal` The app is built with the backend `FastAPI` on Python. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The app paints a public route first from HTML the server produced from the finished-document store. `src: Technical requirements para 1`
- [ ] `C-TR-04` `constraint` The app never prerenders the console. `src: Technical requirements para 1`
- [ ] `C-TR-05` `literal` The app stores records in `PostgreSQL`. `src: Technical requirements para 1`
- [ ] `C-TR-06` `literal` The app stores media bytes in `minio`. `src: Technical requirements para 1`
- [ ] `C-TR-07` `literal` The app answers `GET /api/health` with `200` once ready. `src: Technical requirements para 1`
- [ ] `C-TR-08` `capability` The app writes one structured line per request to standard output. `src: Technical requirements para 1`
- [ ] `C-TR-09` `data` The app carries the method, the path, the status, the request identifier, the principal identifier in a log line. `src: Technical requirements para 1`
- [ ] `C-TR-10` `constraint` The app writes no password, no bearer token, no object-store credential to a log line. `src: Technical requirements para 1`
- [ ] `C-TR-11` `constraint` The app writes no visitor name, no visitor address, no form text to a log line. `src: Technical requirements para 1`
- [ ] `C-TR-12` `constraint` The app introduces no second database, cache, queue, object store, identity provider, mail vendor. `src: Technical requirements para 2`
- [ ] `C-TR-13` `literal` The app reads `DATABASE_URL` from the environment. `src: Technical requirements para 3`
- [ ] `C-TR-14` `literal` The app reads `STORAGE_ENDPOINT` from the environment. `src: Technical requirements para 3`
- [ ] `C-TR-15` `literal` The app reads `STORAGE_BUCKET` from the environment. `src: Technical requirements para 3`
- [ ] `C-TR-16` `literal` The app reads `STORAGE_ACCESS_KEY` from the environment. `src: Technical requirements para 3`
- [ ] `C-TR-17` `literal` The app reads `STORAGE_SECRET_KEY` from the environment. `src: Technical requirements para 3`
- [ ] `C-TR-18` `literal` The app reads `APP_PUBLIC_URL` from the environment. `src: Technical requirements para 3`
- [ ] `C-TR-19` `literal` The app reads `APP_PUBLIC_PORT` from the environment. `src: Technical requirements para 3`
- [ ] `C-TR-20` `constraint` The app hardcodes no host, no port. `src: Technical requirements para 3`
- [ ] `C-TR-21` `capability` The app accepts a request identifier from the caller, or mints one. `src: Technical requirements para 4`
- [ ] `C-TR-22` `capability` The app echoes the request identifier on the response. `src: Technical requirements para 4`
- [ ] `C-TR-23` `capability` The app writes the request identifier onto every audit entry the request causes. `src: Technical requirements para 4`
- [ ] `C-TR-24` `contract` The app carries a strict transport policy on every response. `src: Technical requirements para 5`
- [ ] `C-TR-25` `contract` The app carries a policy forbidding content-type sniffing on every response. `src: Technical requirements para 5`
- [ ] `C-TR-26` `contract` The app carries a policy denying every frame ancestor on every response. `src: Technical requirements para 5`
- [ ] `C-TR-27` `contract` The app carries a policy denying camera, microphone, geolocation, payment on every response. `src: Technical requirements para 5`
- [ ] `C-TR-28` `contract` The app carries a cross-origin opener policy confined to the same origin. `src: Technical requirements para 5`
- [ ] `C-TR-29` `contract` The app limits referrer information to the origin on a cross-origin navigation. `src: Technical requirements para 5`
- [ ] `C-TR-30` `constraint` The app reaches no state-changing action by a safe method. `src: Technical requirements para 5`
- [ ] `C-TR-31` `constraint` The app puts no credential, no API key, no administrative token in the script bundle. `src: Technical requirements para 5`
- [ ] `C-TR-32` `constraint` The app puts no credential in a stylesheet, in an inline script, in a JSON payload served anonymously. `src: Technical requirements para 5`
- [ ] `C-TR-33` `capability` The app serves a favicon, declaring the favicon in the document head of every route rendered. `src: Technical requirements para 6`
- [ ] `C-TR-34` `capability` The app declares a social preview title, a description, an image on every public route. `src: Technical requirements para 6`
- [ ] `C-TR-35` `constraint` The app shares no social preview title, no description between two public routes. `src: Technical requirements para 6`
- [ ] `C-TR-36` `constraint` The app resolves every declared social preview image to a real object. `src: Technical requirements para 6`
- [ ] `C-TR-37` `constraint` The app narrows the public search, the archive filters, the console lists in the store. `src: Technical requirements para 7`
- [ ] `C-TR-38` `contract` The app pages a console list by cursor rather than by offset. `src: Technical requirements para 7`
- [ ] `C-TR-39` `contract` The app keeps the largest element painted on any public route text rather than a visual layer. `src: Technical requirements para 8`
- [ ] `C-TR-40` `contract` The app answers a public document read, an archive page, a search inside one budget at 20000 content records. `src: Technical requirements para 8`
- [ ] `C-TR-41` `contract` The app answers inside that budget at 4000 audit entries. `src: Technical requirements para 8`

## C-DM Data model

- [ ] `C-DM-01` `data` The app carries fourteen tables. `src: Data model para 1`
- [ ] `C-DM-02` `data` The app stores every timestamp in UTC. `src: Data model para 1`
- [ ] `C-DM-03` `literal` The app writes the password `deku-demo-pw-2026` into `/app/USER_README.md` beside each account. `src: Data model, password paragraph`
- [ ] `C-DM-04` `data` The app stores a principal's email unique, lowercase. `src: Data model, principals`
- [ ] `C-DM-05` `data` The app carries a key, a name, a wordmark, a primary colour role, an archived flag on a division. `src: Data model, divisions`
- [ ] `C-DM-06` `data` The app allows a membership to carry a null division only for `group_admin`. `src: Data model, memberships`
- [ ] `C-DM-07` `data` The app carries a city, a country, a jurisdiction, address lines on an office. `src: Data model, offices`
- [ ] `C-DM-08` `data` The app stores both a normalised telephone form, a display telephone form on an office. `src: Data model, offices`
- [ ] `C-DM-09` `constraint` The app marks exactly one office per jurisdiction the data controller contact. `src: Data model, offices`
- [ ] `C-DM-10` `data` The app carries a latitude, a longitude, a marker label on an office. `src: Data model, offices`
- [ ] `C-DM-11` `constraint` The app keeps no two records of one type sharing a slug. `src: Data model, content_records`
- [ ] `C-DM-12` `data` The app carries a fast-path count over seven days on a content record. `src: Data model, content_records`
- [ ] `C-DM-13` `data` The app carries a stable block identifier on every content block. `src: Data model, content_blocks`
- [ ] `C-DM-14` `constraint` The app keeps at most one submission per record carrying a null completion instant. `src: Data model, submissions`
- [ ] `C-DM-15` `constraint` The app keeps no approval stage decided by the stage's submission author. `src: Data model, approval_stages`
- [ ] `C-DM-16` `constraint` The app keeps no two stages of one submission decided by the same principal. `src: Data model, approval_stages`
- [ ] `C-DM-17` `constraint` The app keeps a delegation's expiry no more than 30 days after the grant. `src: Data model, delegations`
- [ ] `C-DM-18` `constraint` The app keeps a reference code paired with a version unique in the register. `src: Data model, policy_entries`
- [ ] `C-DM-19` `data` The app records the policy reference code, the policy version a published revision carried. `src: Data model, disclosure_bindings`
- [ ] `C-DM-20` `constraint` The app never rewrites a disclosure binding after publication. `src: Data model, disclosure_bindings`
- [ ] `C-DM-21` `data` The app carries an object key, a content type, a byte size, a checksum on a media row. `src: Data model, media`
- [ ] `C-DM-22` `data` The app carries a width, a height, a focal point on a media row. `src: Data model, media`
- [ ] `C-DM-23` `data` The app carries a scan state on a media row. `src: Data model, media`
- [ ] `C-DM-24` `data` The app carries a route path, a locale, a jurisdiction variant, a rendered instant, an entity tag, a payload on a published document. `src: Data model, published_documents`
- [ ] `C-DM-25` `data` The app carries the policy versions, the declared dependencies on a published document. `src: Data model, published_documents`
- [ ] `C-DM-26` `constraint` The app reads only the published document table on the public serving path. `src: Data model, published_documents`
- [ ] `C-DM-27` `data` The app carries a public reference, a subject area, a country, a jurisdiction on an enquiry. `src: Data model, enquiries`
- [ ] `C-DM-28` `data` The app carries a consent notice version, a consent instant, a delivery state on an enquiry. `src: Data model, enquiries`
- [ ] `C-DM-29` `capability` The app derives the release counter rather than storing the counter. `src: Data model, derived`
- [ ] `C-DM-30` `capability` The app derives whether a policy entry is currently in force. `src: Data model, derived`
- [ ] `C-DM-31` `capability` The app derives the archive's page count. `src: Data model, derived`
- [ ] `C-DM-32` `capability` The app derives a chapter's numeral once an unpublished chapter renumbers the set. `src: Data model, derived`
- [ ] `C-DM-33` `constraint` The app accepts exactly one of two transitions on one record from the same starting state. `src: Data model, concurrency paragraph`
- [ ] `C-DM-34` `constraint` The app records exactly one publication for two publications of one embargoed record at the instant. `src: Data model, concurrency paragraph`
- [ ] `C-DM-35` `literal` The app seeds the Geneva office at `12 Quai des Bergues, 1201 Geneva`, `+41225550118`, `gva@calder.example.com`. `src: Data model, seed data`
- [ ] `C-DM-36` `literal` The app seeds the Dubai office at `Level 14, Gate Village 7, DIFC, Dubai`, `+97145550142`, `dxb@calder.example.com`. `src: Data model, seed data`
- [ ] `C-DM-37` `literal` The app seeds the Singapore office at `8 Marina View, Asia Square Tower 1, Singapore`, `+6562550173`, `sgp@calder.example.com`. `src: Data model, seed data`
- [ ] `C-DM-38` `literal` The app seeds the media enquiries address `media@calder.example.com`. `src: Data model, seed data`
- [ ] `C-DM-39` `literal` The app seeds nine published releases, the newest titled `Calder joins Energy LEAP for Operational Excellence`. `src: Data model, seed data`
- [ ] `C-DM-40` `literal` The app seeds the release `Calder Maritime acquires its first vessel` as the oldest published release. `src: Data model, seed data`
- [ ] `C-DM-41` `literal` The app seeds one embargoed `market_sensitive` release titled `Calder Trading agrees a multi-year naphtha supply arrangement`. `src: Data model, seed data`
- [ ] `C-DM-42` `capability` The app seeds the embargoed release with a lead image already in the bucket. `src: Data model, seed data`
- [ ] `C-DM-43` `literal` The app seeds one withdrawn release titled `Calder restates its 2022 throughput figures`. `src: Data model, seed data`
- [ ] `C-DM-44` `literal` The app seeds the withdrawal reason `Superseded by a corrected statement`. `src: Data model, seed data`
- [ ] `C-DM-45` `capability` The app seeds one `draft` release on `trading`. `src: Data model, seed data`
- [ ] `C-DM-46` `capability` The app seeds one `compliance_review` release on `capital` whose legal stage was decided by `legal_reviewer@example.com`. `src: Data model, seed data`
- [ ] `C-DM-47` `capability` The app seeds one `approved` release on `capital` classified `general`. `src: Data model, seed data`
- [ ] `C-DM-48` `ui` The app seeds the oil family carrying the nine product names the brief pins, in the brief's order. `src: Data model, seed data`
- [ ] `C-DM-49` `literal` The app seeds the metals family carrying `Ferroalloys`, `Dry Bulk`, `Base Metals`. `src: Data model, seed data`
- [ ] `C-DM-50` `capability` The app seeds `Renewables` carrying a body, no image. `src: Data model, seed data`
- [ ] `C-DM-51` `capability` The app seeds three vessel records on `maritime`, two owned, one chartered. `src: Data model, seed data`
- [ ] `C-DM-52` `capability` The app seeds two investment records on `kite-energy`. `src: Data model, seed data`
- [ ] `C-DM-53` `capability` The app seeds eight person records on `group`, six published, one scheduled to stop displaying, one unpublished. `src: Data model, seed data`
- [ ] `C-DM-54` `literal` The app seeds one figures record carrying an office count of `15`, a nationality count of `27`. `src: Data model, seed data`
- [ ] `C-DM-55` `literal` The app seeds the figures record carrying a female share of the global team of `35`, a female share of management of `22`. `src: Data model, seed data`
- [ ] `C-DM-56` `data` The app carries an as-at date on the figures record. `src: Data model, seed data`
- [ ] `C-DM-57` `capability` The app renders the home diversity paragraph from the figures record rather than from the template. `src: Data model, seed data`
- [ ] `C-DM-58` `literal` The app seeds six register entries: `POL-CONDUCT`, `POL-PRIVACY-CH`, `POL-PRIVACY-AE`, `POL-PRIVACY-SG`, `POL-TERMS`, `POL-DISC-REG`. `src: Data model, seed data`
- [ ] `C-DM-59` `capability` The app seeds the three privacy notice entries at version 3 sharing a parent. `src: Data model, seed data`
- [ ] `C-DM-60` `capability` The app retains the conduct register entry version 1 as a superseded version carrying the period the version applied. `src: Data model, seed data`
- [ ] `C-DM-61` `capability` The app publishes five register entries externally, the regulated disclaimer as both. `src: Data model, seed data`
- [ ] `C-DM-62` `capability` The app derives the copyright year from the latest publication instant, or from the build instant. `src: Data model, copyright paragraph`
- [ ] `C-DM-63` `constraint` The app never authors the copyright year. `src: Data model, copyright paragraph`
- [ ] `C-DM-64` `constraint` The app seeds idempotently, duplicating no row on a restart. `src: Data model, final line`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app carries no confidential reporting channel, no anonymous case intake, no claim code, no break-glass access. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The app carries no live three dimensional scene layer, no mesh loading, no texture transcoding, no camera path through geometry. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` The app carries no ambient audio layer, no audio meter, no sound control. `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` The app carries no federated sign-in, no directory provisioning, no second factor, no step-up assurance. `src: Constraints bullet 4`
- [ ] `C-CN-05` `constraint` The app carries no service credential, no integration credential, no passkey, no recovery code. `src: Constraints bullet 4`
- [ ] `C-CN-06` `constraint` The app carries no email delivery, no notification delivery of any kind. `src: Constraints bullet 5`
- [ ] `C-CN-07` `constraint` The app carries no outbound webhook, no event subscriber, no inbound hook, no third-party integration. `src: Constraints bullet 6`
- [ ] `C-CN-08` `constraint` The app carries no third-party script, no tag manager, no external analytics, no external consent platform. `src: Constraints bullet 7`
- [ ] `C-CN-09` `constraint` The app offers no cached copy of a previously visited route with the network off. `src: Constraints bullet 8`
- [ ] `C-CN-10` `constraint` The app carries no residency choice, no per-region key, no retention policy engine, no erasure workflow, no subject access export. `src: Constraints bullet 9`
- [ ] `C-CN-11` `constraint` The app carries one locale, English, with no translation workflow, no locale negotiation, no right-to-left mirroring. `src: Constraints bullet 10`
- [ ] `C-CN-12` `constraint` The app keeps the two scroll-cue strings as two strings rather than reusing one. `src: Constraints bullet 10`
- [ ] `C-CN-13` `constraint` The app carries no trading, position, cargo, vessel movement, price, counterparty data. `src: Constraints bullet 11`
- [ ] `C-CN-14` `constraint` The app holds no credential reaching any system holding trading data. `src: Constraints bullet 11`
- [ ] `C-CN-15` `constraint` The app makes no external network call at runtime beyond the two named backing services. `src: Constraints bullet 12`
- [ ] `C-CN-16` `constraint` The app ships no native application, no packaged desktop build. `src: Constraints bullet 13`
- [ ] `C-CN-17` `constraint` The app stays responsive with 20000 content records across the five divisions. `src: Constraints bullet 14`
- [ ] `C-CN-18` `constraint` The app stays responsive with 4000 audit entries. `src: Constraints bullet 14`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The app listens on the container-internal port `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The app serves the HTTP API on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-05` `literal` The app writes login credentials to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-06` `literal` The app creates an empty `.browser_screenshots/` directory at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-07` `literal` The app creates an empty `.downloads/` directory at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` The app serves a production build behind a static or preview server. `src: Deployment contract bullet 7`
- [ ] `C-DC-09` `contract` The app keeps the server running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-10` `contract` The app runs the server outside the shell process tree. `src: Deployment contract bullet 8`
- [ ] `C-DC-11` `literal` The app binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-12` `constraint` The app downloads, installs, starts no copy of a named backing service. `src: Deployment contract bullet 10`
- [ ] `C-DC-13` `constraint` The app uses no provider outside the two named in the brief. `src: Deployment contract bullet 11`
- [ ] `C-DC-14` `constraint` The app declares no persistent volume, no fixed container name, no custom network. `src: Deployment contract bullet 12`
- [ ] `C-DC-15` `contract` The app returns a top-level JSON array from a list endpoint. `src: Deployment contract, conventions`
- [ ] `C-DC-16` `contract` The app rejects an invalid or unauthorized call as a client error rather than as a server error. `src: Deployment contract, conventions`
- [ ] `C-DC-17` `contract` The app treats an identifier as an opaque string, parsing no meaning from the identifier. `src: Deployment contract, conventions`
- [ ] `C-DC-18` `contract` The app renders a timestamp as ISO-8601 in UTC with a trailing `Z`. `src: Deployment contract, conventions`
- [ ] `C-DC-19` `contract` The app carries a machine-readable `code`, a human-readable `message`, the `request_id` on a rejection. `src: Deployment contract, conventions`
- [ ] `C-DC-20` `contract` The app refuses an unknown field in a request body rather than ignoring the field. `src: Deployment contract, conventions`
- [ ] `C-DC-21` `literal` The app pages a console list request by `cursor`, `page_size`. `src: Deployment contract, conventions`
- [ ] `C-DC-22` `literal` The app returns `has_more`, `next_cursor` on a paged response. `src: Deployment contract, conventions`
- [ ] `C-DC-23` `contract` The app keeps a cursor stable as records are being written. `src: Deployment contract, conventions`
- [ ] `C-DC-24` `literal` The app accepts an optional `Idempotency-Key` on every write. `src: Deployment contract, conventions`
- [ ] `C-DC-25` `contract` The app requires bearer auth on everything outside the login, the health, the public surfaces. `src: Deployment contract, conventions`
- [ ] `C-DC-26` `literal` The app answers `GET /api/me` with a principal identifier, an email, a display name, memberships. `src: Deployment contract, API shapes`
- [ ] `C-DC-27` `literal` The app lists records at `GET /api/content/records`. `src: Deployment contract, API shapes`
- [ ] `C-DC-28` `literal` The app lists revisions at `GET /api/content/records/{id}/revisions`. `src: Deployment contract, API shapes`
- [ ] `C-DC-29` `literal` The app transitions a record at `POST /api/workflow/records/{id}/transition`. `src: Deployment contract, API shapes`
- [ ] `C-DC-30` `literal` The app publishes a record at `POST /api/workflow/records/{id}/publish`. `src: Deployment contract, API shapes`
- [ ] `C-DC-31` `literal` The app lists register entries at `GET /api/policy/entries`. `src: Deployment contract, API shapes`
- [ ] `C-DC-32` `literal` The app lists the archive at `GET /api/public/releases`. `src: Deployment contract, API shapes`
- [ ] `C-DC-33` `literal` The app returns one release at `GET /api/public/releases/{slug}`. `src: Deployment contract, API shapes`
- [ ] `C-DC-34` `literal` The app lists divisions at `GET /api/public/divisions`. `src: Deployment contract, API shapes`
- [ ] `C-DC-35` `literal` The app lists offices at `GET /api/public/offices`. `src: Deployment contract, API shapes`
- [ ] `C-DC-36` `literal` The app returns the group figures at `GET /api/public/figures`. `src: Deployment contract, API shapes`
- [ ] `C-DC-37` `literal` The app lists register entries publicly at `GET /api/public/policies`. `src: Deployment contract, API shapes`
- [ ] `C-DC-38` `literal` The app rejects a call with the code `unauthorized` where no valid credential was presented. `src: Deployment contract, error catalogue`
- [ ] `C-DC-39` `literal` The app rejects a call with the code `forbidden_permission` where the decision denied the action. `src: Deployment contract, error catalogue`
- [ ] `C-DC-40` `literal` The app rejects a call with the code `not_found` where the resource does not exist or may not be known. `src: Deployment contract, error catalogue`
- [ ] `C-DC-41` `literal` The app rejects a call with the code `gone` where the resource existed, was withdrawn. `src: Deployment contract, error catalogue`
- [ ] `C-DC-42` `literal` The app rejects a call with the code `conflict_version` where the revision or state supplied is not the stored one. `src: Deployment contract, error catalogue`
- [ ] `C-DC-43` `literal` The app rejects a call with the code `conflict_state` where the resource state forbids the action. `src: Deployment contract, error catalogue`
- [ ] `C-DC-44` `literal` The app rejects a call with the code `validation_failed` carrying a per-field list in `details`. `src: Deployment contract, error catalogue`
- [ ] `C-DC-45` `literal` The app rejects a call with the code `rate_limited` carrying how long until attempts are accepted again. `src: Deployment contract, error catalogue`
- [ ] `C-DC-46` `constraint` The app answers an embargoed slug, a record on an unheld division, a slug never issued all as `not_found`. `src: Deployment contract, error catalogue note`
- [ ] `C-DC-47` `constraint` The app uses `gone` only where the absence is itself the public statement. `src: Deployment contract, error catalogue note`
- [ ] `C-DC-48` `constraint` The app lets no store error, no stack trace reach a caller. `src: Deployment contract, error catalogue note`
- [ ] `C-DC-49` `constraint` The app keeps no in-memory list of media standing in for the bucket. `src: Deployment contract, no mocks`
- [ ] `C-DC-50` `constraint` The app writes no media bytes to the app container's own filesystem. `src: Deployment contract, no mocks`
- [ ] `C-DC-51` `constraint` The app holds no data address in a block payload standing in for an object. `src: Deployment contract, no mocks`
- [ ] `C-DC-52` `constraint` The app returns no self-answered success standing in for a provider. `src: Deployment contract, no mocks`

## Pinned literals

| Value | What it is | Item | Where the instruction states it |
|---|---|---|---|
| `author@example.com` | a seeded address | C-RL-43 | User roles, seeded accounts table |
| `author` | a value the brief pins | C-RL-43 | User roles, seeded accounts table |
| `trading` | a value the brief pins | C-RL-43 | User roles, seeded accounts table |
| `legal_reviewer` | a value the brief pins | C-RL-44 | User roles, seeded accounts table |
| `capital` | a value the brief pins | C-RL-44 | User roles, seeded accounts table |
| `author2@example.com` | a seeded address | C-RL-45 | User roles, seeded accounts table |
| `legal_reviewer@example.com` | a seeded address | C-RL-46 | User roles, seeded accounts table |
| `compliance_officer@example.com` | a seeded address | C-RL-47 | User roles, seeded accounts table |
| `compliance_officer` | a value the brief pins | C-RL-47 | User roles, seeded accounts table |
| `publisher@example.com` | a seeded address | C-RL-48 | User roles, seeded accounts table |
| `publisher` | a value the brief pins | C-RL-48 | User roles, seeded accounts table |
| `group_admin@example.com` | a seeded address | C-RL-49 | User roles, seeded accounts table |
| `deku-demo-pw-2026` | a value the brief pins | C-RL-50 | User roles, seeded accounts table |
| `POST /api/auth/login` | an endpoint the brief pins | C-CF-01 | Core features, Auth rule 1 |
| `access_token` | a value the brief pins | C-CF-02 | Core features, Auth rule 1 |
| `POST /api/auth/logout` | an endpoint the brief pins | C-CF-08 | Core features, Auth rule 4 |
| `group` | a value the brief pins | C-CF-31 | Core features, Divisions rule 1 |
| `Calder Group` | a value the brief pins | C-CF-31 | Core features, Divisions rule 1 |
| `Calder Trading` | a value the brief pins | C-CF-32 | Core features, Divisions rule 1 |
| `Calder Capital` | a value the brief pins | C-CF-33 | Core features, Divisions rule 1 |
| `maritime` | a value the brief pins | C-CF-34 | Core features, Divisions rule 1 |
| `Calder Maritime` | a value the brief pins | C-CF-34 | Core features, Divisions rule 1 |
| `kite-energy` | a value the brief pins | C-CF-35 | Core features, Divisions rule 1 |
| `Kite Energy` | a value the brief pins | C-CF-35 | Core features, Divisions rule 1 |
| `GET /api/admin/members` | an endpoint the brief pins | C-CF-45 | Core features, Divisions rule 3 |
| `group_admin` | a value the brief pins | C-CF-48 | Core features, Divisions rule 5 |
| `POST /api/admin/memberships` | an endpoint the brief pins | C-CF-48 | Core features, Divisions rule 5 |
| `GET /api/admin/exceptions` | an endpoint the brief pins | C-CF-57 | Core features, Divisions rule 8 |
| `paragraph` | a value the brief pins | C-CF-76 | Core features, Records rule 6 |
| `subheading_2` | a value the brief pins | C-CF-76 | Core features, Records rule 6 |
| `subheading_3` | a value the brief pins | C-CF-76 | Core features, Records rule 6 |
| `list_unordered` | a value the brief pins | C-CF-76 | Core features, Records rule 6 |
| `list_ordered` | a value the brief pins | C-CF-76 | Core features, Records rule 6 |
| `quote` | a value the brief pins | C-CF-76 | Core features, Records rule 6 |
| `image` | a value the brief pins | C-CF-76 | Core features, Records rule 6 |
| `table` | a value the brief pins | C-CF-76 | Core features, Records rule 6 |
| `draft` | a value the brief pins | C-CF-83 | Core features, Records rule 8 |
| `POST /api/content/records` | an endpoint the brief pins | C-CF-83 | Core features, Records rule 8 |
| `PATCH /api/content/records/{id}` | an endpoint the brief pins | C-CF-85 | Core features, Records rule 8 |
| `in_review` | a value the brief pins | C-CF-106 | Core features, chain rule 1 |
| `legal_review` | a value the brief pins | C-CF-106 | Core features, chain rule 1 |
| `compliance_review` | a value the brief pins | C-CF-106 | Core features, chain rule 1 |
| `changes_requested` | a value the brief pins | C-CF-106 | Core features, chain rule 1 |
| `approved` | a value the brief pins | C-CF-106 | Core features, chain rule 1 |
| `embargoed` | a value the brief pins | C-CF-106 | Core features, chain rule 1 |
| `published` | a value the brief pins | C-CF-106 | Core features, chain rule 1 |
| `unpublished` | a value the brief pins | C-CF-106 | Core features, chain rule 1 |
| `archived` | a value the brief pins | C-CF-106 | Core features, chain rule 1 |
| `POST /api/workflow/records/{id}/submit` | an endpoint the brief pins | C-CF-108 | Core features, chain rule 2 |
| `POST /api/workflow/delegations` | an endpoint the brief pins | C-CF-140 | Core features, chain rule 9 |
| `GET /api/workflow/inbox` | an endpoint the brief pins | C-CF-162 | Core features, chain rule 13 |
| `general` | a value the brief pins | C-CF-175 | Core features, classification rule 1 |
| `regulated` | a value the brief pins | C-CF-175 | Core features, classification rule 1 |
| `market_sensitive` | a value the brief pins | C-CF-175 | Core features, classification rule 1 |
| `restricted` | a value the brief pins | C-CF-175 | Core features, classification rule 1 |
| `POST /api/content/records/{id}/classify` | an endpoint the brief pins | C-CF-178 | Core features, classification rule 2 |
| `POST /api/workflow/records/{id}/schedule` | an endpoint the brief pins | C-CF-201 | Core features, embargo rule 1 |
| `DELETE /api/workflow/records/{id}/schedule` | an endpoint the brief pins | C-CF-222 | Core features, embargo rule 8 |
| `alt_text` | a value the brief pins | C-CF-230 | Core features, Media rule 1 |
| `POST /api/content/records/{id}/media` | an endpoint the brief pins | C-CF-230 | Core features, Media rule 1 |
| `media/{division_key}/{record_id}/{sha256_of_bytes}.{ext}` | a value the brief pins | C-CF-231 | Core features, Media rule 2 |
| `GET /api/media/{mediaId}` | an endpoint the brief pins | C-CF-238 | Core features, Media rule 6 |
| `/` | a value the brief pins | C-CF-244 | Core features, public site rule 1 |
| `/trading/` | a value the brief pins | C-CF-244 | Core features, public site rule 1 |
| `/capital/` | a value the brief pins | C-CF-244 | Core features, public site rule 1 |
| `/maritime/` | a value the brief pins | C-CF-244 | Core features, public site rule 1 |
| `/kite-energy/` | a value the brief pins | C-CF-244 | Core features, public site rule 1 |
| `/who-we-are/` | a value the brief pins | C-CF-244 | Core features, public site rule 1 |
| `/news/` | a value the brief pins | C-CF-244 | Core features, public site rule 1 |
| `/news/{slug}/` | a value the brief pins | C-CF-244 | Core features, public site rule 1 |
| `/sustainability/` | a value the brief pins | C-CF-244 | Core features, public site rule 1 |
| `/contact/` | a value the brief pins | C-CF-244 | Core features, public site rule 1 |
| `/privacy-policy/` | a value the brief pins | C-CF-244 | Core features, public site rule 1 |
| `/terms-of-use/` | a value the brief pins | C-CF-244 | Core features, public site rule 1 |
| `/search` | a value the brief pins | C-CF-244 | Core features, public site rule 1 |
| `9` | a value the brief pins | C-CF-254 | Core features, public site rule 4 |
| `/news/?page=2` | a value the brief pins | C-CF-255 | Core features, public site rule 5 |
| `/news/?division=trading` | a value the brief pins | C-CF-256 | Core features, public site rule 5 |
| `/news/?year=2023` | a value the brief pins | C-CF-257 | Core features, public site rule 5 |
| `6` | a value the brief pins | C-CF-259 | Core features, public site rule 5 |
| `POST /api/workflow/records/{id}/unpublish` | an endpoint the brief pins | C-CF-269 | Core features, public site rule 8 |
| `Oil` | a value the brief pins | C-CF-275 | Core features, public site rule 9 |
| `Metals` | a value the brief pins | C-CF-275 | Core features, public site rule 9 |
| `CH` | a value the brief pins | C-CF-300 | Core features, public site rule 16 |
| `AE-DIFC` | a value the brief pins | C-CF-300 | Core features, public site rule 16 |
| `SG` | a value the brief pins | C-CF-300 | Core features, public site rule 16 |
| `GET /api/public/search` | an endpoint the brief pins | C-CF-303 | Core features, public site rule 17 |
| `/search?q=` | a value the brief pins | C-CF-305 | Core features, public site rule 17 |
| `POST /api/public/enquiries` | an endpoint the brief pins | C-CF-323 | Core features, enquiry rule 1 |
| `subject_area` | a value the brief pins | C-CF-324 | Core features, enquiry rule 1 |
| `GET /api/admin/audit` | an endpoint the brief pins | C-CF-390 | Core features, audit rule 4 |
| `dependency_unavailable` | a value the brief pins | C-CF-417 | Core features, Edge case 20 |
| `"CalderSans", "Century Schoolbook L", "Futura", "Avenir Next", sans-serif` | a value the brief pins | C-UX-33 | UI/UX notes, type |
| `News` | a value the brief pins | C-UX-171 | UI/UX notes, copy |
| `Menu` | a value the brief pins | C-UX-171 | UI/UX notes, copy |
| `Contact` | a value the brief pins | C-UX-171 | UI/UX notes, copy |
| `ESG` | a value the brief pins | C-UX-171 | UI/UX notes, copy |
| `Privacy policy` | a value the brief pins | C-UX-171 | UI/UX notes, copy |
| `Terms of use` | a value the brief pins | C-UX-171 | UI/UX notes, copy |
| `Scroll down to discover` | a value the brief pins | C-UX-172 | UI/UX notes, copy |
| `Swipe down` | a value the brief pins | C-UX-172 | UI/UX notes, copy |
| `Who we are` | a value the brief pins | C-UX-172 | UI/UX notes, copy |
| `Explore Our` | a value the brief pins | C-UX-173 | UI/UX notes, copy |
| `Products:` | a value the brief pins | C-UX-173 | UI/UX notes, copy |
| `Environmental` | a value the brief pins | C-UX-174 | UI/UX notes, copy |
| `Social` | a value the brief pins | C-UX-174 | UI/UX notes, copy |
| `Governance` | a value the brief pins | C-UX-174 | UI/UX notes, copy |
| `Contact us` | a value the brief pins | C-UX-174 | UI/UX notes, copy |
| `First` | a value the brief pins | C-UX-174 | UI/UX notes, copy |
| `Last` | a value the brief pins | C-UX-174 | UI/UX notes, copy |
| `Geneva, Switzerland` | a value the brief pins | C-UX-175 | UI/UX notes, copy |
| `Dubai, UAE` | a value the brief pins | C-UX-175 | UI/UX notes, copy |
| `Singapore` | a value the brief pins | C-UX-175 | UI/UX notes, copy |
| `fs-h1` | a value the brief pins | C-FE-01 | Front-end specification, type scale |
| `2.5rem` | a value the brief pins | C-FE-01 | Front-end specification, type scale |
| `5rem` | a value the brief pins | C-FE-01 | Front-end specification, type scale |
| `1.2` | a value the brief pins | C-FE-01 | Front-end specification, type scale |
| `.25rem` | a value the brief pins | C-FE-02 | Front-end specification, type scale |
| `.5rem` | a value the brief pins | C-FE-02 | Front-end specification, type scale |
| `fs-h2` | a value the brief pins | C-FE-03 | Front-end specification, type scale |
| `2.25rem` | a value the brief pins | C-FE-03 | Front-end specification, type scale |
| `3.125rem` | a value the brief pins | C-FE-03 | Front-end specification, type scale |
| `1.4` | a value the brief pins | C-FE-03 | Front-end specification, type scale |
| `fs-h3` | a value the brief pins | C-FE-04 | Front-end specification, type scale |
| `1.75rem` | a value the brief pins | C-FE-04 | Front-end specification, type scale |
| `fs-h4` | a value the brief pins | C-FE-05 | Front-end specification, type scale |
| `.75rem` | a value the brief pins | C-FE-05 | Front-end specification, type scale |
| `1.25rem` | a value the brief pins | C-FE-05 | Front-end specification, type scale |
| `fs-h5` | a value the brief pins | C-FE-06 | Front-end specification, type scale |
| `1rem` | a value the brief pins | C-FE-06 | Front-end specification, type scale |
| `1.6` | a value the brief pins | C-FE-06 | Front-end specification, type scale |
| `fs-s1` | a value the brief pins | C-FE-07 | Front-end specification, type scale |
| `1.5rem` | a value the brief pins | C-FE-07 | Front-end specification, type scale |
| `fs-s2` | a value the brief pins | C-FE-08 | Front-end specification, type scale |
| `fs-body` | a value the brief pins | C-FE-09 | Front-end specification, type scale |
| `.08rem` | a value the brief pins | C-FE-09 | Front-end specification, type scale |
| `fs-body-s` | a value the brief pins | C-FE-10 | Front-end specification, type scale |
| `.06rem` | a value the brief pins | C-FE-10 | Front-end specification, type scale |
| `fs-cta` | a value the brief pins | C-FE-11 | Front-end specification, type scale |
| `.025rem` | a value the brief pins | C-FE-11 | Front-end specification, type scale |
| `fs-cta-s` | a value the brief pins | C-FE-12 | Front-end specification, type scale |
| `.03rem` | a value the brief pins | C-FE-12 | Front-end specification, type scale |
| `fs-label` | a value the brief pins | C-FE-13 | Front-end specification, type scale |
| `fs-numerals` | a value the brief pins | C-FE-14 | Front-end specification, type scale |
| `fs-label-lg` | a value the brief pins | C-FE-15 | Front-end specification, type scale |
| `14px` | a value the brief pins | C-FE-15 | Front-end specification, type scale |
| `16.8px` | a value the brief pins | C-FE-15 | Front-end specification, type scale |
| `fs-h1-index` | a value the brief pins | C-FE-16 | Front-end specification, type scale |
| `62px` | a value the brief pins | C-FE-16 | Front-end specification, type scale |
| `Operating Efficiently, Leading with Innovation.` | a value the brief pins | C-FE-69 | Front-end specification, journey |
| `Energy investments` | a value the brief pins | C-FE-71 | Front-end specification, journey |
| `Delivering sustainable energy solutions` | a value the brief pins | C-FE-79 | Front-end specification, journey |
| `Our pledge to corporate social responsibility` | a value the brief pins | C-FE-84 | Front-end specification, journey |
| `#WhoWeAre` | a value the brief pins | C-FE-86 | Front-end specification, journey |
| `#WhatWeDo` | a value the brief pins | C-FE-86 | Front-end specification, journey |
| `#GlobalConnectivity` | a value the brief pins | C-FE-86 | Front-end specification, journey |
| `#Sustainability` | a value the brief pins | C-FE-86 | Front-end specification, journey |
| `/#Sustainability` | a value the brief pins | C-FE-91 | Front-end specification, journey |
| `SolidStart` | a value the brief pins | C-TR-01 | Technical requirements para 1 |
| `FastAPI` | a value the brief pins | C-TR-02 | Technical requirements para 1 |
| `PostgreSQL` | a value the brief pins | C-TR-05 | Technical requirements para 1 |
| `minio` | a value the brief pins | C-TR-06 | Technical requirements para 1 |
| `GET /api/health` | an endpoint the brief pins | C-TR-07 | Technical requirements para 1 |
| `200` | a value the brief pins | C-TR-07 | Technical requirements para 1 |
| `DATABASE_URL` | a value the brief pins | C-TR-13 | Technical requirements para 3 |
| `STORAGE_ENDPOINT` | a value the brief pins | C-TR-14 | Technical requirements para 3 |
| `STORAGE_BUCKET` | a value the brief pins | C-TR-15 | Technical requirements para 3 |
| `STORAGE_ACCESS_KEY` | a value the brief pins | C-TR-16 | Technical requirements para 3 |
| `STORAGE_SECRET_KEY` | a value the brief pins | C-TR-17 | Technical requirements para 3 |
| `APP_PUBLIC_URL` | a value the brief pins | C-TR-18 | Technical requirements para 3 |
| `APP_PUBLIC_PORT` | a value the brief pins | C-TR-19 | Technical requirements para 3 |
| `/app/USER_README.md` | a value the brief pins | C-DM-03 | Data model, password paragraph |
| `12 Quai des Bergues, 1201 Geneva` | a value the brief pins | C-DM-35 | Data model, seed data |
| `+41225550118` | a value the brief pins | C-DM-35 | Data model, seed data |
| `gva@calder.example.com` | a seeded address | C-DM-35 | Data model, seed data |
| `Level 14, Gate Village 7, DIFC, Dubai` | a value the brief pins | C-DM-36 | Data model, seed data |
| `+97145550142` | a value the brief pins | C-DM-36 | Data model, seed data |
| `dxb@calder.example.com` | a seeded address | C-DM-36 | Data model, seed data |
| `8 Marina View, Asia Square Tower 1, Singapore` | a value the brief pins | C-DM-37 | Data model, seed data |
| `+6562550173` | a value the brief pins | C-DM-37 | Data model, seed data |
| `sgp@calder.example.com` | a seeded address | C-DM-37 | Data model, seed data |
| `media@calder.example.com` | a seeded address | C-DM-38 | Data model, seed data |
| `Calder joins Energy LEAP for Operational Excellence` | a value the brief pins | C-DM-39 | Data model, seed data |
| `Calder Maritime acquires its first vessel` | a value the brief pins | C-DM-40 | Data model, seed data |
| `Calder Trading agrees a multi-year naphtha supply arrangement` | a value the brief pins | C-DM-41 | Data model, seed data |
| `Calder restates its 2022 throughput figures` | a value the brief pins | C-DM-43 | Data model, seed data |
| `Superseded by a corrected statement` | a value the brief pins | C-DM-44 | Data model, seed data |
| `Ferroalloys` | a value the brief pins | C-DM-49 | Data model, seed data |
| `Dry Bulk` | a value the brief pins | C-DM-49 | Data model, seed data |
| `Base Metals` | a value the brief pins | C-DM-49 | Data model, seed data |
| `15` | a value the brief pins | C-DM-54 | Data model, seed data |
| `27` | a value the brief pins | C-DM-54 | Data model, seed data |
| `35` | a value the brief pins | C-DM-55 | Data model, seed data |
| `22` | a value the brief pins | C-DM-55 | Data model, seed data |
| `POL-CONDUCT` | a value the brief pins | C-DM-58 | Data model, seed data |
| `POL-PRIVACY-CH` | a value the brief pins | C-DM-58 | Data model, seed data |
| `POL-PRIVACY-AE` | a value the brief pins | C-DM-58 | Data model, seed data |
| `POL-PRIVACY-SG` | a value the brief pins | C-DM-58 | Data model, seed data |
| `POL-TERMS` | a value the brief pins | C-DM-58 | Data model, seed data |
| `POL-DISC-REG` | a value the brief pins | C-DM-58 | Data model, seed data |
| `4173` | a value the brief pins | C-DC-02 | Deployment contract bullet 1 |
| `.browser_screenshots/` | a value the brief pins | C-DC-06 | Deployment contract bullet 6 |
| `.downloads/` | a value the brief pins | C-DC-07 | Deployment contract bullet 6 |
| `0.0.0.0` | a value the brief pins | C-DC-11 | Deployment contract bullet 9 |
| `cursor` | a value the brief pins | C-DC-21 | Deployment contract, conventions |
| `page_size` | a value the brief pins | C-DC-21 | Deployment contract, conventions |
| `has_more` | a value the brief pins | C-DC-22 | Deployment contract, conventions |
| `next_cursor` | a value the brief pins | C-DC-22 | Deployment contract, conventions |
| `Idempotency-Key` | a value the brief pins | C-DC-24 | Deployment contract, conventions |
| `GET /api/me` | an endpoint the brief pins | C-DC-26 | Deployment contract, API shapes |
| `GET /api/content/records` | an endpoint the brief pins | C-DC-27 | Deployment contract, API shapes |
| `GET /api/content/records/{id}/revisions` | an endpoint the brief pins | C-DC-28 | Deployment contract, API shapes |
| `POST /api/workflow/records/{id}/transition` | an endpoint the brief pins | C-DC-29 | Deployment contract, API shapes |
| `POST /api/workflow/records/{id}/publish` | an endpoint the brief pins | C-DC-30 | Deployment contract, API shapes |
| `GET /api/policy/entries` | an endpoint the brief pins | C-DC-31 | Deployment contract, API shapes |
| `GET /api/public/releases` | an endpoint the brief pins | C-DC-32 | Deployment contract, API shapes |
| `GET /api/public/releases/{slug}` | an endpoint the brief pins | C-DC-33 | Deployment contract, API shapes |
| `GET /api/public/divisions` | an endpoint the brief pins | C-DC-34 | Deployment contract, API shapes |
| `GET /api/public/offices` | an endpoint the brief pins | C-DC-35 | Deployment contract, API shapes |
| `GET /api/public/figures` | an endpoint the brief pins | C-DC-36 | Deployment contract, API shapes |
| `GET /api/public/policies` | an endpoint the brief pins | C-DC-37 | Deployment contract, API shapes |
| `unauthorized` | a value the brief pins | C-DC-38 | Deployment contract, error catalogue |
| `forbidden_permission` | a value the brief pins | C-DC-39 | Deployment contract, error catalogue |
| `not_found` | a value the brief pins | C-DC-40 | Deployment contract, error catalogue |
| `gone` | a value the brief pins | C-DC-41 | Deployment contract, error catalogue |
| `conflict_version` | a value the brief pins | C-DC-42 | Deployment contract, error catalogue |
| `conflict_state` | a value the brief pins | C-DC-43 | Deployment contract, error catalogue |
| `validation_failed` | a value the brief pins | C-DC-44 | Deployment contract, error catalogue |
| `details` | a value the brief pins | C-DC-44 | Deployment contract, error catalogue |
| `rate_limited` | a value the brief pins | C-DC-45 | Deployment contract, error catalogue |
| `We cannot find that page. It may have moved, or the address may be mistyped.` | the not-found line | C-CF-309 | Core features, public site rule 19 |
| `This release was withdrawn on <date>. It is no longer published.` | the gone line | C-CF-309 | Core features, public site rule 19 |
| `Something went wrong at our end. Please try again. If you need to tell us about this, quote reference <request_id>.` | the server error line | C-CF-309 | Core features, public site rule 19 |
| `We are carrying out planned maintenance and expect to be back by <time>.` | the maintenance line | C-CF-309 | Core features, public site rule 19 |
| `Too many requests. Please wait <duration> and try again.` | the rate-limited line | C-CF-309 | Core features, public site rule 19 |
| `Calder is a global commodity trading and asset investment company.` | the chapter one headline | C-FE-58 | Front-end specification, journey |
| `We provide energy solutions with integrity and efficiency` | the chapter two heading | C-FE-58 | Front-end specification, journey |
| `Identify and seize opportunities that maximise value` | the capital proposition | C-FE-58 | Front-end specification, journey |
| `We strive to create an environment where everyone can thrive and contribute to our success.` | the people statement | C-FE-58 | Front-end specification, journey |
| `Power and Gas` | an oil family product name | C-DM-35 | Data model, seed data |
| `Crude oil` | an oil family product name | C-DM-35 | Data model, seed data |
| `Marine Fuels` | an oil family product name | C-DM-35 | Data model, seed data |
| `Gasoline` | an oil family product name | C-DM-35 | Data model, seed data |
| `LPG (Liquefied Petroleum Gas)` | an oil family product name | C-DM-35 | Data model, seed data |
| `Fuel Oil` | an oil family product name | C-DM-35 | Data model, seed data |
| `Downstream` | an oil family product name | C-DM-35 | Data model, seed data |
| `Naphtha` | an oil family product name | C-DM-35 | Data model, seed data |
| `Renewables` | an oil family product name | C-DM-35 | Data model, seed data |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 3 | 14 |
| User roles | 6 | 50 |
| Core features | 71 | 419 |
| User flow | 6 | 40 |
| UI and UX notes | 13 | 180 |
| Front-end specification | 15 | 129 |
| Technical requirements | 7 | 41 |
| Data model | 7 | 64 |
| Constraints | 1 | 18 |
| Deployment contract | 11 | 52 |
