# Constellation Drawing Canvas

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, sign in, join two catalogue stars into a glowing line, name the finished figure and publish a link that reopens that exact drawing, without hitting an error page. A different stranger, signed in as somebody else, must not be able to read a private sky's rendered image by any means: the rendered image must exist as a real object in the MinIO bucket, and a copy on the app container's own filesystem does not count.

## Overview

Constellation Drawing Canvas is a single-screen night sky that a stargazer draws on. The whole viewport is one dark drawing surface carrying a catalogue of ten thousand stars at their true equatorial positions, each sized by how bright it really is and tinted by how hot it really is. The stargazer clicks one star, then a second, and a glowing line in the currently chosen colour joins the two. Lines accumulate into a figure, the figure gets a name, and named figures accumulate into a personal collection. A finished sky can be published as a link that anybody can open.

The people who use it are hobby stargazers working alone. There is no team, no collaboration and no audience beyond whoever is handed a published link. Each stargazer sees only their own collection.

It deliberately is not a social product and not an observatory tool. There are no comments, no likes, no follows, no messaging, no telescope control, no ephemeris, no planets, no deep sky objects and no time travel: the sky is fixed at one epoch and does not move with the clock. There is no public gallery, no browsing of other stargazers' work and no discovery surface of any kind. A published link is the only way a sky ever leaves its owner.

The genuinely hard part is that a published sky is a frozen artifact rather than a live view: once published, what the link returns must never change again, even as the stargazer keeps drawing on the sky it came from.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Stargazer | Sign in; read the star catalogue; create, rename and delete their own skies; add and undo segments on their own skies; render and read their own skies; publish their own skies | **Cannot read, render, modify, publish or delete any sky owned by another stargazer.** **Cannot read another stargazer's rendered image, by its own route or by any other.** **Cannot list another stargazer's collection** |
| Visitor (not signed in) | Open a published link and read the frozen sky behind it | **Cannot read any sky that has not been published.** **Cannot list any collection.** **Cannot create, modify, render or publish anything** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a Visitor session to any Stargazer-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged. The same holds between two Stargazers: a request from one Stargazer's session for another Stargazer's sky is denied and changes nothing.

Signup is closed. Accounts exist only as seeded records. Two are seeded, both Stargazers:

| Email | Password |
|---|---|
| `stargazer@example.com` | `deku-demo-pw-2026` |
| `stargazer2@example.com` | `deku-demo-pw-2026` |

## Core features

### Sign in

1. A Stargazer signs in with email and password and receives a bearer token in `access_token`, which is sent on every later request.
2. Passwords are stored hashed, never in readable form.
3. A request carrying no token, or a token the server did not issue, is rejected as unauthorized and changes nothing.
4. There is no signup form and no password reset. An attempt to create an account is refused.
5. Signing out ends that session: the token it carried is refused from then on, and any other session of the same Stargazer keeps working.

### The star catalogue

1. The catalogue holds exactly `10000` stars and never changes. It is an immutable reference dataset and may be cached indefinitely: no endpoint creates, edits or deletes a star.
2. Every star carries a catalogue id, a right ascension in degrees, a declination in degrees, an apparent magnitude and a colour index.
3. Apparent magnitude runs the astronomical way round: a **smaller** magnitude is a **brighter** star. The brightest stars in this catalogue sit at magnitude `-1.50` and the faintest at `6.49`.
4. Star size on screen follows brightness, so a magnitude `-1.50` star is a visible bloom and a magnitude `6.49` star is a single soft point. Star tint follows a colour-index formula rather than a stored per-star colour, running from a mid, vivid blue at the hot end through a near-white core to a light, soft orange and then a soft red at the cool end.
5. Reading the catalogue is open to any signed-in Stargazer. It is not open to a Visitor.

### Finding the star under the pointer

1. A click on the sky is hit-tested against the catalogue and resolves to exactly one star, or to none at all. The hit test is generous enough to forgive a few pixels.
2. Resolution takes a sky position and an angular radius, and considers every catalogue star whose great-circle angular separation from that position is less than or equal to the radius.
3. Among those, the star that wins is the **brightest**, which is the one with the smallest apparent magnitude. It is not the closest. A dim star sitting exactly under the pointer loses to a brighter star elsewhere inside the radius.
4. When two candidates share the same magnitude, the one with the lower catalogue id wins.
5. When no star lies inside the radius, no star is resolved and nothing is selected.

### Drawing a constellation

1. A sky is a named figure owned by one Stargazer and drawn in one palette colour.
2. The first click of a pair marks a pending endpoint: that star brightens and pulses, and the hint line changes from its opening message to a connecting prompt. The second click draws a segment between the two stars, clears the pending state and plays one piano note. Clicking the pending star again, or pressing escape, cancels the pending state and plays nothing.
3. A segment stores the two catalogue star ids, never a screen position. The line is drawn from the live catalogue positions every frame, so it stays pinned to its two stars as the sky pans and zooms.
4. A segment whose `from_star_id` or `to_star_id` is not a catalogue id is refused as invalid, the offending field is named, and no segment is written.
5. A segment joining a star to itself is refused as invalid and no segment is written.
6. Editing a figure is limited to undo and clear. Undo removes the most recently added segment of that sky and nothing else. Undo on a sky with no segments is refused as invalid and changes nothing. Undos arriving at the same instant each remove a segment of their own, newest first: four simultaneous undos on a sky of six segments remove positions `6`, `5`, `4` and `3`, each reported once.
7. Clearing a sky asks first, through a confirmation that reads `Clear all constellations?` with a `Cancel` and a `Clear`. Cancel dismisses and changes nothing; Clear removes every segment of that sky.
8. Segments are ordered. The order they were added in is the order they are returned in and the order undo walks backwards through. Segments sent to one sky at the same instant are each written at a position of their own, so a sky's positions always run from `1` to its segment count with no gap and no repeat, and no request is refused or fails because another arrived with it.

### Naming and the collection

1. A sky is created from a slide-over panel that takes a name and a palette colour, and confirms with a toast.
2. A name is required, is trimmed of surrounding whitespace and must not be empty once trimmed. An empty or whitespace-only name is refused inline with the `name` field named in the message, and no sky is written.
3. A name longer than `80` characters is refused inline the same way, and no sky is written.
4. The collection lists that Stargazer's skies newest first, and nobody else's. Two skies created at the same moment are ordered by the larger identifier first, so the order is total and never depends on which row is read first.
5. A Stargazer whose collection is empty sees a stated empty state inviting them to start a figure, never a blank panel.

### The preset constellation layer

1. Behind the Stargazer's own work sits a faint layer of the real named asterisms, drawn in a near-white neutral at low opacity with the constellation name set beside each figure.
2. A toolbar control toggles this layer on and off. Its behaviour is a plain toggle that asks nothing first. When it is on, the official figures and their names are visible under the drawing; when it is off, the sky shows bare stars and the Stargazer's own lines only.

### Publishing a sky

1. Publishing takes the sky as it stands and stores a **frozen copy** of it: the sky name, the palette colour, the ordered list of segments as pairs of catalogue star ids, the view centre and zoom it was framed at, and the moment it was published.
2. Publishing returns a `share_token` that addresses the frozen copy at a short-link route, and a `manage_token` that is the only thing able to unpublish it.
3. **Both tokens are minted by the server.** A `share_token` or `manage_token` sent in the publish request body is ignored entirely: the tokens that come back are the server's own, they differ from anything the caller supplied, and a token the caller invented never addresses or manages anything.
4. Once stored, a frozen copy is never edited. Drawing another segment on the sky, renaming it, undoing a segment or clearing it leaves what the published link returns exactly as it was.
5. Publishing the same sky again mints a **new** `share_token` over the sky as it stands now. The earlier token keeps working and keeps returning the earlier drawing.
6. A publish request carries a caller-chosen `share_key`. Two publish requests that carry the same `share_key` describe one intended publish, not two.
7. Anybody may open a published link without signing in. A sky that has never been published has no link, and guessing a token that was never minted resolves to nothing.
8. The publish panel carries an unattended decoy field named `observer_note`. A request that arrives with `observer_note` filled in is refused and nothing is published. A session may also publish at most `5` times in quick succession: where the same form is submitted repeatedly in one burst, the sixth request is refused whatever it carries.

### Rendering a sky to an image

1. A sky renders to a scalable vector image of the current view with the drawing on it, and that image is stored as an object in the MinIO bucket.
2. The object key is `renders/{sky_id}/{revision}.svg`, where `revision` starts at `1` for a sky's first render and increases by one on each later render of that sky. For example the second render of sky `7` is stored at `renders/7/2.svg`. Renders of one sky requested at the same instant each take a revision of their own, so no two renders ever share a revision or a key.
3. **Renders are append-only.** A later render writes a new key and never replaces or removes an earlier one. Every render a sky has ever had remains readable at its own key.
4. The rendered image carries one line element per segment, in segment order, and one point element per star that any segment touches.
5. The stored object is the image. The app may not keep the bytes on its own filesystem or in its own database and serve those instead.
6. A rendered image is read back through the app, which resolves who is asking before it streams the bytes. The bucket is private and stays private.
7. A sky that has never been rendered has no object under its own key prefix, and asking for its latest render is refused as a client error rather than answered by generating an image on the spot.

### The sky itself

1. The sky fills the viewport, never scrolls, and opens centred on right ascension six hours, declination zero.
2. A live readout in the top right names the sky coordinate at the centre of the view. At first load it reads exactly `RA 06h 00m 00s   Dec -00° 00'`, with three spaces between the two halves. Right ascension is shown in hours, minutes and seconds; declination in signed degrees and arcminutes, and the sign is always written, including for zero.
3. The readout updates as the sky pans and settles into a quieter state when motion stops.
4. Reframing is a first-class move: a globe control flies the view to a named region and a map pin recentres on a located point, each as one slow deliberate glide rather than a cut.
4. Dragging pans the sky and the wheel or a pinch zooms it, easing to a stop rather than snapping. Zoom is clamped at both ends, so the field can neither be lost entirely nor magnified until one star fills the screen.
5. A one-line hint sits bottom centre and opens reading `Select two stars to connect them`.
6. Every content image in the product carries alternative text describing what it shows, and any image that is purely decorative declares itself decorative rather than carrying an empty description.
7. Every internal link on every route resolves to a real route of this product. There are no dead links.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/login` | Sign in | Public |
| `/` | The sky canvas with the collection beside it | Stargazer |
| `/skies/:sky_id` | One sky open on the canvas | Stargazer, owner only |
| `/c/:share_token` | A published sky, frozen | Public |

**Entry and redirects.** A Visitor who opens `/` or `/skies/:sky_id` is sent to `/login`. A Stargazer who signs in successfully lands on `/`. A Stargazer who opens `/skies/:sky_id` for a sky they do not own is denied and never shown its contents. Signing out returns to `/login` and the old token stops working. A token that has expired mid-action sends the Stargazer back to `/login` with the reason stated, and the action it was carrying is not performed. `/c/:share_token` is reachable by anyone at any time and never redirects to `/login`.

**Journeys.**

1. *Draw and publish.* Open `/login`, sign in as `stargazer@example.com`. The collection appears beside the sky with `Monoceros Arch` at the top. Open the slide-over, type `Summer Kite` and pick the green palette colour, confirm, and a toast reports the sky was created. Click a star, then a second star: a green line joins them and a note sounds. Publish it, copy the link, and open that link in a fresh session with nobody signed in: the same two stars are joined by the same green line.
2. *Publishing freezes.* With `Summer Kite` published, add a third segment to it. Open the published link again: it still shows the drawing as it was at publish time, not the new segment.
3. *Undo.* Open `Lepus Lantern`, which carries three segments. Undo once: the third segment is gone and two remain. Undo again: one remains.
4. *Another stargazer is shut out.* Sign in as `stargazer2@example.com`. The collection shows `Corvus Sketch` and nothing belonging to `stargazer@example.com`. Asking for `Lepus Lantern` directly is denied, and so is asking for its rendered image.
5. *Empty.* Open `The Kite`, which has no segments. The canvas states that the figure is empty and invites a first connection rather than showing a blank sky with no explanation.

**States.** The collection has an empty state. The catalogue has a loading state while the ten thousand stars arrive, and the sky is drawable before the last of them lands. Every refusal states what was wrong and names the field when a field was at fault. An error never leaves the canvas blank or the app unresponsive.

## UI/UX notes

The north star is that the sky is real and the drawing belongs to the person who made it: somebody arriving should feel they are looking at the actual night sky rather than a decorated background, and that the pen in their hand is made of starlight. The register is a **consumer creative canvas**, so atmosphere is welcome and the subject, the sky itself, is seen first and dominates everything.

The product is **dark committed**. There is no light mode and none is expected. The sky is the darkest thing on screen, running from a near-black neutral ground down to pure black, the absolute backdrop behind everything, and every other surface sits above it.

**The design system.** Two palettes, one type family, one shape scale and one motion vocabulary carry the whole product, and nothing outside that system is invented.

**Palette by role.** The star field runs a temperature ramp: a near-white neutral at the white-hot core of a bright star, falling through a mid, vivid blue for the hottest stars and a deep, soft blue and a deep, muted blue in the haze around them, out to full transparency at the rim. The cool end of the ramp is derived from each star's colour index rather than stored, running through a light, soft orange for the golden stars and on to a soft red for the coolest, so the field's warmth comes from the data. The drawing palette is eight fixed line colours and is the only saturated thing a Stargazer controls: a light, soft red; a light, soft orange; a near-white, soft amber; a light, soft green; a near-white, soft blue; a near-white, soft indigo; a near-white, soft magenta; and a plain near-white neutral. Each is soft and light enough to glow against the sky and distinct enough that two figures never read as one. Chrome text is a near-white neutral held well back from full strength, with a second, fainter step for secondary text and thin rules, and the faintest step of all reserved for hairline dividers and the preset constellation lines. Modal panels are a cool near-black, popovers a plainer near-black, and both sit over a scrim that dims the sky without hiding it. The exact values are yours, so long as the eight line colours stay mutually distinguishable against the sky and nothing in the chrome ever competes with a star for attention.

Colour is never the only signal. A figure carries a name as well as a colour, the pending endpoint pulses as well as brightens, and a refusal states its reason in words.

**Typography.** One family does the whole interface: `Roboto`, with its light cut and its condensed cut also in use. Give a normative fallback stack. The scale is exact: `19px` and `18px` at weight `300` carry the product title and the coordinate readout; `16px` at weight `400` carries buttons, modal copy and the hint line; `15px` and `14px` at weight `300` carry secondary chrome; `13.3333px` at weight `400` carries tooltips; `13px` at weight `400` carries the star information chip. Figures in the coordinate readout align, so the readout does not jitter as it counts.

**Shape and density.** The layout is **spacious** and edge-anchored: almost the whole screen is sky, and the chrome is a thin frame pinned to the four edges rather than a document that flows. Corners are gently rounded, with the colour dots as perfect circles, the modal box the softest corner in the product, the palette popup a shade tighter, and the star information chip and modal buttons tighter still. Nothing scrolls.

**Layout archetype.** A **sidebar-nav** collection list sits alongside the canvas as a **split detail-pane**: the collection on one side, the open sky filling the rest. The sidebar collapses so the sky can take the whole viewport, and collapsing it is never the only way to reach a sky. Creating a sky arrives as a **slide-over** panel rather than a route change, and the result is confirmed with a **toast**.

**Stacking.** The sky sits behind everything. The chrome floats above it, the colour popup above the chrome, and modals above everything else.

**Transitions.** Every transition in the product comes from one small set: a fast transform-and-border pair on the hovers and the colour dots, a short opacity fade on chrome text and tooltips, a longer opacity fade on the hint line, and one slow paired transition carrying the reframing glide. **Motion character is `eased`:** things arriving settle with a decisive ease-out and things leaving accelerate away with an ease-in, and exactly two curves are used across the whole product, one for each direction. Motion is small and functional: there are no scroll animations, because there is no scroll. The named moments are these, and each must be built: a toolbar button brightens and grows slightly when pointed at while its tooltip fades up; the studio wordmark grows very slightly when pointed at; a modal arrives by growing the last fraction up to full size while it fades in, so it reads as placed rather than thrown; the hint line crossfades between messages; the coordinate readout fades into its settled state when panning stops; the view glides into a named region in one slow, deliberate move when the globe control is used, slow enough to keep the stargazer oriented; and a new segment draws in while its two endpoints pulse. The pressed state of a toolbar control reads the same size as its hover state, so pressing does not resize it a second time. The product fully respects a reduced-motion preference: under it the region glide and the modal arrival become plain fades, and the fade is kept rather than removed.

**Iconography and components.** Every control has a resting, pointed-at, pressed, focused and unavailable state, and unavailable is never signalled by colour alone. Escape closes the colour popup and every modal. Destructive actions confirm first. Icon-only controls carry a label a screen reader can read that matches the tooltip a pointer reveals. The toolbar is a row of single-stroke line drawings on a square box, rounded caps and joins, drawn in code rather than loaded: an active-colour dot filled with the current palette colour, a small open zig-zag for the preset-asterism toggle, a globe for flying to a named region, a waste bin for clearing, a serif capital T for naming, a map pin for recentring, and an upward arrow rising out of an open tray for sharing. A downward arrow into the same tray sits inside the share sheet rather than on the toolbar.

**Accessibility floors,** which do not vary: body text and its background meet WCAG AA contrast, touch targets are comfortably sized, every control is reachable and operable from the keyboard with a visible focus ring, icon-only controls carry labels, and meaning is never carried by colour alone. Drawing works without a pointer: arrow keys move a focus cursor between neighbouring catalogue stars, enter confirms an endpoint, and the same two-step selection completes a segment with the same note. Drawing also works without audio: the line and the hint carry the confirmation, and sound is a reward rather than the signal. The product is fully screen-reader operable, and the coordinate readout and the hint are announced when they change materially.

**Responsive.** The surface fills the viewport at every width and never scrolls sideways. On a wide screen the full frame shows: wordmark, title and readout across the top, hint and the whole tool row along the bottom, collection beside the canvas. Narrower, the arrangement holds and the sky simply gets a narrower window. At the narrowest, the title gives way so the wordmark and the readout can share the top, the tool row and hint stay along the bottom within thumb reach, and the collection becomes a panel that opens over the sky. Hit tests widen for touch, because a fingertip is less precise than a cursor. Nothing overflows sideways at any width and every navigation target stays reachable.

What it must not look like: a page dominated by one hue family with no second signal, a marketing composition where the working canvas belongs, or decoration standing in for the sky. Atmosphere over ornament, and the subject over the frame.

## Front-end specification

**Module and component architecture.** The front end divides into these responsibilities. The division is a map of the product, not a file layout, and the names are the product's own vocabulary:

| Module | Responsibility |
|---|---|
| `SkyCanvas` | owns the drawing surface, the render loop and the star point cloud |
| `Catalogue` | loads and indexes the star data, exposing position, magnitude and colour lookups |
| `Projection` | the screen-to-sky and sky-to-screen mapping, both directions |
| `Camera` | pan, zoom, clamping, eased settling and the reframing glide |
| `Picker` | hit-tests a pointer position against the catalogue and resolves the winning star |
| `Constellations` | the segment data model: add, undo, clear, recolour, name and serialise |
| `LineLayer` | renders the Stargazer's segments and the preset asterism layer into the surface |
| `Palette` | the eight colours, the popup and the active-colour state |
| `AudioEngine` | the synthesised sampled-piano voice, its reverb and the note pools |
| `Chrome` | the framed interface, driven by application state |
| `Modals` | the clear confirmation and the share sheet |
| `ShareClient` | serialises a drawing and posts it, and fetches a shared one back |
| `Coordinates` | formats the readout |

A single application store holds the camera centre and zoom, the active palette colour, the pending endpoint, the ordered skies and their segments, the preset layer's visibility and which modal is open. The render loop reads that store every frame and interactions write to it. Pointer events enter `Picker`, which resolves a star and either sets the pending endpoint or completes a segment in `Constellations`, which in turn triggers `AudioEngine` and `LineLayer`.

**The chrome.** A studio wordmark sits top left, set in the interface face, uppercase and solid. The product title sits top centre in the light weight. The live coordinate readout sits top right in the light weight. The one-line hint sits bottom centre, carrying a soft white glow. The tool row sits bottom right. All of it renders above the sky and below the popup layer.

**The coordinate readout.** The format is fixed: the literal `RA `, then hours as two digits followed by `h`, a space, minutes as two digits followed by `m`, a space, seconds as two digits followed by `s`, then three spaces, then the literal `Dec `, then a sign that is always written, degrees as two digits followed by the degree sign, a space, and arcminutes as two digits followed by a prime. Right ascension in hours is the centre's right ascension in degrees divided by fifteen. The opening centre, right ascension `90.000` degrees and declination `0.000` degrees, therefore reads `RA 06h 00m 00s   Dec -00° 00'`.

**Observed implementation, and what binds.** The reference product this brief descends from was observed using a WebGL point-cloud renderer for the field and a sampled piano voice for the audio engine. That observation is evidence of one way to satisfy these requirements and is not itself a requirement: what binds is the capability stated in each section here, built on the stack named in `## Technical requirements`. An implementation that meets every capability on a different renderer is correct.

**The star field.** One full-viewport hardware-accelerated surface carrying the whole catalogue in a single batched draw, with brightness and colour baked into the point data rather than one surface object per star. Each star is a soft radial sprite generated in code: a bright core falling through the blue ramp to full transparency at the rim, composited additively so overlapping haloes brighten rather than replace. The brightest handful carry short four-way spikes drawn as two thin crossed gradients. Size and glow radius scale with brightness. No star texture, no image file: the sprite is generated.

**Star colour from the catalogue.** The warm end of the ramp is not stored. Derive it from each star's colour index: a low index maps into the blue ramp above, and a high index runs through the warm tones toward a soft red, so the golds and corals in the field come from the data rather than from a picture.

**The projection.** The field is a gnomonic projection of the equatorial sphere onto the screen plane, centred on the view direction. Screen positions map to sky coordinates and back again, both ways, so a click finds the star under the pointer and the readout reports the coordinate at the centre of the view. Panning moves the centre in right ascension and declination.

**Segments.** Each segment is a thin line in the sky's palette colour, one to two device pixels wide, with a faint outer glow of the same colour so it reads against the field. Segments composite into the same surface as the stars, so a bright star sits visually on top of the lines meeting it. The endpoints are the true star positions, so a segment reprojects correctly under pan and zoom.

**The colour palette popup.** Tapping the active-colour dot opens a small dark panel above the chrome holding the eight colour dots. Each dot is a perfect circle. The active dot is marked as active, and selection is shown by that state rather than by a separate control. Choosing a colour sets the drawing colour, updates the toolbar dot and closes the popup. The chosen colour applies to every new sky until changed; skies already drawn keep the colour they were drawn in.

**Audio.** The audio engine plays one soft sampled piano note on every completed segment. The notes walk a consonant run, so a figure built line by line sounds like a rising or falling phrase rather than random pitches. Four runs are available and a new figure may reset to the start of one:

```
["C4","E4","G4","A4","C5","E5","G5","A5","G5","E5","C5","A4"]
["E4","G4","B4","E5"]
["C3","E3","G3","C4","E4","G4","C5","E5","G5","C6"]
["C6","G5","E5","C5","G4","E4","C4","G3","E3","C3"]
```

The piano is synthesised in code rather than loaded as recordings: a short enveloped tone per note with a bright attack decaying to a soft body, two slightly detuned voices for warmth, run through a generated reverberation so each note blooms and fades. Audio stays silent until the first user gesture and never blocks drawing while it loads.

**The preset asterism layer.** Thin near-white lines at low opacity join the catalogue stars of the classic named figures, with each constellation's name set beside it in the light weight. Orion, Canis Minor, Monoceros and Lepus are visible in the opening view.

**The star information chip.** Hovering or selecting a star can raise a small chip naming the star and showing its coordinate and brightness, set with a soft white glow, entering with a small upward move before settling.

**Naming.** The text control raises a naming field carrying the same soft white glow, so a finished figure can be titled. The name is stored with the sky and travels with it when it is published.

**Modal structure.** A modal is a cool near-black panel over a scrim that dims the sky. It arrives by growing the last fraction up to full size while fading in. Buttons inside it are tighter-cornered than the panel, with a distinct confirm variant. The clear confirmation reads `Clear all constellations?` with `Cancel` and `Clear`. The share sheet is the same box, titled `Share your Constellation`, presenting the link with a copy action and a download control that renders the current view to an image.

**Copy deck.** These strings are exact:

| Location | String |
|---|---|
| Title, top centre | `Constellation Drawing Canvas` |
| Coordinate readout, opening | `RA 06h 00m 00s   Dec -00° 00'` |
| Hint, opening | `Select two stars to connect them` |
| Clear modal prompt | `Clear all constellations?` |
| Clear modal, dismiss | `Cancel` |
| Clear modal, confirm | `Clear` |
| Share modal title | `Share your Constellation` |

**The zero-asset substitution guide.** Every asset the product might have loaded is substituted by a recipe rather than a file, and this is the whole of that guide: the star sprite is a generated radial gradient, per-star colour comes from the colour-index formula, the piano is synthesised, the toolbar glyphs are procedural, and the typography is a named family.

**No binary assets.** The product ships with no image, font file or audio file of its own. Stars, glow, spikes, toolbar icons and the piano are all generated from code and data. `Roboto` is named and loaded from a font service or self-hosted licensed files, its glyphs set in a near-white neutral; naming a family is not an asset dependency, so the product ships no font binary of its own.

## Technical requirements

The product is built in one dependency sequence: the drawing surface and the catalogue first, because everything hangs off them, then the chrome that orients the view, then selection and drawing, then colour and sound, then the preset layer and naming, then the modals, publishing and rendering, and finally the responsive, accessibility and performance passes. The frontend is **Angular**, served as a production build. The backend is **FastAPI** on Python. The rendering model is a **single-page application over a JSON API**: the browser receives an application shell on first paint and every screen after that is painted from JSON the API returns, so there is no server-rendered HTML page per route. Persistent state lives in **PostgreSQL**, reached through `DATABASE_URL`. Rendered images live in **MinIO**, reached through `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. The app reads its own address from `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode a host or a port. `GET /api/health` returns `200` once the app is ready. Authentication is email and password implemented by the app itself, issuing a bearer token; there is no external identity provider.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor: the only backing services available in this environment are PostgreSQL (`postgres`) and MinIO (`minio`), and reaching for anything else is a contract violation. Both are **already running** and reachable at the variables above. Do not download, install, compile or start a copy of either.

**Reading the catalogue at scale.** The catalogue is ten thousand rows and is never returned whole. Every paged read takes `limit=` to set how many rows come back, defaulting to `100` and capped at `500`, and a `limit=` outside `1` to `500` is refused as invalid. Every paged read also takes an **opaque cursor** in `cursor`, which the client only ever echoes back from a previous response and never constructs or decodes. A page response carries `items`, `next_cursor`, `has_more` and `total_count`, and the opaque cursor in `next_cursor` is the only legal way to ask for the page after it. `total_count` is the number of rows matching the request's filter across the whole catalogue, not the number on this page and not the size of the catalogue. `has_more` is true only when a further page genuinely exists, so the last page of an exactly-filled result reports `has_more` false and a `next_cursor` of null. Walking from the first page to the last at a fixed `limit=` must yield every matching row exactly once, with no row repeated and none skipped, and that must stay true when rows are added to the collection between two page requests.

**Filtering happens before paging.** `GET /api/stars` takes `max_magnitude`, and a request carrying it matches only stars whose apparent magnitude is less than or equal to that value. The filter selects across the whole catalogue and the page is then taken from what matched, so a filtered page is as full as an unfiltered one whenever enough rows match. `GET /api/skies` is paged on the same `limit=` and opaque cursor contract and returns only the calling Stargazer's own skies, newest first.

**Publishing under simultaneous requests and on replay.** A publish request carries a `share_key` chosen by the caller. When two publish requests carrying the same `share_key` arrive at the same moment, **exactly one** of them creates a published sky; the other is rejected with a `409` conflict response, or, when it is handled only after the winner has finished, it is answered as a replay carrying the winner's `share_token`. Either way it creates nothing. When an identical publish request is replayed later, it returns the **same** `share_token` as the first and **must not create a second** published record: after any number of replays exactly one published sky exists for that `share_key`. A conflict response leaves nothing behind, so the rejected caller creates no partial publish and no orphaned token. Application-level checks alone are not enough to hold any of this. Choose any mechanism.

**Tokens are the server's.** A `share_token` or a `manage_token` present in a publish request body is ignored and never becomes the stored token.

**Renders are append-only.** Writing render `revision` `n` for a sky leaves every render from `1` to `n-1` byte-for-byte as it was, at its own key in the bucket.

**Performance.** The first paint of the sky must arrive quickly and the field must hold a smooth, steady frame rate while panning and zooming the full ten-thousand-star catalogue on a three-year-old laptop and a mid-range phone. The catalogue is large, so it loads in the background without blocking the first interaction, and the sky is drawable before every audio voice is ready. Drawing a segment, opening the palette and reframing all respond immediately. The techniques that get there are the app's own choice, but two properties are required rather than optional: the whole field is drawn in a single batched draw with brightness and colour baked into the point data rather than one surface object per star, and **memory stays bounded no matter how many segments are drawn**, so segments are light data batched into one layer rather than a surface object per line. Responsive tuning, accessibility and performance passes are part of the product, not an afterthought.

Every business-rule violation is rejected as a client error with a reason, never as a server error and never as a silent success. A failed operation leaves no partial state.

## Data model

Five tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

### `stargazers`

`id`, `email` (unique), `password_hash`, `created_at`.

### `stars`

`star_id` (text, unique, the catalogue id), `ra_deg`, `dec_deg`, `magnitude`, `colour_index`. Reference data, seeded once and never written again.

The catalogue is generated, not supplied as a file. For each whole number `i` from `1` to `10000`, exactly one row exists:

| Field | Value |
|---|---|
| `star_id` | the letters `HD` followed by `i` written with leading zeros to five digits, so `i` of `1` gives `HD00001` and `i` of `10000` gives `HD10000` |
| `ra_deg` | `((i * 137508) mod 360000) / 1000` |
| `dec_deg` | `(((i * 73900) mod 180000) - 90000) / 1000` |
| `magnitude` | `(((i * 7) mod 800) - 150) / 100` |
| `colour_index` | `(((i * 11) mod 220) - 30) / 100` |

Every division above is exact, so `ra_deg` and `dec_deg` carry three decimal places and `magnitude` and `colour_index` carry two. Worked rows, which must match exactly:

| `i` | `star_id` | `ra_deg` | `dec_deg` | `magnitude` | `colour_index` |
|---|---|---|---|---|---|
| 1 | `HD00001` | `137.508` | `-16.100` | `-1.43` | `-0.19` |
| 7 | `HD00007` | `242.556` | `67.300` | `-1.01` | `0.47` |
| 42 | `HD00042` | `15.336` | `-46.200` | `1.44` | `-0.08` |
| 800 | `HD00800` | `206.400` | `-10.000` | `-1.50` | `-0.30` |
| 10000 | `HD10000` | `240.000` | `10.000` | `2.50` | `-0.30` |

Counts that follow from the rule and must hold: `10000` stars in total, of which `641` have a magnitude of `-1.00` or less, `4412` have a magnitude of `2.00` or less and `6905` have a magnitude of `4.00` or less. The smallest magnitude present is `-1.50` and the largest is `6.49`.

### `skies`

`id`, `owner_id` (a `stargazers` row), `name`, `line_colour` (one of `r`, `o`, `y`, `g`, `b`, `p`, `k`, `w`), `created_at`. The `segment_count` a collection row reports is **derived on read** from the sky's segments rather than stored, so undoing a segment lowers it without a second write. A sky belongs to exactly one Stargazer for its whole life; ownership never transfers.

### `segments`

`id`, `sky_id`, `from_star_id`, `to_star_id`, `position` (the order the segment was added in, starting at `1`), `created_at`. Both star fields hold a `stars.star_id` and must exist in the catalogue. `position` is unique within a sky.

### `published_skies`

`id`, `sky_id`, `share_key`, `share_token` (unique), `manage_token` (unique), `payload_version` (always `1`), `sky_name`, `line_colour`, `payload` (the frozen ordered segment list as pairs of catalogue star ids), `view_ra_deg`, `view_dec_deg`, `view_zoom`, `published_at`. `share_key` is unique per sky. A row here is written once and never updated: republishing writes a new row rather than changing an old one, so a sky may own several, each with its own token and its own frozen payload.

### Seed data

Two Stargazers, `stargazer@example.com` and `stargazer2@example.com`.

`stargazer@example.com` owns four skies. Newest first, the collection reads:

| Sky | `line_colour` | Segments, in order |
|---|---|---|
| `Monoceros Arch` | `b` | `HD00042` to `HD00800`, then `HD00800` to `HD02400` |
| `Lepus Lantern` | `y` | `HD00800` to `HD01600`, then `HD01600` to `HD02400`, then `HD02400` to `HD03200` |
| `The Kite` | `g` | none |
| `Winter Hexagon` | `w` | `HD00007` to `HD00042` |

`stargazer2@example.com` owns one sky, `Corvus Sketch`, colour `p`, carrying one segment from `HD03200` to `HD00001`.

`Lepus Lantern` is seeded already published, at `share_token` `lantern-7f3a91`, with `share_key` `seed-lantern`, framed at view centre right ascension `90.000`, declination `0.000`, zoom `1.0`, and a frozen payload carrying its three segments in order. No other sky is seeded published.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- One Stargazer at a time. There is no sharing of a sky between accounts, no team, no organisation and no tenancy beyond ownership.
- No signup, no password reset, no email of any kind, and no outbound message.
- No comments, likes, follows, messaging or notifications.
- No public gallery and no way to discover another Stargazer's work. A published link is the only route out.
- No planets, no deep sky objects, no time-varying sky and no telescope control. The catalogue is fixed reference data.
- No file upload from the Stargazer. The only object the product writes to the bucket is a render it generated itself.
- No external network calls at runtime. No third-party analytics, font-hosting fallback that fails closed, map service or audio CDN is required for the product to work, and no analytics measurement identifier is configured: the default is none.
- No native application and no offline mode.
- The app must stay responsive with the full ten-thousand-star catalogue loaded and a sky carrying at least two hundred segments.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.**

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/login` | `{"email", "password"}` | `{"access_token"}` |
| `POST /api/auth/logout` | none | `{"signed_out"}` |
| `GET /api/health` | none | `{"status"}` |
| `GET /api/stars` | `limit`, `cursor`, `max_magnitude` | `{"items": [{"star_id", "ra_deg", "dec_deg", "magnitude", "colour_index"}], "next_cursor", "has_more", "total_count"}` |
| `GET /api/sky/pick` | `ra_deg`, `dec_deg`, `radius_deg` | `{"star": {"star_id", "ra_deg", "dec_deg", "magnitude", "colour_index"}}`, and `{"star": null}` when nothing is inside the radius |
| `GET /api/skies` | `limit`, `cursor` | `{"items": [{"id", "name", "line_colour", "segment_count", "created_at"}], "next_cursor", "has_more", "total_count"}` |
| `POST /api/skies` | `{"name", "line_colour"}` | `{"id", "name", "line_colour", "segment_count", "created_at"}` |
| `GET /api/skies/{sky_id}` | none | `{"id", "name", "line_colour", "segments": [{"position", "from_star_id", "to_star_id"}]}` |
| `POST /api/skies/{sky_id}/segments` | `{"from_star_id", "to_star_id"}` | `{"position", "from_star_id", "to_star_id"}` |
| `DELETE /api/skies/{sky_id}/segments/last` | none | `{"removed_position"}` |
| `POST /api/skies/{sky_id}/renders` | none | `{"revision", "object_key"}` |
| `GET /api/skies/{sky_id}/renders/latest` | none | the stored image bytes, content type `image/svg+xml`; refused as a client error when the sky has never been rendered |
| `POST /api/skies/{sky_id}/publish` | `{"share_key", "view_ra_deg", "view_dec_deg", "view_zoom", "observer_note"}` | `{"share_token", "manage_token", "published_at"}` |
| `GET /api/shares/{share_token}` | none | `{"payload_version", "sky_name", "line_colour", "segments": [{"position", "from_star_id", "to_star_id"}], "view_ra_deg", "view_dec_deg", "view_zoom", "published_at"}` |

List endpoints return their rows under `items`. A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as a client error, never as a `5xx` and never as a silent success. Bearer auth is required on everything except `POST /api/auth/login`, `GET /api/health` and `GET /api/shares/{share_token}`.

**No mocks.** The rendered image must exist as a real object in the MinIO bucket at its own key. An in-memory dictionary of renders, a table of image bytes in PostgreSQL, a file written to the app container's filesystem, or a route that generates the image afresh on every read and stores nothing, are all violations however correct the picture looks. MinIO is the fact: the app's own interface and its own tables can only reflect what lives in the bucket, never substitute for it.

## Definition of done

A stargazer signs in, joins two catalogue stars into a glowing line, names the figure and publishes a link that a stranger can open without an account and see that exact drawing. Drawing more on a sky after publishing never changes what an existing link returns. Another stargazer signed in to their own account can reach none of it, and a rendered sky exists as a real object in the bucket rather than as bytes the app keeps to itself.
