# Pixelary

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, draw a piece of pixel art without making an account, publish it to the
gallery, and see it credited on their own artist page, without hitting an error
page.

A different stranger, signed in as anybody else, must not be able to read a
private piece's artwork by any means, including by asking the object store for
it directly. The published artwork must exist as real bytes in the object store
at its pinned key: a copy on the app container's own disk does not count, and
neither does a row that claims an upload happened.

## Overview

Pixelary is two products under one name, and the relationship between them is
the product. The tool is a free pixel-art editor that runs in a browser with no
account and no installation. The community is a gallery, a following graph,
comments, topics, contests and challenges, built around what people make with
the tool. Either one alone is not the product.

The site's job is to get somebody from arriving to drawing in one click, and
then from drawing to posting. The drawing action appears in the chrome on every
route, in the hero, and again on the not-found page.

Five audiences arrive here. Somebody who wants to draw right now asks "can I
just start?" and is served by the drawing action, with no account required. A
young artist building an audience asks "where do I post this?" and is served by
profile galleries and the feeds. A browser with no intention of drawing asks
"show me something good" and is served by the topic cards and the artwork grid.
A teacher or a parent asks "is this safe for a class?" and is served by a
parents and teachers page linked from the hero. A game developer asks "can I
export a sprite sheet?" and is served by the export formats and the embed
surface.

The genuinely hard part is that a piece of artwork has three different kinds of
existence at once, and they must never disagree: a document the editor owns, a
stored object addressed by the hash of its own bytes, and a gallery row that
decides who may see either. A piece made private must leave every feed, every
tag listing, every search result and every embed, and its stored object must
stop answering anybody but its author, all from one action.

Pixelary deliberately is not several things. There is no real-time collaborative
drawing session, no direct messaging, no native application, no advertising and
no third-party script of any kind. There is no image-similarity search: you
cannot upload a picture and find visually similar ones, and that refusal is a
requirement rather than an omission, because on a site with a young audience a
general reverse-image lookup is a tool for finding one person's work across the
whole site. The forums, the shop, the hiring board and the online comics exist
as navigation entries that resolve to the not-found page; they are not built.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Visitor (no account) | Draw in the editor, use every tool, save to their own device, export every format, read public pieces, read profiles, search | **Cannot publish, like, comment, follow or remix.** **Cannot read any piece that is private, pending, restricted or removed** |
| `reader` | Everything a visitor can, plus like, comment, follow, mute and block, and read their own notifications | **Cannot publish a piece.** **Cannot read another account's private or unlisted work.** **Cannot change another account's piece** |
| `author` | Everything a `reader` can, plus publish, remix, set a piece's visibility, edit and delete their own pieces, and delete comments on their own pieces | **Cannot change, delete or unpublish another author's piece.** **Cannot read another author's private work.** **Cannot alter a moderation decision** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a `reader` session
to any `author`-only endpoint must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged.

Signup is open. Anybody may create an account from the sign-in modal, and an
account is not required to draw, to save locally or to export.

An age is collected at signup and stored as a date of birth, never as a computed
age, so an account changes state on the right day with no migration. An account
below the local age of digital consent gets a restricted mode: its profile is
not indexed and does not appear in listings, it is reachable only by its direct
address, its follower and following lists are private by default, it receives no
messages from strangers, and it cannot post publicly without a guardian action.
Those restrictions lift automatically on the transition day and the account is
told what changed. Work posted while restricted stays restricted until the
account republishes it deliberately.

Seeded accounts, all with the password `deku-demo-pw-2026`:

| Email | Handle | Display name | Role |
|---|---|---|---|
| `author@example.com` | `nova` | `Nova Reyes` | `author` |
| `author2@example.com` | `bram` | `Bram Okafor` | `author` |
| `reader@example.com` | `pilot` | `Pilot Vance` | `reader` |

## Core features

### Auth

Email and password with bearer tokens. Passwords are stored hashed with a
memory-hard function using a unique salt per account, and the cost parameters
are stored beside the hash so they can be raised later; a sign-in against a hash
below current policy rehashes it. The unknown-account path and the wrong-password
path take the same time and return the same message, and signup, reset and
sign-in never reveal whether an address is registered.

1. `POST /api/auth/signup` takes a display name, an email address, a password and
   a date of birth, and returns the new account with a bearer token.
2. `POST /api/auth/login` returns a short-lived access token and a long-lived
   refresh token.
3. Refresh tokens rotate on every use and form a family. Presenting a refresh
   token that has already been exchanged means the family is compromised: the
   whole family is revoked at once, every session opened under it ends, and the
   account is told which device was affected. Refusing the reused token while
   leaving the rest of the family alive is not acceptable. A retried exchange
   inside a grace window of `10` seconds is not treated as theft.
4. Changing a password revokes every session except the acting one.
5. A second factor is offered: time-based codes that are single use within their
   window, plus ten single-use backup codes.

### The editor

The editor works with no account and with no network. It is a separate thing
from the gallery: it must remain fully usable when every other part of the
service is unavailable, so it must not depend on the gallery's data layer.

1. Three coordinate spaces exist and must never be confused: the document space
   of whole art pixels, the screen space of layout pixels, and the device space
   of physical pixels. Converting a screen position to a document position
   rounds downward, never toward zero: with the artwork panned so its left edge
   is off screen, painting at document column minus one and at document column
   zero must produce two distinct pixels, not one double-width column.
2. The drawing surface's backing store is sized by the device pixel ratio, the
   ratio is read at paint time rather than cached at start-up, and image
   smoothing is off. A one-pixel checkerboard drawn at zoom `1` on a double
   density display must leave every device pixel fully one colour or the other.
3. Panning is snapped to a whole multiple of the zoom whenever the zoom is `1`
   or greater. Panning by half of a document pixel at zoom `8` must leave the
   rendered edges unchanged.
4. Zoom runs from `0.125` to `64`, in powers of two below `1` and then the steps
   `1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64`. The default is the largest step
   at which the whole artwork fits with a margin. Zooming about a point is
   computed fresh from the pointer's screen position every time: zooming in
   twenty notches and out twenty notches on a fixed point must leave the same
   document coordinate under the pointer as at the start.
5. Upscaling at zoom `1` and above is nearest neighbour. Downscaling below zoom
   `1` is an area average, not nearest neighbour: a one-pixel outline rendered at
   zoom `0.5` must still be visible on all four sides. This is the same code path
   that makes gallery thumbnails.
6. The render order, back to front, is the transparency checker, the composited
   artwork, the onion skin, the selection marching ants, the tool preview, the
   pixel grid, and the cursor and brush outline. The checker is drawn in document
   space so it moves with the artwork rather than crawling under it while you
   pan. The grid and the ants are drawn in screen space and are exactly one
   device pixel wide at every zoom. The pixel grid is hidden below zoom `8`.
7. Each layer is stored as tiles of `64` by `64` document pixels. A tool
   operation reports a dirty rectangle and only the intersecting tiles are
   recomposited. The composite is cached per tile and invalidated by a change to
   any layer within it, by a layer visibility or blend change, and by a frame
   change. Painting is coalesced to one repaint per animation frame. A tile that
   has never been drawn to is not allocated, so an empty `4096` by `4096`
   document costs its tile index and nothing else.
8. Every pointer move consumes the full list of coalesced positions the browser
   holds, not only the most recent one, and consecutive samples are joined by the
   line algorithm rather than painted as isolated dots. A fast diagonal must be
   an unbroken line. Predicted positions may drive the preview overlay only and
   are never committed. Pointer capture is taken on pointer down and released on
   pointer up or cancel, so a stroke that leaves the surface still ends
   correctly. One finger draws; two fingers pan and zoom, and the transition from
   one contact to two discards the stroke in progress rather than committing it.
   Stylus pressure may drive brush size, quantized to whole brush sizes.

### The tools

Thirteen tools, each with a keyboard shortcut and each reachable without a
pointer: pencil (`B`), eraser (`E`), fill (`G`), line (`L`), rectangle (`U`),
ellipse (`O`), eyedropper (`I`, or `Alt` held), select rectangle (`M`), lasso
(`Q`), wand (`W`), move (`V`), pan (`Space` held or a middle drag), and dither
(`D`). The pencil, eraser, line, rectangle, ellipse, eyedropper, select, lasso,
move and dither tools commit on pointer up; fill and wand commit on pointer down;
pan never modifies the document.

1. Brush sizes are whole numbers from `1` to `32`, square by default with a
   circular option. An odd size centres on the anchor pixel. An even size has no
   centre pixel and occupies the square whose top-left corner is the anchor,
   extending right and down, and that choice is fixed rather than decided per
   stroke: a long line drawn left to right with a size `2` brush and the same
   line drawn right to left must produce identical pixels.
2. Lines are integer, with no floating point anywhere in them. The endpoint is
   plotted. Where two segments of a freehand stroke meet, the shared endpoint is
   plotted once and not twice, which is invisible at full opacity and very
   visible at partial. Holding `Shift` constrains to the nearest of the eight
   octants by comparing the two deltas against each other and against zero,
   never by rounding an angle in degrees.
3. Circles and ellipses are integer midpoint constructions. An even diameter has
   no centre pixel and is mirrored about the boundary between pixels rather than
   about a pixel, so a `20` by `20` ellipse has a bounding box of exactly `20` by
   `20`. The outline is exactly one pixel thick everywhere with no doubled pixels
   at the octant boundaries. A filled shape is produced by spanning between the
   symmetric pairs the outline generates, so the filled shape's boundary pixels
   equal the outline's exactly.
4. Fill is an iterative scanline flood fill, never recursive: filling a `4096` by
   `4096` empty document must complete rather than exhausting the stack.
   Connectivity is four-way by default with an eight-way option, exposed rather
   than chosen, because the two give materially different results on the diagonal
   lines that pixel art is made of. Tolerance is a distance in a perceptually
   uniform colour space, not a per-channel difference, so the tool behaves
   comparably on a blue ramp and on an equivalent green ramp. The fill reads from
   the composite or the active layer by setting and writes only to the active
   layer. It is bounded by the selection mask. A fill whose seed already holds
   the target colour changes nothing and records no history entry, so pressing
   undo afterwards undoes the action before it.
5. The eyedropper picks from the composite by default and from the active layer
   with a modifier. In indexed mode it picks the palette index rather than the
   resolved colour, so picking from a region and drawing back into it survives a
   later palette edit. Picking a fully transparent pixel selects the transparent
   index rather than doing nothing.
6. A selection is a one-bit mask the size of the document, never a path. New
   replaces the mask; `Shift` adds; `Alt` subtracts; `Shift` with `Alt`
   intersects. The lasso is a polygon rasterized with the even-odd rule and
   closed automatically. The wand is the fill algorithm run in mask-writing mode.
   Invert complements within the document bounds. Marching ants are drawn from
   the mask boundary and are paused under reduced motion. Every drawing tool is
   clipped to the mask, with no exception for the shape tools, the fill or paste.
7. Moving a selection lifts the masked pixels into a floating buffer, clears the
   source region on the active layer, and follows the pointer. The float commits
   on any of six triggers: a tool change, a layer change, a frame change,
   `Enter`, a save, an export, or the document being closed. `Esc` cancels,
   discarding the float and restoring the source region. A floating selection is
   never lost silently, and the commit is a single history entry including the
   original lift, so one undo puts everything back exactly as it was.
8. Symmetry offers a vertical and a horizontal mirror axis. On an odd dimension
   the axis lies on a pixel and on an even dimension between two, and every
   plotted pixel is also plotted at the reflection computed as the size minus one
   minus the coordinate, which is correct for both parities.
9. Shape and line tools draw to an overlay and commit nothing until pointer up.
   `Esc` during a drag cancels, leaving no history entry and no dirty tiles. The
   overlay is cleared on cancel, on commit, on a tool change and on window blur.

### The document

1. A document carries an id, a width and a height each between `1` and `4096`
   with the product of the two at most `4194304`, a mode of `indexed` or
   `truecolor`, a palette (required in indexed mode), between `1` and `512`
   frames, between `1` and `64` layers ordered back to front, a sparse map of
   cels addressed by frame and layer, an optional selection mask, and metadata
   carrying a title, a created and a modified timestamp, an author and tags.
2. Cels are sparse. A missing entry is the empty cel and costs nothing. The
   document is not a list of layers each holding frames, and not a list of frames
   each holding layers: creating `64` layers by `512` frames empty must cost
   almost nothing.
3. A layer carries a name, a visibility, a lock, an opacity from `0` to `255`, a
   blend mode and an optional group. Adding a layer inserts it directly above the
   active layer rather than at the top. Deleting is refused when it is the only
   layer, and the active layer becomes the one below, or above when there is none
   below. Duplicating copies every cel across every frame and names the copy with
   an incrementing suffix that never collides. Reordering is by index and groups
   move with their contents. Locking blocks every write, including fills, paste
   and the commit of a floating selection, and the refusal is surfaced rather
   than silent. Visibility affects the composite and the export, never the stored
   pixels.
4. Merging down composites the active layer onto the one below, per frame, using
   the upper layer's blend and transparency during the composite rather than
   afterwards: merging a half-transparent layer onto an opaque one must leave the
   picture exactly as it looked before the merge. On a frame where the upper cel
   is empty the lower cel is left untouched rather than rewritten with itself.
   Flatten repeats merging down to a single layer, preserving the visible result
   exactly, including transparency.
5. Blend modes are normal, multiply, screen, overlay, add, subtract, and erase,
   where erase subtracts the upper layer's alpha from the lower. Blending is done
   in straight, non-premultiplied, 8-bit integer arithmetic: compositing two
   identical fully opaque pixels must produce output identical to the input for
   every one of the `256` values per channel. In indexed mode blending happens on
   resolved colours and the result maps back to the nearest palette entry, except
   in normal mode at full transparency, where the index passes through untouched
   so an ordinary paste does not subtly recolour itself.
6. Frames carry a duration in milliseconds from `10` to `10000`. Playback is
   scheduled against a wall clock, so the next frame is due at the start plus the
   sum of the durations and a late tick skips rather than drifts: a `100`
   millisecond frame played `600` times must take `60` seconds, not `60` seconds
   plus one tick per frame. Looping is on by default with ping-pong optional.
   Inserting a frame adds an empty cel on every layer. Duplicating copies every
   cel of the source frame. Reordering and deleting are by index with the active
   frame clamped afterwards. Named frame ranges can be tagged and are used by the
   sprite-sheet export.
7. Onion skin shows from `0` to `8` frames before and after, on a transparency
   ramp falling linearly from a distance of one to a distance of eight, tinted in
   one hue before and another after as a colourize rather than a multiply, and
   wrapping around the ends when the animation loops. It is drawn into the view
   only and never affects what is exported or saved.
8. History entries carry a kind of pixels, structure or document, a dirty
   rectangle for pixel commands, tile deltas before and after, the full layer and
   frame metadata for structural commands, and a monotonic sequence number. One
   stroke is one entry, from pointer down to pointer up, however many samples it
   contained: drawing a `200` sample stroke and pressing undo once must remove
   the whole stroke. Entries store tile deltas rather than document snapshots.
   The stack is bounded by bytes rather than by a count, evicting the oldest
   entries first. A structural change and a pixel change made by one user action
   are one entry, so merging down and undoing once restores both the layer and
   its pixels. A no-op produces no entry. Redo is cleared by a new entry and only
   by a new entry. Undo and redo are not applied underneath a live preview.
9. Resizing the canvas is non-resampling with a nine-way anchor, one history
   entry, and cels cropped or extended with empty tiles. Resizing the image
   upscales by whole factors with nearest neighbour, and offers nearest and area
   average for downscaling with a warning that it is lossy. Cropping to the
   selection uses the mask's bounding box and clears the selection afterwards.
   Trimming crops to the bounding box of all non-transparent pixels across every
   frame and every layer, not only the current one, so content that is widest on
   a later frame is not cropped away.

### Colour and palettes

1. Two modes exist. In indexed mode a pixel is one byte, an index into a palette
   of between `2` and `256` entries, and the stored byte is the index and never
   the colour. In truecolor mode a pixel is four bytes of straight RGBA, with a
   palette present only as a swatch set. Indexed is the default, because editing
   palette entry `n` must recolour every pixel holding index `n` everywhere in
   the document at once, without touching a single stored pixel: set two palette
   entries to the same colour, draw with both, change one, and only that one's
   pixels change. Converting between modes is explicit, is one history entry, and
   the truecolor to indexed direction warns that it is lossy.
2. Every nearest-colour decision and every tolerance uses one distance function,
   computed in a perceptually uniform space rather than as Euclidean distance in
   RGB, with alpha compared separately and any difference between fully
   transparent and not treated as infinitely far. The transparent index is never
   returned as the nearest match for an opaque colour, and the reverse.
3. A palette carries an id, a name, its entries with an index, red, green, blue
   and alpha channels and an optional name, at most one transparent index,
   optional named ordered ramps, and a locked flag. Adding an entry is refused at
   `256` in indexed mode with the count shown. Editing an entry recolours in
   place as one history entry. Deleting an entry requires a replacement index and
   remaps every pixel holding the deleted index to it in the same history entry.
   Reordering remaps every pixel so the rendered image does not change, which is
   the entire point of reordering. Sorting by hue, by lightness or by usage count
   is a reorder. Entries within a small distance of each other are offered for
   merge and never merged automatically.
4. Quantization reduces an arbitrary image to a chosen number of colours by a
   weighted variance minimization over a colour histogram computed in the
   perceptual space, not a median cut in RGB. It is deterministic: the same input
   bytes and the same target count produce the same palette in the same order
   every time, with ties broken by lowest channel index then lowest value and
   never by hash iteration order, a pointer or a clock. Fully transparent pixels
   are excluded from the histogram and assigned the transparent index afterwards.
   The palette is emitted in a stable order, by lightness ascending, with the
   transparent index first when one exists.
5. Dithering offers ordered Bayer matrices at `4` by `4` and `8` by `8` for the
   dither brush and any preview, indexed by document coordinates and never by
   screen coordinates, so the pattern stays fixed to the artwork while the view
   is panned or zoomed. Floyd-Steinberg error diffusion is used on import and
   quantization only, with serpentine scanning and errors clamped to the
   representable range before diffusing, and it is never applied to art that is
   already indexed, because diffusing error through hand-placed pixels destroys
   them.
6. Alpha is binary by default: a pixel is present or it is not. Partial alpha is
   permitted, stored, and preserved through save and the still-image export.
   Every export path that cannot carry partial alpha states its threshold rather
   than silently rounding, and the animated path thresholds at an alpha of `128`
   and says so in the export dialog with a count of how many pixels will change.

### Export

Every encoder is written by the app, and determinism runs across all of them:
exporting the same document twice, in one session and in two, must produce
identical bytes. That forbids an embedded timestamp, a build version string, an
unordered map iteration and any random tie-break.

1. Formats are a still image carrying one frame with full alpha, which is the
   default download and the canonical thumbnail; an animated still-image format
   carrying frames with full alpha and a per-frame delay, for the high-quality
   animation export; the widely-requested animated format carrying frames with
   one-bit alpha and `256` colours; a sprite sheet laying frames out on a grid
   with a description file, for game use; and the document format, which carries
   everything losslessly and is what a save writes.
2. The still-image export is written at 8 bits per channel, and an indexed
   document is written as a palette image rather than expanded to truecolor. No
   colour profile is written and none is applied, because a profile changes the
   pixels and in pixel art that is corruption: exporting and re-importing must
   return identical pixels. Scaling is by whole factors only with nearest
   neighbour, from `1x` to `32x`, capped at `16384` in either dimension. Only a
   title and an author are written as metadata, and only when the artist opts in,
   because a timestamp would destroy byte-identical output. Compression uses a
   fixed level and a fixed filter strategy.
3. The widely-requested animated format is the encoder most likely to be built
   wrongly. Its structure is a header, a logical screen descriptor, a global
   colour table, then per frame a graphic control extension, an image descriptor,
   an optional local colour table and the compressed data; a looping animation
   additionally carries the application extension block declaring the loop count,
   once, before the first frame. In its dictionary compression the code size
   starts at the minimum code size plus one, where the minimum is the larger of
   `2` and the base-two logarithm of the palette size rounded up; the clear code
   is one shifted left by the minimum and the end code is the clear code plus
   one; the code width grows when the next code to be assigned would not fit,
   which is before it is used rather than after; a clear code is emitted and the
   dictionary reset when it reaches `4096` entries, because omitting that
   produces a file that decodes correctly in some viewers and as garbage in
   others; codes are packed least-significant-bit first across byte boundaries
   into sub-blocks of at most `255` bytes, each preceded by its length and
   terminated by a zero-length block; and an end-of-information code is emitted
   before the terminator.
4. That format's delay field is in hundredths of a second while frame durations
   here are in milliseconds, so the conversion divides by ten and rounds, with a
   floor of `2`. The floor is not optional, because a delay of `0` or `1` is
   treated as `10` by most viewers and a fast animation would export at a tenth
   of its speed. The rounding error is accumulated and carried between frames, so
   a run of `16` millisecond frames alternates between `2` and `1` hundredths
   rather than running the animation a quarter slow: exporting `100` frames of
   `16` milliseconds must total within one hundredth of a second of `1.6`
   seconds.
5. Frames are written with the disposal method that restores to background when
   any pixel that was opaque becomes transparent between frames, and with the
   method that leaves the frame in place otherwise. Choosing leave-in-place
   unconditionally makes transparent areas of later frames show the previous
   frame through them and the animation smears. Where leave-in-place is used,
   only the changed bounding box is encoded, positioned by the image descriptor's
   offsets, and the first frame is always full. One palette index is the
   transparent one, declared per frame, and a document whose palette is already
   full at `256` colours loses its least-used colour to make room and the export
   says so.
6. A sprite sheet lays frames out by row with an explicit column count, or as a
   single row, or as a single column, with padding from `0` to `8` transparent
   pixels that artwork never bleeds into, an optional power-of-two mode that pads
   the sheet rather than the cells, and an optional per-cell trim whose offset is
   recorded. The description file names each cell's rectangle, its offset, its
   duration and its frame tag, and it is part of the export: a sheet without it
   cannot be used without somebody re-measuring it by hand.
7. Export scope is the whole document (every visible layer, every frame), the
   current frame, the selection (its bounding box, with pixels outside the mask
   made transparent), one layer across frames ignoring the visibility of the
   others, or a named frame range. Hidden layers are excluded from every scope. A
   locked layer is not excluded: locking prevents editing, not seeing.

### Saving, offline and versions

1. A document being drawn is written to the device's own durable store before it
   is written anywhere else, and the editor is fully usable with no network at
   all. Losing an hour of work to a dropped connection is the worst outcome this
   product can produce.
2. Autosave writes only the tiles that changed, never the whole document, because
   a full write every few seconds on a large canvas makes the brush stutter.
   Dirty tiles go to the local store every `5` seconds in which the document
   changed, and upload to the service every `60` seconds in which it changed when
   signed in and online. Committing a large operation triggers an immediate local
   write, as does hiding the tab, using the page-lifecycle event that is
   guaranteed to fire rather than the one that is not. An explicit save is a full
   local write plus a full upload with a version stamped.
3. A version is written on every explicit save, and automatically at most once
   per `900` seconds and only when the document changed materially. The last `20`
   versions are retained, plus the first, plus any version the artist pinned.
   Restoring opens the version as a new document rather than overwriting, so
   restoring is never destructive. The version list shows the changed pixel count
   and a thumbnail rather than a byte size.
4. Two devices editing one saved document without a live session is the ordinary
   case. The service holds a version vector per document. When the uploader's
   base version is current, the upload is accepted and the version advances. When
   the base is behind and the changes touch disjoint tiles, they merge
   automatically and the artist is told it merged. When the base is behind and
   the tiles overlap, the service must not merge and must not overwrite: it
   stores the upload as a branch, presents both with thumbnails, and lets the
   artist choose or keep both. When the base version no longer exists, the upload
   is stored as a new document and never discarded. A silent last-write-wins on a
   drawing is data loss the artist cannot detect until much later.
5. Operations made offline are queued locally and replayed on reconnect. An
   operation that cannot be applied, because the layer it referred to is gone, is
   reported to the artist with a count rather than dropped quietly. The queue
   survives a browser restart and is bounded, and beyond the bound the artist is
   told to save locally and reconnect before continuing.
6. The local store can be evicted by the browser without warning. Persistent
   storage is requested at the first save and the artist is told plainly whether
   it was granted. A document that exists only locally is labelled as such, so
   "is this backed up" is never a guess. Under eviction pressure the oldest
   already-uploaded documents go first and local-only documents go last, never
   automatically without asking. If a store write fails, drawing continues in
   memory and a persistent banner says that saving is not working; the editor
   must not silently stop saving.

### Publishing and the object store

Artwork bytes live in MinIO, the S3-compatible object store already running at
`STORAGE_ENDPOINT` with the bucket named by `STORAGE_BUCKET` and the credentials
`STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. All four are read from the
environment and none is hardcoded.

1. `POST /api/pieces` publishes a document. The request carries a title, an
   optional description, from `0` to `10` tags, a visibility of `public`,
   `unlisted` or `private`, an optional `parent_id` when the piece is a remix,
   and the rendered artwork.
2. The rendered artwork is written to the object store under the fixed key scheme
   `pieces/{piece_id}/{sha256_of_bytes}.{ext}`, for example
   `pieces/42/9f2a1c7b4e0d8a5f3c6b9e2d4a7f0c1b8e5d3a6f9c2b4e7d0a1f8c5b3e6d9a2f.png`.
   Derived renditions use `thumbs/{piece_id}/{size}/{sha256_of_bytes}.png`, for
   example `thumbs/42/256/9f2a1c7b4e0d8a5f3c6b9e2d4a7f0c1b8e5d3a6f9c2b4e7d0a1f8c5b3e6d9a2f.png`.
   The bytes exist nowhere else: not on the app container's filesystem, not as a
   column in the database, and not as an in-memory blob the app hands back to
   itself.
3. Objects are addressed by the hash of their canonical bytes, which is only
   stable because the export is deterministic. Identical bytes are stored once
   with a reference count. Quota is charged per reference rather than per stored
   object, so two accounts uploading the same bytes each pay for it and neither
   can free the other's copy by deleting theirs. Deduplication is never surfaced
   to a user, because telling one account that their file already exists reveals
   the existence of another account's private file.
4. Protected artwork is not publicly readable. A `private` piece's object, and a
   piece in `pending`, `restricted` or `removed`, must be reachable only through
   `GET /api/pieces/{id}/file`, which authenticates the caller and serves only to
   the piece's author. Pick one of two mechanisms for every protected read and be
   consistent: an authenticated streaming endpoint, or a presigned link valid for
   at most five minutes and never issued to a caller who is not entitled. A
   request for a protected object by a signed-out visitor, or by any account that
   is not its author, is denied and the bytes are not served.
5. Derivatives are generated on publish: thumbnails at `64`, `128`, `256` and
   `512` on the long edge, scaled by a whole factor with nearest neighbour when
   the source divides evenly and area-averaged when it does not; an animated
   preview for animated pieces, capped in length and size; a static poster taken
   from the first frame, always; and an instant placeholder rendered from a
   colour summary of the piece's own palette while the real rendition loads.
   Scaling a `32` square piece up must stay crisp and scaling a `500` square
   piece down must stay legible, and a single rule for both is wrong in one
   direction or the other.
6. Uploads are bounded. A document from the editor may carry up to `4194304`
   pixels per frame, `512` frames and `64` layers. An imported still image is at
   most `20MB` with decoded dimensions capped at `8192` in either axis before
   quantization. A palette file is at most `64KB`. An avatar or banner is at most
   `5MB` and is re-encoded on receipt.
7. Decode safety is enforced on every upload. The format is decided from the
   leading bytes, never from the file name and never from what the client
   declared, and a mismatch is not an error because the detected type wins.
   Dimensions are read from the header and checked before any decode allocates,
   so a file declaring `60000` by `60000` is refused at no cost. Decoding happens
   in an isolated worker with a memory cap and a wall-clock cap, and a decode
   exceeding either is stopped and the upload refused with a specific message.
   Everything is re-encoded on receipt from decoded pixels, so nothing anybody
   uploaded is ever served back byte for byte. Uploaded objects are served from a
   path that carries no session credential, with inline rendering disabled for
   anything outside a small allow list.
8. Quota is reserved when an upload session opens and settled on completion, so
   twenty parallel uploads cannot exceed the quota twenty times over. A
   reservation idle for `1800` seconds is reaped and released. A chunk received
   twice is acknowledged, not re-stored, and not charged twice. Over quota, new
   uploads are refused while existing work is untouched and still served. Quota
   counts source documents, not generated derivatives.
9. Publishing is idempotent. Every state-changing request carries a
   client-generated key and the service holds that key with its response for
   `300` seconds. A retry with the same key returns the stored response and
   creates nothing. Two different requests colliding on one key: the second is
   refused as a conflict rather than silently handed the first one's answer. A
   flaky connection during a publish must not put two copies of somebody's
   artwork in the gallery.

### The gallery

1. A piece carries an id, an author, the document it came from, a title, a
   description, its tags, its visibility, a created and a published timestamp,
   its dimensions, its frame count, its palette size, an optional `parent_id`,
   counters for views, likes, comments and remixes, and a moderation state with
   labels.
2. `GET /api/pieces` serves the feeds. `new` orders by published timestamp
   descending. `popular` orders by score over a rolling window. `following`
   serves pieces by followed accounts, newest first. `tag` serves one tag,
   ordered either way. A profile feed serves one author, newest first, with that
   author's own private pieces included only when they are the viewer.
3. Scoring the popular feed is engagement over a super-linear time decay: likes plus twice
   remixes plus half the comments, all divided by the hours since publication
   plus `2`, raised to the power `1.5`. A remix weighs more than a like because a
   remix costs effort. Views do not enter the score at all, because a view is
   trivially manufactured. The score is recomputed on a schedule, at most every
   `300` seconds per piece, and never on a read. A piece with fewer than `3`
   distinct engaging accounts is not eligible for the popular feed whatever its
   score.
4. Pagination is by cursor on every feed; offset pagination is not acceptable.
   For orderings by published timestamp the cursor is the pair of the published
   timestamp and the id, which is a total order that never changes, and the query
   is a strict inequality on the pair. For the popular feed the ordering key
   changes underneath the reader, so the first page request takes a snapshot: the
   service materializes the ordered id list for that window, stores it under a
   token for `600` seconds, and every following page reads from the snapshot.
   Paging ten deep while scores change must show no id twice and skip none. An
   expired snapshot token returns a distinct answer and the client restarts the
   feed at the top rather than showing a failure. A piece deleted or hidden after
   the snapshot was taken is skipped at read time and the page is backfilled to a
   full length, so a moderated piece never leaves a hole.
5. Remix lineage is a directed acyclic graph. A remix records its `parent_id` at
   creation, from the document it was opened from. A cycle is refused at write
   time, by walking the ancestors before the insert, with the walk bounded.
   Depth is unbounded for storage and shown to a depth of `10`, with a control
   that shows the whole chain. Deleting a parent neither deletes nor orphans its
   children: the parent becomes a tombstone carrying its author's name and the
   fact of removal, so attribution survives, and the tombstone shows the
   thumbnail unless the parent was removed for a policy reason, in which case it
   shows no artwork. Remix permission is per piece: allowed, allowed with
   attribution, or refused, and changing it later does not retroactively unmake
   existing remixes. The counter on a piece counts direct children only; the
   chain view walks transitively with a cap of `1000` nodes per request.
   Attribution is not a rendering detail: the parent chain is stored on the piece
   and travels with every export and every embed.
6. Counters are derived from their rows and never incremented as a bare number.
   Likes, comments and remixes are counted from the rows, cached, and reconciled
   on a schedule. `100` concurrent likes on one piece must leave the count equal
   to the row count exactly. Views are a sharded counter incremented at most once
   per viewer per piece per `3600` seconds, deduplicated by a rolling window
   rather than by a stored row per view. A count is a cache of a query.

### Profiles and the handle namespace

1. Every first-level path segment is either a reserved word or an artist handle,
   so `/{handle}` is a profile. The reserved list is closed and versioned, and it
   contains `home`, `gallery`, `art`, `draw`, `digital`, `challenges`, `groups`,
   `contests`, `comics`, `palettes`, `stages`, `hire`, `forums`, `shop`, `pro`,
   `about`, `terms`, `privacy`, `help`, `contact`, `settings`, `search`, `api`,
   `admin`, `static`, `assets`, `topics`, `badges`, `blog`, `bases`, `tutorials`,
   `painter`, `parents` and `notifications`.
2. Adding a reserved word is a migration rather than a configuration change: an
   existing handle colliding with it must be renamed with the artist's consent
   and a permanent redirect left in place. Silently shadowing an artist's profile
   takes their address away.
3. Handles are compared after normalization, so two handles that render
   identically cannot both exist.
4. A profile shows a banner, an avatar overlapping the banner's lower edge, the
   handle above the display name, a follow control with a person-plus icon, an
   overflow control, a tab row and the artwork grid. The tabs are `Gallery`,
   `Albums`, `Followers`, `Following`, `About` and `More`, and the first, third
   and fourth carry counts beside their labels in a lighter weight at the same
   size. A zero is shown rather than hidden, because hiding a zero makes an empty
   profile look broken rather than new.
5. Three ownership states exist. Signed out: the follow control prompts sign-in,
   no private work appears, nothing is editable. Another member: the follow
   control acts, and block and report are available under the overflow. The
   owner: an edit-profile control replaces follow, private and unlisted work
   appears with its state shown, and a drafts tab appears that nobody else has.
6. A blocked viewer sees the profile as not found rather than as blocked, which
   is what stops block-probing. A restricted account's follower and following
   lists are visible to the owner always and to others only when the account
   permits it, and a restricted account does not permit it by default. The free
   text of the about tab is not linkified beyond the profile's own declared
   links.
7. An artist with no public work shows a drawn empty state, and the primary
   action when the viewer is the owner. A profile carrying one piece and a
   handful of followers is the normal case on this site, not an edge condition,
   so it must look intentional rather than broken.

### Following, comments and notifications

1. Following is one way and needs no approval, except for a restricted account.
   Blocking is mutual and absolute: it removes any follow in both directions and
   hides both parties from each other's feeds, listings, search results and
   notifications, and it is not surfaced to the blocked account as a distinct
   state. Muting is one way and silent: content is hidden from the muter and the
   muted account is unaware. Follow counters are derived. An account may follow
   at most `7500` others, at a rate of at most `200` per day, which is the whole
   follow-churn defence.
2. Comments thread one level deep, not arbitrarily. A comment body is at most
   `1000` extended grapheme clusters, and carries text plus a restricted set of
   small images from the site itself, never an arbitrary upload. A comment is
   editable for `300` seconds, after which it is immutable and shows an edited
   marker when it was edited. A comment is deletable by its author, by the
   piece's author or by a moderator, leaving a tombstone that preserves the reply
   thread's shape. Ordering is oldest first, stable, cursor paginated on the pair
   of the created timestamp and the id. An account may post one comment per `10`
   seconds, and one identical comment per `3600` seconds across the whole site.
3. A notification carries an id, a recipient, a kind, an actor, a subject, a
   created timestamp, an optional read timestamp and a group key. The kinds are
   like, comment, reply, follow, remix, mention, moderation and system.
4. Notifications collapse by their group key, which is the kind, the subject and
   the hour bucket. Twelve likes on one piece within an hour is one notification
   reading that twelve people liked it, not twelve rows: `50` likes in an hour
   must produce one notification. A group can be expanded, and stores at most
   `50` actors with a count beyond that.
5. Marking read is monotonic by notification id, so an acknowledgement naming an
   older id never moves the marker backwards and two devices cannot make the
   badge flicker. Marking read is idempotent. The unread count is derived from
   the rows whose read timestamp is null rather than stored as a number, so a
   notification deleted while unread decrements it. Read state reaches the
   account's other sessions promptly.
6. A mention is written with a leading at-sign and is resolved once, at write
   time, against the permissions and blocks in force at that moment, and stored
   as a resolved reference. Resolving at read time means a comment can start
   notifying somebody months later because they changed their display name to
   match a word in it. A mention of an account that has blocked the author
   produces no notification and renders as plain text.

### Moderation

1. The publish pipeline runs synchronous checks on size, format, rate limit and
   account state, then the piece is live in state `pending`, and asynchronous checks
   resolve it to `ok`, `restricted` or `removed`. Publication is not blocked on
   the asynchronous checks, but a piece in `pending` is visible only to its
   author and by direct link and never appears in a feed, a tag listing or
   search until it resolves.
2. Two hashes are computed and stored per piece: a cryptographic hash of the
   canonical exported bytes, which is exact, and a perceptual hash, which is
   robust to scaling and small edits. The perceptual hash is computed on a
   normalized rendering: composited, scaled to `32` by `32` through the
   area-average path, converted to luminance. Similarity is a Hamming distance,
   and the duplicate threshold and the review threshold are separate configured
   numbers, neither of which is ever the single trigger for a removal. A
   perceptual hash match never removes anything by itself: pixel art is small and
   heavily quantized, and palettes, templates and base sprites collide at rates
   that would be alarming in photographs and are normal here. Two unrelated `16`
   by `16` pieces that collide must both survive, with a review raised.
3. Automated classification assigns labels with confidence rather than a single
   score, because adult, violence, gore and hateful-symbol are different
   decisions with different consequences. Each label has two thresholds: below
   the lower, nothing happens; between them the piece is restricted and queued
   for review; above the upper it is removed and queued for review. Every
   automated removal reaches a human queue. The decision is stored with its model
   version so a later model can be evaluated against past decisions rather than
   silently rewriting them. Small pixel art defeats most classifiers, so the
   upper threshold is set high and review is the norm.
4. The review queue is ordered by potential harm and then by age, not by age
   alone. A reviewer may approve, restrict, remove or escalate, and each action
   requires a reason from a fixed list. Every action tells the author what
   happened, which rule applied and how to appeal. One appeal per action is
   allowed and is reviewed by a different person than the original reviewer.
   Reinstatement restores the piece with its original publication time, its
   counters and its place in every remix chain: a reinstated piece that comes
   back as new with its likes gone and its remix children orphaned has not been
   reinstated.
5. Every moderation action is recorded in an append-only, hash-chained audit
   record carrying an id, the actor (person or system), the subject, the action,
   the reason, an optional model version, the predecessor's hash and its own.
   Altering or removing an entry breaks every hash after it. Entries are appended
   through a single writer per shard so the predecessor is unambiguous: `100`
   concurrent actions must leave a chain that verifies end to end.
6. Reports are rate limited per reporter and deduplicated per piece, and the
   reported content is snapshotted at report time so a deletion does not destroy
   the evidence. A reporter whose reports are consistently rejected is quietly
   rate limited further; one who is consistently right is weighted up in the
   queue ordering.

### Search and discovery

1. Titles, descriptions, tags, author names and palette names are searchable.
   Pixels are not: finding remixes and near duplicates of a given piece is
   offered, and a general search by uploading a picture is not, and that refusal
   is stated here rather than in a policy document because it is exactly the kind
   of feature somebody adds later without knowing why it was left out.
2. Tags number from `0` to `10` per piece, are lowercase, normalized, and between
   `1` and `30` clusters long. The namespace is flat with no hierarchy, and
   curated aliases map variants onto one canonical tag. Creation is free with a
   suggestion list from existing tags ordered by use. A tag can be marked
   restricted, which removes it from suggestions and from public listings without
   unpublishing the pieces carrying it.
3. Matching is by prefix on tags and author names and by full token on titles and
   descriptions. Results are permission-filtered at query time and never from a
   permission snapshot stored in the index: a piece made private five seconds ago
   must not appear. The consequence is that a result page is fetched over-wide
   and trimmed, so the total is approximate and the response says so. Restricted
   and removed pieces never appear, including to their own author, who sees them
   on their profile with their state shown instead. An empty result is
   distinguished in the response from an unavailable index, which answers with a
   retry hint, because "nothing found" and "search is behind" mean very different
   things to somebody looking for their own work.
4. A newly published piece becomes searchable within `30` seconds at the 99th
   percentile. A removal propagates within `5` seconds at the 99th percentile,
   and removals are processed ahead of insertions, because content a moderator
   removed remaining findable is a safety failure while a new piece taking half a
   minute to appear is an inconvenience. An edit is reindexed as a delete plus an
   insert, never in place.
5. Four discovery surfaces exist: a tag directory of curated tags each with a
   count and a sample; a palette directory ordered by use count, each entry
   linking to work using it; challenges, which are time-boxed prompts with an
   entry, a deadline and a results view; and similar work, drawn from tag overlap
   and the remix graph and never from image similarity.

### The home page, the art centre and the not-found page

1. The home page is a hero band, a filter row, a topic row, the infinite artwork
   grid and the footer. The hero carries a full-bleed pixel-art backdrop under a
   dark overlay, a headline reading `CREATE AND SHARE ART` in capitals, a kicker
   reading `LEARN - SHARE - MAKE PIXEL ART - SHOP`, two lines of centred body
   copy, the two actions `START DRAWING` and `CREATE ACCOUNT` side by side, and a
   link reading `For Teachers and Parents` with a book icon below them.
2. The hero credit is not decoration. The hero backdrop is a piece of artwork by
   a member, and the credit line in the corner names them and links to them.
   Dropping that line while keeping the artwork takes an artist's credit off
   their own work on their own site, so it is required.
3. The filter row carries seven entries in order: `Explore`, `Topics`,
   `Highlighted`, `Trending`, `Popular`, `Staff Picks`, `Featured`. The active
   entry is a pill; the others are plain text. `Highlighted`, `Staff Picks` and
   `Featured` are human-curated and must be distinguishable in the data model
   from the computed feeds, because a curated feed cannot be regenerated and an
   algorithmic one must be.
4. The topic row carries six cards: `Cats`, `Christmas`, `People`, `Technology`,
   `Valentine`, `Ocean`. Each is a card whose ground is a piece of artwork and
   whose content is a single label at the lower left, on a dark scrim that is
   required rather than optional because the artwork behind it is arbitrary and
   cannot be assumed dark. The set is editorial and seasonal rather than
   computed, so it has an editing surface and a schedule: computing it from tag
   popularity would show `Christmas` in July.
5. The art centre at `/art` is the same grid with proper controls: a header
   carrying the route title and a count of works, a filter bar carrying the feeds
   plus a tag filter and a sort control, the infinite grid, and an empty state
   that names the filter and offers an action clearing it rather than a bare "no
   results". Every filter and sort is in the address, so a filtered gallery can
   be linked and returned to. Changing a filter resets the grid to the top and
   starts a new pagination snapshot. Going back returns to the previous filter
   and the previous scroll position, restoring the pages already fetched rather
   than refetching from the top. Opening a piece from the grid opens it as an
   overlay over the grid with the address updated, so going back is a dismissal
   rather than a rebuild; a full navigation happens only when a piece is opened
   directly from outside the site.
6. An unknown address renders the product's own not-found page and is answered
   with a not-found status. It is a centred card on the page ground carrying the
   headline `Oops!`, the body `Looks like something went wrong! Don't worry,
   we're here to help!`, a primary action returning to the editor and a secondary
   `Contact Support` action, a muted credit line naming the error and the artist
   whose work the page shows, and two illustrated characters that drift in
   opposition on a slow loop, one above the card's upper right corner and one
   below its lower left. The page carries the address that failed so a report can
   name it. The unbuilt drawer destinations render this page and are not
   redirects.
7. A path that looks like a handle but resolves to nobody renders a distinct
   page saying there is no artist with that name and offering a search, rather
   than the generic error. Most failures on this site are mistyped handles, and
   treating them as generic errors wastes the site's most common failure.
8. A privacy page and a terms page are reachable from the footer of every page.
   The privacy page states what Pixelary records about an artist and how long it
   is kept. The terms page states the rules of posting and is linked from the
   signup form as well as the footer. Both share one long-form template with a
   capped measure, a table of contents of in-page links, a last-updated date, a
   summary of what changed, and no motion of any kind, which is also the template
   for the about, help, contact us, parents and teachers, and shop order lookup
   pages.
9. A first-party consent panel asks a first-time visitor once about non-essential
   cookies, records a decision per category, and never blocks first paint. It is
   reachable afterwards from the footer control reading `Do not Sell or Share My
   Personal Information`. Refusing is exactly as easy as accepting: one control
   each, the same size and the same prominence. The panel sits at the toast level
   of the stacking scale, not above everything.
10. Every internal link on every public route resolves, and every public route
    carries its own title and description.

### Embeds, the public read interface and the supporter tier

1. A piece can be embedded elsewhere as a framed view of fixed aspect carrying
   the piece, its title and its author. The embed shows the animated preview
   rather than the editor. Attribution, meaning the author's name and the remix
   chain root, is always present and cannot be removed by a parameter. The embed
   sets no cookies, sends no identifiers, and reports a view at most once per
   viewer per `3600` seconds. A piece that becomes private, restricted or removed
   stops rendering in every existing embed within `60` seconds and shows a
   neutral placeholder rather than an error.
2. Public pieces and profiles are readable with no token, rate limited by
   address. An account's own private work requires a scoped token. Writing
   anything requires a scoped token. Scopes are granular: reading public data,
   reading an account's own work, publishing on its behalf and commenting on its
   behalf are four separate grants, and an application asks for the least it
   needs. An application acting for an account can never exceed what that account
   could do itself, so its effective permission is the intersection of its scopes
   and the account's own rights.
3. Three things deliberately do not exist: an endpoint returning accounts by age,
   location or any attribute that would let somebody assemble a target list; an
   endpoint that accepts an image and returns visually similar pieces; and any
   route exposing another account's private or unlisted work, including to an
   application the author has authorized, unless a scope names it explicitly.
4. Outbound webhooks deliver at least once, in no guaranteed order, with a
   sequence on each payload, retried with exponential backoff and jitter over `8`
   attempts spanning about a day, dead-lettered for `72` hours and re-drivable by
   hand. Each payload is signed over its timestamp and its raw body, verified
   before parsing with a constant-time comparison and a skew window of `300`
   seconds; verifying against a re-serialized body fails on any payload whose key
   order or whitespace differs from what was signed. Each payload carries a
   stable delivery id and consumers deduplicate on it. A target failing
   everything for `72` hours is disabled and its owner told.
5. The supporter tier is an entitlement. A plan carries an id, an interval of
   month or year, a price of `1000` integer minor units in `usd`, and its
   features. A subscription carries a status, a period start and end, a
   cancel-at-period-end flag and a payment source. An entitlement carries an
   account, a feature, a source of subscription, gift or grant, and a start and
   end. The product checks entitlements and never subscriptions, so a gift, a
   staff grant and a paid subscription are indistinguishable at the point of use.
6. Behind the tier: larger canvases and more frames, more storage and more
   version history, priority in the export queue, profile customization, and no
   advertising. Never behind the tier: any drawing tool, the undo history depth,
   any export format, attribution and the remix chain, and anything to do with
   moderation. A pixel-art editor that puts the line tool behind a subscription
   is not a pixel-art editor: what the tier buys is capacity and convenience.
7. A subscription moves from incomplete to active, and from active to past due,
   unpaid and cancelled, or back to active on recovery. Past due still grants for
   a grace period of `7` days while dunning runs. Recovery restores active
   without changing the period end, so recovering does not shorten a period
   already paid for.
8. When an entitlement lapses, work that exceeded the free limits is never
   deleted and never made inaccessible. It becomes read-only for editing beyond
   the limit: the artist can still open it, export it and delete it. Every piece
   of a lapsed account must still open, still export and still be deletable by
   its author.
9. Proration on a plan change is computed over the real period length. Credit for the
   unused remainder is the seconds remaining over the seconds in the actual
   period, never over an assumed thirty days, because a monthly period is `28`,
   `29`, `30` or `31` days. The new plan's charge is computed over the same
   remaining seconds. Both are computed in integer minor units with rounding half
   away from zero applied once at the end and never per line. A downgrade credit
   larger than the new charge becomes account credit rather than a refund.
   Upgrades take effect immediately and downgrades at the period end, and both
   are shown as scheduled changes the account can cancel. A currency travels with
   every amount and there is no default currency anywhere.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Hero, filter row, topic row, the infinite artwork grid, footer | none |
| `/art` | The art centre: the grid with filters, tags and sort held in the address | none |
| `/draw` | The editor | none |
| `/piece/{id}` | One piece, its lineage, its comments | none for a public piece |
| `/{handle}` | An artist gallery and profile | none for a public profile |
| `/search` | Search over titles, descriptions, tags, artists and palettes | none |
| `/privacy` | The privacy page | none |
| `/terms` | The terms page | none |
| `/notifications` | Grouped notifications for the signed-in account | bearer |
| any other path | The not-found page, answered with a not-found status | none |

**Entry and redirects.** A request to a protected route without a session opens
the sign-in modal with the intended route remembered, and signing in returns
there. Signing out returns to `/`. A token that expires mid-action leaves the
editor running and the local save working, and asks for sign-in at the next
upload rather than interrupting a stroke. A `reader` who reaches a publish
control is refused by the server. A signed-out visitor who follows a link to a
private piece gets the not-found page, not a sign-in prompt, and not the artwork.

**Journey 1: draw and publish.** Open `/draw` with no account. Draw with the
pencil, add a second layer, add a second frame, pick colours from the palette.
Press the publish action: a modal opens over the editor. Sign up inside it as a
new account. The modal lists every document in the local store with a thumbnail
and asks which to upload; nothing is uploaded until that choice is made. Choose
the current document, give it the title `Harbour Lights`, add the tags `ocean`
and `night`, leave it public, and publish. The piece appears at once on
`/{handle}` in `pending`, and it appears in the public feeds once its state
resolves to `ok`.

**Journey 2: browse, open and remix.** Open `/`, choose the `Ocean` topic card,
and open a piece from the grid; it opens as an overlay over the grid with the
address updated. Press remix. The editor opens with the parent's document loaded
and the parent recorded. Draw, publish. Both pieces now show the credit chain,
the parent's remix counter has gone up by one, and attempting to remix one of the
new piece's own ancestors from it is refused.

**Journey 3: protect a piece.** Sign in as `author@example.com`. Open the piece
`Night Market Draft` on `/nova` and set it to `private`. It leaves every feed,
every tag listing and every search result. Signed out in another browser, its
page answers not-found, `GET /api/pieces/{id}/file` is denied, and asking the
object store for its key directly returns nothing readable. Signed back in as its
author, it opens, its artwork renders, and it exports.

**Journey 4: like, comment and follow.** Sign in as `reader@example.com`. Like
`Cat In A Window`: the row updates immediately and the count settles to the true
row count. Comment on it, then reply once to that comment; a third level is not
offered. Follow `nova`. The `following` feed now carries `nova`'s public pieces.
Block `bram`: `bram` disappears from feeds, listings, search results and
notifications in both directions, and `/bram` answers not-found.

**States.** Every list has an empty state that names the filter and offers to
clear it. Every grid cell reserves its height from the artwork's declared
dimensions before the image arrives, so the grid never reflows. Images load
lazily, one screen ahead, and a cell shows a skeleton while loading. Animated
pieces show their first frame until they are at least half visible, then play,
and pieces that are off screen do not run. The infinite grid appends a page when
the reader is within two screens of the end, and appends it once: a scroll that
crosses the trigger twice must not fetch twice. The grid also exposes a load-more
control, because an infinite scroll with no control is unreachable without a
pointer and leaves the footer unreachable entirely. Every page has a loading
state. No error crashes the app.

## UI/UX notes

The character is set by the product itself rather than by a house style: bright,
direct and loud, built to put other people's artwork first. A visitor's first
moment should be somebody else's drawing, not the interface around it. The
register is consumer and editorial, so the subject is seen before the chrome, and
the chrome is deliberately quiet in a way that a marketing page would not be.

The design tension worth naming is that the working interface is dense while the
subject is expressive. Resolve it in favour of the artwork: the grid is the page,
and everything else is arranged so as not to compete with it. Information density
over decoration; artwork over chrome; restraint over atmosphere. A competing
product could rationally hold the opposite, which is why this is a stance and not
a platitude.

Colour by role, with the exact values yours so long as the relationships hold.
The page ground is a near-white cool neutral and surfaces are a near-white
neutral, so a card reads as lifted without a border. Body text is a deep cool
neutral; muted metadata is a mid cool neutral. Hairlines under the secondary
bars are a near-white neutral drawn as a spread shadow rather than a border, so
they occupy no space and never double into a thick line where two panels meet.
The primary action, every link and the active navigation state wear one mid,
vivid blue, and nothing else on a page wears it. Confirmation is a mid, soft
green. Anything destructive or failed is a light, vivid red, and it appears
nowhere else. A caution state is a mid, vivid amber. The profile banner ground is
a deep cool neutral. The upload segment of the drawing control is a light, vivid
red-orange and the paint segment is a vivid green. A light, soft magenta, a
light, soft indigo, a mid, soft teal and a light, soft cyan exist in the token
layer and do no work at all: reaching for one of them is inventing rather than
designing. The rarely-used effect sweeps reach for a mid, vivid teal, a mid,
vivid cyan, a mid, vivid indigo, a light, vivid blue, a mid, vivid orange and a
mid, vivid green, and they stay rare.

Nothing important is a flat fill. Every action of consequence is a colour sweep:
the drawing action sweeps from blue to violet, signing up sweeps through four
warm stops so it reads as a sweep rather than a two-colour transition, the
supporter tier is a violet sweep, and the two small segments beside the drawing
action are one green and one orange sweep. The angle and the stop count of the
four-stop sweep are load-bearing; two stops at a round angle is a different
button. A sweep responds to a pointer by lifting very slightly and brightening,
because inventing a second sweep for every hover state is not a design.

Typography is exact, because type is an identity rather than a value to echo. One
text family, `Roboto`, backed by the system sans stack, with a monospace stack of
`SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New",
monospace` reserved for identifiers. Body is `14.4px` on a `23.04px` line, one
step under the browser default, which is what lets a gallery card carry a title,
an artist and three counts without becoming a paragraph. Control labels are
`16px` at weight 500. Lead paragraphs are `18px` on `28.8px`. Dense metadata is
`14px` on `22.4px`. Body inside a card is `16px` on `25.6px`. Captions and counts
are `12px`. Section headings are `21.6px` at weight 700 on a `21.6px` line, so a
heading is a single line by design. Subheadings are `20px`. Badges are `12px` at
weight 500. Figures align wherever counts stack.

Density is comfortable. Spacing runs on one scale in even steps from none to
generous, applied through a single set of utilities rather than decided per
element, so two panels never disagree about their gutter. Shape is pills for
controls, soft corners for cards, and barely-rounded corners for badges and close
controls. A pill radius on a short control and the same radius on a tall panel
are deliberately the same value and must not be normalized into one scale: on the short control it reads as a pill
and on the panel as a soft corner, and that is the site's one idiosyncrasy.

Motion is eased, and it has two speeds and no more: one shared speed for colour,
background, border and shadow together, and a second, slower one reserved for
movement. Every property that is animated is named; nothing animates everything
it can. The source material's blanket transition, which animates every property
an element has, is the one thing here this product does not reproduce: it is a
framework default multiplied across a large page, not a design. The named moments are an entrance that rises while it fades in, a lateral
entrance for sequenced rows, a loading shimmer that sweeps across a skeleton
cell, a bar that crosses several times its own width, a ring that expands from a
point and fades out, a reply that rises and unsquashes horizontally as it
arrives, a rejection that shakes and decays at both ends so it reads as a
head-shake rather than a wobble, a pair of characters that drift in opposition on
a slow loop, and a spinner that completes a whole turn rather than stopping one
degree short. Nothing here is driven by the scroll position: there is no
parallax, no pinning and no scroll-driven timeline, and adding one would be
inventing. A hover effect only applies where the device actually has a pointer,
or tapping the drawing action on a phone leaves it stuck looking lifted and
bright until something else is tapped.

Under a request for reduced motion the drifting characters hold their rest
position, the shimmer and the loading bar become a static tint, the ripple does
not run, the rejection shake does not run and its meaning is carried by colour
and text alone, the marching ants stop, animated artwork holds its first frame,
and every entrance is replaced by its end state. This is honoured under every
part of the motion character, with no exception.

Accessibility is contract rather than taste. Body text meets WCAG AA contrast on
both grounds. The artist byline under a card is set faint in the source material
and does not pass, so it is raised to the minimum that does; that is the one
measured value here overridden rather than reproduced, and meaning is never
carried by colour alone. Every count is labelled for a screen reader, because
three bare numbers in a row are meaningless read aloud and they are the most
repeated content on the site. Every content image carries alternative text: for a
piece with a title it is the title and the artist, for a piece without one it is
a generated description of its dimensions and dominant colours, and it is never
empty and never a file name; decorative marks declare themselves decorative and
are hidden from assistive technology, while an icon that is a control's only
content carries a name saying what it does rather than what it depicts. Full
keyboard navigation works everywhere with a visible focus ring that is never
removed, and a sweep-painted pill takes its ring outside its own bounds because a
ring inside a sweep is invisible. The drawer traps focus while open and returns
it to the button that opened it, and every dropdown closes on `Esc`. Touch
targets are comfortably sized, and the small segments of the drawing control are
padded until they are. The editor is usable without a pointer: arrow keys move a
drawing cursor by one pixel, a modifier moves it by ten, space applies the
current tool, zoom and pan are keyboard operable, and no palette entry is
identified by its colour alone because entries carry indices and optional names.

Layout is responsive and mobile first, with the narrow viewport arrangement
designed rather than inherited: at a narrow viewport nothing overflows sideways
and every navigation target stays reachable. Four columns of artwork at a wide
viewport become three at a tablet breakpoint and two on a phone; the topic row
goes from six across down to two. As the viewport narrows the chrome sheds its
wordmark, its navigation entries and its search input, leaving the menu button,
the mark, a search icon that expands over the bar, and the sign-in control. The
drawing action never leaves the chrome at any width: after everything else has
been dropped it is still there, which is the site telling you what it is for.
Artwork is never cropped to fit a cell, because pixel art is frequently long or
tall and cropping a piece to tidy a grid defaces somebody's work.

Each page leads with one clear primary action, visually distinct from every
secondary one, and the drawing action is that action nearly everywhere. What this
must not look like: a page dominated by a single hue family with no second
signal; decoration standing in for content; a marketing composition where the
working interface belongs; a card grid where every cell has been squared off so
the page looks tidy and every drawing looks wrong.

## Technical requirements

Build the rendered pages with SolidStart and serve them from a Node process
running Express, which also serves the JSON API under the `/api` prefix on the
same origin. The rendering model is server-rendered pages with hydrated islands:
the browser receives complete HTML for every route on first paint, and only the
editor and the artwork grid hydrate into interactive islands. Persist relational
data in PostgreSQL, read from `DATABASE_URL`. Store artwork bytes in MinIO, read
from `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and
`STORAGE_SECRET_KEY`. Authenticate with app-implemented email and password,
issuing bearer tokens. `GET /api/health` returns `200` once the app is ready.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor: the only backing services available in this environment are
PostgreSQL and MinIO, and reaching for anything else is a contract violation.

No credential, API key, access token or admin secret appears in anything the
browser downloads. Nothing in the client bundle, in server-rendered markup, in an
inline script, in a source map or in any response body carries a value that
grants access to PostgreSQL, to MinIO or to another account's session. The object
store's keys stay on the server, and the browser reaches protected artwork only
through the app's own authenticated route.

The application ships no third-party script of any kind and makes no external
network call at runtime. No advertising, no analytics vendor, no consent vendor,
no font binary, no icon font and no external stylesheet. Icons are inline
geometry on a `24` unit grid with a `2` unit stroke, round caps and joins,
inheriting colour, at sizes of `16`, `20` and `24` and nothing else. An icon font
is a binary, it renders as nothing until it loads, and it is invisible to a
screen reader, so it is not acceptable here.

No binary asset ships. The zero-asset rule is absolute, and every asset class the
source material used has a substitution: each is produced by a deterministic
generator, so the same seed yields the same output and a rebuild is not a
redesign. The artwork placeholder is generated from the piece id: a grid of `16`,
`24` or `32` cells on the long edge, a palette of `4` to `8` entries drawn as a
ramp, one of four seeded compositions (a landscape with a horizon band and two to
five silhouette shapes, a bilaterally symmetric character, a Bayer-ordered
pattern tile, or a character composited into a landscape), ordered dithering
applied to the ramps only, and whole-factor nearest-neighbour scaling up to the
card size. The placeholder must be real pixel art at a real pixel-art resolution:
a blurred gradient in a card is not a substitute, because the whole visual
argument of this site is that the grid is visible. Animated placeholders are a
four-frame loop from the same generator, where the character variant bobs by one
pixel, the pattern variant cycles its palette by one step and the landscape
variant moves two silhouette shapes by one pixel each. Avatars are a seeded
identicon on a `5` by `5` grid mirrored about the vertical axis in two palette
colours, scaled by a whole factor, so one account always renders the same avatar.
The brand mark is a heart drawn as pixel art on an `11` by `10` grid, scaled by a
whole factor, beside a letter-spaced capitalized wordmark; it is generated as
pixel art rather than a smooth vector, because on this site the mark is the
argument. Grain, where used, is an inline fractal-noise filter desaturated to
zero and tiled, at a very low opacity over both dark and light grounds. Naming a
font family is not an asset dependency; shipping one is, so the display and text
roles fall back to the system stacks.

Advertising slots are not present, but the space where they would sit is
reserved as an empty bordered region of the same dimensions, so that a build
which later adds advertising does not have to relayout. A page that collapses a
slot and later restores it pushes every card below it down, which is the largest
single source of layout shift on a page of this shape.

The editor core depends on nothing above it. It imports nothing from the site
layer, and the site layer never mutates the document: publishing reads a
rendition and does not reach into the document. The editor must remain fully
usable when every other part of the service is unavailable, and it cannot do that
if it depends on the gallery's data layer. Site state (the open drawer, the open
dropdown, the active filter, the grid cursor and snapshot token) does not survive
a reload; the consent decision and the session do.

Performance targets, at every viewport, on a mid-range device over a fast mobile
connection: first contentful paint under `1.5` seconds, the largest contentful
element under `2.5` seconds, interaction latency under `200` milliseconds at the
75th percentile, cumulative layout shift under `0.05`, no single main-thread task
over `50` milliseconds, script on the first view of the home page under `250KB`
compressed, total transfer on that first view under `1MB`, and zero third-party
requests. The layout-shift target is half the usual one on purpose, because a
grid of images of unpredictable aspect is the worst case for shift. Artwork is
decoded off the main thread and painted with nearest-neighbour scaling. The grid
recycles rows beyond two screens in either direction, because an infinite grid
that keeps every cell mounted exhausts memory on a phone within seconds of
scrolling.

Editor targets: a usable empty canvas within `1` second; frame time under `16`
milliseconds at the 95th percentile while drawing at zoom `16` on a `1024` square
document; a stroke durable in the device's own store within `5` seconds of
pointer up at the 99th percentile; undo of a large stroke under `50`
milliseconds; export of a `64` frame animation under `3` seconds and off the main
thread; and memory after an hour of drawing bounded by the history and tile
bounds above.

The stacking scale is named rather than numeric, with six levels in order: base,
raised, chrome, dropdown, modal, toast. Nothing is placed above the toast level.

Every response to a rate-limited route carries the permitted count for the
window, the count remaining, the seconds until it resets, an opaque bucket
identity and a scope of user, shared or global. The bucket identity is the opaque
value and not the route string, because routes share buckets and a client keying
its own accounting by route will exceed a shared bucket while believing it is
well inside the limit. The limits are: publish a piece, `20` per `3600` seconds
per account; upload bytes, `500MB` per `86400` seconds per account; comment, `1`
per `10` seconds and `100` per `3600` seconds per account; an identical comment,
`1` per `3600` seconds per account and content hash; like, `600` per `3600`
seconds per account; follow, `200` per `86400` seconds per account; report, `50`
per `86400` seconds per account; sign-in attempt, `10` per `600` seconds per
account and `50` per `600` seconds per address; autosave upload, `1` per `30`
seconds per document; export, `60` per `3600` seconds per account; anything
anonymous, half the signed-in limit, keyed by network address; a global ceiling of
`50` per second per account; and invalid requests, `10000` per `600` seconds per
address. Allowance is evaluated against a monotonic clock with state held in one
place per key, so two application instances cannot each grant a full allowance,
and a window that resets on the hour is not acceptable because it permits double
the intended rate across the boundary. A request refused for rate has not
consumed allowance; a request that succeeded but whose response was lost has
consumed it exactly once. Responses that deny, forbid or rate-limit count toward
the invalid-request budget, and crossing it blocks the address ahead of the
application, which is why a client told to stop must stop.

Manipulation defences reduce a piece's eligibility quietly and never produce a
visible punishment on suspicion, because the false-positive case is a popular new
artist. Many accounts from one address in a short window get a signup challenge
and then a block. Likes clustered from accounts created the same day are excluded
from the eligibility count, silently. A remix chain created entirely by one
account to inflate a counter counts remix weight once per distinct author per
ancestor. Comment text repeated across many pieces hits the identical-comment
limit and then review. The same content hash uploaded under many accounts is
flagged for review and never auto-removed.

Text is handled by role rather than by its English wording. The string catalogue
is keyed by role: every user-facing string is keyed by role so editing the English does not orphan a translation,
interpolation is by named placeholder because concatenating translated fragments
assumes an English word order, plurals use the full category set for the target
language rather than two forms, and dates, times and numbers are formatted by the
platform for the reader's locale rather than assembled by hand. In a right-to-left
locale the interface mirrors: the tool palette moves to the right, the layer stack
to the left, and chevrons flip, using logical properties throughout. The artwork
never mirrors. The drawing surface, its coordinate system, the layer order and
every tool are unaffected by the interface's direction, because a canvas that
flipped would silently change the meaning of every coordinate in every saved
document, which is corruption rather than a layout choice.

Hostile text is neutralized. Length limits are counted in extended grapheme
clusters and never in code units, so a family emoji is one character. Truncation
is always at a grapheme boundary and never inside a joined sequence.
Bidirectional overrides are stripped from display names, titles and tags and
neutralized in comment bodies. Zero-width and invisible characters are stripped
from names, titles and tags, preserved in comment bodies, and counted toward the
limit either way. A display name that renders identically to an existing
account's, using look-alike characters, is refused. Identifiers are normalized
before comparison and stored normalized, so two spellings of one name cannot both
exist. Sorting uses locale-aware collation rather than code-point order. Layer
names, palette entry names, frame tags and document titles follow every rule
above and are additionally restricted to what an export format can carry, with a
documented substitution rather than a silent drop.

Observability is first-class. Logging is structured, one line per request,
carrying a correlation id, the route, the bucket and the outcome. What is
measured: request rate, error rate and
duration per route and bucket; the editor's time to first stroke, frame time at
each zoom step and dropped frames per stroke by device class; save success rate
and the time from stroke to a durable local write by device class; upload success
rate and decode failure reasons by format; export duration and failure rate by
format and document size; moderation queue depth and age by label; search index
lag; and the depth of every bounded queue. Moderation queue age is a first-class
alert rather than a dashboard, because a queue past its target means automated
decisions are standing unreviewed. Artwork bytes, upload contents, credentials,
tokens and full network addresses are never written to a log: a build that logs
artwork for debugging has created a second, unmanaged copy of every private
drawing on the site.

Under pressure, degradation follows a fixed ladder and never runs out of order:
popular-feed recomputation pauses with the last ordering frozen and labelled;
view counting drops; notifications batch to one delivery per `300` seconds;
search answers that its index is unavailable; new uploads are refused with a
retryable answer; the export queue becomes client-side only; new collaborative
sessions are refused; publishing is refused while editing and saving continue;
and finally the service reads but does not write. The editor and the local save
are never degraded at any level, and moderation is absent from that ladder on
purpose because it is never degraded either. Backpressure is explicit: every queue has a bound and a
documented behaviour at that bound: shed a non-essential signal, refuse with a
retryable answer, or close a session and let it reconnect. An unbounded queue is
a defect, and dropping a saved change is never a permitted behaviour.

Recovery behaviour: a fanout backlog drains oldest first and suppresses
notifications older than `600` seconds; a search index that is behind answers
with a retry hint rather than partial results; a duplicate delivery after a
replay is deduplicated by event id; a bad deploy is rolled back, which the
migration rule below makes always possible; and corruption in one document's
tiles is restored from the last snapshot plus the operation log, with the
document marked as recovered so the artist is told.

Every cached gallery response is keyed including the viewer's moderation
visibility class, never by the path alone, so a response cached for a signed-out
viewer is never served to a moderator and a response cached before a removal
never survives it. Invalidation is explicit on publish, unpublish, a moderation
state change, a deletion and a profile change; expiry is a backstop rather than
the mechanism, and its lifetime is short enough to keep the embed promise above.
Gallery reads are high-volume, cacheable and mostly anonymous; editor sessions
are long-lived, stateful and low-bandwidth; uploads and exports are bursty and
heavy and go through a bounded queue that shows a position and refuses new
entries with a retryable answer rather than growing without limit; search is
moderate; moderation is low volume and high importance and is never degraded.

## Data model

Thirteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account
so a grader can sign in.

### accounts

`id`, `email` (unique, normalized before comparison), `handle` (unique after
normalization, and never a reserved word), `display_name`, `password_hash`,
`hash_params`, `date_of_birth`, `restricted` (derived from the date of birth
against the local age of digital consent, recomputed on read rather than stored
as a frozen flag), `role` (`author` or `reader`), `created_at`. Follower and
following counts are derived from `follows`, never stored.

### documents

`id`, `account_id` (null for a document that has never been adopted), `title`,
`width`, `height`, `mode` (`indexed` or `truecolor`), `palette_id`,
`frame_count`, `layer_count`, `version`, `created_at`, `modified_at`. Tiles are
addressed by the document, the layer, the frame and the tile coordinates,
together with the version they belong to. A save writes only the tiles that
changed, so a version is a small delta plus a pointer to its parent version, and
reading a version resolves tiles by walking back, with a full snapshot written
every `20` versions so the walk is bounded. A tile that is entirely empty is not
stored, because the absence is the value. A tile is immutable once written:
editing writes a new tile at a new version, which is what makes version history
and the conflict handling possible at all.

### pieces

`id`, `account_id`, `document_id`, `title`, `description`, `visibility`
(`public`, `unlisted` or `private`), `moderation_state` (`pending`, `ok`,
`restricted` or `removed`), `moderation_labels`, `parent_id` (null, or the piece
this one was remixed from), `remix_permission` (`allowed`,
`allowed_with_attribution` or `refused`), `width`, `height`, `frame_count`,
`palette_size`, `object_key`, `content_hash`, `perceptual_hash`, `created_at`,
`published_at`. `views`, `likes`, `comments` and `remixes` are derived from their
rows and cached; they are never stored as a bare number that a write increments.
A piece has at most one parent, and the lineage it forms is acyclic: a piece can
never be a remix of one of its own descendants.

### piece_tags

`piece_id`, `tag` (lowercase, normalized, between `1` and `30` clusters).
Unique per pair. At most `10` rows per piece.

### likes

`id`, `account_id`, `piece_id`, `created_at`. Unique on the pair of the account
and the piece, so one account likes one piece at most once. Two simultaneous
likes of the same piece by the same account leave exactly one row. The like count
a feed reports is the count of these rows and must equal it exactly under
concurrent writes.

### comments

`id`, `piece_id`, `account_id`, `parent_comment_id` (null, or a top-level
comment; a reply to a reply is refused), `body` (at most `1000` extended grapheme
clusters), `edited` , `deleted` , `created_at`. A deleted comment leaves a
tombstone preserving the thread's shape.

### follows

`follower_id`, `followee_id`, `created_at`. Unique per pair, one direction only,
and a row may not name the same account twice.

### blocks

`account_id`, `blocked_id`, `kind` (`block` or `mute`), `created_at`. A `block`
removes any follow in both directions on insert.

### notifications

`id`, `recipient_id`, `kind` (`like`, `comment`, `reply`, `follow`, `remix`,
`mention`, `moderation` or `system`), `actor_id`, `subject_id`, `group_key` (the
kind, the subject and the hour bucket), `created_at`, `read_at` (null until
read). The unread count is derived from the rows whose `read_at` is null.

### moderation_actions

`id`, `actor_id`, `subject_id`, `action` (`approve`, `restrict`, `remove`,
`escalate` or `reinstate`), `reason`, `model_version` (null for a human action),
`prev_hash`, `hash`, `created_at`. Append only. Each row carries the hash of its
predecessor, so altering or removing one breaks every hash after it, and the
chain must verify end to end after any number of concurrent actions.

### entitlements

`id`, `account_id`, `feature`, `source` (`subscription`, `gift` or `grant`),
`starts_at`, `ends_at`. The product reads this table and never the subscription
table, so a gift, a grant and a paid subscription are indistinguishable at the
point of use.

### subscriptions

`id`, `account_id`, `plan_id`, `status` (`incomplete`, `active`, `past_due`,
`unpaid` or `cancelled`), `period_start`, `period_end`, `cancel_at_period_end`,
`payment_source_id`. A plan carries an interval of `month` or `year`, a price of
`1000` integer minor units and a currency of `usd`.

### page_views

`piece_id`, `viewer_key`, `window_start`. At most one row per viewer per piece
per `3600` seconds.

### Publishing and announcing are one write

A piece and the outbox row that announces it are written together, and a separate
reader picks the instruction up and carries it out. Announcing from application
code after the write has already committed is not acceptable: a failure in the
gap leaves a piece that exists on its author's profile and appears in nobody's
feed, forever, with nothing to detect it.

### Consistency

An author reading their own work reads their own writes. Anyone reading a feed
gets monotonic reads within a session. Moderation state and entitlements are read
from the primary, always, and never from a replica: a stale feed is an
inconvenience while a stale moderation state means removed content being served.

### Schema change

A schema change expands, migrates and contracts, in three deploys and never
fewer, so no single deploy both writes a new shape and removes the old one and a
rollback to the immediately previous version is always possible without data
loss.

### Seed data

Three accounts as listed in `## User roles`. Five pieces:

| Title | Author | Visibility | Tags | Shape |
|---|---|---|---|---|
| `Harbour Lights` | `nova` | `public` | `ocean`, `night` | animated, four frames |
| `Cat In A Window` | `nova` | `public` | `cats` | still |
| `Night Market Draft` | `nova` | `private` | `technology` | still |
| `Valentine Robot` | `bram` | `public` | `valentine`, `technology` | still |
| `Ocean Study` | `bram` | `unlisted` | `ocean` | still |

Six topics: `Cats`, `Christmas`, `People`, `Technology`, `Valentine`, `Ocean`.
Two palettes: `Harbour Eight`, eight entries; `Night Sixteen`, sixteen entries.
`nova` follows `bram`. `pilot` follows nobody. `Cat In A Window` carries three
likes from three distinct accounts so it is eligible for the popular feed, and
`Valentine Robot` carries one, so it is not.

`Night Market Draft` is the boundary case this product turns on: it is published,
it has a real object in the store, and it is readable by `nova` alone.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual specification that does not fit in `## UI/UX
notes`. Everything here is a requirement of the finished interface.

### Module and component architecture

The interface is built in layers, and each layer depends only on the ones below
it. Tokens depend on nothing. The primitives are a button, a pill, a sweep-painted
pill, a segmented control, a field, a card, a badge, a dropdown, a modal and a
skeleton, and they depend on tokens alone. The compositions are the chrome, the
drawer, the footer, the artwork card, the artist card, the grid, the filter row
and the topic card, and they are built from primitives. The site routes are built
from compositions. The editor shell is built from tokens and primitives only, and
the editor core sits under it and depends on nothing above it at all. Every
component belongs to exactly one of those layers, and a module that reaches
upward is in the wrong one.

Each primitive has a fixed set of variants: five sweeps for the sweep-painted
pill, each with the brightening hover; three segments for the segmented control;
one card softness with the very soft shadow; two badge shapes; one dropdown
softness with its own shadow; a modal whose header and footer carry the matching
paired corners; a skeleton carrying the loading shimmer, static under reduced
motion; and a field that is round in search and softer in a form.

### Page spine

The home page's spine, top to bottom, is the hero band, the filter row, the topic
row, the infinite artwork grid and the footer. Every other route reuses the same
spine with its own middle: the art centre replaces the hero with a header and a
filter bar, and a profile replaces it with a banner and a tab row.

### The chrome

One bar on every route, in two states. The reduced variant, on the home page,
carries `Home`, `Gallery`, `Challenges` and `App`. The full variant, on every
other route, carries `Home`, `Gallery`, `Contests`, `Challenges`, `App` and
`Pro`. The difference is a state and not a second component: the two extra
entries are hidden on the home page, and the bar does not reflow when they are,
because the search field absorbs the width.

The bar carries, left to right: a menu button that opens the drawer; the brand
mark, linking to the home page; a letter-spaced capital wordmark following the
mark, dropped as the viewport narrows; a search field with the placeholder
`Search Pixelary`, which expands into a results dropdown reading `Search all
results for ""`; the navigation entries as an icon beside a label; the segmented
drawing control; and a sign-in pill reading `Login / Sign up`, right aligned.

The segmented control is one pill cut into three segments rather than three
buttons side by side: a wide central `Start Drawing` segment carrying no rounding
at all, flanked by a paint segment rounded only on its left and an upload segment
rounded only on its right. The rounding is what proves the grouping.

The bar is fixed at the top and does not change on scroll: no shrink, no shadow
appearing, no colour change. On a site whose job is showing artwork, anything
moving up there competes with it.

### The drawer

Fourteen entries in order, each an icon beside a label: `Home`, `Gallery`,
`Digital Art`, `Challenges`, `Groups`, `Contests`, `Online Comics`, `Palettes`,
`Stages`, `Hire`, `Forums`, `Shop`, `Pixelary pro`. The drawer is the real
navigation and the chrome is a shortlist of it. It opens from the menu button and
closes by the button, by `Esc`, and by a click on the scrim, which is a dark
overlay. Focus moves into the drawer on open and returns to the button on close,
and focus is trapped while it is open.

### The footer

One flat list of sixteen links, in order, with no columns, no headings and no
social row: `Painter App`, `Tutorials`, `Topics`, `Badges`, `Blog`, `Bases`,
`Help`, `About`, `Contact Us`, `Mobile App`, `Pixelary Number App`, `Parents &
Teachers`, `Privacy Policy`, `Terms of Use`, `Shop Order Lookup`, and `Do not
Sell or Share My Personal Information`. Below them sits a smaller copyright line
reading `Copyright 2026 Pixelary Inc`. The last two entries are legal obligations
rather than navigation, and the privacy-choice control is required on every
route.

### Iconography

The iconography is closed at twenty-eight marks, authored as inline geometry, and
this is the whole set:
menu (three bars), search, home, gallery, bolt for challenges, star for contests,
a mobile device for the application, a badge for the paid tier, pencil for
drawing, brush for the paint segment, an upload arrow for the upload segment,
person for sign-in, person-plus for follow, heart for likes, eye for views, a
speech bubble for comments, funnel for the gallery filter, chevron down for every
dropdown, an overflow of three dots, close for modals, palette, group, comic
panel, stage, briefcase for hire, forum, bag for the shop, and book for the
teachers and parents link. A close control is drawn as a cross of two strokes
with rounded joins. Recolouring a mark by inverting it is not acceptable: inline
geometry takes a colour directly, and inverting is a workaround for a raster
asset this build does not have.

### The artwork card

A softly rounded surface on the page ground, carrying a very soft shadow, the
artwork filling the card's width at its own aspect, and a metadata block beneath
it. The metadata block reads, in order: the view, like and comment counts as
small muted figures on one line; the piece title in body size at weight 500; and
a line reading `By` followed by the artist handle, where `By` is set back and the
handle is not. The hierarchy is made with weight and transparency rather than
with size, which is what keeps the block compact. An animated piece carries a
small `GIF` badge at its top right, on a dark scrim with a soft text shadow.
Counts carry thousands separators at every locale and abbreviate above one
hundred thousand, and the layout must not reflow when a five-figure count becomes
six.

Hovering an artist handle opens an artist card after a pause of about half a
second, and it closes about a fifth of a second after the pointer leaves both the
trigger and the card, with the gap between them treated as part of the card.
Opening it instantly makes a gallery unusable, because a single pass across the
grid fires several. Its shadow is cast upward rather than downward, which is what
makes it read as floating above the row rather than resting on it.

### The keyframe catalogue

The keyframe catalogue is closed. Every moment named in `## UI/UX notes` is in it
and nothing else is: the rising entrance, the lateral entrance and its mirror, the
tall entrance, the two opposed floats, the loading shimmer, the crossing bar, the
expanding ring, the arriving reply that unsquashes horizontally, the rejection
shake, the drifting tiled ground, the bar arriving from above, the spinner, its
pulsing alternative, and the striped progress bar. The spinner completes a whole
turn: a loop that stops one degree short of a full rotation jumps backwards on
every revolution, and that defect in the source material is corrected rather than
copied.

### The grid

A fixed-column grid with a uniform gutter and no masonry. Artwork is displayed at
its own aspect within a fixed-width cell and cells are never cropped to a square.
Column counts, from the narrowest tier up to desktop width: two for artwork and
two for topic cards at the narrowest tier;
two and three at the small tier; three and four at the medium tier; four and six
at the large tier; and four and six again at the largest, where only the
container gutters widen.

### The profile

A full-width banner whose ground is a deep neutral where no banner artwork is
set; a large square avatar at the banner's left, overlapping its lower edge, with
a white border, softly rounded corners and nearest-neighbour rendering; the
handle above the display name, the name large and heavy in white on the banner; a
follow pill; a three-dot overflow at the banner's right edge; a tab row on a
white ground below the banner; a filter dropdown reading `All Drawings` with a
funnel icon; and the grid on the page ground. The avatar steps down in size as
the viewport narrows.

### The not-found page

A centred card on the page ground carrying the headline `Oops!`, large and heavy
in a near-black neutral; the body `Looks like something went wrong! Don't worry,
we're here to help!`; the actions `Start Drawing` as a sweep-painted pill and
`Contact Support` as a neutral pill; a small muted credit line reading `Error:
404 Page not found` followed by the artist credit; and two illustrated characters
drifting in opposition, one above the card's upper right corner and one below its
lower left.

### Copy deck

Home hero: the headline `CREATE AND SHARE ART`; the kicker `LEARN - SHARE - MAKE
PIXEL ART - SHOP`; two lines of body copy that describe what Pixelary is without
claiming an audience size; the actions `START DRAWING` and `CREATE ACCOUNT`; the
link `For Teachers and Parents`.

Filter row: `EXPLORE`, `TOPICS`, `HIGHLIGHTED`, `TRENDING`, `POPULAR`, `STAFF
PICKS`, `FEATURED`.

Chrome: the search placeholder `Search Pixelary`; the navigation `HOME`,
`GALLERY`, `CHALLENGES`, `APP`; the actions `START DRAWING` and `LOGIN / SIGN
UP`.

Consent panel: the body `We use cookies to ensure that you have the best
experience possible on our website.`; the link `Our privacy policy`; the action
`Got It`.

Editor: the tools `Pencil`, `Eraser`, `Fill`, `Line`, `Rectangle`, `Ellipse`,
`Eyedropper`, `Select`, `Lasso`, `Wand`, `Move`, `Pan`, `Dither`; the panels
`Layers`, `Frames`, `Palette`, `History`; the actions `Save`, `Export`,
`Publish`, `Undo`, `Redo`, `Resize`, `Crop`, `Trim`; the states `Saved locally`,
`Saving...`, `Not backed up`, `Offline, changes queued`.

These nine system messages carry the product's honesty commitments and may not be
softened into generic error text:

```
offline          You are offline. Your work is being saved on this device.
storage_failed   Saving is not working on this device. Export your work now.
conflict         This drawing was changed somewhere else. Both versions are
                 kept. Choose which to continue from.
lapsed           Your subscription has ended. Everything you have made is still
                 here and can still be exported.
pending          Posted. It will appear in the galleries in a moment.
removed          This piece was removed. Here is why, and how to appeal.
reinstated       This piece is back, with its original date and its credits.
index_lag        Search is catching up. Your work is not lost.
```

## Constraints

- Single tenant. One Pixelary, one set of accounts, no organisations and no
  workspaces.
- No real-time collaborative drawing session, no presence, no shared cursors and
  no operation log shared between artists. One artist edits one document.
- No direct messaging between accounts.
- No payment capture. The supporter tier is recorded as an entitlement and a
  plan; no card is taken and no invoice exists anywhere.
- No email of any kind. There is no mail server in this environment, so nothing
  is ever sent: a moderation notice, a mention and a follow all reach their
  recipient as a notification in the product and nowhere else.
- No external network call at runtime, and no third-party script, font binary,
  icon font, stylesheet, advertising tag, analytics tag or consent vendor.
- No native application. The mobile application entries in the navigation resolve
  to the not-found page.
- Forums, the shop, hiring, groups, stages, online comics, badges, tutorials,
  bases and the blog are navigation entries only. They resolve to the not-found
  page and are not built.
- No multi-region placement and no edge cache tier. The caching rules describe
  one process.
- No image-similarity search, by deliberate refusal.
- No endpoint returns accounts by age, location or any other attribute that would
  let somebody assemble a target list.
- The product name is `Pixelary`, the operating company in the footer is
  `Pixelary Inc`, the studio credited is `Northsound`, and the town named in the
  footer credit is `Northport, MN`. No audience-size claim appears anywhere: the
  source material's own figure is not this product's to repeat.
- The app must stay responsive with `2000` pieces, `200` accounts and `20000`
  likes in the database, and with a feed page of `24` pieces.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written
  to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server - never a dev
  server.
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
| `POST /api/auth/signup` | `{ display_name, email, password, date_of_birth }` | `{ account, access_token, refresh_token }` |
| `POST /api/auth/login` | `{ email, password }` | `{ account, access_token, refresh_token }` |
| `POST /api/auth/refresh` | `{ refresh_token }` | `{ access_token, refresh_token }` |
| `GET /api/health` | none | `{ status }` |
| `GET /api/pieces` | `feed`, `tag`, `sort`, `cursor`, `snapshot` | `{ pieces, next_cursor, snapshot }` |
| `POST /api/pieces` | `{ title, description, tags, visibility, parent_id, document_id, artwork }` plus an idempotency key | the created piece |
| `GET /api/pieces/{id}` | none | the piece with its lineage and counters |
| `PATCH /api/pieces/{id}` | `{ title, description, tags, visibility, remix_permission }` | the updated piece |
| `DELETE /api/pieces/{id}` | none | the tombstone |
| `GET /api/pieces/{id}/file` | none | the artwork bytes, for entitled callers only |
| `GET /api/pieces/{id}/lineage` | `depth` | the ancestor and descendant chain |
| `POST /api/pieces/{id}/likes` | none | `{ likes }` |
| `DELETE /api/pieces/{id}/likes` | none | `{ likes }` |
| `GET /api/pieces/{id}/comments` | `cursor` | a top-level JSON array of comments |
| `POST /api/pieces/{id}/comments` | `{ body, parent_comment_id }` | the created comment |
| `DELETE /api/comments/{id}` | none | the tombstone |
| `GET /api/artists/{handle}` | `tab`, `cursor` | the profile with its counts |
| `POST /api/artists/{handle}/follow` | none | `{ followers }` |
| `DELETE /api/artists/{handle}/follow` | none | `{ followers }` |
| `POST /api/artists/{handle}/block` | `{ kind }` | `{ blocked }` |
| `GET /api/topics` | none | a top-level JSON array of topics |
| `GET /api/tags` | `prefix` | a top-level JSON array of tags with counts |
| `GET /api/palettes` | `cursor` | a top-level JSON array of palettes with use counts |
| `GET /api/search` | `q`, `cursor` | `{ results, approximate_total, index_state }` |
| `GET /api/notifications` | `cursor` | `{ notifications, unread }` |
| `POST /api/notifications/read` | `{ up_to_id }` | `{ unread }` |
| `GET /api/consent` | none | `{ choices }` |
| `PUT /api/consent` | `{ choices }` | `{ choices }` |
| `GET /api/embed/{id}` | none | the embeddable view, or a neutral placeholder |

Every list endpoint returns a top-level JSON array or an object whose named
member is one. Field names are exact. Bearer authentication is required on
everything except login, signup, health, the public read endpoints and the
webhook receivers, which authenticate by signature rather than by a user token. A
successful call returns the named resource or shape; an invalid or unauthorized
call is rejected as a client error, never as a server error and never as a silent
success.

### No mocks

The artwork bytes must live in MinIO under the key scheme above. An in-memory map
of piece ids to image data, a column of image bytes in PostgreSQL, a directory of
files on the app container's own disk, and a response the app composes and hands
back to itself all fail this requirement however convincing the interface looks.
MinIO is the fact: the app's interface and its own tables can only reflect what
lives in the object store, never substitute for it. The same holds in the other
direction: an object present in the store with no row that governs who may read
it is not a published piece.

## Definition of done

A visitor can draw a piece of pixel art in the browser with no account, publish
it, and find it credited to them on their own artist page and in the public
gallery. An artist can remix somebody else's piece and both pieces carry the
credit chain afterwards. A piece its author has made private is gone from every
feed, every tag listing and every search result, and its artwork is served to
nobody but that author. Every drawing the app exports twice is the same file
both times.
