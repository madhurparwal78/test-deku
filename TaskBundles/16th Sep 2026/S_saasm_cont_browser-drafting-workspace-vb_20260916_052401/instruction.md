# Draftline

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, sign up, create a drawing, draw geometry on a named layer with the
cursor snapped to an exact point, save it as a version, invite a colleague into
it by email, and see that colleague's comment pinned to the drawing, without
hitting an error page. A drawing nobody has been invited into must stay
unreadable to every other account, and so must its saved bytes: the bytes of
every saved version must live as real objects in the `minio` bucket at the key
scheme below, and an entry the app keeps on its own disk or inside a database
column is not a saved version.

## Overview

Draftline is a professional two-dimensional drafting workspace that runs in a
browser with no install. It opens a drawing at true scale on an infinite canvas,
draws and edits geometry on named layers with snapping precise to the unit, saves
each save as an immutable numbered version in cloud object storage, and lets a
named colleague into the same drawing under a stated permission. A wall that is
ten metres long is ten metres in the drawing, and it stays ten metres whether the
view is pulled out to the whole site or pushed in on a single bolt hole.

Two people use it. A **drafter** owns drawings, draws and edits geometry, manages
layers, saves versions, and decides who else gets in. A **reviewer** is somebody
let into another person's drawing to read it, measure it, and leave comments
pinned to an exact place, without ever changing a line of the geometry.

The product is a working tool, not a document to read, and its information
architecture reflects that. After sign-in there is one full-screen workspace: an
infinite drawing canvas at the centre, a top bar, a left tool group, floating
panels for layers and properties, a command input, a status bar, and a docked
assistant panel. You move between surfaces by panel and by tab, never by loading
a new page. The public pages and the library are ordinary addressed pages; the
workspace is not a set of pages at all.

It deliberately is not several things. There is no reading or writing of the
industry binary drawing format, no three-dimensional solid modelling, no
constraint solver, no plotting to a printer, no payment, no subscription, and no
email or notification of any kind. The full scope-out list is in `## Constraints`
and it is part of the specification, not an apology.

The genuinely hard part is collaboration over a drawing graph. A drawing is not a
document of independent lines: entities own handles, dimensions are associative to
the geometry they measure, blocks reference their definitions, and layers gate all
of it, so the drawing is a cross-referenced graph rather than a list. Two people
can be in one drawing at once and the graph must survive it: a saved change must
reach the other person's open workspace without a reload, concurrent edits must
leave the drawing internally consistent with every reference still pointing
somewhere real, and two saves that both start from the same version must resolve
to exactly one accepted version with no gap in the numbering and nothing
half-written left behind.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `drafter` | Create drawings and own them. Create, edit and delete entities, layers and annotations on any drawing they own or were shared into at `edit`. Save versions, restore a version, compare versions. Invite, change and remove collaborators on drawings they own. Comment on anything they can read. | **Cannot read, edit, save, share or comment on a drawing they neither own nor were shared into.** **Cannot change the share list of a drawing owned by somebody else, even when shared into it at `edit`.** |
| `reviewer` | Open, pan, zoom, measure and download any drawing shared with them. Comment on a drawing shared at `comment`. Read version history. | **Cannot create a drawing.** **Cannot create, edit or delete any entity, layer or annotation on any drawing, under any share access.** **Cannot save a version, restore a version, or share a drawing.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a `reviewer`
session to any `drafter`-only endpoint must be rejected by the server (an
unauthorized request is denied, not served), leaving the protected state
unchanged.

Per-drawing access is a relationship, not a third role. A share carries `view`,
`comment` or `edit`. `view` reads and downloads. `comment` adds commenting.
`edit` adds writing geometry, and is only ever effective for an account whose
role is `drafter`: a `reviewer` shared at `edit` still cannot write, because the
role is the ceiling and the share is the door.

Signup is open. Anyone can create an account from the signup form, and every
signup creates a `drafter`. A `reviewer` account exists only by seed.

Seeded accounts, all with the password `deku-demo-pw-2026`:

| Email | Display name | Role |
|---|---|---|
| `drafter@example.com` | Mira Vance | `drafter` |
| `drafter2@example.com` | Owen Blake | `drafter` |
| `reviewer@example.com` | Priya Raman | `reviewer` |

## Core features

### Auth

Email and password accounts implemented by the app itself. Passwords are stored
hashed and no endpoint ever returns a hash. A successful login returns a bearer
token; the client sends it on every request except signup, login, health, and the
public pages. A token expires after 24 hours.

1. Signing up with an email that already has an account is rejected as invalid,
   the form says which field is at fault, and no second account row is written.
2. Signing in with the right email and the wrong password is rejected, and the
   response distinguishes nothing about whether the email exists.
3. A request carrying no token, an expired token or a token that has been
   tampered with is rejected as unauthorized on every route except signup, login,
   health and the public pages.

### The drawing library

`/drawings` lists every drawing the signed-in account can reach, which is every
drawing it owns plus every drawing shared with it, newest first. Each drawing is
a card carrying its name, its units, its current version number, when it last
changed, and who owns it when the owner is somebody else.

4. A drawing the account neither owns nor was shared into never appears in the
   list, and the list says nothing that would reveal it exists.
5. A library with no reachable drawings says so in its own words and offers the
   first step of creating one.

Creating a drawing is three steps, each at its own address. `/drawings/new/template`
picks one of `blank`, `architectural` or `mechanical`. `/drawings/new/units`
chooses one of `millimeters`, `meters`, `inches` or `feet`. `/drawings/new/name`
names it and creates it. Leaving a step incomplete and jumping to a later one
returns to the first step that is still unanswered, and nothing is created until
the last step is completed.

6. A drawing created from `architectural` opens with the layers `Base`, `Walls`,
   `Dimensions` and `Notes` already present. One created from `mechanical` opens
   with `Base`, `Outline`, `Centerlines` and `Dimensions`. One created from
   `blank` opens with `Base` alone.
7. A `reviewer` reaching any of the three creation steps, or calling the create
   endpoint directly, is refused and no drawing row is written.

### The drawing workspace and canvas

`/drawings/{id}` is the workspace. The canvas is an infinite, pannable, zoomable
surface showing the drawing in real-world coordinates at the drawing's units.
Drawing units cover architectural, engineering, decimal, fractional and
scientific formats, in both imperial and metric. Every rule in this subsection is
a normative capability of the running product, not a description of a screen.

8. The view supports pan, zoom in and out about the cursor, zoom to a window
   dragged on screen, zoom to extents, zoom to previous, and regenerate. Zoom to
   extents frames every visible entity in the drawing with all of it on screen.
9. Every entity renders with its own colour, linetype, lineweight, transparency
   and draw order. An entity whose colour is unset takes its layer's colour; an
   entity whose lineweight is unset takes its layer's lineweight.
10. Coordinates round trip exactly. A point entered at a fraction of a
    millimetre and a point entered kilometres from the origin are both stored and
    returned unchanged, in the same drawing, and snapping stays accurate at both
    of them. Geometry must not drift, fail to close, or refuse to snap far from
    the origin or at extreme zoom.
11. The workspace stays interactive with `20000` entities on one drawing across
    `40` layers: panning and zooming degrade by drawing less detail rather than
    stalling, and hit testing, selection and snapping stay immediate as the
    entity count grows. The seeded drawing `Site Survey Grid` is exactly that
    size, so the bar is something a person can open and pan rather than a figure
    nobody can reach.
12. The canvas presents model space, the drawing at real scale, and one paper
    space layout, a sheet carrying a viewport onto the model at a chosen scale.
    Tabs in the status bar switch between them, and a layer turned off inside the
    viewport stays visible in model space.

### Precision input, the command input and drafting aids

Professional drafting is exact to the unit, so the input aids are the product,
not a convenience.

13. **Object snaps.** As the cursor moves, the app offers the nearest meaningful
    point and marks it before the click: endpoint, midpoint, centre, node,
    quadrant, intersection, extension, insertion, perpendicular, tangent,
    nearest, apparent intersection and parallel. The offered point is the
    geometrically nearest meaningful one for the active snap set, at any zoom,
    against the whole entity set, and it resolves within a keystroke. Clicking
    while a snap is marked places the point exactly there, not at the pixel the
    cursor was over.
14. **Tracking.** Orthogonal mode constrains movement to the axes. Polar tracking
    constrains it to a configurable angle increment. Object snap tracking aligns
    to points already acquired and shows the alignment while it holds.
15. **Coordinate entry.** A point can be typed as an absolute coordinate, as a
    coordinate relative to the last point, as a polar distance and angle, or as a
    direct distance in the direction the cursor is pointing. Typed entry and
    clicked entry produce identical geometry for the same intended point.
16. **Grid and snap.** A visible grid and a snap resolution, each independently
    toggled from the status bar, along with orthogonal mode, polar tracking,
    object snap and lineweight display. Every toggle reads on or off at a glance
    and keeps its state for the session.
17. **The command input.** A text line that accepts every command by its full
    name and by its alias, echoes the running command's prompt and its options,
    accepts the answer, and recalls what was typed before. Every tool in this
    brief is reachable both from the toolbar and by name at the command input,
    and the two paths produce the same result.

### Drawing and editing

18. **Creation.** Lines, polylines with arc and width segments, construction
    lines and rays, circles by centre and radius, by two points, by three points
    and by tangent-tangent-radius, arcs by each of those methods, ellipses and
    elliptical arcs, rectangles with chamfer, fillet and width options, inscribed
    and circumscribed polygons, splines by fit points and by control vertices,
    points with named point styles, donuts, hatches and gradient fills with
    predefined and custom patterns, pick-point island detection, scale, angle and
    origin control, regions and boundary extraction, revision clouds
    rectangular, polygonal and freehand, and wipeouts.
19. **Associative hatch.** A hatch created inside a boundary follows that
    boundary: reshaping the boundary reshapes the fill, and the fill never has to
    be redrawn by hand.
20. **Modification.** Move, copy, rotate, scale, mirror, offset, and array
    rectangular, polar and along a path. Trim, extend, fillet, chamfer and blend
    curves. Stretch, lengthen, break, break at point and join. Explode, and
    cleanup of duplicated geometry.
21. **Grip editing.** Selecting an entity puts multi-function grips on it.
    Dragging one stretches, moves or rotates that vertex alone, and dragging the
    grip of a straight polyline segment converts that segment to an arc.
22. **Selection.** Window, crossing, fence, window polygon and crossing polygon,
    plus last, previous and all. Overlapping entities cycle on repeated clicks at
    the same point. A quick select filters the drawing by property, so "every
    entity on `Walls` whose colour index is `1`" is one operation.
23. **Match properties.** One tool paints a source entity's properties onto other
    entities, and only the properties that apply to the target kind are carried.
24. Every modification is refused for a `reviewer` and for anyone whose share
    access is `view` or `comment`, on the server, and the entity rows are
    unchanged by the refusal.

### Layers and object properties

25. **The layer manager**, a floating panel, creates, renames, deletes and
    reorders layers, and for each layer sets colour index, linetype, lineweight,
    transparency, a plot or no-plot flag and a description, and toggles on or
    off, freeze or thaw, and lock or unlock.
26. A layer name is unique within its drawing and the comparison ignores case, so
    a second layer named `walls` beside an existing `Walls` is rejected as
    invalid with a message naming the field, and no layer row is written.
27. Deleting a layer that still holds entities is rejected and says how many
    entities are on it. The layer named `Base` exists on every drawing and can be
    neither renamed nor deleted.
28. Layer states can be saved by name and restored, layers can be filtered by
    name and by property, any layer can be made current, and picking an entity
    can isolate, freeze or turn off the layer that entity sits on.
29. **The properties panel** inspects and edits the full property set of the
    current selection, including colour, layer, linetype, linetype scale,
    lineweight, transparency and thickness. A property may be set directly or may
    follow its layer or its containing block, and the panel shows which of the
    three is in force.
30. Turning a layer off removes its entities from the canvas and from selection
    while leaving every row intact; turning it back on brings them back
    unchanged.

### Annotation

31. **Text.** Single-line and multi-line text governed by named text styles, with
    font, height, bold, italic, underline, stacked fractions, bullets and
    numbering, columns, and a background mask.
32. **Dimensions.** Linear, aligned, angular, radius, diameter, arc length,
    ordinate, baseline and continued dimensions, plus multileaders, governed by
    named dimension styles and named leader styles. Centre marks and centrelines
    are included.
33. **Associative dimensions.** A dimension stores which entity it measures. When
    that entity moves or changes size, the dimension's stored measurement is
    recomputed and the displayed value changes with it. A dimension left showing
    its old number after its geometry moved is wrong.

### Blocks

34. Geometry can be saved as a named block definition with a base point, a unit
    and a description, and inserted into the drawing from the current drawing or
    from the account's library, with a preview before placing.
35. A block carries attributes, which are editable text fields inside the block,
    such as a room number. Those attributes can be extracted from every instance
    into a table.
36. A block with stored visibility states can be inserted and switched between
    those states. Authoring new dynamic parameters is out of scope and is listed
    in `## Constraints`.

### Versions in the cloud object store

Every saved version's bytes live in `minio`, and nowhere else.

The drawing exchange document is the app's own plain text format, extension
`.dxe`, UTF-8, one record per line, in this order: one `DRAWING` line carrying
the name and the units, one `LAYER` line per layer carrying its name, colour
index, draw order position and its on, frozen, locked and plotting flags, one
`ENTITY` line per entity carrying its kind, its layer name, its colour index or
the word `BYLAYER`, its linetype, its lineweight, and its coordinates, and a
final `END` line. A worked example of the first three lines:

```text
DRAWING Harbour Pavilion|millimeters
LAYER Base|7|0|on|thawed|unlocked|plotting
ENTITY line|Walls|BYLAYER|continuous|-1|0,0|10000,0
```

37. **Saving.** An explicit save captures every layer and entity as one drawing
    exchange document, writes those bytes to `minio` under
    `STORAGE_BUCKET` at the key
    `drawings/{drawing_id}/v{version_number}/{byte_digest}.dxe`, where
    `byte_digest` is the lowercase hex SHA-256 of the exact bytes written, and
    records a version row carrying that key, that digest, the author, the time,
    the entity count, and an optional label. A worked example of a key:
    `drawings/7/v3/9f2a4c1e8b07d5a3f61c92b48e0d7fa5c3b19e64d820af7513c6e9b0a41d27f8.dxe`.
38. Version numbers start at `1` and increase by exactly one. They are unique per
    drawing and never have a gap.
39. **The concurrent save.** A save names the version it started from. Two saves
    of the same drawing that both name the same starting version must not both
    succeed: exactly one is accepted, and the other is rejected with a message
    saying the drawing has moved on and naming the version that now exists. The
    rejected save writes nothing: no version row, no object in the bucket, no
    change to the drawing's current version.
40. A version is immutable once written. Restoring version `n` never rewrites
    `n`; it writes a new highest version carrying that geometry, attributed to
    whoever restored it.
41. **Autosave and recovery.** Unsaved work is captured automatically while
    editing. On reopening the drawing after a crash or a tab close, the autosave
    is offered back for recovery, naming when it was captured. Accepting the
    recovery restores that geometry; declining it discards the autosave and
    leaves the last saved version in force. An autosave never becomes a numbered
    version on its own.
42. **Version history** at `/drawings/{id}/versions` lists every version newest
    first with its number, its author's display name, its time and its label.
    Downloading a version returns exactly the bytes stored under its key, and the
    SHA-256 of what is returned equals the version's recorded digest.
43. **Compare.** Two versions of a drawing can be compared, and the result marks
    geometry added, removed and changed, each distinguished from the others by a
    different colour.

### Sharing, presence and live co-editing

44. **Inviting.** The owner of a drawing invites an account by its email address
    at `view`, `comment` or `edit`, from `/drawings/{id}/share`. Inviting an
    email with no account is rejected as invalid and names the field. Inviting
    somebody already invited changes their access instead of adding a second
    invitation. The owner can change or remove any access, and cannot invite
    themselves.
45. A shared drawing appears in the invitee's library immediately, marked with
    its owner and with the access they were given.
46. **Presence.** The workspace shows who else is in the drawing right now, by
    display name, and each person's colour is distinct from the others. Somebody
    who has left stops being shown within two minutes.
47. **Live co-editing.** When one editor saves a change to a drawing, that change
    appears in another editor's already-open workspace without that person
    reloading the page, and it appears within a few seconds of the save. Neither
    person's view is reset by the other's change: the second editor keeps their
    own pan, zoom, current layer and selection.
48. **Referential integrity under co-editing.** Concurrent edits resolve to a
    drawing that is still internally consistent. A dimension whose measured
    entity another person moved follows that entity and shows the new
    measurement. A block definition another person is still using cannot be
    deleted out from under them, and the attempt is refused with a message naming
    how many instances depend on it. A layer another person is drawing onto
    cannot be deleted out from under them either.
49. **Comments.** A comment is pinned to a point on the drawing, is shown as a
    marker at that point, and opens a thread. Threads carry replies and a
    resolved state set on the thread's first comment. A comment whose body is
    empty is rejected as invalid, inline, naming the field, and no comment row is
    written. Comments appear for everyone in the drawing without a reload, on the
    same terms as rule 47.
50. A `reviewer` shared at `comment` can write a comment and cannot write an
    entity. The same reviewer shared at `view` can write neither. Both refusals
    happen on the server, and both leave every row unchanged.

### Confidentiality of an unshared drawing

51. A drawing with no share rows is readable only by its owner. Every other
    account asking for it by its address, by its API endpoint, for its entities,
    its layers, its versions, its comments or its share list is refused, and the
    refusal reveals nothing about whether the drawing exists.
52. The saved bytes are protected with the drawing. A version's bytes are served
    only through the app's own authenticated download endpoint, and only to an
    account that may read that drawing. The bucket is never addressed directly by
    the browser, and no link that reaches an object in the bucket without passing
    that check is ever handed out.
53. The seeded drawing `Harbour Pavilion` is owned by Mira Vance and shared with
    nobody. Priya Raman must not be able to read it, its entities, its versions
    or its bytes by any means.

### Measure, markup and the assistant

54. **Measure.** Distance between two points, the radius of a curve, an angle,
    and the area and perimeter of a closed region, each reported in the drawing's
    units. A quick measure shows the nearby dimensions of whatever the cursor
    rests on without placing anything.
55. **Markup.** Freehand strokes, shapes, callouts and text notes drawn over the
    drawing for review. Markup is stored apart from the geometry, can be hidden
    as a group, and changing or deleting markup never changes an entity.
56. **The assistant panel**, titled `Draft Assistant`, is a docked side panel
    that answers a question about a command or about the current drawing and
    opens the matching help in context. It opens, docks, pops out, resizes and
    closes like every other floating panel.

### The public edge

57. **The privacy page** at `/privacy`, linked from the footer of every page a
    signed-out visitor can reach, states what Draftline stores about an account
    and about a drawing, where a drawing's bytes are kept, and how long a deleted
    drawing's versions are retained.
58. **The terms page** at `/terms`, linked from the same footer and linked from
    the signup form itself, states the terms of use.
59. **Form validation.** Every form in the product rejects invalid input inline
    before anything is written, names the field that is at fault in words next to
    that field, and leaves every other field's entry as the person typed it. A
    rejected form writes nothing.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | entry; resolves to the library when signed in, to sign-in when not | public |
| `/login` | sign in | public |
| `/signup` | open signup, creating a drafter | public |
| `/privacy` | what the product stores | public |
| `/terms` | terms of use | public |
| `/drawings` | the library, a card grid, newest first | drafter, reviewer |
| `/drawings/new/template` | create, step one: pick a template | drafter |
| `/drawings/new/units` | create, step two: choose units | drafter |
| `/drawings/new/name` | create, step three: name and create | drafter |
| `/drawings/{id}` | the workspace | owner, or shared at any access |
| `/drawings/{id}/versions` | version history, restore, compare | owner, or shared at any access |
| `/drawings/{id}/share` | invite, change and remove access | owner |

**Entry and redirects.** An unauthenticated request for a protected route lands
on `/login` with the destination remembered, and signing in continues to it.
Signing in with no remembered destination lands on `/drawings`. Signing out
returns to `/login`, and the workspace that was open is not reachable by going
back. A token that expires mid-edit does not discard the edit: the workspace says
the session ended, keeps what is on the canvas, and continues after a fresh
sign-in. A `reviewer` reaching a creation step or a share page is returned to the
library. An account reaching a drawing it neither owns nor was shared into is
returned to the library, told only that it is not available to them.

**Journeys.**

1. **Open and read.** Sign in as `drafter@example.com` with `deku-demo-pw-2026`.
   Land on `/drawings` and see `Harbour Pavilion` and `Rail Shed Section` as
   cards, newest first. Open `Harbour Pavilion`. The entry field fills the screen
   with the badge held centred inside its sweeping ring until the workspace is
   ready, then the drawing arrives: a ten-metre rectangle on `Walls`, a circle
   beside it, a linear dimension on `Dimensions` reading its long side, and a
   multi-line note on `Notes`. Zoom to extents frames all four.
2. **Draw precisely.** Type the line command's name at the command input. It
   prompts for a first point. Move the cursor near the rectangle's lower-right
   corner until the endpoint snap marks it, and click: the point lands exactly on
   the corner. Type a relative coordinate for the second point and press enter. A
   new line appears on the current layer in that layer's colour, and the status
   bar has been reading the cursor coordinate the whole time.
3. **Layer work.** Open the layers panel. Create `Services` at colour index `3`
   and make it current. Draw a circle; it arrives green. Turn `Walls` off: the
   rectangle and the first circle leave the canvas and the new circle stays. Turn
   it back on and they return unchanged.
4. **Save a version.** Save with the label `Setting out`. A confirmation says the
   version was saved and names it. `/drawings/1/versions` now lists version `3`
   by Mira Vance with its time and label. Download it and receive the drawing
   exchange document whose first line reads `DRAWING Harbour Pavilion|millimeters`.
5. **Share and comment.** Open `/drawings/2/share` for `Rail Shed Section` and
   invite `reviewer@example.com` at `comment`. Sign in as `reviewer@example.com`,
   find `Rail Shed Section` in the library marked as Mira Vance's, open it, click
   a point on a wall and write a comment. The marker appears at that point and
   the thread lists it. Try to drag a line: the canvas refuses and says the share
   gives comment access only.
6. **Confidentiality.** Still signed in as `reviewer@example.com`, ask for
   `Harbour Pavilion` by its address, then for its entities, then for its version
   download. Every one is refused and none of them confirms the drawing exists.
7. **Two editors, one drawing.** Mira Vance and Owen Blake are both in `Rail Shed
   Section` at `edit`. The presence strip names both. Owen moves a wall and
   saves. Within a few seconds the wall moves in Mira's open workspace, her pan,
   zoom and current layer untouched, and the dimension measuring that wall shows
   its new length. Mira, who began her own save from the older version, is
   refused with a message that the drawing has moved on and is offered the newer
   version; nothing of her rejected save reached the bucket.

**States.** A library with no reachable drawings says so and offers the first
creation step. A drawing with no entities shows an empty canvas with its grid and
a line naming the command input. A version history with one version says the
drawing has been saved once. A comment list with no threads says so. Entry shows
the black field, the centred badge and the sweeping ring until the workspace is
ready, and each panel shows its own quiet placeholder rather than snapping into
place. A refused save, a refused edit and a refused read each say what happened
in words and leave the canvas exactly as it was. No route in the product ever
shows a blank screen or an unhandled error.

## UI/UX notes

The north star: somebody opening this should understand within a second that the
drawing is the product and the interface is scaffolding around it, quiet and out
of the way, dense with exactly the controls a drafter reaches for without
looking. The register is an operational tool for a trained discipline: quiet,
utilitarian, work-focused, built for scanning and for repeated action many times
a minute. No hero, no editorial composition, no decoration standing in for
content. The one place atmosphere is allowed is the entry screen, and it earns it
by promising the dark canvas that follows.

Because the product must support speed and repetition, it takes density over
breathing room, large hit areas over generous margins, and controls that never
move between sessions. Because it must guide at exactly two moments, creating a
drawing and inviting a colleague, those two screens carry one obvious next action
and quieten everything else; every other screen leads with the canvas. Because it
must reassure while a save is in flight, nothing on the canvas moves during a
save and the outcome is stated in words rather than implied by something going
quiet. Restraint in the chrome over presence in the chrome: a consumer drawing
tool would rationally choose a coloured branded frame, and this one must not,
because the drawing carries the only saturated colour on screen. Words over icons
wherever a command has a name, because the discipline's vocabulary is the fastest
input a trained user has. Continuous readout over on-demand readout: the cursor
coordinate, the current layer and the drafting toggles are always visible, never
behind a menu.

**Two colour worlds, and they must never be confused.** The interface chrome is
near-neutral and light, in four roles. The dominant chrome colour, carrying icons
and secondary text, is a light cool neutral, present enough to read and recessive
enough never to compete with geometry; it is the most-used colour in the product
by a wide margin. Panels and raised surfaces sit on a near-white neutral, plainer
and lighter than the field behind them, and the two must stay visibly separate
without a border drawn between them. Strong text, headings and the current value
in a field take a deep cool neutral, which is the only genuinely dark ink in the
chrome. Selection is a near-white, muted blue wash laid over what is selected: it
is translucent, so geometry stays legible through it, and it appears nowhere
except to mean that something is selected. Nothing in the chrome is saturated; if
a chrome surface reads as coloured at a glance, it is wrong.

The drawing colour index is the second world and belongs to entities and layers,
never to the interface: index `1` is a mid, vivid red and its near variants,
index `2` a light, vivid orange, index `3` a deep, soft green, index `4` a light,
soft lime in the yellow green band, index `5` a near-white, muted blue, index `6`
a mid, vivid violet with a muted magenta variant, and index `7` a near-white
neutral. The model background
is a near-black neutral, which is not a theme choice but the field the index
colours read correctly against. Alongside the seven indices the product exposes
the standard named colour table, so a colour can be asked for by name rather than
by number: near-white cool neutrals, near-white warm neutrals, near-white muted
oranges, a mid soft red, a light soft orange, a mid vivid orange, a light vivid
orange, light neutrals and the near-black neutral. Asking by name and picking an
index reach the same result. The exact shades are yours, so long as the chrome
stays unsaturated, the index stays saturated, and no index colour ever appears on
a chrome surface.

**Type.** The typography is one neutral sans across the whole chrome, named with
a fallback stack that holds the layout before and without the web font, and no
font binary shipped. Three roles, told apart by size and weight relative to one
another
rather than by family: interface body, by far the most used, comfortable at a
desk and set so a dense panel of them still scans; panel and dialog headings,
noticeably larger than body at the same weight, so a heading reads as a title by
size alone rather than by shouting; and emphasised labels, only slightly larger
than body but heavier, used for the assistant panel's title and the few labels
that must be found without reading. That weight contrast is the only one in the
chrome, so spending it anywhere else spends it. Coordinates, dimensions,
lineweights and any column of measurements line up digit under digit wherever
amounts stack, so two numbers can be compared by their shape.

**Shape, depth and density.** Corners are softened at two distinct amounts and no
others: the small square icon buttons of the toolbars are barely rounded, just
enough not to read as cut, and floating panels are softened more, enough to read
as separate objects lying on the canvas. Nothing else in the product is rounded.
Depth is shallow and deliberate: floating panels and their drag handles sit above
everything and the canvas owns the entire rest of the screen. A panel lifts off
the drawing on a soft, diffuse shadow so it is never lost against busy geometry,
and that shadow is the only depth cue in the product. Density is compact: a full
layer list and a full property set fit on screen together without scrolling, and
toolbar buttons sit shoulder to shoulder so the hand learns where they are.

**Components and their states.** The icon button is the toolbars' unit: small,
square, barely rounded, drawing a single-colour vector glyph in the chrome grey,
with five states, resting, pointed-at, pressed, focused and unavailable. Pointing
at one moves its shadow, its background and its glyph colour together to a
settled state, while the focus ring is the deliberate exception and snaps in far
faster, because a keyboard user needs it the instant focus lands. Unavailable is
never signalled by colour alone. The floating panel has a softened corner, a
near-white surface and a lifted shadow, and every one can be docked or popped
out, moved, closed and resized by a handle. The resize handle is a thin strip
carrying a grip of pale diagonal lines, partly transparent at rest and firming
toward full presence when pointed at, drawn rather than loaded as an image. The
status bar toggles for snap, grid, orthogonal mode, polar tracking, object snap
and lineweight display each read on or off at a glance, announce their state, and
stay in the same place forever. Escape closes whatever is open, and a destructive
action confirms first.

**Motion.** The character is eased: considered entrance and exit, movement that
reads as a designed interface rather than a machine. Everything in the chrome
moves at one speed on one curve, settling rather than starting sharply, and
nothing uses a different speed to feel special. Exactly three moments carry
motion. A control settles: its shadow, its background and its text move together
to the new state when it is pointed at or pressed, with the focus outline
snapping in much faster than the rest. A glyph recolours, quicker than the
control it sits in. And the loading mark sweeps: on the entry screen a thin ring
turns continuously around the badge and loops until the workspace is ready, which
is the one motion a visitor sees before signing in. A few interface moments may
overshoot their target slightly and settle back for a little life, and that is a
scoped exception, never the base character. Nothing on the canvas animates at
all: geometry appears where it is drawn, immediately, because a drafter judging a
snap cannot be shown a shape that is still arriving. Under a reduced-motion
preference the ring holds still and reports progress without turning and every
chrome transition resolves to its end state at once; nothing is removed by the
preference, it only stops moving.

**Responsive behaviour.** This is not a page that reflows into a phone column. The
workspace fills the browser window at any viewport and gives as much of it as
possible to the canvas; as the window narrows the chrome yields first, panels
collapse to their edge and can be brought back, and the canvas never falls below
the majority of the screen. The layout holds at every width between a small
laptop and a large desktop, with no width at which a panel overlaps the status
bar or a toolbar truncates without a way to reach what it hid. At a narrow
viewport nothing overflows sideways and every navigation target stays reachable.
On a touch screen the canvas takes two-finger pan and zoom, a tap to select and a
long press for a context menu, with every target comfortably sized for a
fingertip. The public pages, sign-in, signup, privacy and terms, are ordinary
documents and do reflow to a single readable column.

**Accessibility floors.** Body text and its background meet WCAG AA contrast, and
the chrome grey is verified against every surface it sits on and lifted where it
falls short. The command input is a complete keyboard path to every command in
the product and is its primary accessibility affordance: a command that exists
only as a toolbar button is a hole in it. Every panel, dialog, toggle and the
assistant are reachable by keyboard navigation with a visible focus ring. Every
icon-only control carries a name, and so does every presence marker and every
comment marker. Meaning is never carried by colour alone: a layer that is off,
locked or frozen says so in text as well as in its swatch. Touch targets are
comfortably sized.

**What this must not look like.** Not a marketing composition: no hero, no
oversized heading, no illustration where the working interface belongs. Not a
page dominated by one hue family with no second signal. Not decoration standing
in for content: every glyph names a command and no shape exists to fill a space.
Not a generic dashboard template with a drawing pasted into the middle, because
the panels float over the canvas and are moved by the user rather than sitting as
fixed cards in a grid.

## Technical requirements

The browser receives an application shell on first paint and every later screen
is assembled in the browser from JSON served by the app's own API. This is the
coherent model for the product: the workspace is one screen whose canvas holds
continuous interactive state, and a page load in the middle of a drawing session
would discard it.

- **Frontend:** Preact with Vite, built to a production bundle.
- **Backend:** Litestar (Python), serving the HTTP API on the same origin under
  the `/api` prefix.
- **Database:** PostgreSQL, reached at `DATABASE_URL`.
- **Object store:** `minio`, reached at `STORAGE_ENDPOINT` with `STORAGE_BUCKET`,
  `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`.
- **Auth:** email and password implemented by the app, with bearer tokens.
  Passwords hashed. Tokens expire after 24 hours.
- **Health:** `GET /api/health` returns `200` once the app is ready.
- **Logging:** request logs to stdout.

Read every host, port and credential from the environment; never hardcode one.
The backing services named in this brief are already running and reachable at
those environment variables. Do not download, install, compile or start a copy of
either of them.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor: the only backing services available in this environment are
PostgreSQL and `minio`, and reaching for anything else is a contract violation.

**Drawing bytes.** A saved version's bytes exist as a real object in the `minio`
bucket at the key scheme in `## Core features`, and nowhere else. Bytes held on
the app container's filesystem, or in a database column, or assembled on demand
from the entity rows at download time, are all a contract violation: the
downloaded bytes must be the bytes that were stored, and their SHA-256 must equal
the digest recorded with the version.

**Protected reads.** A version's bytes reach the browser only through the app's
own authenticated download endpoint, which checks that the requesting account may
read that drawing before it serves anything. No address that reaches an object in
the bucket without passing that check is ever issued to a client.

**Live reach.** A change one editor saves reaches another editor's already-open
workspace within a few seconds without that person reloading, and presence
reflects who is in the drawing now. How that reach is achieved is your design
work; no additional backing service is available for it.

**Responsiveness bar.** The app stays interactive with `20000` entities on one
drawing across `40` layers, and with `200` versions in one drawing's history.
First readiness is covered by the entry screen, which stays up only while real
work is being done and is driven by real progress rather than a fixed wait. Once
loaded, panning and zooming stay smooth by drawing less detail rather than by
stalling.

**Discovery.** `GET /sitemap.xml` lists every public route in the product, and
`GET /robots.txt` points at that sitemap by its absolute address. Every public
route declares its own social preview title and image in the document head, no
two public routes declare the same pair, and every declared preview image
resolves with a success response and an image content type.

## Data model

Nine tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account
so a grader can sign in.

### accounts

`id`, `email` (unique, lowercased on write), `password_hash` (never returned by
any endpoint), `display_name`, `role` (`drafter` or `reviewer`), `created_at`.
Signup always writes `role` as `drafter`; a `reviewer` exists only by seed.

### drawings

`id`, `owner_id`, `name`, `units` (`millimeters`, `meters`, `inches` or `feet`),
`template` (`blank`, `architectural` or `mechanical`), `current_version`
(`0` before the first save), `created_at`, `updated_at`.

### layers

`id`, `drawing_id`, `name`, `color_index` (`1` to `7`), `linetype`, `lineweight`,
`transparency`, `visible`, `frozen`, `locked`, `plotting`, `description`,
`position` (draw order, ascending). `name` is unique within a drawing,
case-insensitively. `position` is unique within a drawing. Every drawing carries
a layer named `Base` that cannot be renamed or deleted.

### entities

`id`, `drawing_id`, `layer_id`, `kind` (one of `line`, `polyline`, `circle`,
`arc`, `rectangle`, `polygon`, `ellipse`, `spline`, `point`, `hatch`, `cloud`,
`text`, `dimension`, `markup`, `block_instance`), `points` (an ordered JSON list
of `{"x": <number>, "y": <number>}` in drawing units), `color_index` (null means
the colour follows its layer), `linetype` (`continuous`, `dashed`, `center` or
`hidden`), `lineweight` (hundredths of a millimetre; `-1` means follow the
layer), `transparency`, `draw_order`, `properties` (a JSON object carrying the
kind's own fields, such as `radius`, `text`, `height`, `pattern`, `measures` and
`measured_value`), `created_at`, `updated_at`.

Coordinates are stored as given and are never rounded on write: a value entered
at a fraction of a millimetre and a value entered kilometres from the origin both
round trip exactly, in the same drawing. `measured_value` on a `dimension` is
derived from the entity named in `measures`, recomputed whenever that entity
changes, and never left stale.

### versions

`id`, `drawing_id`, `number`, `author_id`, `label` (null for an automatic save),
`object_key`, `byte_digest` (lowercase hex SHA-256 of the stored bytes),
`entity_count`, `created_at`. `number` starts at `1`, increases by exactly one,
is unique per drawing, and never has a gap. A version row is never updated after
it is written.

### shares

`id`, `drawing_id`, `account_id`, `access` (`view`, `comment` or `edit`),
`created_at`. `(drawing_id, account_id)` is unique. A drawing's owner never has a
share row for their own drawing.

### comments

`id`, `drawing_id`, `author_id`, `parent_id` (null for the first comment in a
thread), `anchor_x`, `anchor_y`, `body` (non-empty), `resolved` (meaningful on a
thread's first comment only), `created_at`.

### presence

`id`, `drawing_id`, `account_id`, `last_seen_at`. `(drawing_id, account_id)` is
unique. An entry whose `last_seen_at` is more than two minutes old is not
present.

### undo_steps

`id`, `drawing_id`, `account_id`, `position` (ascending within an account and
drawing), `inverse` (a JSON record of what restores the exact prior state of
every entity the step touched), `undone`, `created_at`. One step covers every
entity a single action changed, including the dependents that action rippled
into, so undoing it restores all of them together or none of them. Redo replays
the same step forward.

### Invariants

- `drawings.current_version` always equals the highest `versions.number` for that
  drawing, or `0` when the drawing has none.
- Two saves of one drawing that both name the same starting version resolve to
  exactly one accepted version. The other is rejected, no version number is
  skipped, no version row is half-written, and no object is left in the bucket
  for the rejected save.
- No entity references a layer belonging to a different drawing.
- Deleting a layer that still holds entities does not happen, and neither does
  deleting a block definition that still has instances.
- A reviewer never owns a row in `drawings`, `entities`, `layers` or `versions`.

### Seed data

Three accounts as listed in `## User roles`, with the display names Mira Vance,
Owen Blake and Priya Raman.

Four drawings, all in `millimeters`:

| Name | Owner | Current version | Shared with |
|---|---|---|---|
| `Harbour Pavilion` | Mira Vance | `2` | nobody |
| `Rail Shed Section` | Mira Vance | `1` | Priya Raman at `comment` |
| `Kiln House Elevation` | Owen Blake | `1` | nobody |
| `Site Survey Grid` | Mira Vance | `1` | Priya Raman at `view` |

`Harbour Pavilion` carries the layers `Base` at colour index `7`, `Walls` at `1`,
`Dimensions` at `3` and `Notes` at `6`, in that draw order, and the geometry: one
closed rectangle on `Walls` ten metres along its long side, one circle on
`Walls`, one linear dimension on `Dimensions` measuring that long side, and one
multi-line text note on `Notes`. Every seeded version's bytes exist as an object
in the `minio` bucket at that version's recorded key.

`Site Survey Grid` is the density fixture. It carries exactly `40` layers and
exactly `20000` entities, generated in code rather than shipped as a file: lines,
polylines, circles and text spread across the layers so every layer holds
geometry and no layer is empty. It exists so the responsiveness bar above is an
observable property of a drawing somebody can open, and so that turning a layer
off on it visibly removes that layer's share of the drawing.

Seeding must be idempotent: restarting the app must not duplicate rows and must
not write a second copy of any object.

## Front-end specification

This section carries the visual detail in full. It states no rule that is not
already a requirement elsewhere; it says what the surfaces are and how they
behave.

### The entry screen and its preloader

The preloader is a near-black neutral field filling the window, with nothing on
it but the Draftline badge, centred and holding dead centre at every window size,
inside a thin ring that sweeps continuously around it. No navigation, no words, no chrome.
The badge is a small softened square in the product's red carrying a monogram
over a short label, both in a near-white neutral. Badge and ring are both drawn
as inline vector geometry rather than loaded as image files, so no animation file
and no logo binary is needed. The field is the same near-black the model space
opens into, so the entry screen is already showing where the user is headed.
Entry does not scroll: the page height is the window height, always.

### The workspace frame

A fixed top bar spanning the window carries the badge, the current drawing's
name, the tool groups, and the account and share controls at the right. It owns
the small square icon buttons.

A left tool group holds the creation and modification tools, grouped by what they
do rather than alphabetically, each a single icon button with a name available on
hover and to a screen reader.

Floating panels for layers, properties, blocks and the assistant lie over the
canvas. They are dockable, poppable, movable, closable and resizable.

The iconography is inline vector geometry throughout, never image files, so every
glyph stays sharp at any size and can be recoloured with the rest of the chrome.
Every icon is drawn on one small square grid as stroked or filled paths in a
single colour. Two glyphs are specified exactly because they are the panel
furniture: the dock glyph is a filled square occupying one quadrant with a
rectangular cut-out inside it, completed by an outward corner, which is the
conventional mark for a docked or picture-in-picture panel; the close glyph is a
single diagonal cross with squared ends. Every remaining glyph, the whole drawing
and editing toolset, follows the same construction.

A bottom status bar carries the cursor coordinate readout, the drafting toggles
for snap, grid, orthogonal mode, polar tracking, object snap and lineweight
display, and the model and paper space layout tabs.

The panel resize handle is a thin strip carrying a grip of pale diagonal lines,
partly transparent at rest, drawn as a repeating diagonal pattern rather than as
an image, and brightening toward full presence when it is pointed at.

### The canvas surface

The canvas fills everything the frame does not. It renders in real-world
coordinates and holds its own pan and zoom. Entity appearance matches what a
desktop drafting tool would draw: the colour comes from the drawing colour index
or from the entity's layer, the linetype pattern is drawn along the geometry,
lineweight is drawn at the stated width when lineweight display is on and at a
uniform hairline when it is off, transparency is honoured, and draw order decides
what covers what.

Level of detail is a rendering decision, not a data decision: when the view is
pulled far out, fine geometry may be simplified or dropped from the frame, and
nothing is dropped from the drawing.

Snap markers appear at the offered point before the click, each snap kind drawn
as its own distinct marker shape so the kind is readable without colour.
Tracking alignments are drawn as thin guide lines from the acquired point, and
they disappear the moment the alignment stops holding.

### The library

`/drawings` is a card grid under a persistent left sidebar carrying the account,
the library and the sign-out. A card shows the drawing's name, its units, its
current version number, when it last changed, and its owner when that is somebody
else, plus a small preview of the drawing's extents. Cards are ordered newest
first and the grid reflows by width without a card ever being cut off.

### The creation sequence

Three screens, one per address. Each shows where it is in the sequence, carries
one obvious next action, and lets the previous step be returned to without
losing what was already answered. Nothing is created until the last step.

### Feedback and the two readouts

There are two feedback surfaces and they do different jobs. The status bar is the
continuous readout: the cursor coordinate, the current layer, the running
command's prompt, and the drafting toggles, always present, never interrupting.
A short confirmation appears near the edge of the screen for a discrete outcome
that has just happened, such as a version saved, a colleague invited, or a save
refused because the drawing moved on. It states the outcome in words, can be
dismissed, and never covers the status bar or the command input.

### The assistant panel

A docked side panel titled `Draft Assistant`, opened from the top bar, carrying a
question field and the answers it has given in this session. It behaves like
every other floating panel: dockable, poppable, movable, closable, resizable by
the same grip.

### Procedural assets, no binaries

Every asset in this product is drawn in code. Name a font family and give it a
real fallback stack rather than shipping a font file. Draw the badge as a
softened rectangle filled with a red from the drawing palette, carrying a
near-white monogram and a near-white lower label, sized to sit inside the ring.
Draw the sweeping loader as a stroked ring with a rotating arc on the near-black
field. Rebuild the resize grip from the repeating diagonal pattern described
above. Draw every tool icon as inline vector geometry in the style of the dock
and close glyphs: single colour, one small square grid, stroked or filled paths,
recoloured by the chrome grey. Generate the seeded drawings' geometry in code,
rather than shipping a sample drawing file.

### Copy that is pinned

- The browser tab of every page reads:
  `Draftline Web App, Online CAD Editor and Viewer`.
- The assistant panel's title reads `Draft Assistant`.
- Everything else the interface says is the standard vocabulary of the drafting
  discipline, the names of the commands and the tools, and it is kept as it is.

## Constraints

Single tenancy: one Draftline, no organisations, no workspaces above the account.

Not built, and each for a stated reason. **Reading or writing the industry binary
drawing format**, because it is proprietary, undocumented, version evolving and
bit packed, and an approximate implementation corrupts real drawings; the
product's own plain text drawing exchange document is the only format it reads
and writes. **Three-dimensional solid modelling and boolean operations** on
solids, union, subtract and intersect, and any unified rendering of flat drafting
and shaded or wireframe three-dimensional views in one pipeline, with visual
styles, hidden line removal and a camera. **A variational geometric constraint
solver**, and with it the authoring of new dynamic block parameters; inserting a
block, editing its attributes and switching between its stored visibility states
all stay. **Massive assemblies** of thousands of instanced parts with demand
loading and unloading. **External references** to other drawings with attach,
detach, reload, unload, overlay, path control and clipping, **raster image
underlays**, and **page based document underlays** with geometry import.
**Plotting** to a printer, plot style tables mapping colour and lineweight to
output, multi sheet publishing, and export to a page based document or to a
foreign exchange format. **Tables with cell formatting, merges and formulas**,
**auto updating fields**, **annotative scaling** across viewport scales, and
**geometric tolerance symbols**.

No payment, no subscription, no entitlement tier: every signed-in account gets
the whole editor. No email, no messaging, no notification of any kind. No native
desktop or mobile application. No third party storage connector beyond the one
object store named in this brief. No external network call at runtime.

No borrowed identity ships. No third party brand name, no proprietary font
binary, no logo file and no sample drawing file is included; every asset is drawn
in code. Any class-name prefix your tooling generates is a framework artefact and
must not carry a product name.

There is no separate asset host: no font or media delivery host, no third party
media host, and no address outside this app's own origin is fetched at runtime.
There is no analytics id and no analytics of any kind; nothing about a visitor is
sent anywhere.

The stack an existing product was observed to use is informational and is not a
requirement here. Build the capabilities above in the stack named in
`## Technical requirements`, and take no library, component kit, rendering
approach or version from anything that was observed elsewhere.

The performance bar is part of the specification: the app must stay responsive at
`20000` entities on one drawing, `40` layers on one drawing, and `200` versions
in one drawing's history. Performance work that reaches those figures by dropping
data rather than by drawing less of it is a failure of the bar, not a way of
meeting it.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`, `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of
  the shell. An ordinary background job dies with its shell, and the app will not
  be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy
  of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{"email", "password", "display_name"}` | the account and a bearer token |
| `POST /api/auth/login` | `{"email", "password"}` | the account and a bearer token |
| `GET /api/auth/me` | none | the signed-in account |
| `GET /api/drawings` | none | a top-level JSON array of reachable drawings, newest first |
| `POST /api/drawings` | `{"name", "units", "template"}` | the created drawing |
| `GET /api/drawings/{id}` | none | the drawing with its layer list |
| `GET /api/drawings/{id}/entities` | optional `layer_id`, `kind` | a top-level JSON array of entities |
| `POST /api/drawings/{id}/entities` | `{"layer_id", "kind", "points", "color_index", "linetype", "lineweight", "properties"}` | the created entity |
| `PATCH /api/drawings/{id}/entities/{entity_id}` | any writable entity field | the updated entity |
| `DELETE /api/drawings/{id}/entities/{entity_id}` | none | an empty success |
| `GET /api/drawings/{id}/layers` | none | a top-level JSON array of layers in draw order |
| `POST /api/drawings/{id}/layers` | `{"name", "color_index", "linetype", "lineweight", "description"}` | the created layer |
| `PATCH /api/drawings/{id}/layers/{layer_id}` | any writable layer field | the updated layer |
| `DELETE /api/drawings/{id}/layers/{layer_id}` | none | an empty success |
| `GET /api/drawings/{id}/versions` | none | a top-level JSON array of versions, newest first |
| `POST /api/drawings/{id}/versions` | `{"base_version", "label"}` | the created version, carrying `number`, `object_key` and `byte_digest` |
| `GET /api/drawings/{id}/versions/{number}/download` | none | the stored bytes of that version |
| `POST /api/drawings/{id}/versions/{number}/restore` | none | the new highest version |
| `GET /api/drawings/{id}/versions/compare` | `from`, `to` | added, removed and changed entities |
| `GET /api/drawings/{id}/shares` | none | a top-level JSON array of shares |
| `POST /api/drawings/{id}/shares` | `{"email", "access"}` | the created or updated share |
| `DELETE /api/drawings/{id}/shares/{share_id}` | none | an empty success |
| `GET /api/drawings/{id}/comments` | none | a top-level JSON array of comment threads |
| `POST /api/drawings/{id}/comments` | `{"parent_id", "anchor_x", "anchor_y", "body"}` | the created comment |
| `POST /api/drawings/{id}/comments/{comment_id}/resolve` | none | the updated thread |
| `GET /api/drawings/{id}/presence` | none | a top-level JSON array of who is in the drawing now |
| `POST /api/drawings/{id}/presence` | none | the caller's refreshed presence entry |
| `POST /api/drawings/{id}/undo` | none | the entities the step restored |
| `POST /api/drawings/{id}/redo` | none | the entities the step reapplied |
| `GET /api/health` | none | `200` |

Field names are exact. Every list endpoint returns a top-level JSON array. A
successful call returns the named resource or shape; an invalid or unauthorized
call is rejected as a client error, never as a server error and never as a silent
success, and carries a message naming the reason. Bearer auth is required on
every endpoint except signup, login and health.

### No mocks

`minio` is the only place a saved version's bytes live. An in-memory dictionary
of drawing bytes, a directory of `.dxe` files on the app container's own disk, a
column in PostgreSQL holding the document, a download endpoint that rebuilds the
document from the entity rows instead of reading the object it recorded, and a
stubbed success response the app returns to itself are all contract violations,
however correct the workspace looks. The named provider is the fact: the app's UI
and its own tables can only reflect what lives in the provider, never substitute
for it.

## Definition of done

A drafter can sign in, open a drawing, snap a new line exactly to the corner of
an existing one, put it on a named layer, and save a version whose bytes are
retrievable from the cloud store byte for byte. A colleague invited at comment
can open that drawing, measure it and pin a comment to a point, and cannot change
a single line of it. A drawing nobody was invited into stays unreadable to
everybody else, bytes included. When two people save the same drawing from the
same starting version, one save is accepted and the other is told the drawing has
moved on.
