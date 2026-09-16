# Checklist: Draftline

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 256
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The app runs in a browser with no install step for the user. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app draws a drawing at true real-world scale on an infinite canvas. `src: Overview para 1`
- [ ] `C-OV-03` `role` The app gives a drafter ownership of a drawing. `src: Overview para 2`
- [ ] `C-OV-04` `role` The app gives a reviewer read access to a drawing shared with the reviewer. `src: Overview para 2`
- [ ] `C-OV-05` `ui` The app presents one full-screen workspace after sign-in. `src: Overview para 3`
- [ ] `C-OV-06` `ui` The app moves between workspace surfaces without loading a new page. `src: Overview para 3`
- [ ] `C-OV-07` `capability` The app keeps a drawing internally consistent under concurrent editing. `src: Overview para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` The app lets a drafter create a drawing. `src: User roles table row 1`
- [ ] `C-RL-02` `role` The app lets a drafter edit geometry on a drawing the drafter owns. `src: User roles table row 1`
- [ ] `C-RL-03` `role` The app lets the owner of a drawing invite a collaborator. `src: User roles table row 1`
- [ ] `C-RL-04` `constraint` The app denies a drafter every read of a drawing the drafter neither owns nor was shared into. `src: User roles table row 1`
- [ ] `C-RL-05` `constraint` The app denies a non-owner every change to another owner's share list. `src: User roles table row 1`
- [ ] `C-RL-06` `role` The app lets a reviewer open a drawing shared with the reviewer. `src: User roles table row 2`
- [ ] `C-RL-07` `role` The app lets a reviewer comment on a drawing shared at comment. `src: User roles table row 2`
- [ ] `C-RL-08` `constraint` The app denies a reviewer the creation of a drawing. `src: User roles table row 2`
- [ ] `C-RL-09` `constraint` The app denies a reviewer every entity write under every share access. `src: User roles table row 2`
- [ ] `C-RL-10` `contract` The app enforces authorization on the server for every mutating endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-11` `constraint` The app leaves the protected row unchanged after denying an unauthorized request. `src: User roles, authorization paragraph`
- [ ] `C-RL-12` `capability` The app opens signup to anyone. `src: User roles, signup paragraph`
- [ ] `C-RL-13` `literal` The app assigns the role drafter to every account created at signup. `src: User roles, signup paragraph`
- [ ] `C-RL-14` `literal` The app seeds an account at drafter@example.com named Mira Vance. `src: User roles, seeded accounts table`
- [ ] `C-RL-15` `literal` The app seeds an account at drafter2@example.com named Owen Blake. `src: User roles, seeded accounts table`
- [ ] `C-RL-16` `literal` The app seeds an account at reviewer@example.com named Priya Raman. `src: User roles, seeded accounts table`

## C-CF Core features

- [ ] `C-CF-01` `literal` The app accepts deku-demo-pw-2026 at login for every seeded account. `src: Core features, Auth`
- [ ] `C-CF-02` `contract` The app stores a password hashed. `src: Core features, Auth`
- [ ] `C-CF-03` `constraint` The app returns no password hash from any endpoint. `src: Core features, Auth`
- [ ] `C-CF-04` `contract` The app returns a bearer token on a successful login. `src: Core features, Auth`
- [ ] `C-CF-05` `literal` The app expires a bearer token after 24 hours. `src: Core features, Auth`
- [ ] `C-CF-06` `constraint` The app rejects a signup whose email already has an account. `src: Core features, Auth rule 1`
- [ ] `C-CF-07` `constraint` The app writes no second account row for a rejected signup. `src: Core features, Auth rule 1`
- [ ] `C-CF-08` `constraint` The app rejects a request carrying no bearer token on every protected route. `src: Core features, Auth rule 3`
- [ ] `C-CF-09` `constraint` The app rejects a request carrying an expired bearer token. `src: Core features, Auth rule 3`
- [ ] `C-CF-10` `capability` The app lists every reachable drawing newest first in the library. `src: Core features, drawing library`
- [ ] `C-CF-11` `ui` The app shows a drawing's name, units, current version number, owner on its library card. `src: Core features, drawing library`
- [ ] `C-CF-12` `constraint` The app omits an unreachable drawing from the library listing. `src: Core features rule 4`
- [ ] `C-CF-13` `ui` The app shows an empty-library message offering the first creation step. `src: Core features rule 5`
- [ ] `C-CF-14` `literal` The app creates a drawing across the three named creation addresses, choosing a template from blank, architectural, mechanical, units from millimeters, meters, inches, feet. `src: Core features, drawing library`
- [ ] `C-CF-15` `constraint` The app returns a visitor jumping ahead to the first unanswered creation step. `src: Core features, drawing library`
- [ ] `C-CF-16` `literal` The app opens an architectural drawing with the layers Base, Walls, Dimensions, Notes. `src: Core features rule 6`
- [ ] `C-CF-17` `constraint` The app writes no drawing row for a reviewer's direct create call. `src: Core features rule 7`
- [ ] `C-CF-18` `capability` The app pans, zooms about the cursor, zooms to a window, zooms to extents, zooms to previous, regenerates the drawing view. `src: Core features rule 8`
- [ ] `C-CF-19` `data` The app renders an entity with its own linetype, lineweight, draw order. `src: Core features rule 9`
- [ ] `C-CF-20` `data` The app takes an unset entity colour from the entity's layer. `src: Core features rule 9`
- [ ] `C-CF-21` `data` The app returns a coordinate entered at a fraction of a millimetre or kilometres from the origin unchanged. `src: Core features rule 10`
- [ ] `C-CF-22` `literal` The app stays interactive with 20000 entities across 40 layers on one drawing. `src: Core features rule 11`
- [ ] `C-CF-23` `capability` The app presents one paper space layout carrying a viewport onto the model, reached by a status bar tab. `src: Core features rule 12`
- [ ] `C-CF-24` `capability` The app marks the geometrically nearest meaningful point for the active object snap set before the click lands. `src: Core features rule 13`
- [ ] `C-CF-25` `literal` The app provides endpoint, midpoint, centre, node, quadrant, intersection, extension, insertion, perpendicular, tangent, nearest, apparent intersection, parallel snaps. `src: Core features rule 13`
- [ ] `C-CF-26` `capability` The app constrains the pointer under orthogonal mode, polar tracking, object snap tracking. `src: Core features rule 14`
- [ ] `C-CF-27` `capability` The app accepts an absolute, relative, polar or direct-distance typed coordinate, producing the geometry a click at that point produces. `src: Core features rule 15`
- [ ] `C-CF-28` `ui` The app toggles grid, snap, orthogonal mode, polar tracking, object snap, lineweight display from the status bar. `src: Core features rule 16`
- [ ] `C-CF-29` `capability` The app accepts every command by its full name plus by its alias at the command input. `src: Core features rule 17`
- [ ] `C-CF-30` `ui` The app echoes the running command's prompt plus recalls earlier input at the command input. `src: Core features rule 17`
- [ ] `C-CF-31` `capability` The app creates lines, polylines, construction lines, rays, circles, arcs, ellipses, rectangles, polygons, splines, vertices, donuts. `src: Core features rule 18`
- [ ] `C-CF-32` `capability` The app creates hatches, gradient fills, regions, revision clouds, wipeouts. `src: Core features rule 18`
- [ ] `C-CF-33` `capability` The app reshapes a hatch when the hatch boundary is reshaped. `src: Core features rule 19`
- [ ] `C-CF-34` `capability` The app modifies geometry by move, copy, rotate, scale, mirror, offset, array. `src: Core features rule 20`
- [ ] `C-CF-35` `capability` The app trims, extends, fillets, chamfers, blends, stretches, lengthens, breaks, joins, explodes geometry. `src: Core features rule 20`
- [ ] `C-CF-36` `capability` The app places grips on a selected entity, dragging one grip moves that vertex alone. `src: Core features rule 21`
- [ ] `C-CF-37` `capability` The app selects by window, crossing, fence, window polygon, crossing polygon, last, previous, all. `src: Core features rule 22`
- [ ] `C-CF-38` `capability` The app cycles overlapping entities on repeated clicks plus filters a selection by property. `src: Core features rule 22`
- [ ] `C-CF-39` `capability` The app paints a source entity's properties onto other entities. `src: Core features rule 23`
- [ ] `C-CF-40` `constraint` The app refuses every modification from a share at view or comment access. `src: Core features rule 24`
- [ ] `C-CF-41` `capability` The app creates, renames, deletes, reorders a layer from the layer manager. `src: Core features rule 25`
- [ ] `C-CF-42` `data` The app sets a layer's colour index, linetype, lineweight, transparency, plot flag, description. `src: Core features rule 25`
- [ ] `C-CF-43` `capability` The app toggles a layer on, off, frozen, thawed, locked, unlocked. `src: Core features rule 25`
- [ ] `C-CF-44` `constraint` The app rejects a layer name matching an existing layer name under case folding. `src: Core features rule 26`
- [ ] `C-CF-45` `constraint` The app rejects the deletion of a layer still holding entities. `src: Core features rule 27`
- [ ] `C-CF-46` `literal` The app refuses the renaming plus the deletion of the layer named Base. `src: Core features rule 27`
- [ ] `C-CF-47` `capability` The app saves a named layer state for restoring, isolates the layer of a picked entity. `src: Core features rule 28`
- [ ] `C-CF-48` `ui` The app edits the full property set of a selection from the properties panel, showing whether a property is set directly, follows the layer or follows the block. `src: Core features rule 29`
- [ ] `C-CF-49` `capability` The app removes a turned-off layer's entities from the canvas, leaving every entity row intact. `src: Core features rule 30`
- [ ] `C-CF-50` `capability` The app creates single-line plus multi-line text under a named text style, with rich formatting. `src: Core features rule 31`
- [ ] `C-CF-51` `capability` The app creates linear, aligned, angular, radius, diameter, arc length, ordinate, baseline, continued dimensions, plus multileaders, centre marks, centrelines. `src: Core features rule 32`
- [ ] `C-CF-52` `data` The app recomputes a dimension's stored measurement when the measured entity moves. `src: Core features rule 33`
- [ ] `C-CF-53` `capability` The app saves geometry as a named block definition, inserting the block with a preview. `src: Core features rule 34`
- [ ] `C-CF-54` `capability` The app edits a block attribute plus extracts block attributes into a table. `src: Core features rule 35`
- [ ] `C-CF-55` `capability` The app switches a block instance between its stored visibility states. `src: Core features rule 36`
- [ ] `C-CF-56` `literal` The app writes a saved version as a UTF-8 drawing exchange document whose lines open on DRAWING, carry one LAYER line per layer, one ENTITY line per entity, then close on END. `src: Core features, versions in the cloud object store`
- [ ] `C-CF-57` `literal` The app stores version bytes in the bucket at drawings/{drawing_id}/v{version_number}/{byte_digest}.dxe. `src: Core features rule 37`
- [ ] `C-CF-58` `data` The app records the lowercase hex SHA-256 digest, the author, the time, the entity count on a version row. `src: Core features rule 37`
- [ ] `C-CF-59` `data` The app numbers versions from 1 upward in steps of exactly one with no gap. `src: Core features rule 38`
- [ ] `C-CF-60` `data` The app accepts exactly one of two saves naming the same starting version. `src: Core features rule 39`
- [ ] `C-CF-61` `ui` The app names the version that now exists when refusing the losing save. `src: Core features rule 39`
- [ ] `C-CF-62` `constraint` The app writes no version row plus no bucket object for a refused save. `src: Core features rule 39`
- [ ] `C-CF-63` `constraint` The app never rewrites a version row once the version is written. `src: Core features rule 40`
- [ ] `C-CF-64` `capability` The app writes a new highest version when restoring an earlier version. `src: Core features rule 40`
- [ ] `C-CF-65` `capability` The app captures unsaved work automatically plus offers the autosave back for recovery when the drawing reopens. `src: Core features rule 41`
- [ ] `C-CF-66` `ui` The app lists versions newest first with number, author, time, label. `src: Core features rule 42`
- [ ] `C-CF-67` `data` The app returns the exact stored bytes on a version download. `src: Core features rule 42`
- [ ] `C-CF-68` `capability` The app marks geometry added, removed, changed between two compared versions. `src: Core features rule 43`
- [ ] `C-CF-69` `capability` The app invites an account by email at view, comment or edit from the share page, letting the owner remove that access again. `src: Core features rule 44`
- [ ] `C-CF-70` `constraint` The app rejects an invitation to an email carrying no account. `src: Core features rule 44`
- [ ] `C-CF-71` `constraint` The app changes an existing collaborator's access rather than adding a second invitation. `src: Core features rule 44`
- [ ] `C-CF-72` `capability` The app shows a shared drawing in the invitee's library immediately. `src: Core features rule 45`
- [ ] `C-CF-73` `capability` The app names every account currently in a drawing, dropping a departed account within two minutes. `src: Core features rule 46`
- [ ] `C-CF-74` `ui` The app gives each present account a distinct colour on the presence strip. `src: Core features rule 46`
- [ ] `C-CF-75` `capability` The app shows one editor's saved change in another editor's open workspace without a reload. `src: Core features rule 47`
- [ ] `C-CF-76` `constraint` The app preserves the second editor's pan, zoom, current layer, selection across another editor's change. `src: Core features rule 47`
- [ ] `C-CF-77` `constraint` The app refuses the deletion of a block definition still carrying instances. `src: Core features rule 48`
- [ ] `C-CF-78` `capability` The app pins a comment to a point on the drawing plus opens a thread carrying replies plus a resolved state. `src: Core features rule 49`
- [ ] `C-CF-79` `constraint` The app rejects a comment carrying an empty body plus writes no comment row. `src: Core features rule 49`
- [ ] `C-CF-80` `constraint` The app denies a reviewer at view access every comment write. `src: Core features rule 50`
- [ ] `C-CF-81` `constraint` The app denies every account other than the owner any read of a drawing carrying no share row, revealing nothing about its existence. `src: Core features rule 51`
- [ ] `C-CF-82` `contract` The app serves version bytes only through its own authenticated download endpoint. `src: Core features rule 52`
- [ ] `C-CF-83` `literal` The app denies Priya Raman every read of Harbour Pavilion. `src: Core features rule 53`
- [ ] `C-CF-84` `capability` The app measures distance, radius, angle, area, perimeter in the drawing's units. `src: Core features rule 54`
- [ ] `C-CF-85` `capability` The app draws freehand strokes, shapes, callouts, text notes as markup, changing no entity. `src: Core features rule 55`
- [ ] `C-CF-86` `literal` The app titles the docked assistant panel Draft Assistant plus answers a question about a command in context. `src: Core features rule 56`
- [ ] `C-CF-87` `literal` The app serves a privacy page stating what a drawing's stored bytes are, with the retention period for a deleted drawing. `src: Core features rule 57`
- [ ] `C-CF-88` `contract` The app links the privacy page from the footer of every publicly reachable page. `src: Core features rule 57`
- [ ] `C-CF-89` `contract` The app links the terms page from the footer of every public page plus from the signup form. `src: Core features rule 58`
- [ ] `C-CF-90` `constraint` The app rejects invalid form input inline, names the failing field, writes nothing. `src: Core features rule 59`
- [ ] `C-CF-91` `ui` The app preserves every other field's entry on a rejected form. `src: Core features rule 59`

## C-UF User flow

- [ ] `C-UF-01` `contract` The app resolves the entry address to the library for a signed-in account plus to sign-in for a signed-out visitor. `src: User flow route table row 1`
- [ ] `C-UF-02` `contract` The app serves the sign-in, signup, privacy, terms addresses publicly. `src: User flow route table row 2`
- [ ] `C-UF-03` `contract` The app serves the workspace plus the version history to the owner or a shared account. `src: User flow route table row 10`
- [ ] `C-UF-04` `contract` The app serves the share page to the owner alone. `src: User flow route table row 12`
- [ ] `C-UF-05` `capability` The app sends an unauthenticated request for a protected route to sign-in plus continues to the remembered destination afterwards. `src: User flow, entry and redirects`
- [ ] `C-UF-06` `constraint` The app blocks a back-navigation return to the workspace after sign-out. `src: User flow, entry and redirects`
- [ ] `C-UF-07` `capability` The app keeps canvas work when a token expires mid-edit plus continues after a fresh sign-in. `src: User flow, entry and redirects`
- [ ] `C-UF-08` `capability` The app returns a reviewer reaching a creation step or a share page to the library. `src: User flow, entry and redirects`
- [ ] `C-UF-09` `ui` The app shows an empty-canvas message naming the command input. `src: User flow, states`
- [ ] `C-UF-10` `ui` The app shows a loading field until the workspace is ready, with a quiet placeholder inside a panel that is still loading. `src: User flow, states`
- [ ] `C-UF-11` `ui` The app explains a refused save in words plus leaves the canvas unchanged. `src: User flow, states`
- [ ] `C-UF-12` `constraint` The app shows no blank screen plus no unhandled error on any route. `src: User flow, states`
- [ ] `C-UF-13` `ui` The app shows an empty-comment-list message when a drawing carries no thread. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The app keeps every chrome surface unsaturated, placing no drawing index colour on one. `src: UI/UX notes, two colour worlds`
- [ ] `C-UX-02` `ui` The app carries icons plus secondary text in a light cool neutral as the dominant chrome colour. `src: UI/UX notes, two colour worlds`
- [ ] `C-UX-03` `ui` The app places panels on a near-white neutral surface that stays visibly separate from the field behind, with no drawn border. `src: UI/UX notes, two colour worlds`
- [ ] `C-UX-04` `ui` The app sets strong text in a deep cool neutral as the only dark ink in the chrome. `src: UI/UX notes, two colour worlds`
- [ ] `C-UX-05` `ui` The app washes a selection in a translucent near-white muted blue used for nothing else. `src: UI/UX notes, two colour worlds`
- [ ] `C-UX-06` `literal` The app colours the drawing index from a mid vivid red at 1 through a deep soft green at 3 plus a mid vivid violet at 6 to a near-white neutral at 7. `src: UI/UX notes, drawing colour index`
- [ ] `C-UX-07` `ui` The app draws model space on a near-black neutral background. `src: UI/UX notes, drawing colour index`
- [ ] `C-UX-08` `capability` The app reaches the same colour from a colour name as from a colour index. `src: UI/UX notes, drawing colour index`
- [ ] `C-UX-09` `ui` The app names one interface font family carrying a fallback stack, shipping no font binary. `src: UI/UX notes, type`
- [ ] `C-UX-10` `ui` The app distinguishes a panel heading from body by size alone, reserving the only heavier type for emphasised labels. `src: UI/UX notes, type`
- [ ] `C-UX-11` `ui` The app aligns stacked measurements digit under digit. `src: UI/UX notes, type`
- [ ] `C-UX-12` `ui` The app rounds an icon button corner barely, a floating panel corner more, nothing else. `src: UI/UX notes, shape`
- [ ] `C-UX-13` `ui` The app lifts a floating panel above the canvas on a soft diffuse shadow, the only depth cue in the product. `src: UI/UX notes, shape`
- [ ] `C-UX-14` `ui` The app fits a full layer list beside a full property set without scrolling. `src: UI/UX notes, density`
- [ ] `C-UX-15` `ui` The app gives an icon button resting, pointed-at, pressed, focused, unavailable states, signalling unavailable by more than colour. `src: UI/UX notes, components`
- [ ] `C-UX-16` `ui` The app moves a pointed-at button's shadow, background, glyph colour together, snapping the focus ring in faster. `src: UI/UX notes, components`
- [ ] `C-UX-17` `ui` The app draws a panel resize grip as pale diagonal lines firming on hover. `src: UI/UX notes, components`
- [ ] `C-UX-18` `ui` The app closes an open surface on Escape plus confirms a destructive action before acting. `src: UI/UX notes, components`
- [ ] `C-UX-19` `ui` The app moves every chrome transition at one speed on one curve. `src: UI/UX notes, motion`
- [ ] `C-UX-20` `ui` The app sweeps a thin ring continuously around the badge until the workspace is ready. `src: UI/UX notes, motion`
- [ ] `C-UX-21` `constraint` The app animates nothing on the drawing canvas. `src: UI/UX notes, motion`
- [ ] `C-UX-22` `ui` The app stills the sweeping ring under a reduced-motion preference, removing no content. `src: UI/UX notes, motion`
- [ ] `C-UX-23` `ui` The app fills the browser window at every viewport size. `src: UI/UX notes, responsive behaviour`
- [ ] `C-UX-24` `ui` The app collapses a panel toward its edge as the window narrows, keeping the canvas the majority of the screen with nothing overflowing sideways. `src: UI/UX notes, responsive behaviour`
- [ ] `C-UX-25` `capability` The app accepts two-finger pan, two-finger zoom, tap to select, long press for a context menu on a touch screen. `src: UI/UX notes, responsive behaviour`
- [ ] `C-UX-26` `ui` The app reflows a public page to one readable column. `src: UI/UX notes, responsive behaviour`
- [ ] `C-UX-27` `contract` The app meets WCAG AA contrast between body text plus its background. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-28` `contract` The app reaches every command through the command input by keyboard navigation. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-29` `ui` The app shows a visible focus ring on every keyboard-reachable control. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-30` `ui` The app names every icon-only control, every presence marker, every comment marker. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-31` `constraint` The app states a layer's off, locked or frozen condition in text beside its swatch. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-32` `contract` The app sizes every touch target comfortably for a fingertip. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-33` `ui` The app keeps the space above the drawing canvas free of a marketing composition. `src: UI/UX notes, what this must not look like`
- [ ] `C-UX-34` `ui` The app lets keyboard focus leave the drawing canvas to reach every floating panel. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-35` `ui` The app fills toolbar space only with a glyph that names a command. `src: UI/UX notes, what this must not look like`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app builds its frontend with Preact on Vite plus serves its backend with Litestar. `src: Technical requirements, stack`
- [ ] `C-TR-02` `contract` The app serves the HTTP API under the /api prefix on its own origin. `src: Technical requirements, stack`
- [ ] `C-TR-03` `contract` The app reaches PostgreSQL at DATABASE_URL. `src: Technical requirements, stack`
- [ ] `C-TR-04` `contract` The app reaches minio at STORAGE_ENDPOINT using STORAGE_BUCKET, STORAGE_ACCESS_KEY, STORAGE_SECRET_KEY. `src: Technical requirements, stack`
- [ ] `C-TR-05` `contract` The app serves an application shell on first paint plus assembles every later screen in the browser from JSON. `src: Technical requirements para 1`
- [ ] `C-TR-06` `contract` The app returns 200 from the health endpoint once ready. `src: Technical requirements, stack`
- [ ] `C-TR-07` `constraint` The app hardcodes no host, port or credential, starts no copy of a named backing service. `src: Technical requirements, environment paragraph`
- [ ] `C-TR-08` `constraint` The app introduces no second database, cache, queue, object store, identity provider or mail vendor. `src: Technical requirements, library paragraph`
- [ ] `C-TR-09` `contract` The app stores a saved version's bytes as a real object in the minio bucket plus nowhere else. `src: Technical requirements, drawing bytes`
- [ ] `C-TR-10` `constraint` The app rebuilds no downloaded document from entity rows, returning bytes whose SHA-256 equals the recorded digest. `src: Technical requirements, drawing bytes`
- [ ] `C-TR-11` `contract` The app confirms the requesting account may read a drawing before serving that drawing's bytes. `src: Technical requirements, protected reads`
- [ ] `C-TR-12` `capability` The app delivers a saved change to another open workspace within a few seconds. `src: Technical requirements, live reach`
- [ ] `C-TR-13` `literal` The app stays interactive with 200 versions in one drawing's history. `src: Technical requirements, responsiveness bar`
- [ ] `C-TR-14` `constraint` The app drives the entry screen by real progress rather than a fixed wait. `src: Technical requirements, responsiveness bar`
- [ ] `C-TR-15` `literal` The app lists every public route in the sitemap. `src: Technical requirements, discovery`
- [ ] `C-TR-16` `literal` The app vertices the robots file at the sitemap by absolute address. `src: Technical requirements, discovery`
- [ ] `C-TR-17` `capability` The app declares a social preview title plus image on every public route, no two alike, each image resolving. `src: Technical requirements, discovery`

## C-DM Data model

- [ ] `C-DM-01` `data` The app stores every timestamp in UTC. `src: Data model, opening`
- [ ] `C-DM-02` `contract` The app writes every seeded account's credentials into the documented credentials file. `src: Data model, password paragraph`
- [ ] `C-DM-03` `data` The app keeps an account email unique under lowercasing on write. `src: Data model, accounts`
- [ ] `C-DM-04` `data` The app restricts an account role to drafter or reviewer. `src: Data model, accounts`
- [ ] `C-DM-05` `data` The app restricts a drawing's units to millimeters, meters, inches or feet, its template to blank, architectural or mechanical. `src: Data model, drawings`
- [ ] `C-DM-06` `data` The app sets a drawing's current version to 0 before the first save plus to the highest version number afterwards. `src: Data model, drawings`
- [ ] `C-DM-07` `data` The app restricts a layer colour index to the range 1 through 7. `src: Data model, layers`
- [ ] `C-DM-08` `data` The app keeps a layer name plus a layer draw-order position unique within a drawing. `src: Data model, layers`
- [ ] `C-DM-09` `data` The app stores an entity coordinate list as an ordered sequence of x plus y in drawing units, rounding nothing on write. `src: Data model, entities`
- [ ] `C-DM-10` `data` The app treats a null entity colour index plus a lineweight of -1 as following the layer. `src: Data model, entities`
- [ ] `C-DM-11` `data` The app restricts an entity linetype to continuous, dashed, center or hidden. `src: Data model, entities`
- [ ] `C-DM-12` `data` The app derives a dimension's measured value from the entity the dimension measures. `src: Data model, entities`
- [ ] `C-DM-13` `data` The app keeps a version number unique within a drawing plus records its digest as lowercase hex SHA-256. `src: Data model, versions`
- [ ] `C-DM-14` `data` The app keeps one share row per drawing plus account pair, restricted to view, comment or edit. `src: Data model, shares`
- [ ] `C-DM-15` `data` The app rejects a comment whose body is empty. `src: Data model, comments`
- [ ] `C-DM-16` `data` The app keeps one presence row per drawing plus account pair. `src: Data model, presence`
- [ ] `C-DM-17` `data` The app covers every entity one action changed inside one undo step plus restores them together. `src: Data model, undo_steps`
- [ ] `C-DM-18` `data` The app replays an undo step forward on redo. `src: Data model, undo_steps`
- [ ] `C-DM-19` `constraint` The app lets no entity reference a layer belonging to a different drawing. `src: Data model, invariants`
- [ ] `C-DM-20` `constraint` The app lets a reviewer own no drawing, entity, layer or version row. `src: Data model, invariants`
- [ ] `C-DM-21` `literal` The app seeds Harbour Pavilion owned by Mira Vance at current version 2 plus shared with nobody. `src: Data model, seed data`
- [ ] `C-DM-22` `literal` The app seeds Rail Shed Section shared to Priya Raman at comment. `src: Data model, seed data`
- [ ] `C-DM-23` `literal` The app seeds Kiln House Elevation owned by Owen Blake. `src: Data model, seed data`
- [ ] `C-DM-24` `literal` The app seeds Harbour Pavilion with the layers Base at 7, Walls at 1, Dimensions at 3, Notes at 6. `src: Data model, seed data`
- [ ] `C-DM-25` `data` The app seeds Harbour Pavilion with a closed rectangle ten metres along its long side, a circle, a linear dimension, a multi-line note. `src: Data model, seed data`
- [ ] `C-DM-26` `data` The app stores every seeded version's bytes as an object in the minio bucket. `src: Data model, seed data`
- [ ] `C-DM-27` `literal` The app seeds Site Survey Grid with exactly 40 layers carrying exactly 20000 entities between them, every layer holding geometry. `src: Data model, seed data`
- [ ] `C-DM-28` `constraint` The app duplicates no row when seeding runs a second time. `src: Data model, seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The app fills the entry window with a near-black neutral field carrying the centred badge inside a sweeping ring plus nothing else. `src: Front-end specification, entry screen`
- [ ] `C-FE-02` `ui` The app draws the badge as a softened square in the product's red carrying a near-white monogram. `src: Front-end specification, entry screen`
- [ ] `C-FE-03` `ui` The app fixes a top bar carrying the badge, the drawing name, the tool groups, the account controls. `src: Front-end specification, workspace frame`
- [ ] `C-FE-04` `ui` The app groups left tool buttons by purpose rather than alphabetically. `src: Front-end specification, workspace frame`
- [ ] `C-FE-05` `ui` The app makes every floating panel dockable, poppable, movable, closable, resizable. `src: Front-end specification, workspace frame`
- [ ] `C-FE-06` `ui` The app draws every icon as inline vector geometry on one small square grid rather than an image file. `src: Front-end specification, workspace frame`
- [ ] `C-FE-07` `ui` The app draws the dock glyph as a filled quadrant square carrying a cut-out plus the close glyph as a diagonal cross with squared ends. `src: Front-end specification, workspace frame`
- [ ] `C-FE-08` `ui` The app places a bottom status bar carrying the cursor coordinate readout beside the model plus paper space tabs. `src: Front-end specification, workspace frame`
- [ ] `C-FE-09` `ui` The app renders lineweight at a uniform hairline when lineweight display is off. `src: Front-end specification, canvas surface`
- [ ] `C-FE-10` `constraint` The app drops no entity from the drawing when dropping detail from a frame. `src: Front-end specification, canvas surface`
- [ ] `C-FE-11` `ui` The app draws each snap kind as its own distinct marker shape. `src: Front-end specification, canvas surface`
- [ ] `C-FE-12` `ui` The app removes a tracking guide line the moment the alignment stops holding. `src: Front-end specification, canvas surface`
- [ ] `C-FE-13` `ui` The app places the library card grid under a persistent left sidebar, reflowing by width without cutting a card off. `src: Front-end specification, library`
- [ ] `C-FE-14` `ui` The app shows a small preview of a drawing's extents on the drawing's card. `src: Front-end specification, library`
- [ ] `C-FE-15` `ui` The app shows where the visitor is in the creation sequence, letting the previous step be returned to without losing what was already answered. `src: Front-end specification, creation sequence`
- [ ] `C-FE-16` `ui` The app keeps the status bar readout present without interrupting. `src: Front-end specification, feedback`
- [ ] `C-FE-17` `ui` The app states a discrete outcome in a dismissible confirmation near the screen edge that never covers the status bar. `src: Front-end specification, feedback`
- [ ] `C-FE-18` `constraint` The app ships no logo binary, generating the seeded drawings' geometry in code. `src: Front-end specification, procedural assets`
- [ ] `C-FE-19` `contract` The app titles every browser tab with the pinned product title string. `src: Front-end specification, pinned copy`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app offers no organisation above the account plus charges no payment. `src: Constraints para 1`
- [ ] `C-CN-02` `constraint` The app reads plus writes no industry binary drawing format. `src: Constraints para 2`
- [ ] `C-CN-03` `constraint` The app performs no boolean operation on a three-dimensional solid plus renders no shaded three-dimensional view. `src: Constraints para 2`
- [ ] `C-CN-04` `constraint` The app authors no new dynamic block parameter. `src: Constraints para 2`
- [ ] `C-CN-05` `constraint` The app attaches no external drawing reference plus no raster image underlay. `src: Constraints para 2`
- [ ] `C-CN-06` `constraint` The app plots to no printer plus exports to no page based document. `src: Constraints para 2`
- [ ] `C-CN-07` `constraint` The app builds no table carrying a formula plus provides no auto updating field. `src: Constraints para 2`
- [ ] `C-CN-08` `constraint` The app sends no email plus makes no external network call at runtime. `src: Constraints para 3`
- [ ] `C-CN-09` `constraint` The app fetches no address outside its own origin at runtime plus records no analytics. `src: Constraints, asset host paragraph`
- [ ] `C-CN-10` `constraint` The app carries no third party brand name, no proprietary font binary, no sample drawing file. `src: Constraints, borrowed identity paragraph`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app reads its outward port from APP_PUBLIC_PORT plus listens on the container-internal port 4173. `src: Deployment contract, bullet 1`
- [ ] `C-DC-02` `contract` The app reads its public address from APP_PUBLIC_URL. `src: Deployment contract, bullet 1`
- [ ] `C-DC-03` `contract` The app serves GET /api/health with status 200. `src: Deployment contract, bullet 3`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual step plus runs detached so the server outlives the build session. `src: Deployment contract, bullet 4`
- [ ] `C-DC-05` `contract` The app writes login credentials to /app/USER_README.md. `src: Deployment contract, bullet 5`
- [ ] `C-DC-06` `contract` The app creates empty .browser_screenshots/ plus .downloads/ directories at the app root. `src: Deployment contract, bullet 6`
- [ ] `C-DC-07` `contract` The app serves a production build behind a static or preview server bound to 0.0.0.0. `src: Deployment contract, bullet 7`
- [ ] `C-DC-08` `constraint` The app deploys no edge function plus declares no persistent volume, fixed container name or custom network. `src: Deployment contract, bullet 11`
- [ ] `C-DC-09` `contract` The app returns a top-level JSON array from every list endpoint. `src: Deployment contract, API shapes`
- [ ] `C-DC-10` `contract` The app rejects an invalid or unauthorized call as a client error naming the reason. `src: Deployment contract, API shapes`
- [ ] `C-DC-11` `contract` The app requires bearer auth on every endpoint apart from signup, login, health. `src: Deployment contract, API shapes`
- [ ] `C-DC-12` `contract` The app accepts the signup, login, current-account endpoints at their pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-13` `contract` The app accepts the drawing list plus create endpoints at their pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-14` `contract` The app accepts the entity list, create, update, delete endpoints at their pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-15` `contract` The app accepts the layer list, create, update, delete endpoints at their pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-16` `contract` The app accepts the version create, download, restore, compare endpoints at their pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-17` `contract` The app accepts the share list, create, delete endpoints at their pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-18` `contract` The app accepts the comment list, create, resolve endpoints at their pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-19` `contract` The app accepts the presence, undo, redo endpoints at their pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-20` `constraint` The app keeps no in-memory substitute for the minio bucket plus returns no stubbed success standing in for a store write. `src: Deployment contract, no mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | password for every seeded account | C-CF-01 | Core features, Auth |
| `drafter@example.com` | seeded drafter account | C-RL-14 | User roles, seeded accounts table |
| `drafter2@example.com` | second seeded drafter account | C-RL-14 | User roles, seeded accounts table |
| `reviewer@example.com` | seeded reviewer account | C-RL-14 | User roles, seeded accounts table |
| `drafter` | the owning account role | C-RL-12 | User roles, signup paragraph |
| `reviewer` | the reading account role | C-RL-14 | User roles, seeded accounts table |
| `24 hours` | bearer token lifetime | C-CF-01 | Core features, Auth |
| `blank` | template choice | C-CF-10 | Core features, drawing library |
| `architectural` | template choice | C-CF-10 | Core features, drawing library |
| `mechanical` | template choice | C-CF-10 | Core features, drawing library |
| `millimeters` | units choice | C-CF-10 | Core features, drawing library |
| `meters` | units choice | C-CF-10 | Core features, drawing library |
| `inches` | units choice | C-CF-10 | Core features, drawing library |
| `feet` | units choice | C-CF-10 | Core features, drawing library |
| `Base` | the undeletable layer on every drawing | C-CF-16 | Core features rule 6 |
| `Walls` | seeded layer on Harbour Pavilion | C-CF-16 | Core features rule 6 |
| `Dimensions` | seeded layer on Harbour Pavilion | C-CF-16 | Core features rule 6 |
| `Notes` | seeded layer on Harbour Pavilion | C-CF-16 | Core features rule 6 |
| `20000` | entity count the workspace stays interactive at | C-CF-22 | Core features rule 11 |
| `40` | layer count the workspace stays interactive at | C-CF-22 | Core features rule 11 |
| `200` | version count the app stays interactive at | C-TR-13 | Technical requirements, responsiveness bar |
| `.dxe` | drawing exchange document extension | C-CF-56 | Core features, versions in the cloud object store |
| `drawings/{drawing_id}/v{version_number}/{byte_digest}.dxe` | object key scheme | C-CF-57 | Core features rule 37 |
| `two minutes` | presence expiry | C-CF-73 | Core features rule 46 |
| `Harbour Pavilion` | seeded unshared drawing | C-CF-83 | Core features rule 53 |
| `Rail Shed Section` | seeded shared drawing | C-DM-21 | Data model, seed data |
| `Kiln House Elevation` | seeded drawing of the second drafter | C-DM-21 | Data model, seed data |
| `Mira Vance` | seeded drafter display name | C-DM-21 | Data model, seed data |
| `Owen Blake` | seeded second drafter display name | C-DM-21 | Data model, seed data |
| `Priya Raman` | seeded reviewer display name | C-DM-21 | Data model, seed data |
| `Draft Assistant` | assistant panel title | C-CF-86 | Core features rule 56 |
| `-1` | lineweight value meaning follow the layer | C-DM-09 | Data model, entities |
| `1 through 7` | the drawing colour index range | C-DM-07 | Data model, layers |
| `2` | seeded current version of Harbour Pavilion | C-DM-21 | Data model, seed data |
| `mid vivid red` | drawing colour index 1 | C-UX-06 | UI/UX notes, drawing colour index |
| `deep soft green` | drawing colour index 3 | C-UX-06 | UI/UX notes, drawing colour index |
| `mid vivid violet` | drawing colour index 6 | C-UX-06 | UI/UX notes, drawing colour index |
| `near-white neutral` | drawing colour index 7 | C-UX-06 | UI/UX notes, drawing colour index |
| `4173` | container-internal port | C-DC-01 | Deployment contract, bullet 1 |
| `0.0.0.0` | bind address | C-DC-07 | Deployment contract, bullet 7 |
| `/app/USER_README.md` | credentials file path | C-DC-05 | Deployment contract, bullet 5 |
| `/api/health` | health route | C-DC-03 | Deployment contract, bullet 3 |
| `DATABASE_URL` | database connection variable | C-TR-01 | Technical requirements, stack |
| `STORAGE_ENDPOINT` | object store variable | C-TR-01 | Technical requirements, stack |
| `STORAGE_BUCKET` | bucket name variable | C-TR-01 | Technical requirements, stack |
| `APP_PUBLIC_PORT` | outward port variable | C-DC-01 | Deployment contract, bullet 1 |
| `APP_PUBLIC_URL` | public address variable | C-DC-01 | Deployment contract, bullet 1 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the interface font family | C-UX-09 | named by role with no family given, so the builder chooses one |
| the polar tracking angle increment | C-CF-26 | called configurable with no default increment stated |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 3 | 7 |
| User roles | 1 | 16 |
| Core features | 17 | 91 |
| User flow | 9 | 13 |
| UI and UX notes | 9 | 35 |
| Technical requirements | 5 | 17 |
| Data model | 3 | 28 |
| Front-end specification | 2 | 19 |
| Constraints | 3 | 10 |
| Deployment contract | 10 | 20 |
