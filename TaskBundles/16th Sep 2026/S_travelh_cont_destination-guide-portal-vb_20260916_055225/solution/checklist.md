# Checklist: Destination Guide Portal

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 855
Unpinned values flagged: 2

Declared section code: `C-FE` Front-end specification.

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public guide to places in the region Marnavel. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app serves a private desk with its own sign-in for editors of the guide. `src: Overview para 1`
- [ ] `C-OV-03` `constraint` A visitor reads the published place index with no account. `src: Overview para 2`
- [ ] `C-OV-04` `capability` A visitor browses the places of the guide as a flat index. `src: Overview para 2`
- [ ] `C-OV-05` `capability` A visitor browses places through the three seeded themed collections. `src: Overview para 2`
- [ ] `C-OV-06` `capability` A visitor opens a place to read its guide entry with a gallery attached. `src: Overview para 2`
- [ ] `C-OV-07` `capability` A visitor scans a calendar of upcoming events under month headings. `src: Overview para 2`
- [ ] `C-OV-08` `capability` A visitor downloads a regional guide document from its card. `src: Overview para 2`
- [ ] `C-OV-09` `capability` A visitor looks through the pictures of every place in one masonry grid. `src: Overview para 2`
- [ ] `C-OV-10` `capability` An editor signs in at a separate address to write an entry. `src: Overview para 2`
- [ ] `C-OV-11` `capability` An editor attaches pictures to an entry. `src: Overview para 2`
- [ ] `C-OV-12` `capability` An editor uploads a guide document for an entry. `src: Overview para 2`
- [ ] `C-OV-13` `capability` An editor presses Publish to put an entry live in the guide. `src: Overview para 2`
- [ ] `C-OV-14` `capability` An editor holds an entry as a draft. `src: Overview para 2`
- [ ] `C-OV-15` `constraint` The app offers no reservation. `src: Overview para 3`
- [ ] `C-OV-16` `constraint` The app offers no ticket. `src: Overview para 3`
- [ ] `C-OV-17` `constraint` The app offers no payment. `src: Overview para 3`
- [ ] `C-OV-18` `constraint` The app carries no visitor account. `src: Overview para 3`
- [ ] `C-OV-19` `constraint` The app carries no comment on a place. `src: Overview para 3`
- [ ] `C-OV-20` `constraint` The app carries no rating on a place. `src: Overview para 3`
- [ ] `C-OV-21` `constraint` The app sends no email. `src: Overview para 3`
- [ ] `C-OV-22` `constraint` The app runs no search service. `src: Overview para 3`
- [ ] `C-OV-23` `capability` An unfinished entry stays unreachable to a visitor, the not-found surface standing at its own destination address. `src: Overview para 4`
- [ ] `C-OV-24` `capability` An unfinished entry stays unreachable to a visitor through the bytes of a picture attached to the entry. `src: Overview para 4`
- [ ] `C-OV-25` `capability` Unpublishing a live place removes the place from every public response at once. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor reads every published place on the index. `src: User roles table`
- [ ] `C-RL-02` `role` A visitor reads the published places listed in every themed collection. `src: User roles table`
- [ ] `C-RL-03` `role` A visitor reads the events calendar ordered by start date. `src: User roles table`
- [ ] `C-RL-04` `role` A visitor reads the guide document library. `src: User roles table`
- [ ] `C-RL-05` `role` A visitor reads the images in the photo gallery. `src: User roles table`
- [ ] `C-RL-06` `constraint` A visitor holds no account for the desk sign-in. `src: User roles table`
- [ ] `C-RL-07` `constraint` A visitor with no token is denied the desk entry list. `src: User roles table`
- [ ] `C-RL-08` `constraint` A visitor sees no entry in state draft on any public surface. `src: User roles table`
- [ ] `C-RL-09` `constraint` A visitor sees no entry in state draft at the address of the entry. `src: User roles table`
- [ ] `C-RL-10` `constraint` A visitor reaches no picture belonging to an entry in state draft. `src: User roles table`
- [ ] `C-RL-11` `constraint` A visitor reaches no guide document belonging to an entry in state draft. `src: User roles table`
- [ ] `C-RL-12` `constraint` A visitor reaches no desk address beyond the sign-in card. `src: User roles table`
- [ ] `C-RL-13` `constraint` No query string on a public endpoint makes a response carry a draft for a visitor. `src: User roles table`
- [ ] `C-RL-14` `role` An editor signs in at the desk. `src: User roles table`
- [ ] `C-RL-15` `role` An editor reads every entry in both states. `src: User roles table`
- [ ] `C-RL-16` `role` An editor creates an entry in the draft state. `src: User roles table`
- [ ] `C-RL-17` `role` An editor edits an entry by saving the entry again. `src: User roles table`
- [ ] `C-RL-18` `role` An editor attaches a picture to an entry with a description for the picture. `src: User roles table`
- [ ] `C-RL-19` `role` An editor attaches a guide document to an entry. `src: User roles table`
- [ ] `C-RL-20` `role` An editor publishes an entry live from the desk. `src: User roles table`
- [ ] `C-RL-21` `role` An editor returns an entry to draft. `src: User roles table`
- [ ] `C-RL-22` `constraint` An editor creates no entry outside the draft state in one call. `src: User roles table`
- [ ] `C-RL-23` `constraint` An editor publishes no entry that fails one of the five publish conditions. `src: User roles table`
- [ ] `C-RL-24` `constraint` An editor creates no themed collection beside the three seeded collections. `src: User roles table`
- [ ] `C-RL-25` `constraint` An editor renames no seeded themed collection. `src: User roles table`
- [ ] `C-RL-26` `constraint` An editor creates no event. `src: User roles table`
- [ ] `C-RL-27` `constraint` An editor edits no event. `src: User roles table`
- [ ] `C-RL-28` `constraint` An editor reaches no desk address with a missing token. `src: User roles table`
- [ ] `C-RL-29` `contract` The app enforces authorization server-side on every desk endpoint, denying a caller with no token. `src: User roles para 2`
- [ ] `C-RL-30` `constraint` The app denies a direct desk API call from a visitor session with no token. `src: User roles para 2`
- [ ] `C-RL-31` `constraint` The app leaves the entry unchanged when a desk publish is denied for a missing token. `src: User roles para 2`
- [ ] `C-RL-32` `constraint` The app carries no registration form beside the desk sign-in card. `src: User roles para 3`
- [ ] `C-RL-33` `constraint` The app carries no registration endpoint. `src: User roles para 3`
- [ ] `C-RL-34` `literal` The app seeds one editor account at `editor@example.com`. `src: User roles, seeded account table`
- [ ] `C-RL-35` `literal` The app accepts the password `deku-demo-pw-2026` for the seeded editor account. `src: User roles, seeded account table`
- [ ] `C-RL-36` `constraint` The app exposes no password reset endpoint. `src: Core features rule 43`

## C-CF Core features

- [ ] `C-CF-01` `data` The app holds every entry in state `published` or state `draft`. `src: Core features para 1`
- [ ] `C-CF-02` `literal` The app spells the state of a seeded published place `published` in lowercase. `src: Core features para 1`
- [ ] `C-CF-03` `literal` The app spells the draft entry state `draft` in lowercase. `src: Core features para 1`
- [ ] `C-CF-04` `constraint` The app applies the published filter once in the data layer. `src: Core features para 1`
- [ ] `C-CF-05` `constraint` The app keeps a draft entry out of the place index response. `src: Core features rule 1`
- [ ] `C-CF-06` `constraint` The app lists no draft entry in a themed collection response. `src: Core features rule 1`
- [ ] `C-CF-07` `constraint` The app keeps a draft entry out of the photo gallery response. `src: Core features rule 1`
- [ ] `C-CF-08` `constraint` The app keeps a draft entry out of the guide document library response. `src: Core features rule 1`
- [ ] `C-CF-09` `constraint` The app accepts no state parameter on a public endpoint. `src: Core features rule 1`
- [ ] `C-CF-10` `literal` The app answers `404` at the address of a draft entry. `src: Core features rule 2`
- [ ] `C-CF-11` `capability` The app renders the not-found surface at the address of a draft entry. `src: Core features rule 2`
- [ ] `C-CF-12` `literal` The app withholds `403` at the address of a draft entry. `src: Core features rule 2`
- [ ] `C-CF-13` `literal` The app streams the bytes of a picture at `GET /api/media/images/{image_id}`. `src: Core features rule 3`
- [ ] `C-CF-14` `literal` The app serves a guide document at `GET /api/media/brochures/{brochure_id}`. `src: Core features rule 3`
- [ ] `C-CF-15` `capability` The app resolves the owning entry state of an object at the moment of the request. `src: Core features rule 3`
- [ ] `C-CF-16` `capability` The app returns the bytes of an object owned by a published entry. `src: Core features rule 3`
- [ ] `C-CF-17` `literal` The app answers `404` for the bytes of an object owned by a draft entry. `src: Core features rule 3`
- [ ] `C-CF-18` `capability` The app resolves a regional guide document that has no owning entry. `src: Core features rule 3`
- [ ] `C-CF-19` `constraint` The app keeps the object store closed to an anonymous caller. `src: Core features rule 4`
- [ ] `C-CF-20` `constraint` The app stops an object resolving for a draft entry by the state check at request time. `src: Core features rule 4`
- [ ] `C-CF-21` `capability` The app removes a place from the index, every collection, the gallery, the library on unpublishing. `src: Core features rule 36`
- [ ] `C-CF-22` `capability` The app closes the object route for an entry from the moment the entry returns to draft. `src: Core features rule 5`
- [ ] `C-CF-23` `constraint` The app stops every object resolving at once after an entry returns to draft. `src: Core features rule 5`
- [ ] `C-CF-24` `literal` The app stores an uploaded picture under the key `entries/<entry_id>/gallery/<sha256_of_bytes>.<ext>`. `src: Core features rule 6`
- [ ] `C-CF-25` `capability` The app writes an uploaded picture into the object store as a real object. `src: Core features rule 6`
- [ ] `C-CF-26` `literal` The app stores a guide document attached to an entry under the key `entries/<entry_id>/brochure/<sha256_of_bytes>.pdf`. `src: Core features rule 6`
- [ ] `C-CF-27` `literal` The app stores a regional guide document under the key `regional/<brochure_id>/<sha256_of_bytes>.pdf`. `src: Core features rule 6`
- [ ] `C-CF-28` `constraint` The app writes no picture bytes to the filesystem of the app container rather than the bucket. `src: Core features rule 7`
- [ ] `C-CF-29` `constraint` The app writes no picture bytes into a database column rather than the bucket. `src: Core features rule 7`
- [ ] `C-CF-30` `constraint` The app streams no picture from its own bundle in place of the bucket. `src: Core features rule 7`
- [ ] `C-CF-31` `capability` The app shows a picture count against an entry on the desk list that equals the objects the store holds for the entry. `src: Core features rule 8`
- [ ] `C-CF-32` `capability` The app reads the file size on a guide document card from the metadata of the stored object. `src: Core features rule 9`
- [ ] `C-CF-33` `constraint` The app reads the size of a stored object rather than a figure an editor typed. `src: Core features rule 9`
- [ ] `C-CF-34` `capability` The app carries an event in the public events response only when the effective end date of the event is today or later in UTC. `src: Core features rule 10`
- [ ] `C-CF-35` `constraint` The app excludes an event whose end date has passed from the events response. `src: Core features rule 10`
- [ ] `C-CF-36` `capability` The app treats the start date of an event as the end date of the event when the event carries no end date. `src: Core features rule 11`
- [ ] `C-CF-37` `capability` The app keeps an event whose end date is today in the events response for the whole of today. `src: Core features rule 12`
- [ ] `C-CF-38` `constraint` The app exposes no desk endpoint that creates an event. `src: Core features rule 13`
- [ ] `C-CF-39` `constraint` The app exposes no desk endpoint that edits an event. `src: Core features rule 13`
- [ ] `C-CF-40` `constraint` The app exposes no desk endpoint that deletes an event. `src: Core features rule 13`
- [ ] `C-CF-41` `capability` The app lists published entries only on the place index. `src: Core features rule 14`
- [ ] `C-CF-42` `literal` The app pages the place index at 24 entries. `src: Core features rule 14`
- [ ] `C-CF-43` `capability` The app reads the count line on the place index as the number of published entries. `src: Core features rule 14`
- [ ] `C-CF-44` `capability` The app filters the place index on place name. `src: Core features rule 15`
- [ ] `C-CF-45` `capability` The app filters the place index on theme. `src: Core features rule 15`
- [ ] `C-CF-46` `capability` The app sorts the place index by name ascending. `src: Core features rule 15`
- [ ] `C-CF-47` `capability` The app sorts the place index by recently added. `src: Core features rule 15`
- [ ] `C-CF-48` `capability` The app holds every filter choice on the place index in the address. `src: Core features rule 15`
- [ ] `C-CF-49` `capability` The app holds the sort choice on the place index in the query string. `src: Core features rule 15`
- [ ] `C-CF-50` `capability` The app survives a reload of a filtered place index address with the filter still applied. `src: Core features rule 15`
- [ ] `C-CF-51` `capability` The app replaces the place index grid with one sentence when a filter matches nothing. `src: Core features rule 16`
- [ ] `C-CF-52` `capability` The app offers a control clearing the filter when a filter matches nothing. `src: Core features rule 16`
- [ ] `C-CF-53` `constraint` The app renders no blank region when a place index filter matches nothing. `src: Core features rule 16`
- [ ] `C-CF-54` `capability` The app carries the guide text of an entry on the place entry surface. `src: Core features rule 17`
- [ ] `C-CF-55` `capability` The app carries the theme badges of an entry beside the place name. `src: Core features rule 17`
- [ ] `C-CF-56` `capability` The app carries a fact panel holding the nearest station on the place entry surface. `src: Core features rule 17`
- [ ] `C-CF-57` `capability` The app carries the best months to visit in the fact panel of a place entry. `src: Core features rule 17`
- [ ] `C-CF-58` `capability` The app carries a distance figure in the fact panel of a place entry. `src: Core features rule 17`
- [ ] `C-CF-59` `capability` The app carries a strip of every picture attached to an entry on the place entry surface. `src: Core features rule 17`
- [ ] `C-CF-60` `capability` The app carries a related row of up to three other published entries sharing a theme with the entry. `src: Core features rule 17`
- [ ] `C-CF-61` `constraint` The app excludes the current entry from the related row of the entry. `src: Core features rule 17`
- [ ] `C-CF-62` `capability` The app orders the related row of a place entry by sort index. `src: Core features rule 17`
- [ ] `C-CF-63` `capability` The app renders the related row with the entries that exist when fewer than three qualify. `src: Core features rule 17`
- [ ] `C-CF-64` `data` The app keeps a place slug in lowercase kebab form. `src: Core features rule 18`
- [ ] `C-CF-65` `data` A place slug is unique across both entry states, so a publish on a taken slug is refused. `src: Core features rule 18`
- [ ] `C-CF-66` `literal` The app reserves the eleven top-level segments `desk`, `api`, `media`, `event`, `brochures`, `photo-gallery`, `collection`, `destination`, `privacy`, `terms`, `404` from a place slug. `src: Core features rule 18`
- [ ] `C-CF-67` `literal` The app returns exactly three seeded collections named `Coastline`, `Highlands`, `Backwater`. `src: Core features rule 19`
- [ ] `C-CF-68` `constraint` The app creates no fourth collection beside the three seeded collections. `src: Core features rule 19`
- [ ] `C-CF-69` `constraint` The app deletes no seeded collection on any request. `src: Core features rule 19`
- [ ] `C-CF-70` `data` The app allows an entry to carry zero to three themed collections. `src: Core features rule 20`
- [ ] `C-CF-71` `capability` The app shows an entry carrying no collection on the place index. `src: Core features rule 20`
- [ ] `C-CF-72` `constraint` The app lists an entry carrying no collection in no themed collection. `src: Core features rule 20`
- [ ] `C-CF-73` `capability` The app renders the head of an empty themed collection that holds no published entry. `src: Core features rule 21`
- [ ] `C-CF-74` `capability` The app renders the editorial introduction of a themed collection that holds no published entry. `src: Core features rule 21`
- [ ] `C-CF-75` `capability` The app renders one sentence in place of the grid of a themed collection that holds no published entry. `src: Core features rule 21`
- [ ] `C-CF-76` `literal` The app answers `200` for a themed collection that holds no published entry. `src: Core features rule 21`
- [ ] `C-CF-77` `capability` The app lists the guide documents of published entries in the library. `src: Core features rule 22`
- [ ] `C-CF-78` `capability` The app lists the regional guide documents in the library. `src: Core features rule 22`
- [ ] `C-CF-79` `constraint` The app keeps a guide document attached to a draft entry out of the library. `src: Core features rule 22`
- [ ] `C-CF-80` `capability` The app generates the cover of a guide document card from the first page of the document at upload time. `src: Core features rule 23`
- [ ] `C-CF-81` `capability` The library response carries the page count of every guide document. `src: Core features rule 23`
- [ ] `C-CF-82` `literal` The app shows the file size of a guide document in megabytes to one decimal place. `src: Core features rule 23`
- [ ] `C-CF-83` `constraint` The app uses no separately uploaded picture as the cover of a guide document. `src: Core features rule 23`
- [ ] `C-CF-84` `literal` The app serves a guide document download with a `Content-Disposition` of `attachment`. `src: Core features rule 24`
- [ ] `C-CF-85` `capability` The app derives the filename of a guide document download from the title of the document. `src: Core features rule 24`
- [ ] `C-CF-86` `capability` The app carries the images of every published entry in the photo gallery response. `src: Core features rule 25`
- [ ] `C-CF-87` `capability` The app filters the photo gallery by theme. `src: Core features rule 25`
- [ ] `C-CF-88` `capability` The app holds the theme choice on the photo gallery in the query string. `src: Core features rule 25`
- [ ] `C-CF-89` `literal` The app pages the photo gallery at 24 tiles. `src: Core features rule 25`
- [ ] `C-CF-90` `capability` The app extends the photo gallery grid through an explicit control at the foot of the grid. `src: Core features rule 25`
- [ ] `C-CF-91` `constraint` The app extends the photo gallery grid by a control at its foot rather than on scroll position. `src: Core features rule 25`
- [ ] `C-CF-92` `capability` The app opens a lightbox carrying the picture when a gallery tile is selected. `src: Core features rule 26`
- [ ] `C-CF-93` `capability` The app carries the place name in the lightbox of a gallery picture. `src: Core features rule 26`
- [ ] `C-CF-94` `capability` The app carries a link to the place entry in the lightbox of a gallery picture. `src: Core features rule 26`
- [ ] `C-CF-95` `capability` The app steps through the filtered lightbox set with previous, next controls that wrap at both ends. `src: Core features rule 26`
- [ ] `C-CF-96` `capability` The app takes an email in a field on the desk sign-in card. `src: Core features rule 27`
- [ ] `C-CF-97` `capability` The app takes a password at the desk sign-in surface. `src: Core features rule 27`
- [ ] `C-CF-98` `capability` The app states in its message that the credentials did not match on a failed sign-in. `src: Core features rule 27`
- [ ] `C-CF-99` `constraint` The app tells an unknown address apart from a wrong password nowhere on a failed sign-in. `src: Core features rule 27`
- [ ] `C-CF-100` `capability` The app lists every entry in both states on the desk list. `src: Core features rule 28`
- [ ] `C-CF-101` `capability` The app orders the desk list by last edited descending. `src: Core features rule 28`
- [ ] `C-CF-102` `literal` The app carries the columns name, themes, state, picture count, last edited on the desk list. `src: Core features rule 28`
- [ ] `C-CF-103` `ui` A badge naming the state of the entry sits on each row of the desk list. `src: Core features rule 28`
- [ ] `C-CF-104` `capability` The app filters the desk list across all, published, draft. `src: Core features rule 28`
- [ ] `C-CF-105` `capability` The app carries a count for each state on the desk list filter. `src: Core features rule 28`
- [ ] `C-CF-106` `literal` The app serves the composer at `/desk/entry/new`. `src: Core features rule 29`
- [ ] `C-CF-107` `literal` The app serves the composer carrying the web address field at `/desk/entry/<id>`. `src: Core features rule 29`
- [ ] `C-CF-108` `literal` The app requires a composer name field of 3 to 80 characters. `src: Core features rule 29`
- [ ] `C-CF-109` `literal` The app requires a composer summary field of up to 240 characters. `src: Core features rule 29`
- [ ] `C-CF-110` `literal` The app requires a composer guide field of up to 20000 characters. `src: Core features rule 29`
- [ ] `C-CF-111` `literal` The app accepts zero to three themes on the composer field. `src: Core features rule 29`
- [ ] `C-CF-112` `literal` The app accepts zero to twenty pictures on the composer picture field. `src: Core features rule 29`
- [ ] `C-CF-113` `literal` The app accepts one optional guide document in the composer. `src: Core features rule 29`
- [ ] `C-CF-114` `capability` The app fills the web address field from the place name until an editor edits the field. `src: Core features rule 30`
- [ ] `C-CF-115` `capability` The app stops deriving the composer slug from the name the moment the editor edits the slug by hand. `src: Core features rule 30`
- [ ] `C-CF-116` `capability` The app validates the name length on the server, refusing a name shorter than the minimum. `src: Core features rule 31`
- [ ] `C-CF-117` `capability` The app repeats the required-field validation on the client before a publish. `src: Core features rule 31`
- [ ] `C-CF-118` `capability` The app names the failing field in a composer refusal. `src: Core features rule 31`
- [ ] `C-CF-119` `constraint` The app writes nothing when the summary runs over the character limit. `src: Core features rule 31`
- [ ] `C-CF-120` `data` The app requires a description on every picture. `src: Core features rule 32`
- [ ] `C-CF-121` `constraint` The app attaches no picture with an empty description to a published entry. `src: Core features rule 32`
- [ ] `C-CF-122` `capability` The app saves an entry as a draft with uploads still in flight. `src: Core features rule 33`
- [ ] `C-CF-123` `capability` The app retries a failed picture upload, keeping the chosen file in the field. `src: Core features rule 33`
- [ ] `C-CF-124` `capability` The app retries a failed upload, keeping the summary field with the rest of the form. `src: Core features rule 33`
- [ ] `C-CF-125` `capability` The app creates every entry in state draft. `src: Core features rule 34`
- [ ] `C-CF-126` `constraint` The app carries no request that lands an entry outside the draft state in one call. `src: Core features rule 34`
- [ ] `C-CF-127` `constraint` The app refuses a publish at the API when a required field is empty. `src: Core features rule 35`
- [ ] `C-CF-128` `constraint` The app refuses a publish at the API when the slug is already held by another entry in either state. `src: Core features rule 35`
- [ ] `C-CF-129` `constraint` The app refuses a publish at the API when the slug is a reserved segment. `src: Core features rule 35`
- [ ] `C-CF-130` `constraint` The app refuses a publish at the API when an attached picture is still uploading. `src: Core features rule 35`
- [ ] `C-CF-131` `constraint` The app refuses a publish at the API when an attached picture has an empty description. `src: Core features rule 35`
- [ ] `C-CF-132` `capability` The app names the failing condition of the five in a publish refusal, such as a taken slug. `src: Core features rule 35`
- [ ] `C-CF-133` `constraint` The app refuses a publish naming a reserved slug at the API rather than by a disabled control. `src: Core features rule 35`
- [ ] `C-CF-134` `capability` The app shows a published entry on the place index. `src: Core features rule 36`
- [ ] `C-CF-135` `capability` The app shows a published entry in each themed collection of the entry. `src: Core features rule 36`
- [ ] `C-CF-136` `capability` The app shows a published entry at the address of the entry. `src: Core features rule 36`
- [ ] `C-CF-137` `capability` The app shows the images of a published entry in the photo gallery response. `src: Core features rule 36`
- [ ] `C-CF-138` `capability` The app shows the guide document of a published entry in the library. `src: Core features rule 36`
- [ ] `C-CF-139` `capability` The app removes a place returned to draft from every one of those five public surfaces. `src: Core features rule 36`
- [ ] `C-CF-140` `capability` The app serves a privacy page reachable from the footer of every surface. `src: Core features rule 37`
- [ ] `C-CF-141` `capability` The app states on the privacy page what the board records about a visitor. `src: Core features rule 37`
- [ ] `C-CF-142` `capability` The app states on the privacy page how long the board keeps what the board records. `src: Core features rule 37`
- [ ] `C-CF-143` `capability` The app serves a terms page reachable from the footer of every surface. `src: Core features rule 38`
- [ ] `C-CF-144` `capability` The app links the terms page from the desk sign-in card. `src: Core features rule 38`
- [ ] `C-CF-145` `capability` The app states on the terms page the conditions on using the guide. `src: Core features rule 38`
- [ ] `C-CF-146` `capability` The app states on the terms page the conditions on reusing the photographs of the guide. `src: Core features rule 38`
- [ ] `C-CF-147` `capability` The app renders the board not-found surface at any unmatched path. `src: Core features rule 39`
- [ ] `C-CF-148` `ui` The not-found surface carries the global header, the global footer, a heading, one sentence, a single control back to the home surface. `src: Core features rule 39`
- [ ] `C-CF-149` `literal` The app answers `404` at any unknown path. `src: Core features rule 39`
- [ ] `C-CF-150` `capability` The app resolves every internal link on every public surface. `src: Core features rule 40`
- [ ] `C-CF-151` `constraint` The app answers `404` on no internal link of a public surface. `src: Core features rule 40`
- [ ] `C-CF-152` `literal` The app takes an email with a password at `POST /api/auth/login`. `src: Core features rule 41`
- [ ] `C-CF-153` `literal` The app answers a successful desk sign-in with an `access_token` value that lands the editor on the entry list. `src: Core features rule 41`
- [ ] `C-CF-154` `literal` The app reads a desk request token from an `Authorization: Bearer <token>` header. `src: Core features rule 41`
- [ ] `C-CF-155` `constraint` The app requires the bearer token on every endpoint under `/api/desk/`. `src: Core features rule 41`
- [ ] `C-CF-156` `literal` The app ends the desk session at `POST /api/auth/logout`, returning the editor to the sign-in card. `src: Core features rule 41`
- [ ] `C-CF-157` `constraint` The app denies a desk request that carries no token. `src: Core features rule 42`
- [ ] `C-CF-158` `constraint` The app denies a desk request that carries a malformed token. `src: Core features rule 42`
- [ ] `C-CF-159` `constraint` The app leaves an entry unchanged when a desk request naming the entry is denied. `src: Core features rule 42`
- [ ] `C-CF-160` `literal` The app expires a bearer token 12 hours after the token is issued. `src: Core features rule 42`
- [ ] `C-CF-161` `data` The app stores a desk password hashed. `src: Core features rule 43`
- [ ] `C-CF-162` `constraint` The sign-in card carries no password reset control. `src: Core features rule 43`
- [ ] `C-CF-163` `literal` The app denies a desk request carrying a token presented after `POST /api/auth/logout`. `src: Deployment contract, API shapes table`
- [ ] `C-CF-164` `constraint` The app denies a desk request that carries an expired token. `src: Core features rule 42`
- [ ] `C-CF-165` `literal` The app serves the index of the three collections at `/collection`. `src: Core features rule 19`
- [ ] `C-CF-166` `ui` A collection index card carries the collection name, its standfirst, its published count. `src: Core features rule 19`
- [ ] `C-CF-167` `literal` The `Themes` label in the header goes to `/collection`. `src: Core features rule 19`
- [ ] `C-CF-168` `capability` The search control opens `/destination` with the name filter focused. `src: Front-end specification, header`
- [ ] `C-CF-169` `constraint` The search control reaches no search service of its own. `src: Front-end specification, header`
- [ ] `C-CF-170` `literal` The app answers `GET /api/desk/entries/counts` with the keys `all`, `published`, `draft`. `src: Deployment contract, API shapes table`
- [ ] `C-CF-171` `capability` The app orders the related row of a place by sort index ascending. `src: Core features rule 17`
- [ ] `C-CF-172` `literal` The composer requires a nearest station of up to 80 characters. `src: Core features rule 29`
- [ ] `C-CF-173` `literal` The composer requires best months of up to 80 characters. `src: Core features rule 29`
- [ ] `C-CF-174` `literal` The composer requires the distance field as a positive integer of kilometres. `src: Core features rule 29`
- [ ] `C-CF-175` `capability` The app creates the entry row on the first save rather than on entering the composer. `src: Core features rule 33`
- [ ] `C-CF-176` `constraint` The app lists no entry on `/desk` until the editor saves one. `src: Core features rule 33`
- [ ] `C-CF-177` `constraint` The app issues an upload target naming an `object_key` only for an entry that already has an id. `src: Core features rule 33`
- [ ] `C-CF-178` `capability` The app accepts a draft saved with an empty required field such as the summary. `src: Core features rule 31`
- [ ] `C-CF-179` `literal` The app downloads `Marnavel in Three Days` as the filename `marnavel-in-three-days.pdf`. `src: Core features rule 24`
- [ ] `C-CF-180` `literal` The app answers `GET /api/desk/entries/{id}` with one entry in either state carrying its `images`, its `brochure`. `src: Deployment contract, API shapes table`
- [ ] `C-CF-181` `literal` The desk list response carries the picture count as `picture_count` on each row. `src: Core features rule 28`
- [ ] `C-CF-182` `literal` The app selects the rows of the desk list with `?state=all`, `?state=published`, `?state=draft`. `src: Deployment contract, API shapes table`

## C-UF User flow

- [ ] `C-UF-01` `literal` The app serves the home surface at `/`, carrying the footer link to the privacy page. `src: User flow route table`
- [ ] `C-UF-02` `literal` The app serves the place index at `/destination`. `src: User flow route table`
- [ ] `C-UF-03` `literal` The app serves a place entry at `/destination/<slug>`. `src: User flow route table`
- [ ] `C-UF-04` `literal` The app serves a themed collection at `/collection/<slug>`. `src: User flow route table`
- [ ] `C-UF-05` `literal` The app serves the events calendar at `/event`. `src: User flow route table`
- [ ] `C-UF-06` `literal` The app serves the guide document library of download cards at `/brochures`. `src: User flow route table`
- [ ] `C-UF-07` `literal` The app serves the photo gallery at `/photo-gallery`. `src: User flow route table`
- [ ] `C-UF-08` `literal` The app serves the privacy page at `/privacy`, linked from the footer. `src: User flow route table`
- [ ] `C-UF-09` `literal` The app serves the terms page at `/terms`, linked from the footer. `src: User flow route table`
- [ ] `C-UF-10` `literal` The app serves the board not-found surface at `/404`. `src: User flow route table`
- [ ] `C-UF-11` `literal` The app serves the editor sign-in card at `/desk/login`. `src: User flow route table`
- [ ] `C-UF-12` `literal` The app serves the desk entry list at `/desk`. `src: User flow route table`
- [ ] `C-UF-13` `role` The app requires an editor token at `/desk`, denying a caller without one. `src: User flow route table`
- [ ] `C-UF-14` `role` The app requires an editor session at `/desk/entry/new`. `src: User flow route table`
- [ ] `C-UF-15` `role` The app requires an editor session at `/desk/entry/<id>`. `src: User flow route table`
- [ ] `C-UF-16` `capability` The app lands a signed-out request for a desk address on `/desk/login`. `src: User flow, entry and redirects`
- [ ] `C-UF-17` `capability` The app lands a successful sign-in on `/desk`. `src: User flow, entry and redirects`
- [ ] `C-UF-18` `capability` The app returns a sign-out to `/desk/login`. `src: User flow, entry and redirects`
- [ ] `C-UF-19` `constraint` The app denies the desk entry list at the address that was open after a sign-out. `src: User flow, entry and redirects`
- [ ] `C-UF-20` `constraint` The app denies a save whose token expired part-way through an edit. `src: User flow, entry and redirects`
- [ ] `C-UF-21` `constraint` The app leaves the entry unchanged when a save is denied for an expired token. `src: User flow, entry and redirects`
- [ ] `C-UF-22` `capability` The app states the reason on returning an editor with an expired token to the sign-in card. `src: User flow, entry and redirects`
- [ ] `C-UF-23` `constraint` The app leaves the published place index open to a visitor. `src: User flow, entry and redirects`
- [ ] `C-UF-24` `capability` The app renders the not-found surface at any unmatched path rather than an error page. `src: User flow, entry and redirects`
- [ ] `C-UF-25` `constraint` The app renders no forbidden page at the address of a draft entry. `src: User flow, entry and redirects`
- [ ] `C-UF-26` `ui` The place index count line reads `8 places` against the seeded guide. `src: User flow journey 1`
- [ ] `C-UF-27` `capability` The app narrows the place index to `Saltmere` for the name filter text `salt`. `src: User flow journey 1`
- [ ] `C-UF-28` `ui` Cards already on the place index hold at half opacity during a filter request in flight. `src: User flow journey 1`
- [ ] `C-UF-29` `capability` The app applies the same filter after a reload of a copied place index address. `src: User flow journey 1`
- [ ] `C-UF-30` `capability` A visitor drags the picture strip of a place entry sideways. `src: User flow journey 2`
- [ ] `C-UF-31` `capability` A visitor follows one of the three related places from a place entry. `src: User flow journey 2`
- [ ] `C-UF-32` `capability` The app derives the month headings of the events calendar from the data. `src: User flow journey 3`
- [ ] `C-UF-33` `constraint` The app shows no month heading for a month holding no event. `src: User flow journey 3`
- [ ] `C-UF-34` `ui` The events calendar shows `Highfen Harvest Fair` present on the final day of the event. `src: User flow journey 3`
- [ ] `C-UF-35` `constraint` The events response excludes `Penmara Kite Days`, an event that has ended. `src: User flow journey 3`
- [ ] `C-UF-36` `capability` A visitor receives a file named after the guide document rather than an identifier. `src: User flow journey 4`
- [ ] `C-UF-37` `capability` A visitor steps through the gallery lightbox set with the arrow keys. `src: User flow journey 5`
- [ ] `C-UF-38` `capability` A visitor closes the gallery lightbox with the escape key. `src: User flow journey 5`
- [ ] `C-UF-39` `capability` The app returns the keyboard focus to the tile that opened the lightbox on close. `src: User flow journey 5`
- [ ] `C-UF-40` `ui` A failed sign-in shivers the card once. `src: User flow journey 6`
- [ ] `C-UF-41` `ui` A failed sign-in takes the failure colour on both sign-in fields. `src: User flow journey 6`
- [ ] `C-UF-42` `literal` A failed sign-in reads `Those details did not match. Try again.` `src: User flow journey 6`
- [ ] `C-UF-43` `capability` The app fills the web address field in as `ferrow-sands` from the place name `Ferrow Sands`. `src: User flow journey 7`
- [ ] `C-UF-44` `capability` The app keeps a hand-edited web address unchanged when the place name is retyped. `src: User flow journey 7`
- [ ] `C-UF-45` `literal` A publish refused for an empty required field reads `Fill in every required field before publishing.` `src: User flow journey 8`
- [ ] `C-UF-46` `literal` A publish refused for a reserved web address reads `That web address is reserved. Choose another.` `src: User flow journey 8`
- [ ] `C-UF-47` `literal` A publish refused for a taken web address reads `That web address is already taken.` `src: User flow journey 8`
- [ ] `C-UF-48` `literal` A successful publish raises a message beginning `Published.` `src: User flow journey 9`
- [ ] `C-UF-49` `capability` A newly published place entry renders at the address of the entry to a signed-out visitor. `src: User flow journey 9`
- [ ] `C-UF-50` `literal` A return to draft raises a message beginning `Returned to draft.` `src: User flow journey 10`
- [ ] `C-UF-51` `capability` The app removes a place returned to draft from the place index for a signed-out visitor. `src: User flow journey 10`
- [ ] `C-UF-52` `capability` The app removes the pictures of a place returned to draft from the photo gallery. `src: User flow journey 10`
- [ ] `C-UF-53` `capability` The app removes the guide document of a place returned to draft from the library. `src: User flow journey 10`
- [ ] `C-UF-54` `literal` The empty state of a themed collection opens with `Nothing is in`. `src: User flow, states`
- [ ] `C-UF-55` `literal` The empty state of the events calendar reads `Nothing is scheduled just now. The places are still there.` `src: User flow, states`
- [ ] `C-UF-56` `ui` The desk entry list carries an empty line of its own. `src: User flow, states`
- [ ] `C-UF-57` `ui` Every picture upload in the composer field shows determinate progress. `src: User flow, states`
- [ ] `C-UF-58` `literal` A failed region on a surface reads `Something went wrong at our end. Try again in a moment.`, with the global header still drawn around the surface. `src: User flow, states`
- [ ] `C-UF-59` `constraint` An error leaves the rest of the surface usable, with the global header still drawn. `src: User flow, states`
- [ ] `C-UF-60` `literal` The app serves the themed collection index at `/collection`. `src: User flow route table`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The home surface opens on a full-bleed moving panel behind a dark wash. `src: Front-end specification, header media`
- [ ] `C-UX-02` `ui` The chrome of the public surfaces reads as a pale frame around the photography. `src: UI/UX notes para 1`
- [ ] `C-UX-03` `ui` The warmth of a public surface comes from the imagery with one accent colour. `src: UI/UX notes para 1`
- [ ] `C-UX-04` `ui` No decoration stands in for content on a public surface. `src: UI/UX notes para 1`
- [ ] `C-UX-05` `ui` The page ground of every surface is a near-white neutral. `src: UI/UX notes para 2`
- [ ] `C-UX-06` `ui` Section bands sit on a near-white neutral one step below the page ground. `src: UI/UX notes para 2`
- [ ] `C-UX-07` `ui` The change of ground between neighbouring bands is the only separation drawn between them. `src: UI/UX notes para 2`
- [ ] `C-UX-08` `ui` Body text takes a deep cool neutral. `src: UI/UX notes para 2`
- [ ] `C-UX-09` `ui` Metadata takes a mid cool neutral. `src: UI/UX notes para 2`
- [ ] `C-UX-10` `ui` A heading on a light ground takes a near-black neutral. `src: UI/UX notes para 2`
- [ ] `C-UX-11` `ui` The footer is the one dark region of the product, a deep neutral carrying white text. `src: UI/UX notes para 2`
- [ ] `C-UX-12` `ui` A mid, vivid orange marks everything a visitor can act on. `src: UI/UX notes para 2`
- [ ] `C-UX-13` `ui` A mid, vivid orange marks everything currently selected. `src: UI/UX notes para 2`
- [ ] `C-UX-14` `ui` A secondary mid, vivid amber carries the home eyebrow line. `src: UI/UX notes para 2`
- [ ] `C-UX-15` `ui` An inline link inside prose takes a mid, vivid blue. `src: UI/UX notes para 2`
- [ ] `C-UX-16` `ui` Failure takes a mid, vivid red, appearing nowhere but a validation failure. `src: UI/UX notes para 2`
- [ ] `C-UX-17` `ui` Success takes a deep, soft teal, appearing nowhere but the live badge with the publish confirmation. `src: UI/UX notes para 2`
- [ ] `C-UX-18` `ui` A draft badge takes a mid, vivid amber fill with deep cool neutral text on the fill. `src: UI/UX notes para 2`
- [ ] `C-UX-19` `constraint` The orange accent carries no body text on a near-white ground. `src: UI/UX notes para 2`
- [ ] `C-UX-20` `ui` The light cool neutral carries placeholder text with disabled text only. `src: UI/UX notes para 2`
- [ ] `C-UX-21` `constraint` Every pairing carrying body text meets the WCAG AA contrast bar in the scheme shipped. `src: UI/UX notes para 2`
- [ ] `C-UX-22` `literal` Display headings take the family `Playfair Display`. `src: UI/UX notes para 3`
- [ ] `C-UX-23` `literal` Body, navigation, metadata, controls take the family `IBM Plex Sans Condensed`. `src: UI/UX notes para 3`
- [ ] `C-UX-24` `constraint` No font file ships with the build. `src: UI/UX notes para 3`
- [ ] `C-UX-25` `ui` Figures align wherever counts stack on the desk list. `src: UI/UX notes para 3`
- [ ] `C-UX-26` `ui` Density reads as spacious, with a generous reading measure. `src: UI/UX notes para 4`
- [ ] `C-UX-27` `ui` Bands are separated by air rather than by lines. `src: UI/UX notes para 4`
- [ ] `C-UX-28` `ui` The layout archetype is a fixed pale top navigation bar present on every surface. `src: UI/UX notes para 4`
- [ ] `C-UX-29` `ui` The navigation collapses into a drawer entering from the right over a dimmed page on the narrow tiers. `src: UI/UX notes para 4`
- [ ] `C-UX-30` `ui` Motion character is eased, with entrances decelerating. `src: UI/UX notes para 5`
- [ ] `C-UX-31` `ui` One long reveal on the home surface waits a beat, then glides in. `src: UI/UX notes para 5`
- [ ] `C-UX-32` `ui` A field that fails validation nudges sideways once. `src: UI/UX notes para 5`
- [ ] `C-UX-33` `ui` A leaving message fades out. `src: UI/UX notes para 5`
- [ ] `C-UX-34` `ui` Every transition collapses to effectively nothing under a reduced-motion preference. `src: UI/UX notes para 5`
- [ ] `C-UX-35` `ui` The header holds its poster frame rather than playing under a reduced-motion preference. `src: UI/UX notes para 5`
- [ ] `C-UX-36` `ui` The nudge becomes a static border change to the failure colour under a reduced-motion preference. `src: UI/UX notes para 5`
- [ ] `C-UX-37` `ui` Nothing in the product is carried by motion alone. `src: UI/UX notes para 5`
- [ ] `C-UX-38` `constraint` Every interactive element is reachable in document order from the skip link. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-39` `constraint` The focus ring is restyled rather than removed. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-40` `ui` Keyboard navigation works throughout the lightbox. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-41` `ui` One first-level heading sits on every surface, the privacy page among them. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-42` `ui` Headings descend without skipping a level. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-43` `ui` Landmarks for the banner, the navigation, the main region, the content information sit on every surface around the header. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-44` `constraint` Every content picture carries alternative text taken from a required field on the upload of the picture. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-45` `constraint` The decorative header motion layer carries an empty alternative text. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-46` `constraint` Touch targets are comfortably sized. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-47` `ui` An icon-only control carries a label. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-48` `ui` A state badge carries its own word beside the fill of the badge. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-49` `ui` The product is responsive across five breakpoints. `src: UI/UX notes, the responsive paragraph`
- [ ] `C-UX-50` `constraint` Nothing overflows sideways at a narrow viewport. `src: UI/UX notes, the responsive paragraph`
- [ ] `C-UX-51` `ui` Every navigation target stays reachable behind the drawer at a narrow viewport. `src: UI/UX notes, the responsive paragraph`
- [ ] `C-UX-52` `ui` Rows of cards fold to a single column at a narrow viewport. `src: UI/UX notes, the responsive paragraph`
- [ ] `C-UX-53` `ui` The product commits to the light scheme. `src: UI/UX notes, the responsive paragraph`
- [ ] `C-UX-54` `ui` No surface is dominated by one hue family with a single signal. `src: UI/UX notes, the design-against-failures paragraph`
- [ ] `C-UX-55` `ui` No band is rendered empty rather than omitted. `src: UI/UX notes, the design-against-failures paragraph`
- [ ] `C-UX-56` `ui` No marketing composition stands where the working desk belongs. `src: UI/UX notes, the design-against-failures paragraph`
- [ ] `C-UX-57` `constraint` No grid grows on scroll, so the footer stays in reach. `src: UI/UX notes, the design-against-failures paragraph`
- [ ] `C-UX-58` `constraint` Keyboard navigation works throughout the navigation drawer. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-59` `constraint` Keyboard navigation fills every composer field, the picture description field among them. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-60` `constraint` The lightbox, the drawer, the composer each trap focus, handing focus back on close. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-61` `ui` Figures align wherever counts stack on the calendar month headings. `src: UI/UX notes para 3`
- [ ] `C-UX-62` `ui` A control shows a resting, a pointed-at, a pressed, a focused, an unavailable state. `src: UI/UX notes, the component states paragraph`
- [ ] `C-UX-63` `ui` A field carries its label above with any failure message directly beneath. `src: UI/UX notes, the component states paragraph`
- [ ] `C-UX-64` `capability` Anything opening over the page closes on the escape key. `src: UI/UX notes, the component states paragraph`
- [ ] `C-UX-65` `ui` Unavailable is signalled by more than colour. `src: UI/UX notes, the component states paragraph`
- [ ] `C-UX-66` `ui` The amber marks a state that is unfinished rather than wrong. `src: UI/UX notes, the component states paragraph`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app serves every public route as HTML carrying content on first paint. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The app hydrates only the interactive parts of a public route over the served markup. `src: Technical requirements para 1`
- [ ] `C-TR-03` `literal` The frontend is `Nuxt 3`. `src: Technical requirements para 1`
- [ ] `C-TR-04` `literal` The HTTP API is `Fastify`. `src: Technical requirements para 1`
- [ ] `C-TR-05` `literal` The datastore holding every entry field is `PostgreSQL`. `src: Technical requirements para 1`
- [ ] `C-TR-06` `literal` Object storage in the bucket is `MinIO`. `src: Technical requirements para 1`
- [ ] `C-TR-07` `contract` The app implements desk authentication with an email, a password exchanged for a bearer token. `src: Technical requirements para 1`
- [ ] `C-TR-08` `contract` The app stores every desk password hashed rather than in plain text. `src: Technical requirements para 1`
- [ ] `C-TR-09` `literal` The app answers `GET /api/health` with `200` once ready. `src: Technical requirements para 1`
- [ ] `C-TR-10` `contract` The app logs one structured line per request to standard output. `src: Technical requirements para 1`
- [ ] `C-TR-11` `literal` A structured log line carries the method, the path, the status. `src: Technical requirements para 1`
- [ ] `C-TR-12` `constraint` The app introduces no second database behind the published entry fields. `src: Technical requirements para 2`
- [ ] `C-TR-13` `constraint` The app introduces no second object store beside the `MinIO` bucket. `src: Technical requirements para 2`
- [ ] `C-TR-14` `constraint` The app introduces no identity provider. `src: Technical requirements para 2`
- [ ] `C-TR-15` `constraint` The app introduces no mail vendor. `src: Technical requirements para 2`
- [ ] `C-TR-16` `literal` The app reads the `PostgreSQL` connection from `DATABASE_URL`. `src: Technical requirements, environment variable table`
- [ ] `C-TR-17` `literal` The app reads the `MinIO` endpoint from `STORAGE_ENDPOINT`. `src: Technical requirements, environment variable table`
- [ ] `C-TR-18` `literal` The app reads the bucket every object is written into from `STORAGE_BUCKET`. `src: Technical requirements, environment variable table`
- [ ] `C-TR-19` `literal` The app reads the access key for the bucket from `STORAGE_ACCESS_KEY`. `src: Technical requirements, environment variable table`
- [ ] `C-TR-20` `literal` The app reads the matching key value for the bucket from `STORAGE_SECRET_KEY`. `src: Technical requirements, environment variable table`
- [ ] `C-TR-21` `literal` The app answers on the origin read from `APP_PUBLIC_URL`, where the health route is reachable. `src: Technical requirements, environment variable table`
- [ ] `C-TR-22` `literal` The app reads the port the outside world uses from `APP_PUBLIC_PORT`. `src: Technical requirements, environment variable table`
- [ ] `C-TR-23` `constraint` The app hardcodes no host. `src: Technical requirements para 3`
- [ ] `C-TR-24` `constraint` The app downloads no copy of `PostgreSQL`. `src: Technical requirements, the running services paragraph`
- [ ] `C-TR-25` `constraint` The app starts no copy of `MinIO`. `src: Technical requirements, the running services paragraph`
- [ ] `C-TR-26` `constraint` The bucket is closed to an anonymous caller. `src: Technical requirements, the object reads paragraph`
- [ ] `C-TR-27` `capability` The app streams every picture from the bucket itself, resolving the owning entry state as the app answers. `src: Technical requirements, the object reads paragraph`
- [ ] `C-TR-28` `constraint` The app hands the browser no time-limited link that keeps resolving after an entry is unpublished. `src: Technical requirements, the object reads paragraph`
- [ ] `C-TR-29` `constraint` Two simultaneous publish attempts naming one web address admit exactly one winner. `src: Technical requirements, the concurrency paragraph`
- [ ] `C-TR-30` `capability` The losing publish attempt on a contended slug names the collision. `src: Technical requirements, the concurrency paragraph`
- [ ] `C-TR-31` `constraint` No entry is left half-published after two concurrent publish attempts on one slug. `src: Technical requirements, the concurrency paragraph`
- [ ] `C-TR-32` `constraint` Saving one entry twice in a row leaves one entry. `src: Technical requirements, the concurrency paragraph`
- [ ] `C-TR-33` `capability` The second save of one entry is the state that stands. `src: Technical requirements, the concurrency paragraph`
- [ ] `C-TR-34` `literal` The largest piece of content on the home surface paints in under 2.5 seconds on a fourth-generation mobile connection. `src: Technical requirements, the performance paragraph`
- [ ] `C-TR-35` `literal` No surface shifts its layout by more than a tenth of a viewport as content arrives. `src: Technical requirements, the performance paragraph`
- [ ] `C-TR-36` `literal` An interaction paints its next frame in under two hundred milliseconds. `src: Technical requirements, the performance paragraph`
- [ ] `C-TR-37` `literal` The compressed JavaScript the home surface delivers stays under 180KB. `src: Technical requirements, the performance paragraph`
- [ ] `C-TR-38` `literal` No more than three requests block first paint on the home surface. `src: Technical requirements, the performance paragraph`
- [ ] `C-TR-39` `literal` The place index pages at 24 records. `src: Technical requirements, the performance paragraph`
- [ ] `C-TR-40` `literal` The photo gallery pages at 24 records. `src: Technical requirements, the performance paragraph`
- [ ] `C-TR-41` `constraint` The header motion layer blocks no first paint. `src: Technical requirements, the media weight paragraph`
- [ ] `C-TR-42` `capability` The poster frame of the header motion layer is part of the initial response. `src: Technical requirements, the media weight paragraph`
- [ ] `C-TR-43` `constraint` Only the header still with the first row of cards loads eagerly. `src: Technical requirements, the media weight paragraph`
- [ ] `C-TR-44` `constraint` Publishing then unpublishing one entry leaves a single entry row. `src: Technical requirements, the concurrency paragraph`
- [ ] `C-TR-45` `constraint` No lossless still ships for a photographic image. `src: Technical requirements, the media weight paragraph`
- [ ] `C-TR-46` `constraint` The app writes no log file. `src: Technical requirements para 1`
- [ ] `C-TR-47` `constraint` The app uses no log service. `src: Technical requirements para 1`
- [ ] `C-TR-48` `constraint` The app introduces no cache. `src: Technical requirements para 2`
- [ ] `C-TR-49` `constraint` The app introduces no queue. `src: Technical requirements para 2`
- [ ] `C-TR-50` `constraint` The app uses only the libraries named in the brief plus their direct dependencies. `src: Technical requirements para 2`
- [ ] `C-TR-51` `constraint` The app downloads, installs, compiles or starts no copy of `PostgreSQL`. `src: Technical requirements, the running services paragraph`
- [ ] `C-TR-52` `constraint` The app downloads, installs, compiles or starts no copy of `MinIO`. `src: Technical requirements, the running services paragraph`
- [ ] `C-TR-53` `capability` The app streams every guide document from the bucket itself, resolving the owning entry state as the app answers. `src: Technical requirements para 5`
- [ ] `C-TR-54` `contract` The app reaches the `MinIO` bucket an uploaded object lands in at its environment variables. `src: Technical requirements, the running services paragraph`
- [ ] `C-TR-55` `constraint` Every still below the fold loads lazily. `src: Technical requirements, the media weight paragraph`
- [ ] `C-TR-56` `constraint` Every still is delivered responsively. `src: Technical requirements, the media weight paragraph`

## C-DM Data model

- [ ] `C-DM-01` `data` The app holds seven tables, one per entity. `src: Data model para 1`
- [ ] `C-DM-02` `data` The app stores every timestamp in UTC, so an event ending today is read against a UTC day. `src: Data model para 1`
- [ ] `C-DM-03` `literal` The app accepts the password `deku-demo-pw-2026` for every seeded account. `src: Data model para 2`
- [ ] `C-DM-04` `contract` The app writes each seeded account beside the password into `/app/USER_README.md`. `src: Data model para 2`
- [ ] `C-DM-05` `data` The app stores an editor row with an `id`, an `email`, a `password_hash`. `src: Data model, editors`
- [ ] `C-DM-06` `data` The app keeps the editor `email` unique. `src: Data model, editors`
- [ ] `C-DM-07` `literal` The app seeds one editor row at `editor@example.com`. `src: Data model, editors`
- [ ] `C-DM-08` `data` The app stores a seeded collection row with an `id`, a `slug`, a `name`, a `standfirst`. `src: Data model, collections`
- [ ] `C-DM-09` `data` The app keeps the seeded collection `slug` unique. `src: Data model, collections`
- [ ] `C-DM-10` `literal` The app seeds the collection slugs `coastline`, `highlands`, `backwater` behind the collections endpoint. `src: Data model, collections`
- [ ] `C-DM-11` `ui` The `standfirst` of a collection renders under the name of the collection. `src: Data model, collections`
- [ ] `C-DM-12` `data` The app stores the entry fields `slug`, `name`, `summary`, `guide`, `state`, `featured`, `sort_index`. `src: Data model, entries`
- [ ] `C-DM-13` `data` The app stores the fact panel values `transport_point`, `best_months`, `distance_km` on an entry row. `src: Data model, entries`
- [ ] `C-DM-14` `data` The app stores `created_at`, `updated_at` so the index sorts by the most recent entry first. `src: Data model, entries`
- [ ] `C-DM-15` `data` The app stores the fact `distance_km` of a place entry as an integer. `src: Data model, entries`
- [ ] `C-DM-16` `constraint` The app carries no owner column on an entry. `src: Data model, entries`
- [ ] `C-DM-17` `capability` The app derives the published count on the index head on read. `src: Data model, entries`
- [ ] `C-DM-18` `capability` The app derives the picture count on the desk list on read. `src: Data model, entries`
- [ ] `C-DM-19` `capability` The app derives the byte size on a guide document card from the stored object on read. `src: Data model, entries`
- [ ] `C-DM-20` `capability` The app derives the month headings of the calendar on read. `src: Data model, entries`
- [ ] `C-DM-21` `capability` The app derives the related row of a place on read. `src: Data model, entries`
- [ ] `C-DM-22` `constraint` One entry holds a given `slug` at any time, so a publish naming a taken slug is refused. `src: Data model invariant 1`
- [ ] `C-DM-23` `constraint` A publish attempt whose slug is already held changes nothing. `src: Data model invariant 1`
- [ ] `C-DM-24` `constraint` Exactly one of two publish attempts arriving at once on a given slug wins. `src: Data model invariant 1`
- [ ] `C-DM-25` `constraint` An entry comes into existence in state `draft`. `src: Data model invariant 2`
- [ ] `C-DM-26` `constraint` No public response carries an entry in state `draft` under any query string. `src: Data model invariant 3`
- [ ] `C-DM-27` `constraint` The public membership of a collection is exactly the published entries joined to the collection. `src: Data model invariant 4`
- [ ] `C-DM-28` `data` The app joins entries to collections through an `entry_collections` row carrying `entry_id`, `collection_id`. `src: Data model, entry_collections`
- [ ] `C-DM-29` `data` The app keeps the `entry_id` with `collection_id` pair unique. `src: Data model, entry_collections`
- [ ] `C-DM-30` `data` The app stores an image row carrying `object_key` from the upload scheme, plus `alt_text`, `width`, `height`, `position`. `src: Data model, images`
- [ ] `C-DM-31` `data` The app requires a picture description in `alt_text` on an image row. `src: Data model, images`
- [ ] `C-DM-32` `data` The app stores the intrinsic `width` with the intrinsic `height` of an image so a still reserves its space before arriving. `src: Data model, images`
- [ ] `C-DM-33` `data` The app orders the picture strip of an entry by the stored `position` of each picture. `src: Data model, images`
- [ ] `C-DM-34` `data` The app stores a brochure row carrying `id`, `entry_id`, `object_key`, `title`, `page_count`. `src: Data model, brochures`
- [ ] `C-DM-35` `data` The app leaves `entry_id` null on a regional guide document. `src: Data model, brochures`
- [ ] `C-DM-36` `data` The app reads `page_count` from the document at upload. `src: Data model, brochures`
- [ ] `C-DM-37` `data` The app reads `byte_size` from the stored object when a card is rendered. `src: Data model, brochures`
- [ ] `C-DM-38` `data` The app stores an event row carrying `id`, `entry_id`, `name`, `description`, `starts_on`, `ends_on`. `src: Data model, events`
- [ ] `C-DM-39` `data` The app allows a missing `ends_on` date on an event row. `src: Data model, events`
- [ ] `C-DM-40` `data` Each calendar row under its month heading names the event with the place the event happens at. `src: Data model, events`
- [ ] `C-DM-41` `literal` The app seeds nine entries, eight `published` with one `draft`. `src: Data model, seed data`
- [ ] `C-DM-42` `literal` The app seeds the published slugs `alder-cove`, `thistle-bay`, `rook-hollow`, `penmara`. `src: Data model, seed data table`
- [ ] `C-DM-43` `literal` The app seeds the published slugs `glasswater`, `highfen`, `saltmere`, `brindle-tor`. `src: Data model, seed data table`
- [ ] `C-DM-44` `literal` The app seeds the draft place `Ossary Fen` at the slug `ossary-fen`. `src: Data model, seed data table`
- [ ] `C-DM-45` `literal` The app seeds `Alder Cove` with a picture count of 3 carrying the guide document `Alder Cove on Foot`. `src: Data model, seed data table`
- [ ] `C-DM-46` `literal` The app seeds the draft `Ossary Fen` with 3 pictures carrying the guide document `Ossary Fen in Winter`. `src: Data model, seed data table`
- [ ] `C-DM-47` `literal` The app seeds six entries flagged `featured` at sort indexes 1 through 6. `src: Data model, seed data table`
- [ ] `C-DM-48` `literal` The app seeds 20 pictures, 17 on published entries with 3 on the draft entry. `src: Data model, seed data para`
- [ ] `C-DM-49` `constraint` Every seeded picture carries a non-empty description. `src: Data model, seed data para`
- [ ] `C-DM-50` `literal` The app seeds three regional guide documents named `Marnavel in Three Days`, `The Coast Road`, `Backwater Passages`. `src: Data model, seed data para`
- [ ] `C-DM-51` `literal` The app seeds the event `Penmara Kite Days` at Penmara already ended before today. `src: Data model, seed data event table`
- [ ] `C-DM-52` `literal` The app seeds the event `Highfen Harvest Fair` at Highfen ending today. `src: Data model, seed data event table`
- [ ] `C-DM-53` `literal` The app seeds the event `Thistle Bay Regatta` with a start date of today plus 2 carrying a missing end date. `src: Data model, seed data event table`
- [ ] `C-DM-54` `literal` The app seeds the event `Alder Lantern Nights` at Alder Cove with a start date of today plus 9. `src: Data model, seed data event table`
- [ ] `C-DM-55` `constraint` Seeding is idempotent, so restarting the app duplicates none of the seeded places. `src: Data model, seed data closing`
- [ ] `C-DM-56` `literal` The seeded `Coastline` collection lists `alder-cove`, `thistle-bay`, `penmara`, `saltmere`. `src: Data model, seed data table`
- [ ] `C-DM-57` `literal` The seeded `Highlands` collection lists `rook-hollow`, `highfen`, `brindle-tor`. `src: Data model, seed data table`
- [ ] `C-DM-58` `literal` The seeded `Backwater` collection lists `thistle-bay`, `glasswater`, `saltmere`. `src: Data model, seed data table`
- [ ] `C-DM-59` `literal` The app seeds the fact panel of the place `Alder Cove` with `Alder Halt`, `May to September`, a distance of 12. `src: Data model, seed data fact panel table`
- [ ] `C-DM-60` `literal` The app seeds the fact panel of the place `Saltmere` with `Saltmere Halt`, `April to September`, a distance of 19. `src: Data model, seed data fact panel table`
- [ ] `C-DM-61` `literal` The app renders `distance_km` as the integer followed by a space with `km`, so `Alder Cove` reads `12 km`. `src: Data model, seed data fact panel table`
- [ ] `C-DM-62` `data` The app carries `published_count` on each row the collections endpoint returns. `src: Deployment contract, API shapes table`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The primary accent, a mid, vivid orange, carries the hover target, the active navigation label, a warmed border. `src: Front-end specification, colour tokens by role`
- [ ] `C-FE-02` `ui` The secondary accent, a mid, vivid amber, carries the home eyebrow with a badge fill. `src: Front-end specification, colour tokens by role`
- [ ] `C-FE-03` `ui` The card ground on a section band sits on a near-white neutral one step below the page ground. `src: Front-end specification, colour tokens by role`
- [ ] `C-FE-04` `ui` The alternating band ground sits a hair off the section ground. `src: Front-end specification, colour tokens by role`
- [ ] `C-FE-05` `ui` The card border takes a near-white neutral below the card ground. `src: Front-end specification, colour tokens by role`
- [ ] `C-FE-06` `ui` The input field border with the table rule takes a near-white cool neutral. `src: Front-end specification, colour tokens by role`
- [ ] `C-FE-07` `ui` Secondary body text in the collection introduction takes a deep neutral. `src: Front-end specification, colour tokens by role`
- [ ] `C-FE-08` `ui` A caption such as the month abbreviation on a date block takes a mid cool neutral. `src: Front-end specification, colour tokens by role`
- [ ] `C-FE-09` `ui` Disabled text with placeholder text takes a light cool neutral. `src: Front-end specification, colour tokens by role`
- [ ] `C-FE-10` `ui` A card on the desk carries one soft drop shadow, offset downward, blurred, dark at roughly a third opacity. `src: Front-end specification, colour tokens closing`
- [ ] `C-FE-11` `ui` A divider rule below a card is a hairline in a near-white neutral. `src: Front-end specification, colour tokens closing`
- [ ] `C-FE-12` `literal` The display family `Playfair Display` falls back to `Georgia, "Times New Roman", serif`. `src: Front-end specification, the two type families`
- [ ] `C-FE-13` `literal` `IBM Plex Sans Condensed` falls back to `system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif`. `src: Front-end specification, the two type families`
- [ ] `C-FE-14` `constraint` Naming a hosted family adds no asset dependency to the build. `src: Front-end specification, type closing`
- [ ] `C-FE-15` `literal` Body default type in the reading column is 16px at a 24px line height. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-16` `literal` A lead paragraph such as the library standfirst is 18px at a 27px line height. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-17` `literal` Metadata on a place card is 14px at a 21px line height. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-18` `literal` A navigation label is 14px at a 14px line height. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-19` `literal` An eyebrow with a badge is 13px at an 11.7px line height, below the display heading. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-20` `literal` Long form guide text is 16px at a 32px line height. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-21` `literal` A place card title is 20px at a 24px line height. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-22` `literal` The top section heading step is 28px at a 33.6px line height. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-23` `literal` The middle section heading step is 26.74px at a 32.088px line height. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-24` `literal` The bottom section heading step is 23.14px at a 27.768px line height. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-25` `literal` Footer fine print is 12px at an 18px line height. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-26` `constraint` The three heading steps are one clamped rule rather than three declarations, the place index heading among them. `src: Front-end specification, type scale closing`
- [ ] `C-FE-27` `ui` One product radius carries cards, inputs, buttons, the event row. `src: Front-end specification, radius`
- [ ] `C-FE-28` `ui` A tighter inner radius carries a control nested inside a composer field. `src: Front-end specification, radius`
- [ ] `C-FE-29` `ui` A softer media radius carries gallery tiles with the picture strip. `src: Front-end specification, radius`
- [ ] `C-FE-30` `ui` An outline button with the floating scroll control is a full pill. `src: Front-end specification, radius`
- [ ] `C-FE-31` `ui` A close button with a social mark is a circle. `src: Front-end specification, radius`
- [ ] `C-FE-32` `literal` Five breakpoints are named `sm`, `md`, `lg`, `xl`, `xxl` in ascending order. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-33` `ui` The content column is centred with a gutter stepping at each breakpoint. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-34` `ui` The grid is twelve columns wide, the reading column taking some of them. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-35` `ui` In-flow content sits at the base of the stacking order. `src: Front-end specification, elevation`
- [ ] `C-FE-36` `ui` A sticky filter bar sits just above the in-flow content in the stacking order. `src: Front-end specification, elevation`
- [ ] `C-FE-37` `ui` The global header sits above the floating scroll control in the stacking order. `src: Front-end specification, elevation`
- [ ] `C-FE-38` `ui` The navigation drawer sits over the backdrop in the stacking order. `src: Front-end specification, elevation`
- [ ] `C-FE-39` `ui` The lightbox modal opened from a tile sits over the drawer in the stacking order. `src: Front-end specification, elevation`
- [ ] `C-FE-40` `ui` The toast stack sits in front of everything in the stacking order. `src: Front-end specification, elevation`
- [ ] `C-FE-41` `constraint` Eleven inline vector marks are drawn from coordinates in the build. `src: Front-end specification, iconography`
- [ ] `C-FE-42` `constraint` No icon font ships with the build. `src: Front-end specification, iconography`
- [ ] `C-FE-43` `ui` The search control mark in the header is one circle with a line for its handle. `src: Front-end specification, interface marks`
- [ ] `C-FE-44` `ui` The menu mark is three lines evenly spaced on the vertical. `src: Front-end specification, interface marks`
- [ ] `C-FE-45` `ui` The arrow mark is one path plus one heavier line in the accent orange. `src: Front-end specification, interface marks`
- [ ] `C-FE-46` `ui` The rotation of the arrow mark is baked into the drawn geometry rather than applied at run time. `src: Front-end specification, interface marks`
- [ ] `C-FE-47` `ui` The progress ring is one unfilled circular path driven by its dash offset. `src: Front-end specification, interface marks`
- [ ] `C-FE-48` `ui` The progress ring reads as tracking the scroll position rather than as an animation. `src: Front-end specification, interface marks`
- [ ] `C-FE-49` `ui` Seven social marks in the footer render at one square box, evenly spaced on the horizontal. `src: Front-end specification, social marks`
- [ ] `C-FE-50` `ui` The two viewBox families of the social marks align optically on one baseline. `src: Front-end specification, social marks`
- [ ] `C-FE-51` `ui` Each social mark carries an accessible name naming its destination network. `src: Front-end specification, social marks`
- [ ] `C-FE-52` `ui` The header is fixed to the top of the viewport, spanning the full width. `src: Front-end specification, header`
- [ ] `C-FE-53` `ui` The pale header ground is a very shallow vertical lift between two near-white neutrals. `src: Front-end specification, header`
- [ ] `C-FE-54` `ui` The header carries the wordmark, the primary navigation, the search control from left to right. `src: Front-end specification, header`
- [ ] `C-FE-55` `ui` The menu mark takes the place of the navigation below the `lg` tier. `src: Front-end specification, header`
- [ ] `C-FE-56` `literal` The primary navigation carries five labels `Places`, `Themes`, `What is on`, `Guides`, `Gallery`. `src: Front-end specification, header`
- [ ] `C-FE-57` `ui` The active navigation label takes the accent orange. `src: Front-end specification, header`
- [ ] `C-FE-58` `ui` A navigation label transitions its colour gently rather than snapping. `src: Front-end specification, header`
- [ ] `C-FE-59` `ui` The drawer enters from the right over a backdrop fading to half opacity. `src: Front-end specification, navigation drawer`
- [ ] `C-FE-60` `ui` The navigation drawer rests offscreen, travelling on the horizontal alone. `src: Front-end specification, navigation drawer`
- [ ] `C-FE-61` `ui` The footer ground is the deep neutral with body text in white at the metadata size. `src: Front-end specification, footer`
- [ ] `C-FE-62` `ui` The footer carries four link columns. `src: Front-end specification, footer`
- [ ] `C-FE-63` `literal` The footer carries the enquiry address `visit@example.com`. `src: Front-end specification, footer`
- [ ] `C-FE-64` `ui` The footer carries a fine print line at the smallest size. `src: Front-end specification, footer`
- [ ] `C-FE-65` `ui` A footer link moves from white to the accent orange on hover. `src: Front-end specification, footer`
- [ ] `C-FE-66` `ui` The privacy page with the terms page is linked from a footer column on every surface. `src: Front-end specification, footer`
- [ ] `C-FE-67` `ui` The not-found surface carries a heading at the top type step over one sentence of explanation. `src: Front-end specification, not-found surface`
- [ ] `C-FE-68` `ui` The not-found surface carries a single pill button back to the home surface. `src: Front-end specification, not-found surface`
- [ ] `C-FE-69` `capability` A floating control pinned to the viewport edge stays reachable at a narrow width, opening an accessibility panel. `src: Front-end specification, accessibility control`
- [ ] `C-FE-70` `capability` The accessibility panel offers a text size increase, a contrast inversion, a reset. `src: Front-end specification, accessibility control`
- [ ] `C-FE-71` `capability` The state of the accessibility control survives navigation within a session. `src: Front-end specification, accessibility control`
- [ ] `C-FE-72` `constraint` The accessibility control is the first focusable element after the skip link. `src: Front-end specification, accessibility control`
- [ ] `C-FE-73` `ui` Four easing characters carry the product, from decelerating entrances to accelerating exits. `src: Front-end specification, motion language`
- [ ] `C-FE-74` `ui` Position changes are symmetric in the motion set. `src: Front-end specification, motion language`
- [ ] `C-FE-75` `ui` The product default state change is a short, gently symmetric ease. `src: Front-end specification, motion language`
- [ ] `C-FE-76` `ui` The properties `color`, `background-color`, `border-color` move together on one ease wherever a control takes a hover state. `src: Front-end specification, motion language`
- [ ] `C-FE-77` `ui` The long reveal holds a pause, then travels for just under a second, decelerating. `src: Front-end specification, motion language`
- [ ] `C-FE-78` `ui` The long reveal is the only entrance in the product that waits. `src: Front-end specification, motion language`
- [ ] `C-FE-79` `ui` The drawer slide with the toast entrance is a short decelerating travel. `src: Front-end specification, motion language`
- [ ] `C-FE-80` `ui` The lightbox backdrop fades on close as a short linear opacity ramp. `src: Front-end specification, motion language`
- [ ] `C-FE-81` `ui` The ring fill is a stroke-offset change short enough to read as direct coupling to scroll. `src: Front-end specification, motion language`
- [ ] `C-FE-82` `ui` The nudge moves a failing field out one way, further back the other, a smaller correction, then home. `src: Front-end specification, motion language`
- [ ] `C-FE-83` `ui` The fade out runs the opacity of a leaving toast to nothing. `src: Front-end specification, motion language`
- [ ] `C-FE-84` `ui` No spinner, progress stripe or placeholder glow is required of the build. `src: Front-end specification, motion language`
- [ ] `C-FE-85` `ui` The scroll indicator ring is pinned bottom right, above in-flow content, below the header. `src: Front-end specification, scroll indicator`
- [ ] `C-FE-86` `ui` The scroll indicator rests slightly below its final position, lifting into place on first scroll. `src: Front-end specification, scroll indicator`
- [ ] `C-FE-87` `ui` The scroll indicator stroke fills in proportion to document scroll progress. `src: Front-end specification, scroll indicator`
- [ ] `C-FE-88` `capability` Pressing the scroll indicator at the foot of the grid returns to the top of the document. `src: Front-end specification, scroll indicator`
- [ ] `C-FE-89` `ui` The home header is a full-bleed motion panel occupying the viewport below the header bar. `src: Front-end specification, header media`
- [ ] `C-FE-90` `ui` The home header motion layer is muted, looping, playing inline, with no controls. `src: Front-end specification, header media`
- [ ] `C-FE-91` `ui` A scrim runs corner to corner over the home header motion layer. `src: Front-end specification, header media`
- [ ] `C-FE-92` `constraint` The poster frame is the final state where the home header motion layer cannot play through. `src: Front-end specification, header media`
- [ ] `C-FE-93` `capability` Every still loads behind a generated blur placeholder produced from its own average colour at build time. `src: Front-end specification, progressive stills`
- [ ] `C-FE-94` `capability` Each still is delivered at a minimum of three widths with a size declaration matching the five breakpoints. `src: Front-end specification, progressive stills`
- [ ] `C-FE-95` `constraint` Each still declares its intrinsic width with its intrinsic height so no layout shift occurs. `src: Front-end specification, progressive stills`
- [ ] `C-FE-96` `ui` A tile that zooms on hover scales its inner image alone, keeping its frame clipping. `src: Front-end specification, media radius and framing`
- [ ] `C-FE-97` `ui` The picture strip beneath a place heading carries a soft inset shadow along its top. `src: Front-end specification, detail strip`
- [ ] `C-FE-98` `capability` The picture strip scrolls horizontally on touch, by drag on pointer. `src: Front-end specification, detail strip`
- [ ] `C-FE-99` `ui` The scrollbar of the picture strip is hidden with its keyboard scrolling kept. `src: Front-end specification, detail strip`
- [ ] `C-FE-100` `ui` The home bands run header media, header content, triptych, featured row, events strip, guide promotion, gallery teaser, footer. `src: Front-end specification, surface home`
- [ ] `C-FE-101` `ui` The triptych, the events strip, the gallery teaser sit on the section ground. `src: Front-end specification, surface home`
- [ ] `C-FE-102` `ui` The featured row with the guide promotion sits on the page ground. `src: Front-end specification, surface home`
- [ ] `C-FE-103` `ui` The home header content is left aligned, vertically centred, at seven twelfths of the grid on a wide screen. `src: Front-end specification, surface home header content`
- [ ] `C-FE-104` `literal` The home eyebrow reads `PLAN YOUR VISIT` in the secondary amber. `src: Front-end specification, surface home header content`
- [ ] `C-FE-105` `ui` The home display heading sits at the top type step in the display serif in white. `src: Front-end specification, surface home header content`
- [ ] `C-FE-106` `ui` The home pill button carries a transparent ground with a hairline white border. `src: Front-end specification, surface home header content`
- [ ] `C-FE-107` `ui` The three home text elements enter on the long reveal, staggered in band order. `src: Front-end specification, surface home header content`
- [ ] `C-FE-108` `ui` The home pill button is present from first paint rather than animating in. `src: Front-end specification, surface home header content`
- [ ] `C-FE-109` `ui` The home pill button inverts to a white ground with a deep cool neutral label on hover. `src: Front-end specification, surface home header content`
- [ ] `C-FE-110` `ui` The triptych is three cards in a row on a wide screen, stacked below the `md` tier. `src: Front-end specification, surface home triptych`
- [ ] `C-FE-111` `ui` A themed triptych card carries a still, a title at the card-title size, a one-line description in the mid cool neutral. `src: Front-end specification, surface home triptych`
- [ ] `C-FE-112` `ui` A triptych card lifts slightly on the vertical on hover with its title taking the accent orange. `src: Front-end specification, surface home triptych`
- [ ] `C-FE-113` `constraint` A fourth collection beside the three seeded collections appears in no triptych. `src: Front-end specification, surface home triptych`
- [ ] `C-FE-114` `ui` The featured row draws up to six place cards flagged `featured`, ordered by sort index ascending. `src: Front-end specification, surface home featured row`
- [ ] `C-FE-115` `constraint` The featured row pads nothing where fewer than six entries carry the flag. `src: Front-end specification, surface home featured row`
- [ ] `C-FE-116` `constraint` The whole featured band is omitted where no entry carries the flag. `src: Front-end specification, surface home featured row`
- [ ] `C-FE-117` `capability` The upcoming events strip carries the next four events by start date ascending. `src: Front-end specification, surface home events strip`
- [ ] `C-FE-118` `ui` An events strip item carries a date block, the event name at the card-title size, a place name in the mid cool neutral. `src: Front-end specification, surface home events strip`
- [ ] `C-FE-119` `ui` A link at the foot of the events strip leads to the calendar. `src: Front-end specification, surface home events strip`
- [ ] `C-FE-120` `ui` The guide promotion is a two column band pairing a still with a heading, two sentences, a pill button. `src: Front-end specification, surface home guide promotion`
- [ ] `C-FE-121` `ui` The gallery teaser is eight tiles in a masonry arrangement linking to the photo gallery. `src: Front-end specification, surface home gallery teaser`
- [ ] `C-FE-122` `ui` The place index head carries a breadcrumb, a heading at the top type step, a count line in the mid cool neutral. `src: Front-end specification, surface place index`
- [ ] `C-FE-123` `ui` A breadcrumb link above the place grid takes the secondary deep neutral, moving to the accent orange on hover. `src: Front-end specification, surface place index`
- [ ] `C-FE-124` `ui` The filter bar is sticky beneath the global header, above in-flow content. `src: Front-end specification, surface place index`
- [ ] `C-FE-125` `ui` The name filter settles before running rather than firing on every keystroke. `src: Front-end specification, surface place index`
- [ ] `C-FE-126` `literal` The index theme filter offers `Coastline`, `Highlands`, `Backwater`, an all option. `src: Front-end specification, surface place index`
- [ ] `C-FE-127` `ui` The filter bar ground is the page ground with a hairline bottom border in the card border neutral. `src: Front-end specification, surface place index`
- [ ] `C-FE-128` `ui` A filter field carries the product radius with a hairline input border. `src: Front-end specification, surface place index`
- [ ] `C-FE-129` `constraint` The focus ring is a soft wide halo in the inline-link blue. `src: Front-end specification, surface place index`
- [ ] `C-FE-130` `ui` The place grid is three cards across at `xl`, two at `md`, one below. `src: Front-end specification, surface place index`
- [ ] `C-FE-131` `ui` A place card carries a still at the media radius, the name at the card-title size, theme badges, a summary truncated to two lines. `src: Front-end specification, surface place index`
- [ ] `C-FE-132` `ui` The place entry head is a full width still at three fifths of the viewport height under the home header scrim. `src: Front-end specification, surface place entry`
- [ ] `C-FE-133` `ui` The place name sits over the head still at the top type step in the display serif in white. `src: Front-end specification, surface place entry`
- [ ] `C-FE-134` `ui` The place entry body is two columns on a wide screen, a single column below. `src: Front-end specification, surface place entry`
- [ ] `C-FE-135` `ui` The main column of a place entry takes eight twelfths, carrying the guide text at the long-form size. `src: Front-end specification, surface place entry`
- [ ] `C-FE-136` `ui` A guide subheading sits at the bottom type step in the display serif. `src: Front-end specification, surface place entry`
- [ ] `C-FE-137` `ui` Paragraph spacing in the guide text is one line height. `src: Front-end specification, surface place entry`
- [ ] `C-FE-138` `ui` The side column of a place entry takes four twelfths, sticky on a wide screen. `src: Front-end specification, surface place entry`
- [ ] `C-FE-139` `ui` The fact panel sits on the section ground at the product radius. `src: Front-end specification, surface place entry`
- [ ] `C-FE-140` `ui` A fact panel label sits at the eyebrow size in the mid cool neutral above a value at the body size. `src: Front-end specification, surface place entry`
- [ ] `C-FE-141` `ui` The picture strip sits between the body with the related row. `src: Front-end specification, surface place entry`
- [ ] `C-FE-142` `ui` The collection head is a full width still at two fifths of the viewport height under the same scrim. `src: Front-end specification, surface themed collection`
- [ ] `C-FE-143` `ui` The collection name sits over the head still at the top type step in white. `src: Front-end specification, surface themed collection`
- [ ] `C-FE-144` `ui` A breadcrumb link over the collection still takes white, moving to the accent orange on hover. `src: Front-end specification, surface themed collection`
- [ ] `C-FE-145` `ui` The collection introduction is two to four paragraphs in a single centred column of six twelfths. `src: Front-end specification, surface themed collection`
- [ ] `C-FE-146` `ui` A collection card border moves from a near-white neutral to the accent orange on hover. `src: Front-end specification, surface themed collection`
- [ ] `C-FE-147` `ui` The calendar head carries a breadcrumb, a heading, a count line reading the number of upcoming events. `src: Front-end specification, surface events calendar`
- [ ] `C-FE-148` `ui` The calendar breadcrumb takes white over its dark ground, moving to the accent orange on hover. `src: Front-end specification, surface events calendar`
- [ ] `C-FE-149` `ui` Month headings sit at the bottom type step in the display serif. `src: Front-end specification, surface events calendar`
- [ ] `C-FE-150` `ui` The month groups are real headings so a screen reader jumps between months. `src: Front-end specification, surface events calendar`
- [ ] `C-FE-151` `ui` An event row is a horizontal card at the product radius on the page ground with a hairline border. `src: Front-end specification, surface events calendar`
- [ ] `C-FE-152` `ui` The date block of an event row is a fixed square on the section ground carrying the day numeral over the month abbreviation. `src: Front-end specification, surface events calendar`
- [ ] `C-FE-153` `ui` The date block carries the start day with a range indicator where an event spans days. `src: Front-end specification, surface events calendar`
- [ ] `C-FE-154` `ui` The centre of an event row carries the event name, the place name, a description truncated to two lines. `src: Front-end specification, surface events calendar`
- [ ] `C-FE-155` `ui` The still on an event row card sits at the product radius at about a sixth of the width on a wide screen. `src: Front-end specification, surface events calendar`
- [ ] `C-FE-156` `ui` The border with the name of a hovered event row both take the accent orange. `src: Front-end specification, surface events calendar`
- [ ] `C-FE-157` `ui` The head with the count line reading zero remain where no upcoming event exists. `src: Front-end specification, surface events calendar`
- [ ] `C-FE-158` `ui` The library head carries a breadcrumb, a heading, two sentences of standfirst in an eight twelfths column. `src: Front-end specification, surface brochure library`
- [ ] `C-FE-159` `ui` The library grid is four cards across at `xl`, three at `lg`, two at `md`, one below. `src: Front-end specification, surface brochure library`
- [ ] `C-FE-160` `ui` A library card carries a cover still at the product radius in a three by four aspect ratio. `src: Front-end specification, surface brochure library`
- [ ] `C-FE-161` `ui` A library card carries a metadata line at the eyebrow size in the mid cool neutral. `src: Front-end specification, surface brochure library`
- [ ] `C-FE-162` `ui` A library card carries a pill download control. `src: Front-end specification, surface brochure library`
- [ ] `C-FE-163` `ui` The gallery masonry keeps each still's own aspect ratio at four columns on a wide screen. `src: Front-end specification, surface photo gallery`
- [ ] `C-FE-164` `ui` The masonry gutter between tiles is one grid gutter at every breakpoint. `src: Front-end specification, surface photo gallery`
- [ ] `C-FE-165` `ui` The still opened from a tile is fitted to the lightbox viewport with a margin of one grid gutter. `src: Front-end specification, surface photo gallery`
- [ ] `C-FE-166` `ui` The lightbox caption bar carries the place name at the body size in a heavier cut. `src: Front-end specification, surface photo gallery`
- [ ] `C-FE-167` `ui` The lightbox close control is a circle at half opacity, rising to full on hover. `src: Front-end specification, surface photo gallery`
- [ ] `C-FE-168` `capability` The lightbox closes on a backdrop press. `src: Front-end specification, surface photo gallery`
- [ ] `C-FE-169` `ui` The desk sign-in card is a single centred card at the product radius on the page ground with the card shadow. `src: Front-end specification, surface editor desk`
- [ ] `C-FE-170` `ui` The sign-in card holds an email field, a password field, a submit control. `src: Front-end specification, surface editor desk`
- [ ] `C-FE-171` `ui` A failed sign-in sets both field borders to the failure red. `src: Front-end specification, surface editor desk`
- [ ] `C-FE-172` `ui` The terms page is linked from the foot of the desk sign-in card. `src: Front-end specification, surface editor desk`
- [ ] `C-FE-173` `ui` The live badge on the desk list takes the success teal with white text. `src: Front-end specification, surface editor desk`
- [ ] `C-FE-174` `ui` The draft badge on the desk list takes the amber with deep cool neutral text. `src: Front-end specification, surface editor desk`
- [ ] `C-FE-175` `ui` The desk chrome introduces no token the public surfaces do not already define. `src: Front-end specification, surface editor desk`
- [ ] `C-FE-176` `capability` Pictures with the guide document go to the object store, leaving the app holding the resulting object identifiers. `src: Front-end specification, surface editor desk upload`
- [ ] `C-FE-177` `constraint` Every attached picture upload finishes before the entry may be published. `src: Front-end specification, surface editor desk upload`
- [ ] `C-FE-178` `ui` A publish with an unpublish is confirmed by a toast. `src: Front-end specification, surface editor desk publish`
- [ ] `C-FE-179` `ui` The component architecture is nine shared modules. `src: Front-end specification, shared components`
- [ ] `C-FE-180` `ui` The place card takes one entry with a variant that governs which fields render alone. `src: Front-end specification, shared components`
- [ ] `C-FE-181` `ui` The toast stack is pinned bottom right, entering on a short decelerating travel. `src: Front-end specification, toast`
- [ ] `C-FE-182` `ui` A success toast carries a left border in the success teal, a failure toast in the failure red. `src: Front-end specification, toast`
- [ ] `C-FE-183` `literal` A toast dismisses after five seconds or on press. `src: Front-end specification, toast`
- [ ] `C-FE-184` `literal` The toast stack holds at most three, a fourth displacing the oldest. `src: Front-end specification, toast`
- [ ] `C-FE-185` `constraint` Nothing on the public side raises a toast. `src: Front-end specification, toast`
- [ ] `C-FE-186` `constraint` A view receiving an entry carries no state check of its own. `src: Front-end specification, data boundaries`
- [ ] `C-FE-187` `capability` The editor surfaces read both states through a separate authenticated path. `src: Front-end specification, data boundaries`
- [ ] `C-FE-188` `literal` The featured row runs one column below `md`, two at `md`, three at `lg`, four at `xl`. `src: Front-end specification, column counts by surface`
- [ ] `C-FE-189` `literal` The gallery masonry runs one column below `md`, two at `md`, three at `lg`, four at `xl`. `src: Front-end specification, column counts by surface`
- [ ] `C-FE-190` `literal` The event row is stacked below `lg`, horizontal at `lg` with `xl`. `src: Front-end specification, column counts by surface`
- [ ] `C-FE-191` `capability` The primary navigation becomes the drawer below the `lg` tier. `src: Front-end specification, responsive behaviour`
- [ ] `C-FE-192` `capability` The place entry side column moves from sticky beside the body to inline beneath the body below `lg`. `src: Front-end specification, responsive behaviour`
- [ ] `C-FE-193` `constraint` The still on an event row is absent from the response below the `md` tier rather than hidden. `src: Front-end specification, responsive behaviour`
- [ ] `C-FE-194` `capability` A print stylesheet is supplied for the place entry surface alone. `src: Front-end specification, print`
- [ ] `C-FE-195` `capability` The print stylesheet removes the chrome, sets the side column inline, reduces the picture strip to its first still. `src: Front-end specification, print`
- [ ] `C-FE-196` `capability` The print stylesheet prints link destinations after their labels. `src: Front-end specification, print`
- [ ] `C-FE-197` `constraint` No photograph, film, icon file, font file or compressed texture ships with the build. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-198` `capability` The motion header is a generated loop of three horizontal bands drifting at coprime rates behind a slow vertical gradient. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-199` `capability` Every still is a generated two-point radial gradient keyed by a seed derived from the entry slug. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-200` `constraint` The same entry always produces the same still, so the grid reshuffles no colours between builds. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-201` `capability` The grain is an inline vector turbulence filter, desaturated, composited at low opacity. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-202` `capability` A guide document is generated at seed time carrying a cover, a contents page, one page per picture description. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-203` `literal` The navigation labels read `Places`, `Themes`, `What is on`, `Guides`, `Gallery`. `src: Front-end specification, copy global chrome`
- [ ] `C-FE-204` `literal` The search control label reads `Search the guide`. `src: Front-end specification, copy global chrome`
- [ ] `C-FE-205` `literal` The menu mark label reads `Open menu`. `src: Front-end specification, copy global chrome`
- [ ] `C-FE-206` `literal` The footer legal line reads `Marnavel Coast Board. All rights reserved.` `src: Front-end specification, copy global chrome`
- [ ] `C-FE-207` `literal` The social label reads `Follow Marnavel Coast Board`. `src: Front-end specification, copy global chrome`
- [ ] `C-FE-208` `literal` The skip link reads `Skip to content`. `src: Front-end specification, copy global chrome`
- [ ] `C-FE-209` `literal` The home heading reads `Take the long way through Marnavel`. `src: Front-end specification, copy home`
- [ ] `C-FE-210` `literal` The home lead sentence opens `Eight places worth the detour,` before naming the best month. `src: Front-end specification, copy home`
- [ ] `C-FE-211` `literal` The home call to action reads `Start exploring`. `src: Front-end specification, copy home`
- [ ] `C-FE-212` `literal` The home band headings read `Three ways in`, `Worth the detour`, `Coming up`, `In pictures`. `src: Front-end specification, copy home`
- [ ] `C-FE-213` `literal` The guide promotion heading reads `Take the guide with you`. `src: Front-end specification, copy home`
- [ ] `C-FE-214` `literal` The guide promotion call to action reads `Download the guide`. `src: Front-end specification, copy home`
- [ ] `C-FE-215` `literal` The index heading reads `Every place in the guide`. `src: Front-end specification, copy place index`
- [ ] `C-FE-216` `literal` The index count line reads `{n} places`. `src: Front-end specification, copy place index`
- [ ] `C-FE-217` `literal` The index filter labels read `Filter by name` with `All themes`. `src: Front-end specification, copy place index`
- [ ] `C-FE-218` `literal` The index sort labels read `Name, A to Z` with `Recently added`. `src: Front-end specification, copy place index`
- [ ] `C-FE-219` `literal` The index empty control reads `Clear filter`. `src: Front-end specification, copy place index`
- [ ] `C-FE-220` `literal` The fact panel labels read `Nearest station`, `Best months`, `Distance`. `src: Front-end specification, copy place index`
- [ ] `C-FE-221` `literal` The related row heading pairs the word `Nearby` with the word `alike`. `src: Front-end specification, copy place index`
- [ ] `C-FE-222` `literal` The events heading reads `What is on in Marnavel`. `src: Front-end specification, copy collections events`
- [ ] `C-FE-223` `literal` The events count line reads `{n} coming up`. `src: Front-end specification, copy collections events`
- [ ] `C-FE-224` `literal` The events empty control reads `Browse places`. `src: Front-end specification, copy collections events`
- [ ] `C-FE-225` `literal` The events date range joiner reads `to`. `src: Front-end specification, copy collections events`
- [ ] `C-FE-226` `literal` The library heading reads `Guides to download`. `src: Front-end specification, copy collections events`
- [ ] `C-FE-227` `literal` The library standfirst below its heading opens `Printed companions to the places`. `src: Front-end specification, copy collections events`
- [ ] `C-FE-228` `literal` The library metadata line reads `{n} pages, {size} MB`. `src: Front-end specification, copy collections events`
- [ ] `C-FE-229` `literal` The library download control reads `Download`. `src: Front-end specification, copy collections events`
- [ ] `C-FE-230` `literal` The photo-gallery heading reads `Marnavel in pictures`. `src: Front-end specification, copy collections events`
- [ ] `C-FE-231` `literal` The paging control at the foot of the gallery grid reads `Show more`. `src: Front-end specification, copy collections events`
- [ ] `C-FE-232` `literal` The lightbox controls read `Close`, `Previous picture`, `Next picture`. `src: Front-end specification, copy collections events`
- [ ] `C-FE-233` `literal` The lightbox link label carries the words `Read about` ahead of the place name. `src: Front-end specification, copy collections events`
- [ ] `C-FE-234` `literal` The sign-in card heading reads `Sign in to the desk`. `src: Front-end specification, copy editor desk`
- [ ] `C-FE-235` `literal` The desk list heading reads `Entries`. `src: Front-end specification, copy editor desk`
- [ ] `C-FE-236` `literal` The desk filter controls read `All`, `Live`, `Draft`. `src: Front-end specification, copy editor desk`
- [ ] `C-FE-237` `literal` The desk badges read `Live` with `Draft`. `src: Front-end specification, copy editor desk`
- [ ] `C-FE-238` `literal` The composer field labels read `Place name`, `Web address`, `Summary`, `The guide`. `src: Front-end specification, copy editor desk`
- [ ] `C-FE-239` `literal` The composer field labels read `Themes, up to three`, `Show on the front page`, `Pictures`, `Guide document`. `src: Front-end specification, copy editor desk`
- [ ] `C-FE-240` `literal` The picture description label opens with the verb `Describe`. `src: Front-end specification, copy editor desk`
- [ ] `C-FE-241` `literal` The desk controls read `Save draft`, `Publish`, `Return to draft`, `New entry`. `src: Front-end specification, copy editor desk`
- [ ] `C-FE-242` `literal` The refusal shown during an attached picture upload reads `Wait for the uploads to finish.` `src: Front-end specification, copy editor desk`
- [ ] `C-FE-243` `literal` The description refusal reads `Describe every picture before publishing.` `src: Front-end specification, copy editor desk`
- [ ] `C-FE-244` `literal` The saved toast reads `Saved.` `src: Front-end specification, copy editor desk`
- [ ] `C-FE-245` `literal` The not-found heading reads `We cannot find that page`. `src: Front-end specification, copy errors`
- [ ] `C-FE-246` `literal` The not-found surface body carries the phrase `may have moved`. `src: Front-end specification, copy errors`
- [ ] `C-FE-247` `literal` The not-found control reads `Back to the guide`. `src: Front-end specification, copy errors`
- [ ] `C-FE-248` `literal` The failure message for an attached picture reads `That upload did not finish.` `src: Front-end specification, copy errors`
- [ ] `C-FE-249` `literal` The privacy heading reads `What we record`. `src: Front-end specification, copy errors`
- [ ] `C-FE-250` `literal` The terms heading reads `Using the guide`. `src: Front-end specification, copy errors`
- [ ] `C-FE-251` `constraint` A font swap reflows no heading. `src: Front-end specification, type`
- [ ] `C-FE-252` `ui` The still fade runs on the same short linear opacity ramp as the backdrop fade. `src: Front-end specification, motion language`
- [ ] `C-FE-253` `ui` The scroll indicator carries a soft two-part drop shadow. `src: Front-end specification, scroll indicator`
- [ ] `C-FE-254` `ui` A needed loading affordance is carried by one of the named motion moments. `src: Front-end specification, motion language`
- [ ] `C-FE-255` `literal` Body default type in the reading column is 16px at 400 with a 24px line height. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-256` `literal` A navigation label is 14px at 700. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-257` `literal` A place card title is 20px at 600. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-258` `literal` A month heading is a section step at 500 in the display family. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-259` `literal` An eyebrow is 13px at 700. `src: Front-end specification, the rendered type scale`
- [ ] `C-FE-260` `ui` The collection index head carries a breadcrumb, a heading at the top type step, one sentence of standfirst. `src: Front-end specification, surface themed collection index`
- [ ] `C-FE-261` `ui` The collection index body is three cards in a row at the `lg` tier, stacked below `md`. `src: Front-end specification, surface themed collection index`
- [ ] `C-FE-262` `constraint` The collection index renders no empty state, because the set is fixed at three. `src: Front-end specification, surface themed collection index`
- [ ] `C-FE-263` `literal` The collection index heading reads `Three ways into Marnavel`. `src: Front-end specification, copy collections events`
- [ ] `C-FE-264` `literal` The collection index count reads `{n} places`. `src: Front-end specification, copy collections events`
- [ ] `C-FE-265` `ui` The footer column **Places** holds `Places`, `Themes`, `Gallery`. `src: Front-end specification, footer`
- [ ] `C-FE-266` `ui` The footer column **Plan** holds `What is on`, `Guides`. `src: Front-end specification, footer`
- [ ] `C-FE-267` `ui` The footer column **Board** holds `Enquiries`, `Privacy`. `src: Front-end specification, footer`
- [ ] `C-FE-268` `ui` The footer column **Legal** holds `Terms` with the fine print. `src: Front-end specification, footer`
- [ ] `C-FE-269` `capability` The desk sends the bytes of an uploaded picture to the issued target rather than through the app. `src: Technical requirements, the object writes paragraph`
- [ ] `C-FE-270` `constraint` The composer offers no field for a guide document cover. `src: Core features rule 23`
- [ ] `C-FE-271` `capability` A document registered with no picture of any kind still shows a cover. `src: Core features rule 23`
- [ ] `C-FE-272` `capability` A retried upload reuses the `object_key` the first attempt was issued. `src: Core features rule 33`
- [ ] `C-FE-273` `ui` The `Enquiries` string is the Board column heading over the enquiry address rather than a link. `src: Front-end specification, footer`
- [ ] `C-FE-274` `capability` Publishing shows the entry on the home surface only where the entry is flagged `featured`. `src: Front-end specification, surface editor desk publish`
- [ ] `C-FE-275` `ui` The cover of a guide document carries the place name set in the display family over the generated page. `src: Front-end specification, Media system`
- [ ] `C-FE-276` `literal` The events strip call to action reads `See the full calendar`. `src: Front-end specification, Copy`
- [ ] `C-FE-277` `literal` The index empty message reads `Nothing matches that. Try a different theme, or clear the filter.`. `src: Front-end specification, Copy`
- [ ] `C-FE-278` `literal` The collection index standfirst reads `Every place in the guide sits in one of these three, or in none of them.`. `src: Front-end specification, Copy`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app serves one board with one region. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The app carries no tenancy. `src: Constraints bullet 1`
- [ ] `C-CN-03` `constraint` The app carries no translation. `src: Constraints bullet 1`
- [ ] `C-CN-04` `constraint` The app carries no availability. `src: Constraints bullet 2`
- [ ] `C-CN-05` `constraint` The app carries no itineraries. `src: Constraints bullet 3`
- [ ] `C-CN-06` `constraint` The app carries no editor-created collection beside the three seeded collections. `src: Constraints bullet 4`
- [ ] `C-CN-07` `constraint` The app carries no editor-created event. `src: Constraints bullet 4`
- [ ] `C-CN-08` `constraint` The app carries no second editor role. `src: Constraints bullet 5`
- [ ] `C-CN-09` `constraint` The app carries no approval step. `src: Constraints bullet 5`
- [ ] `C-CN-10` `constraint` The app carries no per-entry ownership. `src: Constraints bullet 5`
- [ ] `C-CN-11` `constraint` The app carries no mail service. `src: Constraints bullet 6`
- [ ] `C-CN-12` `constraint` The app carries no full-text index. `src: Constraints bullet 7`
- [ ] `C-CN-13` `constraint` The app carries no consent banner. `src: Constraints bullet 8`
- [ ] `C-CN-14` `constraint` The app makes no third-party network call at run time beyond the font service. `src: Constraints bullet 8`
- [ ] `C-CN-15` `constraint` The app carries no offline mode. `src: Constraints bullet 9`
- [ ] `C-CN-16` `constraint` The app ships no binary asset. `src: Constraints bullet 10`
- [ ] `C-CN-17` `ui` The app carries no scroll-scrubbed animation. `src: Constraints bullet 11`
- [ ] `C-CN-18` `literal` The app stays responsive with the seeded 9 places, 20 pictures, 5 guide documents, 4 events. `src: Constraints bullet 12`
- [ ] `C-CN-19` `literal` The app stays responsive at 90 entries, 200 pictures, 40 events. `src: Constraints bullet 12`
- [ ] `C-CN-20` `constraint` The app serves one language. `src: Constraints bullet 1`
- [ ] `C-CN-21` `constraint` The app carries no second board. `src: Constraints bullet 1`
- [ ] `C-CN-22` `constraint` The app carries no price. `src: Constraints bullet 2`
- [ ] `C-CN-23` `constraint` The app carries no favourite. `src: Constraints bullet 3`
- [ ] `C-CN-24` `constraint` The app carries no saved trip. `src: Constraints bullet 3`
- [ ] `C-CN-25` `constraint` The app carries no search beyond the name filter of the place index. `src: Constraints bullet 7`
- [ ] `C-CN-26` `constraint` The app collects no analytics. `src: Constraints bullet 8`
- [ ] `C-CN-27` `constraint` The app carries no cookie choice. `src: Constraints bullet 8`
- [ ] `C-CN-28` `constraint` The app carries no native application. `src: Constraints bullet 9`
- [ ] `C-CN-29` `constraint` The app carries no background worker. `src: Constraints bullet 9`
- [ ] `C-CN-30` `ui` The progress ring is the only scroll-coupled property in the product. `src: Constraints bullet 11`
- [ ] `C-CN-31` `constraint` The one third-party request the product makes at run time is the font service. `src: Constraints bullet 8`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The app maps the port as `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `literal` The app listens on the container-internal port `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The app reads both the origin with the port from the environment rather than hardcoding either. `src: Deployment contract bullet 1`
- [ ] `C-DC-05` `contract` The app answers the health route with every API route on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-06` `literal` The app answers `GET /api/health` with `200` once ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-07` `contract` The app starts from the environment image with no manual step. `src: Deployment contract bullet 4`
- [ ] `C-DC-08` `contract` The app writes the login credentials to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-09` `contract` The app leaves an empty `.browser_screenshots/` directory at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-10` `contract` The app leaves an empty `.downloads/` directory at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-11` `contract` The app serves a production build behind a static or preview server. `src: Deployment contract bullet 7`
- [ ] `C-DC-12` `contract` The server keeps running after the build session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-13` `contract` The server runs as no child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-14` `contract` The app binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-15` `constraint` The app binds neither `127.0.0.1` nor `localhost`. `src: Deployment contract bullet 9`
- [ ] `C-DC-16` `contract` The app reaches the backing service holding the published entry fields at its environment variable. `src: Deployment contract bullet 10`
- [ ] `C-DC-17` `constraint` The app starts no copy of a named backing service. `src: Deployment contract bullet 10`
- [ ] `C-DC-18` `constraint` The app writes an uploaded object to no provider beside the bucket named in the brief. `src: Deployment contract bullet 11`
- [ ] `C-DC-19` `constraint` The app carries no edge function. `src: Deployment contract bullet 11`
- [ ] `C-DC-20` `constraint` The app carries no persistent volume. `src: Deployment contract, the volumes and networks bullet`
- [ ] `C-DC-21` `constraint` The app carries no fixed container name. `src: Deployment contract, the volumes and networks bullet`
- [ ] `C-DC-22` `constraint` The app carries no custom network. `src: Deployment contract, the volumes and networks bullet`
- [ ] `C-DC-23` `literal` The app answers `GET /api/entries` with a top-level JSON array of published entries. `src: Deployment contract, API shapes table`
- [ ] `C-DC-24` `literal` The place index accepts the filter keys `theme`, `name`, `sort`, `page` on `GET /api/entries`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-25` `literal` An entry in the `GET /api/entries` array carries `id`, `slug`, `name`, `summary`, `featured`, `sort_index`, `themes`, `images`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-26` `literal` The app answers `GET /api/entries/{slug}` with one published entry carrying `guide`, `related`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-27` `literal` The app answers `404` at `GET /api/entries/{slug}` for a draft or absent entry. `src: Deployment contract, API shapes table`
- [ ] `C-DC-28` `literal` The app returns a top-level array carrying `slug`, `name`, `standfirst` at `GET /api/collections`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-29` `literal` The app answers `GET /api/collections/{slug}` with `200` for a collection holding no published entry. `src: Deployment contract, API shapes table`
- [ ] `C-DC-30` `literal` The app answers `GET /api/events` ordered by `starts_on` ascending. `src: Deployment contract, API shapes table`
- [ ] `C-DC-31` `literal` An event in the `GET /api/events` array carries `id`, `name`, `description`, `starts_on`, `ends_on`, the place name. `src: Deployment contract, API shapes table`
- [ ] `C-DC-32` `literal` The app answers `GET /api/brochures` with the documents of published entries plus the regional ones. `src: Deployment contract, API shapes table`
- [ ] `C-DC-33` `literal` A document in the library response at `GET /api/brochures` carries `id`, `title`, `page_count`, `byte_size`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-34` `literal` The app answers the `GET /api/images` response paged at 24 with `id`, `alt_text`, `width`, `height`, the owning place `slug`, `name`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-35` `literal` The app answers `GET /api/media/images/{image_id}` with the picture bytes streamed from the bucket. `src: Deployment contract, API shapes table`
- [ ] `C-DC-36` `literal` The app answers `GET /api/media/brochures/{brochure_id}` with a download filename drawn from the guide document title. `src: Deployment contract, API shapes table`
- [ ] `C-DC-37` `literal` The app answers `POST /api/auth/login` with an `access_token` for the desk editor. `src: Deployment contract, API shapes table`
- [ ] `C-DC-38` `literal` The app answers `GET /api/desk/entries` with an array of the entries the `state` filter selects. `src: Deployment contract, API shapes table`
- [ ] `C-DC-39` `literal` The app answers `POST /api/desk/entries` with a created entry in state `draft`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-40` `literal` The app answers `PATCH /api/desk/entries/{id}` with the entry produced by saving. `src: Deployment contract, API shapes table`
- [ ] `C-DC-41` `literal` The app answers `POST /api/desk/entries/{id}/publish` with the entry published or a refusal naming the failing condition. `src: Deployment contract, API shapes table`
- [ ] `C-DC-42` `literal` The app answers `POST /api/desk/entries/{id}/unpublish` with the place in state `draft`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-43` `literal` The app answers `POST /api/desk/uploads` with a scoped expiring target naming the `object_key` from the scheme. `src: Deployment contract, API shapes table`
- [ ] `C-DC-44` `literal` The app answers `POST /api/desk/images` with the registered picture naming its bucket object. `src: Deployment contract, API shapes table`
- [ ] `C-DC-45` `literal` The app answers `POST /api/desk/brochures` with `page_count` plus `byte_size` read from the stored object. `src: Deployment contract, API shapes table`
- [ ] `C-DC-46` `constraint` No public endpoint accepts a state parameter. `src: Deployment contract, API shapes closing paragraph`
- [ ] `C-DC-47` `constraint` Every endpoint under `/api/desk/` requires the bearer token. `src: Deployment contract, API shapes closing paragraph`
- [ ] `C-DC-48` `constraint` A malformed or unauthorized desk call is rejected as a client error rather than a server error. `src: Deployment contract, API shapes closing paragraph`
- [ ] `C-DC-49` `constraint` An unauthorized desk call is denied rather than answered as a silent success. `src: Deployment contract, API shapes closing paragraph`
- [ ] `C-DC-50` `constraint` An in-memory pictures array stands in for no stored object. `src: Deployment contract, no mocks`
- [ ] `C-DC-51` `constraint` Bytes written to the filesystem of the app container stand in for no object in the bucket. `src: Deployment contract, no mocks`
- [ ] `C-DC-52` `constraint` Bytes stored in a database column stand in for no object in the bucket. `src: Deployment contract, no mocks`
- [ ] `C-DC-53` `constraint` A `byte_size` the app computed once, then stored, stands in for no reading of the object. `src: Deployment contract, no mocks`
- [ ] `C-DC-54` `constraint` A publicly-readable bucket with an unguessable key denies no anonymous caller. `src: Deployment contract, no mocks`
- [ ] `C-DC-55` `constraint` The app hardcodes no port. `src: Deployment contract bullet 1`
- [ ] `C-DC-56` `literal` The app takes `POST /api/desk/uploads` with the keys `entry_id`, `kind`, `filename`, `content_type`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-57` `literal` The app answers `POST /api/desk/uploads` with the keys `url`, `method`, `headers`, `object_key`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-58` `literal` The app takes `POST /api/auth/login` with the keys `email`, `password`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-59` `literal` Each row of the desk list carries `id`, `slug`, `name`, `state`, `themes`, `picture_count`, `updated_at`. `src: Deployment contract, API shapes table`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `editor@example.com` | The app seeds one editor account at `editor@example.com` | C-RL-34 | User roles, seeded account table |
| `deku-demo-pw-2026` | The app accepts the password `deku-demo-pw-2026` for the seeded editor account | C-RL-35 | User roles, seeded account table |
| `published` | The app spells the state of a seeded published place `published` in lowercase | C-CF-02 | Core features para 1 |
| `draft` | The app spells the draft entry state `draft` in lowercase | C-CF-03 | Core features para 1 |
| `404` | The app answers `404` at the address of a draft entry | C-CF-10 | Core features rule 2 |
| `403` | The app withholds `403` at the address of a draft entry | C-CF-12 | Core features rule 2 |
| `GET /api/media/images/{image_id}` | The app streams the bytes of a picture at `GET /api/media/images/{image_id}` | C-CF-13 | Core features rule 3 |
| `GET /api/media/brochures/{brochure_id}` | The app serves a guide document at `GET /api/media/brochures/{brochure_id}` | C-CF-14 | Core features rule 3 |
| `entries/<entry_id>/gallery/<sha256_of_bytes>.<ext>` | The app stores an uploaded picture under the key `entries/<entry_id>/gallery/<sha256_of_bytes... | C-CF-24 | Core features rule 6 |
| `entries/<entry_id>/brochure/<sha256_of_bytes>.pdf` | The app stores a guide document attached to an entry under the key `entries/<entry_id>/brochu... | C-CF-26 | Core features rule 6 |
| `regional/<brochure_id>/<sha256_of_bytes>.pdf` | The app stores a regional guide document under the key `regional/<brochure_id>/<sha256_of_byt... | C-CF-27 | Core features rule 6 |
| `desk` | The app reserves the eleven top-level segments `desk`, `api`, `media`, `event`, `brochures`, ... | C-CF-66 | Core features rule 18 |
| `api` | The app reserves the eleven top-level segments `desk`, `api`, `media`, `event`, `brochures`, ... | C-CF-66 | Core features rule 18 |
| `media` | The app reserves the eleven top-level segments `desk`, `api`, `media`, `event`, `brochures`, ... | C-CF-66 | Core features rule 18 |
| `event` | The app reserves the eleven top-level segments `desk`, `api`, `media`, `event`, `brochures`, ... | C-CF-66 | Core features rule 18 |
| `brochures` | The app reserves the eleven top-level segments `desk`, `api`, `media`, `event`, `brochures`, ... | C-CF-66 | Core features rule 18 |
| `photo-gallery` | The app reserves the eleven top-level segments `desk`, `api`, `media`, `event`, `brochures`, ... | C-CF-66 | Core features rule 18 |
| `collection` | The app reserves the eleven top-level segments `desk`, `api`, `media`, `event`, `brochures`, ... | C-CF-66 | Core features rule 18 |
| `destination` | The app reserves the eleven top-level segments `desk`, `api`, `media`, `event`, `brochures`, ... | C-CF-66 | Core features rule 18 |
| `privacy` | The app reserves the eleven top-level segments `desk`, `api`, `media`, `event`, `brochures`, ... | C-CF-66 | Core features rule 18 |
| `terms` | The app reserves the eleven top-level segments `desk`, `api`, `media`, `event`, `brochures`, ... | C-CF-66 | Core features rule 18 |
| `Coastline` | The app returns exactly three seeded collections named `Coastline`, `Highlands`, `Backwater` | C-CF-67 | Core features rule 19 |
| `Highlands` | The app returns exactly three seeded collections named `Coastline`, `Highlands`, `Backwater` | C-CF-67 | Core features rule 19 |
| `Backwater` | The app returns exactly three seeded collections named `Coastline`, `Highlands`, `Backwater` | C-CF-67 | Core features rule 19 |
| `200` | The app answers `200` for a themed collection that holds no published entry | C-CF-76 | Core features rule 21 |
| `Content-Disposition` | The app serves a guide document download with a `Content-Disposition` of `attachment` | C-CF-84 | Core features rule 24 |
| `attachment` | The app serves a guide document download with a `Content-Disposition` of `attachment` | C-CF-84 | Core features rule 24 |
| `/desk/entry/new` | The app serves the composer at `/desk/entry/new` | C-CF-106 | Core features rule 29 |
| `/desk/entry/<id>` | The app serves the composer carrying the web address field at `/desk/entry/<id>` | C-CF-107 | Core features rule 29 |
| `POST /api/auth/login` | The app takes an email with a password at `POST /api/auth/login` | C-CF-152 | Core features rule 41 |
| `access_token` | The app answers a successful desk sign-in with an `access_token` value that lands the editor ... | C-CF-153 | Core features rule 41 |
| `Authorization: Bearer <token>` | The app reads a desk request token from an `Authorization: Bearer <token>` header | C-CF-154 | Core features rule 41 |
| `POST /api/auth/logout` | The app ends the desk session at `POST /api/auth/logout`, returning the editor to the sign-in... | C-CF-156 | Core features rule 41 |
| `/collection` | The app serves the index of the three collections at `/collection` | C-CF-165 | Core features rule 19 |
| `Themes` | The `Themes` label in the header goes to `/collection` | C-CF-167 | Core features rule 19 |
| `GET /api/desk/entries/counts` | The app answers `GET /api/desk/entries/counts` with the keys `all`, `published`, `draft` | C-CF-170 | Deployment contract, API shapes table |
| `all` | The app answers `GET /api/desk/entries/counts` with the keys `all`, `published`, `draft` | C-CF-170 | Deployment contract, API shapes table |
| `Marnavel in Three Days` | The app downloads `Marnavel in Three Days` as the filename `marnavel-in-three-days.pdf` | C-CF-179 | Core features rule 24 |
| `marnavel-in-three-days.pdf` | The app downloads `Marnavel in Three Days` as the filename `marnavel-in-three-days.pdf` | C-CF-179 | Core features rule 24 |
| `GET /api/desk/entries/{id}` | The app answers `GET /api/desk/entries/{id}` with one entry in either state carrying its `ima... | C-CF-180 | Deployment contract, API shapes table |
| `images` | The app answers `GET /api/desk/entries/{id}` with one entry in either state carrying its `ima... | C-CF-180 | Deployment contract, API shapes table |
| `brochure` | The app answers `GET /api/desk/entries/{id}` with one entry in either state carrying its `ima... | C-CF-180 | Deployment contract, API shapes table |
| `picture_count` | The desk list response carries the picture count as `picture_count` on each row | C-CF-181 | Core features rule 28 |
| `?state=all` | The app selects the rows of the desk list with `?state=all`, `?state=published`, `?state=draft` | C-CF-182 | Deployment contract, API shapes table |
| `?state=published` | The app selects the rows of the desk list with `?state=all`, `?state=published`, `?state=draft` | C-CF-182 | Deployment contract, API shapes table |
| `?state=draft` | The app selects the rows of the desk list with `?state=all`, `?state=published`, `?state=draft` | C-CF-182 | Deployment contract, API shapes table |
| `/` | The app serves the home surface at `/`, carrying the footer link to the privacy page | C-UF-01 | User flow route table |
| `/destination` | The app serves the place index at `/destination` | C-UF-02 | User flow route table |
| `/destination/<slug>` | The app serves a place entry at `/destination/<slug>` | C-UF-03 | User flow route table |
| `/collection/<slug>` | The app serves a themed collection at `/collection/<slug>` | C-UF-04 | User flow route table |
| `/event` | The app serves the events calendar at `/event` | C-UF-05 | User flow route table |
| `/brochures` | The app serves the guide document library of download cards at `/brochures` | C-UF-06 | User flow route table |
| `/photo-gallery` | The app serves the photo gallery at `/photo-gallery` | C-UF-07 | User flow route table |
| `/privacy` | The app serves the privacy page at `/privacy`, linked from the footer | C-UF-08 | User flow route table |
| `/terms` | The app serves the terms page at `/terms`, linked from the footer | C-UF-09 | User flow route table |
| `/404` | The app serves the board not-found surface at `/404` | C-UF-10 | User flow route table |
| `/desk/login` | The app serves the editor sign-in card at `/desk/login` | C-UF-11 | User flow route table |
| `/desk` | The app serves the desk entry list at `/desk` | C-UF-12 | User flow route table |
| `Those details did not match. Try again.` | A failed sign-in reads `Those details did not match. Try again.` | C-UF-42 | User flow journey 6 |
| `Fill in every required field before publishing.` | A publish refused for an empty required field reads `Fill in every required field before publ... | C-UF-45 | User flow journey 8 |
| `That web address is reserved. Choose another.` | A publish refused for a reserved web address reads `That web address is reserved. Choose anot... | C-UF-46 | User flow journey 8 |
| `That web address is already taken.` | A publish refused for a taken web address reads `That web address is already taken.` | C-UF-47 | User flow journey 8 |
| `Published.` | A successful publish raises a message beginning `Published.` | C-UF-48 | User flow journey 9 |
| `Returned to draft.` | A return to draft raises a message beginning `Returned to draft.` | C-UF-50 | User flow journey 10 |
| `Nothing is in` | The empty state of a themed collection opens with `Nothing is in` | C-UF-54 | User flow, states |
| `Nothing is scheduled just now. The places are still there.` | The empty state of the events calendar reads `Nothing is scheduled just now. The places are s... | C-UF-55 | User flow, states |
| `Something went wrong at our end. Try again in a moment.` | A failed region on a surface reads `Something went wrong at our end. Try again in a moment.`,... | C-UF-58 | User flow, states |
| `Playfair Display` | Display headings take the family `Playfair Display` | C-UX-22 | UI/UX notes para 3 |
| `IBM Plex Sans Condensed` | Body, navigation, metadata, controls take the family `IBM Plex Sans Condensed` | C-UX-23 | UI/UX notes para 3 |
| `Nuxt 3` | The frontend is `Nuxt 3` | C-TR-03 | Technical requirements para 1 |
| `Fastify` | The HTTP API is `Fastify` | C-TR-04 | Technical requirements para 1 |
| `PostgreSQL` | The datastore holding every entry field is `PostgreSQL` | C-TR-05 | Technical requirements para 1 |
| `MinIO` | Object storage in the bucket is `MinIO` | C-TR-06 | Technical requirements para 1 |
| `GET /api/health` | The app answers `GET /api/health` with `200` once ready | C-TR-09 | Technical requirements para 1 |
| `DATABASE_URL` | The app reads the `PostgreSQL` connection from `DATABASE_URL` | C-TR-16 | Technical requirements, environment variable table |
| `STORAGE_ENDPOINT` | The app reads the `MinIO` endpoint from `STORAGE_ENDPOINT` | C-TR-17 | Technical requirements, environment variable table |
| `STORAGE_BUCKET` | The app reads the bucket every object is written into from `STORAGE_BUCKET` | C-TR-18 | Technical requirements, environment variable table |
| `STORAGE_ACCESS_KEY` | The app reads the access key for the bucket from `STORAGE_ACCESS_KEY` | C-TR-19 | Technical requirements, environment variable table |
| `STORAGE_SECRET_KEY` | The app reads the matching key value for the bucket from `STORAGE_SECRET_KEY` | C-TR-20 | Technical requirements, environment variable table |
| `APP_PUBLIC_URL` | The app answers on the origin read from `APP_PUBLIC_URL`, where the health route is reachable | C-TR-21 | Technical requirements, environment variable table |
| `APP_PUBLIC_PORT` | The app reads the port the outside world uses from `APP_PUBLIC_PORT` | C-TR-22 | Technical requirements, environment variable table |
| `coastline` | The app seeds the collection slugs `coastline`, `highlands`, `backwater` behind the collectio... | C-DM-10 | Data model, collections |
| `highlands` | The app seeds the collection slugs `coastline`, `highlands`, `backwater` behind the collectio... | C-DM-10 | Data model, collections |
| `backwater` | The app seeds the collection slugs `coastline`, `highlands`, `backwater` behind the collectio... | C-DM-10 | Data model, collections |
| `alder-cove` | The app seeds the published slugs `alder-cove`, `thistle-bay`, `rook-hollow`, `penmara` | C-DM-42 | Data model, seed data table |
| `thistle-bay` | The app seeds the published slugs `alder-cove`, `thistle-bay`, `rook-hollow`, `penmara` | C-DM-42 | Data model, seed data table |
| `rook-hollow` | The app seeds the published slugs `alder-cove`, `thistle-bay`, `rook-hollow`, `penmara` | C-DM-42 | Data model, seed data table |
| `penmara` | The app seeds the published slugs `alder-cove`, `thistle-bay`, `rook-hollow`, `penmara` | C-DM-42 | Data model, seed data table |
| `glasswater` | The app seeds the published slugs `glasswater`, `highfen`, `saltmere`, `brindle-tor` | C-DM-43 | Data model, seed data table |
| `highfen` | The app seeds the published slugs `glasswater`, `highfen`, `saltmere`, `brindle-tor` | C-DM-43 | Data model, seed data table |
| `saltmere` | The app seeds the published slugs `glasswater`, `highfen`, `saltmere`, `brindle-tor` | C-DM-43 | Data model, seed data table |
| `brindle-tor` | The app seeds the published slugs `glasswater`, `highfen`, `saltmere`, `brindle-tor` | C-DM-43 | Data model, seed data table |
| `Ossary Fen` | The app seeds the draft place `Ossary Fen` at the slug `ossary-fen` | C-DM-44 | Data model, seed data table |
| `ossary-fen` | The app seeds the draft place `Ossary Fen` at the slug `ossary-fen` | C-DM-44 | Data model, seed data table |
| `Alder Cove` | The app seeds `Alder Cove` with a picture count of 3 carrying the guide document `Alder Cove ... | C-DM-45 | Data model, seed data table |
| `Alder Cove on Foot` | The app seeds `Alder Cove` with a picture count of 3 carrying the guide document `Alder Cove ... | C-DM-45 | Data model, seed data table |
| `Ossary Fen in Winter` | The app seeds the draft `Ossary Fen` with 3 pictures carrying the guide document `Ossary Fen ... | C-DM-46 | Data model, seed data table |
| `featured` | The app seeds six entries flagged `featured` at sort indexes 1 through 6 | C-DM-47 | Data model, seed data table |
| `The Coast Road` | The app seeds three regional guide documents named `Marnavel in Three Days`, `The Coast Road`... | C-DM-50 | Data model, seed data para |
| `Backwater Passages` | The app seeds three regional guide documents named `Marnavel in Three Days`, `The Coast Road`... | C-DM-50 | Data model, seed data para |
| `Penmara Kite Days` | The app seeds the event `Penmara Kite Days` at Penmara already ended before today | C-DM-51 | Data model, seed data event table |
| `Highfen Harvest Fair` | The app seeds the event `Highfen Harvest Fair` at Highfen ending today | C-DM-52 | Data model, seed data event table |
| `Thistle Bay Regatta` | The app seeds the event `Thistle Bay Regatta` with a start date of today plus 2 carrying a mi... | C-DM-53 | Data model, seed data event table |
| `Alder Lantern Nights` | The app seeds the event `Alder Lantern Nights` at Alder Cove with a start date of today plus 9 | C-DM-54 | Data model, seed data event table |
| `Alder Halt` | The app seeds the fact panel of the place `Alder Cove` with `Alder Halt`, `May to September`,... | C-DM-59 | Data model, seed data fact panel table |
| `May to September` | The app seeds the fact panel of the place `Alder Cove` with `Alder Halt`, `May to September`,... | C-DM-59 | Data model, seed data fact panel table |
| `Saltmere` | The app seeds the fact panel of the place `Saltmere` with `Saltmere Halt`, `April to Septembe... | C-DM-60 | Data model, seed data fact panel table |
| `Saltmere Halt` | The app seeds the fact panel of the place `Saltmere` with `Saltmere Halt`, `April to Septembe... | C-DM-60 | Data model, seed data fact panel table |
| `April to September` | The app seeds the fact panel of the place `Saltmere` with `Saltmere Halt`, `April to Septembe... | C-DM-60 | Data model, seed data fact panel table |
| `distance_km` | The app renders `distance_km` as the integer followed by a space with `km`, so `Alder Cove` r... | C-DM-61 | Data model, seed data fact panel table |
| `km` | The app renders `distance_km` as the integer followed by a space with `km`, so `Alder Cove` r... | C-DM-61 | Data model, seed data fact panel table |
| `12 km` | The app renders `distance_km` as the integer followed by a space with `km`, so `Alder Cove` r... | C-DM-61 | Data model, seed data fact panel table |
| `Georgia, "Times New Roman", serif` | The display family `Playfair Display` falls back to `Georgia, "Times New Roman", serif` | C-FE-12 | Front-end specification, the two type families |
| `system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif` | `IBM Plex Sans Condensed` falls back to `system-ui, -apple-system, "Segoe UI", Roboto, Arial,... | C-FE-13 | Front-end specification, the two type families |
| `sm` | Five breakpoints are named `sm`, `md`, `lg`, `xl`, `xxl` in ascending order | C-FE-32 | Front-end specification, layout and breakpoints |
| `md` | Five breakpoints are named `sm`, `md`, `lg`, `xl`, `xxl` in ascending order | C-FE-32 | Front-end specification, layout and breakpoints |
| `lg` | Five breakpoints are named `sm`, `md`, `lg`, `xl`, `xxl` in ascending order | C-FE-32 | Front-end specification, layout and breakpoints |
| `xl` | Five breakpoints are named `sm`, `md`, `lg`, `xl`, `xxl` in ascending order | C-FE-32 | Front-end specification, layout and breakpoints |
| `xxl` | Five breakpoints are named `sm`, `md`, `lg`, `xl`, `xxl` in ascending order | C-FE-32 | Front-end specification, layout and breakpoints |
| `Places` | The primary navigation carries five labels `Places`, `Themes`, `What is on`, `Guides`, `Gallery` | C-FE-56 | Front-end specification, header |
| `What is on` | The primary navigation carries five labels `Places`, `Themes`, `What is on`, `Guides`, `Gallery` | C-FE-56 | Front-end specification, header |
| `Guides` | The primary navigation carries five labels `Places`, `Themes`, `What is on`, `Guides`, `Gallery` | C-FE-56 | Front-end specification, header |
| `Gallery` | The primary navigation carries five labels `Places`, `Themes`, `What is on`, `Guides`, `Gallery` | C-FE-56 | Front-end specification, header |
| `visit@example.com` | The footer carries the enquiry address `visit@example.com` | C-FE-63 | Front-end specification, footer |
| `PLAN YOUR VISIT` | The home eyebrow reads `PLAN YOUR VISIT` in the secondary amber | C-FE-104 | Front-end specification, surface home header content |
| `Search the guide` | The search control label reads `Search the guide` | C-FE-204 | Front-end specification, copy global chrome |
| `Open menu` | The menu mark label reads `Open menu` | C-FE-205 | Front-end specification, copy global chrome |
| `Marnavel Coast Board. All rights reserved.` | The footer legal line reads `Marnavel Coast Board. All rights reserved.` | C-FE-206 | Front-end specification, copy global chrome |
| `Follow Marnavel Coast Board` | The social label reads `Follow Marnavel Coast Board` | C-FE-207 | Front-end specification, copy global chrome |
| `Skip to content` | The skip link reads `Skip to content` | C-FE-208 | Front-end specification, copy global chrome |
| `Take the long way through Marnavel` | The home heading reads `Take the long way through Marnavel` | C-FE-209 | Front-end specification, copy home |
| `Eight places worth the detour,` | The home lead sentence opens `Eight places worth the detour,` before naming the best month | C-FE-210 | Front-end specification, copy home |
| `Start exploring` | The home call to action reads `Start exploring` | C-FE-211 | Front-end specification, copy home |
| `Three ways in` | The home band headings read `Three ways in`, `Worth the detour`, `Coming up`, `In pictures` | C-FE-212 | Front-end specification, copy home |
| `Worth the detour` | The home band headings read `Three ways in`, `Worth the detour`, `Coming up`, `In pictures` | C-FE-212 | Front-end specification, copy home |
| `Coming up` | The home band headings read `Three ways in`, `Worth the detour`, `Coming up`, `In pictures` | C-FE-212 | Front-end specification, copy home |
| `In pictures` | The home band headings read `Three ways in`, `Worth the detour`, `Coming up`, `In pictures` | C-FE-212 | Front-end specification, copy home |
| `Take the guide with you` | The guide promotion heading reads `Take the guide with you` | C-FE-213 | Front-end specification, copy home |
| `Download the guide` | The guide promotion call to action reads `Download the guide` | C-FE-214 | Front-end specification, copy home |
| `Every place in the guide` | The index heading reads `Every place in the guide` | C-FE-215 | Front-end specification, copy place index |
| `{n} places` | The index count line reads `{n} places` | C-FE-216 | Front-end specification, copy place index |
| `Filter by name` | The index filter labels read `Filter by name` with `All themes` | C-FE-217 | Front-end specification, copy place index |
| `All themes` | The index filter labels read `Filter by name` with `All themes` | C-FE-217 | Front-end specification, copy place index |
| `Name, A to Z` | The index sort labels read `Name, A to Z` with `Recently added` | C-FE-218 | Front-end specification, copy place index |
| `Recently added` | The index sort labels read `Name, A to Z` with `Recently added` | C-FE-218 | Front-end specification, copy place index |
| `Clear filter` | The index empty control reads `Clear filter` | C-FE-219 | Front-end specification, copy place index |
| `Nearest station` | The fact panel labels read `Nearest station`, `Best months`, `Distance` | C-FE-220 | Front-end specification, copy place index |
| `Best months` | The fact panel labels read `Nearest station`, `Best months`, `Distance` | C-FE-220 | Front-end specification, copy place index |
| `Distance` | The fact panel labels read `Nearest station`, `Best months`, `Distance` | C-FE-220 | Front-end specification, copy place index |
| `Nearby` | The related row heading pairs the word `Nearby` with the word `alike` | C-FE-221 | Front-end specification, copy place index |
| `alike` | The related row heading pairs the word `Nearby` with the word `alike` | C-FE-221 | Front-end specification, copy place index |
| `What is on in Marnavel` | The events heading reads `What is on in Marnavel` | C-FE-222 | Front-end specification, copy collections events |
| `{n} coming up` | The events count line reads `{n} coming up` | C-FE-223 | Front-end specification, copy collections events |
| `Browse places` | The events empty control reads `Browse places` | C-FE-224 | Front-end specification, copy collections events |
| `to` | The events date range joiner reads `to` | C-FE-225 | Front-end specification, copy collections events |
| `Guides to download` | The library heading reads `Guides to download` | C-FE-226 | Front-end specification, copy collections events |
| `Printed companions to the places` | The library standfirst below its heading opens `Printed companions to the places` | C-FE-227 | Front-end specification, copy collections events |
| `{n} pages, {size} MB` | The library metadata line reads `{n} pages, {size} MB` | C-FE-228 | Front-end specification, copy collections events |
| `Download` | The library download control reads `Download` | C-FE-229 | Front-end specification, copy collections events |
| `Marnavel in pictures` | The photo-gallery heading reads `Marnavel in pictures` | C-FE-230 | Front-end specification, copy collections events |
| `Show more` | The paging control at the foot of the gallery grid reads `Show more` | C-FE-231 | Front-end specification, copy collections events |
| `Close` | The lightbox controls read `Close`, `Previous picture`, `Next picture` | C-FE-232 | Front-end specification, copy collections events |
| `Previous picture` | The lightbox controls read `Close`, `Previous picture`, `Next picture` | C-FE-232 | Front-end specification, copy collections events |
| `Next picture` | The lightbox controls read `Close`, `Previous picture`, `Next picture` | C-FE-232 | Front-end specification, copy collections events |
| `Read about` | The lightbox link label carries the words `Read about` ahead of the place name | C-FE-233 | Front-end specification, copy collections events |
| `Sign in to the desk` | The sign-in card heading reads `Sign in to the desk` | C-FE-234 | Front-end specification, copy editor desk |
| `Entries` | The desk list heading reads `Entries` | C-FE-235 | Front-end specification, copy editor desk |
| `All` | The desk filter controls read `All`, `Live`, `Draft` | C-FE-236 | Front-end specification, copy editor desk |
| `Live` | The desk filter controls read `All`, `Live`, `Draft` | C-FE-236 | Front-end specification, copy editor desk |
| `Draft` | The desk filter controls read `All`, `Live`, `Draft` | C-FE-236 | Front-end specification, copy editor desk |
| `Place name` | The composer field labels read `Place name`, `Web address`, `Summary`, `The guide` | C-FE-238 | Front-end specification, copy editor desk |
| `Web address` | The composer field labels read `Place name`, `Web address`, `Summary`, `The guide` | C-FE-238 | Front-end specification, copy editor desk |
| `Summary` | The composer field labels read `Place name`, `Web address`, `Summary`, `The guide` | C-FE-238 | Front-end specification, copy editor desk |
| `The guide` | The composer field labels read `Place name`, `Web address`, `Summary`, `The guide` | C-FE-238 | Front-end specification, copy editor desk |
| `Themes, up to three` | The composer field labels read `Themes, up to three`, `Show on the front page`, `Pictures`, `... | C-FE-239 | Front-end specification, copy editor desk |
| `Show on the front page` | The composer field labels read `Themes, up to three`, `Show on the front page`, `Pictures`, `... | C-FE-239 | Front-end specification, copy editor desk |
| `Pictures` | The composer field labels read `Themes, up to three`, `Show on the front page`, `Pictures`, `... | C-FE-239 | Front-end specification, copy editor desk |
| `Guide document` | The composer field labels read `Themes, up to three`, `Show on the front page`, `Pictures`, `... | C-FE-239 | Front-end specification, copy editor desk |
| `Describe` | The picture description label opens with the verb `Describe` | C-FE-240 | Front-end specification, copy editor desk |
| `Save draft` | The desk controls read `Save draft`, `Publish`, `Return to draft`, `New entry` | C-FE-241 | Front-end specification, copy editor desk |
| `Publish` | The desk controls read `Save draft`, `Publish`, `Return to draft`, `New entry` | C-FE-241 | Front-end specification, copy editor desk |
| `Return to draft` | The desk controls read `Save draft`, `Publish`, `Return to draft`, `New entry` | C-FE-241 | Front-end specification, copy editor desk |
| `New entry` | The desk controls read `Save draft`, `Publish`, `Return to draft`, `New entry` | C-FE-241 | Front-end specification, copy editor desk |
| `Wait for the uploads to finish.` | The refusal shown during an attached picture upload reads `Wait for the uploads to finish.` | C-FE-242 | Front-end specification, copy editor desk |
| `Describe every picture before publishing.` | The description refusal reads `Describe every picture before publishing.` | C-FE-243 | Front-end specification, copy editor desk |
| `Saved.` | The saved toast reads `Saved.` | C-FE-244 | Front-end specification, copy editor desk |
| `We cannot find that page` | The not-found heading reads `We cannot find that page` | C-FE-245 | Front-end specification, copy errors |
| `may have moved` | The not-found surface body carries the phrase `may have moved` | C-FE-246 | Front-end specification, copy errors |
| `Back to the guide` | The not-found control reads `Back to the guide` | C-FE-247 | Front-end specification, copy errors |
| `That upload did not finish.` | The failure message for an attached picture reads `That upload did not finish.` | C-FE-248 | Front-end specification, copy errors |
| `What we record` | The privacy heading reads `What we record` | C-FE-249 | Front-end specification, copy errors |
| `Using the guide` | The terms heading reads `Using the guide` | C-FE-250 | Front-end specification, copy errors |
| `Three ways into Marnavel` | The collection index heading reads `Three ways into Marnavel` | C-FE-263 | Front-end specification, copy collections events |
| `See the full calendar` | The events strip call to action reads `See the full calendar` | C-FE-276 | Front-end specification, Copy |
| `Nothing matches that. Try a different theme, or clear the filter.` | The index empty message reads `Nothing matches that. Try a different theme, or clear the filt... | C-FE-277 | Front-end specification, Copy |
| `Every place in the guide sits in one of these three, or in none of them.` | The collection index standfirst reads `Every place in the guide sits in one of these three, o... | C-FE-278 | Front-end specification, Copy |
| `4173` | The app listens on the container-internal port `4173` | C-DC-03 | Deployment contract bullet 1 |
| `GET /api/entries` | The app answers `GET /api/entries` with a top-level JSON array of published entries | C-DC-23 | Deployment contract, API shapes table |
| `theme` | The place index accepts the filter keys `theme`, `name`, `sort`, `page` on `GET /api/entries` | C-DC-24 | Deployment contract, API shapes table |
| `name` | The place index accepts the filter keys `theme`, `name`, `sort`, `page` on `GET /api/entries` | C-DC-24 | Deployment contract, API shapes table |
| `sort` | The place index accepts the filter keys `theme`, `name`, `sort`, `page` on `GET /api/entries` | C-DC-24 | Deployment contract, API shapes table |
| `page` | The place index accepts the filter keys `theme`, `name`, `sort`, `page` on `GET /api/entries` | C-DC-24 | Deployment contract, API shapes table |
| `id` | An entry in the `GET /api/entries` array carries `id`, `slug`, `name`, `summary`, `featured`,... | C-DC-25 | Deployment contract, API shapes table |
| `slug` | An entry in the `GET /api/entries` array carries `id`, `slug`, `name`, `summary`, `featured`,... | C-DC-25 | Deployment contract, API shapes table |
| `summary` | An entry in the `GET /api/entries` array carries `id`, `slug`, `name`, `summary`, `featured`,... | C-DC-25 | Deployment contract, API shapes table |
| `sort_index` | An entry in the `GET /api/entries` array carries `id`, `slug`, `name`, `summary`, `featured`,... | C-DC-25 | Deployment contract, API shapes table |
| `themes` | An entry in the `GET /api/entries` array carries `id`, `slug`, `name`, `summary`, `featured`,... | C-DC-25 | Deployment contract, API shapes table |
| `GET /api/entries/{slug}` | The app answers `GET /api/entries/{slug}` with one published entry carrying `guide`, `related` | C-DC-26 | Deployment contract, API shapes table |
| `guide` | The app answers `GET /api/entries/{slug}` with one published entry carrying `guide`, `related` | C-DC-26 | Deployment contract, API shapes table |
| `related` | The app answers `GET /api/entries/{slug}` with one published entry carrying `guide`, `related` | C-DC-26 | Deployment contract, API shapes table |
| `standfirst` | The app returns a top-level array carrying `slug`, `name`, `standfirst` at `GET /api/collecti... | C-DC-28 | Deployment contract, API shapes table |
| `GET /api/collections` | The app returns a top-level array carrying `slug`, `name`, `standfirst` at `GET /api/collecti... | C-DC-28 | Deployment contract, API shapes table |
| `GET /api/collections/{slug}` | The app answers `GET /api/collections/{slug}` with `200` for a collection holding no publishe... | C-DC-29 | Deployment contract, API shapes table |
| `GET /api/events` | The app answers `GET /api/events` ordered by `starts_on` ascending | C-DC-30 | Deployment contract, API shapes table |
| `starts_on` | The app answers `GET /api/events` ordered by `starts_on` ascending | C-DC-30 | Deployment contract, API shapes table |
| `description` | An event in the `GET /api/events` array carries `id`, `name`, `description`, `starts_on`, `en... | C-DC-31 | Deployment contract, API shapes table |
| `ends_on` | An event in the `GET /api/events` array carries `id`, `name`, `description`, `starts_on`, `en... | C-DC-31 | Deployment contract, API shapes table |
| `GET /api/brochures` | The app answers `GET /api/brochures` with the documents of published entries plus the regiona... | C-DC-32 | Deployment contract, API shapes table |
| `title` | A document in the library response at `GET /api/brochures` carries `id`, `title`, `page_count... | C-DC-33 | Deployment contract, API shapes table |
| `page_count` | A document in the library response at `GET /api/brochures` carries `id`, `title`, `page_count... | C-DC-33 | Deployment contract, API shapes table |
| `byte_size` | A document in the library response at `GET /api/brochures` carries `id`, `title`, `page_count... | C-DC-33 | Deployment contract, API shapes table |
| `GET /api/images` | The app answers the `GET /api/images` response paged at 24 with `id`, `alt_text`, `width`, `h... | C-DC-34 | Deployment contract, API shapes table |
| `alt_text` | The app answers the `GET /api/images` response paged at 24 with `id`, `alt_text`, `width`, `h... | C-DC-34 | Deployment contract, API shapes table |
| `width` | The app answers the `GET /api/images` response paged at 24 with `id`, `alt_text`, `width`, `h... | C-DC-34 | Deployment contract, API shapes table |
| `height` | The app answers the `GET /api/images` response paged at 24 with `id`, `alt_text`, `width`, `h... | C-DC-34 | Deployment contract, API shapes table |
| `GET /api/desk/entries` | The app answers `GET /api/desk/entries` with an array of the entries the `state` filter selects | C-DC-38 | Deployment contract, API shapes table |
| `state` | The app answers `GET /api/desk/entries` with an array of the entries the `state` filter selects | C-DC-38 | Deployment contract, API shapes table |
| `POST /api/desk/entries` | The app answers `POST /api/desk/entries` with a created entry in state `draft` | C-DC-39 | Deployment contract, API shapes table |
| `PATCH /api/desk/entries/{id}` | The app answers `PATCH /api/desk/entries/{id}` with the entry produced by saving | C-DC-40 | Deployment contract, API shapes table |
| `POST /api/desk/entries/{id}/publish` | The app answers `POST /api/desk/entries/{id}/publish` with the entry published or a refusal n... | C-DC-41 | Deployment contract, API shapes table |
| `POST /api/desk/entries/{id}/unpublish` | The app answers `POST /api/desk/entries/{id}/unpublish` with the place in state `draft` | C-DC-42 | Deployment contract, API shapes table |
| `POST /api/desk/uploads` | The app answers `POST /api/desk/uploads` with a scoped expiring target naming the `object_key... | C-DC-43 | Deployment contract, API shapes table |
| `object_key` | The app answers `POST /api/desk/uploads` with a scoped expiring target naming the `object_key... | C-DC-43 | Deployment contract, API shapes table |
| `POST /api/desk/images` | The app answers `POST /api/desk/images` with the registered picture naming its bucket object | C-DC-44 | Deployment contract, API shapes table |
| `POST /api/desk/brochures` | The app answers `POST /api/desk/brochures` with `page_count` plus `byte_size` read from the s... | C-DC-45 | Deployment contract, API shapes table |
| `entry_id` | The app takes `POST /api/desk/uploads` with the keys `entry_id`, `kind`, `filename`, `content... | C-DC-56 | Deployment contract, API shapes table |
| `kind` | The app takes `POST /api/desk/uploads` with the keys `entry_id`, `kind`, `filename`, `content... | C-DC-56 | Deployment contract, API shapes table |
| `filename` | The app takes `POST /api/desk/uploads` with the keys `entry_id`, `kind`, `filename`, `content... | C-DC-56 | Deployment contract, API shapes table |
| `content_type` | The app takes `POST /api/desk/uploads` with the keys `entry_id`, `kind`, `filename`, `content... | C-DC-56 | Deployment contract, API shapes table |
| `url` | The app answers `POST /api/desk/uploads` with the keys `url`, `method`, `headers`, `object_key` | C-DC-57 | Deployment contract, API shapes table |
| `method` | The app answers `POST /api/desk/uploads` with the keys `url`, `method`, `headers`, `object_key` | C-DC-57 | Deployment contract, API shapes table |
| `headers` | The app answers `POST /api/desk/uploads` with the keys `url`, `method`, `headers`, `object_key` | C-DC-57 | Deployment contract, API shapes table |
| `email` | The app takes `POST /api/auth/login` with the keys `email`, `password` | C-DC-58 | Deployment contract, API shapes table |
| `password` | The app takes `POST /api/auth/login` with the keys `email`, `password` | C-DC-58 | Deployment contract, API shapes table |
| `updated_at` | Each row of the desk list carries `id`, `slug`, `name`, `state`, `themes`, `picture_count`, `... | C-DC-59 | Deployment contract, API shapes table |
| `A printed companion to every place in this guide, with maps, seasons and the roads between them. Free to download, made to be folded.` | the guide promotion body, both sentences | C-FE-120 | Front-end specification, Copy |
| `Eight places worth the detour, and the best month to see each one.` | the home lead, in full | C-FE-210 | Front-end specification, Copy |
| `Nearby and alike` | the related row heading, in full | C-FE-221 | Front-end specification, Copy |
| `Printed companions to the places in this guide. Each one folds to pocket size and needs no signal to read.` | the brochures lead, both sentences | C-FE-227 | Front-end specification, Copy |
| `Read about this place` | the lightbox link label, a fixed string with no name in it | C-FE-233 | Front-end specification, Copy |
| `Describe this picture` | the alternative-text field label, in full | C-FE-240 | Front-end specification, Copy |
| `It may have moved, or it may never have been here. The guide is still where you left it.` | the not-found body, both sentences | C-FE-246 | Front-end specification, Copy |
| `That upload did not finish. Try it again.` | the upload failure message, both sentences | C-FE-248 | Front-end specification, Copy |
| `Published. It is live now.` | the publish toast, both sentences | C-UF-48 | User flow journey 9 |
| `Returned to draft. It is no longer public.` | the unpublish toast, both sentences | C-UF-50 | User flow journey 9 |
| `Nothing is in this theme yet. It will fill up.` | the collection empty message, both sentences | C-UF-54 | Front-end specification, Copy |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the sha256 of the bytes inside an object key | C-CF-24 | the key scheme names the digest of the bytes rather than a value the brief can pin ahead of an upload |
| the standfirst sentence of each seeded collection | C-DM-11 | the brief requires a one-sentence standfirst per collection without fixing its wording |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 25 |
| User roles | 3 | 36 |
| Core features | 9 | 182 |
| User flow | 6 | 60 |
| UI and UX notes | 3 | 66 |
| Technical requirements | 9 | 56 |
| Data model | 2 | 62 |
| Front-end specification | 16 | 278 |
| Constraints | 1 | 31 |
| Deployment contract | 11 | 59 |

The middle column is the mechanical count of sentences carrying a modal or reporting verb. It understates the real obligation count, because a great many asks in this brief are stated as plain declaratives in a table row. Every section was read row by row and sentence by sentence, and the right-hand column is the result of that read rather than of the verb scan.

