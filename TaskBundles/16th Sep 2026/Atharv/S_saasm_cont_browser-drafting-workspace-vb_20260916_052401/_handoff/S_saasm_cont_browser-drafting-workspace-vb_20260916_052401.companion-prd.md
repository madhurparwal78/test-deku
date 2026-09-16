# Product requirements: browser drafting workspace

A professional 2D drafting and design application that runs entirely in a web
browser with no install, opens and edits industry standard CAD drawings at
desktop fidelity, and lets several people edit the same drawing at once. Every
literal in this document was measured from a capture of the reference
application and frozen in an evidence ledger; nothing here is recalled or
invented. Where the reference hid its editor behind a sign in wall, this
document says so plainly and specifies the capability instead of a measured
pixel (Section 30).

## 0. How to use this document

This is one document written for two readers at once. Every numbered section
first says exactly what to build, in the terms an engineer or a building agent
needs, and then closes with a short block, marked **In plain language**, that
says what a user would actually see and feel. The two halves describe the same
thing a few lines apart, under the same number.

Every name written inside angle brackets, like `<BRAND>` or `<SITE_ORIGIN>`, is
a blank you fill in with your own. The reference application belongs to a real
company; this specification is deliberately brand neutral so it can be rebuilt
for any drafting product without carrying the original's name, mark, font or
third party service names. Choose your own values and keep them consistent.

The application being specified is a browser based drawing editor for technical
professionals. There is no page to scroll: after sign in it is a single
full screen workspace built around an infinite drawing canvas, with a top bar, a
left tool group, floating panels for properties and layers, a command input, a
status bar, and a side assistant panel. The one thing an unauthenticated visitor
ever sees is the loading screen (Section 7); everything past it requires an
account, so most of this document specifies capabilities and marks what could
not be measured directly.

### 0.1 Placeholder token table

| Token | Meaning | Suggested placeholder |
|---|---|---|
| `<BRAND>` | the product name in running text | Draftline |
| `<BRAND_MARK>` | the square app badge glyph | a two letter monogram |
| `<SITE_ORIGIN>` | production web origin | your own domain |
| `<APP_HOST>` | application and sync host | your own host |
| `<ASSET_HOST>` | font and media delivery host | your own media host |
| `<BRAND_FONT>` | the proprietary interface sans | your licensed sans, with a fallback |
| `<ASSISTANT_NAME>` | the in app assistant | Draft Assistant |
| `<IDENTITY_PROVIDER>` | the account and single sign on system | your own identity service |
| `<STORAGE_PROVIDER>` | the cloud document store | your own document store |
| `<GA_MEASUREMENT_ID>` | analytics id, if used | your own id |

> **In plain language.** This page is written twice over, on purpose. Each part
> starts with the exact recipe a builder follows, then finishes with a plain
> description of what you would see on the finished product, told in the same
> order and under the same numbers. Anything in pointy brackets is a
> fill in the blank for your own company, so nothing here carries someone else's
> name or logo. The product itself is not a website you scroll: once you sign
> in, it is one full screen drawing workspace, the kind a draftsperson uses to
> make technical drawings. The only thing a visitor without an account ever sees
> is the loading screen, so much of this document describes what the tool must be
> able to do rather than a picture we could take of it.

## 1. Product overview

The product is a browser delivered professional drafting editor. It opens, edits
and saves industry standard CAD drawing files with fidelity to a desktop
drafting application, so a drawing opened here is the same file a colleague opens
on a workstation. It requires no installation and runs on any modern browser,
which is its whole reason to exist: it reaches machines and people a desktop
install cannot.

The reference titled its page "`<BRAND>` Web App, Online CAD Editor and Viewer"
(Section 28). It is one node of a family, a desktop application, this web
application, and a mobile application, that share the same cloud stored drawing.

The application is built as a heavy client. The capture pulled 312 script files
totalling roughly 836 megabytes of transferred JavaScript, alongside a compiled
geometry and rendering core (Section 3.1). This is not a marketing page with a
few widgets; it is an application shell that downloads a drawing engine and runs
it in the browser.

The character of the build is precision and fidelity, not decoration. The state
changing actions are numerous and are the point: create and edit geometry, edit
properties, save versions, and co edit with others (Sections 10, 11, 18, 19).

> **In plain language.** This is a full drawing program that happens to live in a
> web browser instead of being installed on your computer. It opens the same
> professional drawing files a desktop drafting tool uses, so nothing is lost
> passing a file between a colleague on a desktop and you in a browser. It is a
> serious piece of software: opening it quietly downloads a large drawing engine
> and runs it right there in the tab. The point of the product is doing real
> work, drawing, changing, measuring and saving, not reading a page.

## 2. Information architecture

### 2.1 Routes

The reference is a single application served at one origin. The capture reached
six paths, and every one of them rendered the same loading screen (Section 7),
because the editor behind them requires a signed in account:

| Path | Meaning | Notes |
|---|---|---|
| `/` | application entry | loads the shell, then the loading screen |
| `/2/` | a versioned or numbered entry | same loading screen |
| `/gc` | a short entry alias | same loading screen |
| `/v1` | an entry variant | same loading screen |
| `/v2` | an entry variant | same loading screen |
| `/412` | a short numeric entry | same loading screen |

These are application entry points, not separate content pages. All six also
appeared only as strings inside the script bundles, which is consistent with a
single page application that routes internally after load rather than serving
distinct documents (Section 30).

### 2.2 In application surfaces

Past the loading screen the application is not a set of pages but a set of
surfaces inside one screen: the drawing canvas (Section 8), the top bar and tool
groups (Section 5), floating panels for layers and properties (Sections 12, 5),
the command input and status bar (Section 9), the layout and paper space tabs
(Section 16), and the assistant panel (Section 20). Navigation between them is by
panel and tab, never by page load.

> **In plain language.** There is really only one screen. The six web addresses
> the crawler tried all lead to the same loading screen, because everything real
> is locked behind signing in. Once you are in, you do not move between pages;
> you work in one window that holds the drawing in the middle and a set of tools,
> panels and tabs arranged around it, and you switch tools and panels rather than
> loading new pages.

## 3. Design system

### 3.1 Observed implementation (informational)

None of the following are requirements. They are what the reference used,
recorded with the evidence tier that produced each. Rebuild the capabilities
(Sections 8 through 21) in whatever stack the implementation prefers.

| Signal | Value | Tier |
|---|---|---|
| view layer | React, runtime version literal `18.3.1` | tier 2 and 3 |
| component kit | a Material component library, `Mui` and emotion `css-` class families | tier 5 and 6 |
| styling | styled components, `sc-` class family | tier 6 |
| 3D and rendering | three.js, identifiers `BufferGeometry` and `RenderPass` post processing | tier 6 |
| low level graphics | WebGL, shader source carrying `gl_Position` | tier 6, definitive |
| three.js age | bracketed by a deprecation string `will be removed in r184` | tier 7 |
| vector animation | Rive, identifier `rive-app` | tier 6 |
| motion helper | Framer Motion | tier 6 |
| line and text reveal | GSAP DrawSVG and SplitText | tier 6 |
| audio | Web Audio API, `AudioContext` | tier 6 |
| live channel | server sent event streams, 26 `text/event-stream` responses | tier 4 |
| source maps | present inline, base64 data source maps | tier 0, definitive |

Other version literals surviving minification, unattributed but recorded:
`1.9.1`, `3.10.1`, `3.8.1`, `8.4.38`, `0.22.0`, `1.0.0`, `0.46.0`, `11.0.28`,
`20.29.0`, `1.4.1`.

### 3.2 Colour

Two colour worlds coexist and must not be confused. The first is the application
chrome: a light, near neutral interface. The second is the drawing colour index,
the saturated primaries a CAD entity is coloured by, which arrive as integer
literals in the drawing engine rather than as interface CSS.

Interface chrome, measured as computed colours, most used first:

| Role | Value | Uses |
|---|---|---|
| primary interface grey, icons and secondary text | `rgb(162, 166, 176)` | 288 |
| panel and surface near white | `rgb(245, 245, 245)` | 36 |
| dark slate ink | `rgb(34, 41, 51)` | 18 |
| translucent blue selection tint | `rgba(188, 211, 238, 0.25)` | 18 |

Drawing colour index, measured as engine integer literals. These are the classic
entity colours a drawing is drawn in, not interface colours:

| Swatch | Value | Role |
|---|---|---|
| red | `#ff0000`, `#e00000`, `#fc0000`, `#e00002` | entity colour 1 and its near variants |
| magenta | `#ff00ff`, `#b54ba0` | entity colour 6 and a muted variant |
| green | `#008000` | entity colour 3 |
| yellow green | `#daf26b`, `#adcea1` | index greens |
| white and greys | `#ffffff`, `#a9a9a9`, `#d3d3d3` | entity colour 7 and greys |
| near black | `#001000` | dark model background family |

The engine also carries a full colour name map (`#f0f8ff`, `#faebd7`, `#f0ffff`,
`#f5f5dc`, `#ffe4c4`, `#ffebcd`, `#a52a2a`, `#deb887`, `#d2691e`, `#ff7f50`,
`#fff8dc`), the standard named colour table a drawing tool exposes so a user can
name a colour rather than pick a number.

### 3.3 Typography

One interface family, `<BRAND_FONT>`, a proprietary neutral sans delivered as a
web font (Section 29). The rendered scale actually painted:

| Size | Weight | Line height | Uses | Role |
|---|---|---|---|---|
| 16px | 400 | normal | 252 | interface body default, by far the most used |
| 24px | 400 | normal | 162 | panel and dialog headings |
| 20px | 600 | 26px | 18 | emphasised labels, for example the assistant title |

Name the family and give a normative fallback stack; do not ship the font binary
(Section 29).

### 3.4 Layout tokens

Corner radii cluster at two values: `2px` on the small square icon buttons of the
toolbars (36 uses) and `8px` on the floating panels (18 uses). The stacking order
observed is shallow and deliberate: `z-index` values `70` and `69` sit at the top
for the floating panels and their handles, over a canvas that owns the rest of
the screen.

> **In plain language.** The tool itself is light and quiet to look at: soft grey
> icons and text, near white panels, a touch of dark slate for strong text, and a
> pale blue wash to show what you have selected. That restraint is on purpose, so
> the drawing, which can be any colour, stands out against a calm interface. The
> drawing has its own separate set of strong, pure colours, bright red, magenta,
> green, white, the traditional colours a technical drawing is drawn in, plus a
> full list of named colours so you can ask for "coral" instead of a number. Text
> is one clean typeface at a comfortable reading size, panels have gently rounded
> corners, and the floating panels always sit above the drawing.

## 4. Iconography

Interface icons are inline vector geometry, not image files, so they stay sharp
at any size and can be recoloured. Two were captured as geometry; transcribe them
as coordinates. Both are drawn on a `0 0 16 16` grid.

### 4.1 Dock or window glyph

A `0 0 16 16` icon built from one `path` plus a `polygon`. The path is
`M0,16H8V8H0Zm2-6H6v4H2Z`: a filled square occupying the lower left quadrant with
a rectangular cut out inside it, the conventional mark for a docked or
picture in picture panel. The accompanying `polygon` completes an outward corner.

### 4.2 Close glyph

A `0 0 16 16` icon, a single `path` drawing a diagonal cross:
`M13.3996 3.40001L12.5996 2.60001L7.99961 7.30001L3.39961 2.60001L2.59961 3.40001L7.29961 8.00001L2.59961 12.6L3.39961 13.4L7.99961 8.70001L12.5996 13.4L13.3996 12.6L8.69961 8.00001L13.3996 3.40001Z`.
It is the panel and dialog close control, a stroked X with squared ends.

The rest of the toolbar iconography, the drawing and editing tools, was not
reachable behind the sign in wall and is specified by capability, not geometry
(Sections 10, 11, 30).

> **In plain language.** The little symbols in the tool are drawn as shapes rather
> than saved as pictures, so they stay crisp at any size. We could only capture
> two before the sign in wall: a small square badge that means "pop this panel out
> or dock it", and the X you click to close a panel. The many drawing tool icons
> live behind the login, so those are described by what they do rather than drawn
> here.

## 5. Global chrome

The chrome is the frame around the canvas. It was not directly observable behind
the sign in wall, so this section is normative capability informed by the
measured component families (Section 3.1) and the two captured glyphs
(Section 4). Where a value is measured, it is quoted.

### 5.1 Top bar

A fixed top bar carrying the application badge `<BRAND_MARK>`, the current
drawing name, primary menus or a ribbon of tool groups, and account and share
controls at the right. It owns the small square icon buttons whose corners are
`2px` and whose fill transitions on `fill 0.2s cubic-bezier(0.4, 0, 0.2, 1)`
(Section 6).

### 5.2 Floating panels

Panels for layers, properties, blocks and references float over the canvas. The
measured panel surface uses an `8px` radius and a lifted shadow
`rgba(0, 0, 0, 0.32) 0px 4px 16px 0px`, and sits at `z-index` `70` over the
canvas. Panels are dockable and closable (the glyphs in Section 4), and a panel
can be resized by a handle (Section 5.4).

### 5.3 Status bar

A bottom status bar carrying the coordinate readout and the drafting toggles
(snap, grid, ortho, polar tracking, object snap, lineweight display), plus model
and layout tab access (Section 16). Each toggle is a stateful control reflecting
on or off.

### 5.4 The resize handle

A measured detail worth reproducing exactly: the panel resize handle is a thin
strip at `opacity` `0.5` carrying a diagonal hatch drawn as a repeating gradient,
`linear-gradient(135deg, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0) 50%, rgb(245, 245, 245) 50%, rgb(245, 245, 245) 60%, rgba(0, 0, 0, 0) 60%, rgba(0, 0, 0, 0) 70%, rgb(245, 245, 245) 70%)`,
which reads as a grip of pale diagonal lines. It brightens toward full presence
on hover.

> **In plain language.** Around the edges of the drawing sits the usual furniture:
> a bar across the top with the drawing's name, the menus and your account, panels
> that float over the drawing for things like layers and properties, and a strip
> along the bottom with your cursor position and the row of on and off switches a
> draftsperson flicks constantly. The panels can be popped out, moved, closed and
> resized; the little resize grip is a patch of faint diagonal lines that firms up
> when you point at it. Each panel gently lifts off the drawing with a soft shadow
> so it never gets lost against it.

## 6. Motion language

### 6.1 Easing vocabulary

Measured easing curves, most used first. Quote them exactly.

| Curve | Uses | Role |
|---|---|---|
| `cubic-bezier(0.4, 0, 0.2, 1)` | 50 | the standard material settle, used across the chrome |
| `cubic-bezier(0.77, 0, 0.265, 2)` | 8 | an overshoot curve, a spring that passes its target and returns |
| `cubic-bezier(0.0, 0, 0.2, 1)` | 2 | decelerate in |
| `cubic-bezier(0.4, 0, 1, 1)` | 2 | accelerate out |
| `cubic-bezier(0.4, 0, 0.6, 1)` | 2 | a gentle in out |
| `cubic-bezier(0.65, 0.815, 0.735, 0.395)` | 1 | a reveal curve |
| `cubic-bezier(0.165, 0.84, 0.44, 1)` | 1 | a strong ease out |
| `cubic-bezier(0.35, 0.8, 0.4, 1)` | 1 | a soft ease out |
| `cubic-bezier(0.25, 1, 0.5, 1)` | 1 | the fast settle used on reveals |

### 6.2 Transitions declared

- `all` (360 uses), the catch all base the component kit applies broadly.
- `box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1), background-color 0.3s cubic-bezier(0.4, 0, 0.2, 1), color 0.3s cubic-bezier(0.4, 0, 0.2, 1), outline-width 0.05s cubic-bezier(0.4, 0, 0.2, 1)`
  (36 uses), the button and control interaction: shadow, fill and text colour move
  together over roughly a third of a second, with the focus outline snapping in
  faster.
- `fill 0.2s cubic-bezier(0.4, 0, 0.2, 1)` (36 uses), the icon recolour.

### 6.3 The loading animation

The loading screen animates a vector mark (Section 7) and was delivered through a
vector animation runtime and a set of animation frames (Section 29). It is the
one motion the capture could see run, and it loops until the application is ready.

> **In plain language.** Motion in the interface is calm and consistent. Buttons
> and controls do not snap; their shadow, fill and text colour glide together to a
> settled state in about a third of a second, while the focus ring that shows
> keyboard users where they are snaps in quickly. A few places use a springy curve
> that overshoots a hair and settles back, for a bit of life. The one piece of
> motion a visitor actually sees is the loading mark on the opening screen, which
> turns steadily until the tool is ready.

## 7. The preloader

This is the one surface fully observable without an account, and every route
(Section 2) resolves to it. On a pure black field, centred, sits the square
application badge `<BRAND_MARK>` inside a thin circular indicator that sweeps
continuously, drawn as an animated polygon ring (a many sided outline that reads
as a spinning circle). Nothing else is on the screen: no navigation, no text, no
chrome. The badge is a small rounded square in the brand colour with a letterform
over a lower label.

The black field is the model space background a drafting tool traditionally
opens into, so the loading screen doubles as a promise of the dark canvas to
come. The mark holds dead centre at every scroll position, because there is no
scroll: the page height never changes across the nine sampled positions.

> **In plain language.** Before anything loads you get a very simple screen: a
> solid black background with the small square product badge in the middle, ringed
> by a thin line that sweeps around and around like a clock hand, telling you it
> is working. There is nothing else, no menu, no words. The background is pure
> black on purpose, because that is the colour the drawing area itself opens into,
> so the loading screen is already showing you where you are headed.

## 8. The drawing canvas and rendering surface

The canvas is the product. It is an infinite, zoomable, pannable drawing surface
rendered by a compiled graphics pipeline (the reference used a WebGL pipeline
with post processing, Section 3.1). This section is normative capability; the
editor was behind the sign in wall (Section 30).

### 8.1 Capability requirement (normative)

- Render a real world coordinate space with configurable drawing units
  (architectural, engineering, decimal, fractional, scientific; imperial and
  metric).
- Pan, zoom to a window, zoom to extents, zoom to previous, and regenerate, all
  interactive and smooth on drawings of hundreds of thousands of entities.
- Draw every 2D entity type faithfully: lines, polylines with arc and width
  segments, circles, arcs, ellipses and elliptical arcs, splines, points,
  hatches and gradient fills, text, dimensions, tables and wipeouts.
- Reproduce entity appearance exactly: colour by the drawing colour index
  (Section 3.2), linetype, lineweight, transparency and draw order, matching a
  desktop drafting tool.
- Maintain a spatial index so hit testing, selection and snapping (Section 9)
  stay instant as the entity count grows.
- Hold a smooth interactive feel while panning and zooming a large drawing, and
  degrade with level of detail rather than stalling.

### 8.2 The model and paper duality

The canvas presents model space (the drawing at real scale) and one or more paper
space layouts (the sheet, with viewports onto the model), switched by tabs in the
status bar (Section 16).

> **In plain language.** The drawing area is the whole point of the product. It is
> an endless sheet you can slide around and zoom into without limit, showing the
> drawing at its true size, a wall that is ten metres long is ten metres in the
> drawing. It has to draw every kind of thing a technical drawing contains,
> straight lines, curves, circles, text, dimensions, filled areas, and show each
> in exactly the right colour and thickness, matching the desktop tool precisely.
> And it has to stay smooth even when the drawing holds hundreds of thousands of
> pieces. There is a second mode, a printable sheet with framed windows looking
> onto the drawing, that you switch to with a tab.

## 9. Precision input and drawing aids

Professional drafting is precise to the unit, so the input aids are not a
convenience, they are the product. Normative capability:

- **Object snaps**: endpoint, midpoint, centre, node, quadrant, intersection,
  extension, insertion, perpendicular, tangent, nearest, apparent intersection
  and parallel. The nearest meaningful point must resolve within a keystroke, at
  any zoom, against the full entity set.
- **Tracking**: polar tracking at configurable angle increments, orthogonal mode,
  and object snap tracking that aligns to acquired points.
- **Coordinate entry**: absolute, relative, polar and direct distance entry,
  typed at the command input or shown as dynamic input beside the cursor.
- **Grid and snap**: a visible grid and a snap resolution, each toggled from the
  status bar (Section 5).
- **The command input**: a text command line accepting command names and their
  aliases, echoing prompts and options, and recalling history, the hallmark of a
  professional drafting tool and a first class input method equal to the toolbar.

> **In plain language.** A technical drawing is exact, so the tool spends most of
> its cleverness helping you place a point in precisely the right spot. As you move
> the cursor it silently offers meaningful points, the exact end of a line, the
> centre of a circle, the crossing of two lines, so your next click lands true. It
> can lock movement to set angles, follow guide lines off points you have touched,
> and take exact typed distances and directions. And it keeps the old typed
> command line that professionals are fast with: you can type what you want as
> readily as clicking a button.

## 10. Drawing and creation tools

Normative capability. The full creation toolset of a professional 2D drafting
tool:

- Lines, polylines (with arc segments and width), construction lines and rays.
- Circles by every method (centre radius, two point, three point,
  tangent tangent radius), arcs by every method, ellipses and elliptical arcs.
- Rectangles (with chamfer, fillet and width options) and polygons (inscribed and
  circumscribed).
- Splines by fit points and by control vertices.
- Points with named point styles, and donuts.
- Hatch and gradient fill: predefined and custom patterns, pick point island
  detection, associative hatches that follow their boundary, and scale, angle and
  origin control.
- Regions and boundary extraction.
- Revision clouds (rectangular, polygonal and freehand) and wipeouts.

Each tool is reachable both from a toolbar and by its command name and alias
(Section 9).

> **In plain language.** This is the box of things you can draw: straight lines and
> connected line and arc paths, circles and arcs made whichever way suits the
> geometry you already have, rectangles and regular polygons, smooth curves,
> points, filled and patterned areas that update themselves if you reshape their
> boundary, and mark up shapes like the little clouds used to flag a revision.
> Every one of these is available either by clicking a tool or by typing its name,
> whichever is faster for you.

## 11. Editing and modification tools

Normative capability. The full modification toolset:

- Move, copy, rotate, scale, mirror, offset and array (rectangular, polar and
  along a path).
- Trim, extend, fillet, chamfer and blend curves.
- Stretch, lengthen, break, break at point and join.
- Explode, and duplicate cleanup.
- Grip editing: multi function grips on a selected entity to stretch, move or
  rotate its vertices directly, including converting a straight polyline segment
  to an arc by dragging a grip.
- Selection: window, crossing, fence, window polygon and crossing polygon, plus
  last, previous and all; selection cycling for overlapping entities; and a quick
  select that filters by property.
- Match properties, painting one entity's properties onto others.

> **In plain language.** This is the other half: changing what is already drawn.
> You can move, copy, spin, resize, mirror and repeat things in neat rows or rings;
> trim lines back to where they meet, extend them to reach, round or bevel corners;
> and grab the little handles on a shape to nudge a single corner. You can select
> things by dragging a box around them, by drawing a line across them, or by asking
> for "every red circle" in one go, and you can copy one object's look onto another
> with a single tool.

## 12. Layers and object properties

Normative capability, informed by the measured floating panel (Section 5):

- A full layer manager: create, rename and delete layers; toggle on or off,
  freeze or thaw, lock or unlock; set colour (Section 3.2), linetype, lineweight,
  transparency, plot or no plot, and a description.
- Layer states saved and restored; layer filters; make current; and isolate,
  freeze or turn off a layer by picking an entity on it.
- Per object overrides for colour, layer, linetype, linetype scale, lineweight,
  transparency and thickness.
- A properties panel that inspects and edits the full property set of any
  selection, and an inheritance model where a property can follow its layer or
  its block rather than being set directly.

The layer and properties panels are floating panels (Section 5.2): `8px` corner,
lifted shadow, dockable and closable.

> **In plain language.** Everything you draw lives on a named layer, like sheets of
> transparent film stacked up, walls on one, wiring on another, and a layer manager
> lets you name them, colour them, hide them, lock them and control which ones
> print. You can turn a whole layer off to get it out of the way, or click one line
> to isolate just its layer. A properties panel shows every detail of whatever you
> have selected and lets you change it, and most things can simply inherit their
> look from their layer so you set it once.

## 13. Annotation

Normative capability. A drawing is worthless without its notes, dimensions and
schedules:

- **Text**: single line and multi line text with rich formatting (font, height,
  bold, italic, underline, stacked fractions, bullets and numbering, columns and a
  background mask), governed by named text styles.
- **Dimensions**: linear, aligned, angular, radius, diameter, arc length, ordinate,
  baseline and continued; named dimension styles; associative dimensions that
  update when their geometry changes; multileaders and leader styles.
- **Tables**: cell formatting, merges, formulas and named table styles.
- **Fields**: auto updating text tied to a property, a date or a sheet value.
- **Annotative scaling**: annotation that displays correctly across viewport
  scales.
- Geometric tolerance symbols, centre marks and centrelines.

> **In plain language.** A drawing is not finished until it is labelled, so the tool
> has a full kit for words and numbers: rich text notes, and dimensions of every
> kind, the measured lengths, angles, radii and so on, which stay correct on their
> own when you resize the thing they measure. There are tables with cells and even
> simple formulas, bits of text that fill themselves in from the drawing's own
> information, and clever labels that stay a readable size whatever scale the sheet
> is shown at.

## 14. Blocks and content reuse

Normative capability:

- Insert blocks from the current drawing, from libraries and from connected
  content, with a preview.
- Create block definitions from selected geometry, with a base point, name, unit
  and description.
- Dynamic blocks: insert and manipulate a block with visibility states and with
  stretch, flip, array, rotation and lookup parameters. Manipulation and playback
  are required; full authoring of dynamic block parameters is a later capability
  (Section 30).
- Attributes: editable text fields carried inside a block, and extraction of those
  attributes into a table or export.

> **In plain language.** Anything you draw once and reuse, a door, a chair, a title
> block, can be saved as a reusable stamp called a block, then dropped in wherever
> you need it. Smart versions of these can flex when placed, the same door block
> stretched to a wider opening or flipped to hinge the other way, and blocks can
> carry little fill in labels, like a room number, that you can later pull out into
> a schedule automatically.

## 15. External references and underlays

Normative capability:

- External references: attach, detach, reload and unload other drawings, with
  attach and overlay modes, path control and clipping.
- Image underlays: attach, clip and adjust raster images.
- Document underlays: attach and clip a page based document, snap to its vector
  geometry, and import that geometry into the drawing.
- Underlays for other exchange formats where applicable.

> **In plain language.** A drawing rarely stands alone. You can hang other people's
> drawings underneath yours as live references that update when they do, so a floor
> plan can sit under your electrical layout without copying it in. You can also
> bring in photographs and scanned pages as backdrops to trace or measure over, and
> even lift the lines straight out of a page based document into your own drawing.

## 16. Layouts, viewports and plotting

Normative capability:

- Paper space layouts with page setup: sheet size, plot area, scale and
  orientation.
- Viewports: create, scale to standard scales, lock, and freeze layers or override
  layer properties per viewport.
- Plot and publish: output to a page based document, single or multi sheet, and to
  print, governed by plot styles that map colour and lineweight to output.
- Export to the drawing exchange formats and to a page based document; import from
  a page based document and from images.
- Sheet metadata and a title block driven by blocks, attributes and fields
  (Sections 13, 14).

> **In plain language.** When it is time to hand the drawing over, you lay it out on
> a printable sheet at a chosen scale, with framed windows onto the drawing, each
> window able to show different layers or a different zoom. Then you plot it: to a
> shareable page document or to a printer, with a style sheet deciding how the
> on screen colours turn into printed line weights. You can also send the drawing
> out in the standard exchange formats other tools read.

## 17. Measure, markup and review

Normative capability:

- Measure tools: distance, radius, angle, area and perimeter, and a quick measure
  that shows nearby dimensions on hover.
- Markup and redline tools for reviewers: freehand, shapes, callouts and text
  notes.
- Comments anchored to a location or an entity, with threads and mentions
  (Section 19).
- Drawing compare: visualise the differences between two drawings or two versions,
  with added, removed and changed geometry colour coded.

> **In plain language.** Not everyone who opens a drawing is drawing; many are
> checking. So there are quick tools to measure a distance, an angle or an area
> just by pointing, tools to scribble review marks and notes on top without
> changing the drawing itself, and a way to leave comments pinned to an exact spot
> for someone else to answer. There is also a compare view that lights up exactly
> what changed between two versions, in colour, so a reviewer sees the difference
> at a glance.

## 18. Files, storage and sharing

Normative capability, with the measured live channel (Section 3.1) supporting
the collaborative parts:

- Open, create (from a template), upload and save industry standard drawing files
  and their exchange format.
- Cloud document store as the home for drawings (`<STORAGE_PROVIDER>`), with third
  party storage connectors.
- Explicit save, save a copy, and automatic save with crash and tab close
  recovery.
- Version history: named and automatic versions, each with author and time,
  restore to any version, and compare (Section 17).
- Share with role based permission (view, comment, edit) by link, and manage
  collaborators.

> **In plain language.** Your drawings live in the cloud, not on one computer, so
> the same file opens on a desktop, in this browser and on a phone, always the
> latest version. The tool saves as you go and can recover your work if the tab
> crashes, and it keeps a full history so you can look at, or roll back to, any
> earlier version. Sharing is a link with a chosen level of trust: some people can
> only look, some can comment, some can edit.

## 19. Real time collaboration

The reference carried a live event channel (26 server sent event streams,
Section 3.1), the backbone of live collaboration. Normative capability:

- Several people edit the same drawing at once, each seeing the others' cursors,
  selections and edits appear live.
- Presence: who is in the drawing right now, shown as avatars.
- A merge model that resolves concurrent edits to the shared drawing while keeping
  it internally consistent (a moved line keeps its dimension, a referenced block is
  not deleted from under another editor). This is the hard core of Section 21.
- Comment and markup threads (Section 17) synchronised live, with notifications
  and resolution state.

> **In plain language.** Several people can be in the same drawing at the same time,
> the way several people can type in the same shared document, each seeing the
> others' cursors move and their changes appear the instant they make them, with
> little avatars showing who is here. The tricky part the tool must get right is
> that a drawing is not just text: if one person moves a wall while another is
> dimensioning it, the dimension has to follow the wall, and nobody's work may
> quietly corrupt the file. Comments and review marks show up for everyone live
> too.

## 20. The assistant panel

The one interface string the capture recovered past the shell names an assistant:
the reference mounts a panel titled `<ASSISTANT_NAME>` (a `MuiTypography` heading,
Section 28) at the emphasised `20px` weight `600` label size (Section 3.3).
Normative capability:

- A docked side panel offering an in application assistant: ask a question about a
  command or the drawing, get guidance, and trigger help in context.
- The panel is a floating and dockable surface (Section 5.2), openable and
  closable, and resizable by the measured handle (Section 5.4).

Its full behaviour was behind the sign in wall and is specified by capability, not
measurement (Section 30).

> **In plain language.** Off to one side sits a help assistant you can open, ask a
> question of, and close again, the way a chat panel tucks into the edge of an app.
> It is there to answer "how do I do this" without making you leave the drawing.
> The panel behaves like the others: you can pop it out, move it, close it and drag
> its edge to resize it. Exactly how clever it is lived behind the login, so we
> describe what it is for rather than what it said.

## 21. The irreducible core: features no model or agent can build

This section is the honest heart of the estimate. Sections 8 through 20 describe a
large but conventional application: panels, tools, files, a live channel. The
subsystems below are different in kind. Each is years of specialised research, in
several cases proprietary or undocumented, and none can be produced by a code
generating model or an autonomous agent from a description. They are called out so
the plan does not mistake this product for a weekend build. The measured stack
(Section 3.1) shows the reference carrying exactly this class of machinery: a
compiled geometry core, a WebGL pipeline with post processing, and a live sync
channel.

The hardest guarantees, and where each is specified:

- Precision geometry kernel, exact calculations not approximations: Section 21.1.
- Boolean operations on complex 3D solids without breaking integrity:
  Section 21.1.
- Parametric and constraint based modelling, one dimension updates all dependents:
  Section 21.4.
- Massive assemblies of thousands of parts kept responsive: Section 21.7.
- Precise coordinate systems and snapping accurate at any zoom, millimetres to
  kilometres: Section 21.8, with Section 9.
- File format compatibility across decades of legacy formats, the drawing format
  and its exchange format: Section 21.2, with Section 18.
- A pipeline handling 2D drafting and full 3D shaded or wireframe in real time:
  Section 21.9, building on Section 21.5.
- Undo and version history tracking precise geometric state across interdependent
  objects: Section 21.10, with Section 18.

### 21.1 The precision geometry kernel

A numerically robust geometry kernel that performs exact mathematical
calculations for curves, surfaces and solids, not approximations: exact and
tolerance based intersection, projection and containment for lines, arcs,
ellipses and splines; robust boolean operations and island detection for hatching
over nested loops; offsetting of arbitrary curves with self intersection
handling; and filleting and chamfering with correct trimming. The whole
difficulty is numerical robustness against floating point degeneracy, the line
between a tool that usually works and one that never silently produces wrong
geometry. A model cannot derive this from a prompt.

**Boolean operations on 3D solids.** Where the product edits solids, the kernel
must perform boolean operations,
union, subtract and intersect, on complex 3D solids without breaking geometry
integrity: no cracks, no inverted faces, no lost topology when two intricate
bodies combine. Robust solid modelling booleans are a specialised body of work in
their own right, distinct from the 2D curve operations above, and are among the
hardest guarantees in the whole product. This is a capability requirement; solid
editing scope on web is set in Section 30.

### 21.2 The drawing file format engine

The industry standard drawing format is a proprietary, undocumented, version
evolving binary format with bit packed encoding, object handles and cross
references. Reading and writing it faithfully across many format generations,
preserving every entity and custom object with lossless round trips, is a
specialised discipline. No agent can reverse engineer byte accurate file input and
output from a description, and "close" corrupts real drawings.

### 21.3 Collaboration over a drawing graph

Live co editing of text is well trodden. Live co editing of a richly cross
referenced drawing, where entities own handles, dimensions are associative to
geometry, blocks reference definitions and layers gate everything, is a research
grade problem. It needs a conflict resolution model defined over drawing
operations, not characters, that preserves referential integrity and converges
deterministically across clients running a floating point engine. It cannot be
synthesised by a general agent.

### 21.4 The constraint solver

Dynamic blocks and parametric drawing need a variational geometric constraint
solver: given geometric constraints (coincident, parallel, perpendicular, tangent,
concentric, equal) and dimensional constraints (distance, angle, radius), solve for
a valid configuration in real time as the user drags, with graceful handling of
under and over constrained cases. This is nonlinear equation solving with degrees
of freedom analysis, the province of specialists, and is not producible by
prompting a model.

### 21.5 High performance rendering of massive vector scenes

Rendering hundreds of thousands of entities at an interactive frame rate in a
browser demands a bespoke graphics pipeline (the reference used WebGL with post
processing, Section 3.1): curve and text tessellation at the right level of detail
per zoom, a spatial index for culling and hit testing, and correct lineweights,
linetypes, transparency, draw order and hatch fills matching desktop output. It is
a real time graphics engine, not a chart library.

### 21.6 Precision snapping and inference at scale

Object snap and tracking (Section 9) must resolve the geometrically nearest
meaningful point among massive entity sets in milliseconds, with correct priority
and feedback, coupling the spatial index, the geometry core and interaction
heuristics into one deceptively deep subsystem.

### 21.7 Massive assemblies

The product must hold massive assemblies, drawings and models composed of
thousands of parts and block instances, while keeping editing and rendering
responsive. That means instancing so a repeated part is stored and drawn once and
placed many times, demand loading and unloading of parts as they enter and leave
view, a spatial index that scales, and an edit path that touches only what
changed rather than regenerating the whole assembly. Responsiveness at that count
is an architecture, not a setting, and it is a first order engineering problem.

### 21.8 Multi scale precision and coordinate systems

Precise coordinate systems and snapping must stay exact at any zoom level, from
millimetres to kilometres, in the same drawing. A civil site measured in
kilometres can carry a bolt hole measured in fractions of a millimetre, and both
must round trip and snap true. This requires careful numeric handling so that
precision does not decay far from the origin or at extreme zoom, correct handling
of the world coordinate system and user coordinate systems, and snapping
(Section 9) that stays accurate across that whole range. Getting this wrong shows
up as geometry that drifts, fails to close, or refuses to snap when a user is
zoomed a long way in on a distant part of a large site.

### 21.9 Unified 2D and 3D rendering

The rendering pipeline must handle both 2D drafting views and full 3D models,
shaded or wireframe, in real time, in the same session and often the same view.
That is two rendering disciplines under one engine: exact 2D line work with
correct lineweights, linetypes and draw order (Section 21.5), and 3D display with
hidden line removal, wireframe and shaded modes, visual styles and a camera.
Switching between them, and holding an interactive feel in both on a large model,
is a bespoke pipeline built on the low level graphics layer the reference already
carries (Section 3.1).

### 21.10 Deterministic undo and geometric history

Undo and version history must track precise geometric state changes across
complex, interdependent objects, not just a flat list of clicks. When one edit
ripples, a moved line drags its dimension, a changed parameter reshapes a block,
a boolean rebuilds a solid, undo has to restore every dependent object to its
exact prior state, in order, and version history (Section 18) has to capture that
same interdependent state so a restore is faithful. Building an undo and history
model over a live graph of associative, floating point geometry is far harder than
a text editor's undo stack and is part of this irreducible core.

> **In plain language.** Most of this product is big but ordinary software:
> windows, panels, tools, saving files. This part is not. Underneath sit a handful
> of engines that took specialists many years to build, and in some cases depend on
> secrets that are not written down anywhere. There is the maths engine that works
> out where lines truly cross and never quietly gets it wrong; the reader and
> writer for the drawing file itself, whose exact format is a closely held secret,
> so getting it slightly wrong means ruining people's drawings; the machinery that
> lets many people edit one drawing at once without the pieces coming apart; the
> solver that lets a smart block flex while keeping all its rules true; and the
> drawing engine fast enough to push a huge drawing around smoothly. There is more
> in the same vein: cleanly cutting, joining and combining solid 3D shapes without
> leaving them broken; holding a model of thousands of parts and still feeling
> quick; staying dead accurate whether you are working at the size of a bolt or a
> whole city block, in the same drawing; showing flat drafting and full 3D, plain
> outlines or solid shaded, at the same time and without lag; and an undo that can
> perfectly walk back a change even when it rippled through dozens of connected
> pieces. These are the reason this is a serious build and not something a clever
> assistant can just write from a description.

## 22. Component architecture

Suggested component boundaries, informed by the measured component families
(Section 3.1):

- `AppShell` (top bar, layout, panel host)
- `Preloader` (the badge and sweeping ring, Section 7)
- `DrawingCanvas` (the rendering surface and its input, Sections 8, 9)
- `CommandLine` and `StatusBar` (Sections 9, 5)
- `LayerPanel`, `PropertiesPanel`, `BlocksPanel`, `ReferencesPanel` (floating
  panels, Sections 12, 14, 15)
- `AssistantPanel` (Section 20)
- `LayoutTabs` and `Viewport` (Section 16)
- `PresenceLayer` and `CommentThread` (Section 19)

Shared primitives: `IconButton` (the `2px` square control with the measured fill
and shadow transition, Section 6), `FloatingPanel` (the `8px` shadowed surface
with the resize handle, Section 5), and `SvgIcon` (the geometry in Section 4).
Class prefixes generated by the styling libraries are framework artefacts, not
brand names; keep any chosen prefix free of the brand string (Section 30).

> **In plain language.** If you build this in pieces, the natural parts are the
> outer shell, the loading screen, the big drawing area with its typing line and
> status strip, the floating panels for layers, properties, blocks and references,
> the help assistant, the printable sheet tabs, and the live cursors and comments
> of other people. A few small building blocks, a square icon button, a floating
> panel with a resize grip, and a vector icon, get reused throughout.

## 23. Responsive behaviour

The reference declared no interface media queries in the capture, consistent with
an application that fills the browser window and reflows by its own layout logic
rather than by breakpoint. Normative capability:

- The workspace fills the window at any size and remains usable from a small
  laptop up to a large desktop, with panels collapsible to reclaim canvas.
- On a tablet, the tool must accept touch: two finger pan and zoom, tap to select,
  and long press for a context menu, with controls sized for a fingertip.
- The canvas is the priority surface; chrome yields to it as the window shrinks.

> **In plain language.** This is not a page that reflows into a phone column; it is
> a workspace that fills whatever window it is in and gives as much room as possible
> to the drawing, tucking panels away when space is tight. On a touch screen it
> responds to fingers, sliding and pinching to pan and zoom, tapping to select, so a
> tablet on site works as well as a laptop at a desk.

## 24. Accessibility

Normative capability for an infinite canvas application:

- The command line (Section 9) is a fully keyboard operable path to every command,
  which is the primary accessibility affordance of the product; keep it complete.
- All panels, dialogs, toggles and the assistant must be keyboard reachable and
  focus visible; the measured control transition already snaps a focus outline in
  quickly (Section 6).
- Honour a reduced motion preference: the loading animation and any interface
  motion resolve to a still state.
- Interface colour must meet contrast targets; verify the primary grey
  `rgb(162, 166, 176)` on its surfaces and lift it where it falls short.
- Provide text alternatives and names for tool icons and for shared cursors and
  comments.

> **In plain language.** Someone working by keyboard alone, or asking their device
> for less movement, or relying on a screen reader, should get the same tool. The
> old typed command line is a gift here: everything can be done by typing, no mouse
> needed. Beyond that, every panel and switch must be reachable by keyboard with a
> clear focus marker, the loading spin must be able to hold still, the soft grey
> text must be dark enough to read, and every icon and every shared cursor needs a
> name behind it.

## 25. Performance

The reference is a heavy client: 312 script files, roughly 836 megabytes of
transferred JavaScript, and a font payload delivered as a web font (Section 29).
Targets:

- First meaningful readiness should arrive behind the loading screen (Section 7),
  which covers the download and warm up of the drawing engine; keep that covered
  time honest and driven by real progress.
- Once loaded, pan and zoom must stay smooth on a large drawing, with level of
  detail rather than stalls; animate only cheap properties for interface motion.
- Stream and cache the engine so a returning user does not re download it; the
  reference served inline source maps and split the payload across many files,
  which supports incremental caching.
- The live channel (Section 19) must stay responsive, with edits and presence
  appearing within a moment.

> **In plain language.** This tool is big, opening it pulls down a large engine, so
> the craft is making that feel acceptable: cover the wait with the honest loading
> screen, remember the engine so a second visit is quick, and then keep the drawing
> gliding under your hand no matter how much is in it. Working with others should
> feel instant, with their changes turning up a moment after they make them.

## 26. Backend and data contract

The application is a thin visible shell over a substantial backend. From the
measured signals (Section 3.1) and the capabilities above:

### 26.1 Identity and entitlement

Account sign in through `<IDENTITY_PROVIDER>`, with single sign on for
organisations, and an entitlement check that gates the full editor against a valid
subscription while allowing a lighter view and markup role for others.

### 26.2 Document services

A drawing store (`<STORAGE_PROVIDER>`) plus third party storage connectors; server
side translation of the drawing format to stream to the client engine; thumbnail
and preview generation; export to a page based document and to images; and import
of page based document geometry.

### 26.3 Version and collaboration services

An immutable version store with restore and compare; a co editing session service
with membership, presence and permissioning; and the live channel measured as
server sent event streams (Section 3.1), carrying edits, presence and comments.

### 26.4 Autosave and recovery

Automatic save to the cloud and recovery of unsaved work after a crash or tab
close, with conflict detection on concurrent single writer saves.

### 26.5 Cross product continuity

The same cloud drawing opens identically on desktop, web and mobile, and edits
sync between them.

> **In plain language.** What you see is a thin front for a large machine behind
> the scenes. It signs you in and checks your subscription, keeps your drawings in
> the cloud and can reach into other storage services you connect, turns the heavy
> drawing file into something the browser engine can stream, remembers every
> version so you can go back, and runs the live wiring that lets people work
> together. It saves constantly and can rescue your work if things crash, and it
> keeps the desktop, web and phone versions all looking at the very same drawing.

## 27. Build order

1. The application shell, the loading screen and the design tokens: chrome,
   colours, type, the icon button and floating panel primitives (Sections 3, 5, 7).
2. The drawing canvas and rendering surface with pan, zoom and faithful entity
   display (Section 8), on top of the geometry and rendering core (Section 21).
3. Precision input: object snaps, tracking, coordinate entry and the command line
   (Section 9).
4. Creation and modification tools (Sections 10, 11), then layers and properties
   (Section 12).
5. Annotation, blocks, external references, and layouts and plotting
   (Sections 13, 14, 15, 16).
6. Files, storage, versioning and sharing (Section 18).
7. Real time collaboration and the assistant panel (Sections 19, 20).
8. Measure, markup and compare, then the accessibility and performance passes
   (Sections 17, 24, 25).

The hard core (Section 21) is not a late step; it underlies steps 2 and 7 and is
the long pole of the whole schedule.

> **In plain language.** Build it so you always have something real to look at:
> first the frame and the loading screen, then the drawing area itself so you can
> draw a line, then the precise pointing aids, then the full set of drawing and
> editing tools, then layers, labels and reusable stamps, then sheets and printing,
> then saving and sharing, and finally live teamwork and the helper. The deep
> engines underneath are not a finishing touch; they hold up the whole thing and
> take the longest, so they start at the very beginning.

## 28. Copy deck

Brand and service names are tokenised; keep replacements close in length.

- Page title: "`<BRAND>` Web App, Online CAD Editor and Viewer, by `<BRAND>`"
  (the reference titled its page as the product name followed by "Web App - Online
  CAD Editor & Viewer" and the company name).
- Assistant panel title: `<ASSISTANT_NAME>`.
- Application badge: `<BRAND_MARK>`, a square monogram over a short label.
- The interface otherwise speaks in command names and tool names (Sections 10, 11),
  which are the standard vocabulary of the drafting discipline and are not brand
  copy.

> **In plain language.** There is very little marketing wording in this product,
> because it is a working tool, not a page to read. The browser tab calls it the
> product name and "online CAD editor and viewer". The help panel carries the
> assistant's name. Almost everything else you read is the names of drawing tools
> and commands, the ordinary language of drafting, which you keep as is.

## 29. Zero asset substitution guide

The build must stand up with no supplied binary. For each asset class the
reference used, a procedural replacement, keyed to the measured palette
(Section 3.2).

### 29.1 The interface font

The reference served a proprietary neutral sans as a web font from `<ASSET_HOST>`.
Name the family and give a normative fallback of a neutral grotesque, for example
a system sans stack, so the layout holds before and without the web font. Naming a
family is not a binary dependency; do not ship the font file.

### 29.2 The application badge and loading mark

The badge is a small rounded square in the brand colour carrying a monogram over a
short label. Rebuild it as inline vector geometry: a rounded rectangle filled with
a brand red from the drawing palette (for example `#e00000`), a white monogram and
a white lower label, sized to sit inside the ring. The sweeping loader is an
inline vector ring, a stroked circle with a rotating arc, on the black field of
Section 7; no animation file is needed.

### 29.3 The panel resize grip

Already procedural: the measured diagonal hatch
`linear-gradient(135deg, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0) 50%, rgb(245, 245, 245) 50%, rgb(245, 245, 245) 60%, rgba(0, 0, 0, 0) 60%, rgba(0, 0, 0, 0) 70%, rgb(245, 245, 245) 70%)`
at `opacity` `0.5` rebuilds the grip with no image.

### 29.4 Tool icons

The drawing and editing tool icons were behind the sign in wall (Section 30).
Rebuild them as inline vector geometry in the style of the two measured glyphs
(Section 4): single colour, `0 0 16 16` grid, stroked or filled paths, recoloured
by the interface grey `rgb(162, 166, 176)`.

### 29.5 Sample drawings

For a placeholder drawing to open, generate simple seeded geometry in code, a grid
of rectangles and circles on a couple of named layers in the drawing palette
colours, rather than shipping a sample file.

> **In plain language.** The finished product leans on a custom font, a logo, a
> loading animation and a wall of tool icons, but you can build and ship the whole
> thing with none of those files by making stand ins in code: pick a font by name
> with a safe backup, draw the badge and the spinning ring as shapes, rebuild the
> resize grip from the diagonal lines we measured, draw the tool icons as simple
> shapes in the same style as the two we captured, and generate a plain sample
> drawing to open instead of shipping one.

## 30. Evidence gaps and substitutions

What could not be measured, and what was deliberately changed:

- **The editor is behind a sign in wall.** Every route (Section 2) resolved to the
  loading screen (Section 7). The chrome, the tools, the panels and the canvas
  itself were never rendered to the capture. Everything in Sections 5 and 8 through
  20 is therefore normative capability informed by the measured component families
  (Section 3.1) and the discipline's standard toolset, not a measured pixel. The
  loading screen (Section 7), the colour, type, motion and effect tokens
  (Sections 3, 6), and the two icons (Section 4) are measured.
- **The named target does not resolve.** The originally requested host did not
  exist in the naming system. The capturable product surfaces were the marketing
  page, which a bot filter refused with an access denied response and yielded no
  usable evidence, and this application, which loaded. This application was
  captured; the substitution is recorded here.
- **Taxonomy substitution.** A professional CAD editor has no exact member in the
  closed classification. It was filed as the nearest legal pair: a small business,
  public signup productivity tool shaped as a collaborative workspace. The idea
  field records the real subject.
- **Brand and identity scrub.** The product name, the company name, the proprietary
  font name, the application and asset hosts and the assistant's name were replaced
  with tokens (Section 0.1). Class prefixes in the capture are generated by the
  styling libraries and are framework artefacts, not brand marks.
- **Colour provenance.** The saturated colours (Section 3.2) are engine integer
  literals, the drawing colour index and the named colour table, not interface CSS.
  They are the colours a drawing is drawn in. The interface chrome colours are the
  computed values, the greys and the blue selection tint.
- **No hover or scroll evidence.** The application does not scroll, and the hover
  pass found nothing on the loading screen, so the interaction detail of Sections 5
  through 20 is reconstructed from the component library's declared transitions and
  the discipline's conventions, not observed.
- **Dynamic block authoring.** Playback and manipulation are specified; full
  authoring of dynamic block parameters is marked as a later capability
  (Section 14).

> **In plain language.** This is the honest list of what we could not see and what
> we changed on purpose. The big one: the actual editor is locked behind a login, so
> all we could truly photograph was the loading screen and read the colours, fonts
> and building blocks the page loaded. Everything about the tools and panels is
> therefore a careful description of what the product must do, drawn from what the
> page was built with and from how this kind of software always works, not a picture
> we took. The web address first asked for did not exist, and the public marketing
> page refused our automated browser, so we captured the real application instead
> and wrote that down. We also swapped the real names and logo for blanks so nothing
> here copies the original.

## 31. Acceptance checklist

- [ ] The loading screen shows the square badge centred on a black field inside a
  sweeping ring, at every entry route (Sections 2, 7).
- [ ] The workspace fills the window with a top bar, floating panels, a command
  line and a status bar around a drawing canvas (Sections 5, 8).
- [ ] Floating panels carry the `8px` corner, the lifted shadow, and a resize grip
  of pale diagonal lines that firms up on hover (Sections 5, 5.4).
- [ ] Icon buttons are `2px` square controls whose fill and shadow move on the
  measured transition (Section 6).
- [ ] The canvas pans, zooms and regenerates smoothly and draws every entity type
  in its correct drawing colour, linetype and lineweight (Section 8).
- [ ] Object snaps, tracking, coordinate entry and the command line all place
  points precisely (Section 9).
- [ ] The full creation and modification toolsets are present, each reachable by
  toolbar and by command name (Sections 10, 11).
- [ ] Layers and object properties are fully manageable from floating panels
  (Section 12).
- [ ] Annotation, blocks, external references, and layouts and plotting all work
  (Sections 13, 14, 15, 16).
- [ ] Drawings open, save, autosave, recover, version and share from the cloud
  store (Section 18).
- [ ] Several people co edit one drawing live, with presence, and the drawing stays
  internally consistent (Sections 19, 21).
- [ ] The assistant panel opens, docks, resizes and closes (Sections 20, 5).
- [ ] The command line offers a complete keyboard path, and reduced motion stills
  the loading animation (Section 24).
- [ ] No brand string, no proprietary font file and no asset binary ships;
  procedural substitutes stand in (Sections 29, 30).

> **In plain language.** This is the final walk through. Does the loading screen
> look right, does the workspace come up with its drawing area and panels, do the
> panels and buttons behave as measured, does the drawing area move smoothly and
> draw everything in the correct colours and weights, do the precise pointing aids
> work, are all the drawing and editing tools there both by click and by typing, can
> you manage layers and labels and reusable stamps, can you lay out and print, can
> you save, version and share from the cloud, can several people draw together
> without breaking the file, does the helper panel behave, does everything work by
> keyboard, and did we avoid shipping any borrowed name or file. Tick every box and
> it is done.
