# Checklist: vvvivid

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, constraints, deployment
Sections absent: buildplan
Items: 630
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` The app presents a grid of tiles carrying one tile per tool. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app opens a generator from a tile. `src: Overview para 1`
- [ ] `C-OV-03` `ui` The app places a live preview above a panel of controls. `src: Overview para 1`
- [ ] `C-OV-04` `capability` The app redraws the preview when a control changes. `src: Overview para 1`
- [ ] `C-OV-05` `contract` The app redraws the preview in the browser with no round trip. `src: Overview para 1`
- [ ] `C-OV-06` `capability` The app copies the markup of the drawn graphic. `src: Overview para 1`
- [ ] `C-OV-07` `capability` The app downloads a raster export of the drawn graphic. `src: Overview para 1`
- [ ] `C-OV-08` `constraint` The app requires no account before a generator works. `src: Overview para 1`
- [ ] `C-OV-09` `constraint` The app opens no modal before a generator works. `src: Overview para 1`
- [ ] `C-OV-10` `capability` The app saves the current settings as a named preset for a signed-in author. `src: Overview para 2`
- [ ] `C-OV-11` `contract` The app derives a preset address from the settings of that preset. `src: Overview para 2`
- [ ] `C-OV-12` `contract` The app makes a second save of one set of settings produce one stored row. `src: Overview para 2`
- [ ] `C-OV-13` `data` The app saves a preset as private. `src: Overview para 2`
- [ ] `C-OV-14` `capability` The app publishes an owned preset to a public gallery. `src: Overview para 2`
- [ ] `C-OV-15` `capability` The app lets a reader browse the public gallery. `src: Overview para 2`
- [ ] `C-OV-16` `capability` The app lets an author fork a readable preset. `src: Overview para 2`
- [ ] `C-OV-17` `data` The app records on a fork what that fork came from. `src: Overview para 2`
- [ ] `C-OV-18` `constraint` The app offers no comment surface. `src: Overview para 3`
- [ ] `C-OV-19` `constraint` The app offers no like surface. `src: Overview para 3`
- [ ] `C-OV-20` `constraint` The app offers no follow surface. `src: Overview para 3`
- [ ] `C-OV-21` `constraint` The app offers no messaging surface. `src: Overview para 3`
- [ ] `C-OV-22` `constraint` The app offers no payment surface. `src: Overview para 3`
- [ ] `C-OV-23` `constraint` The app sends no email. `src: Overview para 3`
- [ ] `C-OV-24` `contract` The app keeps a private preset unreachable by three separate routes. `src: Overview para 3`
- [ ] `C-OV-25` `contract` The app addresses a rendered export by the bytes of that export. `src: Overview para 3`
- [ ] `C-OV-26` `contract` The app stores one object for two renders producing identical bytes. `src: Overview para 3`

## C-RL User roles

- [ ] `C-RL-01` `role` A reader changes a control on any generator. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A reader copies the markup of a drawn graphic. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A reader downloads an export of a drawn graphic. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A reader browses the public gallery. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A reader opens a published gallery entry. `src: User roles table row 1`
- [ ] `C-RL-06` `role` A reader reads the lineage of a published entry. `src: User roles table row 1`
- [ ] `C-RL-07` `role` A reader opens an unlisted preset when holding the address of that preset. `src: User roles table row 1`
- [ ] `C-RL-08` `role` A reader reports a gallery entry. `src: User roles table row 1`
- [ ] `C-RL-09` `constraint` The app denies a reader request to save a preset. `src: User roles table row 1`
- [ ] `C-RL-10` `constraint` The app denies a reader request to render into the object store. `src: User roles table row 1`
- [ ] `C-RL-11` `constraint` The app denies a reader request to publish a preset. `src: User roles table row 1`
- [ ] `C-RL-12` `constraint` The app denies a reader request to fork a preset. `src: User roles table row 1`
- [ ] `C-RL-13` `constraint` The app keeps a private preset out of every listing a reader reads. `src: User roles table row 1`
- [ ] `C-RL-14` `constraint` The app denies a reader request for a private preset at the address of that preset. `src: User roles table row 1`
- [ ] `C-RL-15` `constraint` The app denies a reader request for the export of a private preset. `src: User roles table row 1`
- [ ] `C-RL-16` `role` An author saves the current settings as a named preset. `src: User roles table row 2`
- [ ] `C-RL-17` `role` An author renders an export of a readable preset. `src: User roles table row 2`
- [ ] `C-RL-18` `role` An author changes the visibility of a preset that author owns. `src: User roles table row 2`
- [ ] `C-RL-19` `role` An author publishes a preset that author owns. `src: User roles table row 2`
- [ ] `C-RL-20` `role` An author forks any preset that author can read. `src: User roles table row 2`
- [ ] `C-RL-21` `role` An author reads a list of the presets that author owns. `src: User roles table row 2`
- [ ] `C-RL-22` `constraint` The app denies an author request to edit a preset another account owns. `src: User roles table row 2`
- [ ] `C-RL-23` `constraint` The app denies an author request to publish a preset another account owns. `src: User roles table row 2`
- [ ] `C-RL-24` `constraint` The app denies an author request to delete a preset another account owns. `src: User roles table row 2`
- [ ] `C-RL-25` `constraint` The app denies an author request to change the visibility of a preset another account owns. `src: User roles table row 2`
- [ ] `C-RL-26` `constraint` The app refuses a request changing the derived address of a preset. `src: User roles table row 2`
- [ ] `C-RL-27` `contract` The app enforces authorization on the server for every mutating endpoint. `src: User roles para 3`
- [ ] `C-RL-28` `constraint` The app leaves protected state unchanged after a denied request. `src: User roles para 3`
- [ ] `C-RL-29` `constraint` The app offers no public signup. `src: User roles para 4`
- [ ] `C-RL-30` `constraint` The app offers no password reset. `src: User roles para 4`
- [ ] `C-RL-31` `constraint` The app offers no invitation flow. `src: User roles para 4`
- [ ] `C-RL-32` `literal` The app seeds the account `mara@vvvivid.tools` with the role `author`. `src: User roles table 2 row 1`
- [ ] `C-RL-33` `literal` The app seeds the account `tomas@vvvivid.tools` with the role `author`. `src: User roles table 2 row 2`
- [ ] `C-RL-34` `literal` The app seeds the account `visitor@vvvivid.tools` with the role `reader`. `src: User roles table 2 row 3`
- [ ] `C-RL-35` `literal` The app seeds the handle `mara`. `src: User roles table 2 row 1`
- [ ] `C-RL-36` `literal` The app seeds the handle `tomas`. `src: User roles table 2 row 2`
- [ ] `C-RL-37` `literal` The app seeds the handle `visitor`. `src: User roles table 2 row 3`
- [ ] `C-RL-38` `literal` The app seeds the display name Mara Okonkwo. `src: User roles table 2 row 1`
- [ ] `C-RL-39` `literal` The app seeds the display name Tomas Reinholt. `src: User roles table 2 row 2`
- [ ] `C-RL-40` `literal` The app seeds the display name Ines Haddad. `src: User roles table 2 row 3`
- [ ] `C-RL-41` `literal` The app accepts the password `deku-studio-2026` for every seeded account. `src: User roles para 5`

## C-CF Core features

- [ ] `C-CF-01` `contract` The app computes a preset identifier from the settings of that preset. `src: Core features, The derived address`
- [ ] `C-CF-02` `constraint` The app assigns no preset identifier. `src: Core features, The derived address`
- [ ] `C-CF-03` `contract` The app canonicalises the settings into one string before digesting. `src: Core features, The derived address`
- [ ] `C-CF-04` `literal` The app opens the canonical string with the generator key. `src: Core features, The derived address`
- [ ] `C-CF-05` `literal` The app follows the generator key with the generator version in the canonical string. `src: Core features, The derived address`
- [ ] `C-CF-06` `contract` The app writes every parameter into the canonical string as a key joined to a value. `src: Core features, The derived address`
- [ ] `C-CF-07` `contract` The app orders canonical parameters by the schema order of the generator. `src: Core features, The derived address`
- [ ] `C-CF-08` `constraint` The app omits no parameter from the canonical string. `src: Core features, The derived address`
- [ ] `C-CF-09` `constraint` The app writes a parameter equal to the default of that parameter into the canonical string. `src: Core features, The derived address`
- [ ] `C-CF-10` `contract` The app appends the seed to the canonical string after the parameters. `src: Core features, The derived address`
- [ ] `C-CF-11` `contract` The app appends the width to the canonical string after the seed. `src: Core features, The derived address`
- [ ] `C-CF-12` `contract` The app appends the height to the canonical string after the width. `src: Core features, The derived address`
- [ ] `C-CF-13` `literal` The app joins canonical fields with a single vertical bar. `src: Core features, The derived address`
- [ ] `C-CF-14` `constraint` The app puts no whitespace in the canonical string. `src: Core features, The derived address`
- [ ] `C-CF-15` `contract` The app writes a canonical number in plain decimal. `src: Core features, The derived address`
- [ ] `C-CF-16` `constraint` The app writes no trailing zero on a canonical number. `src: Core features, The derived address`
- [ ] `C-CF-17` `constraint` The app writes no exponent on a canonical number. `src: Core features, The derived address`
- [ ] `C-CF-18` `literal` The app digests the canonical string with SHA-256 over the UTF-8 bytes. `src: Core features, The derived address`
- [ ] `C-CF-19` `contract` The app encodes the digest in base32. `src: Core features, The derived address`
- [ ] `C-CF-20` `literal` The app encodes base32 with the lower-case alphabet running `a` to `z` then `2` to `7`. `src: Core features, The derived address`
- [ ] `C-CF-21` `constraint` The app removes base32 padding from the encoded digest. `src: Core features, The derived address`
- [ ] `C-CF-22` `literal` The app takes the leading `19` characters of the encoding as the identifier. `src: Core features, The derived address`
- [ ] `C-CF-23` `literal` The app derives the identifier `iiancd7svxmz3dbmqqk` from the worked canonical string. `src: Core features, The derived address`
- [ ] `C-CF-24` `capability` The app returns the derived identifier when settings are saved. `src: Core features, derived address rule 1`
- [ ] `C-CF-25` `contract` The app returns one identifier for a second save of one set of settings. `src: Core features, derived address rule 2`
- [ ] `C-CF-26` `contract` The app leaves one preset row after a second save of one set of settings. `src: Core features, derived address rule 2`
- [ ] `C-CF-27` `contract` The app leaves one preset row after two simultaneous saves of identical settings. `src: Core features, derived address rule 3`
- [ ] `C-CF-28` `contract` The app returns one identifier to both callers saving identical settings at one instant. `src: Core features, derived address rule 3`
- [ ] `C-CF-29` `contract` The app enforces the single preset row in the datastore. `src: Core features, derived address rule 3`
- [ ] `C-CF-30` `literal` The app rejects a canonical string longer than `8192` bytes as too large. `src: Core features, derived address rule 4`
- [ ] `C-CF-31` `constraint` The app stores nothing after rejecting an oversized canonical string. `src: Core features, derived address rule 4`
- [ ] `C-CF-32` `constraint` The app ignores a supplied preset identifier on a save request. `src: Core features, derived address rule 5`
- [ ] `C-CF-33` `literal` The app restricts a preset visibility to `private`, `unlisted`, `public`. `src: Core features, Visibility`
- [ ] `C-CF-34` `data` The app saves a new preset as `private` by default. `src: Core features, Visibility`
- [ ] `C-CF-35` `constraint` The app keeps a `private` preset out of the gallery. `src: Core features, visibility rule 1`
- [ ] `C-CF-36` `constraint` The app keeps a `private` preset out of every public listing. `src: Core features, visibility rule 1`
- [ ] `C-CF-37` `constraint` The app refuses a `private` preset address to a signed-out visitor as not found. `src: Core features, visibility rule 2`
- [ ] `C-CF-38` `constraint` The app refuses a `private` preset address to a reader as not found. `src: Core features, visibility rule 2`
- [ ] `C-CF-39` `constraint` The app refuses a `private` preset address to an author owning no part of that preset. `src: Core features, visibility rule 2`
- [ ] `C-CF-40` `constraint` The app makes a private refusal indistinguishable from an unknown identifier refusal. `src: Core features, visibility rule 2`
- [ ] `C-CF-41` `constraint` The app refuses the export of a `private` preset to a signed-out visitor. `src: Core features, visibility rule 3`
- [ ] `C-CF-42` `constraint` The app refuses the export of a `private` preset to a reader. `src: Core features, visibility rule 3`
- [ ] `C-CF-43` `constraint` The app refuses the export of a `private` preset to a non-owning author. `src: Core features, visibility rule 3`
- [ ] `C-CF-44` `capability` The app returns a `private` preset at the address of that preset to the owner. `src: Core features, visibility rule 4`
- [ ] `C-CF-45` `ui` The app lists a `private` preset in the list owned by the owner of that preset. `src: Core features, visibility rule 4`
- [ ] `C-CF-46` `capability` The app resolves an `unlisted` preset at the address of that preset for any caller. `src: Core features, visibility rule 5`
- [ ] `C-CF-47` `constraint` The app keeps an `unlisted` preset out of the gallery. `src: Core features, visibility rule 5`
- [ ] `C-CF-48` `constraint` The app keeps an `unlisted` preset out of search. `src: Core features, visibility rule 5`
- [ ] `C-CF-49` `ui` The app describes an unlisted address as shareable rather than as secret. `src: Core features, visibility rule 5`
- [ ] `C-CF-50` `capability` The app resolves a `public` preset for any caller. `src: Core features, visibility rule 6`
- [ ] `C-CF-51` `capability` The app shows a `public` preset in the gallery once published. `src: Core features, visibility rule 6`
- [ ] `C-CF-52` `constraint` The app denies a visibility change requested by an account owning no part of the preset. `src: Core features, visibility rule 7`
- [ ] `C-CF-53` `constraint` The app leaves the row unchanged after a denied visibility change. `src: Core features, visibility rule 7`
- [ ] `C-CF-54` `contract` The app writes a rendered export to the object store. `src: Core features, Rendered exports`
- [ ] `C-CF-55` `constraint` The app writes no rendered export to the datastore. `src: Core features, Rendered exports`
- [ ] `C-CF-56` `literal` The app writes a render to the bucket at `renders/{sha256_of_bytes}.{ext}`. `src: Core features, render rule 1`
- [ ] `C-CF-57` `contract` The app derives the render digest from the bytes of that object. `src: Core features, render rule 1`
- [ ] `C-CF-58` `literal` The app writes the render digest in lower-case hexadecimal. `src: Core features, render rule 1`
- [ ] `C-CF-59` `literal` The app accepts the render extension `svg`. `src: Core features, render rule 1`
- [ ] `C-CF-60` `literal` The app accepts the render extension `png`. `src: Core features, render rule 1`
- [ ] `C-CF-61` `constraint` The app derives an object key from no preset identifier. `src: Core features, render rule 2`
- [ ] `C-CF-62` `constraint` The app derives an object key from no account identifier. `src: Core features, render rule 2`
- [ ] `C-CF-63` `constraint` The app derives an object key from no timestamp. `src: Core features, render rule 2`
- [ ] `C-CF-64` `contract` The app stores one object for two presets rendering to identical bytes. `src: Core features, render rule 3`
- [ ] `C-CF-65` `data` The app references one shared key from both presets rendering to identical bytes. `src: Core features, render rule 3`
- [ ] `C-CF-66` `data` The app records the object key on a render row. `src: Core features, render rule 4`
- [ ] `C-CF-67` `data` The app records the format on a render row. `src: Core features, render rule 4`
- [ ] `C-CF-68` `data` The app records the dimensions on a render row. `src: Core features, render rule 4`
- [ ] `C-CF-69` `data` The app records the byte size on a render row. `src: Core features, render rule 4`
- [ ] `C-CF-70` `constraint` The app holds render bytes in no column of any table. `src: Core features, render rule 4`
- [ ] `C-CF-71` `literal` The app refuses a render larger than `4194304` bytes as too large. `src: Core features, render rule 5`
- [ ] `C-CF-72` `constraint` The app writes no object after refusing an oversized render. `src: Core features, render rule 5`
- [ ] `C-CF-73` `constraint` The app leaves existing renders untouched after refusing an oversized render. `src: Core features, render rule 5`
- [ ] `C-CF-74` `constraint` The app refuses a render format outside the two accepted formats. `src: Core features, render rule 6`
- [ ] `C-CF-75` `constraint` The app writes no object after refusing an unsupported render format. `src: Core features, render rule 6`
- [ ] `C-CF-76` `capability` The app serves the export of a published preset to any caller. `src: Core features, render rule 7`
- [ ] `C-CF-77` `constraint` The app denies a render of a preset another account owns. `src: Core features, render rule 8`
- [ ] `C-CF-78` `constraint` The app writes no object after denying a render on a non-owned preset. `src: Core features, render rule 8`
- [ ] `C-CF-79` `capability` The app forks any preset the requesting author can read. `src: Core features, fork rule 1`
- [ ] `C-CF-80` `ui` The app opens the generator carrying the settings of the parent after a fork. `src: Core features, fork rule 1`
- [ ] `C-CF-81` `capability` The app creates a new preset when a forked setting changes before a save. `src: Core features, fork rule 2`
- [ ] `C-CF-82` `data` The app names the original as the parent of a forked preset. `src: Core features, fork rule 2`
- [ ] `C-CF-83` `contract` The app returns the parent when a fork is saved with no setting changed. `src: Core features, fork rule 2`
- [ ] `C-CF-84` `constraint` The app creates no self-parented row from an unchanged fork. `src: Core features, fork rule 2`
- [ ] `C-CF-85` `data` The app records exactly one parent on a fork. `src: Core features, fork rule 3`
- [ ] `C-CF-86` `contract` The app raises the stored fork count of the parent by exactly one on a fork. `src: Core features, fork rule 3`
- [ ] `C-CF-87` `constraint` The app counts no fork total at read time. `src: Core features, fork rule 3`
- [ ] `C-CF-88` `capability` The app walks lineage toward ancestors for attribution. `src: Core features, fork rule 4`
- [ ] `C-CF-89` `capability` The app walks lineage toward descendants for the fork count. `src: Core features, fork rule 4`
- [ ] `C-CF-90` `literal` The app stops an ancestor walk at a depth of `64`. `src: Core features, fork rule 4`
- [ ] `C-CF-91` `contract` The app reports a stopped ancestor walk rather than truncating in silence. `src: Core features, fork rule 4`
- [ ] `C-CF-92` `constraint` The app orphans no fork when the parent of that fork is deleted. `src: Core features, fork rule 5`
- [ ] `C-CF-93` `data` The app retains the parameters of a tombstoned preset. `src: Core features, fork rule 5`
- [ ] `C-CF-94` `data` The app clears the title of a tombstoned preset. `src: Core features, fork rule 5`
- [ ] `C-CF-95` `data` The app clears the owner of a tombstoned preset. `src: Core features, fork rule 5`
- [ ] `C-CF-96` `literal` The app sets the state of a tombstoned preset to `tombstoned`. `src: Core features, fork rule 5`
- [ ] `C-CF-97` `capability` The app resolves the ancestry of a child through a tombstoned parent. `src: Core features, fork rule 5`
- [ ] `C-CF-98` `constraint` The app keeps a tombstoned preset out of the gallery. `src: Core features, fork rule 6`
- [ ] `C-CF-99` `constraint` The app keeps a tombstoned preset out of every listing. `src: Core features, fork rule 6`
- [ ] `C-CF-100` `ui` The app reports a tombstoned preset as withdrawn rather than as not found. `src: Core features, fork rule 6`
- [ ] `C-CF-101` `capability` The app sets a preset visibility to `public` on publication. `src: Core features, publication rule 1`
- [ ] `C-CF-102` `data` The app creates one gallery entry on publication. `src: Core features, publication rule 1`
- [ ] `C-CF-103` `constraint` The app refuses a publication carrying no account. `src: Core features, publication rule 2`
- [ ] `C-CF-104` `literal` The app requires a publication title between `1` characters long, `80` characters long. `src: Core features, publication rule 2`
- [ ] `C-CF-105` `literal` The app accepts at most `8` tags on a publication. `src: Core features, publication rule 2`
- [ ] `C-CF-106` `contract` The app returns the existing entry when an already published preset is published. `src: Core features, publication rule 3`
- [ ] `C-CF-107` `constraint` The app creates no second entry for an already published preset. `src: Core features, publication rule 3`
- [ ] `C-CF-108` `data` The app holds at most one gallery entry for one preset. `src: Core features, publication rule 3`
- [ ] `C-CF-109` `constraint` The app denies publication of a preset another account owns. `src: Core features, publication rule 4`
- [ ] `C-CF-110` `constraint` The app creates no entry after a denied publication. `src: Core features, publication rule 4`
- [ ] `C-CF-111` `capability` The app lists gallery entries whose state is `live`. `src: Core features, publication rule 5`
- [ ] `C-CF-112` `capability` The app orders the gallery by newest published moment first. `src: Core features, publication rule 5`
- [ ] `C-CF-113` `literal` The app keeps an entry whose state is `limited` reachable at the address of that entry. `src: Core features, publication rule 5`
- [ ] `C-CF-114` `constraint` The app keeps an entry whose state is `limited` out of the gallery listing. `src: Core features, publication rule 5`
- [ ] `C-CF-115` `literal` The app keeps an entry whose state is `removed` out of the gallery listing. `src: Core features, publication rule 5`
- [ ] `C-CF-116` `constraint` The app keeps an entry whose state is `removed` unreachable at the address of that entry. `src: Core features, publication rule 5`
- [ ] `C-CF-117` `capability` The app filters the gallery to one tool. `src: Core features, publication rule 6`
- [ ] `C-CF-118` `capability` The app holds the gallery order under a tool filter. `src: Core features, publication rule 6`
- [ ] `C-CF-119` `ui` The app displays the title on a gallery entry. `src: Core features, publication rule 7`
- [ ] `C-CF-120` `ui` The app displays the publisher handle on a gallery entry. `src: Core features, publication rule 7`
- [ ] `C-CF-121` `ui` The app displays the immediate parent on a gallery entry carrying one. `src: Core features, publication rule 7`
- [ ] `C-CF-122` `ui` The app displays the fork count on a gallery entry. `src: Core features, publication rule 7`
- [ ] `C-CF-123` `capability` The app reads tags back in the stored order of those tags. `src: Core features, publication rule 8`
- [ ] `C-CF-124` `capability` The app accepts a report from a signed-out visitor. `src: Core features, report rule 1`
- [ ] `C-CF-125` `literal` The app accepts the report reason `spam`. `src: Core features, report rule 1`
- [ ] `C-CF-126` `literal` The app accepts the report reason `infringement`. `src: Core features, report rule 1`
- [ ] `C-CF-127` `literal` The app accepts the report reason `offensive`. `src: Core features, report rule 1`
- [ ] `C-CF-128` `data` The app accepts an optional note on a report. `src: Core features, report rule 1`
- [ ] `C-CF-129` `constraint` The app rejects a report reason outside the accepted set as invalid. `src: Core features, report rule 2`
- [ ] `C-CF-130` `constraint` The app stores nothing after rejecting a report reason. `src: Core features, report rule 2`
- [ ] `C-CF-131` `capability` The app raises the report count of an entry on a report. `src: Core features, report rule 3`
- [ ] `C-CF-132` `constraint` The app changes no entry state from a report alone. `src: Core features, report rule 3`
- [ ] `C-CF-133` `constraint` The app exposes no report row through the public interface. `src: Core features, report rule 4`
- [ ] `C-CF-134` `data` The app seeds twenty-four tiles. `src: Core features, The tools`
- [ ] `C-CF-135` `data` The app carries three kinds of thing behind the tiles. `src: Core features, The tools`
- [ ] `C-CF-136` `contract` The app names a tool by an English word whose first letter repeats three times. `src: Core features, The tools`
- [ ] `C-CF-137` `ui` The app sets a tool name in lower case everywhere. `src: Core features, The tools`
- [ ] `C-CF-138` `ui` The app sets a tool name in lower case at the start of a sentence. `src: Core features, The tools`
- [ ] `C-CF-139` `ui` The app sets a tool name in lower case in the page title. `src: Core features, The tools`
- [ ] `C-CF-140` `literal` The app holds a tool name between `5` characters long, `13` characters long. `src: Core features, The tools`
- [ ] `C-CF-141` `ui` The app sets a document name in sentence case with a space. `src: Core features, The tools`
- [ ] `C-CF-142` `constraint` The app puts no category label on a tile. `src: Core features, The tools`
- [ ] `C-CF-143` `ui` The app carries a one-line description on a tile. `src: Core features, The tools`
- [ ] `C-CF-144` `contract` The app renders the tile grid from one stored list. `src: Core features, tools rule 1`
- [ ] `C-CF-145` `contract` The app repeats the tile grid on every route. `src: Core features, tools rule 1`
- [ ] `C-CF-146` `constraint` The app hand-authors no per-route tile grid. `src: Core features, tools rule 1`
- [ ] `C-CF-147` `contract` The app uses the tool name as the route slug of that tool. `src: Core features, tools rule 2`
- [ ] `C-CF-148` `constraint` The app carries no separate slug field. `src: Core features, tools rule 2`
- [ ] `C-CF-149` `capability` The app keeps the route of a retired generator resolving. `src: Core features, tools rule 3`
- [ ] `C-CF-150` `capability` The app keeps the schema of a retired generator. `src: Core features, tools rule 3`
- [ ] `C-CF-151` `capability` The app keeps the presets of a retired generator. `src: Core features, tools rule 3`
- [ ] `C-CF-152` `constraint` The app keeps a retired generator out of the tile grid. `src: Core features, tools rule 3`
- [ ] `C-CF-153` `literal` The app seeds `vvvanish` as the retired generator. `src: Core features, tools rule 3`
- [ ] `C-CF-154` `ui` The app carries a live preview on a generator route. `src: Core features, tools rule 4`
- [ ] `C-CF-155` `ui` The app carries the control panel on a generator route. `src: Core features, tools rule 4`
- [ ] `C-CF-156` `ui` The app carries the full tile grid beneath the content of a generator route. `src: Core features, tools rule 4`
- [ ] `C-CF-157` `contract` The app redraws the preview with no round trip when a control changes. `src: Core features, tools rule 5`
- [ ] `C-CF-158` `contract` The app renders a generator route with scripting unavailable. `src: Core features, tools rule 5`
- [ ] `C-CF-159` `contract` The app submits the controls with scripting unavailable. `src: Core features, tools rule 5`
- [ ] `C-CF-160` `contract` The app draws the preview on the server with scripting unavailable. `src: Core features, tools rule 5`
- [ ] `C-CF-161` `contract` The app produces one graphic from one set of settings in the browser, on the server. `src: Core features, tools rule 6`
- [ ] `C-CF-162` `literal` The app carries a parameter schema on `bbblob`. `src: Core features, tools rule 7`
- [ ] `C-CF-163` `literal` The app carries a parameter schema on `wwwave`. `src: Core features, tools rule 7`
- [ ] `C-CF-164` `literal` The app carries a parameter schema on `gggrid`. `src: Core features, tools rule 7`
- [ ] `C-CF-165` `literal` The app carries a parameter schema on `ffflow`. `src: Core features, tools rule 7`
- [ ] `C-CF-166` `literal` The app carries a parameter schema on `rrripple`. `src: Core features, tools rule 7`
- [ ] `C-CF-167` `literal` The app carries a parameter schema on `gggrit`. `src: Core features, tools rule 7`
- [ ] `C-CF-168` `data` The app orders a parameter schema as a list of descriptors. `src: Core features, tools rule 7`
- [ ] `C-CF-169` `data` The app names a key on a parameter descriptor. `src: Core features, tools rule 7`
- [ ] `C-CF-170` `data` The app names a label on a parameter descriptor. `src: Core features, tools rule 7`
- [ ] `C-CF-171` `data` The app names a kind on a parameter descriptor. `src: Core features, tools rule 7`
- [ ] `C-CF-172` `data` The app names a group on a parameter descriptor. `src: Core features, tools rule 7`
- [ ] `C-CF-173` `data` The app declares a range on a continuous parameter descriptor. `src: Core features, tools rule 7`
- [ ] `C-CF-174` `data` The app declares a step on a continuous parameter descriptor. `src: Core features, tools rule 7`
- [ ] `C-CF-175` `contract` The app walks the schema order when building the canonical string. `src: Core features, tools rule 7`
- [ ] `C-CF-176` `capability` The app serves a terms page stating what may be done with a generated graphic. `src: Core features, The public surface rule 1`
- [ ] `C-CF-177` `ui` The app reaches the terms page from the footer of every route. `src: Core features, The public surface rule 1`
- [ ] `C-CF-178` `ui` The app links the terms page from the publish surface. `src: Core features, The public surface rule 1`
- [ ] `C-CF-179` `contract` The app resolves every internal link on every public route. `src: Core features, The public surface rule 2`
- [ ] `C-CF-180` `constraint` The app leaves no link in the tile grid leading nowhere. `src: Core features, The public surface rule 2`
- [ ] `C-CF-181` `constraint` The app leaves no link in the rail leading nowhere. `src: Core features, The public surface rule 2`
- [ ] `C-CF-182` `constraint` The app leaves no link in a footer leading nowhere. `src: Core features, The public surface rule 2`
- [ ] `C-CF-183` `ui` The app asks a first-time visitor once about non-essential cookies. `src: Core features, The public surface rule 3`
- [ ] `C-CF-184` `capability` The app remembers the cookie answer across a reload. `src: Core features, The public surface rule 3`
- [ ] `C-CF-185` `constraint` The app asks a returning visitor no second time about cookies. `src: Core features, The public surface rule 3`
- [ ] `C-CF-186` `constraint` The app keeps every generator working after a declined cookie choice. `src: Core features, The public surface rule 3`
- [ ] `C-CF-187` `contract` The app rejects invalid input inline on every form. `src: Core features, The public surface rule 4`
- [ ] `C-CF-188` `ui` The app names the wrong field in words beside that field. `src: Core features, The public surface rule 4`
- [ ] `C-CF-189` `constraint` The app writes nothing after rejecting invalid form input. `src: Core features, The public surface rule 4`
- [ ] `C-CF-190` `contract` The app validates the sign-in form inline. `src: Core features, The public surface rule 4`
- [ ] `C-CF-191` `contract` The app validates the save form inline. `src: Core features, The public surface rule 4`
- [ ] `C-CF-192` `contract` The app validates the publish form inline. `src: Core features, The public surface rule 4`
- [ ] `C-CF-193` `contract` The app validates the report form inline. `src: Core features, The public surface rule 4`
- [ ] `C-CF-194` `capability` The app accepts an email address with a password at sign-in. `src: Core features, Auth`
- [ ] `C-CF-195` `literal` The app returns a sign-in token in the field `access_token`. `src: Core features, Auth`
- [ ] `C-CF-196` `contract` The app carries the token on every authenticated request. `src: Core features, Auth`
- [ ] `C-CF-197` `contract` The app stores every password hashed. `src: Core features, Auth`
- [ ] `C-CF-198` `constraint` The app returns no password from any endpoint. `src: Core features, Auth`
- [ ] `C-CF-199` `constraint` The app returns no password hash from any endpoint. `src: Core features, Auth`
- [ ] `C-CF-200` `literal` The app expires a token twenty-four hours after issue. `src: Core features, Auth`
- [ ] `C-CF-201` `constraint` The app denies a request carrying an expired token. `src: Core features, Auth`
- [ ] `C-CF-202` `constraint` The app denies a request carrying a malformed token. `src: Core features, Auth`
- [ ] `C-CF-203` `capability` The app grants a sign-in using a seeded email with `deku-studio-2026`. `src: Core features, Auth rule 1`
- [ ] `C-CF-204` `constraint` The app denies a sign-in using a seeded email with any other password. `src: Core features, Auth rule 2`
- [ ] `C-CF-205` `constraint` The app hides whether an email exists in a denied sign-in response. `src: Core features, Auth rule 2`
- [ ] `C-CF-206` `constraint` The app denies a sign-in using an unknown email. `src: Core features, Auth rule 3`
- [ ] `C-CF-207` `capability` The app returns the email of the current account from the session read. `src: Core features, Auth rule 4`
- [ ] `C-CF-208` `capability` The app returns the handle of the current account from the session read. `src: Core features, Auth rule 4`
- [ ] `C-CF-209` `capability` The app returns the display name of the current account from the session read. `src: Core features, Auth rule 4`
- [ ] `C-CF-210` `capability` The app returns the role of the current account from the session read. `src: Core features, Auth rule 4`
- [ ] `C-CF-211` `constraint` The app denies a session read carrying no token. `src: Core features, Auth rule 4`

## C-UF User flow

- [ ] `C-UF-01` `literal` The app serves the tile grid at `/`. `src: User flow route table`
- [ ] `C-UF-02` `literal` The app serves one generator at `/{tool}`. `src: User flow route table`
- [ ] `C-UF-03` `literal` The app serves the save surface at `/{tool}/save`. `src: User flow route table`
- [ ] `C-UF-04` `literal` The app serves one preset at `/p/{id}`. `src: User flow route table`
- [ ] `C-UF-05` `literal` The app serves the gallery at `/gallery`. `src: User flow route table`
- [ ] `C-UF-06` `literal` The app serves one gallery entry at `/gallery/{id}`. `src: User flow route table`
- [ ] `C-UF-07` `literal` The app serves the author preset list at `/studio`. `src: User flow route table`
- [ ] `C-UF-08` `literal` The app serves the publish surface at `/studio/presets/{id}/publish`. `src: User flow route table`
- [ ] `C-UF-09` `literal` The app serves the publish confirmation at `/studio/presets/{id}/published`. `src: User flow route table`
- [ ] `C-UF-10` `literal` The app serves sign-in at `/sign-in`. `src: User flow route table`
- [ ] `C-UF-11` `literal` The app serves the licence statement at `/license`. `src: User flow route table`
- [ ] `C-UF-12` `constraint` The app requires no sign-in on the tile grid route. `src: User flow route table`
- [ ] `C-UF-13` `constraint` The app requires no sign-in on a generator route. `src: User flow route table`
- [ ] `C-UF-14` `constraint` The app requires no sign-in on the gallery route. `src: User flow route table`
- [ ] `C-UF-15` `constraint` The app requires the author role on every studio route. `src: User flow route table`
- [ ] `C-UF-16` `constraint` The app requires the author role on the save route. `src: User flow route table`
- [ ] `C-UF-17` `capability` The app sends a signed-out visitor from a studio address to `/sign-in`. `src: User flow, Entry and redirects`
- [ ] `C-UF-18` `capability` The app sends a signed-out visitor from a save address to `/sign-in`. `src: User flow, Entry and redirects`
- [ ] `C-UF-19` `capability` The app returns a signed-in author to the address originally asked for. `src: User flow, Entry and redirects`
- [ ] `C-UF-20` `ui` The app refuses a reader at a studio address with a message naming accounts that save. `src: User flow, Entry and redirects`
- [ ] `C-UF-21` `constraint` The app leaves a signed-in reader off the sign-in surface after a refusal. `src: User flow, Entry and redirects`
- [ ] `C-UF-22` `ui` The app refuses an author at a publish address for a preset another account owns. `src: User flow, Entry and redirects`
- [ ] `C-UF-23` `capability` The app returns a visitor to `/` after signing out. `src: User flow, Entry and redirects`
- [ ] `C-UF-24` `capability` The app discards the token when a visitor signs out. `src: User flow, Entry and redirects`
- [ ] `C-UF-25` `ui` The app reports an ended session on the same surface when a token expires. `src: User flow, Entry and redirects`
- [ ] `C-UF-26` `ui` The app offers a sign-in control after a session ends. `src: User flow, Entry and redirects`
- [ ] `C-UF-27` `ui` The app keeps the settings in progress on screen after a session ends. `src: User flow, Entry and redirects`
- [ ] `C-UF-28` `capability` The app shows the seeded tiles in stored order at the grid route. `src: User flow journey 1`
- [ ] `C-UF-29` `ui` The app sets the seeded tile names in lower case. `src: User flow journey 1`
- [ ] `C-UF-30` `ui` The app draws the preview before any control moves. `src: User flow journey 1`
- [ ] `C-UF-31` `capability` The app redraws the preview as a control is dragged. `src: User flow journey 1`
- [ ] `C-UF-32` `ui` The app confirms the copy action in place. `src: User flow journey 1`
- [ ] `C-UF-33` `ui` The app repeats the full grid beneath the about block. `src: User flow journey 1`
- [ ] `C-UF-34` `ui` The app shows the derived address on the save route before a save happens. `src: User flow journey 2`
- [ ] `C-UF-35` `literal` The app accepts the preset title `Tight rule grid`. `src: User flow journey 2`
- [ ] `C-UF-36` `ui` The app marks a saved private preset as private in the author list. `src: User flow journey 2`
- [ ] `C-UF-37` `constraint` The app refuses a private preset address to a signed-out visitor as not found. `src: User flow journey 3`
- [ ] `C-UF-38` `constraint` The app refuses a private preset address to `visitor@vvvivid.tools` as not found. `src: User flow journey 3`
- [ ] `C-UF-39` `constraint` The app refuses a private preset address to `tomas@vvvivid.tools` as not found. `src: User flow journey 3`
- [ ] `C-UF-40` `capability` The app resolves a private preset address for the owner of that preset. `src: User flow journey 3`
- [ ] `C-UF-41` `ui` The app replaces the publish surface with a full-page confirmation. `src: User flow journey 4`
- [ ] `C-UF-42` `ui` The app names the entry address in the publish confirmation. `src: User flow journey 4`
- [ ] `C-UF-43` `capability` The app places a newly published entry first in the gallery. `src: User flow journey 4`
- [ ] `C-UF-44` `ui` The app opens the generator carrying the parent settings after a fork action. `src: User flow journey 5`
- [ ] `C-UF-45` `data` The app names the original as the parent of a preset saved from a fork. `src: User flow journey 5`
- [ ] `C-UF-46` `capability` The app raises the fork count of the original by one after a fork is saved. `src: User flow journey 5`
- [ ] `C-UF-47` `contract` The app returns one identifier when a second account reproduces saved settings. `src: User flow journey 6`
- [ ] `C-UF-48` `constraint` The app creates no second row when a second account reproduces saved settings. `src: User flow journey 6`
- [ ] `C-UF-49` `ui` The app states that no preset has been saved yet on an empty author list. `src: User flow, States`
- [ ] `C-UF-50` `ui` The app states that a filtered tool has nothing published yet on an empty gallery filter. `src: User flow, States`
- [ ] `C-UF-51` `ui` The app shows a fork count of zero on an entry carrying no fork. `src: User flow, States`
- [ ] `C-UF-52` `constraint` The app hides no fork count on an entry carrying no fork. `src: User flow, States`
- [ ] `C-UF-53` `ui` The app holds the final layout shape in every loading state. `src: User flow, States`
- [ ] `C-UF-54` `ui` The app shows a not-found page for an unresolved tool name. `src: User flow, States`
- [ ] `C-UF-55` `ui` The app shows a not-found page for an unresolved preset identifier. `src: User flow, States`
- [ ] `C-UF-56` `ui` The app offers a link home from the not-found page. `src: User flow, States`
- [ ] `C-UF-57` `ui` The app offers a link to the gallery from the not-found page. `src: User flow, States`
- [ ] `C-UF-58` `ui` The app shows a withdrawn page for a tombstoned preset. `src: User flow, States`
- [ ] `C-UF-59` `ui` The app names what failed after a failed request. `src: User flow, States`
- [ ] `C-UF-60` `ui` The app offers the action again after a failed request. `src: User flow, States`
- [ ] `C-UF-61` `constraint` The app leaves no route on a blank page. `src: User flow, States`
- [ ] `C-UF-62` `constraint` The app leaves no route on an unstyled error. `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `literal` The app carries the design direction `clinical-precision`. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The app reads as calibrated, neutral, medical-grade. `src: UI/UX notes para 1`
- [ ] `C-UX-03` `ui` The app carries one neutral sans with a monospace reserved for identifiers. `src: UI/UX notes para 1`
- [ ] `C-UX-04` `ui` The app carries the motion character eased. `src: UI/UX notes para 1`
- [ ] `C-UX-05` `ui` The app holds a comfortable density. `src: UI/UX notes para 1`
- [ ] `C-UX-06` `ui` The app lays a persistent rail beside a content column. `src: UI/UX notes para 1`
- [ ] `C-UX-07` `ui` The app holds everything except the graphic still in the first moment. `src: UI/UX notes, North star`
- [ ] `C-UX-08` `ui` The app reads as an instrument rather than as an editorial page. `src: UI/UX notes, Register`
- [ ] `C-UX-09` `ui` The app takes all colour in the product from the graphic. `src: UI/UX notes, Register`
- [ ] `C-UX-10` `ui` The app grounds the page in a very light neutral. `src: UI/UX notes, Ground`
- [ ] `C-UX-11` `ui` The app seats a panel on a slightly raised neutral. `src: UI/UX notes, Ground`
- [ ] `C-UX-12` `constraint` The app separates a panel from the ground without a border. `src: UI/UX notes, Ground`
- [ ] `C-UX-13` `constraint` The app separates a panel from the ground without a shadow. `src: UI/UX notes, Ground`
- [ ] `C-UX-14` `ui` The app seats the preview on a third surface distinct from the other two. `src: UI/UX notes, Ground`
- [ ] `C-UX-15` `ui` The app makes the preview surface the most neutral thing on the page. `src: UI/UX notes, Ground`
- [ ] `C-UX-16` `ui` The app shows a checkered indication where the graphic is transparent. `src: UI/UX notes, Ground`
- [ ] `C-UX-17` `constraint` The app allows a repeating pattern in the chrome only behind the transparent graphic. `src: UI/UX notes, Ground`
- [ ] `C-UX-18` `ui` The app marks the primary action with one accent. `src: UI/UX notes, Ground`
- [ ] `C-UX-19` `constraint` The app uses the primary accent nowhere else in the interface. `src: UI/UX notes, Ground`
- [ ] `C-UX-20` `ui` The app signals something that failed with one colour. `src: UI/UX notes, Ground`
- [ ] `C-UX-21` `ui` The app signals something in progress with one colour. `src: UI/UX notes, Ground`
- [ ] `C-UX-22` `ui` The app signals something private with one colour. `src: UI/UX notes, Ground`
- [ ] `C-UX-23` `constraint` The app borrows none of the four meanings on a surface that is none of them. `src: UI/UX notes, Ground`
- [ ] `C-UX-24` `constraint` The app tints no panel in a colour tool. `src: UI/UX notes, Ground`
- [ ] `C-UX-25` `ui` The app carries three levels of text presence. `src: UI/UX notes, Ground`
- [ ] `C-UX-26` `ui` The app carries the whole interface in one neutral sans. `src: UI/UX notes, Type`
- [ ] `C-UX-27` `ui` The app reserves the monospace for identifiers. `src: UI/UX notes, Type`
- [ ] `C-UX-28` `ui` The app reserves the monospace for values compared or copied. `src: UI/UX notes, Type`
- [ ] `C-UX-29` `constraint` The app sets nothing else in the monospace. `src: UI/UX notes, Type`
- [ ] `C-UX-30` `ui` The app aligns figures in a column wherever values stack. `src: UI/UX notes, Type`
- [ ] `C-UX-31` `ui` The app separates a heading from body copy at a glance. `src: UI/UX notes, Type`
- [ ] `C-UX-32` `ui` The app reports the current value on every control. `src: UI/UX notes, Calibration`
- [ ] `C-UX-33` `ui` The app sets a reported control value in the monospace face. `src: UI/UX notes, Calibration`
- [ ] `C-UX-34` `ui` The app holds a reported control value still as that value changes. `src: UI/UX notes, Calibration`
- [ ] `C-UX-35` `ui` The app groups controls under quiet headings. `src: UI/UX notes, Calibration`
- [ ] `C-UX-36` `ui` The app collapses a control group. `src: UI/UX notes, Calibration`
- [ ] `C-UX-37` `ui` The app shows the derived address on the save surface before anything is saved. `src: UI/UX notes, Calibration`
- [ ] `C-UX-38` `ui` The app labels the derived address as derived from the settings. `src: UI/UX notes, Calibration`
- [ ] `C-UX-39` `ui` The app moves everything at one shared speed. `src: UI/UX notes, Motion`
- [ ] `C-UX-40` `ui` The app moves everything on one shared easing. `src: UI/UX notes, Motion`
- [ ] `C-UX-41` `constraint` The app gives nothing a different speed to feel special. `src: UI/UX notes, Motion`
- [ ] `C-UX-42` `ui` The app redraws the preview on the frame after a control moves. `src: UI/UX notes, Motion`
- [ ] `C-UX-43` `constraint` The app animates no preview redraw. `src: UI/UX notes, Motion`
- [ ] `C-UX-44` `ui` The app lifts a tile toward the pointer, returns that tile on release. `src: UI/UX notes, Motion`
- [ ] `C-UX-45` `ui` The app eases the height of a panel that opens. `src: UI/UX notes, Motion`
- [ ] `C-UX-46` `ui` The app confirms the copy action by changing the label of that action. `src: UI/UX notes, Motion`
- [ ] `C-UX-47` `ui` The app holds a copy confirmation long enough to read. `src: UI/UX notes, Motion`
- [ ] `C-UX-48` `constraint` The app moves nothing else to announce a copy. `src: UI/UX notes, Motion`
- [ ] `C-UX-49` `ui` The app clears the WCAG AA contrast floor on body text against every ground. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-50` `ui` The app clears the WCAG AA contrast floor on every control label. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-51` `ui` The app clears the large-text contrast floor on large text. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-52` `ui` The app reaches every control by keyboard navigation in reading order. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-53` `ui` The app adjusts a slider by arrow key. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-54` `ui` The app reports a slider value as text rather than as position alone. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-55` `ui` The app shows a focus indicator visible against all three grounds. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-56` `ui` The app removes every transition for a reduced-motion reader. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-57` `ui` The app arrives everything in the final state for a reduced-motion reader. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-58` `constraint` The app signals unavailable by more than colour. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-59` `ui` The app carries a text description naming the tool on the graphic. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-60` `ui` The app carries the wordmark in the rail. `src: UI/UX notes, The rail`
- [ ] `C-UX-61` `ui` The app carries the tool groups in the rail. `src: UI/UX notes, The rail`
- [ ] `C-UX-62` `ui` The app carries the gallery link in the rail. `src: UI/UX notes, The rail`
- [ ] `C-UX-63` `ui` The app carries the author preset list in the rail when signed in. `src: UI/UX notes, The rail`
- [ ] `C-UX-64` `ui` The app carries the account handle in the rail when signed in. `src: UI/UX notes, The rail`
- [ ] `C-UX-65` `constraint` The app holds the rail still as the page scrolls. `src: UI/UX notes, The rail`
- [ ] `C-UX-66` `ui` The app collapses the rail to one control on a narrow viewport. `src: UI/UX notes, The rail`
- [ ] `C-UX-67` `ui` The app opens the collapsed rail as a full-height panel. `src: UI/UX notes, The rail`
- [ ] `C-UX-68` `ui` The app repeats the tile grid at the foot of every route. `src: UI/UX notes, The tile grid`
- [ ] `C-UX-69` `ui` The app carries the tool name on a tile card. `src: UI/UX notes, The tile grid`
- [ ] `C-UX-70` `ui` The app carries the one-line description on a tile card. `src: UI/UX notes, The tile grid`
- [ ] `C-UX-71` `constraint` The app carries nothing else on a tile card. `src: UI/UX notes, The tile grid`
- [ ] `C-UX-72` `ui` The app shows one tile column on a phone, two on a tablet, four on a wide screen. `src: UI/UX notes, The tile grid`
- [ ] `C-UX-73` `constraint` The app never collapses the gap between tiles. `src: UI/UX notes, The tile grid`
- [ ] `C-UX-74` `ui` The app makes the whole tile card the link target. `src: UI/UX notes, The tile grid`
- [ ] `C-UX-75` `ui` The app seats the preview above the controls at every width. `src: UI/UX notes, The generator route`
- [ ] `C-UX-76` `ui` The app keeps the copy action reachable at any scroll position. `src: UI/UX notes, The generator route`
- [ ] `C-UX-77` `ui` The app keeps the export action reachable at any scroll position. `src: UI/UX notes, The generator route`
- [ ] `C-UX-78` `ui` The app seats the about block beneath the tool. `src: UI/UX notes, The generator route`
- [ ] `C-UX-79` `ui` The app sets the save surface as a single column. `src: UI/UX notes, The save route`
- [ ] `C-UX-80` `ui` The app carries a title field on the save surface. `src: UI/UX notes, The save route`
- [ ] `C-UX-81` `ui` The app carries a visibility choice of three options on the save surface. `src: UI/UX notes, The save route`
- [ ] `C-UX-82` `ui` The app explains each visibility option in one line. `src: UI/UX notes, The save route`
- [ ] `C-UX-83` `ui` The app states that an unlisted address is shareable rather than secret. `src: UI/UX notes, The save route`
- [ ] `C-UX-84` `ui` The app shows a rendered thumbnail on a gallery entry card. `src: UI/UX notes, The gallery`
- [ ] `C-UX-85` `ui` The app shows the entry title on a gallery entry card. `src: UI/UX notes, The gallery`
- [ ] `C-UX-86` `ui` The app shows the publisher handle on a gallery entry card. `src: UI/UX notes, The gallery`
- [ ] `C-UX-87` `ui` The app shows the fork count on a gallery entry card. `src: UI/UX notes, The gallery`
- [ ] `C-UX-88` `ui` The app names the parent on a gallery entry carrying one. `src: UI/UX notes, The gallery`
- [ ] `C-UX-89` `ui` The app sets the tool filter as a row of tool names. `src: UI/UX notes, The gallery`
- [ ] `C-UX-90` `constraint` The app sets the tool filter as no dropdown. `src: UI/UX notes, The gallery`
- [ ] `C-UX-91` `ui` The app fills the viewport with the publish confirmation. `src: UI/UX notes, The publish confirmation`
- [ ] `C-UX-92` `ui` The app names the entry address in the publish confirmation. `src: UI/UX notes, The publish confirmation`
- [ ] `C-UX-93` `ui` The app states that publication is attributable in the confirmation. `src: UI/UX notes, The publish confirmation`
- [ ] `C-UX-94` `ui` The app states that publication is one-way in the confirmation. `src: UI/UX notes, The publish confirmation`
- [ ] `C-UX-95` `ui` The app offers the entry as a way onward from the confirmation. `src: UI/UX notes, The publish confirmation`
- [ ] `C-UX-96` `ui` The app offers the gallery as a way onward from the confirmation. `src: UI/UX notes, The publish confirmation`
- [ ] `C-UX-97` `constraint` The app leaves the publish confirmation on screen until the reader moves on. `src: UI/UX notes, The publish confirmation`
- [ ] `C-UX-98` `ui` The app carries one primary action style. `src: UI/UX notes, Components`
- [ ] `C-UX-99` `ui` The app carries one quieter alternative action style. `src: UI/UX notes, Components`
- [ ] `C-UX-100` `ui` The app gives the primary action the strongest contrast in the interface. `src: UI/UX notes, Components`
- [ ] `C-UX-101` `ui` The app gives every action resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes, Components`
- [ ] `C-UX-102` `ui` The app gives every field resting, focused, filled, invalid, disabled states. `src: UI/UX notes, Components`
- [ ] `C-UX-103` `ui` The app states in words beneath an invalid field what is wrong. `src: UI/UX notes, Components`
- [ ] `C-UX-104` `ui` The app holds the layout from a narrow phone viewport to a wide desktop viewport. `src: UI/UX notes, Responsive`
- [ ] `C-UX-105` `ui` The app holds the layout at every width between the breakpoints. `src: UI/UX notes, Responsive`
- [ ] `C-UX-106` `constraint` The app overflows nothing sideways at a narrow viewport. `src: UI/UX notes, Responsive`
- [ ] `C-UX-107` `constraint` The app scrolls no surface horizontally. `src: UI/UX notes, Responsive`
- [ ] `C-UX-108` `ui` The app scales the preview to the column at a narrow viewport. `src: UI/UX notes, Responsive`
- [ ] `C-UX-109` `ui` The app keeps every navigation target reachable at a narrow viewport. `src: UI/UX notes, Responsive`
- [ ] `C-UX-110` `ui` The app keeps every tile reachable at a narrow viewport. `src: UI/UX notes, Responsive`
- [ ] `C-UX-111` `constraint` The app hides no control on the narrow layout. `src: UI/UX notes, Responsive`
- [ ] `C-UX-112` `constraint` The app does not read as a marketing page. `src: UI/UX notes, What it must not look like`
- [ ] `C-UX-113` `constraint` The app keeps the chrome from competing with the output of that chrome. `src: UI/UX notes, What it must not look like`
- [ ] `C-UX-114` `constraint` The app puts no decoration in place of content. `src: UI/UX notes, What it must not look like`
- [ ] `C-UX-115` `constraint` The app borrows no layout from an unrelated subject. `src: UI/UX notes, What it must not look like`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app renders every route as a complete document from the server. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The app enhances the generator route on the client. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The app redraws the preview locally after a control change. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` The app works through ordinary form submission with scripting unavailable. `src: Technical requirements para 1`
- [ ] `C-TR-05` `literal` The app builds its frontend as vanilla progressive enhancement. `src: Technical requirements stack`
- [ ] `C-TR-06` `constraint` The app builds its frontend with no framework. `src: Technical requirements stack`
- [ ] `C-TR-07` `literal` The app builds its backend with Express. `src: Technical requirements stack`
- [ ] `C-TR-08` `literal` The app templates its documents with Nunjucks. `src: Technical requirements stack`
- [ ] `C-TR-09` `literal` The app serves its JSON API under the `/api` prefix on one origin. `src: Technical requirements stack`
- [ ] `C-TR-10` `literal` The app stores data in PostgreSQL reached through `DATABASE_URL`. `src: Technical requirements stack`
- [ ] `C-TR-11` `literal` The app stores objects in MinIO reached through `STORAGE_ENDPOINT`. `src: Technical requirements stack`
- [ ] `C-TR-12` `literal` The app reads the bucket name from `STORAGE_BUCKET`. `src: Technical requirements stack`
- [ ] `C-TR-13` `literal` The app reads the store key from `STORAGE_ACCESS_KEY`. `src: Technical requirements stack`
- [ ] `C-TR-14` `literal` The app reads the store secret from `STORAGE_SECRET_KEY`. `src: Technical requirements stack`
- [ ] `C-TR-15` `constraint` The app keeps the bucket private. `src: Technical requirements stack`
- [ ] `C-TR-16` `literal` The app reads its signing secret from `AUTH_SECRET`. `src: Technical requirements stack`
- [ ] `C-TR-17` `contract` The app loads one drawing core in the browser, on the server. `src: Technical requirements para 2`
- [ ] `C-TR-18` `literal` The app signs in at `POST /api/auth/login`. `src: Technical requirements API table`
- [ ] `C-TR-19` `literal` The app reads the current account at `GET /api/session`. `src: Technical requirements API table`
- [ ] `C-TR-20` `literal` The app reports readiness at `GET /api/health`. `src: Technical requirements API table`
- [ ] `C-TR-21` `literal` The app lists tiles at `GET /api/generators`. `src: Technical requirements API table`
- [ ] `C-TR-22` `literal` The app reads one generator at `GET /api/generators/{key}`. `src: Technical requirements API table`
- [ ] `C-TR-23` `literal` The app lists the gallery at `GET /api/gallery`. `src: Technical requirements API table`
- [ ] `C-TR-24` `literal` The app reads one entry at `GET /api/gallery/{presetId}`. `src: Technical requirements API table`
- [ ] `C-TR-25` `literal` The app reads one preset at `GET /api/presets/{id}`. `src: Technical requirements API table`
- [ ] `C-TR-26` `literal` The app streams an export at `GET /api/presets/{id}/render`. `src: Technical requirements API table`
- [ ] `C-TR-27` `literal` The app accepts a report at `POST /api/reports`. `src: Technical requirements API table`
- [ ] `C-TR-28` `literal` The app lists owned presets at `GET /api/studio/presets`. `src: Technical requirements API table`
- [ ] `C-TR-29` `literal` The app saves a preset at `POST /api/presets`. `src: Technical requirements API table`
- [ ] `C-TR-30` `literal` The app edits a preset at `PATCH /api/presets/{id}`. `src: Technical requirements API table`
- [ ] `C-TR-31` `literal` The app tombstones a preset at `DELETE /api/presets/{id}`. `src: Technical requirements API table`
- [ ] `C-TR-32` `literal` The app renders a preset at `POST /api/presets/{id}/render`. `src: Technical requirements API table`
- [ ] `C-TR-33` `literal` The app forks a preset at `POST /api/presets/{id}/fork`. `src: Technical requirements API table`
- [ ] `C-TR-34` `literal` The app publishes a preset at `POST /api/presets/{id}/publish`. `src: Technical requirements API table`
- [ ] `C-TR-35` `literal` The app reports a read with `200`. `src: Technical requirements outcomes`
- [ ] `C-TR-36` `literal` The app reports a creation with `201`. `src: Technical requirements outcomes`
- [ ] `C-TR-37` `literal` The app reports a malformed body with `400`. `src: Technical requirements outcomes`
- [ ] `C-TR-38` `literal` The app reports a missing token with `401`. `src: Technical requirements outcomes`
- [ ] `C-TR-39` `literal` The app reports an unentitled caller with `403`. `src: Technical requirements outcomes`
- [ ] `C-TR-40` `literal` The app reports an invisible identifier with `404`. `src: Technical requirements outcomes`
- [ ] `C-TR-41` `literal` The app reports a conflict with `409`. `src: Technical requirements outcomes`
- [ ] `C-TR-42` `literal` The app reports a payload above the cap with `413`. `src: Technical requirements outcomes`
- [ ] `C-TR-43` `literal` The app reports an unsupported format with `415`. `src: Technical requirements outcomes`
- [ ] `C-TR-44` `constraint` The app returns `404` alone for a preset the caller may not see. `src: Technical requirements outcomes`
- [ ] `C-TR-45` `literal` The app serves a production build on port `4173`. `src: Technical requirements para last`
- [ ] `C-TR-46` `literal` The app binds `0.0.0.0`. `src: Technical requirements para last`
- [ ] `C-TR-47` `constraint` The app installs every dependency at image build time. `src: Technical requirements para last`

## C-DM Data model

- [ ] `C-DM-01` `data` The app defines seven tables. `src: Data model para 1`
- [ ] `C-DM-02` `contract` The app stores every timestamp in UTC. `src: Data model para 1`
- [ ] `C-DM-03` `contract` The app gives every table its own `id`. `src: Data model para 1`
- [ ] `C-DM-04` `data` The app stores an account email, handle, display name, password hash, creation moment. `src: Data model, accounts`
- [ ] `C-DM-05` `data` The app keeps an account email unique. `src: Data model, accounts`
- [ ] `C-DM-06` `data` The app keeps an account handle unique. `src: Data model, accounts`
- [ ] `C-DM-07` `literal` The app restricts an account role to `author` or `reader`. `src: Data model, accounts`
- [ ] `C-DM-08` `data` The app seeds three accounts. `src: Data model, accounts`
- [ ] `C-DM-09` `data` The app stores a generator key, title, blurb, position, creation moment. `src: Data model, generators`
- [ ] `C-DM-10` `literal` The app restricts a generator kind to `generator`, `colour`, `document`. `src: Data model, generators`
- [ ] `C-DM-11` `literal` The app restricts a generator status to `live` or `retired`. `src: Data model, generators`
- [ ] `C-DM-12` `data` The app keeps a generator key unique. `src: Data model, generators`
- [ ] `C-DM-13` `data` The app seeds twenty-four generator rows as read-only. `src: Data model, generators`
- [ ] `C-DM-14` `literal` The app seeds the tile `pppick` as a `colour` tool. `src: Data model, generators table row 1`
- [ ] `C-DM-15` `literal` The app seeds the tile `mmmingle` as a `colour` tool. `src: Data model, generators table row 2`
- [ ] `C-DM-16` `literal` The app seeds the tile `bbblob` describing SVG blobs. `src: Data model, generators table row 3`
- [ ] `C-DM-17` `literal` The app seeds the tile `wwwave` describing a SVG wave generator. `src: Data model, generators table row 4`
- [ ] `C-DM-18` `literal` The app seeds the tile `gggrid` describing SVG grid patterns. `src: Data model, generators table row 5`
- [ ] `C-DM-19` `literal` The app seeds the tile `ffflow` describing fluid SVG gradients. `src: Data model, generators table row 6`
- [ ] `C-DM-20` `literal` The app seeds the tile `rrripple` describing SVG ripples. `src: Data model, generators table row 7`
- [ ] `C-DM-21` `literal` The app seeds the tile `gggrit` describing a noise texture generator. `src: Data model, generators table row 8`
- [ ] `C-DM-22` `literal` The app seeds the document tile `Style Selectors`. `src: Data model, generators table row 9`
- [ ] `C-DM-23` `literal` The app seeds the document tile `Vector Spinners`. `src: Data model, generators table row 10`
- [ ] `C-DM-24` `literal` The app seeds the tile `tttile`. `src: Data model, generators table row 11`
- [ ] `C-DM-25` `literal` The app seeds the tile `aaambient`. `src: Data model, generators table row 12`
- [ ] `C-DM-26` `literal` The app seeds the tile `iiisogrid`. `src: Data model, generators table row 13`
- [ ] `C-DM-27` `literal` The app seeds the tile `ggglow`. `src: Data model, generators table row 14`
- [ ] `C-DM-28` `literal` The app seeds the tile `qqquilt`. `src: Data model, generators table row 15`
- [ ] `C-DM-29` `literal` The app seeds the tile `mmmesh`. `src: Data model, generators table row 16`
- [ ] `C-DM-30` `literal` The app seeds the tile `cccurve`. `src: Data model, generators table row 17`
- [ ] `C-DM-31` `literal` The app seeds the tile `hhhelix`. `src: Data model, generators table row 18`
- [ ] `C-DM-32` `literal` The app seeds the tile `ooorbit`. `src: Data model, generators table row 19`
- [ ] `C-DM-33` `literal` The app seeds the tile `bbbeam`. `src: Data model, generators table row 20`
- [ ] `C-DM-34` `literal` The app seeds the tile `mmmaze`. `src: Data model, generators table row 21`
- [ ] `C-DM-35` `literal` The app seeds the tile `ssspark`. `src: Data model, generators table row 22`
- [ ] `C-DM-36` `literal` The app seeds the tile `cccheer`. `src: Data model, generators table row 23`
- [ ] `C-DM-37` `literal` The app seeds the parameter keys `complexity`, `contrast`, `edges`, `fill` on `bbblob`. `src: Data model, parameter table`
- [ ] `C-DM-38` `literal` The app seeds the parameter keys `amplitude`, `frequency`, `layers` on `wwwave`. `src: Data model, parameter table`
- [ ] `C-DM-39` `literal` The app seeds the parameter keys `columns`, `rows`, `thickness`, `stroke` on `gggrid`. `src: Data model, parameter table`
- [ ] `C-DM-40` `literal` The app seeds the parameter keys `stops`, `angle`, `blur`, `palette` on `ffflow`. `src: Data model, parameter table`
- [ ] `C-DM-41` `literal` The app seeds the parameter keys `rings`, `spacing`, `falloff` on `rrripple`. `src: Data model, parameter table`
- [ ] `C-DM-42` `literal` The app seeds the parameter keys `density`, `scale`, `opacity`, `tint` on `gggrit`. `src: Data model, parameter table`
- [ ] `C-DM-43` `data` The app stores a preset generator key, generator version, params, seed. `src: Data model, presets`
- [ ] `C-DM-44` `data` The app stores a preset ratio, width, height. `src: Data model, presets`
- [ ] `C-DM-45` `data` The app stores a nullable title on a preset. `src: Data model, presets`
- [ ] `C-DM-46` `data` The app references the owning account from a preset. `src: Data model, presets`
- [ ] `C-DM-47` `data` The app references a nullable parent preset from a preset. `src: Data model, presets`
- [ ] `C-DM-48` `literal` The app restricts a preset state to `live` or `tombstoned`. `src: Data model, presets`
- [ ] `C-DM-49` `data` The app stores a fork count on a preset. `src: Data model, presets`
- [ ] `C-DM-50` `literal` The app holds a preset identifier at `19` characters. `src: Data model, presets`
- [ ] `C-DM-51` `data` The app seeds four presets. `src: Data model, presets`
- [ ] `C-DM-52` `literal` The app seeds the public preset `Soft four-lobe` on `bbblob`. `src: Data model, presets`
- [ ] `C-DM-53` `literal` The app seeds the public preset `Three-layer crest` on `wwwave`. `src: Data model, presets`
- [ ] `C-DM-54` `literal` The app seeds the unlisted preset `Tight rule grid` on `gggrid`. `src: Data model, presets`
- [ ] `C-DM-55` `literal` The app seeds the private preset `Dawn wash` on `ffflow`. `src: Data model, presets`
- [ ] `C-DM-56` `contract` The app derives every seeded preset identifier from the settings of that row. `src: Data model, presets`
- [ ] `C-DM-57` `data` The app stores a render object key, format, width, height, byte size, creation moment. `src: Data model, renders`
- [ ] `C-DM-58` `data` The app references the preset from a render row. `src: Data model, renders`
- [ ] `C-DM-59` `data` The app keeps a gallery entry preset reference unique. `src: Data model, gallery_entries`
- [ ] `C-DM-60` `data` The app stores a gallery entry publisher, published moment, title, report count. `src: Data model, gallery_entries`
- [ ] `C-DM-61` `data` The app stores a nullable thumbnail object key on a gallery entry. `src: Data model, gallery_entries`
- [ ] `C-DM-62` `literal` The app restricts a gallery entry state to `live`, `limited`, `removed`. `src: Data model, gallery_entries`
- [ ] `C-DM-63` `data` The app seeds two live gallery entries. `src: Data model, gallery_entries`
- [ ] `C-DM-64` `data` The app stores a tag, a position on a gallery entry tag row. `src: Data model, gallery_entry_tags`
- [ ] `C-DM-65` `capability` The app reads gallery entry tags back in position order. `src: Data model, gallery_entry_tags`
- [ ] `C-DM-66` `literal` The app holds at most `8` tag rows per gallery entry. `src: Data model, gallery_entry_tags`
- [ ] `C-DM-67` `data` The app stores a report reason, a nullable note, a creation moment. `src: Data model, reports`
- [ ] `C-DM-68` `data` The app references a nullable reporter account from a report. `src: Data model, reports`
- [ ] `C-DM-69` `data` The app seeds no report. `src: Data model, reports`
- [ ] `C-DM-70` `contract` The app makes a preset identifier equal the derivation of the settings of that preset. `src: Data model, invariants`
- [ ] `C-DM-71` `contract` The app leaves one row after two identical saves whatever order those saves arrive in. `src: Data model, invariants`
- [ ] `C-DM-72` `contract` The app keeps a generator key unique across the catalogue. `src: Data model, invariants`
- [ ] `C-DM-73` `contract` The app holds at most one gallery entry for one preset. `src: Data model, invariants`
- [ ] `C-DM-74` `contract` The app makes an object key the digest of the bytes of that object. `src: Data model, invariants`
- [ ] `C-DM-75` `contract` The app names an object that exists in the bucket from a stored object key. `src: Data model, invariants`
- [ ] `C-DM-76` `contract` The app retains the parameters of a tombstoned preset carrying forks. `src: Data model, invariants`
- [ ] `C-DM-77` `contract` The app retains the parent link of a tombstoned preset. `src: Data model, invariants`
- [ ] `C-DM-78` `contract` The app equals a preset fork count to the number of live presets naming that preset as parent. `src: Data model, invariants`
- [ ] `C-DM-79` `constraint` The app holds image bytes in no column of any table. `src: Data model, invariants`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app serves one catalogue of tools. `src: Constraints`
- [ ] `C-CN-02` `constraint` The app serves one gallery. `src: Constraints`
- [ ] `C-CN-03` `constraint` The app offers no account deletion. `src: Constraints`
- [ ] `C-CN-04` `constraint` The app offers no social graph. `src: Constraints`
- [ ] `C-CN-05` `constraint` The app offers no near-duplicate clustering. `src: Constraints`
- [ ] `C-CN-06` `constraint` The app offers no ranking figure. `src: Constraints`
- [ ] `C-CN-07` `constraint` The app offers no account standing. `src: Constraints`
- [ ] `C-CN-08` `constraint` The app offers no real-time collaboration. `src: Constraints`
- [ ] `C-CN-09` `constraint` The app offers no shared editing session. `src: Constraints`
- [ ] `C-CN-10` `constraint` The app offers no public generation API. `src: Constraints`
- [ ] `C-CN-11` `constraint` The app offers no API keys. `src: Constraints`
- [ ] `C-CN-12` `constraint` The app offers no quotas. `src: Constraints`
- [ ] `C-CN-13` `constraint` The app offers no metering. `src: Constraints`
- [ ] `C-CN-14` `constraint` The app offers no workspaces. `src: Constraints`
- [ ] `C-CN-15` `constraint` The app offers no team membership. `src: Constraints`
- [ ] `C-CN-16` `constraint` The app owns a preset by one account. `src: Constraints`
- [ ] `C-CN-17` `constraint` The app offers no collections. `src: Constraints`
- [ ] `C-CN-18` `constraint` The app offers no curated feed. `src: Constraints`
- [ ] `C-CN-19` `constraint` The app offers no moderation queue. `src: Constraints`
- [ ] `C-CN-20` `constraint` The app offers no review decision. `src: Constraints`
- [ ] `C-CN-21` `constraint` The app offers no print-resolution rendering. `src: Constraints`
- [ ] `C-CN-22` `constraint` The app offers no colour vision simulation. `src: Constraints`
- [ ] `C-CN-23` `constraint` The app offers no print gamut work. `src: Constraints`
- [ ] `C-CN-24` `constraint` The app accepts no upload of any kind. `src: Constraints`
- [ ] `C-CN-25` `constraint` The app generates every graphic from parameters. `src: Constraints`
- [ ] `C-CN-26` `constraint` The app renders no format outside the two accepted formats. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `literal` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-02` `literal` The app maps `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract`
- [ ] `C-DC-03` `literal` The app listens on container-internal port `4173`. `src: Deployment contract`
- [ ] `C-DC-04` `constraint` The app reads both port values from the environment. `src: Deployment contract`
- [ ] `C-DC-05` `constraint` The app hardcodes neither port value. `src: Deployment contract`
- [ ] `C-DC-06` `literal` The app serves its HTTP API under the `/api` prefix on the same origin. `src: Deployment contract`
- [ ] `C-DC-07` `literal` The app returns `200` from `GET /api/health` once ready. `src: Deployment contract`
- [ ] `C-DC-08` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-09` `literal` The app writes login credentials to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-10` `literal` The app creates an empty `.browser_screenshots/` directory at the app root. `src: Deployment contract`
- [ ] `C-DC-11` `literal` The app creates an empty `.downloads/` directory at the app root. `src: Deployment contract`
- [ ] `C-DC-12` `contract` The app serves a production build behind a static or preview server. `src: Deployment contract`
- [ ] `C-DC-13` `constraint` The app serves no dev server. `src: Deployment contract`
- [ ] `C-DC-14` `contract` The app keeps the server running after the session ends. `src: Deployment contract`
- [ ] `C-DC-15` `constraint` The app keeps the server off the shell process tree. `src: Deployment contract`
- [ ] `C-DC-16` `literal` The app binds `0.0.0.0`. `src: Deployment contract`
- [ ] `C-DC-17` `literal` The app binds neither `127.0.0.1` nor `localhost`. `src: Deployment contract`
- [ ] `C-DC-18` `constraint` The app starts no copy of a backing service. `src: Deployment contract`
- [ ] `C-DC-19` `constraint` The app uses only the providers named in the brief. `src: Deployment contract`
- [ ] `C-DC-20` `constraint` The app uses no edge functions. `src: Deployment contract`
- [ ] `C-DC-21` `constraint` The app uses no persistent volume. `src: Deployment contract`
- [ ] `C-DC-22` `constraint` The app uses no fixed container name. `src: Deployment contract`
- [ ] `C-DC-23` `constraint` The app uses no custom network. `src: Deployment contract`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `mara@vvvivid.tools` | seeded author account | C-RL-32 | User roles |
| `author` | write role | C-RL-32 | User roles |
| `tomas@vvvivid.tools` | seeded author account | C-RL-33 | User roles |
| `visitor@vvvivid.tools` | seeded reader account | C-RL-34 | User roles |
| `reader` | read role | C-RL-34 | User roles |
| `mara` | seeded author handle | C-RL-35 | User roles |
| `tomas` | seeded author handle | C-RL-36 | User roles |
| `visitor` | seeded reader handle | C-RL-37 | User roles |
| `deku-studio-2026` | corpus password | C-RL-41 | User roles |
| `a` | base32 alphabet start | C-CF-20 | Core features |
| `z` | base32 alphabet letter end | C-CF-20 | Core features |
| `2` | base32 digit start | C-CF-20 | Core features |
| `7` | base32 digit end | C-CF-20 | Core features |
| `19` | preset identifier length | C-CF-22 | Core features |
| `iiancd7svxmz3dbmqqk` | worked example identifier | C-CF-23 | Core features |
| `8192` | canonical string cap in bytes | C-CF-30 | Core features |
| `private` | preset visibility | C-CF-33 | Core features |
| `unlisted` | preset visibility | C-CF-33 | Core features |
| `public` | preset visibility | C-CF-33 | Core features |
| `renders/{sha256_of_bytes}.{ext}` | object key scheme | C-CF-56 | Core features |
| `svg` | render format | C-CF-59 | Core features |
| `png` | render format | C-CF-60 | Core features |
| `4194304` | render cap in bytes | C-CF-71 | Core features |
| `64` | ancestor walk depth cap | C-CF-90 | Core features |
| `tombstoned` | preset state | C-CF-96 | Core features |
| `1` | shortest publication title | C-CF-104 | Core features |
| `80` | longest publication title | C-CF-104 | Core features |
| `8` | tag cap per entry | C-CF-105 | Core features |
| `limited` | gallery entry state | C-CF-113 | Core features |
| `removed` | gallery entry state | C-CF-115 | Core features |
| `spam` | report reason | C-CF-125 | Core features |
| `infringement` | report reason | C-CF-126 | Core features |
| `offensive` | report reason | C-CF-127 | Core features |
| `5` | shortest tool name | C-CF-140 | Core features |
| `13` | longest tool name | C-CF-140 | Core features |
| `vvvanish` | seeded retired generator | C-CF-153 | Core features |
| `bbblob` | seeded tile name | C-CF-162 | Core features |
| `wwwave` | seeded tile name | C-CF-163 | Core features |
| `gggrid` | seeded tile name | C-CF-164 | Core features |
| `ffflow` | seeded tile name | C-CF-165 | Core features |
| `rrripple` | seeded tile name | C-CF-166 | Core features |
| `gggrit` | seeded tile name | C-CF-167 | Core features |
| `access_token` | sign-in token field | C-CF-195 | Core features |
| `/` | route | C-UF-01 | User flow |
| `/{tool}` | route | C-UF-02 | User flow |
| `/{tool}/save` | route | C-UF-03 | User flow |
| `/p/{id}` | route | C-UF-04 | User flow |
| `/gallery` | route | C-UF-05 | User flow |
| `/gallery/{id}` | route | C-UF-06 | User flow |
| `/studio` | route | C-UF-07 | User flow |
| `/studio/presets/{id}/publish` | route | C-UF-08 | User flow |
| `/studio/presets/{id}/published` | route | C-UF-09 | User flow |
| `/sign-in` | route | C-UF-10 | User flow |
| `/license` | route | C-UF-11 | User flow |
| `Tight rule grid` | seeded unlisted preset | C-UF-35 | User flow |
| `clinical-precision` | design direction | C-UX-01 | UI and UX notes |
| `/api` | API prefix | C-TR-09 | Technical requirements |
| `DATABASE_URL` | datastore variable | C-TR-10 | Technical requirements |
| `STORAGE_ENDPOINT` | object store variable | C-TR-11 | Technical requirements |
| `STORAGE_BUCKET` | bucket variable | C-TR-12 | Technical requirements |
| `STORAGE_ACCESS_KEY` | store key variable | C-TR-13 | Technical requirements |
| `STORAGE_SECRET_KEY` | store secret variable | C-TR-14 | Technical requirements |
| `AUTH_SECRET` | signing secret variable | C-TR-16 | Technical requirements |
| `POST /api/auth/login` | API endpoint | C-TR-18 | Technical requirements |
| `GET /api/session` | API endpoint | C-TR-19 | Technical requirements |
| `GET /api/health` | API endpoint | C-TR-20 | Technical requirements |
| `GET /api/generators` | API endpoint | C-TR-21 | Technical requirements |
| `GET /api/generators/{key}` | API endpoint | C-TR-22 | Technical requirements |
| `GET /api/gallery` | API endpoint | C-TR-23 | Technical requirements |
| `GET /api/gallery/{presetId}` | API endpoint | C-TR-24 | Technical requirements |
| `GET /api/presets/{id}` | API endpoint | C-TR-25 | Technical requirements |
| `GET /api/presets/{id}/render` | API endpoint | C-TR-26 | Technical requirements |
| `POST /api/reports` | API endpoint | C-TR-27 | Technical requirements |
| `GET /api/studio/presets` | API endpoint | C-TR-28 | Technical requirements |
| `POST /api/presets` | API endpoint | C-TR-29 | Technical requirements |
| `PATCH /api/presets/{id}` | API endpoint | C-TR-30 | Technical requirements |
| `DELETE /api/presets/{id}` | API endpoint | C-TR-31 | Technical requirements |
| `POST /api/presets/{id}/render` | API endpoint | C-TR-32 | Technical requirements |
| `POST /api/presets/{id}/fork` | API endpoint | C-TR-33 | Technical requirements |
| `POST /api/presets/{id}/publish` | API endpoint | C-TR-34 | Technical requirements |
| `200` | read status | C-TR-35 | Technical requirements |
| `201` | creation status | C-TR-36 | Technical requirements |
| `400` | invalid status | C-TR-37 | Technical requirements |
| `401` | unauthenticated status | C-TR-38 | Technical requirements |
| `403` | unentitled status | C-TR-39 | Technical requirements |
| `404` | invisible status | C-TR-40 | Technical requirements |
| `409` | conflict status | C-TR-41 | Technical requirements |
| `413` | oversize status | C-TR-42 | Technical requirements |
| `415` | unsupported format status | C-TR-43 | Technical requirements |
| `4173` | container internal port | C-TR-45 | Technical requirements |
| `0.0.0.0` | bind address | C-TR-46 | Technical requirements |
| `generator` | tile kind | C-DM-10 | Data model |
| `colour` | tile kind | C-DM-10 | Data model |
| `document` | tile kind | C-DM-10 | Data model |
| `live` | row state | C-DM-11 | Data model |
| `retired` | generator status | C-DM-11 | Data model |
| `pppick` | seeded tile name | C-DM-14 | Data model |
| `mmmingle` | seeded tile name | C-DM-15 | Data model |
| `Style Selectors` | seeded document tile | C-DM-22 | Data model |
| `Vector Spinners` | seeded document tile | C-DM-23 | Data model |
| `tttile` | seeded tile name | C-DM-24 | Data model |
| `aaambient` | seeded tile name | C-DM-25 | Data model |
| `iiisogrid` | seeded tile name | C-DM-26 | Data model |
| `ggglow` | seeded tile name | C-DM-27 | Data model |
| `qqquilt` | seeded tile name | C-DM-28 | Data model |
| `mmmesh` | seeded tile name | C-DM-29 | Data model |
| `cccurve` | seeded tile name | C-DM-30 | Data model |
| `hhhelix` | seeded tile name | C-DM-31 | Data model |
| `ooorbit` | seeded tile name | C-DM-32 | Data model |
| `bbbeam` | seeded tile name | C-DM-33 | Data model |
| `mmmaze` | seeded tile name | C-DM-34 | Data model |
| `ssspark` | seeded tile name | C-DM-35 | Data model |
| `cccheer` | seeded tile name | C-DM-36 | Data model |
| `complexity` | seeded tile name | C-DM-37 | Data model |
| `contrast` | seeded tile name | C-DM-37 | Data model |
| `edges` | seeded tile name | C-DM-37 | Data model |
| `fill` | seeded tile name | C-DM-37 | Data model |
| `amplitude` | seeded tile name | C-DM-38 | Data model |
| `frequency` | seeded tile name | C-DM-38 | Data model |
| `layers` | seeded tile name | C-DM-38 | Data model |
| `columns` | seeded tile name | C-DM-39 | Data model |
| `rows` | seeded tile name | C-DM-39 | Data model |
| `thickness` | seeded tile name | C-DM-39 | Data model |
| `stroke` | seeded tile name | C-DM-39 | Data model |
| `stops` | seeded tile name | C-DM-40 | Data model |
| `angle` | seeded tile name | C-DM-40 | Data model |
| `blur` | seeded tile name | C-DM-40 | Data model |
| `palette` | seeded tile name | C-DM-40 | Data model |
| `rings` | seeded tile name | C-DM-41 | Data model |
| `spacing` | seeded tile name | C-DM-41 | Data model |
| `falloff` | seeded tile name | C-DM-41 | Data model |
| `density` | seeded tile name | C-DM-42 | Data model |
| `scale` | seeded tile name | C-DM-42 | Data model |
| `opacity` | seeded tile name | C-DM-42 | Data model |
| `tint` | seeded tile name | C-DM-42 | Data model |
| `Soft four-lobe` | seeded public preset | C-DM-52 | Data model |
| `Three-layer crest` | seeded public preset | C-DM-53 | Data model |
| `Dawn wash` | seeded private preset | C-DM-55 | Data model |
| `APP_PUBLIC_URL` | public address variable | C-DC-01 | Deployment contract |
| `${APP_PUBLIC_PORT}:4173` | port mapping | C-DC-02 | Deployment contract |
| `/app/USER_README.md` | credentials file path | C-DC-09 | Deployment contract |
| `.browser_screenshots/` | reserved directory | C-DC-10 | Deployment contract |
| `.downloads/` | reserved directory | C-DC-11 | Deployment contract |
| `127.0.0.1` | forbidden bind address | C-DC-17 | Deployment contract |
| `localhost` | forbidden bind address | C-DC-17 | Deployment contract |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the range on a continuous parameter descriptor | C-CF-180 | the descriptor carries a range, the numbers inside are left open |
| the step on a continuous parameter descriptor | C-CF-181 | the descriptor carries a step, the numbers inside are left open |
| the tag vocabulary on a publication | C-CF-109 | a tag is stored in order, the words allowed inside are left open |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 4 | 26 |
| User roles | 5 | 41 |
| Core features | 34 | 211 |
| User flow | 12 | 62 |
| UI and UX notes | 21 | 115 |
| Technical requirements | 5 | 47 |
| Data model | 8 | 79 |
| Constraints | 1 | 26 |
| Deployment contract | 12 | 23 |
