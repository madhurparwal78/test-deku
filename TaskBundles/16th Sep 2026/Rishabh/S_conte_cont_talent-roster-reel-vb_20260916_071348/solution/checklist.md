# Checklist: VERITE

Source: instruction.md
Sections present: overview, user roles, core features, user flow, ui and ux notes, front-end specification, technical requirements, data model, constraints, deployment contract
Sections absent: build plan
Items: 280
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` The product publishes a numbered index of delivered films, `001` through `012`. `src: Overview`
- [ ] `C-OV-02` `capability` The product publishes a roster of the directors, photographers the house represents. `src: Overview`
- [ ] `C-OV-03` `capability` The product shows one mail address in the footer of every public route. `src: Overview`
- [ ] `C-OV-04` `role` Only the producer authenticates in order to act on anything. `src: Overview`
- [ ] `C-OV-05` `constraint` The product has no cart, no payment, no search field, no comment, no rating. `src: Overview`
- [ ] `C-OV-06` `constraint` The build ships no binary asset of any kind. `src: Overview`
- [ ] `C-OV-07` `capability` Each generated asset derives from the owning item's own identifier, so a reload reproduces the same field. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` An anonymous reader reads every published work without an account. `src: User roles`
- [ ] `C-RL-02` `role` An anonymous reader is refused every studio route. `src: User roles`
- [ ] `C-RL-03` `role` An anonymous reader is refused the preview route. `src: User roles`
- [ ] `C-RL-04` `role` Signup creates an account whose role is `visitor`. `src: User roles`
- [ ] `C-RL-05` `role` A `visitor` is refused every studio route. `src: User roles`
- [ ] `C-RL-06` `role` A `visitor` is refused every write. `src: User roles`
- [ ] `C-RL-07` `role` A `producer` creates works, talents, attaches media, sets the index order, publishes, unpublishes. `src: User roles`
- [ ] `C-RL-08` `role` A `producer` reads the page-view log. `src: User roles`
- [ ] `C-RL-09` `role` No account with the role `producer` is created through signup. `src: User roles`
- [ ] `C-RL-10` `literal` The seeded account `producer@example.com` holds the role `producer`. `src: User roles table row 1`
- [ ] `C-RL-11` `literal` The seeded account `producer2@example.com` holds the role `producer`. `src: User roles table row 2`
- [ ] `C-RL-12` `literal` The seeded account `visitor@example.com` holds the role `visitor`. `src: User roles table row 3`
- [ ] `C-RL-13` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `capability` An unpublished item is absent from the work index response. `src: Core features rule 1`
- [ ] `C-CF-02` `capability` An unpublished item is absent from the entry cluster. `src: Core features rule 1`
- [ ] `C-CF-03` `capability` An unpublished item is absent from the roster response. `src: Core features rule 1`
- [ ] `C-CF-04` `capability` An unpublished item is absent from the derived discipline set. `src: Core features rule 1`
- [ ] `C-CF-05` `capability` An unpublished work is absent from a neighbouring work's next, previous links. `src: Core features rule 1`
- [ ] `C-CF-06` `capability` A direct public request for an unpublished item's address returns a not-found status. `src: Core features rule 1`
- [ ] `C-CF-07` `constraint` A response for an unpublished item's address reveals nothing about whether such an item exists. `src: Core features rule 1`
- [ ] `C-CF-08` `role` The poster, stills, reel of an unpublished item are refused to everyone who is not a `producer`. `src: Core features rule 1`
- [ ] `C-CF-09` `capability` Publishing an item makes the listing, the address, the media readable in one act. `src: Core features rule 1`
- [ ] `C-CF-10` `capability` Unpublishing an item makes the listing, the address, the media unreachable again. `src: Core features rule 1`
- [ ] `C-CF-11` `literal` The seeded unpublished talent `Odile Marchand` sits at `/talents/odile-marchand`. `src: Core features rule 1`
- [ ] `C-CF-12` `literal` The seeded unpublished work `The Quiet Room` sits at `/works/the-quiet-room`. `src: Core features rule 1`
- [ ] `C-CF-13` `capability` The work index displays each ordinal zero padded to three digits. `src: Core features rule 2`
- [ ] `C-CF-14` `capability` The displayed ordinal is computed over the published works at the moment of reading. `src: Core features rule 2`
- [ ] `C-CF-15` `constraint` No ordinal column is stored as a displayed label. `src: Core features rule 2`
- [ ] `C-CF-16` `capability` Unpublishing a work renumbers the remaining published works with no gap. `src: Core features rule 2`
- [ ] `C-CF-17` `constraint` No duplicate ordinal is ever visible to a reader. `src: Core features rule 2`
- [ ] `C-CF-18` `capability` Reordering in the studio changes the displayed ordinals on the next read. `src: Core features rule 2`
- [ ] `C-CF-19` `capability` The roster's filter list is the distinct disciplines of published talent. `src: Core features rule 3`
- [ ] `C-CF-20` `capability` The roster's filter list is ordered by the first published talent carrying each discipline. `src: Core features rule 3`
- [ ] `C-CF-21` `capability` Publishing a talent whose discipline is new adds a filter control. `src: Core features rule 3`
- [ ] `C-CF-22` `capability` Unpublishing the last talent of a discipline removes that filter control. `src: Core features rule 3`
- [ ] `C-CF-23` `constraint` The roster offers no all state; one discipline is always active. `src: Core features rule 3`
- [ ] `C-CF-24` `capability` Selecting a discipline narrows the roster set without navigating. `src: Core features rule 3`
- [ ] `C-CF-25` `capability` Every poster, still, reel the producer uploads is stored in `minio`. `src: Core features rule 4`
- [ ] `C-CF-26` `literal` A stored object uses the key `items/{item_id}/{sha256_of_bytes}.{ext}`. `src: Core features rule 4`
- [ ] `C-CF-27` `data` Every media row records the intrinsic dimensions of the bytes. `src: Core features rule 4`
- [ ] `C-CF-28` `data` Every media row records a text alternative written by the producer. `src: Core features rule 4`
- [ ] `C-CF-29` `constraint` Publishing an item whose media lacks a text alternative is refused. `src: Core features rule 4`
- [ ] `C-CF-30` `capability` A refusal to publish names which media carries no text alternative. `src: Core features rule 4`
- [ ] `C-CF-31` `constraint` A slug never changes when the owning item's title changes. `src: Core features rule 5`
- [ ] `C-CF-32` `constraint` A slug is unique within its kind. `src: Core features rule 5`
- [ ] `C-CF-33` `capability` A changed slug leaves the old address resolving permanently. `src: Core features rule 5`
- [ ] `C-CF-34` `ui` The entry route reports real load progress at the optical centre, reaching `100%`. `src: Core features rule 6`
- [ ] `C-CF-35` `constraint` The entry counter never reaches completion before the route is ready. `src: Core features rule 6`
- [ ] `C-CF-36` `ui` The entry cluster leaves the four corners empty, the exact centre clear. `src: Core features rule 6`
- [ ] `C-CF-37` `constraint` Entry cluster positions are authored, stable across loads, never scattered at random. `src: Core features rule 6`
- [ ] `C-CF-38` `ui` Every still in the entry cluster is a real link reachable by keyboard. `src: Core features rule 6`
- [ ] `C-CF-39` `ui` A focused entry-cluster still shows a visible caption where the cursor label would sit. `src: Core features rule 6`
- [ ] `C-CF-40` `constraint` The entry route does not scroll at any width. `src: Core features rule 6`
- [ ] `C-CF-41` `constraint` No reel plays on the entry route. `src: Core features rule 6`
- [ ] `C-CF-42` `literal` The work index opens on the line `Quiet decisions, made early, are the ones you notice last.` `src: Core features rule 7`
- [ ] `C-CF-43` `ui` The work index opening line arrives out of focus, then sharpens. `src: Core features rule 7`
- [ ] `C-CF-44` `data` Each work carries its own left, right, centre variant as stored data. `src: Core features rule 7`
- [ ] `C-CF-45` `ui` Each work index caption row places the ordinal at the still's left edge. `src: Core features rule 7`
- [ ] `C-CF-46` `ui` Each work index caption row places the title flush with the still's right edge. `src: Core features rule 7`
- [ ] `C-CF-47` `ui` Every work index still rests fully desaturated, returning to full colour under the cursor. `src: Core features rule 7`
- [ ] `C-CF-48` `constraint` The work index offers no filter, no sort, no category, no year, no pagination, no search. `src: Core features rule 7`
- [ ] `C-CF-49` `capability` A work route shows the title, the ordinal, the credits, the reel, the stills. `src: Core features rule 8`
- [ ] `C-CF-50` `capability` A work route links to the next work by ordinal, wrapping `012` back to `001`. `src: Core features rule 8`
- [ ] `C-CF-51` `capability` A credit naming a published talent links to that talent's route. `src: Core features rule 8`
- [ ] `C-CF-52` `ui` At a wide window the roster shows one talent filling the window without scrolling. `src: Core features rule 9`
- [ ] `C-CF-53` `ui` The roster marks the active discipline with a small square in the left margin. `src: Core features rule 9`
- [ ] `C-CF-54` `ui` The roster set advances one talent at a time by wheel, trackpad, arrow key. `src: Core features rule 9`
- [ ] `C-CF-55` `ui` At a phone width the roster becomes a scroll-driven sequence of one talent per screenful. `src: Core features rule 9`
- [ ] `C-CF-56` `ui` A talent route sets the name at exactly the size the roster sets. `src: Core features rule 10`
- [ ] `C-CF-57` `capability` A talent route lists the works that talent is credited on. `src: Core features rule 10`
- [ ] `C-CF-58` `constraint` A talent route shows the house mail address, never the talent's own. `src: Core features rule 10`
- [ ] `C-CF-59` `constraint` A talent route carries no talent email, no phone number, no direct social link. `src: Core features rule 10`
- [ ] `C-CF-60` `constraint` The about route carries no photograph. `src: Core features rule 11`
- [ ] `C-CF-61` `ui` The about opening figure repeats the house name seven times between two mirrored groups. `src: Core features rule 11`
- [ ] `C-CF-62` `ui` The about body arrives blurred, sharpening as the reader scrolls. `src: Core features rule 11`
- [ ] `C-CF-63` `ui` Scrolling back up the about route re-blurs the body. `src: Core features rule 11`
- [ ] `C-CF-64` `role` The preview route requires a producer session. `src: Core features rule 12`
- [ ] `C-CF-65` `constraint` Without a producer session the preview route renders nothing, revealing nothing about what exists. `src: Core features rule 12`
- [ ] `C-CF-66` `capability` The preview route renders a draft through the same components a published counterpart uses. `src: Core features rule 12`
- [ ] `C-CF-67` `literal` The preview route carries the persistent marker `PREVIEW - NOT PUBLISHED`. `src: Core features rule 12`
- [ ] `C-CF-68` `literal` During a fetch the preview route shows `Loading preview...`. `src: Core features rule 12`
- [ ] `C-CF-69` `constraint` Nothing on the preview route is indexable, nothing is held by a shared cache. `src: Core features rule 12`
- [ ] `C-CF-70` `ui` The studio carries a sidebar listing the two kinds plus the page-view log. `src: Core features rule 13`
- [ ] `C-CF-71` `ui` Each studio list is a grid of cards showing poster, title, publication state. `src: Core features rule 13`
- [ ] `C-CF-72` `ui` Adding an item opens a dedicated route rather than a panel over the list. `src: Core features rule 13`
- [ ] `C-CF-73` `ui` Publishing lands on a confirmation screen naming what became public, at which address. `src: Core features rule 13`
- [ ] `C-CF-74` `capability` The studio works list reorders the public index by moving a card. `src: Core features rule 13`
- [ ] `C-CF-75` `capability` An unresolved address returns a real not-found status. `src: Core features rule 14`
- [ ] `C-CF-76` `literal` The not-found route shows the line `That page is not here.` `src: Core features rule 14`
- [ ] `C-CF-77` `constraint` The not-found route never echoes the requested path back into the page. `src: Core features rule 14`
- [ ] `C-CF-78` `constraint` The not-found route offers no search box, no suggestion list, no sitemap, no illustration. `src: Core features rule 14`
- [ ] `C-CF-79` `capability` Every public page view records one row carrying the route, the time. `src: Core features rule 15`
- [ ] `C-CF-80` `role` Only a `producer` reads the page-view log. `src: Core features rule 15`
- [ ] `C-CF-81` `capability` Every public route emits its own title, description, canonical link, social preview. `src: Core features rule 16`
- [ ] `C-CF-82` `constraint` No two public routes share a title or a description. `src: Core features rule 16`
- [ ] `C-CF-83` `literal` The house description reads exactly as the copy deck sets the sentence beginning `A production house for picture`. `src: Core features rule 16`
- [ ] `C-CF-84` `literal` The roster title uses the suffix form `VERITE - Talents`. `src: Core features rule 16`
- [ ] `C-CF-85` `ui` The generated social card carries the wordmark on the near-black ground, with no photograph. `src: Core features rule 16`
- [ ] `C-CF-86` `ui` Every still carries a text alternative naming the work's title, then the ordinal. `src: Core features rule 17`
- [ ] `C-CF-87` `ui` Every portrait carries a text alternative naming the talent's name, then the discipline. `src: Core features rule 17`
- [ ] `C-CF-88` `ui` The centre mark is hidden from assistive technology, carrying no accessible name. `src: Core features rule 17`
- [ ] `C-CF-89` `literal` The wordmark's accessible name reads `VERITE, home`. `src: Core features rule 17`
- [ ] `C-CF-90` `ui` Every route carries exactly one top-level heading. `src: Core features rule 17`
- [ ] `C-CF-91` `ui` An inactive discipline control reaches a contrast ratio of `4.5:1` against the ground. `src: Core features rule 18`
- [ ] `C-CF-92` `constraint` The dimmed label tone is never used for text a reader must read. `src: Core features rule 18`
- [ ] `C-CF-93` `constraint` Neither blended element is the only carrier of any piece of information. `src: Core features rule 18`

## C-UF User flow

- [ ] `C-UF-01` `capability` The address `/works` resolves to the work index. `src: User flow table row 2`
- [ ] `C-UF-02` `capability` The address `/talents` resolves to the roster. `src: User flow table row 4`
- [ ] `C-UF-03` `capability` The address `/about` resolves to the manifesto route. `src: User flow table row 6`
- [ ] `C-UF-04` `capability` The address `/login` resolves to the producer sign-in. `src: User flow table row 8`
- [ ] `C-UF-05` `capability` The address `/studio` resolves to the sidebar with the two lists. `src: User flow table row 9`
- [ ] `C-UF-06` `capability` The address `/studio/page-views` resolves to the page-view log. `src: User flow table row 12`
- [ ] `C-UF-07` `capability` The trailing-slash form of each collection root resolves to the same surface with no redirect flash. `src: User flow`
- [ ] `C-UF-08` `constraint` The fourth top-bar item opens a mail composition rather than resolving to a route. `src: User flow`
- [ ] `C-UF-09` `constraint` The fourth top-bar item carries no active state, never marked as the current route. `src: User flow`
- [ ] `C-UF-10` `literal` The mail composition addresses `prod@verite.example.com`. `src: User flow`
- [ ] `C-UF-11` `capability` A credit reading Director, Rives leads to `/talents/rives`. `src: User flow`
- [ ] `C-UF-12` `capability` A producer creating a talent at `/studio/talents/new` creates one that is unpublished. `src: User flow`
- [ ] `C-UF-13` `capability` A signed-out reader requesting an unpublished talent's address receives the site's own not-found route. `src: User flow`
- [ ] `C-UF-14` `capability` A `visitor` attempting to publish an item over the API is refused, with nothing written. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Every hover resolves to exactly one change, from full strength to half. `src: UI/UX notes`
- [ ] `C-UX-02` `constraint` No hover adds a lift, a scale, a shadow, an underline, a colour shift. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The inactive discipline control moves toward full strength under the cursor. `src: UI/UX notes`
- [ ] `C-UX-04` `constraint` No keyframe animation exists anywhere in the build. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` The build uses exactly two durations, one fast, one slow. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` The slow duration carries exactly two effects, the about blur, the index desaturation. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Three movement curves exist, no more. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` On navigation the persistent frame fades as one thing rather than as a stagger. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` The cursor marker stays visible throughout a route transition. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` One breakpoint separates the wide layout from the narrow layout. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` Below the breakpoint the wordmark, the top bar retract on scroll, then return. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` On a touch device work index stills render in full colour. `src: UI/UX notes`
- [ ] `C-UX-13` `constraint` On a pointer-coarse device the cursor marker is absent. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` Focus is visible on every interactive element, never the same treatment as hover. `src: UI/UX notes`
- [ ] `C-UX-15` `ui` A skip link is the first focusable element. `src: UI/UX notes`
- [ ] `C-UX-16` `ui` The discipline controls are real buttons exposing a selected state. `src: UI/UX notes`
- [ ] `C-UX-17` `ui` A letter-split label exposes the whole word as the accessible name. `src: UI/UX notes`
- [ ] `C-UX-18` `constraint` Smoothed scrolling never intercepts keyboard scrolling, anchor navigation, find-in-page. `src: UI/UX notes`
- [ ] `C-UX-19` `ui` Under a reduced-motion preference the about text resolves to sharp. `src: UI/UX notes`
- [ ] `C-UX-20` `ui` Under a reduced-motion preference no reel plays, leaving the still with a control. `src: UI/UX notes`
- [ ] `C-UX-21` `ui` Under a reduced-motion preference the desaturation still applies, nearly instantly. `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The entry route's ground is a near-black neutral warmed toward red. `src: Front-end specification`
- [ ] `C-FE-02` `ui` Every other route's ground is a near-white neutral warmed toward green. `src: Front-end specification`
- [ ] `C-FE-03` `constraint` No colour outside the two grounds plus the four supporting tones appears in the build. `src: Front-end specification`
- [ ] `C-FE-04` `constraint` The framework error page's four colours appear nowhere in the build. `src: Front-end specification`
- [ ] `C-FE-05` `constraint` The colour-scheme preference query is not part of the build. `src: Front-end specification`
- [ ] `C-FE-06` `constraint` The unplaced supporting tone is not shipped. `src: Front-end specification`
- [ ] `C-FE-07` `ui` One serif display family, one grotesque interface family, both variable. `src: Front-end specification`
- [ ] `C-FE-08` `ui` Both families load with `swap`, with a serif display fallback, a non-serif interface fallback. `src: Front-end specification`
- [ ] `C-FE-09` `literal` Interface text is set at `12px` with a line height of `14.4px`. `src: Front-end specification`
- [ ] `C-FE-10` `ui` Hierarchy comes from position, from the display face, never from resizing the interface face. `src: Front-end specification`
- [ ] `C-FE-11` `ui` The variable axis value falls as the type size rises. `src: Front-end specification`
- [ ] `C-FE-12` `constraint` No type size exists between `24px`, `36px`, exclusive of both. `src: Front-end specification`
- [ ] `C-FE-13` `literal` A talent's name is set at `125px`. `src: Front-end specification`
- [ ] `C-FE-14` `ui` Every interface-face string renders in capitals. `src: Front-end specification`
- [ ] `C-FE-15` `ui` Talent names, work titles are the only display-face strings in title case. `src: Front-end specification`
- [ ] `C-FE-16` `ui` Eight elements mount once, surviving every navigation without remounting. `src: Front-end specification`
- [ ] `C-FE-17` `constraint` The persistent frame is never a child of the route outlet. `src: Front-end specification`
- [ ] `C-FE-18` `ui` The wordmark composites by difference rather than being painted in a fixed colour. `src: Front-end specification`
- [ ] `C-FE-19` `ui` The top bar centres one item in the window, grouping the other three at the right. `src: Front-end specification`
- [ ] `C-FE-20` `ui` The centre mark changes with the route, holding one height across all four variants. `src: Front-end specification`
- [ ] `C-FE-21` `ui` The cursor pair parks off the top left when inactive rather than hiding. `src: Front-end specification`
- [ ] `C-FE-22` `ui` The cursor pair follows the pointer with a frame-rate independent lag. `src: Front-end specification`
- [ ] `C-FE-23` `ui` The studio credit stays legible on the near-black entry route. `src: Front-end specification`
- [ ] `C-FE-24` `literal` The footer's third column sets `WORK WITH US` over the house mail address. `src: Front-end specification`
- [ ] `C-FE-25` `ui` A scrim behind the footer keeps the footer's capitals legible over whatever sits behind. `src: Front-end specification`
- [ ] `C-FE-26` `ui` The counter well serves the entry route, plus the roster at a phone width. `src: Front-end specification`
- [ ] `C-FE-27` `ui` The contact overlay traps focus for as long as the panel stays open. `src: Front-end specification`
- [ ] `C-FE-28` `ui` The contact overlay closes on the escape key. `src: Front-end specification`
- [ ] `C-FE-29` `ui` Marks are sized by height, never by width. `src: Front-end specification`
- [ ] `C-FE-30` `ui` The centre mark sits at half the window height minus a small optical correction. `src: Front-end specification`
- [ ] `C-FE-31` `constraint` No icon font, no sprite sheet, no image-based icon appears anywhere. `src: Front-end specification`
- [ ] `C-FE-32` `ui` One scroll-position source feeds every scrubbed property. `src: Front-end specification`
- [ ] `C-FE-33` `ui` The scroll source writes a class to the document root for the duration of an in-flight scroll. `src: Front-end specification`
- [ ] `C-FE-34` `ui` A reduced-motion preference resolves every registered effect to the end state. `src: Front-end specification`
- [ ] `C-FE-35` `ui` The footer travels up into place over the last third of both long routes. `src: Front-end specification`
- [ ] `C-FE-36` `capability` With the rendering layer unavailable every work stays reachable, captioned. `src: Front-end specification`
- [ ] `C-FE-37` `capability` With the rendering layer unavailable every talent stays reachable, labelled. `src: Front-end specification`
- [ ] `C-FE-38` `ui` Media reveals are wipes from the bottom edge, never fades, never scales. `src: Front-end specification`
- [ ] `C-FE-39` `ui` Stills are overscaled slightly inside their clip, with that scale never animated. `src: Front-end specification`
- [ ] `C-FE-40` `ui` A reel plays muted, looping, without controls, only during the period of being in view. `src: Front-end specification`
- [ ] `C-FE-41` `constraint` A still stays visible before the reel is ready, never replaced by a blank frame. `src: Front-end specification`
- [ ] `C-FE-42` `literal` The navigation carries `WORKS`, `TALENTS`, `CONTACT`, `ABOUT`. `src: Front-end specification`
- [ ] `C-FE-43` `literal` The footer premises line reads `9 PASSAGE BELLEVUE` over `PARIS`. `src: Front-end specification`
- [ ] `C-FE-44` `literal` The two-line house line reads `FOR PICTURE` over `AND ITS MAKERS`. `src: Front-end specification`
- [ ] `C-FE-45` `literal` The filter labels read `DIRECTOR`, `PHOTOGRAPHER`. `src: Front-end specification`
- [ ] `C-FE-46` `literal` The skip link's accessible name reads `Skip to content`. `src: Front-end specification`
- [ ] `C-FE-47` `ui` The about opening figure is symmetrical about its horizontal midline. `src: Front-end specification`
- [ ] `C-FE-48` `ui` The about first paragraph keeps its seven authored line breaks at a wide window. `src: Front-end specification`
- [ ] `C-FE-49` `ui` The about closing lockup nests small words into the negative space beside large ones. `src: Front-end specification`
- [ ] `C-FE-50` `ui` Each generated still is a seeded gradient field carrying real colour, with grain over. `src: Front-end specification`
- [ ] `C-FE-51` `constraint` A generated still draws no text, no dimension label, no diagonal cross. `src: Front-end specification`
- [ ] `C-FE-52` `ui` Each generated reel drifts along one axis, with grain redrawn each frame. `src: Front-end specification`
- [ ] `C-FE-53` `ui` The grain is one tiling field generated once, then reused. `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The server returns complete markup on first paint for every route. `src: Technical requirements`
- [ ] `C-TR-02` `contract` The front end is built with `Alpine.js` over server-rendered templates. `src: Technical requirements`
- [ ] `C-TR-03` `contract` The backend, plus the HTTP API, is built with `Flask`, `Jinja`. `src: Technical requirements`
- [ ] `C-TR-04` `contract` Data is stored in `PostgreSQL`, reached at `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-05` `contract` Uploaded bytes are stored in `minio`, reached at `STORAGE_ENDPOINT`. `src: Technical requirements`
- [ ] `C-TR-06` `literal` The object store bucket is named by `STORAGE_BUCKET`. `src: Technical requirements`
- [ ] `C-TR-07` `literal` The object store credentials are `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`. `src: Technical requirements`
- [ ] `C-TR-08` `contract` Authentication uses email, password, bearer tokens, hashed passwords. `src: Technical requirements`
- [ ] `C-TR-09` `contract` One line per request is logged to stdout. `src: Technical requirements`
- [ ] `C-TR-10` `capability` A route reached without scripting still lists every published work with the ordinal, the caption. `src: Technical requirements`
- [ ] `C-TR-11` `capability` A route reached without scripting still lists every published talent with the discipline. `src: Technical requirements`
- [ ] `C-TR-12` `constraint` No second database, cache, queue, object store, identity provider, mail vendor is introduced. `src: Technical requirements`
- [ ] `C-TR-13` `contract` Every host, port, credential is read from the environment, never hardcoded. `src: Technical requirements`
- [ ] `C-TR-14` `capability` No reel has a source until the owning still is within one window height of the viewport. `src: Technical requirements`
- [ ] `C-TR-15` `capability` A reel more than one window height outside the viewport is paused, with the buffer released. `src: Technical requirements`
- [ ] `C-TR-16` `constraint` No more than two reels play at once. `src: Technical requirements`
- [ ] `C-TR-17` `capability` A save-data hint, a metered connection, a reduced-motion preference suppresses reels. `src: Technical requirements`
- [ ] `C-TR-18` `constraint` A compositing hint is added when an effect starts, removed when the effect ends. `src: Technical requirements`
- [ ] `C-TR-19` `constraint` Nothing animates a property that triggers layout. `src: Technical requirements`
- [ ] `C-TR-20` `constraint` No blanket transition watches every animatable property for change. `src: Technical requirements`
- [ ] `C-TR-21` `capability` Every media reference carries intrinsic dimensions so a tile reserves space before arrival. `src: Technical requirements`
- [ ] `C-TR-22` `capability` Both font families are preloaded, subset to the characters actually used. `src: Technical requirements`
- [ ] `C-TR-23` `capability` The entry counter reports real progress against the fonts, the frame, the cluster stills. `src: Technical requirements`
- [ ] `C-TR-24` `capability` The social preview declares the type, the route's own address, a title, a description, a resolving image. `src: Technical requirements`
- [ ] `C-TR-25` `constraint` No document, script, stylesheet, source map the browser fetches carries a credential. `src: Technical requirements`
- [ ] `C-TR-26` `capability` Every response carries a content-type options header refusing to sniff. `src: Technical requirements`
- [ ] `C-TR-27` `capability` Every response carries a frame-ancestors restriction, a referrer policy, a content security policy. `src: Technical requirements`
- [ ] `C-TR-28` `capability` A preview response forbids storage by a shared cache, forbids indexing. `src: Technical requirements`
- [ ] `C-TR-29` `constraint` No external network call is made at run time. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` The schema holds six tables, with every timestamp in UTC. `src: Data model`
- [ ] `C-DM-02` `data` An account row holds an id, an email, a password hash, a role, a creation time. `src: Data model`
- [ ] `C-DM-03` `data` An account email is unique, compared without regard to case. `src: Data model`
- [ ] `C-DM-04` `data` An item row holds a kind that is one of `work` or `talent`. `src: Data model`
- [ ] `C-DM-05` `data` An item id is stable, opaque, never derived from the title. `src: Data model`
- [ ] `C-DM-06` `data` An item holds a sort key for works, a discipline for talents. `src: Data model`
- [ ] `C-DM-07` `data` An item holds a variant that is one of `left`, `right`, `centre`. `src: Data model`
- [ ] `C-DM-08` `data` An item holds a published flag plus a published time that stays null until publication. `src: Data model`
- [ ] `C-DM-09` `constraint` No ordinal column exists on the item table. `src: Data model`
- [ ] `C-DM-10` `data` A media row holds a role that is one of `poster`, `still`, `reel`. `src: Data model`
- [ ] `C-DM-11` `data` A media row holds a unique object key, a content type, a byte size, a digest. `src: Data model`
- [ ] `C-DM-12` `data` A media row holds intrinsic width, intrinsic height, neither ever null. `src: Data model`
- [ ] `C-DM-13` `data` An item carries exactly one `poster`, at most one `reel`. `src: Data model`
- [ ] `C-DM-14` `data` A credit row holds a role, a name, an optional talent reference, a position. `src: Data model`
- [ ] `C-DM-15` `data` A talent's selected work is derived by reading credits, never stored on the talent. `src: Data model`
- [ ] `C-DM-16` `data` A slug redirect row holds a kind, an old slug unique within kind, the item now pointed at. `src: Data model`
- [ ] `C-DM-17` `data` A page-view row holds the public route viewed, plus the time of the view. `src: Data model`
- [ ] `C-DM-18` `constraint` An object key is unique, so two uploads of identical bytes resolve to one object. `src: Data model`
- [ ] `C-DM-19` `data` The seed publishes twelve works with sort keys in the stated order. `src: Data model`
- [ ] `C-DM-20` `literal` The seed publishes the talents `Rives`, `Halcyon`, `Camille Ferrand`. `src: Data model`
- [ ] `C-DM-21` `data` Every seeded item carries a poster with a text alternative. `src: Data model`
- [ ] `C-DM-22` `data` Every seeded work carries at least one credit referring to a published talent. `src: Data model`
- [ ] `C-DM-23` `constraint` No page view is seeded. `src: Data model`
- [ ] `C-DM-24` `constraint` Seeding is idempotent, so restarting the app duplicates no row. `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product holds one house, with no organisation, no team, no workspace, no second tenant. `src: Constraints`
- [ ] `C-CN-02` `constraint` The product builds no contact form of any kind. `src: Constraints`
- [ ] `C-CN-03` `constraint` The product takes no money, offering no cart, no pricing, no subscription. `src: Constraints`
- [ ] `C-CN-04` `constraint` The product carries no blog, no news, no comment, no like, no rating, no messaging. `src: Constraints`
- [ ] `C-CN-05` `constraint` No represented talent's email, phone number, direct social link appears on any route. `src: Constraints`
- [ ] `C-CN-06` `constraint` The product offers no language switch, no second locale. `src: Constraints`
- [ ] `C-CN-07` `constraint` The product uses no third-party analytics. `src: Constraints`
- [ ] `C-CN-08` `constraint` Every still, reel, mark, grain tile, social card is generated rather than shipped. `src: Constraints`
- [ ] `C-CN-09` `constraint` The two substituted typefaces each carry a continuous variable axis. `src: Constraints`
- [ ] `C-CN-10` `capability` The product stays responsive with the seeded content plus a few thousand page-view rows. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-04` `literal` The route `GET /api/health` returns `200` once the app is ready. `src: Deployment contract`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-06` `literal` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-07` `literal` Empty `.browser_screenshots/`, `.downloads/` directories exist at the app root. `src: Deployment contract`
- [ ] `C-DC-08` `contract` A production build is served behind a static or preview server, never a dev server. `src: Deployment contract`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends, never a child of the shell. `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server binds `0.0.0.0`, never a loopback address. `src: Deployment contract`
- [ ] `C-DC-11` `constraint` No backing service named in the brief is downloaded, installed, compiled, started. `src: Deployment contract`
- [ ] `C-DC-12` `constraint` No edge function is used. `src: Deployment contract`
- [ ] `C-DC-13` `constraint` No persistent volume, no fixed container name, no custom network is declared. `src: Deployment contract`
- [ ] `C-DC-14` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract`
- [ ] `C-DC-15` `contract` An invalid or unauthorized call is rejected as a client error, never as a server error. `src: Deployment contract`
- [ ] `C-DC-16` `constraint` An in-memory buffer, a container filesystem file, a base64 column is not the object store. `src: Deployment contract`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `producer@example.com` | seeded producer account | C-RL-10 | User roles table row 1 |
| `producer` | the writing role | C-RL-10 | User roles table row 1 |
| `producer2@example.com` | second seeded producer account | C-RL-11 | User roles table row 2 |
| `visitor@example.com` | seeded visitor account | C-RL-12 | User roles table row 3 |
| `visitor` | the non-writing role | C-RL-12 | User roles table row 3 |
| `deku-demo-pw-2026` | password for every seeded account | C-RL-13 | User roles |
| `Odile Marchand` | seeded unpublished talent | C-CF-11 | Core features rule 1 |
| `/talents/odile-marchand` | address of the seeded unpublished talent | C-CF-11 | Core features rule 1 |
| `The Quiet Room` | seeded unpublished work | C-CF-12 | Core features rule 1 |
| `/works/the-quiet-room` | address of the seeded unpublished work | C-CF-12 | Core features rule 1 |
| `items/{item_id}/{sha256_of_bytes}.{ext}` | object key scheme | C-CF-26 | Core features rule 4 |
| `Quiet decisions, made early, are the ones you notice last.` | the work index opening line | C-CF-42 | Core features rule 7 |
| `PREVIEW - NOT PUBLISHED` | the preview marker | C-CF-67 | Core features rule 12 |
| `Loading preview...` | the preview waiting copy | C-CF-68 | Core features rule 12 |
| `That page is not here.` | the not-found line | C-CF-76 | Core features rule 14 |
| `A production house for picture` | a value the brief pins | C-CF-83 | Core features rule 16 |
| `VERITE - Talents` | the roster title | C-CF-84 | Core features rule 16 |
| `VERITE, home` | the wordmark accessible name | C-CF-89 | Core features rule 17 |
| `prod@verite.example.com` | the house mail address | C-UF-10 | User flow |
| `12px` | the single interface type size | C-FE-09 | Front-end specification |
| `14.4px` | the interface line height | C-FE-09 | Front-end specification |
| `125px` | the talent name size | C-FE-13 | Front-end specification |
| `WORK WITH US` | the footer contact label | C-FE-24 | Front-end specification |
| `WORKS` | first navigation item | C-FE-42 | Front-end specification |
| `TALENTS` | second navigation item | C-FE-42 | Front-end specification |
| `CONTACT` | third navigation item | C-FE-42 | Front-end specification |
| `ABOUT` | fourth navigation item | C-FE-42 | Front-end specification |
| `9 PASSAGE BELLEVUE` | the footer street line | C-FE-43 | Front-end specification |
| `PARIS` | the footer city line | C-FE-43 | Front-end specification |
| `FOR PICTURE` | first line of the house line | C-FE-44 | Front-end specification |
| `AND ITS MAKERS` | second line of the house line | C-FE-44 | Front-end specification |
| `DIRECTOR` | first filter label | C-FE-45 | Front-end specification |
| `PHOTOGRAPHER` | second filter label | C-FE-45 | Front-end specification |
| `Skip to content` | the skip link accessible name | C-FE-46 | Front-end specification |
| `STORAGE_BUCKET` | the bucket variable | C-TR-06 | Technical requirements |
| `STORAGE_ACCESS_KEY` | the object store key | C-TR-07 | Technical requirements |
| `STORAGE_SECRET_KEY` | the object store secret | C-TR-07 | Technical requirements |
| `Rives` | seeded talent | C-DM-20 | Data model |
| `Halcyon` | seeded talent | C-DM-20 | Data model |
| `Camille Ferrand` | seeded talent | C-DM-20 | Data model |
| `${APP_PUBLIC_PORT}:4173` | the port mapping | C-DC-02 | Deployment contract |
| `GET /api/health` | the health route | C-DC-04 | Deployment contract |
| `200` | the health status | C-DC-04 | Deployment contract |
| `/app/USER_README.md` | where logins are written | C-DC-06 | Deployment contract |
| `.browser_screenshots/` | reserved directory | C-DC-07 | Deployment contract |
| `.downloads/` | reserved directory | C-DC-07 | Deployment contract |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the one breakpoint separating the wide layout from the narrow one | C-UX-10 | named as a single boundary with no value given, under the brief's own rule that a breakpoint is carried as an arrangement rather than as a measurement |
| the fast duration and the slow duration | C-UX-05 | named as two durations that must feel different, with neither value given |
| the overscale applied to a still inside its clip | C-FE-39 | described as slight, with no factor given |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 3 | 7 |
| User roles | 0 | 13 |
| Core features | 11 | 93 |
| User flow | 2 | 14 |
| UI and UX notes | 5 | 21 |
| Front-end specification | 19 | 53 |
| Technical requirements | 9 | 29 |
| Data model | 5 | 24 |
| Constraints | 4 | 10 |
| Deployment contract | 9 | 16 |

