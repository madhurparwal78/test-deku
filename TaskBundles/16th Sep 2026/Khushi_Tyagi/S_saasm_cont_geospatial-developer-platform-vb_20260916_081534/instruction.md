# Geoform

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser, grab the live map on the home
page and spin it, then sign up as a developer, upload a geospatial dataset, watch it process into
a private tileset, name that tileset as a source in a map style, and publish the style so it
reads back from a public address, without hitting an error page.

A different stranger must NOT be able to reach that tileset's tiles before it is published, by any
means: not without a token, not with another developer's token, and not by asking the object store
directly. The uploaded bytes must live in the MinIO bucket at the key scheme this brief pins; a
copy on the app's own filesystem does not count, and neither does a row that claims an upload
happened.

## Overview

Geoform is a location platform sold to developers by open sign-up. It is not one map application;
it is the set of parts other people assemble into their own maps, navigation and search. The
marketing site is the front door, and its centrepiece is a real interactive map running in the
page rather than a picture of one.

Three audiences meet here, and only two of them ever load this application. Visitors land on the
marketing pages, tour the live map, read the solution and company pages, and sign up; no account
is needed to look. Developers sign in, take a scoped token, design a map style in the browser
studio, upload their own geographic data into private tilesets, and call the location services
from their own applications, metered by use. End users, the drivers and shoppers inside the
downstream applications that render Geoform maps, never visit this site at all, and nothing in
this build serves them.

The product is deliberately two things at once: fast, indexable, mostly-static marketing pages,
and one rich interactive map surface embedded in them, over a set of backing services. Keep that
split. The marketing pages must read and rank without the map ever starting.

It deliberately is not several things. There is no real external map provider, no real geocoder,
no live traffic feed, no payment processor and no analytics endpoint. Every road graph, place
index, elevation field and traffic reading in this build is a seeded fixture over one small named
region: the shapes, the bounds and the error behaviour are real, the geography is not. No native
mobile or automotive application is built. No on-premise deployment, no conversational assistant
and no documentation site. It ships no binary asset at all.

The genuinely hard part is the publishing boundary: a dataset a developer uploads must really land
in the object store, must be readable by nobody until that developer publishes it, and must become
readable the moment they do, with the same answer at every door in the product.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `author` | A developer. Signs up without an invitation, owns an account, issues and revokes scoped tokens, creates projects and styles, uploads datasets, cuts them into private tilesets, edits a shared project, and publishes a style version. Reads their own private tilesets, their own projects, their own tokens and their own usage figures. | **Cannot** read another author's private tileset, project, token or usage by any path. **Cannot** publish on a project where their membership is `viewer`. **Cannot** read a token secret after the screen that created it. |
| `reader` | A visitor, signed in or not. Reads every marketing route, every published style and every public tileset's tiles. | **Cannot** read any private tileset, any project, any token, any usage figure or any upload. **Cannot** reach any `/studio` address. |

Project membership is a second dimension and is not the same as the role. Within one project an
author is `owner`, `editor` or `viewer`: an owner and an editor may commit style operations, only
an owner may publish, and a viewer's session is live and read-only.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `reader` session to any `author`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected
state unchanged.

Signup is open. Anyone may create an `author` account from the public sign-up form, and that is
the only way an account comes into being. The following accounts are seeded, and every one of them
signs in with the password `deku-demo-pw-2026`:

| Email | Role | What it holds |
|---|---|---|
| `author@example.com` | author | owner of the seeded project, one published style, one private tileset |
| `author2@example.com` | author | editor on that same project, and one private tileset of their own |
| `reader@example.com` | reader | owns nothing |

The two authors are the isolation boundary the whole product is measured against: each owns a
private tileset the other must never reach, and both edit one shared project, which is where the
conflict rule is observed.

## Core features

### Accounts, tokens and metering

1. Public sign-up creates an `author` account from an electronic mail address and a password, and
   signs the person in. A second sign-up with an address that already exists is refused and
   creates no second account.
2. A sign-in with the right address and the right password returns a bearer token. A sign-in with
   a wrong password is denied, and the response must not reveal whether the address exists.
3. An author creates a named access token with a scope list drawn from the services this brief
   names. The secret is shown exactly once, at creation. Every later read of that token returns
   its name, its scopes and its state, and never the secret again.
4. A token is refused on its next use after it is revoked. Revoking one token leaves every other
   token on the account working.
5. A token carries its scopes: a token scoped to reading tiles is refused when it is presented to
   the directions service, and the refusal names the missing scope.
6. Every billable action counts one usage event against the account and the token that made it:
   a tile served, a map load, a directions call, an isochrone, a matrix, a geocode, a search, and
   stored dataset bytes. The usage view totals them per service, and the totals a developer reads
   reconcile exactly with the actions they made.
7. Usage rolls up against a free-tier allowance. A call past the allowance is refused with a
   reason naming the service and the limit, and it counts nothing: a refused call must not be
   billed.
8. Rate limits and quotas per token protect the shared backend and are returned to the caller as
   clear, catchable limits naming what was exceeded, never as an opaque failure.

### The marketing site

1. The global chrome is three fixed pieces on every marketing page: a promo banner, the top
   navigation, and the footer.
2. The promo banner is a full-width strip above the navigation carrying `BUILD with Geoform`,
   `SEPTEMBER 15-17 | VIRTUAL` and a `Register` control, with a close control at its right. It is
   dismissible, and the dismissal survives a reload.
3. The top navigation carries the brand lockup, then five dropdown menus reading `Products`,
   `Solutions`, `Developers`, `Company` and `Resources`, then the flat links `Pricing` and
   `Contact us`. The right cluster is a language control reading `EN` with a globe glyph, a text
   `Log in`, and a filled `Sign up` control. Once signed in, `Sign up` and `Log in` are replaced
   by `Go to account`.
4. The footer carries the brand lockup, a utility column of `Sign up`, `Pricing`, `Support` and
   `Contact us`, then five link columns. PRODUCTS holds four subgroups: Maps with `Maps Overview`,
   `Geoform GL`, `Mobile Maps kit`, `Studio`, `Static Maps` and `Geoform Tiling Service`; Search
   with `Search Overview`, `Search Box`, `Geocoding` and `Address Autofill`; Navigation with
   `Navigation Overview`, `Navigation for Automotive`, `Navigation for Mobile`,
   `Geoform Assistant`, `Matrix`, `Geoform for EV` and `ADAS kit`; and Data with `Data Overview`,
   `Traffic Data` and `Movement Data`.
5. SOLUTIONS lists `Automotive`, `Business Intelligence`, `On-Demand Logistics`, `Weather`,
   `Telecommunications`, `Outdoors`, `Retail`, `Real Estate`, `Travel` and `Drones & Robots`.
   DEVELOPERS lists `Documentation`, `Quickstart`, `Troubleshooting`, `Platform`, `Status` and
   `Support`. RESOURCES lists `Newsletter` carrying a `SUBSCRIBE` badge, `Customer Showcases`,
   `Blog` and `Webinars`. COMPANY lists `Who we are`, `What we do`, `What we value`, `Newsroom`,
   `Careers` carrying a `HIRING` badge, `Sustainability` and `Nonprofit support`.
6. The home page is a long dark scroll: the hero, the live map, a stack of product rails, a
   customer-story carousel, and a closing partnership band, in that order.
7. The hero reads `Do more with maps & navigation` over the lead `Geoform is the location platform
   of choice for developers, automakers, and innovators`, with a filled `Get started for free`
   control and an outline `Contact us` control. The heading arrives letter by letter as the reader
   reaches it.
8. The live map band reads `Explore Geoform live` with the sub-line `Tour a sample of Geoform
   features in an interactive Geoform GL web map.` and a `View Geoform gallery ->` link.
9. The product rails alternate text and visual, each a heading, a paragraph and a visual, each
   linking into a product. Their headings are pinned: a map-thumbnail row under a `Geoform Maps ->`
   link; `Optimize guidance with customized navigation`; `Efficiently process and host custom
   geospatial data`; `Generate insights with advanced location data offerings`; and
    `Flexibility and control you can trust`.
10. The tiling rail carries the body `Simplify data architecture by transforming vector and raster
    datasets into private tilesets, hosted in the cloud and streamlined for fast in-app
    performance. Or use Geoform Atlas for on-premise or firewalled applications.` The data rail
    carries `Enhance features and analysis with premium datasets for global boundaries, live and
    typical traffic speeds, and privacy forward movement data.` The control rail carries `Create
    the map and location experiences that are best for your business without the limitations of
    other providers. Take advantage of modular services, usage-based pricing, and free tiers to
    experiment and build what you need, how you need. Rest easy knowing that Geoform prioritizes
    data privacy.`
11. The control rail's visual is a device exposing three panels: `Map Styles` with `Default`,
    `Dark` and `Satellite`; `Data Layers` with `Points of Interest`, `Traffic`, `Transit`,
    `Terrain` and `Bikeways`; and `Branding` with `Primary Color`, `Typography` and
    `UI Components`.
12. The customer band reads `Customer stories` over `The world's leading businesses, from startups
    to global enterprises, build with Geoform.` with an `Explore customer stories ->` link and a
    swipeable carousel of story cards, each a placeholder partner mark, a category tag such as
    `TRAVEL` or `UTILITIES`, and a headline. A strip of placeholder customer marks glides sideways
    continuously beside it.
13. The closing band reads `Benefit from our geospatial leadership and expertise to collaborate on
    how location can transform your business.` with a `Connect with Geoform ->` link.
14. Every non-home marketing page follows one template: a centred hero with a large heading, a
    one-line lead and a `Get started` plus `Contact us` pair; a secondary in-page navigation of
    jump links; a `TRUSTED BY THE INDUSTRY LEADERS` logo band; alternating feature bands; a
    product-grid band of cards each carrying `Learn more ->` and `Read the docs ->`; a `Resources`
    band of article cards; and a closing band reading `Ready to get started?` over `Create an
    account or talk to one of our experts.` with `Sign up for free` and `Contact us`.
15. The electric-vehicle page is that template filled in: hero `Geoform for EV` over `Delight EV
    drivers with an integrated navigation solution, from trip planning to paying for charging.`;
    jump links `Convenient`, `Personalized`, `Dynamic` and `Build`; feature headings `Optimize EV
    trip planning` with the body `Discover chargers and recommend stops and charging times.`,
    `Predict range accurately` with `Provide drivers with accurate trip range and estimates of
    remaining battery on arrival.`, `Integrate charging and payment`, and `Use data that is always
    fresh`; and product cards `EV Charge Finder`, `EV Routing`, `EV Playgrounds`, `Geoform Dash`
    and `Navigation Kit`.
16. The Japanese-locale home serves the same layout with Japanese copy, and the language control
    offers `English` and the Japanese label. Nothing in the layout may depend on Latin word
    lengths.
17. Any address that matches no route renders the product's own not-found page, reading
    `Page Not Found` over `The page you are looking for doesn't exist or has been moved`, inside
    the normal chrome, and answers as not found rather than as success.
18. A consent surface asks once about non-essential storage, reading `We care about your privacy`
    with the controls `Customize`, `Strictly necessary only`, `Accept all`, `Reject all` and
    `Submit preferences`. The answer survives a reload.
19. Every content image on every page carries alternative text describing what it shows, and an
    image that is purely decorative declares itself decorative rather than carrying an empty
    description. The map canvas carries a text alternative naming the scene it is showing.
20. A sitemap lists every public route, and a robots file points at it. A route absent from the
    sitemap, or a sitemap the robots file does not name, is a defect.
21. Every page view of a public route is recorded with its route and the time it happened, and an
    account owner can read those records back. No other role can.

### The live map surface

1. The home page embeds a real interactive map: the rendering engine on real tiles, driven live.
   It is not a video, not a still image and not a sequence of pre-rendered frames.
2. A scene rail on the left lists selectable demo scenes, each a title and a one-line description.
   The seeded scenes are pinned: `Globe View` described as `Rotating 3D globe`; `3D Basemap`
   described as `Buildings, landmarks, and trees`; `Markers` described as `Custom pins with
   popups`; `Data Overlay (2D)` described as `Live seismic event heatmap`; and `Wind Speed`.
3. A lighting panel on the right offers four presets, each an icon and a label: `Dawn`, `Day`,
   `Dusk` and `Night`. A colour-theme panel below it offers swatch presets including `Default` and
   `Faded`, each rendered as a row of coloured dots.
4. Selecting a scene re-frames the map and swaps the active data and the lighting together.
   Selecting a lighting preset or a colour theme mutates the live render in place. None of the
   three causes a reload or a refetch of tiles already loaded.
5. The globe scene renders the earth as a lit sphere against a starfield and rotates on its own
   until it is touched, then stops.
6. The map is directly manipulable, and each interaction updates the render continuously rather
   than in steps: drag to pan, wheel or pinch to zoom, and a secondary drag to rotate and tilt.
7. A pulsing marker shows the viewer's nominal position: a dot that sends out an expanding ripple
   which fades as it grows.

### The rendering engine

1. The engine draws vector tiles with the graphics hardware, so the view transforms every frame
   without refetching or re-rasterising.
2. The camera supports pitch and bearing, so the map is not only top-down: buildings extrude from
   their footprints and the globe renders as a lit sphere.
3. Elevation data drapes the styled surface over topography, so terrain has height, and the
   hillshade and sky respond to the active lighting preset.
4. Live overlay layers, the seismic heatmap and the wind field, are composited over the base each
   frame rather than replacing it.
5. Label placement, collision and fade are resolved every frame, so text stays legible and
   non-overlapping as the camera moves.
6. Where the graphics context is unavailable the engine falls back to a still rendered image of
   the current scene and says so. A blank canvas, a thrown error or an empty container is the
   failure this rule exists to prevent.
7. A style change repaints from tiles already loaded. Recolouring a layer, toggling a layer, or
   moving the light must not cause a tile request.

### The tile pipeline

1. The world is addressed as a quadtree: `z=0` is one tile, and each zoom step splits every tile
   into four, so level `z` holds `2^z` by `2^z` tiles.
2. A vector tile carries geometry and attributes rather than pixels, clipped to the tile bounds
   plus a small buffer so a feature crossing an edge still draws correctly. A raster tile carries
   imagery or elevation in the same address scheme.
3. A tile is produced on demand, per tile, from the seeded source data. The build never
   pre-renders the whole region eagerly.
4. Producing a tile selects the source features intersecting its bounds at the requested zoom,
   drops detail that would be invisible at that zoom, and simplifies geometry to the tile's grid,
   so a low-zoom tile is cheaper than a high-zoom one over the same ground.
5. Every zoom level shares one source and one processing definition. Zoom selects detail, never a
   different dataset.
6. A tile that has been produced once is served again without being recomputed, until it is
   marked dirty.
7. When source data changes, only the tiles whose bounds intersect the change, together with their
   parents and children in the pyramid, are marked dirty and re-cut. A change in one place must
   not dirty a tile elsewhere, and must not require reprocessing the whole region.
8. Live layers carry a shorter freshness than the base, so the base stays cached while the live
   layer refreshes.

### Data-driven styling

1. A style is a portable document, not code: it lists sources naming which tilesets feed the map,
   an ordered list of draw layers, the lighting preset, the elevation source, and the icon and
   label atlases.
2. A layer binds a source layer to a paint and layout rule. The layer kinds are fill, line,
   symbol, circle, fill-extrusion, heatmap, raster, hillshade and sky.
3. Paint and layout values are expressions evaluated per feature and per zoom, not constants. The
   expression system supports interpolation, conditionals, arithmetic and attribute lookup, so one
   rule styles thousands of features from their own attributes.
4. A road's width interpolates with zoom; a building's colour keys off its height attribute; a
   marker's size scales with a numeric attribute on the feature. Each of these must be expressible
   without writing a rule per feature.
5. The same style document renders identically wherever it is read. A style is data that travels,
   not behaviour bound to one client.
6. Styles are versioned. A published style is served by reference, so updating the published
   version updates every application reading it, with no change at the caller.

### Dataset ingestion and private tilesets

This is the centre of the product.

1. An author uploads a source dataset through the upload service, authenticated by their token.
   The accepted sources are points, lines and polygons with attributes, or a raster.
2. **The uploaded bytes live in the MinIO bucket and nowhere else.** The object key is
   `uploads/{upload_id}/{sha256_of_bytes}.{ext}`, so an upload of the file `harbor-berths.geojson`
   with digest beginning `9f2a` under upload `u-7fa2` lands at
   `uploads/u-7fa2/9f2a...d0.geojson`. Bytes on the application container's filesystem, bytes in a
   database column, or a row recording an upload that never reached the bucket are each a contract
   violation.
3. Validation runs before tiling. Geometry and attributes are checked, and an oversized or
   malformed source is rejected with an error naming what is wrong. A rejected upload stores no
   bytes and creates no tileset.
4. Ingestion is asynchronous with observable job state. The states are `queued`, `processing`,
   `complete` and `failed`, and the author can read the current state and any error at any time.
   A large upload must not block the request that started it.
5. Tiling cuts the source into the pyramid by a declarative recipe naming which attributes to
   keep, how to simplify per zoom, and the zoom at which each feature first appears.
6. **A tileset is private when it is created, and private means unreadable.** A request for a
   private tileset's tile is answered as not found when it carries no token, when it carries
   another author's token, and when it is made directly against the object store. It is answered
   with the tile only when it carries a token of the owning account carrying the tile-read scope.
7. Publishing a tileset is an explicit act that makes its tiles readable without a token.
   Unpublishing closes them again on the next request. A tileset that becomes readable through any
   route other than publishing is the single most serious failure in this product.
8. Re-uploading a new version of a dataset re-cuts only the tiles whose bounds the change touches
   and invalidates exactly those, so updating data is incremental rather than a full rebuild.
9. Re-uploading bytes identical to those already stored creates no second object and no second
   tileset: the digest in the key is what makes the second upload land on the first.
10. The same processed tileset serves the browser map, a static render and any caller, from one
    stored result.

### The collaborative studio

1. A project is the shared unit: one style plus the datasets it names. Members open it together
   as `owner`, `editor` or `viewer`.
2. An edit is a fine-grained operation on a path into the style tree, never a whole-file save.
   Changing a colour, adding a layer, moving the light and editing an expression are each one
   operation carrying the path it touched, the value before and the value after.
3. Two operations on different paths both land. Neither may displace the other, and both appear in
   the history.
4. Concurrency on one path is handled deterministically rather than by whoever arrives first.
   Two operations on the same path resolve so that: the later commit is the stored
   value, and the author whose value was replaced is told so in their own session rather than
   losing the edit silently. Both operations appear in the history with their actors.
5. A change one member commits appears on another member's open canvas within a second, attributed
   to whoever made it, with no reload. A member who reconnects after a break receives the
   operations they missed, in the order they happened, with nothing repeated and nothing skipped.
6. Each member's presence is visible to the others: their name, their cursor, and what they have
   selected. Presence and edits propagate to every open session with sub-second latency for a
   small team on one project.
7. The canvas is the live rendering engine, so a teammate's paint change repaints the shared map
   for everyone rather than merely changing a value in a panel.
8. Every version is retained and attributable, any earlier version is restorable, and restoring is
   itself a normal logged operation rather than an erasure.
9. Publishing is separate from editing: an owner publishes a named version, and that is what
   downstream applications read. A `viewer` attempting to publish is refused by the server. Work
   in progress is never visible to a reader.

### Location services

Each of these answers over the seeded fixtures. The bounds and the error behaviour are real.

1. Directions take an ordered list of waypoints and a travel profile of `driving`, `walking`,
   `cycling` or `driving-traffic`, and return the route geometry, the total distance, the total
   duration and step-by-step maneuvers each carrying an instruction. The traffic-aware profile
   weights segments by the seeded current speeds, so the same request against a congested seeded
   table and a clear one returns different durations.
2. An isochrone takes an origin and one or more time or distance budgets and returns the reachable
   area as one polygon per budget. The polygons are valid and non-self-intersecting, and a larger
   budget's polygon contains the smaller one's.
3. A matrix takes a set of origins and a set of destinations and returns the full table of
   durations and distances between every pair in one answer. A matrix cell and the equivalent
   directions call must agree, because both read the same graph.
4. Isochrone and matrix are bounded: a stated maximum budget, a stated maximum origin count and a
   stated maximum origin-by-destination size. A request past a bound is refused with a reason
   naming the bound, rather than being truncated silently.
5. Forward geocoding turns text into ranked, typed results carrying coordinates and context. The
   types are `address`, `place`, `poi` and `region`, and a caller may filter by type.
6. Reverse geocoding turns coordinates into the nearest addressable place.
7. Search returns per-keystroke suggestions ranked by a blend of textual match, feature importance
   and distance from a bias point, biased to the current view, so a nearby match outranks a distant
   one with a better textual score. Address autofill completes a full structured address from a
   partial one.
8. A place added to a private dataset is findable by that account immediately, and is not findable
   by any other account.
9. Search shares the coordinate reference the tile pyramid uses, so a result drops a pin exactly
   where the map draws it.
10. The guidance loop snaps a moving position to the most likely road segment, tracks progress
    along the active route, computes distance and time to the next maneuver and to arrival, and
    announces the maneuver ahead of time with a turn card carrying the maneuver arrow, the
    distance, the road name and lane guidance. It surfaces current speed and the speed limit.
11. Leaving the route produces a new route from the current position without a scolding message
    and without stopping guidance. A brief gap in position updates must not strand guidance
    mid-maneuver.

### Data products

1. Traffic data reads return live and typical speeds per road segment, the same weights the
   traffic-aware profile uses, so a route and a traffic read cannot disagree.
2. Movement data reads return aggregated, anonymised measures over areas: counts and speeds, never
   an individual trace. This is a property of what is stored, not a setting that can be turned off.
3. Boundary data reads return administrative areas a caller can join their own data to by a shared
   geographic key.
4. Every data product renders as an ordinary data-driven layer through the same style and
   expression system the rest of the map uses.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | home: hero, the live map, product rails, customer stories, closing band | public |
| `/ev` | the electric-vehicle solution page, the worked example of the template | public |
| `/v2` | a campaign landing variant on the same template | public |
| `/mts` | the tiling-service product page | public |
| `/g/d` | a gated developer demo surface | public |
| `/dei` | a company values page | public |
| `/esg` | a sustainability page | public |
| `/ja` | the Japanese-locale home | public |
| `/blog` | the editorial index | public |
| `/pricing` | plans and the free tier | public |
| `/contact` | the contact form | public |
| `/signup`, `/login` | open registration and sign-in | public |
| `/studio` | the project list | author |
| `/studio/p/{project}` | the editing canvas | author |
| `/studio/p/{project}/history` | version history and restore | author |
| `/studio/tilesets` | the tileset table | author |
| `/studio/tilesets/{tileset}` | one tileset, its recipe and its visibility | author |
| `/studio/uploads/{upload}` | one upload and its job state | author |
| `/studio/tokens` | the token table | author |
| `/studio/usage` | usage per service against the free tier | author |
| `/studio/account` | the account and its plan | author |
| anything else | the product's own not-found page | public |

**Entry and redirects.** An unauthenticated request for any `/studio` address lands on `/login`
and returns to the address that was asked for once the sign-in succeeds. Sign-up at `/signup` is
open, creates an `author` account and lands on `/studio`. Signing out returns to `/` and the old
bearer token stops working immediately. A bearer token that expires part way through a style edit
leaves the style version exactly as it was and returns the person to `/login`. A `reader` asking
for a `/studio` address is refused rather than shown the page with its controls disabled. A
request for a private tileset without the owning account's token is answered as not found.

**Journeys.**

1. Open `/`. Read the hero, grab the map and spin the globe, select the `3D Basemap` scene, select
   the `Night` lighting preset, select the `Faded` colour theme, and watch each change repaint
   with no reload and no new tile request.
2. Sign up at `/signup` with a fresh address. Land in `/studio`, create a token with a tile-read
   scope, copy the secret from the one screen that shows it, then reload the token table and find
   the secret is no longer readable.
3. Open `/studio/tilesets` as `author@example.com`, open the upload dialogue, send a seeded
   dataset, and watch the job move `queued` to `processing` to `complete`. Find the bytes in the
   MinIO bucket under `uploads/`, and the new tileset in the table marked private.
4. Ask for a tile of that new tileset three ways: with no token, with `author2@example.com`'s
   token, and with the owner's token. The first two are answered as not found; the third returns
   the tile.
5. Open the project, name the new tileset as a source, edit a paint value and watch the canvas
   repaint from loaded tiles, then publish the version. Read the published style back from its
   public address with no session at all.
6. Sign in as both authors side by side on `Harbor Basemap`. One edits the water colour while the
   other edits the road width: both land and both appear in the history. Both then edit the water
   colour at once: one commit is stored, the other author is told their value was replaced, and
   the history carries both operations with their actors.
7. Ask for directions between two seeded points and read the distance, the duration and the
   maneuvers; ask for an isochrone at three budgets and read three nested polygons; ask for a
   matrix and read the full grid; type three letters into search and read ranked typed suggestions
   with the nearby match first.

**States.** Every list has an empty state that names what would fill it and offers the action that
would: a studio with no projects, a tileset table with no tilesets, a token table with no tokens.
Every page has a loading state, and the tileset table's is a skeleton of rows rather than a spinner
over the whole screen. An error renders in place with a way back and never replaces the application
with a stack trace. A map that cannot obtain a graphics context renders a still image of the
current scene and says so. A project whose style version is missing says so rather than failing.

## UI/UX notes

A developer arriving should understand within one screen that the map on the page is the real
product running, and that the tools to build one like it are one sign-up away. This is an
operational product with one permitted showpiece: the marketing pages are a calm developer-tool
surface rather than a poster, and the live map is the one place the product performs, because the
performance is the claim.

Two stances govern every judgement, and a competing product could rationally hold either opposite.
**One blue over a palette**: a single hue family carries everything interactive, and a second
saturated family never appears in the chrome. **A dark canvas over a light one**: the ground is
near-black and white text is the figure, which is what makes this read as a tool rather than a
brochure.

The ground is a near-black neutral, not a grey. One mid, vivid blue is the brand and carries every
interactive thing: links, focus, the primary action, accents. It appears nowhere that is not
interactive or an accent. Between ground and brand runs one long cool neutral ladder of roughly a
dozen steps, from near-white through pale fills and hairlines down to a deep cool neutral used for
control fills, and its only job is hierarchy: secondary text, dividers, disabled states. A second
grey family competing with it is the failure. The blue is itself a ten-step ramp, palest wash through pale tint to
near-black foot: the mid step is the action colour, one step darker is its pressed state, and the
deep steps anchor the two signature gradients, a horizontal deep-to-bright action wash and a
vertical sky-to-ink band. Two colours sit outside that discipline on purpose and nowhere else: the
default in-body link colour is a light, vivid cyan distinct from the brand blue, and one accent
sweep runs from a light, vivid indigo into the brand blue. The exact shades are yours, so long as
the relationships hold.

Corners are graded rather than uniform, and the ladder is part of the identity: barely softened on
utility chips, a small consistent radius on the dominant control surfaces, one step softer on
cards, a distinctly softer radius on the grouped nav call-to-action cluster, and a full pill
on buttons and the sign-up control. Nothing is square and nothing but a pill is fully round.
Elevation is one cool-grey shadow used twice, a deeper and longer version under a dropdown panel
and a shallower one under smaller floating panels; it reads cool rather than neutral, which is
what stops the dark ground looking muddy, and nothing else in the product lifts.

Type is one geometric sans in four weights with no second family. Body copy is the dominant size
and everything else is positioned against it: navigation labels, chips and buttons sit a step
below at a heavier weight on a tight line; lead paragraphs are body size at the heavier weight;
secondary body and captions sit smaller on a looser line; subheads sit well above body; and
eyebrow and badge text is the smallest thing in the product, heavier and generously letterspaced.
Display headings run on a fluid scale sized against the viewport rather than fixed, from the
subhead step up to a large display step.

Every control states its states. A button, a menu trigger, a chip and a map control each have a
resting, a pointed-at, a pressed, a focused and an unavailable appearance, and unavailable is never
signalled by colour alone. A pointed-at control cross-fades its text and its border from the deep
cool neutral to the brand blue rather than snapping. Escape closes any overlay, and a destructive
action asks first and names what it is about to affect.

Each page leads with exactly one primary action, visually distinct from every secondary one:
`Get started for free` on the home page, `Get started` on a solution page, the New control in the
studio. Two controls wearing the primary treatment on one screen is the failure.

One house easing governs the motion: a strong ease-out that decelerates late, so movement leaves
quickly and arrives slowly. Three transition families sit under it, and every transition in the
product belongs to one: colour transitions are the most common and run at a middling speed,
background fills transition fastest so a press feels immediate, and border colours follow the
colour timing, while every transform uses the house easing at a slower step. Six named animation
moments, each a runtime animation rather than a still state, carry the product: a spinner, the expanding ripple from
the position dot on the live map, a rotating busy indicator on the map, an attention pulse that
dips opacity and returns, a progress bar that fills toward but never reaches full, and a carousel
preloader. Two motions run continuously on the marketing pages, a customer-mark strip gliding
sideways at a constant speed and a soft shimmer on an icon, and one scroll-driven reveal brings the
hero heading in letter by letter. Under a reduced-motion preference the strip stops, the shimmer
settles, the letter reveal resolves at once and the ripple stops pulsing.

Accessibility is a floor, not a preference. Contrast meets WCAG AA for body text against the dark
ground and for the brand blue against every surface it sits on, and the blue never sets small
secondary body text. Keyboard navigation reaches every control with a visible focus indicator that
is not carried by colour alone, and the map surface is fully operable that way. Icon-only controls
carry text alternatives: the language globe, the menu carets, the close cross, the map controls.
The consent surface is fully labelled. A high-contrast preference is honoured alongside the
reduced-motion one.

The layout is responsive across five widths and holds at every size between them, not only at the
two it was drawn for. Above tablet the navigation is a horizontal bar; at and below it the centre
collapses into one toggle opening a stacked menu, with the sign-up control kept in reach. The
promo banner wraps and keeps its close control. On the home page the hero steps down the fluid
scale, the live map fills the width with its control panels reflowing to sheets at the edges, and
the product rails stack the visual under the text. On a solution page the feature bands go single
column, the product grid reflows to one card wide, and the jump navigation collapses. Nothing
overflows sideways at any width, and every navigation target stays reachable.

What this must not look like: a light consumer marketing page; a page where the blue is used
decoratively rather than for action; a poster where the working interface belongs; or a build
where the live map is a picture.

## Technical requirements

Build the server with **Fastify** on Node and the interface with **Preact** bundled by **Vite**.
The browser receives an application shell and fetches its data as JSON from the API, which is
served on the same origin under the `/api` prefix. The marketing routes are pre-rendered at build
time so the first response for each carries its real markup and its real copy, and they must read
completely with the map never starting. Data lives in **PostgreSQL**, reached at `DATABASE_URL`.
Uploaded bytes, produced tiles and rendered plates live in **MinIO**, reached at
`STORAGE_ENDPOINT` with the bucket named by `STORAGE_BUCKET` and the credentials
`STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. The app's own address and port are read from
`APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode a host or a port; read every one of them
from the environment. Both backing services are already running and must not be downloaded,
installed or started.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing services
available in this environment are PostgreSQL and MinIO, and reaching for anything else is a
contract violation.

`GET /api/health` returns `200` once the app is ready to serve.

Every response carries the standard security headers, including a strict transport policy and a
nosniff content-type policy. A response that omits them is a defect even when its body is correct.

Logs are structured lines carrying identifiers only. No log line may contain a token secret, an
uploaded byte, a place coordinate, an account address or a style document. A log line carrying the
contents of an upload is a defect even when the upload is seeded fixture data.

Three separations are observable from outside and none may be worked around. The marketing pages
answer completely without the map client loading at all. The map client and the studio load only
on the routes that need them, so a reader who never opens the studio never pays for it. The
location services answer independently of one another, so a bounded refusal from one leaves the
others answering.

Liveness and performance are stated as outcomes rather than as techniques:

- A style operation one member commits appears on another member's open canvas within a second.
- A member who reconnects receives the operations they missed, in order, with nothing repeated and
  nothing skipped.
- A tile produced once is served again without being recomputed, until a source change marks it
  dirty.
- A source change marks dirty only the tiles whose bounds it intersects, with their parents and
  children, and leaves every other tile served from cache.
- The rendering engine holds a frame budget of sixty frames a second while panning, zooming,
  rotating and spinning the globe. The goal is smoothness: panning and spinning must feel like a
  game rather than a slideshow, with no blank tile snapping into place.
- The marketing pages paint before the map finishes starting.
- An isochrone, a matrix and a search each answer inside their stated bound, and a request past a
  bound is refused with a reason rather than truncated.

Two behaviours must hold when requests arrive at the same instant, and both are stated as outcomes
rather than as techniques. When two members commit an operation on the same path at the same
moment, exactly one is stored; the other receives a conflict response naming the version it was
composed against, and the store never ends up holding a blend of the two. When the same upload is
sent twice, whether because a client retried or a member double-submitted, the second arrival must
not create a second stored object, a second tileset or a second usage charge.

## Data model

Thirteen entities. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**account.** Electronic mail address, password hash, role, plan tier, free-tier allowance. The
address is unique. Signup is open, so an account is created by the public form rather than seeded
only.

**token.** Its account, a name, a scope list, the hash of its secret, created-at and revoked-at.
The secret is shown once at creation and stored only as a hash, so no read path can return it
again. A revoked token is refused on its next use.

**project.** Its account, a name, its members, and the style version currently published. Exactly
one member carries `owner`.

**project member.** The project, the account, and the membership of `owner`, `editor` or `viewer`.
A viewer commits no operation.

**style version.** Its project, a version number, the style document, the author, a published flag
and published-at. Versions are append-only: nothing in the product edits or deletes one. Derived
rather than stored: whether a version is the current published one, which is read from the
project.

**style operation.** Its style version, the path into the style tree it touched, the value before,
the value after, the actor, the version it was composed against, and the time. This is the unit of
editing; there is no whole-document save.

**upload.** Its account, the original filename, the byte size, the digest of the bytes, the object
key, the state of `queued`, `processing`, `complete` or `failed`, and the error when it failed. The
digest and the account together identify an upload, so identical bytes sent twice by one account
resolve to one row.

**tileset.** Its account, its upload, a name, the tiling recipe, a visibility of `private` or
`public`, and the minimum and maximum zoom. Visibility is `private` at creation and changes only by
an explicit publish or unpublish.

**tile.** Its tileset, its `z`, `x` and `y`, the object key, the source version it was cut from,
and whether it is dirty. The pyramid address identifies it within its tileset.

**place.** The seeded index: a name, a kind of `address`, `place`, `poi` or `region`, coordinates,
and context naming the region it sits in.

**road segment.** The seeded graph: two endpoints, a length, a base speed and a current speed. The
current speed is what makes the traffic-aware profile differ from the plain driving one.

**usage event.** Its account, its token, the service, a count and the time. Append-only. Every
billable action writes one, and the usage view is the sum of them rather than a separately
maintained counter.

**page view.** The route and the time. An account owner reads these back; nobody else does.

Coordinates are decimal degrees in one reference system shared by the tile pyramid, the road graph
and the place index, so a search result, a route vertex and a drawn tile all agree about where a
point is. Money is stored in integer minor units in `usd`.

**Seed data.** One project named `Harbor Basemap`, owned by `author@example.com` with
`author2@example.com` as `editor`, carrying one published style version that names the seeded base
tileset as a source. Two private tilesets, one owned by each author, each cut from its own seeded
upload whose bytes are in the bucket. One seeded road graph and one seeded place index over one
small named region, with one seeded traffic table over the same segments. One seeded elevation
field. Three page views. Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual detail that will not fit inside `## UI/UX notes`. Everything here
is description rather than measurement: where the source material recorded an exact value, the
requirement is the relationship or the character it produced, and the value itself is yours.

### The chrome, in detail

The promo banner is a full-width band in the brand blue above everything, carrying an event lockup,
a date line and a pill control, with a close cross at the far right that lifts from partly faded to
full on approach. Dismissing it removes the band and the navigation sits at the very top from then
on.

The navigation bar is the near-black ground with the brand lockup at the left. The five dropdown
triggers each carry a small downward chevron and open a panel beneath on the cool-grey elevation,
growing from collapsed to full height rather than appearing at once. The two flat links carry no
chevron. The right cluster reads as one group: a language control with a globe glyph and a locale
list, a plain text sign-in link, and the filled pill that is the only primary action on the bar.

The footer is the same near-black ground. The brand lockup and a four-item utility column sit
above five link columns. Column headings are the eyebrow treatment, smallest and letterspaced;
links sit at body size and brighten toward the brand blue on approach. Two links carry small
badges beside them rather than after them.

### Iconography

Every icon is a line drawing at one stroke weight, inheriting the text colour around it, drawn in
code rather than loaded. The brand mark is a filled ring with a four-point compass star punched
through it, set beside the wordmark. The language control uses a globe: an outer circle, two
horizontal latitude chords and an elliptical meridian. The dropdown chevron is a single downward
wedge. The product glyphs are a paper-plane arrow with a small sparkle for location and telemetry,
a meridian-lined world for maps, and a guiding hand for directions. The map marker is a teardrop
roughly half again as tall as it is wide, with a filled inner dot, tinted from the palette.

### The live map surface, in detail

The structure of the surface is one wide panel with three floating control clusters over it rather
than beside it, and every interaction below acts on the live render rather than on a picture of it.
The scene rail sits at the left as a vertical list, each row a title with a one-line description
beneath in the secondary neutral; the active row is marked by more than colour. The lighting panel
sits at the right as four rows, each an icon and a label. The colour-theme panel sits below it,
each preset a row of coloured dots that previews the palette it applies. All three float on the
shallower of the two elevations. At a narrow width they reflow to sheets pinned to the edges of
the map rather than shrinking in place.

### The studio, in detail

The project list, the tileset table, the token table and the usage view are tables, because that is
what they are: a header row, rows that stay put as the eye scans, and one action per row at the
right. Creating anything opens a centred dialogue over a dimmed page rather than navigating away.
An edit applies to the row at once and reconciles when the commit answers; where a commit is
refused, the row returns to its previous value and says why in place rather than in a corner.

The editing canvas is the rendering engine at full size with the style tree beside it. A member's
presence is a small named marker in their own colour; a selection is outlined in that same colour.
The history is a list of operations newest first, each one line: actor, the path touched, from what
to what, and how long ago.

### The drawn asset system

This is a zero-asset build. No binary asset ships with this application, and the substitution guide
below is the whole of it: every illustration is produced by code.

- Map tiles are produced by the pipeline. Where a placeholder is needed before the pipeline
  answers, tiles are drawn in code: a near-black land fill, a deep cool neutral water fill, thin
  mid cool neutral roads from the seeded data, and a faint tile-address label, and the placeholder
  says that it is one.
- The hero visual is a looping colour wash in the palette, seeded so it is stable between runs.
  There is no video file.
- The globe and the city meshes are composed from primitives: a sphere for the globe, extruded
  footprints for buildings.
- The elevation source is a seeded layered-noise height field.
- Icons are the inline geometry described above; label glyphs render from the fallback font stack
  at run time.
- Customer marks and product screenshots are generated placeholder cards keyed by a seed, in the
  neutral ladder. Never a real partner mark.
- Type uses a fallback stack already present on the device; no font file is downloaded.
- Where a grain texture is wanted it is an inline generated noise vector, desaturated and carried
  as a data address rather than a file.

### Responsive behaviour, stated by width

Five widths: phone, large phone, tablet, desktop and wide. Above tablet the navigation is a
horizontal bar. At and below tablet the centre links collapse into a single toggle whose closed
state is three short stacked bars with softened ends, and the sign-up control stays beside it. On a
phone the home page becomes one column: the rails stack the visual under the text, the live map
fills the width with its panels as edge sheets, and the customer carousel becomes a single swipeable
card. A solution page goes single column with its product grid one card wide and its jump
navigation collapsed. The Japanese locale serves the same layout with different script, so no
measure may assume Latin word lengths.

### Announcements and focus

Focus is never lost: opening a dialogue moves focus into it, closing one returns focus to whatever
opened it, and the editing canvas keeps focus inside an open editor until it commits or abandons.
The map surface is reachable and drivable from the keyboard, with pan, zoom and rotate each bound
to keys and each announced. Three things are announced as they happen rather than only drawn: an
operation committed by another member, an upload job changing state, and a bounded service refusing
a request.

## Constraints

- One deployment, one set of accounts. There is no organisation above the account and no
  cross-account read of any kind.
- No real third-party service. No external map provider, no external geocoder, no live traffic
  feed, no payment processor, no analytics endpoint, and no outbound call to any of them at
  runtime.
- Every road graph, place index, elevation field and traffic reading is a seeded fixture over one
  small named region. The build makes no claim to planetary coverage.
- Movement data is aggregated at rest. The build stores no individual trace, so there is no setting
  that could expose one.
- Billing is simulated. No card is taken, no invoice is issued and no money moves.
- No binary asset ships: no image file, no font file, no video, no audio, no icon sprite, no 3D
  model.
- No native application, no offline mode, and no service other than the two named.
- No comments, no ratings, no direct messaging between accounts, and no public sharing of a
  private tileset outside its account.
- The application stays responsive with the seeded region fully tiled and with a dataset upload in
  progress.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password` | the created account and `access_token` |
| `POST /api/auth/login` | `email`, `password` | `access_token`, `role` |
| `POST /api/auth/logout` | none | the session ended |
| `GET /api/tokens` | none | a top-level JSON array of tokens with `name`, `scopes`, `revoked_at`, never a secret |
| `POST /api/tokens` | `name`, `scopes` | the token with its `secret`, shown this once only |
| `DELETE /api/tokens/{token}` | none | the revoked token |
| `POST /api/uploads` | the file, `name` | the upload with `id`, `state`, `sha256`, `object_key` |
| `GET /api/uploads/{upload}` | none | the upload with its current `state` and any `error` |
| `GET /api/tilesets` | none | a top-level JSON array of the caller's tilesets with `visibility` |
| `POST /api/tilesets` | `upload`, `name`, `recipe` | the created tileset, `visibility` `private` |
| `POST /api/tilesets/{tileset}/publish` | none | the tileset, `visibility` `public` |
| `POST /api/tilesets/{tileset}/unpublish` | none | the tileset, `visibility` `private` |
| `GET /api/tiles/{tileset}/{z}/{x}/{y}` | none | the tile, or not found when the caller may not read it |
| `GET /api/styles/{style}` | none | the published style document |
| `GET /api/projects` | none | a top-level JSON array of the caller's projects |
| `GET /api/projects/{project}` | none | the project, its members and its current style version |
| `POST /api/projects/{project}/operations` | `path`, `before`, `after`, `base_version` | the stored operation, or a conflict naming the current version |
| `GET /api/projects/{project}/operations` | `after` | a top-level JSON array of operations in order |
| `POST /api/projects/{project}/publish` | `version` | the published style version |
| `GET /api/projects/{project}/versions` | none | a top-level JSON array of versions with their authors |
| `POST /api/projects/{project}/restore` | `version` | the restored version, recorded as an operation |
| `GET /api/directions/{profile}` | `waypoints` | `geometry`, `distance`, `duration`, `maneuvers` |
| `GET /api/isochrone` | `origin`, `budgets` | a top-level JSON array of one polygon per budget |
| `GET /api/matrix` | `origins`, `destinations` | `durations`, `distances` |
| `GET /api/geocode` | `q`, `types` | a top-level JSON array of ranked typed results |
| `GET /api/reverse` | `lon`, `lat` | the nearest addressable place |
| `GET /api/search` | `q`, `proximity` | a top-level JSON array of ranked suggestions |
| `GET /api/traffic` | `segments` | live and typical speeds per segment |
| `GET /api/movement` | `area` | aggregated counts and speeds, never a trace |
| `GET /api/boundaries` | `kind` | administrative areas |
| `GET /api/usage` | none | totals per service against the free-tier allowance |
| `GET /api/page-views` | none | a top-level JSON array of route and time, for an owner |

Every endpoint except `POST /api/auth/signup`, `POST /api/auth/login`, `GET /api/health`, the
published style and tile reads, and the marketing routes requires a bearer token or an account
token. A request that breaks a rule in this brief is rejected as a client error carrying a reason,
never as a server error and never as a silent success. A list endpoint returns a top-level JSON
array.

### No mocks

Two services back this application and the data has to actually be in them.

The following are contract violations however convincing the interface looks: an in-memory array of
tilesets or projects that disappears when the process restarts; a JSON or SQLite file on the app's
own disk standing in for the database; uploaded bytes written to the application container's
filesystem instead of the bucket; a tileset row recording an upload whose bytes never reached the
bucket; a private tileset made unreachable only by hiding its row while the tile address still
answers; a screenshot or a recorded video standing in for the live map; and a stored image file
standing in for a produced tile.

The named provider is the fact - the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.

## Definition of done

A visitor can open the home page, grab the live map and spin it, and switch its scene, lighting and
colour theme without the page reloading. A developer can sign up, take a scoped token, upload a
geospatial dataset, watch it process into a private tileset whose bytes are in the bucket, and name
it as a source in a style. That tileset answers as not found to everyone but its owner until the
owner publishes it, and answers to anyone the moment they do. Two developers can edit one project
at once without either losing work silently, and the version one of them publishes is what every
downstream reader sees.
