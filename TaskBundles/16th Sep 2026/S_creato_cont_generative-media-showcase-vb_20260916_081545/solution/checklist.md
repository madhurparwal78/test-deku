# Checklist: Lumina

Items: 1331
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC
Unpinned values flagged: 12

Source of every item: `instruction.md`. Nothing here is derived from any
other file, because no other file existed when the extraction ran.

## C-OV Overview

- [ ] `C-OV-01` `capability` Lumina is the public presence of a generative-media company. `src: Overview, instruction.md`
- [ ] `C-OV-02` `capability` One platform is sold to creators, to studios, to developers. `src: Overview, instruction.md`
- [ ] `C-OV-03` `capability` The marketing home is a light document opening on a full-bleed dark video hero. `src: Overview, instruction.md`
- [ ] `C-OV-04` `capability` The developer portal is a dark document with its own slim chrome. `src: Overview, instruction.md`
- [ ] `C-OV-05` `capability` The agent connector is a light document explaining how the generation engine reaches a chat assistant. `src: Overview, instruction.md`
- [ ] `C-OV-06` `capability` The generation application sits behind the three surfaces without being built here. `src: Overview, instruction.md`
- [ ] `C-OV-07` `capability` Copy, media references, model specs, news items, menu structure are editorial records changed by a signed-in account. `src: Overview, instruction.md`
- [ ] `C-OV-08` `constraint` An editorial change lands without a deploy. `src: Overview, instruction.md`
- [ ] `C-OV-09` `capability` An unpublished item has two bodies: the record, the uploaded poster. `src: Overview, instruction.md`
- [ ] `C-OV-10` `constraint` A draft whose record is hidden, whose bytes stay fetchable from the store by key, is not private. `src: Overview, instruction.md`
- [ ] `C-OV-11` `constraint` Lumina builds no timeline, runs no model, generates no frame. `src: Overview, instruction.md`
- [ ] `C-OV-12` `constraint` Lumina is not a video encoder, not a scheduler of graphics processors, not a billing system. `src: Overview, instruction.md`
- [ ] `C-OV-13` `constraint` Lumina has no native application, no desktop client, no comment threads. `src: Overview, instruction.md`
- [ ] `C-OV-14` `constraint` Lumina ships no image file, no video file, no font file. `src: Overview, instruction.md`

## C-RL User roles

- [ ] `C-RL-01` `role` Signup is open, so anybody creates an account from the public form. `src: User roles, instruction.md`
- [ ] `C-RL-02` `role` A seeded account exists alongside an account a visitor makes. `src: User roles, instruction.md`
- [ ] `C-RL-03` `role` The `author` role reads every public surface. `src: User roles, instruction.md`
- [ ] `C-RL-04` `role` The `author` role creates a content item. `src: User roles, instruction.md`
- [ ] `C-RL-05` `role` The `author` role edits an item the same account owns. `src: User roles, instruction.md`
- [ ] `C-RL-06` `role` The `author` role uploads a poster to an item the same account owns. `src: User roles, instruction.md`
- [ ] `C-RL-07` `role` The `author` role publishes an item the same account owns. `src: User roles, instruction.md`
- [ ] `C-RL-08` `role` The `author` role unpublishes an item the same account owns. `src: User roles, instruction.md`
- [ ] `C-RL-09` `role` The `author` role reads its own drafts. `src: User roles, instruction.md`
- [ ] `C-RL-10` `role` The `author` role reads its own draft posters. `src: User roles, instruction.md`
- [ ] `C-RL-11` `role` The `author` role is denied reading a content item owned by another account. `src: User roles, instruction.md`
- [ ] `C-RL-12` `role` The `author` role is denied editing a content item owned by another account. `src: User roles, instruction.md`
- [ ] `C-RL-13` `role` The `author` role is denied reading another account's draft poster. `src: User roles, instruction.md`
- [ ] `C-RL-14` `role` The `author` role is denied publishing another account's item. `src: User roles, instruction.md`
- [ ] `C-RL-15` `role` The `author` role is denied deleting an item that has ever been published. `src: User roles, instruction.md`
- [ ] `C-RL-16` `role` The `reader` role reads every public surface. `src: User roles, instruction.md`
- [ ] `C-RL-17` `role` The `reader` role reads every published item. `src: User roles, instruction.md`
- [ ] `C-RL-18` `role` The `reader` role manages its own account. `src: User roles, instruction.md`
- [ ] `C-RL-19` `role` The `reader` role is denied reading any unpublished item. `src: User roles, instruction.md`
- [ ] `C-RL-20` `role` The `reader` role is denied fetching any private media object. `src: User roles, instruction.md`
- [ ] `C-RL-21` `role` The `reader` role is denied reaching any compose surface. `src: User roles, instruction.md`
- [ ] `C-RL-22` `role` The `reader` role is denied publishing anything. `src: User roles, instruction.md`
- [ ] `C-RL-23` `role` An anonymous visitor is not a role. `src: User roles, instruction.md`
- [ ] `C-RL-24` `role` An anonymous visitor reads every public surface, submits the sign-up form, does nothing further. `src: User roles, instruction.md`
- [ ] `C-RL-25` `contract` Authorization is enforced server-side on every mutating endpoint. `src: User roles, instruction.md`
- [ ] `C-RL-26` `contract` A hidden button in the interface is not authorization. `src: User roles, instruction.md`
- [ ] `C-RL-27` `contract` A direct API call from a `reader` session to an `author`-only endpoint is rejected by the server. `src: User roles, instruction.md`
- [ ] `C-RL-28` `contract` A rejected unauthorized call leaves the protected state unchanged. `src: User roles, instruction.md`
- [ ] `C-RL-29` `contract` An unpublished item answers an anonymous caller exactly as a slug that never existed answers. `src: User roles, instruction.md`
- [ ] `C-RL-30` `contract` An unpublished item answers a signed-in caller who does not own the item exactly as a slug that never existed answers. `src: User roles, instruction.md`
- [ ] `C-RL-31` `contract` A private media object is refused by key, so knowing a key is worth nothing without an entitled session. `src: User roles, instruction.md`
- [ ] `C-RL-32` `contract` Publication changes the item's status together with the poster's visibility in one transaction. `src: User roles, instruction.md`
- [ ] `C-RL-33` `ui` A signed-in actor lacking a permission is told which permission is required. `src: User roles, instruction.md`
- [ ] `C-RL-34` `contract` An anonymous actor is told nothing that a missing item would not also have told them. `src: User roles, instruction.md`
- [ ] `C-RL-35` `literal` The seeded account `author@example.com` holds the `author` role. `src: User roles, instruction.md`
- [ ] `C-RL-36` `literal` The account `author@example.com` owns two published news items, one draft, one archived item. `src: User roles, instruction.md`
- [ ] `C-RL-37` `literal` The seeded account `author2@example.com` holds the `author` role. `src: User roles, instruction.md`
- [ ] `C-RL-38` `literal` The account `author2@example.com` owns one draft, the cross-author counterexample. `src: User roles, instruction.md`
- [ ] `C-RL-39` `literal` The seeded account `reader@example.com` holds the `reader` role. `src: User roles, instruction.md`
- [ ] `C-RL-40` `literal` The account `reader@example.com` owns nothing. `src: User roles, instruction.md`
- [ ] `C-RL-41` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles, instruction.md`

## C-CF Core features

- [ ] `C-CF-01` `data` A content item carries a `kind` of `news` or `model_card`. `src: Core features, instruction.md`
- [ ] `C-CF-02` `data` A content item carries a `slug` unique per kind. `src: Core features, instruction.md`
- [ ] `C-CF-03` `data` A content item carries a title, a dek, a body. `src: Core features, instruction.md`
- [ ] `C-CF-04` `data` A content item carries an owning account. `src: Core features, instruction.md`
- [ ] `C-CF-05` `data` A content item carries a poster. `src: Core features, instruction.md`
- [ ] `C-CF-06` `data` A content item carries a `status` of `draft`, `scheduled`, `published`, `archived`. `src: Core features, instruction.md`
- [ ] `C-CF-07` `contract` Creating an item leaves the item at status `draft`. `src: Core features, instruction.md`
- [ ] `C-CF-08` `contract` A draft appears in the owner's own list. `src: Core features, instruction.md`
- [ ] `C-CF-09` `contract` A draft appears on no public surface. `src: Core features, instruction.md`
- [ ] `C-CF-10` `contract` An anonymous request for an unpublished item is refused. `src: Core features, instruction.md`
- [ ] `C-CF-11` `contract` The refusal for an unpublished item is indistinguishable from the refusal for a slug that does not exist. `src: Core features, instruction.md`
- [ ] `C-CF-12` `literal` Requesting `/news/the-media-router-preview` signed out answers exactly as `/news/no-such-item-at-all` answers. `src: Core features, instruction.md`
- [ ] `C-CF-13` `contract` The two refusals share a status, a body, a set of headers. `src: Core features, instruction.md`
- [ ] `C-CF-14` `contract` A differing status for the two responses is the leak the rule names. `src: Core features, instruction.md`
- [ ] `C-CF-15` `contract` A differing message for the two responses is the leak the rule names. `src: Core features, instruction.md`
- [ ] `C-CF-16` `contract` A differing response time for the two responses is the leak the rule names. `src: Core features, instruction.md`
- [ ] `C-CF-17` `contract` A `reader` session holding no ownership receives the same refusal for a draft. `src: Core features, instruction.md`
- [ ] `C-CF-18` `contract` An attempted read of a draft leaves the item's row untouched. `src: Core features, instruction.md`
- [ ] `C-CF-19` `literal` The account `author2@example.com` owns a second draft. `src: Core features, instruction.md`
- [ ] `C-CF-20` `contract` An `author@example.com` session is refused the second author's draft exactly as an anonymous caller is. `src: Core features, instruction.md`
- [ ] `C-CF-21` `contract` Ownership is per item rather than per role. `src: Core features, instruction.md`
- [ ] `C-CF-22` `contract` Publishing an item sets the status to `published`. `src: Core features, instruction.md`
- [ ] `C-CF-23` `contract` Publishing an item sets the poster's visibility to `public`. `src: Core features, instruction.md`
- [ ] `C-CF-24` `contract` The status change happens together with the visibility change in one transaction. `src: Core features, instruction.md`
- [ ] `C-CF-25` `contract` One half of publication without the other half is never observable at any instant by any caller. `src: Core features, instruction.md`
- [ ] `C-CF-26` `contract` Unpublishing reverses both changes in one transaction. `src: Core features, instruction.md`
- [ ] `C-CF-27` `contract` Unpublishing makes the item unreadable again in the same act. `src: Core features, instruction.md`
- [ ] `C-CF-28` `contract` Unpublishing makes the poster unreadable again in the same act. `src: Core features, instruction.md`
- [ ] `C-CF-29` `contract` An item carrying empty alternative text on its poster may not be published. `src: Core features, instruction.md`
- [ ] `C-CF-30` `ui` The refusal to publish names the alternative-text field. `src: Core features, instruction.md`
- [ ] `C-CF-31` `contract` The alternative-text rule is a gate rather than a reminder. `src: Core features, instruction.md`
- [ ] `C-CF-32` `contract` An archived item is unreadable publicly. `src: Core features, instruction.md`
- [ ] `C-CF-33` `contract` An archived item stays readable by the owning account. `src: Core features, instruction.md`
- [ ] `C-CF-34` `contract` Archiving is not deletion. `src: Core features, instruction.md`
- [ ] `C-CF-35` `contract` An item that has ever been published cannot be deleted at all. `src: Core features, instruction.md`
- [ ] `C-CF-36` `data` A slug is unique per kind. `src: Core features, instruction.md`
- [ ] `C-CF-37` `data` A slug is lowercase words joined by hyphens. `src: Core features, instruction.md`
- [ ] `C-CF-38` `contract` A slug is immutable once the item has been published. `src: Core features, instruction.md`
- [ ] `C-CF-39` `contract` A slug change before publication is permitted. `src: Core features, instruction.md`
- [ ] `C-CF-40` `contract` An old slug is not reserved, because nothing ever linked to the old slug. `src: Core features, instruction.md`
- [ ] `C-CF-41` `data` Every status change writes an entry to the item's own history. `src: Core features, instruction.md`
- [ ] `C-CF-42` `data` A history entry carries the actor, the instant, the status before, the status after. `src: Core features, instruction.md`
- [ ] `C-CF-43` `data` The item history is append-only. `src: Core features, instruction.md`
- [ ] `C-CF-44` `contract` Every uploaded byte lives in `minio`. `src: Core features, instruction.md`
- [ ] `C-CF-45` `constraint` No uploaded byte lives on the application's filesystem. `src: Core features, instruction.md`
- [ ] `C-CF-46` `constraint` No uploaded byte lives in a database column. `src: Core features, instruction.md`
- [ ] `C-CF-47` `constraint` No uploaded byte lives in a cache the application controls. `src: Core features, instruction.md`
- [ ] `C-CF-48` `literal` The application reads `STORAGE_ENDPOINT` from the environment. `src: Core features, instruction.md`
- [ ] `C-CF-49` `literal` The application reads `STORAGE_BUCKET` from the environment. `src: Core features, instruction.md`
- [ ] `C-CF-50` `literal` The application reads `STORAGE_ACCESS_KEY` from the environment. `src: Core features, instruction.md`
- [ ] `C-CF-51` `literal` The application reads `STORAGE_SECRET_KEY` from the environment. `src: Core features, instruction.md`
- [ ] `C-CF-52` `constraint` The application never hardcodes a store host. `src: Core features, instruction.md`
- [ ] `C-CF-53` `literal` The object key follows the scheme `media/{item_id}/{sha256_of_bytes}.{ext}`. `src: Core features, instruction.md`
- [ ] `C-CF-54` `literal` A worked key for item `42` holding a WebP poster reads `media/42/9f2a1c7d4e8b6a0f3c5d2e1b8a7f6c5d4e3b2a1908f7e6d5c4b3a2918070605d.webp`. `src: Core features, instruction.md`
- [ ] `C-CF-55` `data` The checksum in a key is taken over the bytes as uploaded. `src: Core features, instruction.md`
- [ ] `C-CF-56` `contract` Re-uploading identical bytes to the same item produces the same key. `src: Core features, instruction.md`
- [ ] `C-CF-57` `contract` Re-uploading identical bytes to the same item stores one object. `src: Core features, instruction.md`
- [ ] `C-CF-58` `data` The extension follows the content type. `src: Core features, instruction.md`
- [ ] `C-CF-59` `contract` The content type is sniffed from the bytes. `src: Core features, instruction.md`
- [ ] `C-CF-60` `constraint` The declared content type is not trusted. `src: Core features, instruction.md`
- [ ] `C-CF-61` `constraint` The file name is not trusted. `src: Core features, instruction.md`
- [ ] `C-CF-62` `contract` A file named `poster.webp` whose bytes are something else is refused. `src: Core features, instruction.md`
- [ ] `C-CF-63` `contract` A refused upload writes nothing. `src: Core features, instruction.md`
- [ ] `C-CF-64` `data` A media object carries a visibility of `private` or `public`. `src: Core features, instruction.md`
- [ ] `C-CF-65` `contract` Visibility follows the owning item's status. `src: Core features, instruction.md`
- [ ] `C-CF-66` `constraint` Visibility is never set on its own. `src: Core features, instruction.md`
- [ ] `C-CF-67` `contract` A private object is unreachable to anyone but the owning account. `src: Core features, instruction.md`
- [ ] `C-CF-68` `contract` A private object is unreachable by every route. `src: Core features, instruction.md`
- [ ] `C-CF-69` `contract` A private object is unreachable by every key. `src: Core features, instruction.md`
- [ ] `C-CF-70` `contract` The product serves objects through the product's own media route. `src: Core features, instruction.md`
- [ ] `C-CF-71` `contract` A media-route request for a private object from an unentitled caller is refused. `src: Core features, instruction.md`
- [ ] `C-CF-72` `contract` The refusal for a private object is indistinguishable from the refusal for a key that does not exist. `src: Core features, instruction.md`
- [ ] `C-CF-73` `contract` Access to a public object uses an authenticated streaming endpoint that reads the object, then writes the bytes. `src: Core features, instruction.md`
- [ ] `C-CF-74` `contract` Access to a public object alternatively uses a presigned address valid for at most five minutes. `src: Core features, instruction.md`
- [ ] `C-CF-75` `contract` One of the two access mechanisms is chosen, then held to consistently. `src: Core features, instruction.md`
- [ ] `C-CF-76` `constraint` A presigned address is never issued to a caller not entitled to the object. `src: Core features, instruction.md`
- [ ] `C-CF-77` `constraint` A presigned address is never issued for a private object at all. `src: Core features, instruction.md`
- [ ] `C-CF-78` `contract` Fetching a draft poster's key copied verbatim from the studio is refused for an anonymous caller. `src: Core features, instruction.md`
- [ ] `C-CF-79` `contract` Fetching a draft poster's key is refused for a signed-in caller who does not own the item. `src: Core features, instruction.md`
- [ ] `C-CF-80` `contract` The object stays present in the store after a refused fetch. `src: Core features, instruction.md`
- [ ] `C-CF-81` `contract` The item stays unchanged after a refused fetch. `src: Core features, instruction.md`
- [ ] `C-CF-82` `data` Alternative text is a property of the media object. `src: Core features, instruction.md`
- [ ] `C-CF-83` `contract` Alternative text is required before the owning item may be published. `src: Core features, instruction.md`
- [ ] `C-CF-84` `ui` Alternative text is carried into the rendered page. `src: Core features, instruction.md`
- [ ] `C-CF-85` `contract` Deleting an item that was never published deletes the item's objects. `src: Core features, instruction.md`
- [ ] `C-CF-86` `contract` Deleting is refused for an item that has ever been published. `src: Core features, instruction.md`
- [ ] `C-CF-87` `contract` No live page ever loses its poster. `src: Core features, instruction.md`
- [ ] `C-CF-88` `capability` Signup is open, so the public form creates an account from an email address plus a password. `src: Core features, instruction.md`
- [ ] `C-CF-89` `data` An email address is unique without regard to case. `src: Core features, instruction.md`
- [ ] `C-CF-90` `contract` A second signup with the same address is refused. `src: Core features, instruction.md`
- [ ] `C-CF-91` `contract` The refusal for a duplicate address does not confirm whether the address was already registered. `src: Core features, instruction.md`
- [ ] `C-CF-92` `data` Every signup carries a client-generated idempotency key. `src: Core features, instruction.md`
- [ ] `C-CF-93` `contract` A double submit creates one account rather than two. `src: Core features, instruction.md`
- [ ] `C-CF-94` `contract` A repeat under the same idempotency key returns the first result. `src: Core features, instruction.md`
- [ ] `C-CF-95` `contract` The password is hashed with a memory-hard function. `src: Core features, instruction.md`
- [ ] `C-CF-96` `data` The hashing parameters are stored beside the record. `src: Core features, instruction.md`
- [ ] `C-CF-97` `literal` The minimum password length is `8`. `src: Core features, instruction.md`
- [ ] `C-CF-98` `constraint` No composition rule applies to a password. `src: Core features, instruction.md`
- [ ] `C-CF-99` `contract` Authentication takes an email with a password. `src: Core features, instruction.md`
- [ ] `C-CF-100` `contract` The client sends a bearer token on every call needing one. `src: Core features, instruction.md`
- [ ] `C-CF-101` `contract` A token expires. `src: Core features, instruction.md`
- [ ] `C-CF-102` `contract` An expired token on a mutating call is refused. `src: Core features, instruction.md`
- [ ] `C-CF-103` `ui` An actor holding an expired token is returned to sign-in with their composed work preserved. `src: Core features, instruction.md`
- [ ] `C-CF-104` `data` A session is an opaque server-side record. `src: Core features, instruction.md`
- [ ] `C-CF-105` `constraint` The session cookie carries no claim, no role. `src: Core features, instruction.md`
- [ ] `C-CF-106` `contract` Signing out revokes the session on the server. `src: Core features, instruction.md`
- [ ] `C-CF-107` `constraint` Signing out does more than clear the cookie. `src: Core features, instruction.md`
- [ ] `C-CF-108` `data` A signup records the route the signup came from. `src: Core features, instruction.md`
- [ ] `C-CF-109` `data` A signup records the label of the control that started the signup. `src: Core features, instruction.md`
- [ ] `C-CF-110` `contract` Signup attribution is carried in the destination address or in a first-party mechanism. `src: Core features, instruction.md`
- [ ] `C-CF-111` `contract` Signup attribution is discarded once the account exists. `src: Core features, instruction.md`
- [ ] `C-CF-112` `contract` A seeded account signs in exactly as an account made through the form does. `src: Core features, instruction.md`
- [ ] `C-CF-113` `ui` The dominant surface on all three public routes is an autoplaying streamed video presented as a poster-first muted looping tile. `src: Core features, instruction.md`
- [ ] `C-CF-114` `ui` The media tile is specified once, then reused everywhere. `src: Core features, instruction.md`
- [ ] `C-CF-115` `ui` A tile is a rounded container holding three stacked layers. `src: Core features, instruction.md`
- [ ] `C-CF-116` `ui` The poster layer shows a still frame before playback is ready. `src: Core features, instruction.md`
- [ ] `C-CF-117` `ui` A low-resolution copy sits behind the sharp poster, blurred, very slightly scaled up. `src: Core features, instruction.md`
- [ ] `C-CF-118` `ui` The blur bleeds past the frame edge rather than stopping at the edge. `src: Core features, instruction.md`
- [ ] `C-CF-119` `ui` The video layer is muted. `src: Core features, instruction.md`
- [ ] `C-CF-120` `ui` The video layer loops. `src: Core features, instruction.md`
- [ ] `C-CF-121` `ui` The video layer plays inline rather than taking over the screen. `src: Core features, instruction.md`
- [ ] `C-CF-122` `ui` The video layer autoplays only when the tile is in view. `src: Core features, instruction.md`
- [ ] `C-CF-123` `ui` The overlay layer carries a bottom-anchored gradient scrim. `src: Core features, instruction.md`
- [ ] `C-CF-124` `ui` The scrim is transparent for the top half of the tile, darkening towards the bottom. `src: Core features, instruction.md`
- [ ] `C-CF-125` `ui` A caption stays legible over any frame. `src: Core features, instruction.md`
- [ ] `C-CF-126` `ui` The overlay layer carries the tile controls. `src: Core features, instruction.md`
- [ ] `C-CF-127` `ui` The poster holds at full strength until the video's first frame is decoded. `src: Core features, instruction.md`
- [ ] `C-CF-128` `ui` The poster then fades away to reveal the video beneath. `src: Core features, instruction.md`
- [ ] `C-CF-129` `ui` Showing an empty rectangle first, filling the rectangle later, is the failure the rule names. `src: Core features, instruction.md`
- [ ] `C-CF-130` `ui` A tile control is a small circular button pinned to a tile corner. `src: Core features, instruction.md`
- [ ] `C-CF-131` `ui` A tile control is a full pill carrying a blurred backdrop plus a layered ring. `src: Core features, instruction.md`
- [ ] `C-CF-132` `ui` The tile carries two controls: pause, mute. `src: Core features, instruction.md`
- [ ] `C-CF-133` `ui` Each tile control announces the action the control will perform. `src: Core features, instruction.md`
- [ ] `C-CF-134` `ui` The pause control's announcement flips between pause, play, as the state changes. `src: Core features, instruction.md`
- [ ] `C-CF-135` `ui` The mute control's announcement flips between mute, unmute, as the state changes. `src: Core features, instruction.md`
- [ ] `C-CF-136` `ui` A tile below the fold is lazy, so the poster is a tiny blurred image. `src: Core features, instruction.md`
- [ ] `C-CF-137` `ui` A lazy tile attaches its stream only as the tile approaches the viewport. `src: Core features, instruction.md`
- [ ] `C-CF-138` `ui` Exactly one stream on a route is eager, the hero's. `src: Core features, instruction.md`
- [ ] `C-CF-139` `ui` Under reduced motion a tile does not autoplay. `src: Core features, instruction.md`
- [ ] `C-CF-140` `ui` Under reduced motion the poster renders with the play control present. `src: Core features, instruction.md`
- [ ] `C-CF-141` `ui` The marketing home document is light. `src: Core features, instruction.md`
- [ ] `C-CF-142` `ui` The marketing home title reads `Lumina | Building Real-World Intelligence`. `src: Core features, instruction.md`
- [ ] `C-CF-143` `ui` The marketing home runs eleven sections in a fixed order. `src: Core features, instruction.md`
- [ ] `C-CF-144` `ui` The fixed order runs the hero, the partner marquee, the three-platform switcher, the research band, the news grid, the footer. `src: Core features, instruction.md`
- [ ] `C-CF-145` `ui` The switcher occupies the centre of the page. `src: Core features, instruction.md`
- [ ] `C-CF-146` `ui` The hero is a full-bleed dark media tile behind a bottom-left copy stack. `src: Core features, instruction.md`
- [ ] `C-CF-147` `literal` The hero display heading reads `Building Real-World Intelligence`. `src: Core features, instruction.md`
- [ ] `C-CF-148` `ui` The hero copy stack carries a lead paragraph. `src: Core features, instruction.md`
- [ ] `C-CF-149` `literal` The hero action is one filled light pill reading `Try Lumina for free`. `src: Core features, instruction.md`
- [ ] `C-CF-150` `ui` The hero action pill carries a chevron. `src: Core features, instruction.md`
- [ ] `C-CF-151` `ui` The hero heading carries a soft shadow, so the heading survives an arbitrary frame behind. `src: Core features, instruction.md`
- [ ] `C-CF-152` `ui` The hero lead carries a soft shadow, so the lead survives an arbitrary frame behind. `src: Core features, instruction.md`
- [ ] `C-CF-153` `literal` The partner marquee eyebrow reads `We partner with the world's leading organizations to advance their industries:`. `src: Core features, instruction.md`
- [ ] `C-CF-154` `ui` The partner marquee drifts a horizontal track of partner name-tiles. `src: Core features, instruction.md`
- [ ] `C-CF-155` `ui` The partner marquee track sits under an edge-fade mask on both sides. `src: Core features, instruction.md`
- [ ] `C-CF-156` `ui` The partner marquee track is duplicated head to tail, so the loop is seamless. `src: Core features, instruction.md`
- [ ] `C-CF-157` `ui` The partner marquee runs on a timer rather than on scroll position. `src: Core features, instruction.md`
- [ ] `C-CF-158` `literal` The switcher section heading reads `Three platforms built on-top of the same Real-World Intelligence models`. `src: Core features, instruction.md`
- [ ] `C-CF-159` `ui` The switcher holds a horizontal track of three panels. `src: Core features, instruction.md`
- [ ] `C-CF-160` `ui` The switcher tab labels sit above a rule along which the active underline slides. `src: Core features, instruction.md`
- [ ] `C-CF-161` `literal` The three switcher panels are `Lumina Creative`, `Lumina Dev`, `Lumina Robotics`. `src: Core features, instruction.md`
- [ ] `C-CF-162` `ui` The switcher track advances as the reader moves through the section. `src: Core features, instruction.md`
- [ ] `C-CF-163` `ui` The research band is a full-bleed panel over a living green field under a darkening overlay. `src: Core features, instruction.md`
- [ ] `C-CF-164` `literal` The research band eyebrow reads `Lumina Research`. `src: Core features, instruction.md`
- [ ] `C-CF-165` `ui` The research band carries a heading. `src: Core features, instruction.md`
- [ ] `C-CF-166` `literal` The research band carries a `Learn more` link. `src: Core features, instruction.md`
- [ ] `C-CF-167` `ui` The research band carries three stacked research cards on the right. `src: Core features, instruction.md`
- [ ] `C-CF-168` `ui` A research card carries a title, an up-right arrow, a one-line abstract. `src: Core features, instruction.md`
- [ ] `C-CF-169` `literal` The news grid heading reads `See the latest from Lumina`. `src: Core features, instruction.md`
- [ ] `C-CF-170` `ui` A news card carries a poster, a title, a one-line dek, a `Learn more` link. `src: Core features, instruction.md`
- [ ] `C-CF-171` `contract` The news grid renders published items only. `src: Core features, instruction.md`
- [ ] `C-CF-172` `contract` The news grid orders items newest first. `src: Core features, instruction.md`
- [ ] `C-CF-173` `contract` The news grid reads the same records the studio edits. `src: Core features, instruction.md`
- [ ] `C-CF-174` `capability` Changing a news item is an editorial change with no deploy. `src: Core features, instruction.md`
- [ ] `C-CF-175` `capability` Changing a research card is an editorial change with no deploy. `src: Core features, instruction.md`
- [ ] `C-CF-176` `capability` Changing a partner tile is an editorial change with no deploy. `src: Core features, instruction.md`
- [ ] `C-CF-177` `ui` The developer portal document is dark. `src: Core features, instruction.md`
- [ ] `C-CF-178` `ui` The developer portal wears its own slim chrome, shorter than the marketing bar. `src: Core features, instruction.md`
- [ ] `C-CF-179` `literal` The developer chrome carries a `Lumina Dev` lockup at the inline start. `src: Core features, instruction.md`
- [ ] `C-CF-180` `literal` The developer chrome carries `Explore` beside the lockup. `src: Core features, instruction.md`
- [ ] `C-CF-181` `literal` The developer chrome carries `Docs` beside the lockup. `src: Core features, instruction.md`
- [ ] `C-CF-182` `ui` The `Docs` destination opens in a new tab, saying so. `src: Core features, instruction.md`
- [ ] `C-CF-183` `literal` The developer chrome carries `Log In` at the inline end. `src: Core features, instruction.md`
- [ ] `C-CF-184` `literal` The developer chrome carries `Sign Up` at the inline end. `src: Core features, instruction.md`
- [ ] `C-CF-185` `constraint` The developer chrome carries no mega-menu. `src: Core features, instruction.md`
- [ ] `C-CF-186` `constraint` The developer portal carries no marketing footer. `src: Core features, instruction.md`
- [ ] `C-CF-187` `literal` The developer portal title reads `Lumina Developer Portal`. `src: Core features, instruction.md`
- [ ] `C-CF-188` `ui` The developer hero is a full-bleed dark media tile. `src: Core features, instruction.md`
- [ ] `C-CF-189` `literal` The developer hero title reads `The AI Media Platform` over `for Developers`. `src: Core features, instruction.md`
- [ ] `C-CF-190` `ui` The developer hero carries a subtitle naming the model classes served from one enterprise-grade platform. `src: Core features, instruction.md`
- [ ] `C-CF-191` `literal` The developer hero carries the filled action `Get API Key`. `src: Core features, instruction.md`
- [ ] `C-CF-192` `literal` The developer hero carries the ghosted action `Explore Models`. `src: Core features, instruction.md`
- [ ] `C-CF-193` `literal` A trusted-by marquee labelled `Trusted by` carries developer-audience partner tiles. `src: Core features, instruction.md`
- [ ] `C-CF-194` `literal` The capability bento heading reads `One API for production` over `media generation.`. `src: Core features, instruction.md`
- [ ] `C-CF-195` `ui` The capability bento holds four columns. `src: Core features, instruction.md`
- [ ] `C-CF-196` `ui` A bento column carries a label, a title, a description, a call to action. `src: Core features, instruction.md`
- [ ] `C-CF-197` `literal` The four bento labels read `Access`, `Evaluate`, `Automate`, `Control`. `src: Core features, instruction.md`
- [ ] `C-CF-198` `literal` The `Automate` column carries a `NEW` badge. `src: Core features, instruction.md`
- [ ] `C-CF-199` `literal` The router section heading reads `Model Routers for` over `Optimization`. `src: Core features, instruction.md`
- [ ] `C-CF-200` `literal` The router section action reads `Set up a router`. `src: Core features, instruction.md`
- [ ] `C-CF-201` `literal` The code sample section heading reads `Seamless Integration`. `src: Core features, instruction.md`
- [ ] `C-CF-202` `literal` The code sample category row reads `Models`, `Workflows`, `Recipes`, `Characters`. `src: Core features, instruction.md`
- [ ] `C-CF-203` `literal` The code sample language row reads `Node`, `Python`, `cURL`. `src: Core features, instruction.md`
- [ ] `C-CF-204` `ui` The category row drives a dark code panel. `src: Core features, instruction.md`
- [ ] `C-CF-205` `ui` Changing a code tab fades the panel's content once, then holds. `src: Core features, instruction.md`
- [ ] `C-CF-206` `ui` The code panel carries a copy control placing the sample on the clipboard. `src: Core features, instruction.md`
- [ ] `C-CF-207` `ui` The code sample is selectable text rather than an image. `src: Core features, instruction.md`
- [ ] `C-CF-208` `literal` The model catalog heading reads `State-of-the-art` over `Models`. `src: Core features, instruction.md`
- [ ] `C-CF-209` `literal` The model catalog carries the action `View all models`. `src: Core features, instruction.md`
- [ ] `C-CF-210` `literal` The model catalog carries the action `View SDK docs`. `src: Core features, instruction.md`
- [ ] `C-CF-211` `ui` The catalog offers a horizontally scrolled rail of cards under a one-sided fade mask. `src: Core features, instruction.md`
- [ ] `C-CF-212` `ui` The catalog rail is advanced by circular arrow buttons. `src: Core features, instruction.md`
- [ ] `C-CF-213` `ui` The catalog offers a comparison table beside the rail. `src: Core features, instruction.md`
- [ ] `C-CF-214` `contract` Both catalog presentations read the same model records. `src: Core features, instruction.md`
- [ ] `C-CF-215` `contract` Both catalog presentations render the same fields in the same order. `src: Core features, instruction.md`
- [ ] `C-CF-216` `data` The model field order runs name, tagline, resolution, aspect ratios, inputs, maximum duration, price. `src: Core features, instruction.md`
- [ ] `C-CF-217` `contract` A card disagreeing with a table row is impossible by construction rather than by review. `src: Core features, instruction.md`
- [ ] `C-CF-218` `data` Price is an integer in minor units per second of output. `src: Core features, instruction.md`
- [ ] `C-CF-219` `literal` Price renders in `usd`. `src: Core features, instruction.md`
- [ ] `C-CF-220` `literal` `Nova-4.5` costs `12` minor units per second. `src: Core features, instruction.md`
- [ ] `C-CF-221` `literal` `Chisel-2.0` costs `18` minor units per second. `src: Core features, instruction.md`
- [ ] `C-CF-222` `literal` `Worldscape-1` costs `30` minor units per second. `src: Core features, instruction.md`
- [ ] `C-CF-223` `literal` `Perform-2` costs `9` minor units per second. `src: Core features, instruction.md`
- [ ] `C-CF-224` `capability` A model record is editorial, so adding one is a record plus a spec. `src: Core features, instruction.md`
- [ ] `C-CF-225` `constraint` Adding a model record is never a code change. `src: Core features, instruction.md`
- [ ] `C-CF-226` `ui` The agent connector document is light. `src: Core features, instruction.md`
- [ ] `C-CF-227` `ui` The agent connector title reads `Lumina Agent Connector | Generate video from your assistant`. `src: Core features, instruction.md`
- [ ] `C-CF-228` `literal` The connector hero heading reads `Lumina Agent Connector`. `src: Core features, instruction.md`
- [ ] `C-CF-229` `ui` The connector hero carries three stacked lines. `src: Core features, instruction.md`
- [ ] `C-CF-230` `literal` The connector hero action reads `Connect`. `src: Core features, instruction.md`
- [ ] `C-CF-231` `ui` The connector hero carries a row of agent buttons naming an assistant, a chat tool, an editor, a coding sandbox. `src: Core features, instruction.md`
- [ ] `C-CF-232` `literal` The three-step setup heading reads `Connect Lumina in seconds`. `src: Core features, instruction.md`
- [ ] `C-CF-233` `ui` The three-step setup carries three numbered steps. `src: Core features, instruction.md`
- [ ] `C-CF-234` `ui` The second setup step shows the connector address in a monospace field. `src: Core features, instruction.md`
- [ ] `C-CF-235` `literal` The second setup step carries a `Copy` control placing the address on the clipboard. `src: Core features, instruction.md`
- [ ] `C-CF-236` `literal` The capability showcase heading reads `A complete generation studio,` over `inside your agent.`. `src: Core features, instruction.md`
- [ ] `C-CF-237` `ui` The capability showcase carries four alternating rows. `src: Core features, instruction.md`
- [ ] `C-CF-238` `ui` A showcase row carries an eyebrow, a title, a body line, a chat-styled demonstration. `src: Core features, instruction.md`
- [ ] `C-CF-239` `ui` A chat demonstration shows a user prompt bubble on a near-white neutral, then a response tile. `src: Core features, instruction.md`
- [ ] `C-CF-240` `literal` The model pill row heading reads `Access to the latest state-of-the-art models`. `src: Core features, instruction.md`
- [ ] `C-CF-241` `ui` The model pill row wraps a row of model-name pills. `src: Core features, instruction.md`
- [ ] `C-CF-242` `contract` The model pill row reads the same model records the portal renders. `src: Core features, instruction.md`
- [ ] `C-CF-243` `literal` The prompt gallery heading reads `Just tell your agent what you need.` over `Lumina handles the rest.`. `src: Core features, instruction.md`
- [ ] `C-CF-244` `ui` The prompt gallery holds a grid of example prompt cards. `src: Core features, instruction.md`
- [ ] `C-CF-245` `ui` A composed chat input below the gallery shows an add affordance. `src: Core features, instruction.md`
- [ ] `C-CF-246` `literal` The composed chat input shows a `Write a message...` field. `src: Core features, instruction.md`
- [ ] `C-CF-247` `literal` The accordion heading reads `Frequently asked questions`. `src: Core features, instruction.md`
- [ ] `C-CF-248` `ui` The accordion carries four independently expandable rows. `src: Core features, instruction.md`
- [ ] `C-CF-249` `contract` Each accordion answer is present in the document at first render. `src: Core features, instruction.md`
- [ ] `C-CF-250` `contract` An accordion answer is hidden by a style rule rather than absent, so an in-page find reaches the answer. `src: Core features, instruction.md`
- [ ] `C-CF-251` `contract` Any unresolved address renders the product's own not-found shell. `src: Core features, instruction.md`
- [ ] `C-CF-252` `contract` The not-found shell answers not-found. `src: Core features, instruction.md`
- [ ] `C-CF-253` `ui` The not-found shell carries the full marketing header around a centred body. `src: Core features, instruction.md`
- [ ] `C-CF-254` `ui` The not-found shell carries the full marketing footer around a centred body. `src: Core features, instruction.md`
- [ ] `C-CF-255` `ui` The not-found body heading states that the page does not exist. `src: Core features, instruction.md`
- [ ] `C-CF-256` `literal` The not-found body carries a pill reading `Take me home` linking to the home route. `src: Core features, instruction.md`
- [ ] `C-CF-257` `ui` The not-found shell is a real surface rather than an error. `src: Core features, instruction.md`
- [ ] `C-CF-258` `ui` A lost visitor reaches every destination the site has from the not-found shell. `src: Core features, instruction.md`
- [ ] `C-CF-259` `contract` Every internal link on every public route resolves. `src: Core features, instruction.md`
- [ ] `C-CF-260` `contract` A link leading nowhere is a defect. `src: Core features, instruction.md`
- [ ] `C-CF-261` `constraint` An external link is out of scope for the link-integrity rule. `src: Core features, instruction.md`
- [ ] `C-CF-262` `ui` A link opening in a new tab says so in its accessible name. `src: Core features, instruction.md`
- [ ] `C-CF-263` `constraint` The studio is not built here. `src: Core features, instruction.md`
- [ ] `C-CF-264` `constraint` The inference cluster is not built here. `src: Core features, instruction.md`
- [ ] `C-CF-265` `constraint` The credit ledger is not built here. `src: Core features, instruction.md`
- [ ] `C-CF-266` `capability` Streamed inference reaches the browser progressively as output is produced. `src: Core features, instruction.md`
- [ ] `C-CF-267` `constraint` Output is not withheld until the render finishes. `src: Core features, instruction.md`
- [ ] `C-CF-268` `capability` The inference transport is an open resumable stream per job carrying ordered chunks. `src: Core features, instruction.md`
- [ ] `C-CF-269` `data` A stream chunk is tagged with a job identifier, a rising sequence number, a media offset. `src: Core features, instruction.md`
- [ ] `C-CF-270` `capability` A reconnect resumes from the last acknowledged sequence number rather than restarting. `src: Core features, instruction.md`
- [ ] `C-CF-271` `capability` Backpressure is explicit, so a slow reader cannot stall the accelerator. `src: Core features, instruction.md`
- [ ] `C-CF-272` `capability` The server holds a bounded window, dropping intermediate preview frames. `src: Core features, instruction.md`
- [ ] `C-CF-273` `constraint` The server never drops a final frame. `src: Core features, instruction.md`
- [ ] `C-CF-274` `capability` Every stream ends in exactly one terminal event of completed, failed, cancelled. `src: Core features, instruction.md`
- [ ] `C-CF-275` `capability` A completed stream carries a durable artifact reference. `src: Core features, instruction.md`
- [ ] `C-CF-276` `capability` A first meaningful preview arrives inside a stated budget even when the full render takes far longer. `src: Core features, instruction.md`
- [ ] `C-CF-277` `capability` The timeline editor stays interactive at all times. `src: Core features, instruction.md`
- [ ] `C-CF-278` `capability` The timeline editor stays interactive during generation of clips on the timeline. `src: Core features, instruction.md`
- [ ] `C-CF-279` `capability` Model work happens off the interaction path. `src: Core features, instruction.md`
- [ ] `C-CF-280` `capability` Encoding happens off the interaction path. `src: Core features, instruction.md`
- [ ] `C-CF-281` `capability` Heavy decode happens off the interaction path. `src: Core features, instruction.md`
- [ ] `C-CF-282` `data` A clip carries an explicit state of empty, queued, generating, ready, failed. `src: Core features, instruction.md`
- [ ] `C-CF-283` `capability` A generating clip shows its streamed preview inline. `src: Core features, instruction.md`
- [ ] `C-CF-284` `capability` A generating clip sharpens in place under continued trimming around the clip. `src: Core features, instruction.md`
- [ ] `C-CF-285` `capability` Edits are reversible across generation boundaries. `src: Core features, instruction.md`
- [ ] `C-CF-286` `capability` The document saves itself continuously, so a reload restores the exact edit state. `src: Core features, instruction.md`
- [ ] `C-CF-287` `capability` A shared pool of accelerators serves many concurrent jobs. `src: Core features, instruction.md`
- [ ] `C-CF-288` `capability` The scheduler places each job by model type, memory, batch compatibility, queue depth. `src: Core features, instruction.md`
- [ ] `C-CF-289` `capability` The scheduler reports a truthful wait before the requester commits. `src: Core features, instruction.md`
- [ ] `C-CF-290` `capability` Compatible jobs batch without pushing any single job past its latency budget. `src: Core features, instruction.md`
- [ ] `C-CF-291` `capability` The pool grows on queue depth under a spend ceiling. `src: Core features, instruction.md`
- [ ] `C-CF-292` `capability` The pool drains interruptible capacity gracefully, checkpointing, requeueing. `src: Core features, instruction.md`
- [ ] `C-CF-293` `constraint` The pool never loses a job. `src: Core features, instruction.md`
- [ ] `C-CF-294` `capability` A per-account concurrency limit stops one heavy user starving others. `src: Core features, instruction.md`
- [ ] `C-CF-295` `capability` A weighted-fair queue stops one heavy user starving others. `src: Core features, instruction.md`
- [ ] `C-CF-296` `capability` Under saturation the system sheds to a smaller model rather than refusing requests. `src: Core features, instruction.md`
- [ ] `C-CF-297` `capability` Generated clips are first-class citizens of one document under one clip abstraction. `src: Core features, instruction.md`
- [ ] `C-CF-298` `capability` Uploaded clips are first-class citizens of one document under one clip abstraction. `src: Core features, instruction.md`
- [ ] `C-CF-299` `data` A clip carries a common contract regardless of how the pixels were produced. `src: Core features, instruction.md`
- [ ] `C-CF-300` `capability` A conforming layer reconciles frame rate, resolution, aspect, colour. `src: Core features, instruction.md`
- [ ] `C-CF-301` `capability` A generated shot reads as one grade beside a filmed shot. `src: Core features, instruction.md`
- [ ] `C-CF-302` `capability` Playback composites lightweight proxies, swapping to full resolution only where needed. `src: Core features, instruction.md`
- [ ] `C-CF-303` `capability` Every clip resolves to one master timebase. `src: Core features, instruction.md`
- [ ] `C-CF-304` `capability` Transitions, overlaps, audio alignment stay exact across origins. `src: Core features, instruction.md`
- [ ] `C-CF-305` `capability` Export renders the blended timeline to one file deterministically. `src: Core features, instruction.md`
- [ ] `C-CF-306` `capability` Importing an export is stable. `src: Core features, instruction.md`
- [ ] `C-CF-307` `capability` Every generation is a durable addressable task. `src: Core features, instruction.md`
- [ ] `C-CF-308` `capability` Submission returns a task identifier immediately. `src: Core features, instruction.md`
- [ ] `C-CF-309` `data` A task moves through queued, running, then one terminal state of succeeded, failed, cancelled. `src: Core features, instruction.md`
- [ ] `C-CF-310` `capability` A task is observable by polling. `src: Core features, instruction.md`
- [ ] `C-CF-311` `capability` A task is observable by a push channel. `src: Core features, instruction.md`
- [ ] `C-CF-312` `capability` Submission is idempotent under a client-supplied key, so a retry creates no second job. `src: Core features, instruction.md`
- [ ] `C-CF-313` `capability` A task is cancellable. `src: Core features, instruction.md`
- [ ] `C-CF-314` `data` A task carries structured error detail. `src: Core features, instruction.md`
- [ ] `C-CF-315` `capability` A task exposes progress. `src: Core features, instruction.md`
- [ ] `C-CF-316` `capability` A task retains its artifact for a stated window. `src: Core features, instruction.md`
- [ ] `C-CF-317` `contract` A create call returns a handle, a separate wait call resolves the handle. `src: Core features, instruction.md`
- [ ] `C-CF-318` `capability` One router endpoint accepts a request plus a declared preference of cost, latency, quality. `src: Core features, instruction.md`
- [ ] `C-CF-319` `capability` The router endpoint accepts a price ceiling. `src: Core features, instruction.md`
- [ ] `C-CF-320` `capability` The router routes each call to the best-fitting model without the caller naming one. `src: Core features, instruction.md`
- [ ] `C-CF-321` `capability` The router keeps a live scorecard per model. `src: Core features, instruction.md`
- [ ] `C-CF-322` `capability` The router picks the model maximising the chosen objective inside the ceiling. `src: Core features, instruction.md`
- [ ] `C-CF-323` `capability` The router honours fleet state. `src: Core features, instruction.md`
- [ ] `C-CF-324` `capability` The router falls back deterministically when its first choice is saturated. `src: Core features, instruction.md`
- [ ] `C-CF-325` `data` The router records which model served each request. `src: Core features, instruction.md`
- [ ] `C-CF-326` `capability` The preference is set once, applying until changed. `src: Core features, instruction.md`
- [ ] `C-CF-327` `capability` The price ceiling is set once, applying until changed. `src: Core features, instruction.md`
- [ ] `C-CF-328` `capability` Many models from the platform, from third parties, sit behind one interface. `src: Core features, instruction.md`
- [ ] `C-CF-329` `data` Every model is described by the same uniform spec. `src: Core features, instruction.md`
- [ ] `C-CF-330` `capability` An evaluation harness runs one prompt across a chosen set of models. `src: Core features, instruction.md`
- [ ] `C-CF-331` `capability` The evaluation harness returns outputs side by side with per-model quality, speed, cost. `src: Core features, instruction.md`
- [ ] `C-CF-332` `capability` Adding a model is data rather than a code change. `src: Core features, instruction.md`
- [ ] `C-CF-333` `contract` The catalog reads the one model spec. `src: Core features, instruction.md`
- [ ] `C-CF-334` `contract` The router reads the one model spec. `src: Core features, instruction.md`
- [ ] `C-CF-335` `contract` The metering reads the one model spec. `src: Core features, instruction.md`
- [ ] `C-CF-336` `capability` Every generation is metered by output unit. `src: Core features, instruction.md`
- [ ] `C-CF-337` `capability` A metered generation is drawn from an account credit balance or billed against a plan. `src: Core features, instruction.md`
- [ ] `C-CF-338` `data` Cost is recorded per model, per endpoint, per team. `src: Core features, instruction.md`
- [ ] `C-CF-339` `capability` Cost is shown in near-real-time. `src: Core features, instruction.md`
- [ ] `C-CF-340` `capability` Cost is billed on one consolidated invoice. `src: Core features, instruction.md`
- [ ] `C-CF-341` `capability` A spend limit is enforced before a job runs rather than after. `src: Core features, instruction.md`
- [ ] `C-CF-342` `capability` A spend alert is enforced before a job runs rather than after. `src: Core features, instruction.md`
- [ ] `C-CF-343` `capability` One balance serves the studio, the interface, the connector alike. `src: Core features, instruction.md`
- [ ] `C-CF-344` `capability` Generated media carries a tamper-evident signed credential. `src: Core features, instruction.md`
- [ ] `C-CF-345` `data` The credential records that the content is machine-generated, which model produced the content, when. `src: Core features, instruction.md`
- [ ] `C-CF-346` `capability` The credential is embedded in the export. `src: Core features, instruction.md`
- [ ] `C-CF-347` `capability` The credential is verifiable by a public checker. `src: Core features, instruction.md`
- [ ] `C-CF-348` `capability` Provenance survives the blended timeline at clip granularity. `src: Core features, instruction.md`
- [ ] `C-CF-349` `capability` A mixed export declares which frames are synthetic. `src: Core features, instruction.md`
- [ ] `C-CF-350` `capability` Removing the credential is detectable. `src: Core features, instruction.md`
- [ ] `C-CF-351` `capability` The engine is reachable from an external chat agent through a standard connector. `src: Core features, instruction.md`
- [ ] `C-CF-352` `capability` The engine is reachable from an external coding agent through a standard connector. `src: Core features, instruction.md`
- [ ] `C-CF-353` `capability` The user registers the connector address in their agent, then signs in with their platform account. `src: Core features, instruction.md`
- [ ] `C-CF-354` `constraint` No separate key is needed for the connector. `src: Core features, instruction.md`
- [ ] `C-CF-355` `capability` The agent invokes generation as tools, receiving the streamed results inline. `src: Core features, instruction.md`
- [ ] `C-CF-356` `capability` A generation invoked through the connector meters against the same balance. `src: Core features, instruction.md`
- [ ] `C-CF-357` `capability` A generation invoked through the connector honours the same plan, the same model access. `src: Core features, instruction.md`

## C-UF User flow

- [ ] `C-UF-01` `ui` The information architecture is one public marketing tree, one public developer tree, one signed-in editorial tree. `src: User flow, instruction.md`
- [ ] `C-UF-02` `literal` The route `/` serves the marketing home, eleven sections, light, public. `src: User flow, instruction.md`
- [ ] `C-UF-03` `literal` The route `/api-platform` serves the developer portal, dark, its own slim chrome, public. `src: User flow, instruction.md`
- [ ] `C-UF-04` `literal` The route `/mcp` serves the agent connector, light, public. `src: User flow, instruction.md`
- [ ] `C-UF-05` `literal` The route `/news` lists published news items newest first, public. `src: User flow, instruction.md`
- [ ] `C-UF-06` `literal` The route `/news/{slug}` serves one published news item, public. `src: User flow, instruction.md`
- [ ] `C-UF-07` `literal` The route `/models` serves the model catalog as a comparison table, public. `src: User flow, instruction.md`
- [ ] `C-UF-08` `literal` The route `/models/{slug}` serves one model record with its full spec, public. `src: User flow, instruction.md`
- [ ] `C-UF-09` `literal` The route `/pricing` serves plans plus the per-second model prices, public. `src: User flow, instruction.md`
- [ ] `C-UF-10` `literal` The route `/privacy` serves the privacy page, linked from every footer, public. `src: User flow, instruction.md`
- [ ] `C-UF-11` `literal` The route `/terms` serves the terms page, linked from every footer, linked from the sign-up form, public. `src: User flow, instruction.md`
- [ ] `C-UF-12` `literal` The route `/signup` serves the sign-up form, public. `src: User flow, instruction.md`
- [ ] `C-UF-13` `literal` The sign-up form is the one public action touching state. `src: User flow, instruction.md`
- [ ] `C-UF-14` `literal` The route `/login` serves sign-in, public. `src: User flow, instruction.md`
- [ ] `C-UF-15` `literal` The route `/media/{key}` is the only public path to a stored object. `src: User flow, instruction.md`
- [ ] `C-UF-16` `literal` The route `/sitemap.xml` lists every public route, public. `src: User flow, instruction.md`
- [ ] `C-UF-17` `literal` The route `/robots.txt` names the sitemap location, public. `src: User flow, instruction.md`
- [ ] `C-UF-18` `literal` The route `/favicon.ico` serves the site icon, public. `src: User flow, instruction.md`
- [ ] `C-UF-19` `literal` The route `/studio` serves the signed-in editorial home to any account. `src: User flow, instruction.md`
- [ ] `C-UF-20` `literal` The route `/studio/news` serves the author's own news items, drafts included, to an `author`. `src: User flow, instruction.md`
- [ ] `C-UF-21` `literal` The route `/studio/news/{id}` serves one item with the compose panel over the list, to the owning `author`. `src: User flow, instruction.md`
- [ ] `C-UF-22` `literal` The route `/studio/models` serves the model records as an editable table to an `author`. `src: User flow, instruction.md`
- [ ] `C-UF-23` `literal` The route `/studio/models/{id}` serves one model record to the owning `author`. `src: User flow, instruction.md`
- [ ] `C-UF-24` `literal` The route `/studio/account` serves the signed-in account's own settings to any account. `src: User flow, instruction.md`
- [ ] `C-UF-25` `literal` The route `/api/health` serves readiness, public. `src: User flow, instruction.md`
- [ ] `C-UF-26` `contract` An unauthenticated request to any `/studio` route lands on `/login`. `src: User flow, instruction.md`
- [ ] `C-UF-27` `contract` An unauthenticated request to a `/studio` route preserves the intended route. `src: User flow, instruction.md`
- [ ] `C-UF-28` `contract` Signing in returns the actor to the intended route. `src: User flow, instruction.md`
- [ ] `C-UF-29` `contract` Signing out revokes the session on the server, landing on `/`. `src: User flow, instruction.md`
- [ ] `C-UF-30` `ui` A token expiring mid-compose returns the author to `/login` with the composed work preserved. `src: User flow, instruction.md`
- [ ] `C-UF-31` `ui` The composed work is restored after signing in again. `src: User flow, instruction.md`
- [ ] `C-UF-32` `ui` A signed-in `reader` requesting a compose route is told which permission is required. `src: User flow, instruction.md`
- [ ] `C-UF-33` `ui` A signed-in `reader` requesting a compose route is told which role holds the required permission. `src: User flow, instruction.md`
- [ ] `C-UF-34` `contract` An anonymous request for an unpublished item answers exactly as a request for something that does not exist. `src: User flow, instruction.md`
- [ ] `C-UF-35` `contract` An anonymous request for a private object answers exactly as a request for something that does not exist. `src: User flow, instruction.md`
- [ ] `C-UF-36` `contract` Any other unresolved address renders the not-found shell, answering not-found. `src: User flow, instruction.md`
- [ ] `C-UF-37` `ui` A visitor opening `/` sees the hero fill the viewport with a dark tile. `src: User flow, instruction.md`
- [ ] `C-UF-38` `literal` The hero line a visitor reads first is `Building Real-World Intelligence`. `src: User flow, instruction.md`
- [ ] `C-UF-39` `ui` Opening the `Dev` item in the top bar drops a mega-menu panel of destinations. `src: User flow, instruction.md`
- [ ] `C-UF-40` `ui` Opening a top-bar item flips the item's chevron. `src: User flow, instruction.md`
- [ ] `C-UF-41` `ui` The `Dev` mega-menu leads to `/api-platform`. `src: User flow, instruction.md`
- [ ] `C-UF-42` `ui` A visitor on the portal reads the four capability columns. `src: User flow, instruction.md`
- [ ] `C-UF-43` `ui` A visitor on the portal scans the model comparison table. `src: User flow, instruction.md`
- [ ] `C-UF-44` `ui` Using the copy control on the code panel places the text-to-video sample on the clipboard. `src: User flow, instruction.md`
- [ ] `C-UF-45` `ui` Opening `/signup` presents an address field, a password field. `src: User flow, instruction.md`
- [ ] `C-UF-46` `contract` Submitting the sign-up form creates the account. `src: User flow, instruction.md`
- [ ] `C-UF-47` `ui` The sign-up result is a full-page confirmation naming the account. `src: User flow, instruction.md`
- [ ] `C-UF-48` `contract` Signing in with the submitted details works. `src: User flow, instruction.md`
- [ ] `C-UF-49` `ui` An author signed in as `author@example.com` opens `/studio/news` to a list of four items with their statuses. `src: User flow, instruction.md`
- [ ] `C-UF-50` `ui` Choosing the create action slides a panel over the list. `src: User flow, instruction.md`
- [ ] `C-UF-51` `ui` The list stays on screen behind the compose panel. `src: User flow, instruction.md`
- [ ] `C-UF-52` `ui` An author enters a title, a dek, a body, alternative text, then attaches a poster, then saves. `src: User flow, instruction.md`
- [ ] `C-UF-53` `ui` Saving closes the compose panel. `src: User flow, instruction.md`
- [ ] `C-UF-54` `ui` An inline banner confirms the save. `src: User flow, instruction.md`
- [ ] `C-UF-55` `ui` The saved item appears in the list at status `draft`. `src: User flow, instruction.md`
- [ ] `C-UF-56` `contract` The route `/news` does not show a draft. `src: User flow, instruction.md`
- [ ] `C-UF-57` `contract` A signed-out request for `/news/the-media-router-preview` answers exactly as `/news/no-such-item-at-all` answers. `src: User flow, instruction.md`
- [ ] `C-UF-58` `contract` A draft poster's key copied from the studio answers at `/media/{key}` exactly as a key that does not exist answers. `src: User flow, instruction.md`
- [ ] `C-UF-59` `contract` The object is still in the store after the refused fetch. `src: User flow, instruction.md`
- [ ] `C-UF-60` `contract` The item is unchanged after the refused fetch. `src: User flow, instruction.md`
- [ ] `C-UF-61` `ui` An owning author opening the draft, then publishing, lands on a full-page confirmation. `src: User flow, instruction.md`
- [ ] `C-UF-62` `contract` The route `/news` lists the item after publication. `src: User flow, instruction.md`
- [ ] `C-UF-63` `contract` The route `/news/the-media-router-preview` reads after publication. `src: User flow, instruction.md`
- [ ] `C-UF-64` `contract` The poster fetches after publication. `src: User flow, instruction.md`
- [ ] `C-UF-65` `contract` No other item changed status during publication. `src: User flow, instruction.md`
- [ ] `C-UF-66` `contract` Creating an item whose poster carries empty alternative text, then attempting publication, is refused. `src: User flow, instruction.md`
- [ ] `C-UF-67` `ui` The refusal for empty alternative text names the field. `src: User flow, instruction.md`
- [ ] `C-UF-68` `contract` An item refused publication is still at status `draft`. `src: User flow, instruction.md`
- [ ] `C-UF-69` `contract` An `author@example.com` session requesting `/news/partner-campaign-preview` gets the same refusal an anonymous caller gets. `src: User flow, instruction.md`
- [ ] `C-UF-70` `contract` The second author's draft poster is not fetchable by the first author. `src: User flow, instruction.md`
- [ ] `C-UF-71` `contract` A `reader@example.com` session sees only published items at `/news`. `src: User flow, instruction.md`
- [ ] `C-UF-72` `contract` A `reader@example.com` session is refused `/studio/news` with the permission named. `src: User flow, instruction.md`
- [ ] `C-UF-73` `contract` A `reader@example.com` session cannot read the draft. `src: User flow, instruction.md`
- [ ] `C-UF-74` `contract` A `reader@example.com` session cannot fetch the draft's poster. `src: User flow, instruction.md`
- [ ] `C-UF-75` `ui` Every list carries an empty state naming what to do next. `src: User flow, instruction.md`
- [ ] `C-UF-76` `ui` An empty state offers the primary creating action. `src: User flow, instruction.md`
- [ ] `C-UF-77` `ui` Every list carries a separate filtered-to-empty state naming the active filter. `src: User flow, instruction.md`
- [ ] `C-UF-78` `ui` A filtered-to-empty state offers to clear the filter. `src: User flow, instruction.md`
- [ ] `C-UF-79` `ui` Every route carries a loading state in which the document arrives complete. `src: User flow, instruction.md`
- [ ] `C-UF-80` `ui` Each media tile holds its poster until its stream attaches. `src: User flow, instruction.md`
- [ ] `C-UF-81` `contract` Denied responses match not-found responses for an anonymous caller. `src: User flow, instruction.md`
- [ ] `C-UF-82` `contract` Denied responses differ from not-found responses for a signed-in caller. `src: User flow, instruction.md`
- [ ] `C-UF-83` `ui` A degraded dependency replaces its own region with a retry control naming what is unavailable. `src: User flow, instruction.md`
- [ ] `C-UF-84` `ui` The rest of the page works around a degraded region. `src: User flow, instruction.md`
- [ ] `C-UF-85` `ui` An error never crashes the page. `src: User flow, instruction.md`
- [ ] `C-UF-86` `ui` An error screen carries a copyable correlation identifier. `src: User flow, instruction.md`
- [ ] `C-UF-87` `ui` An error screen says whether retrying can succeed. `src: User flow, instruction.md`
- [ ] `C-UF-88` `constraint` An error screen shows no stack trace. `src: User flow, instruction.md`
- [ ] `C-UF-89` `constraint` An error screen shows no internal identifier. `src: User flow, instruction.md`
- [ ] `C-UF-90` `constraint` An error screen shows no hint that a hidden item exists. `src: User flow, instruction.md`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Somebody arriving on the home page understands in the first moment that the company turns typed words into moving pictures. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-02` `ui` The home page reads as cinematic rather than technical. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-03` `ui` A reader on the developer portal decides on that page whether the platform is worth calling. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-04` `ui` The portal answers what the models do, what the models cost, what the code looks like. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-05` `ui` Two registers run off one token set. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-06` `ui` The marketing surfaces are consumer, editorial, light, spacious, atmospheric. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-07` `ui` On a marketing surface the moving image is seen first, largest. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-08` `ui` The developer portal is operational: dark, dense, comparative. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-09` `ui` The portal is built for a reader checking numbers rather than being moved. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-10` `ui` The signed-in studio follows the portal's register. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-11` `ui` On a marketing surface the image wins the tiebreak. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-12` `ui` On the portal the number wins the tiebreak. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-13` `ui` Colour is one token set with a light projection, a dark projection. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-14` `constraint` Colour is never two systems. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-15` `ui` On light the page ground is a near-white neutral, primary text a near-black neutral. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-16` `ui` On dark the ground becomes a near-black neutral, the text a near-white neutral. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-17` `ui` A raised panel sits one step off its ground on either projection. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-18` `ui` A border is a deep cool neutral in both projections. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-19` `ui` A divider is a deep cool neutral in both projections. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-20` `ui` Muted body text is a light cool neutral. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-21` `ui` A second lighter cool neutral carries text that must recede further. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-22` `ui` A scrim is a near-black neutral at low alpha. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-23` `ui` The accents run one warm-to-cool spectrum shared by both projections. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-24` `ui` A light soft magenta is the gradient's start. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-25` `ui` A light soft indigo is the gradient's end. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-26` `ui` A near-white soft blue is the soft violet. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-27` `ui` A light soft orange is the warm accent. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-28` `ui` A light muted green is the positive accent. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-29` `ui` A light vivid blue is the electric accent. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-30` `ui` A light vivid red is the alert. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-31` `ui` A mid vivid red is the alert's pressed state. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-32` `ui` The signature gradient is a top-to-bottom wash from the magenta into the indigo. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-33` `ui` The signature gradient appears on accent chips, on highlight strokes. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-34` `constraint` The signature gradient appears nowhere else. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-35` `ui` A state that is neither positive nor alert borrows neither of those colours. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-36` `ui` A translucency ladder of white at fixed steps carries every glass surface. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-37` `ui` A translucency ladder of black at fixed steps carries every scrim, every border on dark. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-38` `constraint` An alpha is picked from the ladder, never invented. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-39` `ui` Every colour role stays separable in both projections. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-40` `ui` Three families carry the product, each named exactly. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-41` `literal` The interface face is the grotesque sans `Inter` at weights `300`, `400`, `500`, `600`. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-42` `literal` The interface fallback stack is `"Helvetica Neue", "Arial", sans-serif`. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-43` `literal` The display accent is the high-contrast serif `Playfair Display` at a single cut. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-44` `literal` The display fallback is `Georgia, "Times New Roman", serif`. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-45` `constraint` The display serif is reserved for display moments rather than used as a second body face. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-46` `literal` Code is the monospace `IBM Plex Mono` at `400`. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-47` `literal` The monospace fallback stack is `"Menlo", "Monaco", "Consolas", "Courier New", ui-monospace, monospace`. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-48` `literal` Body renders at `16px` over `24px` at `400`. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-49` `literal` Lead renders at `22px` over `29.7px` at `400`. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-50` `literal` Dense body renders at `16px` over `20.8px` at `400`. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-51` `literal` Small renders at `14px` over `22px` at `400`. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-52` `literal` Label renders at `14px` over `17.5px` at `500`. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-53` `literal` Micro renders at `13px` over `16.9px` at `400`. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-54` `literal` Badge renders at `11px` over `14.3px` at `450`. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-55` `literal` Title renders at `24px` over `24px` at `400`. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-56` `ui` Above the rendered scale sit named display steps, named heading steps. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-57` `ui` Text never disappears during a face download, so the fallback shows, then is replaced. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-58` `ui` Corners soften in a small ladder. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-59` `ui` The workhorse softening belongs to cards, to inputs. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-60` `ui` Buttons sit one step tighter than a card. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-61` `ui` The code panel takes a step looser than a card. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-62` `ui` The hero tile takes a step looser than a card. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-63` `ui` A call-to-action text button is a full pill. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-64` `ui` A circular media control is a full pill. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-65` `ui` Depth is layered rather than shadowed. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-66` `ui` The sticky header floats above the page. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-67` `ui` Menus float above the header. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-68` `ui` Modal surfaces float above menus. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-69` `ui` The one real shadow is the soft drop beneath a developer capability column. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-70` `ui` A dark card takes its depth from a radial glow behind the art. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-71` `ui` Density is spacious on the marketing surfaces. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-72` `ui` Density is compact on the portal, in the studio. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-73` `ui` The layout archetype is a top navigation. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-74` `ui` The sticky bar carries the wordmark at the inline start. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-75` `ui` The sticky bar carries seven items in the centre, each opening a mega-menu. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-76` `ui` The sticky bar carries three actions at the inline end. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-77` `ui` The sticky bar is transparent over the dark hero, opaque once scrolled. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-78` `ui` The portal wears its own slimmer bar with no mega-menu. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-79` `ui` The studio model catalog is table-first, one row per model. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-80` `ui` The table columns hold the same fields in the same order, so two models compare by eye. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-81` `ui` The card rail survives beside the table as the browsing view on the portal. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-82` `ui` Composing an item opens a panel sliding over the list the item belongs to. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-83` `ui` Two acts end a task rather than continuing one, landing on a full page. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-84` `ui` Completing the sign-up form lands on a full page. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-85` `ui` Publishing an item lands on a full page. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-86` `ui` Everything other than those two acts confirms inline. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-87` `ui` Motion is quick, understated. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-88` `ui` One house curve starts smoothly, stops smoothly, carrying almost all motion. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-89` `ui` A snappier curve carries colour changes, navigation changes. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-90` `ui` An ease-in carries exits. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-91` `ui` An expressive curve with a long tail carries the showier reveals. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-92` `ui` Durations cluster into a fast state change, a default, a deliberate one. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-93` `ui` The deliberate duration belongs to anything larger than a control. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-94` `ui` A plain fade in is a named moment. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-95` `ui` A paired enter with an exit serves modals, popovers. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-96` `ui` A drawer slides in from the inline end, back out again. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-97` `ui` A popover drops a short distance during its fade. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-98` `ui` A centred toast rises as the toast appears. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-99` `ui` A spin carries loading. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-100` `ui` A pulse carries a pending state. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-101` `ui` A gentler pulse carries a loading avatar. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-102` `ui` A first-run intro reaches full strength a third of the way through, then holds. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-103` `ui` The trusted-by marquee drifts endlessly, linearly, taking well over a minute for a lap. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-104` `ui` The trusted-by marquee runs on a timer rather than on scroll position. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-105` `ui` The code panel fades once when a language tab changes, holding its end state. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-106` `ui` The mega-menu chevron flips as its panel opens. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-107` `ui` Only transform, opacity animate on the marquee, on the carousels. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-108` `constraint` Neither the marquee nor a carousel forces the page to re-lay-out. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-109` `ui` Under reduced motion the marquee holds still. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-110` `ui` Under reduced motion every keyframe enter collapses to its end state. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-111` `ui` Under reduced motion a video poster replaces autoplay. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-112` `constraint` Under reduced motion nothing becomes invisible, nothing is left mid-travel. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-113` `ui` Text meets WCAG AA contrast against its background in both projections. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-114` `ui` The muted tone is reserved for large text, for secondary text. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-115` `ui` The whole product is operable by keyboard navigation with a visible focus ring. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-116` `ui` The mega-menu is operable by keyboard. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-117` `ui` The switcher tabs are operable by keyboard. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-118` `ui` The carousels are operable by keyboard. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-119` `ui` The accordion is operable by keyboard. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-120` `ui` The media controls are operable by keyboard. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-121` `ui` An icon-only control announces the action rather than the icon. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-122` `ui` The pause control says pause, says play, rather than naming a glyph. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-123` `ui` A link opening a new tab says so. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-124` `ui` Landmarks are one banner, one contentinfo, one main per route. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-125` `ui` Every content image carries alternative text. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-126` `ui` A decorative image declares itself decorative. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-127` `ui` Status carries a second signal beyond colour. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-128` `ui` Responsive behaviour holds at every width between the tiers. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-129` `ui` At the narrowest width the sections stack to one column. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-130` `ui` At the narrowest width the multi-column footer folds. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-131` `ui` At the narrowest width the four-column bento folds. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-132` `ui` At the narrowest width the switcher becomes swipeable. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-133` `ui` At the narrowest width the carousels become swipeable. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-134` `ui` Whether a control responds to a hovering pointer is decided by hover capability rather than by viewport width. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-135` `ui` Every hover affordance has a tap equivalent. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-136` `constraint` Nothing depends on hovering. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-137` `constraint` The page never scrolls sideways at any width. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-138` `ui` The layout survives text scaled well beyond its default without losing content. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-139` `constraint` No page is dominated by a single hue family with no second signal. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-140` `constraint` No decoration stands in for content. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-141` `constraint` No developer portal reads as a marketing page. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-142` `constraint` No marketing page reads as a dashboard. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-143` `constraint` No model card differs in spec order from the card beside the model card. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-144` `constraint` No media tile shows an empty rectangle during loading. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-145` `ui` Atmosphere beats density on the marketing surfaces. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-146` `ui` Comparability beats atmosphere on the portal. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-147` `ui` Space beats dividers. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-148` `ui` Stillness beats feedback during a signup. `src: UI/UX notes, instruction.md`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The product runs two palettes off one set of named tokens. `src: Front-end specification, instruction.md`
- [ ] `C-FE-02` `constraint` Two systems that happen to agree are not built. `src: Front-end specification, instruction.md`
- [ ] `C-FE-03` `ui` A near-white neutral is the light page ground, the dark projection's text colour, the most-used value in the system. `src: Front-end specification, instruction.md`
- [ ] `C-FE-04` `ui` A near-black neutral is the primary text on light, the fill of the dark hero. `src: Front-end specification, instruction.md`
- [ ] `C-FE-05` `ui` A deep cool neutral is the secondary dark surface. `src: Front-end specification, instruction.md`
- [ ] `C-FE-06` `ui` A deep neutral is the tertiary dark surface. `src: Front-end specification, instruction.md`
- [ ] `C-FE-07` `ui` A near-black neutral at full strength is the pure overlay. `src: Front-end specification, instruction.md`
- [ ] `C-FE-08` `ui` A second near-black neutral is the developer portal's page ground. `src: Front-end specification, instruction.md`
- [ ] `C-FE-09` `ui` A deep cool neutral carries borders on dark. `src: Front-end specification, instruction.md`
- [ ] `C-FE-10` `ui` A deep cool neutral carries dividers on dark. `src: Front-end specification, instruction.md`
- [ ] `C-FE-11` `ui` A light cool neutral is muted body text. `src: Front-end specification, instruction.md`
- [ ] `C-FE-12` `ui` A second lighter cool neutral is the text that must recede further. `src: Front-end specification, instruction.md`
- [ ] `C-FE-13` `ui` A near-black cool neutral is the developer portal's raised panel. `src: Front-end specification, instruction.md`
- [ ] `C-FE-14` `ui` A deep neutral is the lowest interface layer. `src: Front-end specification, instruction.md`
- [ ] `C-FE-15` `ui` A light soft magenta is the gradient's start accent role. `src: Front-end specification, instruction.md`
- [ ] `C-FE-16` `ui` A light soft indigo is the gradient's end accent role. `src: Front-end specification, instruction.md`
- [ ] `C-FE-17` `ui` A near-white soft blue is the soft violet accent role. `src: Front-end specification, instruction.md`
- [ ] `C-FE-18` `ui` A light soft orange is the warm accent role. `src: Front-end specification, instruction.md`
- [ ] `C-FE-19` `ui` A light muted green is the positive accent role. `src: Front-end specification, instruction.md`
- [ ] `C-FE-20` `ui` A light vivid blue is the electric accent role. `src: Front-end specification, instruction.md`
- [ ] `C-FE-21` `ui` A light vivid red is the soft alert role. `src: Front-end specification, instruction.md`
- [ ] `C-FE-22` `ui` A second sharper light vivid red is the alert proper. `src: Front-end specification, instruction.md`
- [ ] `C-FE-23` `ui` A light vivid red is the destructive role. `src: Front-end specification, instruction.md`
- [ ] `C-FE-24` `ui` A mid vivid red is the destructive pressed state. `src: Front-end specification, instruction.md`
- [ ] `C-FE-25` `ui` The focus ring is a mid vivid blue at partial strength. `src: Front-end specification, instruction.md`
- [ ] `C-FE-26` `ui` Rationing the signature gradient is what makes the gradient memorable. `src: Front-end specification, instruction.md`
- [ ] `C-FE-27` `ui` The translucency ladder is white at a rising series of fixed alphas. `src: Front-end specification, instruction.md`
- [ ] `C-FE-28` `ui` The translucency ladder is black at its own rising series of fixed alphas. `src: Front-end specification, instruction.md`
- [ ] `C-FE-29` `ui` Every glass surface picks a step from the ladder. `src: Front-end specification, instruction.md`
- [ ] `C-FE-30` `ui` Every border on dark picks a step from the ladder. `src: Front-end specification, instruction.md`
- [ ] `C-FE-31` `ui` Every scrim picks a step from the ladder. `src: Front-end specification, instruction.md`
- [ ] `C-FE-32` `ui` The interface face carries four weights. `src: Front-end specification, instruction.md`
- [ ] `C-FE-33` `ui` The display serif carries a single cut. `src: Front-end specification, instruction.md`
- [ ] `C-FE-34` `ui` The monospace carries a single cut. `src: Front-end specification, instruction.md`
- [ ] `C-FE-35` `ui` The named type steps are a display medium, a display large, a display extra-small. `src: Front-end specification, instruction.md`
- [ ] `C-FE-36` `ui` The named type steps include five heading levels. `src: Front-end specification, instruction.md`
- [ ] `C-FE-37` `ui` The named type steps include a large paragraph, a small paragraph. `src: Front-end specification, instruction.md`
- [ ] `C-FE-38` `ui` The named type steps include a caption, an eyebrow. `src: Front-end specification, instruction.md`
- [ ] `C-FE-39` `ui` The named type steps include a body-copy variant, a call-to-action text step. `src: Front-end specification, instruction.md`
- [ ] `C-FE-40` `ui` Each named step maps onto the rendered scale. `src: Front-end specification, instruction.md`
- [ ] `C-FE-41` `constraint` No step outside the rendered scale is invented. `src: Front-end specification, instruction.md`
- [ ] `C-FE-42` `ui` The hero heading carries a soft wide low-opacity shadow. `src: Front-end specification, instruction.md`
- [ ] `C-FE-43` `ui` The hero lead carries a soft wide low-opacity shadow. `src: Front-end specification, instruction.md`
- [ ] `C-FE-44` `constraint` The hero shadow is the only text shadow in the product. `src: Front-end specification, instruction.md`
- [ ] `C-FE-45` `ui` The smallest radius step belongs to the tightest chips. `src: Front-end specification, instruction.md`
- [ ] `C-FE-46` `ui` One step up belongs to buttons, to small chips. `src: Front-end specification, instruction.md`
- [ ] `C-FE-47` `ui` The workhorse radius belongs to cards, to inputs. `src: Front-end specification, instruction.md`
- [ ] `C-FE-48` `ui` Above the workhorse sit media tiles. `src: Front-end specification, instruction.md`
- [ ] `C-FE-49` `ui` Above media tiles sits the code panel. `src: Front-end specification, instruction.md`
- [ ] `C-FE-50` `ui` At the top of the radius ladder sits the full pill. `src: Front-end specification, instruction.md`
- [ ] `C-FE-51` `ui` A circular arrow button on the carousel is a true circle rather than a pill. `src: Front-end specification, instruction.md`
- [ ] `C-FE-52` `ui` Spacing comes off one rhythm rather than being chosen per section. `src: Front-end specification, instruction.md`
- [ ] `C-FE-53` `ui` A small spacing step sits inside a control. `src: Front-end specification, instruction.md`
- [ ] `C-FE-54` `ui` A larger spacing step sits between controls. `src: Front-end specification, instruction.md`
- [ ] `C-FE-55` `ui` A larger step again sits between a heading, its body. `src: Front-end specification, instruction.md`
- [ ] `C-FE-56` `ui` The largest spacing step sits between one section, the next. `src: Front-end specification, instruction.md`
- [ ] `C-FE-57` `ui` Layout is a centred column. `src: Front-end specification, instruction.md`
- [ ] `C-FE-58` `ui` A marketing section runs full-bleed with an inner measure. `src: Front-end specification, instruction.md`
- [ ] `C-FE-59` `ui` The portal's bento sits inside the same measure. `src: Front-end specification, instruction.md`
- [ ] `C-FE-60` `ui` The studio's lists sit inside the same measure. `src: Front-end specification, instruction.md`
- [ ] `C-FE-61` `ui` The developer portal chrome has a fixed height. `src: Front-end specification, instruction.md`
- [ ] `C-FE-62` `ui` The page below the developer chrome starts at a fixed gap. `src: Front-end specification, instruction.md`
- [ ] `C-FE-63` `ui` The developer bar never crowds the first section below. `src: Front-end specification, instruction.md`
- [ ] `C-FE-64` `ui` Layering has four levels: page content, the sticky header, overlays with menus, modal surfaces. `src: Front-end specification, instruction.md`
- [ ] `C-FE-65` `ui` A dialog sitting above everything has its own topmost level. `src: Front-end specification, instruction.md`
- [ ] `C-FE-66` `constraint` No level is invented between two of the four. `src: Front-end specification, instruction.md`
- [ ] `C-FE-67` `ui` Four easings carry everything, named by character rather than by number. `src: Front-end specification, instruction.md`
- [ ] `C-FE-68` `ui` The house easing starts smoothly, stops smoothly. `src: Front-end specification, instruction.md`
- [ ] `C-FE-69` `ui` A snappier easing carries colour, navigation. `src: Front-end specification, instruction.md`
- [ ] `C-FE-70` `ui` An ease-in easing carries exits. `src: Front-end specification, instruction.md`
- [ ] `C-FE-71` `ui` An expressive easing with a long tail carries the showier reveals. `src: Front-end specification, instruction.md`
- [ ] `C-FE-72` `ui` The runtime animation catalogue is the named list in the UI notes. `src: Front-end specification, instruction.md`
- [ ] `C-FE-73` `constraint` Every animation in the product is one catalogue entry rather than a new one invented at the call site. `src: Front-end specification, instruction.md`
- [ ] `C-FE-74` `ui` An icon is drawn as geometry. `src: Front-end specification, instruction.md`
- [ ] `C-FE-75` `constraint` No icon ships as a file. `src: Front-end specification, instruction.md`
- [ ] `C-FE-76` `ui` An icon is a small set of strokes at a square box. `src: Front-end specification, instruction.md`
- [ ] `C-FE-77` `ui` An icon is painted with the current colour, so the surrounding token decides the colour. `src: Front-end specification, instruction.md`
- [ ] `C-FE-78` `ui` An icon carries round caps, round joins. `src: Front-end specification, instruction.md`
- [ ] `C-FE-79` `ui` An icon carries a consistent hairline stroke unless a mark says otherwise. `src: Front-end specification, instruction.md`
- [ ] `C-FE-80` `ui` The interface icon set carries a chevron pointing down. `src: Front-end specification, instruction.md`
- [ ] `C-FE-81` `ui` The interface icon set carries a chevron pointing right. `src: Front-end specification, instruction.md`
- [ ] `C-FE-82` `ui` The interface icon set carries an arrow right, an arrow left. `src: Front-end specification, instruction.md`
- [ ] `C-FE-83` `ui` The interface icon set carries an arrow pointing up, to the right. `src: Front-end specification, instruction.md`
- [ ] `C-FE-84` `ui` The copy mark is a square over a partial square. `src: Front-end specification, instruction.md`
- [ ] `C-FE-85` `ui` The pause mark is two vertical bars. `src: Front-end specification, instruction.md`
- [ ] `C-FE-86` `ui` The globe mark is a circle crossed by one horizontal line, one elliptical meridian. `src: Front-end specification, instruction.md`
- [ ] `C-FE-87` `ui` The mute mark is a speaker whose sound arcs are struck through by a diagonal. `src: Front-end specification, instruction.md`
- [ ] `C-FE-88` `ui` The wordmark is a six-glyph lowercase mark on a wide short box. `src: Front-end specification, instruction.md`
- [ ] `C-FE-89` `ui` The wordmark is substituted by an original six-letter mark at the same proportion. `src: Front-end specification, instruction.md`
- [ ] `C-FE-90` `ui` The menu mark is three stacked rules on a wide short box. `src: Front-end specification, instruction.md`
- [ ] `C-FE-91` `ui` The brand set carries a social mark. `src: Front-end specification, instruction.md`
- [ ] `C-FE-92` `ui` The brand set carries a four-quadrant sign-in mark. `src: Front-end specification, instruction.md`
- [ ] `C-FE-93` `ui` The application mark is four squares in a two-by-two grid. `src: Front-end specification, instruction.md`
- [ ] `C-FE-94` `constraint` A partner logo is never reproduced. `src: Front-end specification, instruction.md`
- [ ] `C-FE-95` `ui` A partner logo becomes a name-tile carrying the partner's placeholder name. `src: Front-end specification, instruction.md`
- [ ] `C-FE-96` `ui` The marketing header is a sticky top bar on the header layer. `src: Front-end specification, instruction.md`
- [ ] `C-FE-97` `ui` The marketing header is transparent over the dark hero, opaque once scrolled. `src: Front-end specification, instruction.md`
- [ ] `C-FE-98` `ui` The marketing header carries the wordmark at the inline start. `src: Front-end specification, instruction.md`
- [ ] `C-FE-99` `ui` The marketing header carries seven top-level items in the centre. `src: Front-end specification, instruction.md`
- [ ] `C-FE-100` `ui` A top-level item is a text label beside a downward chevron opening a mega-menu. `src: Front-end specification, instruction.md`
- [ ] `C-FE-101` `literal` The seven top-level labels read `Creative`, `Dev`, `Robotics`, `Research`, `Resources`, `Enterprise`, `Pricing`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-102` `literal` The marketing header carries `Enterprise Sales` as text at the inline end. `src: Front-end specification, instruction.md`
- [ ] `C-FE-103` `literal` The marketing header carries `Login` as text at the inline end. `src: Front-end specification, instruction.md`
- [ ] `C-FE-104` `literal` The marketing header carries `Try Lumina` as a filled dark pill at the inline end. `src: Front-end specification, instruction.md`
- [ ] `C-FE-105` `ui` On the light document the wordmark is the near-black neutral. `src: Front-end specification, instruction.md`
- [ ] `C-FE-106` `ui` On the light document the header links are the near-black neutral. `src: Front-end specification, instruction.md`
- [ ] `C-FE-107` `ui` Over the dark hero the wordmark inverts to the near-white neutral. `src: Front-end specification, instruction.md`
- [ ] `C-FE-108` `ui` Over the dark hero the header links invert to the near-white neutral. `src: Front-end specification, instruction.md`
- [ ] `C-FE-109` `ui` Opening a top-level item drops a panel of destination columns. `src: Front-end specification, instruction.md`
- [ ] `C-FE-110` `ui` The item's chevron flips as its panel opens. `src: Front-end specification, instruction.md`
- [ ] `C-FE-111` `ui` A mega-menu link carries an underline on hover. `src: Front-end specification, instruction.md`
- [ ] `C-FE-112` `literal` The `Creative` menu lists `Overview`, `Agent`, `Android app`, `iOS app`, `MCP`, `Use Cases`, `Pricing`, `Login`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-113` `literal` The `Dev` menu lists `Platform`, `Models`, `Model Router`, `Workflows`, `Recipes`, `Characters`, `Documentation`, `Pricing`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-114` `literal` The `Robotics` menu lists `Overview`, `Policy Model`, `Offline Policy Evaluation`, `Data Augmentation`, `Video Model Licensing`, `Get Access`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-115` `literal` The `Enterprise` menu lists `Overview`, `Data Security`, `Customer Stories`, `For Education`, `Contact Sales`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-116` `literal` The `Research` menu lists `Research Hub`, `Research News`, `Publications`, `General World Models`, `Worldscape-1`, `Nova-4.5`, `Chisel-2.0`, `Perform-2`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-117` `literal` The `Resources` menu lists `Academy`, `Help Center`, `Resource Hub`, `News`, `Changelog`, `Meetups`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-118` `literal` The `Events & Programs` menu lists `AI Festival`, `AI Summit 2026`, `Gen:48`, `Studios`, `Creative Partners Program`, `Lumina Builders`, `Affiliate Program`, `Talent Network`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-119` `literal` The `Company` menu lists `About Us`, `Careers`, `Safety`, `Brand Guidelines`, `Press`, `Partnerships`, plus a content-credentials destination. `src: Front-end specification, instruction.md`
- [ ] `C-FE-120` `ui` The developer-portal header is a separate slimmer chrome at a fixed height. `src: Front-end specification, instruction.md`
- [ ] `C-FE-121` `literal` The developer chrome lockup carries `Lumina Dev` as its accessible name even where the lockup renders as a mark. `src: Front-end specification, instruction.md`
- [ ] `C-FE-122` `ui` The `Docs` destination carries an up-right arrow marking a new tab. `src: Front-end specification, instruction.md`
- [ ] `C-FE-123` `ui` The developer chrome carries a ghost sign-in button. `src: Front-end specification, instruction.md`
- [ ] `C-FE-124` `ui` The developer chrome carries a filled sign-up button. `src: Front-end specification, instruction.md`
- [ ] `C-FE-125` `constraint` The developer chrome carries neither the mega-menu nor the marketing footer. `src: Front-end specification, instruction.md`
- [ ] `C-FE-126` `ui` The footer is a large multi-column sitemap on every marketing route. `src: Front-end specification, instruction.md`
- [ ] `C-FE-127` `literal` The footer groups destinations under `Creative`, `Dev`, `Robotics`, `Enterprise`, `Research`, `Resources`, `Events & Programs`, `Company`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-128` `ui` A divider separates the sitemap from the legal row. `src: Front-end specification, instruction.md`
- [ ] `C-FE-129` `literal` The footer copyright eyebrow reads `(c) 2026 Lumina AI, Inc.`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-130` `literal` The footer legal row lists `Terms of Use`, `Privacy Policy`, `California Notices`, `Cookie Settings`, `Code of Conduct`, `System Status`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-131` `ui` A marketing navigation link eases its label from full strength to a soft light neutral. `src: Front-end specification, instruction.md`
- [ ] `C-FE-132` `ui` The doubled-glyph layers behind a navigation label ease with the label. `src: Front-end specification, instruction.md`
- [ ] `C-FE-133` `ui` The doubled-glyph easing is what makes the wipe read as crisp rather than as a fade. `src: Front-end specification, instruction.md`
- [ ] `C-FE-134` `ui` On the light document a navigation link runs from the near-black neutral to the soft light neutral. `src: Front-end specification, instruction.md`
- [ ] `C-FE-135` `ui` A filled pill eases its background one step darker on the dark projection. `src: Front-end specification, instruction.md`
- [ ] `C-FE-136` `ui` A filled pill eases its background one step cooler on the light projection. `src: Front-end specification, instruction.md`
- [ ] `C-FE-137` `ui` A filled pill's hover runs over the fast duration. `src: Front-end specification, instruction.md`
- [ ] `C-FE-138` `ui` A developer navigation link raises its opacity from partial to full on hover. `src: Front-end specification, instruction.md`
- [ ] `C-FE-139` `ui` A developer navigation link warms its colour on hover. `src: Front-end specification, instruction.md`
- [ ] `C-FE-140` `ui` A developer secondary button inverts its label from the near-white neutral to a near-black one. `src: Front-end specification, instruction.md`
- [ ] `C-FE-141` `ui` A developer secondary button inverts its background from transparent to the near-white neutral. `src: Front-end specification, instruction.md`
- [ ] `C-FE-142` `ui` A developer secondary button inverts its border from the deep cool neutral to the near-white neutral. `src: Front-end specification, instruction.md`
- [ ] `C-FE-143` `ui` A ghost button drops slightly in opacity rather than changing colour. `src: Front-end specification, instruction.md`
- [ ] `C-FE-144` `ui` A media tile is a rounded container clipped to its own radius. `src: Front-end specification, instruction.md`
- [ ] `C-FE-145` `ui` A hero tile softens a step looser than a card tile. `src: Front-end specification, instruction.md`
- [ ] `C-FE-146` `ui` A media tile stacks a poster, a video, an overlay. `src: Front-end specification, instruction.md`
- [ ] `C-FE-147` `ui` The poster layer is a sharp still frame. `src: Front-end specification, instruction.md`
- [ ] `C-FE-148` `ui` Behind the sharp frame sits a low-resolution copy blurred heavily, scaled up very slightly. `src: Front-end specification, instruction.md`
- [ ] `C-FE-149` `ui` The blur bleeds past the frame edge rather than stopping at a visible line. `src: Front-end specification, instruction.md`
- [ ] `C-FE-150` `ui` The video layer is delivered in segments, so playback starts quickly. `src: Front-end specification, instruction.md`
- [ ] `C-FE-151` `ui` The overlay scrim is fully transparent for the top half of the tile. `src: Front-end specification, instruction.md`
- [ ] `C-FE-152` `ui` The overlay scrim darkens to a strong but not opaque black at the bottom edge. `src: Front-end specification, instruction.md`
- [ ] `C-FE-153` `ui` A caption survives any frame beneath the scrim. `src: Front-end specification, instruction.md`
- [ ] `C-FE-154` `ui` The sharp poster holds at full strength until the video's first frame is decoded. `src: Front-end specification, instruction.md`
- [ ] `C-FE-155` `ui` The poster then eases away, revealing the video beneath. `src: Front-end specification, instruction.md`
- [ ] `C-FE-156` `constraint` A media tile is never empty, never flashes. `src: Front-end specification, instruction.md`
- [ ] `C-FE-157` `ui` A tile control carries a blurred backdrop. `src: Front-end specification, instruction.md`
- [ ] `C-FE-158` `ui` A tile control carries a layered ring of a hairline light stroke over a soft dark drop. `src: Front-end specification, instruction.md`
- [ ] `C-FE-159` `ui` The logo marquee translates a track horizontally under an edge-fade mask. `src: Front-end specification, instruction.md`
- [ ] `C-FE-160` `ui` The edge-fade mask is transparent at both edges, opaque across the middle. `src: Front-end specification, instruction.md`
- [ ] `C-FE-161` `ui` The marquee track is duplicated head to tail, so the loop never shows a seam. `src: Front-end specification, instruction.md`
- [ ] `C-FE-162` `ui` The marquee is a linear endless animation on a timer. `src: Front-end specification, instruction.md`
- [ ] `C-FE-163` `ui` The model-card rail sits under a one-sided fade mask. `src: Front-end specification, instruction.md`
- [ ] `C-FE-164` `ui` The one-sided mask is opaque until near the trailing edge, transparent at that edge. `src: Front-end specification, instruction.md`
- [ ] `C-FE-165` `ui` The rail is advanced by circular arrow buttons. `src: Front-end specification, instruction.md`
- [ ] `C-FE-166` `ui` An arrow button drops to a low opacity when nothing further lies in that direction. `src: Front-end specification, instruction.md`
- [ ] `C-FE-167` `ui` A tiling fractal-noise texture sits at low opacity in an overlay blend over the connector page's dark panels. `src: Front-end specification, instruction.md`
- [ ] `C-FE-168` `ui` The grain texture is desaturated, so the grain reads as tonal rather than as colour speckle. `src: Front-end specification, instruction.md`
- [ ] `C-FE-169` `ui` A developer card takes its depth from a radial wash behind the art. `src: Front-end specification, instruction.md`
- [ ] `C-FE-170` `ui` The radial wash runs from a deep rose through a darker rose to a near-black neutral. `src: Front-end specification, instruction.md`
- [ ] `C-FE-171` `ui` The home document title reads `Lumina | Building Real-World Intelligence`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-172` `ui` The home document is light, running eleven sections. `src: Front-end specification, instruction.md`
- [ ] `C-FE-173` `ui` The hero lead paragraph names foundational Real-World Intelligence that can understand, simulate, act in the world. `src: Front-end specification, instruction.md`
- [ ] `C-FE-174` `ui` The hero lead paragraph names products built on top of that intelligence for individuals, for organizations. `src: Front-end specification, instruction.md`
- [ ] `C-FE-175` `literal` The home primary action reads `Try Lumina for free`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-176` `literal` The switcher panel `Lumina Creative` carries a display line about a complete creative suite. `src: Front-end specification, instruction.md`
- [ ] `C-FE-177` `ui` The `Lumina Creative` body names an all-in-one cloud-based creative platform for video, images, audio in one workspace. `src: Front-end specification, instruction.md`
- [ ] `C-FE-178` `literal` The `Lumina Creative` actions read `Try now`, `Learn more`, `For Enterprise`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-179` `literal` The switcher panel `Lumina Dev` carries a display line about the AI media platform for developers. `src: Front-end specification, instruction.md`
- [ ] `C-FE-180` `ui` The `Lumina Dev` body names the API platform with the company's expertise built in. `src: Front-end specification, instruction.md`
- [ ] `C-FE-181` `literal` The `Lumina Dev` actions read `Get API Key`, `View documentation`, `For Enterprise`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-182` `literal` The switcher panel `Lumina Robotics` carries a display line about a complete toolkit for policy inference through photorealistic simulation. `src: Front-end specification, instruction.md`
- [ ] `C-FE-183` `ui` The `Lumina Robotics` body names every component as powered by the company's state-of-the-art General World Model. `src: Front-end specification, instruction.md`
- [ ] `C-FE-184` `literal` The `Lumina Robotics` actions read `Learn more`, `Contact Sales`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-185` `literal` A caption under the Creative panel reads `Used by 60m+ creatives around the world. Try free, cancel anytime.`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-186` `ui` The research band heading names foundational General World Models capable of simulating all possible worlds. `src: Front-end specification, instruction.md`
- [ ] `C-FE-187` `ui` The research card `Worldscape-1` is described as a state-of-the-art General World Model built to interact with the real world. `src: Front-end specification, instruction.md`
- [ ] `C-FE-188` `ui` The research card `Nova-4.5` is described as the world's best video model. `src: Front-end specification, instruction.md`
- [ ] `C-FE-189` `ui` The research card `General World Models` is described as the long-term research effort into systems understanding the visual world. `src: Front-end specification, instruction.md`
- [ ] `C-FE-190` `literal` The news card `Introducing Lumina Media Router` describes the first preference-optimized router for generative media. `src: Front-end specification, instruction.md`
- [ ] `C-FE-191` `literal` The news card `How Partner 1 Used Lumina to Produce Their Latest National TV Spot` describes a broadcast-ready campaign built from photos of real members. `src: Front-end specification, instruction.md`
- [ ] `C-FE-192` `ui` A news card titled as the AI media report on cost, on speed, on what comes next describes findings from hundreds of enterprises. `src: Front-end specification, instruction.md`
- [ ] `C-FE-193` `ui` A news card announcing a London headquarters names a world model research hub reaching the UK, reaching Europe. `src: Front-end specification, instruction.md`
- [ ] `C-FE-194` `literal` The portal title reads `Lumina Developer Portal`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-195` `literal` The portal hero title reads `The AI Media Platform` over `for Developers`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-196` `ui` The portal hero subtitle names the best image, video, audio, real-time models on one enterprise-grade platform. `src: Front-end specification, instruction.md`
- [ ] `C-FE-197` `literal` The portal hero actions read `Get API Key`, `Explore Models`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-198` `literal` The portal trusted-by marquee is labelled `Trusted by`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-199` `literal` The bento heading reads `One API for production` over `media generation.`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-200` `ui` The bento subtitle names models, workflows, recipes, characters deployed through a single integration. `src: Front-end specification, instruction.md`
- [ ] `C-FE-201` `literal` The `Access` column is titled `Every capability, one integration`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-202` `literal` The `Access` column action reads `Get API Key`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-203` `literal` The `Evaluate` column is titled `Compare before you ship`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-204` `literal` The `Evaluate` column action reads `Evaluate models`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-205` `literal` The `Automate` column is titled `Let the platform pick`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-206` `literal` The `Automate` column action reads `Set up a Router`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-207` `ui` The `Control` column title names monitoring spend across models, across teams. `src: Front-end specification, instruction.md`
- [ ] `C-FE-208` `literal` The `Control` column action reads `View usage`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-209` `ui` A bento column action inverts its label to the near-black neutral on hover. `src: Front-end specification, instruction.md`
- [ ] `C-FE-210` `ui` A bento column action inverts its background to the near-white neutral on hover. `src: Front-end specification, instruction.md`
- [ ] `C-FE-211` `ui` A bento column action inverts its border from the deep cool neutral to the near-white neutral on hover. `src: Front-end specification, instruction.md`
- [ ] `C-FE-212` `literal` The router heading reads `Model Routers for` over `Optimization`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-213` `ui` The router description names a set once for cost, latency, quality, plus a price ceiling. `src: Front-end specification, instruction.md`
- [ ] `C-FE-214` `literal` The router action reads `Set up a router`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-215` `literal` The integration heading reads `Seamless Integration`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-216` `literal` The Node sample imports `LuminaClient` from `@lumina/sdk`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-217` `literal` The Node sample constructs a client with no arguments. `src: Front-end specification, instruction.md`
- [ ] `C-FE-218` `literal` The Node sample calls `client.textToVideo.create` with a prompt text. `src: Front-end specification, instruction.md`
- [ ] `C-FE-219` `literal` The Node sample passes `model` as `"Nova-4.5"`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-220` `literal` The Node sample passes `ratio` as `"1280:720"`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-221` `literal` The Node sample passes `duration` as `5`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-222` `literal` The Node sample passes `seed` as `692126734`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-223` `literal` The Node sample chains `waitForTaskOutput` onto the create call. `src: Front-end specification, instruction.md`
- [ ] `C-FE-224` `contract` The create-then-wait shape in the sample is the task lifecycle stated in the core features. `src: Front-end specification, instruction.md`
- [ ] `C-FE-225` `literal` The catalog heading reads `State-of-the-art` over `Models`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-226` `ui` The catalog description names models served from providers across the industry. `src: Front-end specification, instruction.md`
- [ ] `C-FE-227` `literal` The catalog actions read `View all models`, `View SDK docs`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-228` `literal` The model `Nova-4.5` is tagged `Balanced everyday video generation`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-229` `literal` The model `Nova-4.5` renders at `720p`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-230` `literal` The model `Nova-4.5` accepts inputs `Text, Image`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-231` `literal` The model `Nova-4.5` runs `Up to 10s`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-232` `literal` The model `Nova-4.5` is priced `$0.12/sec`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-233` `literal` The model `Chisel-2.0` is tagged `Precise video editing`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-234` `literal` The model `Chisel-2.0` renders at `Matches input`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-235` `literal` The model `Chisel-2.0` accepts inputs `Text, Video`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-236` `literal` The model `Chisel-2.0` is priced `$0.18/sec`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-237` `literal` The model `Worldscape-1` is tagged `General world simulation`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-238` `literal` The model `Worldscape-1` renders at `720p`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-239` `literal` The model `Worldscape-1` accepts aspect ratios `16:9, 1:1`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-240` `literal` The model `Worldscape-1` is priced `$0.30/sec`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-241` `literal` The model `Perform-2` is tagged `Performance capture`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-242` `literal` The model `Perform-2` accepts inputs `Video`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-243` `literal` The model `Perform-2` accepts aspect ratios `16:9, 9:16, 1:1`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-244` `literal` The model `Perform-2` is priced `$0.09/sec`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-245` `literal` Every model card carries the links `View documentation`, `Try in Playground`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-246` `ui` The connector title reads `Lumina Agent Connector | Generate video from your assistant`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-247` `ui` The connector document is light. `src: Front-end specification, instruction.md`
- [ ] `C-FE-248` `ui` The connector hero's three stacked lines name generating from where somebody already works, using the product inside compatible agents, reaching a partner model beside `Nova-4.5`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-249` `literal` The connector hero action reads `Connect`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-250` `literal` The setup heading reads `Connect Lumina in seconds`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-251` `ui` The setup subhead says setting the connector up is simple, taking just a few moments. `src: Front-end specification, instruction.md`
- [ ] `C-FE-252` `literal` The first setup step is titled `Go to your assistant, Customize`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-253` `literal` The second setup step is titled `Add custom connector`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-254` `ui` The second setup step names the connector `Lumina`, showing the link beside a copy control. `src: Front-end specification, instruction.md`
- [ ] `C-FE-255` `ui` A setup step asks for a sign in with a Lumina account. `src: Front-end specification, instruction.md`
- [ ] `C-FE-256` `literal` The third setup step carries a `View setup guide` link. `src: Front-end specification, instruction.md`
- [ ] `C-FE-257` `literal` The showcase heading reads `A complete generation studio,` over `inside your agent.`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-258` `ui` The first showcase row is titled for generating images, generating videos. `src: Front-end specification, instruction.md`
- [ ] `C-FE-259` `ui` The first showcase prompt asks for two product images of a chocolate. `src: Front-end specification, instruction.md`
- [ ] `C-FE-260` `literal` The showcase row `Product marketing` is titled `Create marketing content from a link`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-261` `ui` The `Product marketing` prompt asks for a polished marketing video built from a product address. `src: Front-end specification, instruction.md`
- [ ] `C-FE-262` `literal` The showcase row `Multi-shot storytelling` is titled `Make dialogue-driven ads`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-263` `ui` The `Multi-shot storytelling` prompt asks for a playful dialogue-driven product spot with two crabs, a can of Fizz. `src: Front-end specification, instruction.md`
- [ ] `C-FE-264` `literal` The showcase row `Product sites` is titled `Add stunning product imagery to your site`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-265` `ui` The `Product sites` prompt asks for a hero video for jewelry products, plus a shopping website. `src: Front-end specification, instruction.md`
- [ ] `C-FE-266` `literal` The pill row heading reads `Access to the latest state-of-the-art models`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-267` `literal` The gallery heading reads `Just tell your agent what you need.` over `Lumina handles the rest.`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-268` `literal` The four prompt cards are labelled `Product URL to marketing video`, `Creative Product ad`, `Image to product ad`, `Product image to dialogue ad`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-269` `literal` The accordion row `What agents can connect to Lumina Connector?` answers with web apps, desktop apps, coding tools, connector-protocol apps. `src: Front-end specification, instruction.md`
- [ ] `C-FE-270` `literal` The accordion row `Which models can agents use?` answers that an agent uses models like `Nova-4.5` plus partner models by plan. `src: Front-end specification, instruction.md`
- [ ] `C-FE-271` `literal` The accordion row `How are connector generations billed?` answers that generations use Lumina credits. `src: Front-end specification, instruction.md`
- [ ] `C-FE-272` `literal` The accordion row `Is an API key required?` answers no, so the connector link plus a sign-in suffices. `src: Front-end specification, instruction.md`
- [ ] `C-FE-273` `ui` The not-found shell centres a body inside the full marketing header, the full marketing footer. `src: Front-end specification, instruction.md`
- [ ] `C-FE-274` `ui` The component architecture is one library of presentation modules over the token set. `src: Front-end specification, instruction.md`
- [ ] `C-FE-275` `ui` A page route is a thin module composing library components. `src: Front-end specification, instruction.md`
- [ ] `C-FE-276` `ui` The component library holds a header in marketing form, in developer form. `src: Front-end specification, instruction.md`
- [ ] `C-FE-277` `ui` The component library holds a mega-menu, a footer. `src: Front-end specification, instruction.md`
- [ ] `C-FE-278` `ui` The component library holds a media tile carrying its poster, video, overlay, controls. `src: Front-end specification, instruction.md`
- [ ] `C-FE-279` `ui` The component library holds a logo marquee, a card carousel with arrow buttons. `src: Front-end specification, instruction.md`
- [ ] `C-FE-280` `ui` The component library holds the platform switcher, a research card, a news card. `src: Front-end specification, instruction.md`
- [ ] `C-FE-281` `ui` The component library holds a capability column, a code sample with language tabs, category tabs. `src: Front-end specification, instruction.md`
- [ ] `C-FE-282` `ui` The component library holds a model card, a chat demonstration, a step list, an accordion. `src: Front-end specification, instruction.md`
- [ ] `C-FE-283` `ui` The component library holds buttons in filled, ghost, secondary, pill forms. `src: Front-end specification, instruction.md`
- [ ] `C-FE-284` `literal` The component library holds badges for `NEW`, for `Enterprise`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-285` `ui` The component library holds the not-found shell. `src: Front-end specification, instruction.md`
- [ ] `C-FE-286` `constraint` Three pages built separately end up with three headers, which is the failure the library prevents. `src: Front-end specification, instruction.md`
- [ ] `C-FE-287` `ui` The width tiers cluster at a phone width, a small-tablet width, a tablet width, a desktop width. `src: Front-end specification, instruction.md`
- [ ] `C-FE-288` `ui` A wide-desktop tier sits above the desktop width. `src: Front-end specification, instruction.md`
- [ ] `C-FE-289` `ui` A floor tier covers very small devices. `src: Front-end specification, instruction.md`
- [ ] `C-FE-290` `ui` Documents grow substantially at the narrowest tier because sections stack. `src: Front-end specification, instruction.md`
- [ ] `C-FE-291` `ui` That growth at the narrowest tier is expected rather than a defect. `src: Front-end specification, instruction.md`
- [ ] `C-FE-292` `ui` The eight-column footer folds to one column at the narrowest tier. `src: Front-end specification, instruction.md`
- [ ] `C-FE-293` `ui` The four-column bento folds to one column at the narrowest tier. `src: Front-end specification, instruction.md`
- [ ] `C-FE-294` `ui` Pointer capability rather than width decides whether hover affordances apply. `src: Front-end specification, instruction.md`
- [ ] `C-FE-295` `ui` Landmarks are one banner, one contentinfo, one main per route. `src: Front-end specification, instruction.md`
- [ ] `C-FE-296` `constraint` The focus ring is never suppressed. `src: Front-end specification, instruction.md`
- [ ] `C-FE-297` `ui` The mega-menu opens, closes, from the keyboard with its items reachable. `src: Front-end specification, instruction.md`
- [ ] `C-FE-298` `ui` The switcher tabs move by arrow keys with only the active tab in the tab order. `src: Front-end specification, instruction.md`
- [ ] `C-FE-299` `ui` The carousel arrows are buttons. `src: Front-end specification, instruction.md`
- [ ] `C-FE-300` `ui` An accordion row toggles independently on enter, on space. `src: Front-end specification, instruction.md`
- [ ] `C-FE-301` `ui` A media control is a button carrying its action as its name. `src: Front-end specification, instruction.md`
- [ ] `C-FE-302` `literal` The pause control announces `Pause`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-303` `literal` The mute control announces `Unmute` once muted. `src: Front-end specification, instruction.md`
- [ ] `C-FE-304` `literal` The developer lockup carries a visually hidden `Lumina Dev`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-305` `literal` A link opening a new tab carries `(opens in new tab)` in its accessible name. `src: Front-end specification, instruction.md`
- [ ] `C-FE-306` `ui` Near-black text on the near-white ground clears the contrast threshold. `src: Front-end specification, instruction.md`
- [ ] `C-FE-307` `ui` Near-white text on the near-black ground clears the contrast threshold. `src: Front-end specification, instruction.md`
- [ ] `C-FE-308` `ui` The muted light cool neutral is reserved for large text, for secondary text. `src: Front-end specification, instruction.md`
- [ ] `C-FE-309` `ui` Motion respects the reduced-motion preference in every place that moves. `src: Front-end specification, instruction.md`
- [ ] `C-FE-310` `constraint` No binary ships with the build. `src: Front-end specification, instruction.md`
- [ ] `C-FE-311` `constraint` No image file, no video file, no font file, no icon file ships. `src: Front-end specification, instruction.md`
- [ ] `C-FE-312` `ui` Every asset is produced from a recipe. `src: Front-end specification, instruction.md`
- [ ] `C-FE-313` `ui` The recipes are part of the build rather than a fallback. `src: Front-end specification, instruction.md`
- [ ] `C-FE-314` `ui` Each font family is named with a normative fallback stack. `src: Front-end specification, instruction.md`
- [ ] `C-FE-315` `ui` A font loads so the fallback shows rather than leaving text invisible. `src: Front-end specification, instruction.md`
- [ ] `C-FE-316` `constraint` Naming an open substitute is not an asset dependency. `src: Front-end specification, instruction.md`
- [ ] `C-FE-317` `constraint` Shipping a font file is an asset dependency. `src: Front-end specification, instruction.md`
- [ ] `C-FE-318` `ui` A placeholder clip is generated as a looping canvas or animated wash of the signature gradient over the near-black neutral field. `src: Front-end specification, instruction.md`
- [ ] `C-FE-319` `ui` A placeholder clip is exported to a short muted loop or rendered live behind the tile. `src: Front-end specification, instruction.md`
- [ ] `C-FE-320` `contract` The poster-first swap-when-ready contract is unchanged by placeholder generation. `src: Front-end specification, instruction.md`
- [ ] `C-FE-321` `ui` A placeholder plays a gradient loop rather than footage. `src: Front-end specification, instruction.md`
- [ ] `C-FE-322` `ui` The build states plainly that a placeholder communicates the tile's behaviour rather than its content. `src: Front-end specification, instruction.md`
- [ ] `C-FE-323` `ui` A poster is a canvas-generated gradient placeholder keyed by a seed. `src: Front-end specification, instruction.md`
- [ ] `C-FE-324` `contract` The same record always yields the same placeholder image. `src: Front-end specification, instruction.md`
- [ ] `C-FE-325` `ui` A card placeholder uses the radial rose-to-near-black wash under a soft grain. `src: Front-end specification, instruction.md`
- [ ] `C-FE-326` `ui` A background poster is the same wash at low resolution behind a heavy blur. `src: Front-end specification, instruction.md`
- [ ] `C-FE-327` `ui` A partner mark becomes a name-tile set in the interface face on a neutral chip at the card softening. `src: Front-end specification, instruction.md`
- [ ] `C-FE-328` `ui` A name-tile is greyscale on the light surface. `src: Front-end specification, instruction.md`
- [ ] `C-FE-329` `ui` A name-tile is the near-white neutral at reduced opacity on the dark surface. `src: Front-end specification, instruction.md`
- [ ] `C-FE-330` `constraint` A real partner mark is never reproduced. `src: Front-end specification, instruction.md`
- [ ] `C-FE-331` `ui` The grain is an inline fractal-noise texture at low opacity in an overlay blend. `src: Front-end specification, instruction.md`
- [ ] `C-FE-332` `ui` The favicon is generated from the wordmark geometry rather than shipped. `src: Front-end specification, instruction.md`
- [ ] `C-FE-333` `ui` The favicon is declared in the document head. `src: Front-end specification, instruction.md`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The application is rendered on the server with hydrated islands. `src: Technical requirements, instruction.md`
- [ ] `C-TR-02` `contract` The document arrives complete from the server. `src: Technical requirements, instruction.md`
- [ ] `C-TR-03` `contract` Only the parts needing behaviour become interactive in the browser. `src: Technical requirements, instruction.md`
- [ ] `C-TR-04` `ui` The mega-menu is an island. `src: Technical requirements, instruction.md`
- [ ] `C-TR-05` `ui` The platform switcher is an island. `src: Technical requirements, instruction.md`
- [ ] `C-TR-06` `ui` The carousels are islands. `src: Technical requirements, instruction.md`
- [ ] `C-TR-07` `ui` The accordion is an island. `src: Technical requirements, instruction.md`
- [ ] `C-TR-08` `ui` The code panel's tabs are an island. `src: Technical requirements, instruction.md`
- [ ] `C-TR-09` `ui` The media tiles are islands. `src: Technical requirements, instruction.md`
- [ ] `C-TR-10` `contract` The hero copy is not an island, so the hero copy reads with scripting unavailable. `src: Technical requirements, instruction.md`
- [ ] `C-TR-11` `contract` The capability bento's text is not an island, so the text reads with scripting unavailable. `src: Technical requirements, instruction.md`
- [ ] `C-TR-12` `contract` The model table is not an island, so the table reads with scripting unavailable. `src: Technical requirements, instruction.md`
- [ ] `C-TR-13` `contract` The footer sitemap is not an island, so the sitemap reads with scripting unavailable. `src: Technical requirements, instruction.md`
- [ ] `C-TR-14` `contract` The not-found shell is not an island, so the shell reads with scripting unavailable. `src: Technical requirements, instruction.md`
- [ ] `C-TR-15` `literal` The back end is `FastAPI` on `Python 3.11+`. `src: Technical requirements, instruction.md`
- [ ] `C-TR-16` `literal` The back end is served by `uvicorn`. `src: Technical requirements, instruction.md`
- [ ] `C-TR-17` `contract` One process serves the rendered documents, the JSON endpoints, the media route. `src: Technical requirements, instruction.md`
- [ ] `C-TR-18` `literal` The front end is `Astro` with islands. `src: Technical requirements, instruction.md`
- [ ] `C-TR-19` `contract` The front end is styled with a utility-class system over the token set. `src: Technical requirements, instruction.md`
- [ ] `C-TR-20` `contract` The front end is built to static output the back end serves. `src: Technical requirements, instruction.md`
- [ ] `C-TR-21` `literal` The database is `PostgreSQL 16` reached at `DATABASE_URL`. `src: Technical requirements, instruction.md`
- [ ] `C-TR-22` `literal` The same connection string arrives as `DB_URL`. `src: Technical requirements, instruction.md`
- [ ] `C-TR-23` `contract` Every record in the data model lives in the database. `src: Technical requirements, instruction.md`
- [ ] `C-TR-24` `literal` The object store is the S3-compatible `minio` instance reached over its HTTP API. `src: Technical requirements, instruction.md`
- [ ] `C-TR-25` `contract` Every uploaded byte lives in the object store. `src: Technical requirements, instruction.md`
- [ ] `C-TR-26` `contract` Sessions are server-side with an opaque cookie. `src: Technical requirements, instruction.md`
- [ ] `C-TR-27` `contract` The session cookie is HTTP-only, same-site, marked secure behind TLS. `src: Technical requirements, instruction.md`
- [ ] `C-TR-28` `contract` A signed-in session is revocable from the server. `src: Technical requirements, instruction.md`
- [ ] `C-TR-29` `contract` Signing out revokes the session rather than only clearing the browser's copy. `src: Technical requirements, instruction.md`
- [ ] `C-TR-30` `constraint` Naming a framework in the technical section does not license naming one anywhere else. `src: Technical requirements, instruction.md`
- [ ] `C-TR-31` `contract` The first document for every route arrives from the server already carrying its content. `src: Technical requirements, instruction.md`
- [ ] `C-TR-32` `contract` A view-source of `/` shows the hero heading as text. `src: Technical requirements, instruction.md`
- [ ] `C-TR-33` `contract` A view-source of `/` shows the switcher's three panel bodies as text. `src: Technical requirements, instruction.md`
- [ ] `C-TR-34` `contract` A view-source of `/` shows the footer's destinations as text. `src: Technical requirements, instruction.md`
- [ ] `C-TR-35` `contract` A view-source of `/api-platform` shows all four capability columns. `src: Technical requirements, instruction.md`
- [ ] `C-TR-36` `contract` A view-source of `/api-platform` shows every model row with its specs. `src: Technical requirements, instruction.md`
- [ ] `C-TR-37` `contract` A view-source of `/news` shows the published items' titles, deks. `src: Technical requirements, instruction.md`
- [ ] `C-TR-38` `constraint` An empty shell filled after a round trip to a JSON endpoint does not satisfy the rendering contract. `src: Technical requirements, instruction.md`
- [ ] `C-TR-39` `contract` A crawler executing no scripts still sees the content. `src: Technical requirements, instruction.md`
- [ ] `C-TR-40` `contract` An island hydrates after the document is readable. `src: Technical requirements, instruction.md`
- [ ] `C-TR-41` `constraint` No island hydrates before the document is readable. `src: Technical requirements, instruction.md`
- [ ] `C-TR-42` `contract` An accordion answer sits in the document at first render, hidden by a style rule. `src: Technical requirements, instruction.md`
- [ ] `C-TR-43` `contract` A reader without scripting still reaches an accordion answer. `src: Technical requirements, instruction.md`
- [ ] `C-TR-44` `contract` A crawler still indexes an accordion answer. `src: Technical requirements, instruction.md`
- [ ] `C-TR-45` `literal` The store is reached at `STORAGE_ENDPOINT` with `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`. `src: Technical requirements, instruction.md`
- [ ] `C-TR-46` `constraint` The bucket holds no anonymous read policy. `src: Technical requirements, instruction.md`
- [ ] `C-TR-47` `contract` A reader reaches an object only through one of the two named mechanisms. `src: Technical requirements, instruction.md`
- [ ] `C-TR-48` `constraint` A presigned address is never issued for a private object. `src: Technical requirements, instruction.md`
- [ ] `C-TR-49` `contract` A media-route request resolves the key to the item owning the key, then decides. `src: Technical requirements, instruction.md`
- [ ] `C-TR-50` `contract` A public object streams back with a content type matching the stored object. `src: Technical requirements, instruction.md`
- [ ] `C-TR-51` `contract` A public object streams back with a caching header suited to something that never changes at that key. `src: Technical requirements, instruction.md`
- [ ] `C-TR-52` `contract` A private object answers exactly as a key that does not exist answers. `src: Technical requirements, instruction.md`
- [ ] `C-TR-53` `contract` The access decision is made before any byte is read from the store. `src: Technical requirements, instruction.md`
- [ ] `C-TR-54` `constraint` A copy of uploaded bytes on the application's own disk does not count. `src: Technical requirements, instruction.md`
- [ ] `C-TR-55` `constraint` A record holding the image inline does not count. `src: Technical requirements, instruction.md`
- [ ] `C-TR-56` `contract` Every mutating endpoint is authorized on the server against the calling session. `src: Technical requirements, instruction.md`
- [ ] `C-TR-57` `contract` The authorization check happens before the work rather than after. `src: Technical requirements, instruction.md`
- [ ] `C-TR-58` `contract` A read endpoint filters by what the caller is entitled to see. `src: Technical requirements, instruction.md`
- [ ] `C-TR-59` `contract` Entitlement filtering is what makes draft responses match missing responses without special-casing at the edge. `src: Technical requirements, instruction.md`
- [ ] `C-TR-60` `contract` `/api/health` reports readiness, naming the database separately from the object store. `src: Technical requirements, instruction.md`
- [ ] `C-TR-61` `contract` `/api/auth/signup` creates an account, then starts a session. `src: Technical requirements, instruction.md`
- [ ] `C-TR-62` `contract` `/api/auth/login` starts a session. `src: Technical requirements, instruction.md`
- [ ] `C-TR-63` `contract` `/api/auth/logout` revokes the session on the server. `src: Technical requirements, instruction.md`
- [ ] `C-TR-64` `contract` `/api/news` returns published items newest first, paginated. `src: Technical requirements, instruction.md`
- [ ] `C-TR-65` `contract` `/api/news/{slug}` returns one published item. `src: Technical requirements, instruction.md`
- [ ] `C-TR-66` `contract` `/api/studio/news` read returns that author's own items, drafts included. `src: Technical requirements, instruction.md`
- [ ] `C-TR-67` `contract` `/api/studio/news` write creates a draft. `src: Technical requirements, instruction.md`
- [ ] `C-TR-68` `contract` `/api/studio/news/{id}` write edits a draft the caller owns. `src: Technical requirements, instruction.md`
- [ ] `C-TR-69` `contract` `/api/studio/news/{id}/media` uploads a poster, returning its key. `src: Technical requirements, instruction.md`
- [ ] `C-TR-70` `contract` `/api/studio/news/{id}/publish` publishes in one transaction. `src: Technical requirements, instruction.md`
- [ ] `C-TR-71` `contract` `/api/studio/news/{id}/unpublish` returns an item to draft in one transaction. `src: Technical requirements, instruction.md`
- [ ] `C-TR-72` `contract` `/api/models` returns the model catalog with full specs. `src: Technical requirements, instruction.md`
- [ ] `C-TR-73` `contract` `/api/studio/models/{id}` edits a model record for its owner. `src: Technical requirements, instruction.md`
- [ ] `C-TR-74` `contract` `/media/{key}` streams a public object, refusing a private one. `src: Technical requirements, instruction.md`
- [ ] `C-TR-75` `contract` A created record answers with the created status. `src: Technical requirements, instruction.md`
- [ ] `C-TR-76` `contract` A refused write from an unentitled session answers forbidden with the required permission named. `src: Technical requirements, instruction.md`
- [ ] `C-TR-77` `contract` An unauthenticated write answers unauthorized. `src: Technical requirements, instruction.md`
- [ ] `C-TR-78` `contract` A malformed body answers unprocessable with the offending field named. `src: Technical requirements, instruction.md`
- [ ] `C-TR-79` `contract` An unpublished item answers not-found to anyone not entitled. `src: Technical requirements, instruction.md`
- [ ] `C-TR-80` `contract` An error body carries a stable correlation identifier. `src: Technical requirements, instruction.md`
- [ ] `C-TR-81` `constraint` An error body carries no stack trace. `src: Technical requirements, instruction.md`
- [ ] `C-TR-82` `constraint` An error body carries no internal identifier. `src: Technical requirements, instruction.md`
- [ ] `C-TR-83` `constraint` An error body carries no hint that a hidden record exists. `src: Technical requirements, instruction.md`
- [ ] `C-TR-84` `contract` Validation lives on the server, which is the authority. `src: Technical requirements, instruction.md`
- [ ] `C-TR-85` `ui` The browser may repeat the same validation for courtesy. `src: Technical requirements, instruction.md`
- [ ] `C-TR-86` `contract` A request bypassing the browser is subject to the same rules. `src: Technical requirements, instruction.md`
- [ ] `C-TR-87` `constraint` An endpoint trusting a client-side check is a contract violation. `src: Technical requirements, instruction.md`
- [ ] `C-TR-88` `contract` The sign-up form requires an address shaped like an address. `src: Technical requirements, instruction.md`
- [ ] `C-TR-89` `contract` The sign-up address is unique across accounts. `src: Technical requirements, instruction.md`
- [ ] `C-TR-90` `contract` The sign-up password meets a stated minimum length. `src: Technical requirements, instruction.md`
- [ ] `C-TR-91` `contract` A duplicate address is refused without revealing whether the existing account belongs to somebody. `src: Technical requirements, instruction.md`
- [ ] `C-TR-92` `ui` A duplicate-address refusal names the field. `src: Technical requirements, instruction.md`
- [ ] `C-TR-93` `contract` An item requires a title. `src: Technical requirements, instruction.md`
- [ ] `C-TR-94` `contract` An item requires a slug unique across items. `src: Technical requirements, instruction.md`
- [ ] `C-TR-95` `contract` An item requires a dek. `src: Technical requirements, instruction.md`
- [ ] `C-TR-96` `contract` An item requires a body. `src: Technical requirements, instruction.md`
- [ ] `C-TR-97` `data` A slug is lowercase words separated by hyphens. `src: Technical requirements, instruction.md`
- [ ] `C-TR-98` `contract` Alternative text is required on a poster before the owning item can be published. `src: Technical requirements, instruction.md`
- [ ] `C-TR-99` `ui` The refusal to publish without alternative text names that field. `src: Technical requirements, instruction.md`
- [ ] `C-TR-100` `contract` A model record requires its name. `src: Technical requirements, instruction.md`
- [ ] `C-TR-101` `contract` A model record requires its tagline. `src: Technical requirements, instruction.md`
- [ ] `C-TR-102` `contract` A model record requires its resolution. `src: Technical requirements, instruction.md`
- [ ] `C-TR-103` `contract` A model record requires its aspect ratio list. `src: Technical requirements, instruction.md`
- [ ] `C-TR-104` `contract` A model record requires its input list. `src: Technical requirements, instruction.md`
- [ ] `C-TR-105` `contract` A model record requires its maximum duration. `src: Technical requirements, instruction.md`
- [ ] `C-TR-106` `contract` A model record requires its price. `src: Technical requirements, instruction.md`
- [ ] `C-TR-107` `constraint` A catalog carrying a hole in one row is not comparable. `src: Technical requirements, instruction.md`
- [ ] `C-TR-108` `contract` An upload is refused unless its declared type is one of the accepted image types. `src: Technical requirements, instruction.md`
- [ ] `C-TR-109` `contract` An upload is refused unless its size is within the stated ceiling. `src: Technical requirements, instruction.md`
- [ ] `C-TR-110` `ui` An upload refusal says which limit was exceeded. `src: Technical requirements, instruction.md`
- [ ] `C-TR-111` `constraint` The declared type is not trusted on its own. `src: Technical requirements, instruction.md`
- [ ] `C-TR-112` `contract` The stored object's type is decided from the bytes. `src: Technical requirements, instruction.md`
- [ ] `C-TR-113` `contract` Publishing changes the item's status together with the poster's visibility. `src: Technical requirements, instruction.md`
- [ ] `C-TR-114` `contract` A failure in either half of publication means neither half happened. `src: Technical requirements, instruction.md`
- [ ] `C-TR-115` `contract` A failed publication leaves the item exactly as the item was. `src: Technical requirements, instruction.md`
- [ ] `C-TR-116` `contract` Unpublishing holds the same all-or-nothing rule. `src: Technical requirements, instruction.md`
- [ ] `C-TR-117` `contract` A reader fetching the poster the instant before publication is refused. `src: Technical requirements, instruction.md`
- [ ] `C-TR-118` `contract` A reader fetching the poster the instant after publication is served. `src: Technical requirements, instruction.md`
- [ ] `C-TR-119` `constraint` No window exists in which one half of publication is true, the other false. `src: Technical requirements, instruction.md`
- [ ] `C-TR-120` `contract` Every address, credential, endpoint arrives from the environment. `src: Technical requirements, instruction.md`
- [ ] `C-TR-121` `literal` The environment supplies the session signing secret. `src: Technical requirements, instruction.md`
- [ ] `C-TR-122` `literal` The environment supplies `APP_PUBLIC_PORT`, `APP_PUBLIC_URL`. `src: Technical requirements, instruction.md`
- [ ] `C-TR-123` `constraint` No secret is present in any file reaching the browser. `src: Technical requirements, instruction.md`
- [ ] `C-TR-124` `constraint` No secret is baked into an image at build time. `src: Technical requirements, instruction.md`
- [ ] `C-TR-125` `contract` The front end receives only the public base address. `src: Technical requirements, instruction.md`
- [ ] `C-TR-126` `contract` The front end asks the server for anything else the front end needs. `src: Technical requirements, instruction.md`
- [ ] `C-TR-127` `contract` A missing required variable stops the process at start. `src: Technical requirements, instruction.md`
- [ ] `C-TR-128` `ui` The startup failure message names the missing variable. `src: Technical requirements, instruction.md`
- [ ] `C-TR-129` `constraint` The process does not start, then fail on the first request, when a variable is missing. `src: Technical requirements, instruction.md`
- [ ] `C-TR-130` `data` A structured log carries a request identifier, the route, the status, the duration. `src: Technical requirements, instruction.md`
- [ ] `C-TR-131` `constraint` A log never carries a password. `src: Technical requirements, instruction.md`
- [ ] `C-TR-132` `constraint` A log never carries a token. `src: Technical requirements, instruction.md`
- [ ] `C-TR-133` `constraint` A log never carries a session identifier. `src: Technical requirements, instruction.md`
- [ ] `C-TR-134` `constraint` A log never carries a secret. `src: Technical requirements, instruction.md`
- [ ] `C-TR-135` `contract` The readiness endpoint reports the database separately from the object store, so a degraded dependency is attributable. `src: Technical requirements, instruction.md`
- [ ] `C-TR-136` `ui` A slow object store degrades the media region to a retry control naming what is unavailable. `src: Technical requirements, instruction.md`
- [ ] `C-TR-137` `ui` The rest of the page still works around a degraded media region. `src: Technical requirements, instruction.md`
- [ ] `C-TR-138` `contract` Documents are served compressed. `src: Technical requirements, instruction.md`
- [ ] `C-TR-139` `contract` Static output is fingerprinted, served with long-lived caching. `src: Technical requirements, instruction.md`
- [ ] `C-TR-140` `constraint` A document is never cached in a way serving one account's page to another. `src: Technical requirements, instruction.md`
- [ ] `C-TR-141` `contract` A listing endpoint is paginated rather than returning every record. `src: Technical requirements, instruction.md`
- [ ] `C-TR-142` `ui` An image below the first viewport loads lazily. `src: Technical requirements, instruction.md`
- [ ] `C-TR-143` `ui` A video below the first viewport loads lazily. `src: Technical requirements, instruction.md`
- [ ] `C-TR-144` `ui` A media element carries its intrinsic proportions, so nothing on the page jumps. `src: Technical requirements, instruction.md`
- [ ] `C-TR-145` `contract` Every route carries a title, a description. `src: Technical requirements, instruction.md`
- [ ] `C-TR-146` `contract` Every route carries a canonical address. `src: Technical requirements, instruction.md`
- [ ] `C-TR-147` `contract` Every route carries the social preview tags a link unfurl needs. `src: Technical requirements, instruction.md`
- [ ] `C-TR-148` `contract` The sitemap lists every public route. `src: Technical requirements, instruction.md`
- [ ] `C-TR-149` `constraint` The sitemap lists no private route. `src: Technical requirements, instruction.md`
- [ ] `C-TR-150` `constraint` A draft's address never appears in the sitemap. `src: Technical requirements, instruction.md`
- [ ] `C-TR-151` `contract` Structured data describes the organisation on the home route. `src: Technical requirements, instruction.md`
- [ ] `C-TR-152` `contract` Structured data describes the article on a published news route. `src: Technical requirements, instruction.md`
- [ ] `C-TR-153` `contract` A response carries a content security policy. `src: Technical requirements, instruction.md`
- [ ] `C-TR-154` `contract` A response carries a referrer policy. `src: Technical requirements, instruction.md`
- [ ] `C-TR-155` `contract` A response carries a frame policy. `src: Technical requirements, instruction.md`
- [ ] `C-TR-156` `contract` A response carries a no-sniff declaration. `src: Technical requirements, instruction.md`
- [ ] `C-TR-157` `contract` A mutating request carries a cross-site request forgery defence. `src: Technical requirements, instruction.md`
- [ ] `C-TR-158` `contract` A password is stored only as a salted computationally expensive hash. `src: Technical requirements, instruction.md`
- [ ] `C-TR-159` `constraint` A stored password is never recoverable. `src: Technical requirements, instruction.md`
- [ ] `C-TR-160` `contract` Authentication endpoints are rate limited per address, per caller. `src: Technical requirements, instruction.md`
- [ ] `C-TR-161` `contract` Account-creation endpoints are rate limited per address, per caller. `src: Technical requirements, instruction.md`
- [ ] `C-TR-162` `ui` A rate-limit refusal says when to retry rather than staying silent. `src: Technical requirements, instruction.md`
- [ ] `C-TR-163` `contract` Every rendered value that came from an account is escaped where the value lands. `src: Technical requirements, instruction.md`
- [ ] `C-TR-164` `contract` The running application is inspectable from outside without any special mode. `src: Technical requirements, instruction.md`
- [ ] `C-TR-165` `contract` The readiness endpoint is the liveness signal. `src: Technical requirements, instruction.md`
- [ ] `C-TR-166` `contract` A seeded account signs in with the stated password. `src: Technical requirements, instruction.md`
- [ ] `C-TR-167` `ui` An interactive element carries a stable meaningful accessible name. `src: Technical requirements, instruction.md`
- [ ] `C-TR-168` `contract` An attachable identifier is semantic rather than positional. `src: Technical requirements, instruction.md`

## C-DM Data model

- [ ] `C-DM-01` `data` A primary key is opaque, sortable. `src: Data model, instruction.md`
- [ ] `C-DM-02` `data` Money is an integer in minor units beside a lowercase currency code. `src: Data model, instruction.md`
- [ ] `C-DM-03` `literal` The currency code is `usd`. `src: Data model, instruction.md`
- [ ] `C-DM-04` `constraint` Money is never a decimal, never a floating-point number. `src: Data model, instruction.md`
- [ ] `C-DM-05` `data` A model's price is minor units per second of output. `src: Data model, instruction.md`
- [ ] `C-DM-06` `data` An instant is UTC, assigned by the database rather than by the application. `src: Data model, instruction.md`
- [ ] `C-DM-07` `contract` Database-assigned instants are what make two processes agree. `src: Data model, instruction.md`
- [ ] `C-DM-08` `data` An enumerated value is constrained by the database rather than being free text. `src: Data model, instruction.md`
- [ ] `C-DM-09` `data` A reference between records declares what happens when its target goes away. `src: Data model, instruction.md`
- [ ] `C-DM-10` `data` A reference restricts by default. `src: Data model, instruction.md`
- [ ] `C-DM-11` `constraint` An uploaded byte is never held in a database column. `src: Data model, instruction.md`
- [ ] `C-DM-12` `constraint` An uploaded byte is never held on the application's own disk. `src: Data model, instruction.md`
- [ ] `C-DM-13` `data` The `account` record holds an email address unique without regard to case. `src: Data model, instruction.md`
- [ ] `C-DM-14` `data` The `account` record holds a display name. `src: Data model, instruction.md`
- [ ] `C-DM-15` `data` The `account` record holds a role of `author` or `reader`. `src: Data model, instruction.md`
- [ ] `C-DM-16` `data` The `account` record holds a plan. `src: Data model, instruction.md`
- [ ] `C-DM-17` `data` The `account` record holds a credit balance in minor units. `src: Data model, instruction.md`
- [ ] `C-DM-18` `data` The `account` record holds a created instant. `src: Data model, instruction.md`
- [ ] `C-DM-19` `contract` The public form creates an account exactly as the seed does. `src: Data model, instruction.md`
- [ ] `C-DM-20` `data` The `session` record holds an opaque token. `src: Data model, instruction.md`
- [ ] `C-DM-21` `data` The `session` record holds the account the session belongs to. `src: Data model, instruction.md`
- [ ] `C-DM-22` `data` The `session` record holds an issued instant, an expiry. `src: Data model, instruction.md`
- [ ] `C-DM-23` `data` The `session` record holds a revoked instant, empty until signing out fills the field. `src: Data model, instruction.md`
- [ ] `C-DM-24` `contract` Server-side revocation is why a copied cookie stops working. `src: Data model, instruction.md`
- [ ] `C-DM-25` `data` The `content_item` record holds a kind of `news` or `model_card`. `src: Data model, instruction.md`
- [ ] `C-DM-26` `data` The `content_item` record holds a slug unique within its kind. `src: Data model, instruction.md`
- [ ] `C-DM-27` `data` The `content_item` record holds a title, a dek, a body. `src: Data model, instruction.md`
- [ ] `C-DM-28` `data` The `content_item` record holds a status of `draft`, `scheduled`, `published`, `archived`. `src: Data model, instruction.md`
- [ ] `C-DM-29` `data` The `content_item` record holds the author account owning the record. `src: Data model, instruction.md`
- [ ] `C-DM-30` `data` The `content_item` record holds a published instant, empty until publication. `src: Data model, instruction.md`
- [ ] `C-DM-31` `data` The `content_item` record holds the poster media object the item displays. `src: Data model, instruction.md`
- [ ] `C-DM-32` `data` The `content_item` record holds a created instant, an updated instant. `src: Data model, instruction.md`
- [ ] `C-DM-33` `contract` Status is the only field deciding whether an anonymous caller may read the record. `src: Data model, instruction.md`
- [ ] `C-DM-34` `data` The `media_object` record holds the store key. `src: Data model, instruction.md`
- [ ] `C-DM-35` `data` The `media_object` record holds a content type decided from the bytes. `src: Data model, instruction.md`
- [ ] `C-DM-36` `constraint` The uploader's declared content type does not decide the stored type. `src: Data model, instruction.md`
- [ ] `C-DM-37` `data` The `media_object` record holds a byte length. `src: Data model, instruction.md`
- [ ] `C-DM-38` `data` The `media_object` record holds a checksum of the bytes. `src: Data model, instruction.md`
- [ ] `C-DM-39` `data` The `media_object` record holds alternative text. `src: Data model, instruction.md`
- [ ] `C-DM-40` `data` The `media_object` record holds a visibility of `private` or `public`. `src: Data model, instruction.md`
- [ ] `C-DM-41` `data` The `media_object` record holds the content item owning the object. `src: Data model, instruction.md`
- [ ] `C-DM-42` `contract` Visibility follows the owning item's status, never set on its own. `src: Data model, instruction.md`
- [ ] `C-DM-43` `data` The `model_spec` record holds a name, a tagline, a resolution. `src: Data model, instruction.md`
- [ ] `C-DM-44` `data` The `model_spec` record holds an aspect-ratio list, an input list. `src: Data model, instruction.md`
- [ ] `C-DM-45` `data` The `model_spec` record holds a maximum duration in seconds. `src: Data model, instruction.md`
- [ ] `C-DM-46` `data` The `model_spec` record holds a price in minor units per second. `src: Data model, instruction.md`
- [ ] `C-DM-47` `data` The `model_spec` record holds a provider, a documentation destination. `src: Data model, instruction.md`
- [ ] `C-DM-48` `contract` The catalog table, the carousel card, the router copy, the pricing page all read the one model record. `src: Data model, instruction.md`
- [ ] `C-DM-49` `contract` A change to a model record lands everywhere at once. `src: Data model, instruction.md`
- [ ] `C-DM-50` `data` The `menu_section` record holds its label, its position. `src: Data model, instruction.md`
- [ ] `C-DM-51` `data` The `menu_destination` record holds its label, its address. `src: Data model, instruction.md`
- [ ] `C-DM-52` `data` The `menu_destination` record holds its position within a section. `src: Data model, instruction.md`
- [ ] `C-DM-53` `data` The `menu_destination` record holds whether the destination opens in a new tab. `src: Data model, instruction.md`
- [ ] `C-DM-54` `contract` The mega-menu reads the menu records. `src: Data model, instruction.md`
- [ ] `C-DM-55` `contract` The footer sitemap reads the menu records. `src: Data model, instruction.md`
- [ ] `C-DM-56` `contract` The not-found shell reads the menu records. `src: Data model, instruction.md`
- [ ] `C-DM-57` `contract` Reading one set of menu records is what makes link integrity a property rather than a hand-maintained list. `src: Data model, instruction.md`
- [ ] `C-DM-58` `data` The `signup_lead` record holds an email address. `src: Data model, instruction.md`
- [ ] `C-DM-59` `data` The `signup_lead` record holds the route the lead came from. `src: Data model, instruction.md`
- [ ] `C-DM-60` `data` The `signup_lead` record holds the label of the control that submitted the form. `src: Data model, instruction.md`
- [ ] `C-DM-61` `data` The `signup_lead` record holds a created instant, an idempotency key. `src: Data model, instruction.md`
- [ ] `C-DM-62` `literal` The object key scheme is `media/{item_id}/{sha256_of_bytes}.{ext}`. `src: Data model, instruction.md`
- [ ] `C-DM-63` `data` The key is derived rather than chosen. `src: Data model, instruction.md`
- [ ] `C-DM-64` `data` The key runs the owning item, then the checksum of the bytes, then the extension matching the sniffed type. `src: Data model, instruction.md`
- [ ] `C-DM-65` `contract` The same bytes uploaded to the same item land at the same key. `src: Data model, instruction.md`
- [ ] `C-DM-66` `contract` Re-uploading identical bytes does not accumulate copies. `src: Data model, instruction.md`
- [ ] `C-DM-67` `contract` An item at `draft`, `scheduled`, `archived` is unreadable to an anonymous caller. `src: Data model, instruction.md`
- [ ] `C-DM-68` `contract` A draft's response matches the response a slug that never existed produces. `src: Data model, instruction.md`
- [ ] `C-DM-69` `contract` A media object owned by an item that is not `published` is unreadable to an anonymous caller by any route. `src: Data model, instruction.md`
- [ ] `C-DM-70` `contract` A media object owned by an item that is not `published` is unreadable with any key. `src: Data model, instruction.md`
- [ ] `C-DM-71` `contract` Publishing makes both changes durable together, or neither. `src: Data model, instruction.md`
- [ ] `C-DM-72` `contract` An uploaded byte exists in the object store, in no other place. `src: Data model, instruction.md`
- [ ] `C-DM-73` `contract` A published content image carries non-empty alternative text. `src: Data model, instruction.md`
- [ ] `C-DM-74` `contract` An item whose poster lacks alternative text cannot be published. `src: Data model, instruction.md`
- [ ] `C-DM-75` `data` A model's price is an integer in minor units per second. `src: Data model, instruction.md`
- [ ] `C-DM-76` `contract` Every model record carries every spec field, so a catalog row never has a hole. `src: Data model, instruction.md`
- [ ] `C-DM-77` `data` An account's email is unique without regard to case. `src: Data model, instruction.md`
- [ ] `C-DM-78` `contract` Seeding is repeatable, so restarting the application does not duplicate a row. `src: Data model, instruction.md`
- [ ] `C-DM-79` `contract` A signup arriving twice under one idempotency key creates one account. `src: Data model, instruction.md`
- [ ] `C-DM-80` `literal` Three accounts are seeded with the password `deku-demo-pw-2026`. `src: Data model, instruction.md`
- [ ] `C-DM-81` `literal` The seeded `author` accounts are `author@example.com`, `author2@example.com`. `src: Data model, instruction.md`
- [ ] `C-DM-82` `literal` The seeded `reader` account is `reader@example.com`. `src: Data model, instruction.md`
- [ ] `C-DM-83` `literal` Four model specs are seeded: `Nova-4.5`, `Chisel-2.0`, `Worldscape-1`, `Perform-2`. `src: Data model, instruction.md`
- [ ] `C-DM-84` `literal` Each seeded model spec carries the full spec row printed in the front-end section. `src: Data model, instruction.md`
- [ ] `C-DM-85` `literal` Four news items are owned by `author@example.com`. `src: Data model, instruction.md`
- [ ] `C-DM-86` `literal` Two of the first author's items are `published`. `src: Data model, instruction.md`
- [ ] `C-DM-87` `literal` One of the first author's items is a draft slugged `the-media-router-preview`. `src: Data model, instruction.md`
- [ ] `C-DM-88` `literal` One of the first author's items is `archived`. `src: Data model, instruction.md`
- [ ] `C-DM-89` `literal` One further draft slugged `partner-campaign-preview` is owned by `author2@example.com`. `src: Data model, instruction.md`
- [ ] `C-DM-90` `contract` The second author's draft gives cross-author isolation a subject. `src: Data model, instruction.md`
- [ ] `C-DM-91` `contract` Every seeded news item carries one poster media object. `src: Data model, instruction.md`
- [ ] `C-DM-92` `contract` A seeded draft's poster is `private`. `src: Data model, instruction.md`
- [ ] `C-DM-93` `contract` The seeded menu records carry every section printed in the front-end section. `src: Data model, instruction.md`
- [ ] `C-DM-94` `contract` The seeded menu records carry every destination printed in the front-end section. `src: Data model, instruction.md`
- [ ] `C-DM-95` `contract` The mega-menu, the footer, the sitemap agree because all three read the seeded menu records. `src: Data model, instruction.md`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No model runs, so no frame is produced. `src: Constraints, instruction.md`
- [ ] `C-CN-02` `constraint` No timeline is built, no graphics processor is scheduled. `src: Constraints, instruction.md`
- [ ] `C-CN-03` `constraint` The generation platform is specified as a contract, never implemented. `src: Constraints, instruction.md`
- [ ] `C-CN-04` `constraint` Plans are displayed, so nothing is charged. `src: Constraints, instruction.md`
- [ ] `C-CN-05` `constraint` No payment instrument is collected. `src: Constraints, instruction.md`
- [ ] `C-CN-06` `constraint` No third-party identity provider is used, so accounts belong to the application. `src: Constraints, instruction.md`
- [ ] `C-CN-07` `constraint` Signing up sends no message. `src: Constraints, instruction.md`
- [ ] `C-CN-08` `constraint` No password-reset flow exists. `src: Constraints, instruction.md`
- [ ] `C-CN-09` `constraint` The seeded passwords are the only credentials the environment carries. `src: Constraints, instruction.md`
- [ ] `C-CN-10` `constraint` No external network call happens at runtime beyond the database, beyond the object store. `src: Constraints, instruction.md`
- [ ] `C-CN-11` `constraint` No analytics vendor, no font service, no image host is contacted. `src: Constraints, instruction.md`
- [ ] `C-CN-12` `constraint` No partner logo is fetched from anywhere. `src: Constraints, instruction.md`
- [ ] `C-CN-13` `constraint` No binary asset of any kind ships with the build. `src: Constraints, instruction.md`
- [ ] `C-CN-14` `constraint` No real partner brand is reproduced, so a partner name is a placeholder. `src: Constraints, instruction.md`
- [ ] `C-CN-15` `constraint` A partner mark renders as a name-tile. `src: Constraints, instruction.md`
- [ ] `C-CN-16` `constraint` No comment thread exists. `src: Constraints, instruction.md`
- [ ] `C-CN-17` `constraint` No search across the site exists. `src: Constraints, instruction.md`
- [ ] `C-CN-18` `constraint` No newsletter exists. `src: Constraints, instruction.md`
- [ ] `C-CN-19` `constraint` One language is served, so no localisation exists. `src: Constraints, instruction.md`
- [ ] `C-CN-20` `constraint` No native application, no desktop client ships. `src: Constraints, instruction.md`
- [ ] `C-CN-21` `constraint` The product is responsive web only. `src: Constraints, instruction.md`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at the address in `APP_PUBLIC_URL`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-02` `literal` The app is served on the port in `APP_PUBLIC_PORT`, whose value is `4173`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-03` `contract` The port is read from the environment, never hardcoded. `src: Deployment contract, instruction.md`
- [ ] `C-DC-04` `contract` The JSON API is served on the same origin under the `/api` prefix. `src: Deployment contract, instruction.md`
- [ ] `C-DC-05` `contract` The developer portal at `/api-platform` is a rendered marketing route rather than an API. `src: Deployment contract, instruction.md`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract, instruction.md`
- [ ] `C-DC-07` `contract` The healthcheck goes green on its own. `src: Deployment contract, instruction.md`
- [ ] `C-DC-08` `constraint` Every backing service is already running before the session begins. `src: Deployment contract, instruction.md`
- [ ] `C-DC-09` `constraint` No backing service is downloaded, installed, compiled, started by the app. `src: Deployment contract, instruction.md`
- [ ] `C-DC-10` `constraint` A service address is read from the environment, never hardcoded. `src: Deployment contract, instruction.md`
- [ ] `C-DC-11` `constraint` No local file, no embedded database, no private instance substitutes for a backing service. `src: Deployment contract, instruction.md`
- [ ] `C-DC-12` `literal` The PostgreSQL instance is reached at `DATABASE_URL`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-13` `literal` The same connection string is supplied again as `DB_URL`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-14` `literal` The object store is reached at `STORAGE_ENDPOINT`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-15` `literal` The bucket name arrives as `STORAGE_BUCKET`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-16` `literal` The store credentials arrive as `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-17` `constraint` No other backend, no identity provider, no email service, no cache, no queue is used. `src: Deployment contract, instruction.md`
- [ ] `C-DC-18` `literal` The seeded accounts are written to `/app/USER_README.md` with their shared password. `src: Deployment contract, instruction.md`
- [ ] `C-DC-19` `literal` The directory `.browser_screenshots/` is reserved at the app root, left empty. `src: Deployment contract, instruction.md`
- [ ] `C-DC-20` `literal` The directory `.downloads/` is reserved at the app root, left empty. `src: Deployment contract, instruction.md`
- [ ] `C-DC-21` `contract` The front end is served as a production build behind a preview server. `src: Deployment contract, instruction.md`
- [ ] `C-DC-22` `constraint` No development server serves the front end. `src: Deployment contract, instruction.md`
- [ ] `C-DC-23` `contract` The server outlives the session. `src: Deployment contract, instruction.md`
- [ ] `C-DC-24` `contract` The server is started fully detached from the shell. `src: Deployment contract, instruction.md`
- [ ] `C-DC-25` `contract` A server started as an ordinary background job is killed the instant the session ends. `src: Deployment contract, instruction.md`
- [ ] `C-DC-26` `contract` The listener binds to `0.0.0.0`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-27` `constraint` The listener binds to neither `127.0.0.1` nor `localhost`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-28` `contract` The listening process has a parent that is not the shell. `src: Deployment contract, instruction.md`
- [ ] `C-DC-29` `constraint` No persistent volume is declared. `src: Deployment contract, instruction.md`
- [ ] `C-DC-30` `constraint` No fixed container name is declared. `src: Deployment contract, instruction.md`
- [ ] `C-DC-31` `constraint` No custom network is declared. `src: Deployment contract, instruction.md`
- [ ] `C-DC-32` `contract` The app tears down cleanly, then runs again. `src: Deployment contract, instruction.md`
- [ ] `C-DC-33` `contract` `POST /api/auth/signup` takes an email with a password, answering `201` with the account identifier, the email, the role. `src: Deployment contract, instruction.md`
- [ ] `C-DC-34` `contract` `POST /api/auth/login` takes an email with a password, answering `200` with the session bearer token. `src: Deployment contract, instruction.md`
- [ ] `C-DC-35` `contract` `POST /api/auth/logout` answers `200` or `204`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-36` `contract` `GET /api/me` answers `200` with the caller's identifier, email, role. `src: Deployment contract, instruction.md`
- [ ] `C-DC-37` `contract` `GET /api/news` takes `limit` with `offset`, answering `200` with a JSON array of published items newest first. `src: Deployment contract, instruction.md`
- [ ] `C-DC-38` `contract` `GET /api/news/{slug}` answers `200` for a published item. `src: Deployment contract, instruction.md`
- [ ] `C-DC-39` `contract` `GET /api/news/{slug}` answers `404` for an item that is not published, whoever asks. `src: Deployment contract, instruction.md`
- [ ] `C-DC-40` `contract` `GET /api/studio/news` answers `200` with a JSON array of the caller's own items. `src: Deployment contract, instruction.md`
- [ ] `C-DC-41` `contract` `GET /api/studio/news` answers `403` for a `reader` session. `src: Deployment contract, instruction.md`
- [ ] `C-DC-42` `contract` `POST /api/studio/news` takes a title, a dek, a body, a slug, answering `201` with the created item at status `draft`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-43` `contract` `PATCH /api/studio/news/{id}` takes any subset of the create fields, answering `200` with the updated item. `src: Deployment contract, instruction.md`
- [ ] `C-DC-44` `contract` `PATCH /api/studio/news/{id}` answers `403` when the caller does not own the item. `src: Deployment contract, instruction.md`
- [ ] `C-DC-45` `contract` `POST /api/studio/news/{id}/media` takes the file with its alternative text, answering `201` with the key at visibility `private`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-46` `contract` `POST /api/studio/news/{id}/publish` answers `200` with the item at status `published`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-47` `contract` `POST /api/studio/news/{id}/publish` answers `403` when the caller does not own the item. `src: Deployment contract, instruction.md`
- [ ] `C-DC-48` `contract` `POST /api/studio/news/{id}/publish` answers `409` when the item is already published. `src: Deployment contract, instruction.md`
- [ ] `C-DC-49` `contract` `POST /api/studio/news/{id}/publish` answers `422` when the poster carries no alternative text. `src: Deployment contract, instruction.md`
- [ ] `C-DC-50` `contract` `POST /api/studio/news/{id}/unpublish` answers `200` with the item at status `draft`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-51` `contract` `GET /api/models` answers `200` with a JSON array of model specs each carrying every spec field. `src: Deployment contract, instruction.md`
- [ ] `C-DC-52` `contract` `GET /media/{key}` answers `200` with the object's bytes at the stored content type. `src: Deployment contract, instruction.md`
- [ ] `C-DC-53` `contract` `GET /media/{key}` answers `404` when the object is private to the caller. `src: Deployment contract, instruction.md`
- [ ] `C-DC-54` `contract` `GET /api/health` answers `200` with a status, a database status, a storage status. `src: Deployment contract, instruction.md`
- [ ] `C-DC-55` `contract` Every business-rule violation answers `4xx` naming the reason. `src: Deployment contract, instruction.md`
- [ ] `C-DC-56` `constraint` No business-rule violation answers `5xx`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-57` `constraint` No business-rule violation answers a silent `200`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-58` `contract` Every endpoint under `/api/studio` requires a valid session. `src: Deployment contract, instruction.md`
- [ ] `C-DC-59` `contract` An anonymous caller to a studio endpoint gets `401`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-60` `contract` A signed-in caller lacking the permission gets `403` with the required permission named. `src: Deployment contract, instruction.md`
- [ ] `C-DC-61` `contract` An unpublished item returns the identical status, body, headers as a slug that never existed. `src: Deployment contract, instruction.md`
- [ ] `C-DC-62` `contract` A private object's key returns the identical status, body, headers as a key that never existed. `src: Deployment contract, instruction.md`
- [ ] `C-DC-63` `contract` Authorization on an item-scoped endpoint is enforced against the caller's session, against the caller's ownership. `src: Deployment contract, instruction.md`
- [ ] `C-DC-64` `contract` A list endpoint returns a JSON array at the top level. `src: Deployment contract, instruction.md`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `author@example.com` | the seeded account `author@example.com` holds the `author` role | `C-RL-35` |
| `author` | the seeded account `author@example.com` holds the `author` role | `C-RL-35` |
| `author2@example.com` | the seeded account `author2@example.com` holds the `author` role | `C-RL-37` |
| `reader@example.com` | the seeded account `reader@example.com` holds the `reader` role | `C-RL-39` |
| `reader` | the seeded account `reader@example.com` holds the `reader` role | `C-RL-39` |
| `deku-demo-pw-2026` | every seeded account signs in with the password `deku-demo-pw-2026` | `C-RL-41` |
| `/news/the-media-router-preview` | requesting `/news/the-media-router-preview` signed out answers exactly as `/news/no-such-item-at-all` answers | `C-CF-12` |
| `/news/no-such-item-at-all` | requesting `/news/the-media-router-preview` signed out answers exactly as `/news/no-such-item-at-all` answers | `C-CF-12` |
| `STORAGE_ENDPOINT` | the application reads `STORAGE_ENDPOINT` from the environment | `C-CF-48` |
| `STORAGE_BUCKET` | the application reads `STORAGE_BUCKET` from the environment | `C-CF-49` |
| `STORAGE_ACCESS_KEY` | the application reads `STORAGE_ACCESS_KEY` from the environment | `C-CF-50` |
| `STORAGE_SECRET_KEY` | the application reads `STORAGE_SECRET_KEY` from the environment | `C-CF-51` |
| `media/{item_id}/{sha256_of_bytes}.{ext}` | the object key follows the scheme `media/{item_id}/{sha256_of_bytes}.{ext}` | `C-CF-53` |
| `42` | a worked key for item `42` holding a WebP poster reads `media/42/9f2a1c7d4e8b6a0f3c5d2e1b8a7f6c5d4e3b2a1908f7e6d5c4b3a2918070605d.webp` | `C-CF-54` |
| `media/42/9f2a1c7d4e8b6a0f3c5d2e1b8a7f6c5d4e3b2a1908f7e6d5c4b3a2918070605d.webp` | a worked key for item `42` holding a WebP poster reads `media/42/9f2a1c7d4e8b6a0f3c5d2e1b8a7f6c5d4e3b2a1908f7e6d5c4b3a2918070605d.webp` | `C-CF-54` |
| `8` | the minimum password length is `8` | `C-CF-97` |
| `Building Real-World Intelligence` | the hero display heading reads `Building Real-World Intelligence` | `C-CF-147` |
| `Try Lumina for free` | the hero action is one filled light pill reading `Try Lumina for free` | `C-CF-149` |
| `We partner with the world's leading organizations to advance their industries:` | the partner marquee eyebrow reads `We partner with the world's leading organizations to advance their industries:` | `C-CF-153` |
| `Three platforms built on-top of the same Real-World Intelligence models` | the switcher section heading reads `Three platforms built on-top of the same Real-World Intelligence models` | `C-CF-158` |
| `Lumina Creative` | the three switcher panels are `Lumina Creative`, `Lumina Dev`, `Lumina Robotics` | `C-CF-161` |
| `Lumina Dev` | the three switcher panels are `Lumina Creative`, `Lumina Dev`, `Lumina Robotics` | `C-CF-161` |
| `Lumina Robotics` | the three switcher panels are `Lumina Creative`, `Lumina Dev`, `Lumina Robotics` | `C-CF-161` |
| `Lumina Research` | the research band eyebrow reads `Lumina Research` | `C-CF-164` |
| `Learn more` | the research band carries a `Learn more` link | `C-CF-166` |
| `See the latest from Lumina` | the news grid heading reads `See the latest from Lumina` | `C-CF-169` |
| `Explore` | the developer chrome carries `Explore` beside the lockup | `C-CF-180` |
| `Docs` | the developer chrome carries `Docs` beside the lockup | `C-CF-181` |
| `Log In` | the developer chrome carries `Log In` at the inline end | `C-CF-183` |
| `Sign Up` | the developer chrome carries `Sign Up` at the inline end | `C-CF-184` |
| `Lumina Developer Portal` | the developer portal title reads `Lumina Developer Portal` | `C-CF-187` |
| `The AI Media Platform` | the developer hero title reads `The AI Media Platform` over `for Developers` | `C-CF-189` |
| `for Developers` | the developer hero title reads `The AI Media Platform` over `for Developers` | `C-CF-189` |
| `Get API Key` | the developer hero carries the filled action `Get API Key` | `C-CF-191` |
| `Explore Models` | the developer hero carries the ghosted action `Explore Models` | `C-CF-192` |
| `Trusted by` | a trusted-by marquee labelled `Trusted by` carries developer-audience partner tiles | `C-CF-193` |
| `One API for production` | the capability bento heading reads `One API for production` over `media generation.` | `C-CF-194` |
| `media generation.` | the capability bento heading reads `One API for production` over `media generation.` | `C-CF-194` |
| `Access` | the four bento labels read `Access`, `Evaluate`, `Automate`, `Control` | `C-CF-197` |
| `Evaluate` | the four bento labels read `Access`, `Evaluate`, `Automate`, `Control` | `C-CF-197` |
| `Automate` | the four bento labels read `Access`, `Evaluate`, `Automate`, `Control` | `C-CF-197` |
| `Control` | the four bento labels read `Access`, `Evaluate`, `Automate`, `Control` | `C-CF-197` |
| `NEW` | the `Automate` column carries a `NEW` badge | `C-CF-198` |
| `Model Routers for` | the router section heading reads `Model Routers for` over `Optimization` | `C-CF-199` |
| `Optimization` | the router section heading reads `Model Routers for` over `Optimization` | `C-CF-199` |
| `Set up a router` | the router section action reads `Set up a router` | `C-CF-200` |
| `Seamless Integration` | the code sample section heading reads `Seamless Integration` | `C-CF-201` |
| `Models` | the code sample category row reads `Models`, `Workflows`, `Recipes`, `Characters` | `C-CF-202` |
| `Workflows` | the code sample category row reads `Models`, `Workflows`, `Recipes`, `Characters` | `C-CF-202` |
| `Recipes` | the code sample category row reads `Models`, `Workflows`, `Recipes`, `Characters` | `C-CF-202` |
| `Characters` | the code sample category row reads `Models`, `Workflows`, `Recipes`, `Characters` | `C-CF-202` |
| `Node` | the code sample language row reads `Node`, `Python`, `cURL` | `C-CF-203` |
| `Python` | the code sample language row reads `Node`, `Python`, `cURL` | `C-CF-203` |
| `cURL` | the code sample language row reads `Node`, `Python`, `cURL` | `C-CF-203` |
| `State-of-the-art` | the model catalog heading reads `State-of-the-art` over `Models` | `C-CF-208` |
| `View all models` | the model catalog carries the action `View all models` | `C-CF-209` |
| `View SDK docs` | the model catalog carries the action `View SDK docs` | `C-CF-210` |
| `usd` | price renders in `usd` | `C-CF-219` |
| `Nova-4.5` | `Nova-4.5` costs `12` minor units per second | `C-CF-220` |
| `12` | `Nova-4.5` costs `12` minor units per second | `C-CF-220` |
| `Chisel-2.0` | `Chisel-2.0` costs `18` minor units per second | `C-CF-221` |
| `18` | `Chisel-2.0` costs `18` minor units per second | `C-CF-221` |
| `Worldscape-1` | `Worldscape-1` costs `30` minor units per second | `C-CF-222` |
| `30` | `Worldscape-1` costs `30` minor units per second | `C-CF-222` |
| `Perform-2` | `Perform-2` costs `9` minor units per second | `C-CF-223` |
| `9` | `Perform-2` costs `9` minor units per second | `C-CF-223` |
| `Lumina Agent Connector` | the connector hero heading reads `Lumina Agent Connector` | `C-CF-228` |
| `Connect` | the connector hero action reads `Connect` | `C-CF-230` |
| `Connect Lumina in seconds` | the three-step setup heading reads `Connect Lumina in seconds` | `C-CF-232` |
| `Copy` | the second setup step carries a `Copy` control placing the address on the clipboard | `C-CF-235` |
| `A complete generation studio,` | the capability showcase heading reads `A complete generation studio,` over `inside your agent.` | `C-CF-236` |
| `inside your agent.` | the capability showcase heading reads `A complete generation studio,` over `inside your agent.` | `C-CF-236` |
| `Access to the latest state-of-the-art models` | the model pill row heading reads `Access to the latest state-of-the-art models` | `C-CF-240` |
| `Just tell your agent what you need.` | the prompt gallery heading reads `Just tell your agent what you need.` over `Lumina handles the rest.` | `C-CF-243` |
| `Lumina handles the rest.` | the prompt gallery heading reads `Just tell your agent what you need.` over `Lumina handles the rest.` | `C-CF-243` |
| `Write a message...` | the composed chat input shows a `Write a message...` field | `C-CF-246` |
| `Frequently asked questions` | the accordion heading reads `Frequently asked questions` | `C-CF-247` |
| `Take me home` | the not-found body carries a pill reading `Take me home` linking to the home route | `C-CF-256` |
| `/` | the route `/` serves the marketing home, eleven sections, light, public | `C-UF-02` |
| `/api-platform` | the route `/api-platform` serves the developer portal, dark, its own slim chrome, public | `C-UF-03` |
| `/mcp` | the route `/mcp` serves the agent connector, light, public | `C-UF-04` |
| `/news` | the route `/news` lists published news items newest first, public | `C-UF-05` |
| `/news/{slug}` | the route `/news/{slug}` serves one published news item, public | `C-UF-06` |
| `/models` | the route `/models` serves the model catalog as a comparison table, public | `C-UF-07` |
| `/models/{slug}` | the route `/models/{slug}` serves one model record with its full spec, public | `C-UF-08` |
| `/pricing` | the route `/pricing` serves plans plus the per-second model prices, public | `C-UF-09` |
| `/privacy` | the route `/privacy` serves the privacy page, linked from every footer, public | `C-UF-10` |
| `/terms` | the route `/terms` serves the terms page, linked from every footer, linked from the sign-up form, public | `C-UF-11` |
| `/signup` | the route `/signup` serves the sign-up form, public | `C-UF-12` |
| `/login` | the route `/login` serves sign-in, public | `C-UF-14` |
| `/media/{key}` | the route `/media/{key}` is the only public path to a stored object | `C-UF-15` |
| `/sitemap.xml` | the route `/sitemap.xml` lists every public route, public | `C-UF-16` |
| `/robots.txt` | the route `/robots.txt` names the sitemap location, public | `C-UF-17` |
| `/favicon.ico` | the route `/favicon.ico` serves the site icon, public | `C-UF-18` |
| `/studio` | the route `/studio` serves the signed-in editorial home to any account | `C-UF-19` |
| `/studio/news` | the route `/studio/news` serves the author's own news items, drafts included, to an `author` | `C-UF-20` |
| `/studio/news/{id}` | the route `/studio/news/{id}` serves one item with the compose panel over the list, to the owning `author` | `C-UF-21` |
| `/studio/models` | the route `/studio/models` serves the model records as an editable table to an `author` | `C-UF-22` |
| `/studio/models/{id}` | the route `/studio/models/{id}` serves one model record to the owning `author` | `C-UF-23` |
| `/studio/account` | the route `/studio/account` serves the signed-in account's own settings to any account | `C-UF-24` |
| `/api/health` | the route `/api/health` serves readiness, public | `C-UF-25` |
| `Inter` | the interface face is the grotesque sans `Inter` at weights `300`, `400`, `500`, `600` | `C-UX-41` |
| `300` | the interface face is the grotesque sans `Inter` at weights `300`, `400`, `500`, `600` | `C-UX-41` |
| `400` | the interface face is the grotesque sans `Inter` at weights `300`, `400`, `500`, `600` | `C-UX-41` |
| `500` | the interface face is the grotesque sans `Inter` at weights `300`, `400`, `500`, `600` | `C-UX-41` |
| `600` | the interface face is the grotesque sans `Inter` at weights `300`, `400`, `500`, `600` | `C-UX-41` |
| `"Helvetica Neue", "Arial", sans-serif` | the interface fallback stack is `"Helvetica Neue", "Arial", sans-serif` | `C-UX-42` |
| `Playfair Display` | the display accent is the high-contrast serif `Playfair Display` at a single cut | `C-UX-43` |
| `Georgia, "Times New Roman", serif` | the display fallback is `Georgia, "Times New Roman", serif` | `C-UX-44` |
| `IBM Plex Mono` | code is the monospace `IBM Plex Mono` at `400` | `C-UX-46` |
| `"Menlo", "Monaco", "Consolas", "Courier New", ui-monospace, monospace` | the monospace fallback stack is `"Menlo", "Monaco", "Consolas", "Courier New", ui-monospace, monospace` | `C-UX-47` |
| `16px` | body renders at `16px` over `24px` at `400` | `C-UX-48` |
| `24px` | body renders at `16px` over `24px` at `400` | `C-UX-48` |
| `22px` | lead renders at `22px` over `29.7px` at `400` | `C-UX-49` |
| `29.7px` | lead renders at `22px` over `29.7px` at `400` | `C-UX-49` |
| `20.8px` | dense body renders at `16px` over `20.8px` at `400` | `C-UX-50` |
| `14px` | small renders at `14px` over `22px` at `400` | `C-UX-51` |
| `17.5px` | label renders at `14px` over `17.5px` at `500` | `C-UX-52` |
| `13px` | micro renders at `13px` over `16.9px` at `400` | `C-UX-53` |
| `16.9px` | micro renders at `13px` over `16.9px` at `400` | `C-UX-53` |
| `11px` | badge renders at `11px` over `14.3px` at `450` | `C-UX-54` |
| `14.3px` | badge renders at `11px` over `14.3px` at `450` | `C-UX-54` |
| `450` | badge renders at `11px` over `14.3px` at `450` | `C-UX-54` |
| `Creative` | the seven top-level labels read `Creative`, `Dev`, `Robotics`, `Research`, `Resources`, `Enterprise`, `Pricing` | `C-FE-101` |
| `Dev` | the seven top-level labels read `Creative`, `Dev`, `Robotics`, `Research`, `Resources`, `Enterprise`, `Pricing` | `C-FE-101` |
| `Robotics` | the seven top-level labels read `Creative`, `Dev`, `Robotics`, `Research`, `Resources`, `Enterprise`, `Pricing` | `C-FE-101` |
| `Research` | the seven top-level labels read `Creative`, `Dev`, `Robotics`, `Research`, `Resources`, `Enterprise`, `Pricing` | `C-FE-101` |
| `Resources` | the seven top-level labels read `Creative`, `Dev`, `Robotics`, `Research`, `Resources`, `Enterprise`, `Pricing` | `C-FE-101` |
| `Enterprise` | the seven top-level labels read `Creative`, `Dev`, `Robotics`, `Research`, `Resources`, `Enterprise`, `Pricing` | `C-FE-101` |
| `Pricing` | the seven top-level labels read `Creative`, `Dev`, `Robotics`, `Research`, `Resources`, `Enterprise`, `Pricing` | `C-FE-101` |
| `Enterprise Sales` | the marketing header carries `Enterprise Sales` as text at the inline end | `C-FE-102` |
| `Login` | the marketing header carries `Login` as text at the inline end | `C-FE-103` |
| `Try Lumina` | the marketing header carries `Try Lumina` as a filled dark pill at the inline end | `C-FE-104` |
| `Overview` | the `Creative` menu lists `Overview`, `Agent`, `Android app`, `iOS app`, `MCP`, `Use Cases`, `Pricing`, `Login` | `C-FE-112` |
| `Agent` | the `Creative` menu lists `Overview`, `Agent`, `Android app`, `iOS app`, `MCP`, `Use Cases`, `Pricing`, `Login` | `C-FE-112` |
| `Android app` | the `Creative` menu lists `Overview`, `Agent`, `Android app`, `iOS app`, `MCP`, `Use Cases`, `Pricing`, `Login` | `C-FE-112` |
| `iOS app` | the `Creative` menu lists `Overview`, `Agent`, `Android app`, `iOS app`, `MCP`, `Use Cases`, `Pricing`, `Login` | `C-FE-112` |
| `MCP` | the `Creative` menu lists `Overview`, `Agent`, `Android app`, `iOS app`, `MCP`, `Use Cases`, `Pricing`, `Login` | `C-FE-112` |
| `Use Cases` | the `Creative` menu lists `Overview`, `Agent`, `Android app`, `iOS app`, `MCP`, `Use Cases`, `Pricing`, `Login` | `C-FE-112` |
| `Platform` | the `Dev` menu lists `Platform`, `Models`, `Model Router`, `Workflows`, `Recipes`, `Characters`, `Documentation`, `Pricing` | `C-FE-113` |
| `Model Router` | the `Dev` menu lists `Platform`, `Models`, `Model Router`, `Workflows`, `Recipes`, `Characters`, `Documentation`, `Pricing` | `C-FE-113` |
| `Documentation` | the `Dev` menu lists `Platform`, `Models`, `Model Router`, `Workflows`, `Recipes`, `Characters`, `Documentation`, `Pricing` | `C-FE-113` |
| `Policy Model` | the `Robotics` menu lists `Overview`, `Policy Model`, `Offline Policy Evaluation`, `Data Augmentation`, `Video Model Licensing`, `Get Access` | `C-FE-114` |
| `Offline Policy Evaluation` | the `Robotics` menu lists `Overview`, `Policy Model`, `Offline Policy Evaluation`, `Data Augmentation`, `Video Model Licensing`, `Get Access` | `C-FE-114` |
| `Data Augmentation` | the `Robotics` menu lists `Overview`, `Policy Model`, `Offline Policy Evaluation`, `Data Augmentation`, `Video Model Licensing`, `Get Access` | `C-FE-114` |
| `Video Model Licensing` | the `Robotics` menu lists `Overview`, `Policy Model`, `Offline Policy Evaluation`, `Data Augmentation`, `Video Model Licensing`, `Get Access` | `C-FE-114` |
| `Get Access` | the `Robotics` menu lists `Overview`, `Policy Model`, `Offline Policy Evaluation`, `Data Augmentation`, `Video Model Licensing`, `Get Access` | `C-FE-114` |
| `Data Security` | the `Enterprise` menu lists `Overview`, `Data Security`, `Customer Stories`, `For Education`, `Contact Sales` | `C-FE-115` |
| `Customer Stories` | the `Enterprise` menu lists `Overview`, `Data Security`, `Customer Stories`, `For Education`, `Contact Sales` | `C-FE-115` |
| `For Education` | the `Enterprise` menu lists `Overview`, `Data Security`, `Customer Stories`, `For Education`, `Contact Sales` | `C-FE-115` |
| `Contact Sales` | the `Enterprise` menu lists `Overview`, `Data Security`, `Customer Stories`, `For Education`, `Contact Sales` | `C-FE-115` |
| `Research Hub` | the `Research` menu lists `Research Hub`, `Research News`, `Publications`, `General World Models`, `Worldscape-1`, `Nova-4.5`, `Chisel-2.0`, `Perform-2` | `C-FE-116` |
| `Research News` | the `Research` menu lists `Research Hub`, `Research News`, `Publications`, `General World Models`, `Worldscape-1`, `Nova-4.5`, `Chisel-2.0`, `Perform-2` | `C-FE-116` |
| `Publications` | the `Research` menu lists `Research Hub`, `Research News`, `Publications`, `General World Models`, `Worldscape-1`, `Nova-4.5`, `Chisel-2.0`, `Perform-2` | `C-FE-116` |
| `General World Models` | the `Research` menu lists `Research Hub`, `Research News`, `Publications`, `General World Models`, `Worldscape-1`, `Nova-4.5`, `Chisel-2.0`, `Perform-2` | `C-FE-116` |
| `Academy` | the `Resources` menu lists `Academy`, `Help Center`, `Resource Hub`, `News`, `Changelog`, `Meetups` | `C-FE-117` |
| `Help Center` | the `Resources` menu lists `Academy`, `Help Center`, `Resource Hub`, `News`, `Changelog`, `Meetups` | `C-FE-117` |
| `Resource Hub` | the `Resources` menu lists `Academy`, `Help Center`, `Resource Hub`, `News`, `Changelog`, `Meetups` | `C-FE-117` |
| `News` | the `Resources` menu lists `Academy`, `Help Center`, `Resource Hub`, `News`, `Changelog`, `Meetups` | `C-FE-117` |
| `Changelog` | the `Resources` menu lists `Academy`, `Help Center`, `Resource Hub`, `News`, `Changelog`, `Meetups` | `C-FE-117` |
| `Meetups` | the `Resources` menu lists `Academy`, `Help Center`, `Resource Hub`, `News`, `Changelog`, `Meetups` | `C-FE-117` |
| `Events & Programs` | the `Events & Programs` menu lists `AI Festival`, `AI Summit 2026`, `Gen:48`, `Studios`, `Creative Partners Program`, `Lumina Builders`, `Affiliate Program`, `Talent Network` | `C-FE-118` |
| `AI Festival` | the `Events & Programs` menu lists `AI Festival`, `AI Summit 2026`, `Gen:48`, `Studios`, `Creative Partners Program`, `Lumina Builders`, `Affiliate Program`, `Talent Network` | `C-FE-118` |
| `AI Summit 2026` | the `Events & Programs` menu lists `AI Festival`, `AI Summit 2026`, `Gen:48`, `Studios`, `Creative Partners Program`, `Lumina Builders`, `Affiliate Program`, `Talent Network` | `C-FE-118` |
| `Gen:48` | the `Events & Programs` menu lists `AI Festival`, `AI Summit 2026`, `Gen:48`, `Studios`, `Creative Partners Program`, `Lumina Builders`, `Affiliate Program`, `Talent Network` | `C-FE-118` |
| `Studios` | the `Events & Programs` menu lists `AI Festival`, `AI Summit 2026`, `Gen:48`, `Studios`, `Creative Partners Program`, `Lumina Builders`, `Affiliate Program`, `Talent Network` | `C-FE-118` |
| `Creative Partners Program` | the `Events & Programs` menu lists `AI Festival`, `AI Summit 2026`, `Gen:48`, `Studios`, `Creative Partners Program`, `Lumina Builders`, `Affiliate Program`, `Talent Network` | `C-FE-118` |
| `Lumina Builders` | the `Events & Programs` menu lists `AI Festival`, `AI Summit 2026`, `Gen:48`, `Studios`, `Creative Partners Program`, `Lumina Builders`, `Affiliate Program`, `Talent Network` | `C-FE-118` |
| `Affiliate Program` | the `Events & Programs` menu lists `AI Festival`, `AI Summit 2026`, `Gen:48`, `Studios`, `Creative Partners Program`, `Lumina Builders`, `Affiliate Program`, `Talent Network` | `C-FE-118` |
| `Talent Network` | the `Events & Programs` menu lists `AI Festival`, `AI Summit 2026`, `Gen:48`, `Studios`, `Creative Partners Program`, `Lumina Builders`, `Affiliate Program`, `Talent Network` | `C-FE-118` |
| `Company` | the `Company` menu lists `About Us`, `Careers`, `Safety`, `Brand Guidelines`, `Press`, `Partnerships`, plus a content-credentials destination | `C-FE-119` |
| `About Us` | the `Company` menu lists `About Us`, `Careers`, `Safety`, `Brand Guidelines`, `Press`, `Partnerships`, plus a content-credentials destination | `C-FE-119` |
| `Careers` | the `Company` menu lists `About Us`, `Careers`, `Safety`, `Brand Guidelines`, `Press`, `Partnerships`, plus a content-credentials destination | `C-FE-119` |
| `Safety` | the `Company` menu lists `About Us`, `Careers`, `Safety`, `Brand Guidelines`, `Press`, `Partnerships`, plus a content-credentials destination | `C-FE-119` |
| `Brand Guidelines` | the `Company` menu lists `About Us`, `Careers`, `Safety`, `Brand Guidelines`, `Press`, `Partnerships`, plus a content-credentials destination | `C-FE-119` |
| `Press` | the `Company` menu lists `About Us`, `Careers`, `Safety`, `Brand Guidelines`, `Press`, `Partnerships`, plus a content-credentials destination | `C-FE-119` |
| `Partnerships` | the `Company` menu lists `About Us`, `Careers`, `Safety`, `Brand Guidelines`, `Press`, `Partnerships`, plus a content-credentials destination | `C-FE-119` |
| `(c) 2026 Lumina AI, Inc.` | the footer copyright eyebrow reads `(c) 2026 Lumina AI, Inc.` | `C-FE-129` |
| `Terms of Use` | the footer legal row lists `Terms of Use`, `Privacy Policy`, `California Notices`, `Cookie Settings`, `Code of Conduct`, `System Status` | `C-FE-130` |
| `Privacy Policy` | the footer legal row lists `Terms of Use`, `Privacy Policy`, `California Notices`, `Cookie Settings`, `Code of Conduct`, `System Status` | `C-FE-130` |
| `California Notices` | the footer legal row lists `Terms of Use`, `Privacy Policy`, `California Notices`, `Cookie Settings`, `Code of Conduct`, `System Status` | `C-FE-130` |
| `Cookie Settings` | the footer legal row lists `Terms of Use`, `Privacy Policy`, `California Notices`, `Cookie Settings`, `Code of Conduct`, `System Status` | `C-FE-130` |
| `Code of Conduct` | the footer legal row lists `Terms of Use`, `Privacy Policy`, `California Notices`, `Cookie Settings`, `Code of Conduct`, `System Status` | `C-FE-130` |
| `System Status` | the footer legal row lists `Terms of Use`, `Privacy Policy`, `California Notices`, `Cookie Settings`, `Code of Conduct`, `System Status` | `C-FE-130` |
| `Try now` | the `Lumina Creative` actions read `Try now`, `Learn more`, `For Enterprise` | `C-FE-178` |
| `For Enterprise` | the `Lumina Creative` actions read `Try now`, `Learn more`, `For Enterprise` | `C-FE-178` |
| `View documentation` | the `Lumina Dev` actions read `Get API Key`, `View documentation`, `For Enterprise` | `C-FE-181` |
| `Used by 60m+ creatives around the world. Try free, cancel anytime.` | a caption under the Creative panel reads `Used by 60m+ creatives around the world. Try free, cancel anytime.` | `C-FE-185` |
| `Introducing Lumina Media Router` | the news card `Introducing Lumina Media Router` describes the first preference-optimized router for generative media | `C-FE-190` |
| `How Partner 1 Used Lumina to Produce Their Latest National TV Spot` | the news card `How Partner 1 Used Lumina to Produce Their Latest National TV Spot` describes a broadcast-ready campaign built from photos of real members | `C-FE-191` |
| `Every capability, one integration` | the `Access` column is titled `Every capability, one integration` | `C-FE-201` |
| `Compare before you ship` | the `Evaluate` column is titled `Compare before you ship` | `C-FE-203` |
| `Evaluate models` | the `Evaluate` column action reads `Evaluate models` | `C-FE-204` |
| `Let the platform pick` | the `Automate` column is titled `Let the platform pick` | `C-FE-205` |
| `Set up a Router` | the `Automate` column action reads `Set up a Router` | `C-FE-206` |
| `View usage` | the `Control` column action reads `View usage` | `C-FE-208` |
| `LuminaClient` | the Node sample imports `LuminaClient` from `@lumina/sdk` | `C-FE-216` |
| `@lumina/sdk` | the Node sample imports `LuminaClient` from `@lumina/sdk` | `C-FE-216` |
| `client.textToVideo.create` | the Node sample calls `client.textToVideo.create` with a prompt text | `C-FE-218` |
| `model` | the Node sample passes `model` as `"Nova-4.5"` | `C-FE-219` |
| `"Nova-4.5"` | the Node sample passes `model` as `"Nova-4.5"` | `C-FE-219` |
| `ratio` | the Node sample passes `ratio` as `"1280:720"` | `C-FE-220` |
| `"1280:720"` | the Node sample passes `ratio` as `"1280:720"` | `C-FE-220` |
| `duration` | the Node sample passes `duration` as `5` | `C-FE-221` |
| `5` | the Node sample passes `duration` as `5` | `C-FE-221` |
| `seed` | the Node sample passes `seed` as `692126734` | `C-FE-222` |
| `692126734` | the Node sample passes `seed` as `692126734` | `C-FE-222` |
| `waitForTaskOutput` | the Node sample chains `waitForTaskOutput` onto the create call | `C-FE-223` |
| `Balanced everyday video generation` | the model `Nova-4.5` is tagged `Balanced everyday video generation` | `C-FE-228` |
| `720p` | the model `Nova-4.5` renders at `720p` | `C-FE-229` |
| `Text, Image` | the model `Nova-4.5` accepts inputs `Text, Image` | `C-FE-230` |
| `Up to 10s` | the model `Nova-4.5` runs `Up to 10s` | `C-FE-231` |
| `$0.12/sec` | the model `Nova-4.5` is priced `$0.12/sec` | `C-FE-232` |
| `Precise video editing` | the model `Chisel-2.0` is tagged `Precise video editing` | `C-FE-233` |
| `Matches input` | the model `Chisel-2.0` renders at `Matches input` | `C-FE-234` |
| `Text, Video` | the model `Chisel-2.0` accepts inputs `Text, Video` | `C-FE-235` |
| `$0.18/sec` | the model `Chisel-2.0` is priced `$0.18/sec` | `C-FE-236` |
| `General world simulation` | the model `Worldscape-1` is tagged `General world simulation` | `C-FE-237` |
| `16:9, 1:1` | the model `Worldscape-1` accepts aspect ratios `16:9, 1:1` | `C-FE-239` |
| `$0.30/sec` | the model `Worldscape-1` is priced `$0.30/sec` | `C-FE-240` |
| `Performance capture` | the model `Perform-2` is tagged `Performance capture` | `C-FE-241` |
| `Video` | the model `Perform-2` accepts inputs `Video` | `C-FE-242` |
| `16:9, 9:16, 1:1` | the model `Perform-2` accepts aspect ratios `16:9, 9:16, 1:1` | `C-FE-243` |
| `$0.09/sec` | the model `Perform-2` is priced `$0.09/sec` | `C-FE-244` |
| `Try in Playground` | every model card carries the links `View documentation`, `Try in Playground` | `C-FE-245` |
| `Go to your assistant, Customize` | the first setup step is titled `Go to your assistant, Customize` | `C-FE-252` |
| `Add custom connector` | the second setup step is titled `Add custom connector` | `C-FE-253` |
| `View setup guide` | the third setup step carries a `View setup guide` link | `C-FE-256` |
| `Product marketing` | the showcase row `Product marketing` is titled `Create marketing content from a link` | `C-FE-260` |
| `Create marketing content from a link` | the showcase row `Product marketing` is titled `Create marketing content from a link` | `C-FE-260` |
| `Multi-shot storytelling` | the showcase row `Multi-shot storytelling` is titled `Make dialogue-driven ads` | `C-FE-262` |
| `Make dialogue-driven ads` | the showcase row `Multi-shot storytelling` is titled `Make dialogue-driven ads` | `C-FE-262` |
| `Product sites` | the showcase row `Product sites` is titled `Add stunning product imagery to your site` | `C-FE-264` |
| `Add stunning product imagery to your site` | the showcase row `Product sites` is titled `Add stunning product imagery to your site` | `C-FE-264` |
| `Product URL to marketing video` | the four prompt cards are labelled `Product URL to marketing video`, `Creative Product ad`, `Image to product ad`, `Product image to dialogue ad` | `C-FE-268` |
| `Creative Product ad` | the four prompt cards are labelled `Product URL to marketing video`, `Creative Product ad`, `Image to product ad`, `Product image to dialogue ad` | `C-FE-268` |
| `Image to product ad` | the four prompt cards are labelled `Product URL to marketing video`, `Creative Product ad`, `Image to product ad`, `Product image to dialogue ad` | `C-FE-268` |
| `Product image to dialogue ad` | the four prompt cards are labelled `Product URL to marketing video`, `Creative Product ad`, `Image to product ad`, `Product image to dialogue ad` | `C-FE-268` |
| `What agents can connect to Lumina Connector?` | the accordion row `What agents can connect to Lumina Connector?` answers with web apps, desktop apps, coding tools, connector-protocol apps | `C-FE-269` |
| `Which models can agents use?` | the accordion row `Which models can agents use?` answers that an agent uses models like `Nova-4.5` plus partner models by plan | `C-FE-270` |
| `How are connector generations billed?` | the accordion row `How are connector generations billed?` answers that generations use Lumina credits | `C-FE-271` |
| `Is an API key required?` | the accordion row `Is an API key required?` answers no, so the connector link plus a sign-in suffices | `C-FE-272` |
| `Pause` | the pause control announces `Pause` | `C-FE-302` |
| `Unmute` | the mute control announces `Unmute` once muted | `C-FE-303` |
| `(opens in new tab)` | a link opening a new tab carries `(opens in new tab)` in its accessible name | `C-FE-305` |
| `FastAPI` | the back end is `FastAPI` on `Python 3.11+` | `C-TR-15` |
| `Python 3.11+` | the back end is `FastAPI` on `Python 3.11+` | `C-TR-15` |
| `uvicorn` | the back end is served by `uvicorn` | `C-TR-16` |
| `Astro` | the front end is `Astro` with islands | `C-TR-18` |
| `PostgreSQL 16` | the database is `PostgreSQL 16` reached at `DATABASE_URL` | `C-TR-21` |
| `DATABASE_URL` | the database is `PostgreSQL 16` reached at `DATABASE_URL` | `C-TR-21` |
| `DB_URL` | the same connection string arrives as `DB_URL` | `C-TR-22` |
| `minio` | the object store is the S3-compatible `minio` instance reached over its HTTP API | `C-TR-24` |
| `APP_PUBLIC_PORT` | the environment supplies `APP_PUBLIC_PORT`, `APP_PUBLIC_URL` | `C-TR-122` |
| `APP_PUBLIC_URL` | the environment supplies `APP_PUBLIC_PORT`, `APP_PUBLIC_URL` | `C-TR-122` |
| `published` | two of the first author's items are `published` | `C-DM-86` |
| `the-media-router-preview` | one of the first author's items is a draft slugged `the-media-router-preview` | `C-DM-87` |
| `archived` | one of the first author's items is `archived` | `C-DM-88` |
| `partner-campaign-preview` | one further draft slugged `partner-campaign-preview` is owned by `author2@example.com` | `C-DM-89` |
| `4173` | the app is served on the port in `APP_PUBLIC_PORT`, whose value is `4173` | `C-DC-02` |
| `/app/USER_README.md` | the seeded accounts are written to `/app/USER_README.md` with their shared password | `C-DC-18` |
| `.browser_screenshots/` | the directory `.browser_screenshots/` is reserved at the app root, left empty | `C-DC-19` |
| `.downloads/` | the directory `.downloads/` is reserved at the app root, left empty | `C-DC-20` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact shade of every colour role | `C-UX-15` |
| the exact alphas on the translucency ladder | `C-FE-27` |
| the exact easing curves shared across the product | `C-FE-67` |
| the exact duration of the fast state change | `C-UX-93` |
| the exact radius of each softening step | `C-FE-45` |
| the base spacing unit every gap is a multiple of | `C-FE-52` |
| the exact width at which each responsive tier changes | `C-FE-289` |
| the exact upload size ceiling | `C-TR-108` |
| the accepted image types for an upload | `C-TR-107` |
| the stated retention window for a task artifact | `C-CF-320` |
| the stated budget for a first meaningful preview | `C-CF-292` |
| the per-account concurrency limit | `C-CF-303` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 3 | 14 |
| User roles | 3 | 41 |
| Core features | 18 | 357 |
| User flow | 8 | 90 |
| UI and UX notes | 5 | 148 |
| Front-end specification | 9 | 333 |
| Technical requirements | 23 | 168 |
| Data model | 3 | 95 |
| Constraints | 2 | 21 |
| Deployment contract | 15 | 64 |
