# Checklist: Pixelary

Coverage target derived from instruction.md alone. Every downstream channel is joined against these ids in both directions.

Items: 356
Unpinned values flagged: 3
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` Pixelary carries a browser pixel-art editor usable with no account `src: Overview`
- [ ] `C-OV-02` `capability` Pixelary carries a community gallery built on what the editor produces `src: Overview`
- [ ] `C-OV-03` `capability` The drawing action appears in the chrome on every route `src: Overview`
- [ ] `C-OV-04` `constraint` No real-time collaborative drawing session exists in the product `src: Overview`
- [ ] `C-OV-05` `constraint` No search by uploaded image exists anywhere in the product `src: Overview`
- [ ] `C-OV-06` `capability` A published piece has a stored object plus a gallery row governing who may read either `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor with no account can draw in the editor using every tool `src: User roles`
- [ ] `C-RL-02` `role` A visitor with no account can export every format `src: User roles`
- [ ] `C-RL-03` `role` A visitor with no account is refused when publishing a piece `src: User roles`
- [ ] `C-RL-04` `role` A `reader` account is refused by the server when publishing a piece `src: User roles`
- [ ] `C-RL-05` `role` An `author` account can publish a piece `src: User roles`
- [ ] `C-RL-06` `role` An `author` account is refused when changing another author's piece `src: User roles`
- [ ] `C-RL-07` `role` An `author` account is refused when reading another author's private piece `src: User roles`
- [ ] `C-RL-08` `contract` Authorization is enforced server-side on every mutating endpoint `src: User roles`
- [ ] `C-RL-09` `role` Signup is open to anybody from the sign-in modal `src: User roles`
- [ ] `C-RL-10` `data` An account stores a date of birth rather than a computed age `src: User roles`
- [ ] `C-RL-11` `role` An account below the local age of digital consent starts in restricted mode `src: User roles`
- [ ] `C-RL-12` `role` A restricted account's profile is absent from every listing `src: User roles`
- [ ] `C-RL-13` `literal` The seeded author account is `author@example.com` `src: User roles`
- [ ] `C-RL-14` `literal` The second seeded author account is `author2@example.com` `src: User roles`
- [ ] `C-RL-15` `literal` The seeded reader account is `reader@example.com` `src: User roles`
- [ ] `C-RL-16` `literal` Every seeded account uses the password `deku-demo-pw-2026` `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `contract` `POST /api/auth/signup` returns the new account with a bearer token `src: Core features, Auth rule 1`
- [ ] `C-CF-02` `contract` `POST /api/auth/login` returns an access token plus a refresh token `src: Core features, Auth rule 2`
- [ ] `C-CF-03` `constraint` The unknown-account path returns the same message as the wrong-password path `src: Core features, Auth`
- [ ] `C-CF-04` `constraint` Signup never reveals whether an address is already registered `src: Core features, Auth`
- [ ] `C-CF-05` `capability` A refresh token rotates on every use `src: Core features, Auth rule 3`
- [ ] `C-CF-06` `capability` The editor opens with no account `src: Core features, The editor`
- [ ] `C-CF-07` `capability` The editor remains usable with no network `src: Core features, The editor`
- [ ] `C-CF-08` `capability` Converting a screen position to a document position rounds downward `src: Core features, The editor rule 1`
- [ ] `C-CF-09` `capability` Document column minus one renders as a pixel distinct from document column zero `src: Core features, The editor rule 1`
- [ ] `C-CF-10` `capability` The drawing surface backing store is sized by the device pixel ratio `src: Core features, The editor rule 2`
- [ ] `C-CF-11` `literal` Zoom runs from `0.125` to `64` `src: Core features, The editor rule 4`
- [ ] `C-CF-12` `capability` Zooming about a point is computed fresh from the pointer position every time `src: Core features, The editor rule 4`
- [ ] `C-CF-13` `capability` Upscaling at zoom one or above uses nearest neighbour `src: Core features, The editor rule 5`
- [ ] `C-CF-14` `capability` Downscaling below zoom one uses an area average `src: Core features, The editor rule 5`
- [ ] `C-CF-15` `ui` The transparency checker is drawn in document space `src: Core features, The editor rule 6`
- [ ] `C-CF-16` `ui` The pixel grid is drawn in screen space at one device pixel `src: Core features, The editor rule 6`
- [ ] `C-CF-17` `ui` The pixel grid is hidden below zoom eight `src: Core features, The editor rule 6`
- [ ] `C-CF-18` `capability` The editor offers thirteen tools each with a keyboard shortcut `src: Core features, The tools`
- [ ] `C-CF-19` `literal` Brush sizes are whole numbers from `1` to `32` `src: Core features, The tools rule 1`
- [ ] `C-CF-20` `capability` A shape outline is exactly one pixel thick everywhere `src: Core features, The tools rule 3`
- [ ] `C-CF-21` `capability` Fill writes only to the active layer `src: Core features, The tools rule 4`
- [ ] `C-CF-22` `capability` A fill whose seed already holds the target colour records no history entry `src: Core features, The tools rule 4`
- [ ] `C-CF-23` `capability` The eyedropper picks the palette index in indexed mode `src: Core features, The tools rule 5`
- [ ] `C-CF-24` `capability` A selection is a one-bit mask the size of the document `src: Core features, The tools rule 6`
- [ ] `C-CF-25` `capability` Every drawing tool is clipped to the selection mask `src: Core features, The tools rule 6`
- [ ] `C-CF-26` `capability` Marching ants pause under reduced motion `src: Core features, The tools rule 6`
- [ ] `C-CF-27` `capability` A floating selection commits on any of six named triggers `src: Core features, The tools rule 7`
- [ ] `C-CF-28` `capability` Escape cancels a floating selection restoring the source region `src: Core features, The tools rule 7`
- [ ] `C-CF-29` `capability` A committed selection move is a single history entry `src: Core features, The tools rule 7`
- [ ] `C-CF-30` `capability` Escape during a shape drag leaves no history entry `src: Core features, The tools rule 9`
- [ ] `C-CF-31` `literal` A document dimension runs from `1` to `4096` on each axis `src: Core features, The document rule 1`
- [ ] `C-CF-32` `literal` A document holds at most `4194304` pixels per frame `src: Core features, The document rule 1`
- [ ] `C-CF-33` `literal` A document holds at most `512` frames `src: Core features, The document rule 1`
- [ ] `C-CF-34` `data` A document holds at most sixty-four layers ordered back to front `src: Core features, The document rule 1`
- [ ] `C-CF-35` `data` Cels are sparse so a missing entry is the empty cel `src: Core features, The document rule 2`
- [ ] `C-CF-36` `capability` Adding a layer inserts directly above the active layer `src: Core features, The document rule 3`
- [ ] `C-CF-37` `capability` Deleting the only layer of a document is refused `src: Core features, The document rule 3`
- [ ] `C-CF-38` `capability` Locking a layer blocks every write with a surfaced refusal `src: Core features, The document rule 3`
- [ ] `C-CF-39` `capability` Merging down applies the upper layer transparency during the composite `src: Core features, The document rule 4`
- [ ] `C-CF-40` `capability` Merging leaves the lower cel untouched where the upper cel is empty `src: Core features, The document rule 4`
- [ ] `C-CF-41` `literal` A frame duration runs from `10` to `10000` milliseconds `src: Core features, The document rule 6`
- [ ] `C-CF-42` `capability` Playback is scheduled against a wall clock so lateness never accumulates `src: Core features, The document rule 6`
- [ ] `C-CF-43` `capability` One stroke produces exactly one history entry `src: Core features, The document rule 8`
- [ ] `C-CF-44` `capability` A structural change plus a pixel change from one action is one history entry `src: Core features, The document rule 8`
- [ ] `C-CF-45` `capability` Trimming crops to the bounding box across every frame plus every layer `src: Core features, The document rule 9`
- [ ] `C-CF-46` `data` An indexed pixel stores the palette index rather than the resolved colour `src: Core features, Colour and palettes rule 1`
- [ ] `C-CF-47` `capability` Editing a palette entry recolours every pixel holding that index at once `src: Core features, Colour and palettes rule 1`
- [ ] `C-CF-48` `literal` An indexed palette holds `2` to `256` entries `src: Core features, Colour and palettes rule 1`
- [ ] `C-CF-49` `capability` Deleting a palette entry remaps every pixel in the same history entry `src: Core features, Colour and palettes rule 3`
- [ ] `C-CF-50` `capability` Reordering a palette remaps pixels so the rendered image is unchanged `src: Core features, Colour and palettes rule 3`
- [ ] `C-CF-51` `capability` Quantization returns the same palette in the same order for the same input `src: Core features, Colour and palettes rule 4`
- [ ] `C-CF-52` `constraint` Error diffusion is never applied to art already in indexed mode `src: Core features, Colour and palettes rule 5`
- [ ] `C-CF-53` `capability` An export path unable to carry partial alpha states its threshold `src: Core features, Colour and palettes rule 6`
- [ ] `C-CF-54` `capability` Exporting the same document twice produces identical bytes `src: Core features, Export`
- [ ] `C-CF-55` `constraint` No export embeds a timestamp `src: Core features, Export`
- [ ] `C-CF-56` `capability` An indexed document exports as a palette image rather than truecolor `src: Core features, Export rule 2`
- [ ] `C-CF-57` `constraint` No colour profile is written into an export `src: Core features, Export rule 2`
- [ ] `C-CF-58` `capability` Export scaling uses whole factors with nearest neighbour `src: Core features, Export rule 2`
- [ ] `C-CF-59` `literal` The animated delay field has a floor of `2` hundredths of a second `src: Core features, Export rule 4`
- [ ] `C-CF-60` `capability` A sprite sheet export includes a description file naming every cell rectangle `src: Core features, Export rule 6`
- [ ] `C-CF-61` `literal` Sprite sheet padding runs from `0` to `8` transparent pixels `src: Core features, Export rule 6`
- [ ] `C-CF-62` `capability` Hidden layers are excluded from every export scope `src: Core features, Export rule 7`
- [ ] `C-CF-63` `capability` A locked layer is included in an export `src: Core features, Export rule 7`
- [ ] `C-CF-64` `capability` A document being drawn is written to the local store before anywhere else `src: Core features, Saving, offline and versions rule 1`
- [ ] `C-CF-65` `capability` Autosave writes only the tiles that changed `src: Core features, Saving, offline and versions rule 2`
- [ ] `C-CF-66` `literal` The last `20` versions of a document are retained `src: Core features, Saving, offline and versions rule 3`
- [ ] `C-CF-67` `capability` Restoring a version opens a new document rather than overwriting `src: Core features, Saving, offline and versions rule 3`
- [ ] `C-CF-68` `capability` A document existing only locally is labelled as not backed up `src: Core features, Saving, offline and versions rule 6`
- [ ] `C-CF-69` `ui` A failed store write raises a persistent banner saying saving is not working `src: Core features, Saving, offline and versions rule 6`
- [ ] `C-CF-70` `contract` `POST /api/pieces` publishes a document as a gallery piece `src: Core features, Publishing and the object store rule 1`
- [ ] `C-CF-71` `literal` A piece carries `0` to `10` tags `src: Core features, Publishing and the object store rule 1`
- [ ] `C-CF-72` `literal` Artwork is stored under the key scheme `pieces/{piece_id}/{sha256_of_bytes}.{ext}` `src: Core features, Publishing and the object store rule 2`
- [ ] `C-CF-73` `literal` Renditions are stored under the key scheme `thumbs/{piece_id}/{size}/{sha256_of_bytes}.png` `src: Core features, Publishing and the object store rule 2`
- [ ] `C-CF-74` `constraint` Artwork bytes never live on the app container filesystem `src: Core features, Publishing and the object store rule 2`
- [ ] `C-CF-75` `constraint` Artwork bytes never live in a database column `src: Core features, Publishing and the object store rule 2`
- [ ] `C-CF-76` `capability` An object is addressed by the hash of its canonical bytes `src: Core features, Publishing and the object store rule 3`
- [ ] `C-CF-77` `capability` Quota is charged per reference rather than per stored object `src: Core features, Publishing and the object store rule 3`
- [ ] `C-CF-78` `constraint` Deduplication is never surfaced to a user `src: Core features, Publishing and the object store rule 3`
- [ ] `C-CF-79` `contract` `GET /api/pieces/{id}/file` serves protected artwork only to the piece author `src: Core features, Publishing and the object store rule 4`
- [ ] `C-CF-80` `capability` A signed-out request for a private piece object is denied `src: Core features, Publishing and the object store rule 4`
- [ ] `C-CF-81` `capability` A request for a private piece object by another account is denied `src: Core features, Publishing and the object store rule 4`
- [ ] `C-CF-82` `literal` Thumbnails are generated at `64`, `128`, `256` plus `512` on the long edge `src: Core features, Publishing and the object store rule 5`
- [ ] `C-CF-83` `capability` A thumbnail uses nearest neighbour when the scale factor is whole `src: Core features, Publishing and the object store rule 5`
- [ ] `C-CF-84` `capability` A thumbnail uses an area average when the scale factor is fractional `src: Core features, Publishing and the object store rule 5`
- [ ] `C-CF-85` `capability` An animated piece receives an animated preview rendition `src: Core features, Publishing and the object store rule 5`
- [ ] `C-CF-86` `capability` Every piece receives a static poster rendition from the first frame `src: Core features, Publishing and the object store rule 5`
- [ ] `C-CF-87` `literal` An imported still image is at most `20MB` `src: Core features, Publishing and the object store rule 6`
- [ ] `C-CF-88` `capability` Upload format is decided from the leading bytes rather than the file name `src: Core features, Publishing and the object store rule 7`
- [ ] `C-CF-89` `capability` A retried publish carrying the same idempotency key creates nothing new `src: Core features, Publishing and the object store rule 9`
- [ ] `C-CF-90` `capability` Two different requests colliding on one idempotency key reject the second `src: Core features, Publishing and the object store rule 9`
- [ ] `C-CF-91` `contract` `GET /api/pieces` serves the new feed ordered by published timestamp descending `src: Core features, The gallery rule 2`
- [ ] `C-CF-92` `contract` `GET /api/pieces` serves a following feed of pieces by followed accounts `src: Core features, The gallery rule 2`
- [ ] `C-CF-93` `contract` `GET /api/pieces` serves a tag feed for one tag `src: Core features, The gallery rule 2`
- [ ] `C-CF-94` `capability` A profile feed includes the author's own private pieces only for that author `src: Core features, The gallery rule 2`
- [ ] `C-CF-95` `capability` Views never enter the popular ranking value `src: Core features, The gallery rule 3`
- [ ] `C-CF-96` `capability` The popular ranking value is recomputed on a schedule rather than on a read `src: Core features, The gallery rule 3`
- [ ] `C-CF-97` `literal` A piece needs `3` distinct engaging accounts before reaching the popular feed `src: Core features, The gallery rule 3`
- [ ] `C-CF-98` `constraint` Offset pagination is refused on every feed `src: Core features, The gallery rule 4`
- [ ] `C-CF-99` `capability` A timestamp-ordered cursor is the pair of published timestamp plus id `src: Core features, The gallery rule 4`
- [ ] `C-CF-100` `capability` The popular feed pages from a snapshot taken at the first page request `src: Core features, The gallery rule 4`
- [ ] `C-CF-101` `capability` An expired snapshot token restarts the feed at the top `src: Core features, The gallery rule 4`
- [ ] `C-CF-102` `capability` A piece hidden after a snapshot is skipped with the page backfilled `src: Core features, The gallery rule 4`
- [ ] `C-CF-103` `data` A remix records the parent piece at creation `src: Core features, The gallery rule 5`
- [ ] `C-CF-104` `capability` A remix forming a lineage cycle is refused at write time `src: Core features, The gallery rule 5`
- [ ] `C-CF-105` `capability` Deleting a parent piece leaves a tombstone carrying the author name `src: Core features, The gallery rule 5`
- [ ] `C-CF-106` `capability` Children of a deleted parent piece survive with attribution `src: Core features, The gallery rule 5`
- [ ] `C-CF-107` `capability` A remix counter counts direct children only `src: Core features, The gallery rule 5`
- [ ] `C-CF-108` `capability` Like counters are derived from their rows rather than incremented `src: Core features, The gallery rule 6`
- [ ] `C-CF-109` `capability` A view is counted at most once per viewer per piece per hour `src: Core features, The gallery rule 6`
- [ ] `C-CF-110` `capability` A bare first-level path segment resolves to an artist profile `src: Core features, Profiles and the handle namespace rule 1`
- [ ] `C-CF-111` `constraint` A reserved word can never be registered as an artist handle `src: Core features, Profiles and the handle namespace rule 1`
- [ ] `C-CF-112` `capability` Handles are compared after normalization so two identical renderings cannot coexist `src: Core features, Profiles and the handle namespace rule 3`
- [ ] `C-CF-113` `ui` A profile tab row shows counts beside the gallery, followers plus following labels `src: Core features, Profiles and the handle namespace rule 4`
- [ ] `C-CF-114` `ui` A zero count on a profile is shown rather than hidden `src: Core features, Profiles and the handle namespace rule 4`
- [ ] `C-CF-115` `role` A profile owner sees an edit control in place of the follow control `src: Core features, Profiles and the handle namespace rule 5`
- [ ] `C-CF-116` `role` A profile owner sees private work with the visibility state shown `src: Core features, Profiles and the handle namespace rule 5`
- [ ] `C-CF-117` `capability` A blocked viewer sees a profile as not found rather than as blocked `src: Core features, Profiles and the handle namespace rule 6`
- [ ] `C-CF-118` `ui` An artist with no public work shows a drawn empty state `src: Core features, Profiles and the handle namespace rule 7`
- [ ] `C-CF-119` `capability` Following is one way with no approval step `src: Core features, Following, comments and notifications rule 1`
- [ ] `C-CF-120` `capability` Blocking removes any follow in both directions `src: Core features, Following, comments and notifications rule 1`
- [ ] `C-CF-121` `capability` Muting hides content from the muter without informing the muted account `src: Core features, Following, comments and notifications rule 1`
- [ ] `C-CF-122` `literal` An account follows at most `7500` others `src: Core features, Following, comments and notifications rule 1`
- [ ] `C-CF-123` `capability` Comments thread exactly one level deep `src: Core features, Following, comments and notifications rule 2`
- [ ] `C-CF-124` `literal` A comment is editable for `300` seconds after posting `src: Core features, Following, comments and notifications rule 2`
- [ ] `C-CF-125` `capability` A deleted comment leaves a tombstone preserving the thread shape `src: Core features, Following, comments and notifications rule 2`
- [ ] `C-CF-126` `capability` Notifications collapse by the kind, the subject plus the hour bucket `src: Core features, Following, comments and notifications rule 4`
- [ ] `C-CF-127` `capability` Marking notifications read is monotonic by notification id `src: Core features, Following, comments and notifications rule 5`
- [ ] `C-CF-128` `capability` The unread notification count is derived from unread rows `src: Core features, Following, comments and notifications rule 5`
- [ ] `C-CF-129` `capability` A mention is resolved to an account once at write time `src: Core features, Following, comments and notifications rule 6`
- [ ] `C-CF-130` `capability` A mention of an account blocking the author renders as plain text `src: Core features, Following, comments and notifications rule 6`
- [ ] `C-CF-131` `capability` A newly published piece enters the `pending` moderation state `src: Core features, Moderation rule 1`
- [ ] `C-CF-132` `capability` A `pending` piece never appears in a feed, a tag listing, a search result `src: Core features, Moderation rule 1`
- [ ] `C-CF-133` `capability` A `pending` piece is visible to the author by direct link `src: Core features, Moderation rule 1`
- [ ] `C-CF-134` `data` Each piece stores a cryptographic hash plus a perceptual hash `src: Core features, Moderation rule 2`
- [ ] `C-CF-135` `constraint` A perceptual hash match never removes a piece by itself `src: Core features, Moderation rule 2`
- [ ] `C-CF-136` `capability` Reinstating a piece restores the original publication time `src: Core features, Moderation rule 4`
- [ ] `C-CF-137` `capability` Reinstating a piece restores the counters plus the remix lineage place `src: Core features, Moderation rule 4`
- [ ] `C-CF-138` `data` Every moderation action appends a row carrying the predecessor hash `src: Core features, Moderation rule 5`
- [ ] `C-CF-139` `capability` The moderation audit chain verifies end to end after concurrent actions `src: Core features, Moderation rule 5`
- [ ] `C-CF-140` `capability` Search covers titles, descriptions, tags, author names, palette names `src: Core features, Search and discovery rule 1`
- [ ] `C-CF-141` `constraint` No general search by uploaded picture is offered `src: Core features, Search and discovery rule 1`
- [ ] `C-CF-142` `literal` A tag is between `1` plus `30` clusters long after normalization `src: Core features, Search and discovery rule 2`
- [ ] `C-CF-143` `capability` Search results are permission-filtered at query time `src: Core features, Search and discovery rule 3`
- [ ] `C-CF-144` `capability` A piece made private disappears from search results `src: Core features, Search and discovery rule 3`
- [ ] `C-CF-145` `capability` An empty search result is distinguished from an unavailable index `src: Core features, Search and discovery rule 3`
- [ ] `C-CF-146` `ui` A tag directory lists curated tags each with a count plus a sample `src: Core features, Search and discovery rule 5`
- [ ] `C-CF-147` `ui` A palette directory lists palettes ordered by use count `src: Core features, Search and discovery rule 5`
- [ ] `C-CF-148` `ui` The home page carries a hero band above the filter row `src: Core features, The home page, the art centre and the not-found page rule 1`
- [ ] `C-CF-149` `ui` The hero headline is rendered in capitals, centred over the backdrop `src: Core features, The home page, the art centre and the not-found page rule 1`
- [ ] `C-CF-150` `ui` The hero credit line names the artist whose work is the backdrop `src: Core features, The home page, the art centre and the not-found page rule 2`
- [ ] `C-CF-151` `ui` The filter row carries seven entries in a fixed order `src: Core features, The home page, the art centre and the not-found page rule 3`
- [ ] `C-CF-152` `data` A curated feed is distinguishable in the data model from a computed feed `src: Core features, The home page, the art centre and the not-found page rule 3`
- [ ] `C-CF-153` `ui` The topic row carries six topic cards `src: Core features, The home page, the art centre and the not-found page rule 4`
- [ ] `C-CF-154` `ui` A topic card label sits on a dark scrim over arbitrary artwork `src: Core features, The home page, the art centre and the not-found page rule 4`
- [ ] `C-CF-155` `capability` The topic row is edited by a person rather than computed from tag popularity `src: Core features, The home page, the art centre and the not-found page rule 4`
- [ ] `C-CF-156` `ui` The art centre header carries the route title plus a count of works `src: Core features, The home page, the art centre and the not-found page rule 5`
- [ ] `C-CF-157` `capability` Every art centre filter is held in the address `src: Core features, The home page, the art centre and the not-found page rule 5`
- [ ] `C-CF-158` `ui` An art centre empty state names the filter plus an action clearing the filter `src: Core features, The home page, the art centre and the not-found page rule 5`
- [ ] `C-CF-159` `capability` Opening a piece from the grid presents an overlay with the address updated `src: Core features, The home page, the art centre and the not-found page rule 5`
- [ ] `C-CF-160` `capability` An unknown address renders the product not-found page `src: Core features, The home page, the art centre and the not-found page rule 6`
- [ ] `C-CF-161` `contract` An unknown address is answered with a not-found status `src: Core features, The home page, the art centre and the not-found page rule 6`
- [ ] `C-CF-162` `ui` The not-found page carries two characters drifting in opposition `src: Core features, The home page, the art centre and the not-found page rule 6`
- [ ] `C-CF-163` `capability` A path resembling an unresolved handle renders a distinct missing-artist page `src: Core features, The home page, the art centre and the not-found page rule 7`
- [ ] `C-CF-164` `capability` A privacy page is reachable from the footer of every page `src: Core features, The home page, the art centre and the not-found page rule 8`
- [ ] `C-CF-165` `capability` A terms page is reachable from the footer of every page `src: Core features, The home page, the art centre and the not-found page rule 8`
- [ ] `C-CF-166` `capability` The terms page is linked from the signup form `src: Core features, The home page, the art centre and the not-found page rule 8`
- [ ] `C-CF-167` `ui` A consent panel asks a first-time visitor once about non-essential cookies `src: Core features, The home page, the art centre and the not-found page rule 9`
- [ ] `C-CF-168` `ui` Refusing consent takes exactly one control matching the accepting control `src: Core features, The home page, the art centre and the not-found page rule 9`
- [ ] `C-CF-169` `constraint` The consent panel never blocks first paint `src: Core features, The home page, the art centre and the not-found page rule 9`
- [ ] `C-CF-170` `capability` Every internal link on every public route resolves `src: Core features, The home page, the art centre and the not-found page rule 10`
- [ ] `C-CF-171` `capability` Every public route carries a title plus a description of its own `src: Core features, The home page, the art centre and the not-found page rule 10`
- [ ] `C-CF-172` `capability` An embed always carries the author name plus the remix chain root `src: Core features, Embeds, the public read interface and the supporter tier rule 1`
- [ ] `C-CF-173` `constraint` Embed attribution cannot be removed by a parameter `src: Core features, Embeds, the public read interface and the supporter tier rule 1`
- [ ] `C-CF-174` `constraint` An embed sets no cookies `src: Core features, Embeds, the public read interface and the supporter tier rule 1`
- [ ] `C-CF-175` `constraint` No endpoint returns accounts by age or by location `src: Core features, Embeds, the public read interface and the supporter tier rule 3`
- [ ] `C-CF-176` `data` The product reads entitlements rather than subscriptions at the point of use `src: Core features, Embeds, the public read interface and the supporter tier rule 5`
- [ ] `C-CF-177` `constraint` No drawing tool sits behind the supporter tier `src: Core features, Embeds, the public read interface and the supporter tier rule 6`
- [ ] `C-CF-178` `constraint` No export format sits behind the supporter tier `src: Core features, Embeds, the public read interface and the supporter tier rule 6`
- [ ] `C-CF-179` `capability` A lapsed entitlement never deletes artwork `src: Core features, Embeds, the public read interface and the supporter tier rule 8`
- [ ] `C-CF-180` `capability` A lapsed account can still open, export, delete every piece `src: Core features, Embeds, the public read interface and the supporter tier rule 8`

## C-UF User flow

- [ ] `C-UF-01` `contract` The route `/` serves the hero, the filter row, the topic row, the grid `src: User flow`
- [ ] `C-UF-02` `contract` The route `/art` serves the art centre grid with filters `src: User flow`
- [ ] `C-UF-03` `contract` The route `/draw` serves the editor with no session required `src: User flow`
- [ ] `C-UF-04` `contract` The route `/piece/{id}` serves one piece with lineage plus comments `src: User flow`
- [ ] `C-UF-05` `contract` The route `/{handle}` serves an artist gallery plus profile `src: User flow`
- [ ] `C-UF-06` `contract` The route `/search` serves search over titles, tags, artists, palettes `src: User flow`
- [ ] `C-UF-07` `contract` The route `/privacy` serves the privacy page with no session required `src: User flow`
- [ ] `C-UF-08` `contract` The route `/terms` serves the terms page with no session required `src: User flow`
- [ ] `C-UF-09` `contract` The route `/notifications` requires a bearer session `src: User flow`
- [ ] `C-UF-10` `capability` A protected route reached without a session opens the sign-in modal `src: User flow, Entry and redirects`
- [ ] `C-UF-11` `capability` Signing in returns the visitor to the remembered intended route `src: User flow, Entry and redirects`
- [ ] `C-UF-12` `capability` Signing out returns the visitor to the home route `src: User flow, Entry and redirects`
- [ ] `C-UF-13` `capability` An expired token leaves the editor running with local saving intact `src: User flow, Entry and redirects`
- [ ] `C-UF-14` `capability` A signed-out visitor following a private piece link gets the not-found page `src: User flow, Entry and redirects`
- [ ] `C-UF-15` `capability` A visitor can draw, sign up in the publish modal, publish one document `src: User flow, Journey 1`
- [ ] `C-UF-16` `capability` The publish modal lists local documents with thumbnails before any upload `src: User flow, Journey 1`
- [ ] `C-UF-17` `constraint` No local document is uploaded until the visitor chooses that document `src: User flow, Journey 1`
- [ ] `C-UF-18` `capability` A remix opens the editor with the parent document loaded `src: User flow, Journey 2`
- [ ] `C-UF-19` `capability` Remixing raises the parent piece remix counter by one `src: User flow, Journey 2`
- [ ] `C-UF-20` `capability` An author can flip a published piece to private from the profile `src: User flow, Journey 3`
- [ ] `C-UF-21` `capability` A reader can like a piece with the count settling to the true row count `src: User flow, Journey 4`
- [ ] `C-UF-22` `capability` A third level of comment reply is never offered `src: User flow, Journey 4`
- [ ] `C-UF-23` `capability` Every list has an empty state naming the filter `src: User flow, States`
- [ ] `C-UF-24` `ui` Every grid cell reserves height before the artwork arrives `src: User flow, States`
- [ ] `C-UF-25` `ui` Grid images load lazily one screen ahead `src: User flow, States`
- [ ] `C-UF-26` `ui` An animated piece off screen holds the first frame without playing `src: User flow, States`
- [ ] `C-UF-27` `capability` The infinite grid appends a page exactly once per trigger crossing `src: User flow, States`
- [ ] `C-UF-28` `ui` The infinite grid exposes a load-more control reachable without a pointer `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The page ground is a near-white cool neutral `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The primary action colour is a mid, vivid blue worn by nothing else `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Confirmation is carried by a mid, soft green `src: UI/UX notes`
- [ ] `C-UX-04` `ui` A destructive or failed state is carried by a light, vivid red `src: UI/UX notes`
- [ ] `C-UX-05` `ui` A caution state is carried by a mid, vivid amber `src: UI/UX notes`
- [ ] `C-UX-06` `constraint` The unused palette families are never reached for as working colours `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Every action of consequence is painted as a colour sweep rather than a flat fill `src: UI/UX notes`
- [ ] `C-UX-08` `ui` A sweep-painted action responds to a pointer by lifting slightly, brightening `src: UI/UX notes`
- [ ] `C-UX-09` `literal` The interface text family is `Roboto` backed by the system sans stack `src: UI/UX notes`
- [ ] `C-UX-10` `literal` Body text is set at `14.4px` on a `23.04px` line `src: UI/UX notes`
- [ ] `C-UX-11` `literal` Section headings are set at `21.6px` in the heavy face `src: UI/UX notes`
- [ ] `C-UX-12` `ui` Spacing runs on one scale in even steps applied through shared utilities `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Motion uses one speed for colour changes plus a slower one for movement `src: UI/UX notes`
- [ ] `C-UX-14` `constraint` No motion is driven by the scroll position `src: UI/UX notes`
- [ ] `C-UX-15` `ui` A hover state applies only where the device has a pointer `src: UI/UX notes`
- [ ] `C-UX-16` `ui` Reduced motion replaces every entrance with the end state of that entrance `src: UI/UX notes`
- [ ] `C-UX-17` `ui` Reduced motion holds animated artwork on the first frame `src: UI/UX notes`
- [ ] `C-UX-18` `ui` Body text meets WCAG AA contrast on both grounds `src: UI/UX notes`
- [ ] `C-UX-19` `ui` The artist byline is raised to the minimum contrast passing WCAG AA `src: UI/UX notes`
- [ ] `C-UX-20` `ui` Every count carries a label for a screen reader `src: UI/UX notes`
- [ ] `C-UX-21` `ui` Every content image carries alternative text naming the piece plus the artist `src: UI/UX notes`
- [ ] `C-UX-22` `ui` A decorative mark is hidden from assistive technology `src: UI/UX notes`
- [ ] `C-UX-23` `ui` An icon-only control carries a name saying what that control does `src: UI/UX notes`
- [ ] `C-UX-24` `ui` Focus is visible on every interactive element `src: UI/UX notes`
- [ ] `C-UX-25` `ui` The open drawer traps focus, returning focus to the opening button `src: UI/UX notes`
- [ ] `C-UX-26` `ui` The editor is operable from the keyboard with arrow keys moving one pixel `src: UI/UX notes`
- [ ] `C-UX-27` `ui` At a narrow viewport nothing overflows sideways `src: UI/UX notes`
- [ ] `C-UX-28` `ui` The drawing action stays in the chrome at every viewport width `src: UI/UX notes`
- [ ] `C-UX-29` `constraint` Artwork is never cropped to fit a grid cell `src: UI/UX notes`
- [ ] `C-UX-30` `ui` Each page leads with one primary action distinct from every secondary one `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Rendered pages are built with SolidStart `src: Technical requirements`
- [ ] `C-TR-02` `contract` The JSON API is served by Express under the `/api` prefix `src: Technical requirements`
- [ ] `C-TR-03` `contract` The browser receives complete HTML for every route on first paint `src: Technical requirements`
- [ ] `C-TR-04` `contract` Relational data is persisted in PostgreSQL read from `DATABASE_URL` `src: Technical requirements`
- [ ] `C-TR-05` `contract` Artwork bytes are stored in MinIO read from `STORAGE_ENDPOINT` `src: Technical requirements`
- [ ] `C-TR-06` `literal` The object store bucket is read from `STORAGE_BUCKET` `src: Technical requirements`
- [ ] `C-TR-07` `literal` The object store credentials are read from `STORAGE_ACCESS_KEY` plus `STORAGE_SECRET_KEY` `src: Technical requirements`
- [ ] `C-TR-08` `contract` `GET /api/health` returns `200` once the app is ready `src: Technical requirements`
- [ ] `C-TR-09` `constraint` No second database, cache, queue, object store, identity provider is introduced `src: Technical requirements`
- [ ] `C-TR-10` `constraint` No credential appears in anything the browser downloads `src: Technical requirements`
- [ ] `C-TR-11` `constraint` No secret value reaches the client bundle, the markup, a source map `src: Technical requirements`
- [ ] `C-TR-12` `constraint` No third-party script ships with the application `src: Technical requirements`
- [ ] `C-TR-13` `constraint` No external network call is made at runtime `src: Technical requirements`
- [ ] `C-TR-14` `constraint` No font binary, icon font, external stylesheet ships `src: Technical requirements`
- [ ] `C-TR-15` `ui` Icons are inline geometry on a twenty-four unit grid with a two unit stroke `src: Technical requirements`
- [ ] `C-TR-16` `constraint` No binary asset ships with the build `src: Technical requirements`
- [ ] `C-TR-17` `capability` The artwork placeholder is generated deterministically from the piece id `src: Technical requirements`
- [ ] `C-TR-18` `ui` The artwork placeholder is real pixel art with a visible grid `src: Technical requirements`
- [ ] `C-TR-19` `capability` An animated placeholder is a four-frame loop from the same generator `src: Technical requirements`
- [ ] `C-TR-20` `capability` An avatar is a seeded identicon deterministic from the account id `src: Technical requirements`
- [ ] `C-TR-21` `ui` The brand mark is generated as pixel art rather than as a smooth vector `src: Technical requirements`
- [ ] `C-TR-22` `ui` Advertising space is reserved as an empty bordered region `src: Technical requirements`
- [ ] `C-TR-23` `constraint` The editor core imports nothing from the site layer `src: Technical requirements`
- [ ] `C-TR-24` `constraint` The site layer never mutates the editor document `src: Technical requirements`
- [ ] `C-TR-25` `ui` The stacking scale is six named levels ending at toast `src: Technical requirements`
- [ ] `C-TR-26` `literal` Publishing is limited to `20` pieces per `3600` seconds per account `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` All timestamps are stored in UTC `src: Data model`
- [ ] `C-DM-02` `literal` Every seeded account uses the password `deku-demo-pw-2026` at login `src: Data model`
- [ ] `C-DM-03` `data` An account row carries a unique normalized email `src: Data model`
- [ ] `C-DM-04` `data` An account row carries a handle unique after normalization `src: Data model`
- [ ] `C-DM-05` `data` A document row carries a width, a height, a mode, a frame count `src: Data model`
- [ ] `C-DM-06` `data` A piece row carries a visibility of `public`, `unlisted`, `private` `src: Data model`
- [ ] `C-DM-07` `data` A piece row carries a `moderation_state` of `pending`, `restricted`, `removed` `src: Data model`
- [ ] `C-DM-08` `data` A piece row carries a `remix_permission` of `allowed_with_attribution` among others `src: Data model`
- [ ] `C-DM-09` `data` A piece lineage is acyclic so no piece remixes a descendant of that piece `src: Data model`
- [ ] `C-DM-10` `data` A like row is unique on the account paired with the piece `src: Data model`
- [ ] `C-DM-11` `data` A comment reply references only a top-level comment `src: Data model`
- [ ] `C-DM-12` `data` A follow row is unique per pair in one direction `src: Data model`
- [ ] `C-DM-13` `data` A notification row carries a group key of kind, subject, hour bucket `src: Data model`
- [ ] `C-DM-14` `data` A moderation action row carries the predecessor hash plus its own hash `src: Data model`
- [ ] `C-DM-15` `data` A plan row carries a price of `1000` integer minor units in `usd` `src: Data model`
- [ ] `C-DM-16` `data` A page view row exists at most once per viewer per piece per hour `src: Data model`
- [ ] `C-DM-17` `literal` The seeded animated piece is titled `Harbour Lights` `src: Data model, Seed data`
- [ ] `C-DM-18` `literal` The seeded public still piece is titled `Cat In A Window` `src: Data model, Seed data`
- [ ] `C-DM-19` `literal` The seeded private piece is titled `Night Market Draft` `src: Data model, Seed data`
- [ ] `C-DM-20` `literal` The seeded second-author piece is titled `Valentine Robot` `src: Data model, Seed data`
- [ ] `C-DM-21` `literal` The seeded unlisted piece is titled `Ocean Study` `src: Data model, Seed data`
- [ ] `C-DM-22` `literal` The seeded palettes are `Harbour Eight` plus `Night Sixteen` `src: Data model, Seed data`
- [ ] `C-DM-23` `literal` The seeded topics are `Cats`, `Christmas`, `People`, `Technology`, `Valentine`, `Ocean` `src: Data model, Seed data`
- [ ] `C-DM-24` `capability` Seeding is idempotent so restarting the app duplicates no row `src: Data model, Seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The chrome carries a reduced entry set on the home route `src: Front-end specification, The chrome`
- [ ] `C-FE-02` `ui` The chrome carries the full entry set on every other route `src: Front-end specification, The chrome`
- [ ] `C-FE-03` `ui` The segmented drawing control is one pill cut into three segments `src: Front-end specification, The chrome`
- [ ] `C-FE-04` `ui` The chrome bar is fixed at the top, unchanged by scrolling `src: Front-end specification, The chrome`
- [ ] `C-FE-05` `ui` The drawer carries fourteen entries each an icon beside a label `src: Front-end specification, The drawer`
- [ ] `C-FE-06` `ui` The drawer closes by the button, by Escape, by a click on the scrim `src: Front-end specification, The drawer`
- [ ] `C-FE-07` `ui` The footer carries sixteen links in one flat list with no columns `src: Front-end specification, The footer`
- [ ] `C-FE-08` `ui` The iconography is closed at twenty-eight inline marks `src: Front-end specification, Iconography`
- [ ] `C-FE-09` `ui` An artwork card carries the counts, the title, the artist byline beneath `src: Front-end specification, The artwork card`
- [ ] `C-FE-10` `ui` An animated piece carries a badge at the card upper right `src: Front-end specification, The artwork card`
- [ ] `C-FE-11` `ui` An artist hover card opens after a pause rather than instantly `src: Front-end specification, The artwork card`
- [ ] `C-FE-12` `ui` The artist hover card shadow is cast upward `src: Front-end specification, The artwork card`
- [ ] `C-FE-13` `ui` The grid is fixed-column with a uniform gutter `src: Front-end specification, The grid`
- [ ] `C-FE-14` `ui` The profile avatar overlaps the banner lower edge `src: Front-end specification, The profile`
- [ ] `C-FE-15` `literal` The not-found headline reads `Oops!` `src: Front-end specification, The not-found page`
- [ ] `C-FE-16` `ui` Nine system messages carry the product honesty commitments unsoftened `src: Front-end specification, Copy deck`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product is single tenant with one set of accounts `src: Constraints`
- [ ] `C-CN-02` `constraint` No presence, shared cursors, shared operation log exists `src: Constraints`
- [ ] `C-CN-03` `constraint` No direct messaging between accounts exists `src: Constraints`
- [ ] `C-CN-04` `constraint` No card is taken so no invoice exists anywhere `src: Constraints`
- [ ] `C-CN-05` `constraint` No email is ever sent by the product `src: Constraints`
- [ ] `C-CN-06` `constraint` A moderation notice reaches its recipient as an in-product notification `src: Constraints`
- [ ] `C-CN-07` `constraint` No native application exists `src: Constraints`
- [ ] `C-CN-08` `constraint` Forums, the shop, hiring, groups, comics resolve to the not-found page `src: Constraints`
- [ ] `C-CN-09` `constraint` No multi-region placement exists `src: Constraints`
- [ ] `C-CN-10` `literal` The product name is `Pixelary` `src: Constraints`
- [ ] `C-CN-11` `constraint` No audience-size claim appears anywhere in the product `src: Constraints`
- [ ] `C-CN-12` `capability` The app stays responsive with two thousand pieces in the database `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173` `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the `/api` prefix `src: Deployment contract`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps `src: Deployment contract`
- [ ] `C-DC-05` `contract` Login credentials are written to `/app/USER_README.md` `src: Deployment contract`
- [ ] `C-DC-06` `contract` Reserved `.browser_screenshots/` plus `.downloads/` directories exist empty `src: Deployment contract`
- [ ] `C-DC-07` `contract` A production build is served behind a static or preview server `src: Deployment contract`
- [ ] `C-DC-08` `contract` The server keeps running after the session ends `src: Deployment contract`
- [ ] `C-DC-09` `contract` The server binds `0.0.0.0` rather than a loopback address `src: Deployment contract`
- [ ] `C-DC-10` `constraint` No backing service is downloaded, installed, compiled, started `src: Deployment contract`
- [ ] `C-DC-11` `constraint` No edge function is used `src: Deployment contract`
- [ ] `C-DC-12` `constraint` No persistent volume, fixed container name, custom network is declared `src: Deployment contract`
- [ ] `C-DC-13` `contract` Every list endpoint returns a top-level JSON array or a named member `src: Deployment contract, API shapes`
- [ ] `C-DC-14` `contract` Bearer authentication is required on every endpoint except the public reads `src: Deployment contract, API shapes`
- [ ] `C-DC-15` `contract` An invalid or unauthorized call is rejected as a client error `src: Deployment contract, API shapes`
- [ ] `C-DC-16` `constraint` An in-memory map of piece ids to image data fails the storage requirement `src: Deployment contract, No mocks`
- [ ] `C-DC-17` `constraint` A directory of files on the app container disk fails the storage requirement `src: Deployment contract, No mocks`
- [ ] `C-DC-18` `contract` The object store is the fact the interface reflects rather than substitutes `src: Deployment contract, No mocks`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `author@example.com` | pinned in instruction.md | `C-RL-13` |
| `author2@example.com` | pinned in instruction.md | `C-RL-14` |
| `reader@example.com` | pinned in instruction.md | `C-RL-15` |
| `deku-demo-pw-2026` | pinned in instruction.md | `C-RL-16` |
| `0.125` | pinned in instruction.md | `C-CF-11` |
| `64` | pinned in instruction.md | `C-CF-11` |
| `1` | pinned in instruction.md | `C-CF-19` |
| `32` | pinned in instruction.md | `C-CF-19` |
| `4096` | pinned in instruction.md | `C-CF-31` |
| `4194304` | pinned in instruction.md | `C-CF-32` |
| `512` | pinned in instruction.md | `C-CF-33` |
| `10` | pinned in instruction.md | `C-CF-41` |
| `10000` | pinned in instruction.md | `C-CF-41` |
| `2` | pinned in instruction.md | `C-CF-48` |
| `256` | pinned in instruction.md | `C-CF-48` |
| `0` | pinned in instruction.md | `C-CF-61` |
| `8` | pinned in instruction.md | `C-CF-61` |
| `20` | pinned in instruction.md | `C-CF-66` |
| `pieces/{piece_id}/{sha256_of_bytes}.{ext}` | pinned in instruction.md | `C-CF-72` |
| `thumbs/{piece_id}/{size}/{sha256_of_bytes}.png` | pinned in instruction.md | `C-CF-73` |
| `128` | pinned in instruction.md | `C-CF-82` |
| `20MB` | pinned in instruction.md | `C-CF-87` |
| `3` | pinned in instruction.md | `C-CF-97` |
| `7500` | pinned in instruction.md | `C-CF-122` |
| `300` | pinned in instruction.md | `C-CF-124` |
| `30` | pinned in instruction.md | `C-CF-142` |
| `Roboto` | pinned in instruction.md | `C-UX-09` |
| `14.4px` | pinned in instruction.md | `C-UX-10` |
| `23.04px` | pinned in instruction.md | `C-UX-10` |
| `21.6px` | pinned in instruction.md | `C-UX-11` |
| `STORAGE_BUCKET` | pinned in instruction.md | `C-TR-06` |
| `STORAGE_ACCESS_KEY` | pinned in instruction.md | `C-TR-07` |
| `STORAGE_SECRET_KEY` | pinned in instruction.md | `C-TR-07` |
| `3600` | pinned in instruction.md | `C-TR-26` |
| `Harbour Lights` | pinned in instruction.md | `C-DM-17` |
| `Cat In A Window` | pinned in instruction.md | `C-DM-18` |
| `Night Market Draft` | pinned in instruction.md | `C-DM-19` |
| `Valentine Robot` | pinned in instruction.md | `C-DM-20` |
| `Ocean Study` | pinned in instruction.md | `C-DM-21` |
| `Harbour Eight` | pinned in instruction.md | `C-DM-22` |
| `Night Sixteen` | pinned in instruction.md | `C-DM-22` |
| `Cats` | pinned in instruction.md | `C-DM-23` |
| `Christmas` | pinned in instruction.md | `C-DM-23` |
| `People` | pinned in instruction.md | `C-DM-23` |
| `Technology` | pinned in instruction.md | `C-DM-23` |
| `Valentine` | pinned in instruction.md | `C-DM-23` |
| `Ocean` | pinned in instruction.md | `C-DM-23` |
| `Oops!` | pinned in instruction.md | `C-FE-15` |
| `Pixelary` | pinned in instruction.md | `C-CN-10` |
| `${APP_PUBLIC_PORT}:4173` | pinned in instruction.md | `C-DC-02` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the local age of digital consent, left to the builder | `C-RL-11` |
| the perceptual-hash duplicate and review thresholds, left to the builder | `C-CF-100` |
| the exact colour values behind each named family and tone | `C-UX-02` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 4 | 6 |
| User roles | 1 | 16 |
| Core features | 97 | 180 |
| User flow | 9 | 28 |
| UI and UX notes | 4 | 30 |
| Technical requirements | 20 | 26 |
| Data model | 11 | 24 |
| Front-end specification | 3 | 16 |
| Constraints | 2 | 12 |
| Deployment contract | 12 | 18 |

