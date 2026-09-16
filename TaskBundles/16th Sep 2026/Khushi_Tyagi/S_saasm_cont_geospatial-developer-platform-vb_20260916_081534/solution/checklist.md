# Checklist: Geoform

Source: instruction.md
Sections present: overview, user roles, core features, user flow, ui and ux notes, technical requirements, data model, front-end specification, constraints, deployment contract
Sections absent: build plan
Items: 294
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public marketing site at the root address. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app embeds a live interactive map in the home page. `src: Overview para 1`
- [ ] `C-OV-03` `capability` The app serves a signed-in studio for developers. `src: Overview para 2`
- [ ] `C-OV-04` `constraint` The app renders every marketing page without the map client loading. `src: Overview para 3`
- [ ] `C-OV-05` `constraint` The app contacts no external map provider at runtime. `src: Overview para 4`
- [ ] `C-OV-06` `constraint` The app contacts no external geocoder at runtime. `src: Overview para 4`
- [ ] `C-OV-07` `constraint` The app serves no planetary coverage beyond one seeded region. `src: Overview para 4`
- [ ] `C-OV-08` `capability` The app keeps an uploaded dataset unreadable until the owner publishes one. `src: Overview para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` An author signs up without an invitation. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An author issues a scoped access token. `src: User roles table row 1`
- [ ] `C-RL-03` `role` An author revokes an access token. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An author uploads a dataset. `src: User roles table row 1`
- [ ] `C-RL-05` `role` An author publishes a style version. `src: User roles table row 1`
- [ ] `C-RL-06` `constraint` An author reads no other author's private tileset. `src: User roles table row 1`
- [ ] `C-RL-07` `constraint` An author reads no other author's usage figure. `src: User roles table row 1`
- [ ] `C-RL-08` `constraint` An author reads no token secret after the screen that created one. `src: User roles table row 1`
- [ ] `C-RL-09` `role` A reader reads every marketing route. `src: User roles table row 2`
- [ ] `C-RL-10` `role` A reader reads every published style. `src: User roles table row 2`
- [ ] `C-RL-11` `constraint` A reader reads no private tileset. `src: User roles table row 2`
- [ ] `C-RL-12` `constraint` A reader reaches no studio address. `src: User roles table row 2`
- [ ] `C-RL-13` `role` A project owner publishes a version. `src: User roles, membership para`
- [ ] `C-RL-14` `role` A project editor commits a style operation. `src: User roles, membership para`
- [ ] `C-RL-15` `constraint` A project viewer commits no style operation. `src: User roles, membership para`
- [ ] `C-RL-16` `constraint` A direct call from a reader session to an author-only endpoint leaves the protected state unchanged. `src: User roles, authorization para`
- [ ] `C-RL-17` `literal` The app seeds an author account at `author@example.com`. `src: User roles, seeded accounts table`
- [ ] `C-RL-18` `literal` The app seeds a second author account at `author2@example.com`. `src: User roles, seeded accounts table`
- [ ] `C-RL-19` `literal` The app seeds a reader account at `reader@example.com`. `src: User roles, seeded accounts table`
- [ ] `C-RL-20` `data` The app gives each seeded author one private tileset. `src: User roles, seeded accounts para`

## C-CF Core features

- [ ] `C-CF-01` `capability` The app creates an author account from the public sign-up form. `src: Core features, accounts, rule 1`
- [ ] `C-CF-02` `constraint` The app refuses a second sign-up for an address that already exists. `src: Core features, accounts, rule 1`
- [ ] `C-CF-03` `capability` The app returns a bearer token on a sign-in with a correct password. `src: Core features, accounts, rule 2`
- [ ] `C-CF-04` `constraint` The app denies a sign-in with a wrong password. `src: Core features, accounts, rule 2`
- [ ] `C-CF-05` `constraint` The app reveals no account existence in a denied sign-in response. `src: Core features, accounts, rule 2`
- [ ] `C-CF-06` `capability` The app shows a new token secret exactly once at creation. `src: Core features, accounts, rule 3`
- [ ] `C-CF-07` `constraint` The app returns no token secret on any later read. `src: Core features, accounts, rule 3`
- [ ] `C-CF-08` `capability` The app refuses a revoked token on the next use. `src: Core features, accounts, rule 4`
- [ ] `C-CF-09` `constraint` The app leaves every other token working after one revocation. `src: Core features, accounts, rule 4`
- [ ] `C-CF-10` `constraint` The app refuses a tile-scoped token presented to the directions service. `src: Core features, accounts, rule 5`
- [ ] `C-CF-11` `capability` The app names the missing scope in a scope refusal. `src: Core features, accounts, rule 5`
- [ ] `C-CF-12` `capability` The app counts one usage event per billable action. `src: Core features, accounts, rule 6`
- [ ] `C-CF-13` `capability` The app reconciles a readable usage total with the actions one account made. `src: Core features, accounts, rule 6`
- [ ] `C-CF-14` `constraint` The app bills nothing for a call refused past the free-tier allowance. `src: Core features, accounts, rule 7`
- [ ] `C-CF-15` `capability` The app returns a quota limit as a catchable limit naming what was exceeded. `src: Core features, accounts, rule 8`
- [ ] `C-CF-16` `literal` The app renders the promo banner line `BUILD with Geoform`. `src: Core features, marketing, rule 2`
- [ ] `C-CF-17` `capability` The app persists a promo banner dismissal across a reload. `src: Core features, marketing, rule 2`
- [ ] `C-CF-18` `ui` The app renders five dropdown menus in the top navigation. `src: Core features, marketing, rule 3`
- [ ] `C-CF-19` `capability` The app replaces the sign-up control with a go-to-account control once signed in. `src: Core features, marketing, rule 3`
- [ ] `C-CF-20` `ui` The app renders five footer link columns on every marketing page. `src: Core features, marketing, rule 4`
- [ ] `C-CF-21` `ui` The app renders four product subgroups in the footer. `src: Core features, marketing, rule 4`
- [ ] `C-CF-22` `literal` The app renders the footer badge `SUBSCRIBE` beside the newsletter link. `src: Core features, marketing, rule 5`
- [ ] `C-CF-23` `literal` The app renders the footer badge `HIRING` beside the careers link. `src: Core features, marketing, rule 5`
- [ ] `C-CF-24` `ui` The app renders the home bands in the stated order. `src: Core features, marketing, rule 6`
- [ ] `C-CF-25` `literal` The app renders the hero heading `Do more with maps & navigation`. `src: Core features, marketing, rule 7`
- [ ] `C-CF-26` `ui` The app brings the hero heading in letter by letter as a reader arrives. `src: Core features, marketing, rule 7`
- [ ] `C-CF-27` `literal` The app renders the live map heading `Explore Geoform live`. `src: Core features, marketing, rule 8`
- [ ] `C-CF-28` `ui` The app alternates text with visual across the product rails. `src: Core features, marketing, rule 9`
- [ ] `C-CF-29` `literal` The app renders the rail heading naming flexibility with control. `src: Core features, marketing, rule 9`
- [ ] `C-CF-30` `ui` The app renders three panels on the control rail device visual. `src: Core features, marketing, rule 11`
- [ ] `C-CF-31` `literal` The app renders five data layer toggles on the control rail. `src: Core features, marketing, rule 11`
- [ ] `C-CF-32` `ui` The app renders a swipeable carousel of customer story cards. `src: Core features, marketing, rule 12`
- [ ] `C-CF-33` `ui` The app glides a strip of placeholder customer marks sideways without stopping. `src: Core features, marketing, rule 12`
- [ ] `C-CF-34` `ui` The app renders every non-home marketing page from one shared template. `src: Core features, marketing, rule 14`
- [ ] `C-CF-35` `literal` The app renders the closing band heading `Ready to get started?`. `src: Core features, marketing, rule 14`
- [ ] `C-CF-36` `literal` The app renders the electric-vehicle hero `Geoform for EV`. `src: Core features, marketing, rule 15`
- [ ] `C-CF-37` `ui` The app renders five product cards on the electric-vehicle page. `src: Core features, marketing, rule 15`
- [ ] `C-CF-38` `capability` The app serves the Japanese-locale home with the same layout. `src: Core features, marketing, rule 16`
- [ ] `C-CF-39` `constraint` The app depends on no Latin word length in any layout measure. `src: Core features, marketing, rule 16`
- [ ] `C-CF-40` `literal` The app renders the not-found heading `Page Not Found`. `src: Core features, marketing, rule 17`
- [ ] `C-CF-41` `capability` The app answers an unmatched address as not found. `src: Core features, marketing, rule 17`
- [ ] `C-CF-42` `capability` The app persists a consent answer across a reload. `src: Core features, marketing, rule 18`
- [ ] `C-CF-43` `ui` The app carries alternative text on every content image. `src: Core features, marketing, rule 19`
- [ ] `C-CF-44` `ui` The app declares a decorative image as decorative. `src: Core features, marketing, rule 19`
- [ ] `C-CF-45` `ui` The app carries a text alternative on the map canvas naming the active scene. `src: Core features, marketing, rule 19`
- [ ] `C-CF-46` `contract` The app lists every public route in a sitemap. `src: Core features, marketing, rule 20`
- [ ] `C-CF-47` `contract` The app names the sitemap from a robots file. `src: Core features, marketing, rule 20`
- [ ] `C-CF-48` `capability` The app records every public page view with a route. `src: Core features, marketing, rule 21`
- [ ] `C-CF-49` `constraint` The app returns no page view record to a reader. `src: Core features, marketing, rule 21`
- [ ] `C-CF-50` `capability` The app renders the home map from the real rendering engine. `src: Core features, live map, rule 1`
- [ ] `C-CF-51` `literal` The app lists the scene `Globe View` described as `Rotating 3D globe`. `src: Core features, live map, rule 2`
- [ ] `C-CF-52` `literal` The app lists the scene `Data Overlay (2D)` described as `Live seismic event heatmap`. `src: Core features, live map, rule 2`
- [ ] `C-CF-53` `literal` The app offers four lighting presets named `Dawn`, `Day`, `Dusk`, `Night`. `src: Core features, live map, rule 3`
- [ ] `C-CF-54` `literal` The app offers the colour themes `Default`, `Faded`. `src: Core features, live map, rule 3`
- [ ] `C-CF-55` `capability` The app swaps the active data with the lighting when a scene is selected. `src: Core features, live map, rule 4`
- [ ] `C-CF-56` `constraint` The app reloads no page when a lighting preset is selected. `src: Core features, live map, rule 4`
- [ ] `C-CF-57` `capability` The app rotates the globe scene until a reader touches one. `src: Core features, live map, rule 5`
- [ ] `C-CF-58` `ui` The app updates the render continuously during a drag. `src: Core features, live map, rule 6`
- [ ] `C-CF-59` `ui` The app sends an expanding ripple out from the position marker. `src: Core features, live map, rule 7`
- [ ] `C-CF-60` `capability` The app draws vector tiles with the graphics hardware. `src: Core features, engine, rule 1`
- [ ] `C-CF-61` `capability` The app extrudes buildings from their footprints under pitch. `src: Core features, engine, rule 2`
- [ ] `C-CF-62` `capability` The app drapes the styled surface over elevation data. `src: Core features, engine, rule 3`
- [ ] `C-CF-63` `capability` The app composites a live overlay layer over the base each frame. `src: Core features, engine, rule 4`
- [ ] `C-CF-64` `capability` The app resolves label collision every frame. `src: Core features, engine, rule 5`
- [ ] `C-CF-65` `capability` The app falls back to a still rendered image where the graphics context is absent. `src: Core features, engine, rule 6`
- [ ] `C-CF-66` `constraint` The app renders no blank canvas when the graphics context is absent. `src: Core features, engine, rule 6`
- [ ] `C-CF-67` `constraint` The app requests no tile when a style value changes. `src: Core features, engine, rule 7`
- [ ] `C-CF-68` `data` The app addresses tiles as a quadtree by zoom, column, row. `src: Core features, tiles, rule 1`
- [ ] `C-CF-69` `data` The app clips a vector tile to its bounds with a buffer. `src: Core features, tiles, rule 2`
- [ ] `C-CF-70` `capability` The app produces a tile on demand rather than eagerly. `src: Core features, tiles, rule 3`
- [ ] `C-CF-71` `capability` The app drops detail invisible at the requested zoom. `src: Core features, tiles, rule 4`
- [ ] `C-CF-72` `constraint` The app uses one source definition across every zoom level. `src: Core features, tiles, rule 5`
- [ ] `C-CF-73` `capability` The app serves a produced tile again without recomputing one. `src: Core features, tiles, rule 6`
- [ ] `C-CF-74` `capability` The app marks dirty only the tiles whose bounds a source change intersects. `src: Core features, tiles, rule 7`
- [ ] `C-CF-75` `constraint` The app marks no distant tile dirty on a local source change. `src: Core features, tiles, rule 7`
- [ ] `C-CF-76` `capability` The app gives a live layer a shorter freshness than the base. `src: Core features, tiles, rule 8`
- [ ] `C-CF-77` `data` The app stores a style as a portable document rather than as code. `src: Core features, styling, rule 1`
- [ ] `C-CF-78` `data` The app supports nine named layer kinds. `src: Core features, styling, rule 2`
- [ ] `C-CF-79` `capability` The app evaluates a paint value as an expression per feature. `src: Core features, styling, rule 3`
- [ ] `C-CF-80` `capability` The app evaluates a paint value as an expression per zoom. `src: Core features, styling, rule 3`
- [ ] `C-CF-81` `capability` The app keys a building colour off a height attribute. `src: Core features, styling, rule 4`
- [ ] `C-CF-82` `constraint` The app needs no rule per feature to style thousands of features. `src: Core features, styling, rule 4`
- [ ] `C-CF-83` `capability` The app renders one style document identically wherever one is read. `src: Core features, styling, rule 5`
- [ ] `C-CF-84` `capability` The app serves a published style by reference. `src: Core features, styling, rule 6`
- [ ] `C-CF-85` `capability` The app accepts a source dataset authenticated by an account token. `src: Core features, ingestion, rule 1`
- [ ] `C-CF-86` `literal` The app stores uploaded bytes at the object key `uploads/{upload_id}/{sha256_of_bytes}.{ext}`. `src: Core features, ingestion, rule 2`
- [ ] `C-CF-87` `constraint` The app writes no uploaded byte to the application container filesystem. `src: Core features, ingestion, rule 2`
- [ ] `C-CF-88` `constraint` The app writes no uploaded byte to a database column. `src: Core features, ingestion, rule 2`
- [ ] `C-CF-89` `constraint` The app records no upload whose bytes never reached the bucket. `src: Core features, ingestion, rule 2`
- [ ] `C-CF-90` `capability` The app rejects a malformed source with an error naming what is wrong. `src: Core features, ingestion, rule 3`
- [ ] `C-CF-91` `constraint` The app stores no byte for a rejected upload. `src: Core features, ingestion, rule 3`
- [ ] `C-CF-92` `constraint` The app creates no tileset for a rejected upload. `src: Core features, ingestion, rule 3`
- [ ] `C-CF-93` `literal` The app reports an upload state of `queued`, `processing`, `complete`, or `failed`. `src: Core features, ingestion, rule 4`
- [ ] `C-CF-94` `constraint` The app blocks no request on a large upload. `src: Core features, ingestion, rule 4`
- [ ] `C-CF-95` `capability` The app cuts a source into the pyramid by a declarative recipe. `src: Core features, ingestion, rule 5`
- [ ] `C-CF-96` `data` The app creates a tileset private. `src: Core features, ingestion, rule 6`
- [ ] `C-CF-97` `constraint` The app answers a private tileset tile request carrying no token as not found. `src: Core features, ingestion, rule 6`
- [ ] `C-CF-98` `constraint` The app answers a private tileset tile request carrying another author's token as not found. `src: Core features, ingestion, rule 6`
- [ ] `C-CF-99` `constraint` The app answers a direct object store request for a private tile as not found. `src: Core features, ingestion, rule 6`
- [ ] `C-CF-100` `capability` The app returns a private tile to a token of the owning account carrying the tile-read scope. `src: Core features, ingestion, rule 6`
- [ ] `C-CF-101` `capability` The app makes tiles readable without a token when a tileset is published. `src: Core features, ingestion, rule 7`
- [ ] `C-CF-102` `capability` The app closes tile reads again on the next request after an unpublish. `src: Core features, ingestion, rule 7`
- [ ] `C-CF-103` `capability` The app re-cuts only the tiles whose bounds a new dataset version touches. `src: Core features, ingestion, rule 8`
- [ ] `C-CF-104` `constraint` The app creates no second object for bytes identical to those already stored. `src: Core features, ingestion, rule 9`
- [ ] `C-CF-105` `constraint` The app creates no second tileset for a repeated identical upload. `src: Core features, ingestion, rule 9`
- [ ] `C-CF-106` `capability` The app serves one stored tileset result to every caller. `src: Core features, ingestion, rule 10`
- [ ] `C-CF-107` `data` The app treats a project as one style with the datasets one names. `src: Core features, studio, rule 1`
- [ ] `C-CF-108` `data` The app records an edit as an operation on a path into the style tree. `src: Core features, studio, rule 2`
- [ ] `C-CF-109` `constraint` The app stores no whole-document save. `src: Core features, studio, rule 2`
- [ ] `C-CF-110` `capability` The app lands both of two operations on different paths. `src: Core features, studio, rule 3`
- [ ] `C-CF-111` `capability` The app stores the later of two commits to one path. `src: Core features, studio, rule 4`
- [ ] `C-CF-112` `capability` The app tells the author whose value was replaced. `src: Core features, studio, rule 4`
- [ ] `C-CF-113` `capability` The app records both same-path operations in the history with their actors. `src: Core features, studio, rule 4`
- [ ] `C-CF-114` `capability` The app shows a committed change on another member's canvas within a second. `src: Core features, studio, rule 5`
- [ ] `C-CF-115` `capability` The app delivers missed operations in order to a reconnecting member. `src: Core features, studio, rule 5`
- [ ] `C-CF-116` `constraint` The app repeats no operation to a reconnecting member. `src: Core features, studio, rule 5`
- [ ] `C-CF-117` `ui` The app shows each member's presence to the others. `src: Core features, studio, rule 6`
- [ ] `C-CF-118` `capability` The app repaints the shared canvas on a teammate's paint change. `src: Core features, studio, rule 7`
- [ ] `C-CF-119` `capability` The app restores an earlier style version. `src: Core features, studio, rule 8`
- [ ] `C-CF-120` `capability` The app records a restore as a logged operation. `src: Core features, studio, rule 8`
- [ ] `C-CF-121` `constraint` The app refuses a publish attempted by a project viewer. `src: Core features, studio, rule 9`
- [ ] `C-CF-122` `constraint` The app shows no work in progress to a reader. `src: Core features, studio, rule 9`
- [ ] `C-CF-123` `literal` The app offers the travel profiles `driving`, `walking`, `cycling`, `driving-traffic`. `src: Core features, services, rule 1`
- [ ] `C-CF-124` `capability` The app returns route geometry with a total distance. `src: Core features, services, rule 1`
- [ ] `C-CF-125` `capability` The app returns step-by-step maneuvers each carrying an instruction. `src: Core features, services, rule 1`
- [ ] `C-CF-126` `capability` The app returns a different duration for a congested seeded traffic table. `src: Core features, services, rule 1`
- [ ] `C-CF-127` `capability` The app returns one polygon per isochrone budget. `src: Core features, services, rule 2`
- [ ] `C-CF-128` `data` The app returns non-self-intersecting isochrone polygons. `src: Core features, services, rule 2`
- [ ] `C-CF-129` `data` The app nests a smaller isochrone budget inside a larger one. `src: Core features, services, rule 2`
- [ ] `C-CF-130` `capability` The app returns the full duration table between every origin-destination pair in one answer. `src: Core features, services, rule 3`
- [ ] `C-CF-131` `data` The app agrees between a matrix cell with the equivalent directions call. `src: Core features, services, rule 3`
- [ ] `C-CF-132` `constraint` The app refuses a request past a stated bound with a reason naming the bound. `src: Core features, services, rule 4`
- [ ] `C-CF-133` `constraint` The app truncates no answer silently at a bound. `src: Core features, services, rule 4`
- [ ] `C-CF-134` `literal` The app types a geocoding result as `address`, `place`, `poi`, or `region`. `src: Core features, services, rule 5`
- [ ] `C-CF-135` `capability` The app filters geocoding results by type. `src: Core features, services, rule 5`
- [ ] `C-CF-136` `capability` The app returns the nearest addressable place for a coordinate pair. `src: Core features, services, rule 6`
- [ ] `C-CF-137` `capability` The app ranks a nearby search match above a distant better textual match. `src: Core features, services, rule 7`
- [ ] `C-CF-138` `capability` The app completes a structured address from a partial one. `src: Core features, services, rule 7`
- [ ] `C-CF-139` `capability` The app finds a place added to a private dataset for the owning account. `src: Core features, services, rule 8`
- [ ] `C-CF-140` `constraint` The app finds no private dataset place for another account. `src: Core features, services, rule 8`
- [ ] `C-CF-141` `data` The app shares one coordinate reference between search with the tile pyramid. `src: Core features, services, rule 9`
- [ ] `C-CF-142` `capability` The app snaps a moving position to the most likely road segment. `src: Core features, services, rule 10`
- [ ] `C-CF-143` `capability` The app announces a maneuver ahead of time with a turn card. `src: Core features, services, rule 10`
- [ ] `C-CF-144` `capability` The app produces a new route from the current position after leaving the route. `src: Core features, services, rule 11`
- [ ] `C-CF-145` `constraint` The app strands no guidance mid-maneuver on a brief position gap. `src: Core features, services, rule 11`
- [ ] `C-CF-146` `data` The app returns the same segment speeds to a traffic read with the traffic-aware profile. `src: Core features, data products, rule 1`
- [ ] `C-CF-147` `constraint` The app returns no individual trace from a movement read. `src: Core features, data products, rule 2`
- [ ] `C-CF-148` `capability` The app returns administrative areas joinable by a shared geographic key. `src: Core features, data products, rule 3`
- [ ] `C-CF-149` `capability` The app renders a data product as a data-driven layer. `src: Core features, data products, rule 4`

## C-UF User flow

- [ ] `C-UF-01` `contract` The app serves a home page at the root address. `src: User flow, route table`
- [ ] `C-UF-02` `contract` The app serves the electric-vehicle page at `/ev`. `src: User flow, route table`
- [ ] `C-UF-03` `contract` The app serves the tiling product page at `/mts`. `src: User flow, route table`
- [ ] `C-UF-04` `contract` The app serves the Japanese home at `/ja`. `src: User flow, route table`
- [ ] `C-UF-05` `contract` The app requires an author session for every address under `/studio`. `src: User flow, route table`
- [ ] `C-UF-06` `contract` The app serves open registration at `/signup`. `src: User flow, route table`
- [ ] `C-UF-07` `capability` The app sends an unauthenticated studio request to the sign-in page. `src: User flow, entry and redirects`
- [ ] `C-UF-08` `capability` The app returns a person to the requested studio address after a sign-in. `src: User flow, entry and redirects`
- [ ] `C-UF-09` `capability` The app stops the old bearer token working immediately on sign-out. `src: User flow, entry and redirects`
- [ ] `C-UF-10` `capability` The app leaves a style version unchanged when a token expires mid-edit. `src: User flow, entry and redirects`
- [ ] `C-UF-11` `constraint` The app refuses a reader asking for a studio address. `src: User flow, entry and redirects`
- [ ] `C-UF-12` `ui` The app names what would fill an empty list in every empty state. `src: User flow, states`
- [ ] `C-UF-13` `ui` The app renders a skeleton of rows as the tileset table loading state. `src: User flow, states`
- [ ] `C-UF-14` `ui` The app renders an error in place with a way back. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The app grounds every surface on a near-black neutral. `src: UI/UX notes, colour para`
- [ ] `C-UX-02` `ui` The app carries every interactive thing on one mid vivid blue. `src: UI/UX notes, colour para`
- [ ] `C-UX-03` `ui` The app runs one cool neutral ladder for hierarchy alone. `src: UI/UX notes, colour para`
- [ ] `C-UX-04` `ui` The app sets the default in-body link colour as a light vivid cyan. `src: UI/UX notes, colour para`
- [ ] `C-UX-05` `ui` The app runs one accent sweep from a light vivid indigo into the brand blue. `src: UI/UX notes, colour para`
- [ ] `C-UX-06` `ui` The app grades corner softness across five control families. `src: UI/UX notes, shape para`
- [ ] `C-UX-07` `ui` The app spends one cool-grey elevation twice. `src: UI/UX notes, shape para`
- [ ] `C-UX-08` `ui` The app sets every voice in one geometric sans. `src: UI/UX notes, type para`
- [ ] `C-UX-09` `ui` The app gives every control an unavailable appearance signalled by more than colour. `src: UI/UX notes, components para`
- [ ] `C-UX-10` `ui` The app leads every page with exactly one primary action. `src: UI/UX notes, primary action para`
- [ ] `C-UX-11` `ui` The app shares one house easing across every transition. `src: UI/UX notes, motion para`
- [ ] `C-UX-12` `ui` The app settles every continuous motion under a reduced-motion preference. `src: UI/UX notes, motion para`
- [ ] `C-UX-13` `constraint` The app meets WCAG AA contrast for body text against the dark ground. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-14` `constraint` The app reaches every control by keyboard navigation with a visible focus indicator. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-15` `ui` The app overflows nothing sideways at any viewport width. `src: UI/UX notes, responsive para`
- [ ] `C-UX-16` `ui` The app collapses the navigation centre into one toggle at tablet width. `src: UI/UX notes, responsive para`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app builds the server with Fastify. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The app builds the interface with Preact. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The app bundles the interface with Vite. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` The app pre-renders every marketing route at build time. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` The app stores rows in PostgreSQL. `src: Technical requirements para 1`
- [ ] `C-TR-06` `contract` The app reads the database address from `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-07` `contract` The app stores bytes in MinIO. `src: Technical requirements para 1`
- [ ] `C-TR-08` `contract` The app reads the object store address from `STORAGE_ENDPOINT`. `src: Technical requirements para 1`
- [ ] `C-TR-09` `contract` The app reads the bucket name from `STORAGE_BUCKET`. `src: Technical requirements para 1`
- [ ] `C-TR-10` `constraint` The app introduces no second database. `src: Technical requirements para 2`
- [ ] `C-TR-11` `contract` The app returns `200` from `GET /api/health` once ready. `src: Technical requirements para 3`
- [ ] `C-TR-12` `contract` The app carries a strict transport policy header on every response. `src: Technical requirements, headers para`
- [ ] `C-TR-13` `contract` The app carries a nosniff content-type policy header on every response. `src: Technical requirements, headers para`
- [ ] `C-TR-14` `constraint` The app writes no token secret into a log line. `src: Technical requirements, logging para`
- [ ] `C-TR-15` `constraint` The app writes no place coordinate into a log line. `src: Technical requirements, logging para`
- [ ] `C-TR-16` `capability` The app loads the studio only on the routes needing one. `src: Technical requirements, separation para`
- [ ] `C-TR-17` `capability` The app holds a frame budget of sixty frames a second during a pan. `src: Technical requirements, liveness list`
- [ ] `C-TR-18` `capability` The app leaves every unaffected tile served from cache after a source change. `src: Technical requirements, liveness list`
- [ ] `C-TR-19` `capability` The app accepts exactly one of two simultaneous operations on one path. `src: Technical requirements, concurrency para`
- [ ] `C-TR-20` `capability` The app creates no second stored object when one upload is sent twice. `src: Technical requirements, concurrency para`
- [ ] `C-TR-21` `capability` The app creates no second usage charge when one upload is sent twice. `src: Technical requirements, concurrency para`

## C-DM Data model

- [ ] `C-DM-01` `data` The app stores every timestamp in UTC. `src: Data model, opening line`
- [ ] `C-DM-02` `literal` The app accepts the password `deku-demo-pw-2026` at login for every seeded account. `src: Data model, seeded password para`
- [ ] `C-DM-03` `contract` The app writes each seeded account into `/app/USER_README.md`. `src: Data model, seeded password para`
- [ ] `C-DM-04` `data` The app keeps an account address unique. `src: Data model, account entity`
- [ ] `C-DM-05` `data` The app stores a token secret only as a hash. `src: Data model, token entity`
- [ ] `C-DM-06` `data` The app carries the owner membership on exactly one project member. `src: Data model, project member entity`
- [ ] `C-DM-07` `data` The app updates no style version after creation. `src: Data model, style version entity`
- [ ] `C-DM-08` `data` The app stores the value before a style operation. `src: Data model, style operation entity`
- [ ] `C-DM-09` `data` The app resolves identical bytes from one account to one upload row. `src: Data model, upload entity`
- [ ] `C-DM-10` `data` The app changes a tileset visibility only by an explicit publish. `src: Data model, tileset entity`
- [ ] `C-DM-11` `data` The app identifies a tile by its pyramid address within a tileset. `src: Data model, tile entity`
- [ ] `C-DM-12` `data` The app stores a road segment current speed apart from its base speed. `src: Data model, road segment entity`
- [ ] `C-DM-13` `data` The app appends a usage event rather than maintaining a counter. `src: Data model, usage event entity`
- [ ] `C-DM-14` `data` The app shares one coordinate reference system across the pyramid, the graph, the index. `src: Data model, coordinates para`
- [ ] `C-DM-15` `data` The app stores money in integer minor units. `src: Data model, coordinates para`
- [ ] `C-DM-16` `data` The app seeds one project named Harbor Basemap. `src: Data model, seed data para`
- [ ] `C-DM-17` `data` The app seeds one road graph over one named region. `src: Data model, seed data para`
- [ ] `C-DM-18` `data` The app duplicates no row when the process restarts. `src: Data model, seed data para`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The app opens a dropdown panel by growing one from collapsed height. `src: Front-end specification, chrome`
- [ ] `C-FE-02` `ui` The app renders footer column headings in the eyebrow treatment. `src: Front-end specification, chrome`
- [ ] `C-FE-03` `ui` The app draws every icon at one stroke thickness inheriting the surrounding text colour. `src: Front-end specification, iconography`
- [ ] `C-FE-04` `ui` The app draws the brand mark as a filled ring with a four-point compass star. `src: Front-end specification, iconography`
- [ ] `C-FE-05` `ui` The app draws the map marker as a teardrop with a filled inner dot. `src: Front-end specification, iconography`
- [ ] `C-FE-06` `ui` The app floats three control clusters over the map rather than beside one. `src: Front-end specification, live map`
- [ ] `C-FE-07` `ui` The app marks the active scene row by more than colour. `src: Front-end specification, live map`
- [ ] `C-FE-08` `ui` The app reflows the map control panels to edge sheets at a narrow width. `src: Front-end specification, live map`
- [ ] `C-FE-09` `ui` The app opens a creation dialogue over a dimmed page rather than navigating away. `src: Front-end specification, studio`
- [ ] `C-FE-10` `ui` The app returns a refused row to its previous value with a reason in place. `src: Front-end specification, studio`
- [ ] `C-FE-11` `ui` The app renders a history entry as one line carrying its actor. `src: Front-end specification, studio`
- [ ] `C-FE-12` `constraint` The app ships no binary asset. `src: Front-end specification, drawn asset system`
- [ ] `C-FE-13` `ui` The app composes the globe from primitives rather than a stored mesh. `src: Front-end specification, drawn asset system`
- [ ] `C-FE-14` `ui` The app generates a placeholder customer mark from a seed. `src: Front-end specification, drawn asset system`
- [ ] `C-FE-15` `ui` The app moves focus into a dialogue when one opens. `src: Front-end specification, announcements`
- [ ] `C-FE-16` `ui` The app returns focus to the opener when a dialogue closes. `src: Front-end specification, announcements`
- [ ] `C-FE-17` `ui` The app announces an operation committed by another member. `src: Front-end specification, announcements`
- [ ] `C-FE-18` `ui` The app binds map pan, zoom, rotate each to keys. `src: Front-end specification, announcements`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app serves one deployment with one set of accounts. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The app reads across no second account. `src: Constraints bullet 1`
- [ ] `C-CN-03` `constraint` The app calls no external service at runtime. `src: Constraints bullet 2`
- [ ] `C-CN-04` `constraint` The app claims no planetary coverage. `src: Constraints bullet 3`
- [ ] `C-CN-05` `constraint` The app stores no individual movement trace. `src: Constraints bullet 4`
- [ ] `C-CN-06` `constraint` The app takes no card. `src: Constraints bullet 5`
- [ ] `C-CN-07` `constraint` The app ships no font file. `src: Constraints bullet 6`
- [ ] `C-CN-08` `constraint` The app ships no 3D model file. `src: Constraints bullet 6`
- [ ] `C-CN-09` `constraint` The app shares no private tileset outside its account. `src: Constraints bullet 8`
- [ ] `C-CN-10` `constraint` The app stays responsive with the seeded region fully tiled. `src: Constraints bullet 9`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The app listens on container-internal port `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The app reads the outside port from `APP_PUBLIC_PORT`. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The app serves the HTTP API under the `/api` prefix on the same origin. `src: Deployment contract bullet 2`
- [ ] `C-DC-05` `contract` The app answers `GET /api/health` with `200` once ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual step. `src: Deployment contract bullet 4`
- [ ] `C-DC-07` `contract` The app writes login credentials to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-08` `contract` The app leaves a `.browser_screenshots/` directory empty at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `contract` The app leaves a `.downloads/` directory empty at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-10` `contract` The app serves a production build behind a static or preview server. `src: Deployment contract bullet 7`
- [ ] `C-DC-11` `contract` The app keeps the server running after the build session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-12` `contract` The app binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-13` `constraint` The app starts no copy of a named backing service. `src: Deployment contract bullet 10`
- [ ] `C-DC-14` `constraint` The app uses no persistent volume. `src: Deployment contract bullet 12`
- [ ] `C-DC-15` `contract` The app returns a top-level JSON array from a list endpoint. `src: Deployment contract, API shapes`
- [ ] `C-DC-16` `contract` The app rejects a rule-breaking request as a client error carrying a reason. `src: Deployment contract, API shapes`
- [ ] `C-DC-17` `constraint` The app returns no server error for a rule-breaking request. `src: Deployment contract, API shapes`
- [ ] `C-DC-18` `constraint` The app stores no tileset in an in-memory array. `src: Deployment contract, no mocks`
- [ ] `C-DC-19` `constraint` The app stores no record outside PostgreSQL. `src: Deployment contract, no mocks`
- [ ] `C-DC-20` `constraint` The app substitutes no stored image file for a produced tile. `src: Deployment contract, no mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `author@example.com` | seeded first author address | C-RL-17 | User roles, seeded accounts table |
| `author2@example.com` | seeded second author address | C-RL-18 | User roles, seeded accounts table |
| `reader@example.com` | seeded reader address | C-RL-19 | User roles, seeded accounts table |
| `BUILD with Geoform` | promo banner lockup | C-CF-16 | Core features, marketing rule 2 |
| `SUBSCRIBE` | newsletter footer badge | C-CF-22 | Core features, marketing rule 5 |
| `HIRING` | careers footer badge | C-CF-23 | Core features, marketing rule 5 |
| `Do more with maps & navigation` | home hero heading | C-CF-25 | Core features, marketing rule 7 |
| `Explore Geoform live` | live map band heading | C-CF-27 | Core features, marketing rule 8 |
| `Ready to get started?` | closing band heading | C-CF-35 | Core features, marketing rule 14 |
| `Geoform for EV` | electric-vehicle hero | C-CF-36 | Core features, marketing rule 15 |
| `Page Not Found` | not-found heading | C-CF-40 | Core features, marketing rule 17 |
| `Globe View` | first seeded scene | C-CF-51 | Core features, live map rule 2 |
| `Rotating 3D globe` | first seeded scene description | C-CF-51 | Core features, live map rule 2 |
| `Data Overlay (2D)` | fourth seeded scene | C-CF-52 | Core features, live map rule 2 |
| `Live seismic event heatmap` | fourth seeded scene description | C-CF-52 | Core features, live map rule 2 |
| `Dawn` | first lighting preset | C-CF-53 | Core features, live map rule 3 |
| `Day` | second lighting preset | C-CF-53 | Core features, live map rule 3 |
| `Dusk` | third lighting preset | C-CF-53 | Core features, live map rule 3 |
| `Night` | fourth lighting preset | C-CF-53 | Core features, live map rule 3 |
| `Default` | first colour theme | C-CF-54 | Core features, live map rule 3 |
| `Faded` | second colour theme | C-CF-54 | Core features, live map rule 3 |
| `uploads/{upload_id}/{sha256_of_bytes}.{ext}` | upload object key scheme | C-CF-86 | Core features, ingestion rule 2 |
| `queued` | first upload state | C-CF-93 | Core features, ingestion rule 4 |
| `processing` | second upload state | C-CF-93 | Core features, ingestion rule 4 |
| `complete` | third upload state | C-CF-93 | Core features, ingestion rule 4 |
| `failed` | fourth upload state | C-CF-93 | Core features, ingestion rule 4 |
| `driving` | first travel profile | C-CF-123 | Core features, services rule 1 |
| `walking` | second travel profile | C-CF-123 | Core features, services rule 1 |
| `cycling` | third travel profile | C-CF-123 | Core features, services rule 1 |
| `driving-traffic` | fourth travel profile | C-CF-123 | Core features, services rule 1 |
| `address` | first geocoding result type | C-CF-134 | Core features, services rule 5 |
| `place` | second geocoding result type | C-CF-134 | Core features, services rule 5 |
| `poi` | third geocoding result type | C-CF-134 | Core features, services rule 5 |
| `region` | fourth geocoding result type | C-CF-134 | Core features, services rule 5 |
| `deku-demo-pw-2026` | password for every seeded account | C-DM-02 | Data model, seeded password para |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the four remaining seeded scene names | C-CF-50 | two scenes are pinned by name; the rail carries more below the fold |
| the tiling recipe's attribute list | C-CF-97 | named as a recipe with no attribute set given |
| the seeded region's own name | C-DM-17 | named as one small region with no place name given |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 4 | 8 |
| User roles | 2 | 20 |
| Core features | 30 | 149 |
| User flow | 7 | 14 |
| UI/UX notes | 3 | 16 |
| Technical requirements | 8 | 21 |
| Data model | 3 | 18 |
| Front-end specification | 4 | 18 |
| Constraints | 1 | 10 |
| Deployment contract | 10 | 20 |
