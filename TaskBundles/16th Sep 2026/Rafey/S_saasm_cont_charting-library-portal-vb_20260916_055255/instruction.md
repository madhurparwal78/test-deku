# Chartic

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser,
walk the option reference to a property, open the example beside it in the editor,
change a line, run it, and take the result away as a shared snippet address that
another browser opens with the same code loaded, without hitting an error page.

A different stranger, signed in as another contributor or not signed in at all,
must NOT be able to read a proposed example's rendered thumbnail by any means: not
through the app, not by guessing an object address, not by asking for the stream a
second time. The thumbnail bytes must live in the object store at their scheme's
key; a copy on the app container's own disk does not count, and a rendered picture
the app returns from its own memory does not count either.

## Overview

Chartic is an open source library that draws charts in a web page. This portal is
everything around that library: the manual, the gallery, the tools and the
downloads. It sells nothing and it asks for nothing. There is no signup wall in
front of anything a visitor reads, no pricing page and no trial. The one conversion
it is built for is a developer arriving with a question, finding the answer in under
a minute, and leaving with working configuration pasted into their own project.

Almost every page here is generated from structured data rather than authored as a
page. The option reference and the interface reference come from a versioned schema,
the gallery from an example corpus, the release table and the changelog from release
records. That is why the portal keeps the extracted schema for every published
release permanently: it is what lets a reader read the manual for the version they
are actually running, and what lets a property that was removed answer with the
version that removed it and the path that replaced it instead of a dead end.

The genuinely hard part is the boundary around a visitor's own material. A
contributed example is code and a theme document is data from a stranger, and both
are held back until a person publishes them: while an example is still proposed, its
rendered thumbnail exists as a real object in the store and is readable by its owner
alone.

The non-goals are as firm as the goals. What this portal deliberately is not: no comment threads, no forum, no advertising,
no visitor tracking that carries an identifier, no spreadsheet converter, no live
co-editing of a snippet, no dark theme for the portal chrome. The charts have a dark
ground and the chrome does not.

## User roles

| Role | Can do |
|---|---|
| reader | Read every published route: the option reference at any retained version, the interface reference, the gallery, the editor, the theme designer, the theme registry, the release archive and the bundle builder. Save a snippet and request a bundle build without signing in. **Cannot propose an example, publish an example, read another account's proposed example, or read a proposed example's thumbnail.** |
| contributor | Everything a reader can do, and: propose an example as a new row in their own example list, edit it while it is proposed, publish it once its validation passes, and withdraw it. **Cannot read, edit, publish or withdraw an example owned by another contributor, and cannot publish an example whose validation has not passed.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a reader session to
any contributor-only endpoint must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged.

Signup is open: anyone can create a contributor account from `/signup` with an email
and a password, and the footer of every page links the privacy page and the terms of
the licence. Three accounts are seeded for grading, all with the password
`deku-demo-pw-2026`:

| Email | Name | Role |
|---|---|---|
| `contributor@example.com` | Noor Haddad | contributor |
| `contributor2@example.com` | Teo Vargas | contributor |
| `reader@example.com` | Lior Sand | reader |

`contributor@example.com` owns the proposed example `bump-chart-lines` and the
published examples `basic-line-smooth`, `stacked-bar-margin` and
`world-population-map`. `contributor2@example.com` owns the published examples
`candle-volume-overlay`, `sunburst-nested-budget` and `radar-skills-compare`.

## Core features

### Auth

Accounts are email and password, implemented by the app. `POST /api/auth/signup`
takes `email`, `name` and `password` and creates a contributor. `POST /api/auth/login`
takes `email` and `password` and returns a bearer `token` plus the signed-in `user`.
Every later call carries `Authorization: Bearer <token>`. A token expires 24 hours
after it is issued.

1. A wrong password and an unknown email are refused with the same message,
   `Sign in failed`, so neither answer reveals whether the account exists. A missing
   token, an unknown token and a token past its expiry are all refused as
   unauthenticated, and nothing they asked to change is changed.
2. Passwords are stored hashed. The literal `deku-demo-pw-2026` must work at login
   for every seeded account and must not appear in any stored record.
3. Signup refuses an email that already has an account, naming the field, and writes
   no second account.

### 1. The versioned option reference

`/option` shows the reference for the current release; `/option/<version>` shows it
for any retained release. The aside holds a tab strip, a search field over the
current document's property paths, and the property tree. The content pane holds one
property block per property.

4. The tree is drawn as the object a reader is about to write, not as a list of
   labels: the heading above it reads `setOption({`, a foldable object row reads
   `name: {...}`, a foldable array-of-objects row reads `name: [{...}]`, a leaf row
   reads its name followed by its default in a quieter tone, and every row ends in a
   comma. A leaf whose default is too long to show ends in an ellipsis instead.
5. A property block carries the parent path in a quiet tone ending in a dot, then
   the property name, then a type badge, then the description, then the version the
   property was introduced in and, where it applies, the version it was deprecated
   in. Every block is addressed by a fragment identifier built from the document
   name and the dotted path with the dots replaced by hyphens:
   `title.show` is addressed `doc-content-title-show`.
6. A default is one of four kinds and the reference never shows one kind as
   another: a literal, shown as data; a computed default, shown as a generated
   sentence naming what it depends on plus one worked value for a stated common
   case; inherited, naming the property it inherits from; or absent. Showing a
   computed default as though it were a literal is the failure this rule exists to
   prevent, because a reader who copies it and hard-codes it has quietly broken
   their chart.
7. A shared property object is stored once and expanded at every path it appears
   at. A reader at `legend.textStyle` sees `fontSize`, `fontFamily` and `fontWeight`
   listed there, never a link to a definition elsewhere. Some properties are only
   meaningful in combination with a sibling, and rule 8 is how the reference says so.
8. Where a property's meaning depends on a sibling's value, the schema holds one
   variant per relevant value and the block shows a selector naming which variant is
   being described. `series.data` has a variant for a line series and a variant for
   a tree series, and the reference describes the chosen one rather than their union.
9. A property that was removed answers with a page saying which version removed it
   and which path supersedes it, where one is known, rather than a not-found:
   `series.hoverAnimation` was deprecated in `5.2.1`, removed in `5.3.0` and
   replaced by `series.emphasis.disabled`.
10. Reading an older version returns that version's schema and says which version
    it is. A property introduced later is absent from an earlier version's tree and
    from its search index: `legend.selectorLabel` arrived in `5.4.3` and is not in
    the `5.3.0` reference.
11. The search field matches on path segments, case-insensitively, and orders
    results by the zero-based index of the first matching segment ascending, then by
    the whole path ascending. For the query `title`, `title` and every path under it
    come before `toolbox.feature.saveAsImage.title`. Choosing a suggestion expands
    the tree along that path, selects the row and moves the content pane to that
    property's fragment. The field answers from data already in the page.
12. Arriving with a fragment expands the tree along the path, selects the row and
    positions the content pane, in that order. Scrolling the content pane past a
    property heading selects that property's row in the tree and scrolls the tree,
    and only the tree, to bring it into view. The back control returns the reader to
    the previously selected property rather than to a previous scroll position.

### 2. The interface reference

`/api-reference` is the same shell over the programmatic surface, with four
top-level nodes: `chartic`, `charticInstance`, `action` and `events`.

13. A function block carries the parent path and the name, a kind badge reading
    `Function`, a signature block in the code family with one argument per line,
    each argument's type after a colon, an optional argument marked with a question
    mark, a trailing arrow and the return type, and the version each argument was
    introduced in shown beside it inside the signature. Then the prose description,
    then a Parameters list with one entry per argument.
14. Signatures and the versions beside them come from the same schema the option
    reference is generated from. `chartic.init` reads
    `init(dom: HTMLElement | null, theme?: string | object, opts?: object) => ChartInstance`,
    with `opts` introduced in `5.2.1`.
15. A mention of another interface node inside a description is a link to that
    node; a mention of an option property is a link that leaves this document for
    the option reference at the same version. Both are generated rather than typed.

### 3. The example gallery

`/gallery` is a category rail beside a grid of cards. Each card renders the
example's real configuration against its real data and is not a picture.

16. Clicking anywhere on a card opens that example in the editor with the same
    configuration loaded.
17. A search field over the gallery matches an example's title and the set of
    property paths the example actually uses, so a visitor asking for
    `xAxis.axisLabel.rotate` gets `stacked-bar-margin` and nothing else. A filter
    narrows to examples whose data is a separate file, and a tag row narrows by a
    cross-cutting concern that is not a chart family: `animation`, `interaction`,
    `large data`, `accessibility` and `dark`.
18. The `uses` set is recorded by running the example and noting every property
    path the library actually reads, so a path set inside a loop or through a
    variable is found. It is never derived by reading the source text.
19. The category rail names a family and, beside it, the slug a developer types:
    `Line` beside `line`, `GEO/Map` beside `map`. The active row is the only row
    wearing the accent.
20. A dark chart ground, a decal pattern that fills each series with its own
    texture, and the renderer choice are one preference set, not a per-chart state.
    Setting any of them in the gallery, in the option reference or in the editor
    changes it everywhere and it survives a reload and a move to another route. The
    portal chrome stays light either way.

### 4. The example editor

`/editor` is two panes, code on the left and the chart it produces on the right.

21. The left pane offers three views of the same thing: `Edit Code`, the option
    object alone; `Full Code`, that object wrapped in everything needed to run it
    standalone; and `Option Preview`, the object the chart actually received after
    every expression in the code has been evaluated.
22. Run evaluates the code and redraws the chart, and the status area then reads
    the wall-clock time of the render, then `Chart has been generated in ` followed
    by the elapsed milliseconds to exactly two decimal places and then `ms` with no
    space before it, then the count of drawn point marks. Run is also bound to a keyboard shortcut, and the
    shortcut is part of the button's accessible name.
23. A syntax error is reported inline in the editor at its line and the previous
    chart stays on screen. A runtime error is reported in the status area with its
    message and the line it came from and the previous chart stays on screen. In
    neither case is the chart replaced by an error.
24. Code that never finishes is stopped from outside itself. An evaluation is
    terminated once it has run for 5 seconds of wall clock, or once it has taken 256
    megabytes of memory, and the status area says which budget ended it, naming
    `wall clock` or `memory`. An evaluation exceeding either is reported as stopped
    and never as a result. A budget a script checks for itself is not a budget,
    because the code being budgeted can be a loop that never yields.
25. Visitor code is untrusted and is evaluated inside a sandbox: a framed document
    granted script execution and nothing else, with no ability to spawn a process: no access to the portal's storage or to the page
    around it, no form submission, no top-level navigation, no popup, no download,
    and a content policy on the frame that denies every network request except the
    library it needs. The frame is visibly contained and carries a label naming it
    visitor content, and the label cannot be covered by what the frame draws.

### 5. Shared snippets

26. Share writes the editor's current code to a snippet and returns a short
    address. It needs no account. The address is `/s/<id>` where `<id>` is 26
    characters drawn from the lowercase letters and the digits `2` to `7`, carrying
    at least 128 bits of entropy: it is not a counter, not derived from the content
    and not guessable. Opening the address loads the editor with that code, that
    language, that library version and the preferences it was saved with.
27. A snippet saved without an account is unlisted and immutable once its editing
    window has closed. A snippet saved by a signed-in contributor is listed in their
    own snippet list and can be edited, which bumps its `revision`, or withdrawn.
28. Deletion is immediate in the serving path. A withdrawn snippet's address
    answers that it is gone, which is a different
    answer from an address that never existed, so a person following an old link
    learns that it once worked. `d4pv2sx6mhk3zrqt7nwy5bgj2f` is seeded withdrawn.
29. A snippet address served to a crawler declares a preview image and a
    description generated from the snippet's own chart, rendered once and held
    against the snippet's `revision` rather than drawn again for every request. A
    snippet saved without an account and never opened by anyone but its creator is
    deleted after 90 days; retention of an owned snippet ends when its owner
    withdraws it.

### 6. The theme designer and the theme registry

`/theme` is a control panel beside a wall of live chart previews, both scrolling on
their own. `/themes` lists every registered theme.

30. The panel leads with a Functions block holding `Download`, `Import`, `Export`,
    `Refresh`, `Reset`, `Help` and `Source Code`, then two read-only rows showing
    the theme's `Name`, defaulting to `Customised`, and its `Series` count,
    defaulting to `3`. Below that a grid of theme tiles, each showing five colour
    chips against that theme's own ground with the selected tile outlined, then an
    accordion of setting groups: `Basic Configuration`, `Visual Map`,
    `Grid (Cartesian)`, `Axes` and `Legend`.
31. Choosing a tile loads that theme into every control below and redraws every
    preview. Changing any control redraws every preview, coalesced to one redraw per
    animation frame and applied by recolouring the existing charts rather than by
    tearing them down and building them again. Dragging a colour control must not
    queue one full redraw per pointer move.
32. `Refresh` redraws every preview with new random data, so a theme is judged
    against more than one dataset. `Reset` returns every control to the selected
    tile after a confirmation. The accordion's open sections and the work in
    progress both survive a reload.
33. `Import` accepts a theme document and refuses one that is not a theme. Every
    key is checked against the theme schema, every value against its declared type,
    a colour must parse as a colour and a number must be finite. A value that is a
    function, or a string the app would evaluate, or a reference to anything outside
    the document, is refused; so is a document past the size limit or the nesting
    limit. A refused import names the offending key and changes no control.
34. Every registered theme carries a generated contrast report: the contrast of
    each series colour against that theme's own ground, the smallest perceptual
    distance between any pair, and both figures recomputed under each of the three
    common forms of colour vision deficiency. A theme that fails is labelled with
    the colliding pairs named, never removed: `sandstone` fails and stays listed.

### 7. The custom bundle builder

`/bundle` is a two-column selection of chart families and components, each with its
own size contribution, over a live estimated total.

35. A selection is a seed for a closure, not a list. Selecting `chart/bar` resolves
    `coord/cartesian`, then `component/axis`, then `scale/interval` and
    `util/format`, so the closure is those five plus `chartic/core`. The interface
    shows the closure and what pulled each member in, not only the selection, and
    the total names the raw, minified and compressed size.
36. A selection naming a module that is not in the published module graph for the
    requested version is refused before any compilation begins, naming the module.
    The requester never supplies source, a configuration file, a plugin or a path:
    they choose from the menu and the portal compiles its own published release.
37. A build is queued rather than answered inline, and the interface shows the
    queue position and then the progress. A build that exceeds its budget is stopped
    and reported as stopped rather than left to hang.
38. The same request produces a byte-identical artifact, and what is returned for
    it is fixed by the request alone. The artifact is addressed
    by the digest of its own bytes, so a second identical request is answered from
    what was already built and the digest is the same. A ready build returns the
    bundle for each requested format, an integrity hash per file in the form a page
    can use, a manifest naming the resolved closure and the sizes before and after
    minification and compression, an install snippet with that integrity hash
    already filled in, and the exact command to reproduce the artifact locally.

### 8. The release archive

`/releases` carries the download table, the verification instructions and the
changelog, all generated from release records and never typed onto the page.

39. Immutability is the whole point of a release record: a published one cannot be
    edited. A correction is a new release. Any
    attempt to change a published record is refused and the stored record is
    unchanged.
40. The download table lists, per release, the version, the release date formatted
    year, month then day separated by slashes, a link to the source archive with a
    link to its signature beside it, and a link to the built artifacts. Under it
    sits a link to the archive of previous versions.
41. The portal states only hashes it computed itself from the artifact it
    published. A mirror whose recorded hash differs from the record is removed from
    the download table at once rather than flagged, and a mirror merely serving an
    older release is shown marked stale. The table shows, per mirror, when it was
    last verified.
42. A changelog entry has one shape, which is the contract with the release
    process: a kind in square brackets, then an area in square brackets, then a
    sentence, then its references, then its credits in parentheses. The version rail
    beside it is the complete release history and is never a window on it. Generation
    of every part of this route is from the records; nothing on it is typed in place.

### 9. Contributed examples

`/my/examples` is a contributor's own list. A new example is proposed as a new row
added inline at the top of that list and edited in place, never on a separate page,
and the row appears the moment it is added with a message confirming the save and
the row reverting if the save is refused.

43. A proposed example's rendered thumbnail is a real object in the store at the
    key scheme `thumbnails/{example_id}/{sha256_of_bytes}.svg`, for example
    `thumbnails/bump-chart-lines/a319ed61bc2c850dc1f06b05a0f22ca22876df0af2aeb72ca80283276a58a176.svg`.
    While the example is `proposed`, `GET /api/examples/<id>/thumbnail` serves those
    bytes to the owning contributor alone: the same request from
    `contributor2@example.com`, from `reader@example.com` and from a caller with no
    token is denied, and the object is never reachable by an unauthenticated address
    of any kind. The proposed example is absent from the gallery, from the gallery
    search and from the public example list. Once it is published the same stream
    answers for everybody.
44. Publishing is refused until the example's validation has passed. An example
    must run without error, produce at least one series, declare a category matching
    the series it creates, and render the same under both renderers within the stated
    tolerance unless it declares one renderer. A refused publish names the failing
    check and leaves the example `proposed`.
45. Only the owner may read, edit, publish or withdraw their own proposed example.
    A request from another contributor is answered as though the example does not
    exist, so the list of who is working on what does not leak.
46. An example never enters the corpus unattended: publishing is always an
    explicit act by the owning contributor, never a consequence of a successful
    validation run.

### 10. The portal's own surface

47. An address that does not exist renders the portal's own not-found page, which
    answers not-found, quotes the address that was asked for, offers a way back to
    the reference, and, where the last segment of the address is a property path an
    earlier version carried, names the version that removed it and the path that
    replaced it. That last line is the point: on a manual almost every dead link is
    a renamed property.
48. A privacy page at `/privacy`, linked from the footer of every page, states what
    is collected about a visitor and for how long. What is collected is a search's
    query text and the rank of the result that was opened, and nothing else: no
    identifier of any kind, no session stitched across requests and no address.
    Aggregation is the only form the portal keeps, individual records are discarded
    within 24 hours, and no third party receives any of it.
49. A form submitted by something that is not a person is refused. Every form
    carries an unattended field named `website_url` which a person never fills, and a
    submission arriving with it filled is refused and writes nothing. A visitor who
    submits the same form repeatedly, more than 10 times inside 60 seconds, is
    refused for the rest of that window and told to wait.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | The portal's front door: what the library is, the current release line, and the way into the reference | public |
| `/login` | Sign in | public |
| `/signup` | Create a contributor account | public |
| `/option` | The option reference at the current release | public |
| `/option/<version>` | The option reference at a retained release | public |
| `/api-reference` | The interface reference | public |
| `/gallery` | The example gallery | public |
| `/editor` | The example editor | public |
| `/s/<id>` | A shared snippet, opened in the editor | public |
| `/theme` | The theme designer | public |
| `/themes` | The theme registry with each theme's contrast report | public |
| `/releases` | The release archive, the download table and the changelog | public |
| `/bundle` | The custom bundle builder | public |
| `/my/examples` | A contributor's own examples and snippets | contributor |
| `/privacy` | What the portal records about a visitor | public |
| `/sitemap.xml` | Every public route, as a sitemap | public |
| `/robots.txt` | The crawler file, pointing at the sitemap | public |

Every route sits behind one fixed sidebar. The sidebar groups its destinations
under `Reference` listing Option reference, Interface reference and Gallery, under
`Tools` listing Editor, Theme designer and Bundle builder, and under `Project`
listing Releases and Privacy. The signed-in contributor's own list is the last item.
The sidebar never scrolls away, and nothing in it is more than one move from
anything else.

### Entry and redirects

- An unauthenticated visitor opening `/my/examples` lands on `/login` and, after
  signing in, arrives at `/my/examples` rather than at the front door.
- Signing in from `/login` with no destination in mind lands on `/option`.
- Signing out returns to `/` and any later call with the retired token is refused
  as unauthenticated.
- A token that expires part way through an edit leaves the row as it was: the save
  is refused, the row reverts to its stored values, a message says the session ended
  and the reader is offered `/login`.
- A reader signed in and opening `/my/examples` sees their own empty list, not
  another account's; a reader calling a contributor-only endpoint directly is denied
  and nothing changes.
- `/option/9.9.9`, a version the portal never published, renders the not-found page.

### Journeys

1. **Read a property and take the example away.** Open `/option`. The landing
   state selects the first node, `title`, and shows its page. Type `rotate` into the
   aside's search field, choose `xAxis.axisLabel.rotate`, and watch the tree expand
   along `xAxis`, then `axisLabel`, with the row selected and the content pane
   sitting on that property. Read the type badge, the description and the version
   the property arrived in. Press `Edit` on the example strip above the property
   list and land in `/editor` with that example's configuration loaded.
2. **Find every example that uses a property.** Open `/gallery`, type
   `xAxis.axisLabel.rotate` into the gallery search, and see exactly one card,
   `Stacked Bar with Margins`. Clear it, choose the tag `large data`, and see
   `World Population Map` and `Candlestick with Volume`. Turn on the filter for
   examples whose data is a separate file and only `World Population Map` remains.
3. **Change a chart and share it.** From `/editor`, switch to `Option Preview` and
   read the object the chart actually received. Return to `Edit Code`, change the
   series smoothing, press `Run`, and read the status area: the time of the render,
   the elapsed milliseconds to two decimal places, and the point count. Press
   `Share`, copy the address it returns, open that address in a second browser and
   find the same code loaded.
4. **Hit the two failure shapes.** In `/editor`, delete a closing brace and press
   `Run`: the error is marked at its line and the chart already on screen stays
   there. Undo, paste a loop that never ends and press `Run`: after 5 seconds the
   status area says the wall clock budget ended it and the chart is still there.
5. **Take a build away.** Open `/bundle`, tick `chart/bar`, and see the closure
   grow to `chart/bar`, `coord/cartesian`, `component/axis`, `scale/interval`,
   `util/format` and `chartic/core`, with each addition naming what pulled it in and
   the total showing the raw, minified and compressed size. Request the build, watch
   the queue position and then the progress, and when it is ready copy the install
   snippet with its integrity hash already in place.
6. **Propose an example and publish it.** Sign in as `contributor@example.com`,
   open `/my/examples`, press `New example` and fill the row that appears at the top
   of the list in place: the title, the category, the tags and the code. The row is
   there the moment it is added and a message confirms the save. Press `Publish`
   while its validation has not passed and read the refusal naming the failing
   check. Fix the category to match the series the code creates, press `Publish`
   again, and find the example in `/gallery`.
7. **Try to read somebody else's proposed work.** Sign in as
   `contributor2@example.com` and open `/my/examples`: `bump-chart-lines` is not
   listed. Ask for it directly and be answered as though it does not exist. Ask for
   its thumbnail and be denied.
8. **Read the manual for the version you are running.** Open `/option/5.3.0`. The
   page says which version it is, `legend.selectorLabel` is absent from the tree,
   and `series.hoverAnimation` answers with its own page naming `5.3.0` as the
   version that removed it and `series.emphasis.disabled` as its replacement.
9. **Check a release before installing it.** Open `/releases`. The download table
   shows `5.4.3` released `2026/02/18` with its source archive, its signature and
   its built artifacts, the mirror `mirror-alpha` with the time it was last verified,
   and `mirror-gamma` marked stale. `mirror-beta` is not in the table at all. Walk
   the two numbered verification procedures under it, then read the changelog entries
   for that release in the version rail.
10. **Judge a theme before shipping it.** Open `/themes` and read `Sandstone`'s
    contrast report: the failing pairs are named and the theme is still listed. Open
    `/theme`, choose the `Dark Slate` tile, watch every preview redraw, press
    `Refresh` to judge it against different numbers, then press `Download` and take
    the document away.

### States

Every list has an empty state naming what would fill it and the action that
creates it: `/my/examples` with nothing in it reads `No examples yet` above
`Propose your first example`; the gallery filtered to nothing reads
`No examples match` above `Clear filters`; the aside's search with no match reads
`No property matches`. Every page has a loading state that holds the exact space
its content will occupy, so nothing on the page moves when the content arrives; a
gallery card holds its chart's height from the first paint. Every error is shown in
place with what failed and what to do next, and no error replaces the page with a
stack trace or an empty screen.

## UI/UX notes

**North star.** A reader should understand, in the first moment, that this is a
reference they can trust and read for an hour: the page is quiet, the words are the
subject, and the only saturated colour on screen is a chart.

**Register.** This is an operational document system, not a marketing site. It
reads quiet and organised, built for scanning and for repeated visits, so there is
no oversized hero, no editorial composition and no atmosphere layered over the
content. The one place expressive colour is allowed is the chart itself, because the
chart is the product.

**Layout archetype: sidebar-nav.** A fixed aside on the left carries the
navigation on every route and never scrolls away with the content. On the option and
interface references that aside is the shell: a tab strip, a search field and the
property tree, with the tree scrolling inside the aside independently of the
document beside it. Those are two separate scrolling regions and treating them as
one is the mistake this arrangement most invites. The tools, the editor and the
theme designer, put two panes side by side and scroll each on its own.

**Density: compact.** Tree rows and property headings sit tight so a reader can see
a whole branch at once, and the reference wins its space back from chrome rather
than from the reading measure. Space over dividers: sections read as separate
because of the room around them, and a hairline appears only under a heading and
between list items.

**Palette by role.** The ground is a near-white neutral and it is almost the whole
page. A document route adds one cool neutral band across the top and one deep cool
neutral strip at the bottom, and those are the only two surfaces on the page that
are not the ground. Body text is a deep neutral; supporting text is a mid cool
neutral, deliberately quieter, and it is used almost twice as often as the body
tone, which is the whole design: most of what a reader sees is turned down so that
the little which is not pulls the eye without shouting.

Two accents, and the split is deliberate. The brand accent is a light, vivid red,
and it wears the brand mark, the active sidebar row and the route loading bar and
nothing else. Inside a generated reference document the accent is a mid, soft red
instead: a saturated one against thirty screens of body copy is unreadable, and the
document accent carries the page title, the selected tree row and a property name
while the parent path in front of that name drops to a light, muted red so the eye
lands on the leaf. A link inside body copy is a mid, soft cyan; a link inside the
front door's own sections is a light, soft blue. The primary action is a light,
vivid blue and it is the only thing on a page wearing it; the secondary action is a
mid cool neutral. A control that is selected is a light, vivid blue; accepted input
is a mid, soft green; a recoverable problem is a light, vivid orange; rejected input
is a light, soft red. Meaning is never carried by colour alone: every one of those
four states also carries a word.

The chart series palette is the one burst of saturated colour on the site, and it
runs light vivid blue, mid vivid lime, mid cool neutral, light vivid orange, mid
vivid cyan, mid vivid amber, light vivid red and mid soft indigo, in that order.
The first entry of that palette is also the primary action colour and the third is
the secondary action colour: the interface and the charts share a root, and a
substitute palette must keep that relationship. The exact shades are yours so long
as the roles and the exclusivity above hold.

**Type.** Typography is two families, and the split is a decision to keep. The interface and the
front door use `"Open Sans", "PingFang SC", Helvetica, Arial, sans-serif`, loaded at
400 and 800. A generated reference document uses the system stack instead,
`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC",
"Microsoft YaHei", "Hiragino Sans GB", "Helvetica Neue", Helvetica, Arial,
sans-serif`, loading nothing: thirty screens of body copy is where a web font costs
most and helps least, and a family break between the chrome and the content is the
right trade. Code is `"Source Code Pro", monospace`. The second family in each stack
is a locale fallback and must be preserved.

The scale is measured and is not a modular ratio, because it is the accumulation of
a document system, a front door and a control library, and imposing a ratio would
change three unrelated surfaces at once. The sizes: 75px over 90px at weight 800 for
the one front-door headline; 35px over 38.5px at 800 for a section heading; 34px
over 46px at 400 for the title of a generated document; 28px over 31px for the word
Properties above a property list; 22px over 24.2px for a document route's page
title; 21px over 30px for the front-door subtitle; 20px over 25px for a property
name; 18px over 22px for a property heading row; 16px over 22.8571px for a primary
button label; 16px over 20px for the parent path in front of a property name; 14px
over 20px for the base, which is most of the page; 13px over 18.5714px for a tree
row and for the search field; 12px over 17.1429px for a caption. Figures align
wherever amounts stack.

**Shape and depth.** Corners are barely softened on controls and code spans, a
little more on a standard action, and fully rounded on the front door's two hero
actions and on a pill. A navigation panel is square where it meets the sidebar and
rounded where it leaves it, so it reads as an extension of the sidebar rather than
as a floating card. Shadow is used one way only: an even halo with no vertical
offset, which says this is above the page and never this is a card. Nothing anywhere
carries a shadow that falls down and to the right. No gradient appears in the
chrome or in the content; the only two places one is allowed are the colour picker's
hue and saturation tracks and the loading skeleton's sweep.

**Motion character: eased.** Movement reads as a designed interface rather than as
a machine: one signature ease-out for anything that arrives, opens, expands or
slides in, and one symmetric in-out for anything that changes in place. There is no
third default and no third curve. The site's default duration is on the slow side and that softness is
deliberate, so a selection colour, a button ground and a tree row all
settle rather than snap. Nothing scrubs to the scroll position. On the front door, elements start
invisible and are revealed as they enter the window in a three-step stagger inside a
group, the heading, then the mark beside it, then the paragraph under it, and
anything already in the window on arrival reveals immediately in the same stagger;
once an element has revealed it never un-reveals on scrolling back. The one showy
moment on the whole portal is the front door's mark, whose eight wedges
unfold one after another and which can be replayed from the control at its centre. A blanket
transition on every property is a defect and not a style: name the properties that
move.

Under a reduced-motion preference the reveal does not animate and every element is
present at full strength on arrival; the mark does not play on arrival and its play
control stays available so a visitor can choose to see it; the pulse on that control
does not run; the route loading bar keeps animating, because it carries information
and removing it removes the information; and every transition collapses to a
non-zero minimum rather than to nothing, because several controls wait on a
transition ending and a duration of zero can stop that ever firing.

**Components by their states.** Every interactive element has a resting, a
pointed-at, a pressed, a focused and an unavailable state, and unavailable is never
signalled by colour alone. Escape closes a panel and returns focus to the control
that opened it. A destructive action confirms first, naming what it will act on. A
gallery card lifts its border to the link tone and gains the halo when pointed at. A
toggle shows its label beside it, and its state is exposed rather than implied. A
tab that leaves the portal is marked as leaving it, rather than dressed to look like
its neighbours.

**Feedback.** A save, a publish, a copy and a withdraw each raise a short message
that names what happened and clears itself, and the row it belongs to shows the new
value at once and reverts with that message if the save is refused.

**Accessibility floors, which are contract and not taste.** Body text and its
background meet WCAG AA contrast, and so does the quiet supporting tone and the
dimmed inactive row in a topic list: quiet text that recedes is the intent, and it
survives being readable. The focus indicator is visible on every interactive element
and holds 3 to 1 against both the element and its surroundings. Touch targets are
comfortably sized. Zoom is never restricted, because the base text is small and a
reader who needs it larger has no other recourse. Full keyboard navigation
throughout: a skip link is the first focusable element and moves focus to the main
region; the tree is a single tab stop where up and down move between visible rows,
right expands, left collapses and then moves to the parent, and enter selects; the
search suggestion list moves with up and down, chooses with enter, dismisses with
escape, and the field announces how many suggestions there are; and the code pane
can be left with escape followed by tab, because trapping a keyboard reader inside a
code editor is the most common failure of a page like this. Every icon-only control
carries a text label. One banner region, one navigation region inside it, one main
region per route, one content-info region for the footer, and a complementary region
for the reference aside; exactly one first-level heading per route, with levels
descending without skipping. Every embedded chart carries a text description
generated from its own data, naming the chart family, how many series it has, what
each axis spans and the highest and lowest values with their labels; a gallery
card's chart is decorative because the caption names it, and is hidden from
assistive technology. The decal control is exposed as a labelled preference with its
state, not as a novelty.

**Responsive behaviour.** Nothing changes across the desktop range: the arrangement
holds from the widest viewport down to the tablet width, and there is one real
switch below it. At that switch the sidebar collapses to a control at the right and
its panels become an inline list; the reference aside becomes a full-width strip
above the content carrying the tab strip, whose four items reorder to `Option`, `API`,
`Tutorial`, `GL`, because on a phone a reader is far likelier to want the tutorial than
the three-dimensional reference, then a row holding a tree control and the search
field, with the tree itself behind that control opening as a full-height
overlay that closes when a row is chosen and moves the content pane; the topic rail
on a document route moves above the content as a collapsed list; the gallery rail
becomes a horizontally scrolling strip and the grid becomes one column; and the
editor and the theme designer stack, code above chart and controls above previews.
The gallery's column count steps down the widths rather than flowing, and a card
keeps its chart height at every count so the cards grow wider and never taller.
Focus order follows the visual order at every width, including after that switch.
Nothing overflows sideways at the narrowest viewport and every navigation target
stays reachable there. The exact breakpoints are yours; the switch is one, not
three, and the steps are a staircase rather than a fluid rule.

## Front-end specification

This section carries the measured surface of the portal. It governs appearance and
arrangement; every rule that decides what the app does lives in `## Core features`.

### The five shells

The frontend architecture is server-rendered documents progressively enhanced in
place, so a shell is a template rather than a client-side layout component. Every
route is one of five shells, and the shell decides the layout before the
content does.

| Shell | Chrome | Body | Routes |
|---|---|---|---|
| front door | fixed sidebar | full-width stacked sections on the ground | `/` |
| document | fixed sidebar | a tinted page header band, then a two-column body: a topic rail on the left and a content column beside it | `/releases`, `/themes`, `/privacy`, the not-found page |
| documentation | fixed sidebar | a fixed aside holding a tab strip, a search field and a tree, and a scrolling content pane beside it | `/option`, `/option/<version>`, `/api-reference` |
| gallery | fixed sidebar | a fixed category rail on the left and a card grid filling the rest | `/gallery` |
| application | fixed sidebar | two panes divided near the half, each independently scrolled | `/editor`, `/theme`, `/bundle` |

### Global chrome

A route loading bar sits at the very top edge and runs while a route is being
fetched. Its leading edge carries a double glow in the brand accent, which is the
only glow anywhere on the portal, and it keeps animating under a reduced-motion
preference because it is a progress indicator.

The sidebar is fixed, sits above the page on an even halo, and carries the brand
mark at its top: a ring with a gap in the brand accent, an arc of roughly fifty
degrees removed at its upper right, a filled dot centred in that gap, and the
wordmark beside it set solid and uppercase in the interface family at weight 800.
The brand link is named for the product, not for the image inside it.

Under the mark come the three groups named in `## User flow`. A group heading is a
quiet caption; a destination is a row that takes the surface-hover tone when
pointed at and the brand accent when it is the current route. Five of the
destinations open a panel listing their own sub-destinations: a panel is square
where it meets the sidebar and rounded where it leaves it, opens on focus as well
as on hover, closes on escape and returns focus to its toggle, and changes only its
ground and its halo when it opens rather than transforming. On the panel matching
the current route, pointing at it lightens the label and both of its
pseudo-elements and does not lighten its top rule.

Below the sidebar's destinations sits a foundation banner naming the software
foundation that holds the trademark, and at the foot of every route a footer on the
one deep cool neutral surface in the portal, carrying the licence line, the links to
the privacy page and the terms of the licence, and a row of icon targets each of
which carries a text name. The trademark mark is set as a superscript beside the
product name.

The chrome deliberately has no global search field, no account menu for a reader who
is not signed in, no language switch, no theme switch for the chrome itself and no
announcement strip.

### Components

Nine components carry the whole portal.

**Button.** Four variants. A hero action is tall, fully rounded, on the primary
action ground with white ink at 16px over 22.8571px, carrying a glyph inset from its
left edge and vertically centred in the label's colour; the secondary hero action is
the same shape on the secondary action ground. A standard action is content height,
lightly rounded, on the primary action ground with white ink at 14px. A tertiary
action is transparent with link-tone ink and a soft offset halo. A pill is fully
rounded at its own height on the front-door link tone. A control-library button is
short, barely rounded, on the state colours with control ink at 13px at weight 500.
Every variant settles its ground rather than snapping it.

**Card.** The gallery card is the only real card in the portal: the ground, a
hairline border, barely rounded, holding a rendered chart at the card's full inner
width and a fixed height, with the caption beneath it at 14px weight 700 in the body
tone, on one line, ellipsised when it is too long. Pointing at it lifts the border to
the link tone and raises the halo.

**Topic rail.** Used by every document route. A caption reading `Topics`, then a
narrow list of rows; the active row wears the brand accent, an inactive row is the
body tone at reduced strength but still at the contrast floor, and a bullet marks
the row outside its text column. The rail tracks the content column in both
directions: the row matching the heading nearest the top of the window is the active
one, and choosing a row moves the content column to that heading.

**Page header band.** The tinted cool neutral band at the top of a document route,
carrying the route title at 40px over 44px at weight 700 in the body tone, a
subtitle beneath it at 16px over 22.8571px in a muted cool neutral, and a trademark
line under that in a lighter cool neutral. A subtitle that runs to several lines
grows the band and the trademark line follows it down.

**Inline code.** The code family at 14.4px over 22px on a very light warm ground
with a deep red ink, barely rounded, with a little padding. A preformatted block uses
the same family at 13px on a light neutral ground, a touch more rounded.

**Search field.** Sits inside the reference aside: an input on the ground with
control ink at 13px, rounded on its left edge only, and an appended button on a
sunken neutral with quiet ink rounded on its right edge only, carrying a small
magnifier glyph centred in it. The suggestion list sits on the ground under a soft
halo.

**Tree.** Short rows. A row carries a fold triangle in a quiet control tone at its
left and the label at 13px over 17px, indented one level per depth on the label and
not on the row. The selected row takes the document accent as its ground with white
ink; an unselected row is transparent with body-tone ink. A toolbox at the right of
the tree's heading row carries one action reading `Collapse All` in the link tone.
The tree renders only expanded nodes: a collapsed branch has no rows in the page at
all.

**Toggle.** A short track, fully rounded, on the control border tone when off and
the selected-control tone when on, with a round white knob travelling its length. The
label sits to the right of the track and is the control's accessible name, and the
state is exposed rather than implied.

**Tab strip.** Centred items; the selected item is full height with near-black ink
and a rule beneath it in the brand accent, an unselected item is near-black at
reduced strength, and an item that leaves the portal is in the link tone and carries
the outbound marker. The outbound marker is decorative and hidden from assistive
technology; that a link leaves the portal is said in the link's name instead.

### Iconography

Every icon is drawn geometry or a font glyph, and there is no icon image in the
chrome. The home mark is the largest piece of geometry in the portal: eight wedges
around a centre, each wedge's corner radius and outer radius shrinking together with
the wedge, drawn in the eight chart series colours in their palette order, with a
round play control at the centre. The outbound marker is a small square with an
arrow leaving its upper right. The repository glyph, the play control, the front
door's two action glyphs, the loading spinner, the close control and the category
rail's per-family glyphs are all drawn from the same icon font at a single weight.
A favicon is served and declared in the head of every route.

### The documentation shell

The aside is fixed, sits above the page on an even halo, and never scrolls with the
document. At its top a tab strip of four items: `Option`, `API`, `GL` and
`Tutorial`. The first three swap both the document in the content pane and the tree
in the aside; the fourth leaves the portal and is marked as leaving it. Switching
between the first three is a route change and not a filter: a different tree, a
different search index and a disjoint fragment space, and the reader arrives at the
top of the new document rather than at a preserved position.

Under the strip sits the search field, and under that the tree, which scrolls
independently of the aside around it. The content pane runs from the aside's right
edge to the window's right edge and scrolls with the window, with the body copy
inset from the pane's left edge.

The content pane carries the document title at 34px over 46px at weight 400 in the
document accent, then the description as body copy in the document body tone, then
an embedded example in a framed chart, then the word `Properties` at 28px over 31px
in a light neutral with a hairline beneath it, then the property blocks. A property
block's heading row carries the parent path at 16px over 20px in the quiet document
accent ending in a dot, then the property name at 20px over 25px in the document
accent, then a bordered type pill carrying the type name, then the description at
14px in the document body tone, with a fold chevron at the right of the heading row.
The parent path being quieter than the property name is what makes a list of forty
properties scannable: the eye lands on the leaf and reads the path only when it
needs to.

Above the property list on a branch page sits an example strip: a `Dark Mode`
toggle, a `Decal Pattern` toggle beside it, a `Render` button carrying a settings
glyph that opens a choice of renderer, an `Edit` link aligned to the strip's right
that opens the example in the editor, and the framed example itself. Those three
controls are the one shared preference set of rule 20 and not a per-example state.

A tab pinned to the right edge of the content pane, vertically centred, reads
`Preview` and opens a panel showing the example for the current property. It exists
because an example wide enough to be useful competes with the prose it illustrates.

The whole document is present in the page, all of its tens of thousands of pixels of
height, which is expensive and is kept deliberately: it is what lets the browser's
own find-in-page search the entire reference, and loading it in pieces would quietly
break that. Property blocks below the window are rendered but their embedded examples
are not started until they approach the window.

### The option reference

Arriving with no fragment selects the first node, `title`, and shows its page. The
tree's top level, in order: `title`, `legend`, `grid`, `xAxis`, `yAxis`, `polar`,
`radiusAxis`, `angleAxis`, `radar`, `dataZoom`, `visualMap`, `tooltip`,
`axisPointer`, `toolbox`, `brush`, `geo`, `parallel`, `parallelAxis`, `singleAxis`,
`timeline`, `graphic`, `calendar`, `matrix`, `thumbnail`, `dataset`, `aria`,
`series`, `darkMode`, `color`, `backgroundColor`, `textStyle`, `animation`,
`animationThreshold` and `animationDuration`. Below that the tree runs between three
and seven levels deep depending on the branch. Versioning of the reference is carried by a version selector above the tab strip,
defaulting to the current release and listing every retained release.

### The interface reference

Four top-level nodes rather than thirty-four: `chartic`, the global object;
`charticInstance`, a chart instance; `action`, the set of messages that can be sent
to a chart; and `events`, the set it emits. A function page carries the parent and
the name in the document accent, a kind badge reading `Function`, the signature
block described in rule 13, a prose description with cross-references, and a
`Parameters` list with one bullet per argument, the name as a code span followed by
its paragraphs.

### The gallery

The category rail is a fixed narrow column of rows, each a glyph in a small box
then a label. The families, in order: `Line`, `Bar`, `Pie`, `Scatter`, `GEO/Map`,
`Candlestick`, `Radar`, `Boxplot`, `Heatmap`, `Graph`, `Lines`, `Tree`, `Treemap`,
`Sunburst`, `Parallel`, `Sankey`, `Funnel`, `Gauge` and `PictorialBar`.

The header row above the grid carries the category name at 26px at weight 400 in the
body tone with the category slug immediately after it at 16px in the muted tone, the
search field, the tag row, the external-data filter, and a `DARK MODE` pill at the
right edge carrying a knob and its label at 13px letterspaced, with a hairline
beneath the whole row. The slug beside the name is the value a developer types shown
next to the word a human reads.

Charts render as they approach the window and are torn down once they are more than
two screens past it, and scrolling fast must cancel the renders queued for cards that
have already left. A card that has not rendered shows the loading skeleton's sweep at
the exact height its chart will occupy, so no card moves when it fills. The renderer
is chosen per card: the vector renderer for a small static thumbnail, because vector
output stays sharp at any pixel density, and the raster renderer for a chart carrying
more than a thousand points. Above sixteen cards in the render window the grid serves
a pre-rendered vector still instead of a live chart and upgrades a card to a live
chart when the pointer enters it or it takes focus; on a device reporting reduced
processing capability or a preference for saving data it always serves the still.

### The editor

The left pane carries the tab strip of `Edit Code`, `Full Code` and
`Option Preview`, where the selected tab takes the link tone on the ground with a
rule beneath it in the same tone and an unselected tab takes the body tone on a light
neutral. Under it a tool row holds a language toggle of two chips, one reading `JS`
on an amber ground and one reading `TS`, then three named controls, a dependency
picker, a runtime switch between the two-dimensional and three-dimensional runtimes,
and a view of the generated standalone document, then the `Run` button on the link
tone in white carrying a play glyph. Under that the code pane, with line numbers in
a gutter, fold markers and syntax colouring.

The right pane carries a toolbar holding the `Dark Mode` toggle, the
`Decal Pattern` toggle and a `Render` button, then the chart frame on the ground
inside a hairline border, then a footer bar holding `Download`, `Screenshot` and
`Share`, with the status area aligned right carrying the render report at 13px in the
muted tone. The divider between the panes is a hairline and can be dragged.

`Download` gives the chart as a vector document at the size it is displayed with
fonts converted to outlines, and `Screenshot` gives it as a raster image at twice the
display resolution on the current ground. Both are produced in the page from the live
chart rather than by a round trip, because the chart is already there and a round
trip would send the visitor's data away. The one case that does need the server is
the preview image for a shared snippet.

### The theme designer

The control panel is a fixed column on the left scrolling on its own, and the
preview pane beside it scrolls on its own, headed `Chart Preview`. The `Functions`
block is collapsible with a chevron at its right and holds its seven controls in a
grid: `Download` as the primary action, then `Import` and `Export` beside it, then
`Refresh` and `Reset` on the next row, then `Help` and `Source Code`, the last of
which leaves the portal. Persistence of the panel is per visitor: the selected tile, the accordion's open
sections and the work in progress all survive a reload. The theme tile grid is two
columns wide; the accordion
beneath it gives each group a header with its label at the left and a chevron at the
right over a hairline divider, and a body holding labelled colour pickers, numeric
fields, select fields and toggles.

The preview wall is two columns of cards, each on the ground inside a hairline
border, barely rounded, with a centred title at 20px weight 700 and a centred
subtitle at 13px in the muted tone, five glyph controls at the card's top right for
restore, save, data view, zoom region and zoom reset, and the chart filling the
card's inner width. The cards, in order: `Line Chart`, `Stacked Area Chart`,
`Bar Chart`, `Stacked Bar Chart`, `Scatter Chart` and `Pie Chart`.

The colour picker is the one component carrying a gradient: a hue track running the
full spectrum, a saturation and lightness square, an alpha track, a field for a
typed value and a set of recently used swatches.

`/themes` lists the ready-made themes as a three-column grid of preview cards, each
a composite of six miniature charts drawn in that theme with the theme's name
beneath and its contrast report beside it. Those composites are pre-rendered rather
than drawn live, because there are dozens of them and each is six charts.

### The release archive

The structure of the route is five blocks and no topic rail. The download table
carries the columns `Version`, `Release Date`,
`Download Source from a Mirror` and `Dist files`, one row per release, with a
centred link beneath it to the archive of previous versions. Under the table sit two
numbered procedures, one for signature verification and one for checksum
verification, each naming its command and its arguments, with a note paragraph
between them. The archive filenames inside those procedures carry the version as a
placeholder rather than as a literal, so the instructions never go stale. A licence
block closes the route, naming the licence and linking its full text.

The route leads with the package manager path rather than burying it, because a
package manager is how most readers install anything: a tab strip of
three copyable one-line install commands, then the archive path beneath it for
readers who need it, then the entry point to the bundle builder reading
`build a bundle with only what you need` with a sentence saying what it saves.

The changelog's version rail replaces the topic rail: a caption reading `Versions`,
then one row per release carrying the version and its date, with the current row in
the brand accent. The content beside it carries a version heading at 26px in the
document accent with the release date aligned right on the same line, then the entry
bullets. A `Kind` and an `Area` are in the body tone, the sentence is body copy with
property names as inline code spans, the references are issue numbers prefixed with
a hash and commit identifiers each linking out, and the credits are contributor
handles comma separated in parentheses, each linking out. An entry may carry several
references and several credits.

### The front door

One screen. The hero carries the brand line at 75px over 90px at weight 800 in the
display tone, the subtitle beneath it at 21px over 30px in the subtitle tone, and
the two fully rounded hero actions under that, with the animated mark to their right
at the desktop widths and beneath the copy at the narrow one, where nothing overlaps
it. A release banner names the newest release and updates with the record rather
than by hand. Below the hero, a features section of cards each with a drawn icon, a
heading at 16px weight 700 and a paragraph at 14px over 24.5px, generated from the
same source as the features copy rather than authored twice. Then a citation section
with its headline at 25px over 36px and a fully rounded citation action, then a
follow section whose heading is 35px over 38.5px at weight 600 and whose buttons are
the only offset shadow in the portal, then the footer.

### Assets

There is no binary asset to supply. The brand mark, the home mark's eight wedges,
every chrome glyph, the theme tiles' colour chips and the preview composites are all
drawn from geometry or from the icon font. Where the reference site served a
photograph, this portal serves nothing: there is no contributor portrait, no event
poster and no texture anywhere. Any image the portal does render carries alternative
text, and a decorative one declares itself decorative.

### Performance

Only the compressed font format is served, subset, with two faces preloaded. No
image is served at more than twice its rendered size. A route that renders no chart
does not load the charting library at all. No blanket transition declaration
survives anywhere. First contentful paint stays under 1.2 seconds on a mid-range
phone over a slow connection on every route; largest contentful paint stays under
2.5 seconds on the front door and the document routes and under 4 seconds on the two
references, which get the looser budget because they deliberately ship the whole
document; cumulative layout shift stays under 0.05 everywhere; interaction to next
paint stays under 200 milliseconds; the first chart is on screen within 2 seconds in
the gallery and the editor; and expanding a tree node paints its rows within 100
milliseconds.

## Technical requirements

Serve this portal as server-rendered pages progressively enhanced in the browser,
not as a client-side application that fetches its own HTML. The backend is
**FastAPI with Jinja templates** and the browser layer is **Alpine.js over those
server templates**. The first paint a browser receives is the complete document for
the route, rendered on the server from the schema, the example corpus and the
release records; Alpine.js then attaches the behaviour that needs a client, which is
the tree, the aside search, the preference toggles, the editor, the theme designer's
preview wall and the bundle builder's live total. A route's content is never a
skeleton that JavaScript fills in from a second request.

The datastore is **PostgreSQL**, read from `DATABASE_URL`. Object bytes live in
**MinIO**, an S3-compatible object store, read from `STORAGE_ENDPOINT`,
`STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. The app's own
address and port come from `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode a
host or a port; read every one of them from the environment. Both backing services
are **already running** and reachable at those variables and must not be
downloaded, installed, compiled or started.

Use only the libraries named here plus their direct dependencies. Do not introduce
a second database, cache, queue, object store, identity provider or mail vendor: the
only backing services available in this environment are PostgreSQL and MinIO, and
reaching for anything else is a contract violation.

**Identity, and the principle behind it.** No account is required to read anything,
to run anything, to share anything or to build anything. An account exists for
exactly one job here: to let somebody manage the examples and snippets they created.
It holds an identifier, an authentication method, a display name and the list of
things it owns, and nothing else: no profile, no stored preferences and no history of
what was read.

Authentication is app-implemented email and password with bearer tokens, as described
under `### Auth`. Passwords are stored hashed and never in a recoverable form.
Authorisation is by role and by ownership, and nothing else in the portal checks a
role at all.

**Rate limiting and abuse.** Per-address rate limiting applies to every write and
every evaluation, with a low burst and a low sustained rate, because an evaluation is
expensive and a page view is not. Reading is not rate limited beyond ordinary network
protection. The evaluation surface is rate limited far more strictly than any read
surface, and a signed-in caller gets a higher limit rather than no limit. An
evaluation's output is not persisted and is not addressable afterwards, so the portal
cannot be used as free hosting. A caller whose repeated executions hit a budget from the
same address gets a lower sustained rate for longer. Abuse of the share surface is answered by rule 49 and by
the report control on every snippet route, which sends the address to a review queue.

`GET /api/health` returns `200` once the app is ready to serve. Log each request as
one structured line carrying the method, the path, the status and the elapsed
milliseconds, to standard output.

**Headers on every response.** Every response carries a strict transport policy, a
nosniff content-type policy, a frame policy, a referrer policy and a content
security policy. The content security policy for the framed document that evaluates
visitor code denies every network destination except the app's own origin, and it
denies form submission, top-level navigation and popups for that frame.

**Nothing the browser downloads carries a credential.** No database URL, no object
store access key, no object store secret and no bearer token belonging to another
account appears in any document, script, stylesheet or JSON the browser can fetch.
The object store's own key material stays server-side: the browser reaches object
bytes only through the app's own stream endpoint.

**A favicon** is served at `/favicon.ico` and declared in the document head of
every route.

**Every public route declares its own title and description**, and no two routes
share either. `/option` and `/option/5.3.0` differ, because the version is part of
what the route is about.

**Every public route declares a social preview title and a preview image**, and the
preview image resolves to real bytes. A snippet route's preview image is the
rendered chart for that snippet's own code, produced once and held against the
snippet's `revision`, and its preview description is the generated chart
description. It is never rendered inside the crawler's own request.

**A sitemap** at `/sitemap.xml` lists every public route, including one entry per
retained option-reference version and one per published example, and `/robots.txt`
points at it.

**Determinism where the portal makes a promise.** Both promises below are
deterministic in the strict sense: the same input gives the same bytes, on any
machine and after a restart. A bundle build for one request
produces the same bytes every time, which means the bundler version, the compiler
target, the minifier and its options are all pinned and every timestamp and absolute
path is kept out of the output. The rendered thumbnail for one example's
configuration is likewise the same bytes every time, which is what lets it be
addressed by the digest of those bytes.

**Budgets are enforced from outside the thing being budgeted.** An evaluation of
visitor code is stopped by the surrounding process when it passes 5 seconds of wall
clock or 256 megabytes of memory, and a bundle build is stopped when it passes 30
seconds or 1 gigabyte. Code that never
yields cannot be stopped by code inside it.

**The object store is the only home for object bytes.** A rendered thumbnail and a
built bundle artifact live in the bucket under their key schemes and nowhere else:
not on the app container's filesystem, not as a column in a table, and not held in
the app's memory between requests. What the portal shows and what its own tables
record can only reflect what is in the bucket; neither may stand in for it.

## Data model

Eleven tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a credential to protect. Hash it as normal; the exact literal must
work at login, and it must be written into `/app/USER_README.md` alongside each
account so a grader can sign in.

**`users`** - `id`, `email` unique, `name`, `role` in `reader` or `contributor`,
`password_hash`, `created_at`. Three rows are seeded, as listed in `## User roles`.

**`releases`** - `version` unique, `released_on`, `commit`, `is_current`,
`published_at`. Three rows are seeded and every one of them is immutable once
published:

| version | released_on | is_current |
|---|---|---|
| `5.4.3` | `2026-02-18` | true |
| `5.3.0` | `2025-11-05` | false |
| `5.2.1` | `2025-07-22` | false |

**`release_artifacts`** - `release_version`, `filename`, `size_bytes`, `sha256`,
`sha512`, `signature_filename`, `attestation`. One row per release, keyed by filename:

| filename | sha256 |
|---|---|
| `chartic-5.4.3.tar.gz` | `7d8968eb8880d7605fda3b6af5eaac8bac52c01423eb7d1f862ab732e9e82787` |
| `chartic-5.3.0.tar.gz` | `68ae5dcb7020eeebfe4f65558278857872e42d7da87979b884c4b5e5beb65c88` |
| `chartic-5.2.1.tar.gz` | `a47ad78a060a73e0347e48d4f425f31169ab858bd302bb4c71d05b9b95d74efe` |

The `5.4.3` archive's `sha512` is
`264915ce0335931833e3d3230344e2b1534f09ae6c179c7ffab856e44eff0e5e16c4299fe9c5be69c89a77664b8065c26374fefdada2c82aeb2ce04d136913ee`
and its signature file is `chartic-5.4.3.tar.gz.asc`. Its `attestation` is the
provenance record: the source revision it was built from, the builder that built it
and the toolchain that built it, signed by the build system rather than by a person,
so a reader can check that the archive is what that revision builds. A signature says
somebody approved the file; provenance says the file is what it claims to be built
from.

**`mirrors`** - `host`, `release_version`, `recorded_sha256`, `serves_version`,
`status` in `active`, `stale` or `removed`, `last_verified_at`. `status` is derived
from the other columns rather than typed: a mirror whose `recorded_sha256` differs
from its artifact's `sha256` is `removed`, one whose `serves_version` is older than
the release it is listed under is `stale`, and one matching on both is `active`.
Three rows are seeded against `5.4.3`:

| host | recorded_sha256 | serves_version | status |
|---|---|---|---|
| `mirror-alpha.chartic-portal.example` | matches the artifact | `5.4.3` | `active` |
| `mirror-beta.chartic-portal.example` | `aec03af8d255a240eaff00776dd6a087c7a87a63faf0449357a3f179406c574b` | `5.4.3` | `removed` |
| `mirror-gamma.chartic-portal.example` | matches the artifact | `5.3.0` | `stale` |

**`changelog_entries`** - `release_version`, `position`, `kind`, `area`,
`sentence`, `references`, `credits`. Two rows are seeded for `5.4.3`: a `Feature`
in the area `legend` reading `Added legend.selectorLabel for the inverse selector`
with the reference `#9142` and the credit `nhaddad`, and a `Fix` in the area
`series` reading `Restored emphasis scaling on a single-point series` with the
references `#9107` and `#9118` and the credit `tvargas`.

**`schema_nodes`** - `release_version`, `path`, `kind` in `object`,
`array_of_objects` or `leaf`, `types`, `default_kind` in `literal`, `computed`,
`inherited` or `absent`, `default_literal`, `default_sentence`,
`default_worked_value`, `inherits_from`, `enum_values`, `applies_to`, `since`,
`deprecated`, `removed`, `replaced_by`, `shared_object`, `variant_of`,
`variant_value`, `description`, `position`. The pair (`release_version`, `path`) is
unique, and one node's row is never shared between two versions. The nodes seeded
for `5.4.3`, beyond the thirty-four top-level branches named in
`## Front-end specification`:

| path | kind | default | since |
|---|---|---|---|
| `title.show` | leaf, boolean | literal `true` | `5.0.0` |
| `title.text` | leaf, string | literal `''` | `5.0.0` |
| `title.textStyle` | object, shared `textStyle` | absent | `5.0.0` |
| `legend.textStyle` | object, shared `textStyle` | absent | `5.0.0` |
| `tooltip.textStyle` | object, shared `textStyle` | absent | `5.0.0` |
| `tooltip.trigger` | leaf, string, enum `item`, `axis`, `none` | literal `item` | `5.0.0` |
| `legend.selectorLabel` | object | absent | `5.4.3` |
| `xAxis.axisLabel` | object | absent | `5.0.0` |
| `xAxis.axisLabel.rotate` | leaf, number | literal `0` | `5.0.0` |
| `xAxis.axisLabel.margin` | leaf, number | literal `8` | `5.0.0` |
| `yAxis.axisLabel` | object | absent | `5.0.0` |
| `yAxis.axisLabel.rotate` | leaf, number | literal `0` | `5.0.0` |
| `dataZoom.filterMode` | leaf, string, enum `filter`, `weakFilter`, `empty`, `none` | literal `filter` | `5.0.0` |
| `toolbox.feature.saveAsImage.title` | leaf, string | literal `'Save as image'` | `5.0.0` |
| `series.barWidth` | leaf, number or string | computed | `5.0.0` |
| `series.label.position` | leaf, string | inherited from `label.position` | `5.0.0` |
| `series.emphasis.scale` | leaf, boolean | literal `true` | `5.3.0` |
| `series.data` | array of objects, variant per `series.type` | absent | `5.0.0` |
| `series.hoverAnimation` | leaf, boolean | literal `true` | `5.0.0` |

The shared object `textStyle` holds the leaves `color`, `fontSize` with the literal
default `12`, `fontFamily` with the literal default `'sans-serif'` and `fontWeight`
with the literal default `'normal'`. It is stored once and expanded at each of the
three paths above.

`series.barWidth` is the worked computed case: its generated sentence reads
`Worked out from the width of the axis band and the number of bar series sharing
it`, and its worked value is `31` for one bar series on a category axis of six
categories in a plot area 720 wide.

`series.data` carries two variants: for `series.type` of `line` its entry is a
number or a two-member array, and for `series.type` of `tree` its entry is an object
carrying `name`, `value` and `children`.

`series.hoverAnimation` is the removal case: `deprecated` is `5.2.1`, `removed` is
`5.3.0` and `replaced_by` is `series.emphasis.disabled`. It is present in `5.2.1`
with no `removed`, and in `5.3.0` and `5.4.3` with `removed` set.
`legend.selectorLabel` exists only under `5.4.3`. `series.emphasis.scale` exists
under `5.3.0` and `5.4.3` and not under `5.2.1`.

**`interface_nodes`** - `release_version`, `path`, `member_kind` in `function`,
`property` or `event`, `signature`, `returns`, `arguments`, `description`,
`since`, `position`. Four top-level nodes are seeded, and `chartic.init` carries the
signature named in rule 14 with `dom` required and `theme` and `opts` optional,
`opts` since `5.2.1`. `charticInstance.setOption` carries
`setOption(option: object, notMerge?: boolean, lazyUpdate?: boolean) => void`.

**`examples`** - `id` unique slug, `title`, `category`, `tags`, `code_js`,
`code_ts`, `data_inline`, `data_file`, `difficulty` in `introductory`, `standard` or
`advanced`, `since`, `uses`, `renderer` in `canvas`, `svg` or `either`,
`thumbnail_key`, `description`, `origin` in `authored`, `contributed` or `derived`,
`state` in `proposed` or `published`, `owner_id`, `validated_at`, `created_at`.
Seven rows are seeded:

| id | title | category | state | data |
|---|---|---|---|---|
| `basic-line-smooth` | `Smoothed Line` | `Line` | published | inline |
| `stacked-bar-margin` | `Stacked Bar with Margins` | `Bar` | published | inline |
| `world-population-map` | `World Population Map` | `GEO/Map` | published | file `population-2026.json` |
| `candle-volume-overlay` | `Candlestick with Volume` | `Candlestick` | published | inline |
| `sunburst-nested-budget` | `Nested Budget Sunburst` | `Sunburst` | published | inline |
| `radar-skills-compare` | `Skill Comparison Radar` | `Radar` | published | inline |
| `bump-chart-lines` | `Bump Chart` | `Lines` | proposed | inline |

`stacked-bar-margin` is the only seeded example whose `uses` carries
`xAxis.axisLabel.rotate`. `world-population-map` and `candle-volume-overlay` are the
only two carrying the tag `large data`, and `world-population-map` is the only one
with a `data_file`. `radar-skills-compare` carries the tag `dark`,
`basic-line-smooth` carries `animation`, and `stacked-bar-margin` and
`sunburst-nested-budget` carry `interaction`. `bump-chart-lines` belongs to
`contributor@example.com`, is `proposed`, has no `validated_at`, and declares the
category `Lines` against code that creates a line series, which is the mismatch its
first publish attempt is refused for.

`basic-line-smooth`'s generated description reads
`Line chart with 1 series. The category axis runs Mon to Sun. Values run from 120 to 260, highest on Sat, lowest on Mon.`
and its seven values draw a count of `7` point marks, one per category.

**`snippets`** - `id` unique, `code`, `language`, `library_version`, `renderer`,
`theme`, `decal`, `created_at`, `updated_at`, `owner_id` nullable, `visibility` in
`unlisted` or `public`, `forked_from`, `revision`, `withdrawn_at`. Two rows are
seeded: `qkzm4p2vx7hd3nzr6tsw5bjy4c` at `revision` `1`, unlisted, owned by
`contributor@example.com`, and `d4pv2sx6mhk3zrqt7nwy5bgj2f` withdrawn, whose address
answers gone.

**`themes`** - `id` unique slug, `name`, `origin` in `built_in` or `contributed`,
`values`, `series_colours`, `ground` in `light` or `dark`, `contrast_report`,
`preview_key`, `since`. Four rows are seeded: `default` named `Default`, light, whose
`series_colours` are the eight chart series colours in their palette order;
`dark-slate` named `Dark Slate`, dark; `vintage` named `Vintage`, light; and
`sandstone` named `Sandstone`, light, whose `contrast_report` fails and names its
colliding pairs.

**`modules`** - `release_version`, `module_id`, `requires`, `raw_bytes`. The graph
seeded for `5.4.3`:

| module_id | requires | raw_bytes |
|---|---|---|
| `chartic/core` | none | `118500` |
| `chart/bar` | `coord/cartesian` | `41200` |
| `chart/line` | `coord/cartesian` | `38600` |
| `chart/pie` | none | `22400` |
| `coord/cartesian` | `component/axis` | `33800` |
| `component/axis` | `scale/interval`, `util/format` | `27600` |
| `scale/interval` | none | `11900` |
| `util/format` | none | `9400` |
| `component/legend` | `util/format` | `15300` |
| `component/tooltip` | `util/format` | `24700` |

`chartic/core` is always in a closure. Selecting `chart/bar` alone resolves the
closure `chartic/core`, `chart/bar`, `coord/cartesian`, `component/axis`,
`scale/interval`, `util/format`, whose raw total is `242400`.

**`bundle_builds`** - `request_digest` unique, `release_version`, `selection`,
`renderers`, `locale`, `formats`, `minify`, `sourcemap`, `closure`, `artifact_key`,
`artifact_sha256`, `integrity`, `sizes`, `status` in `queued`, `building`, `ready`
or `failed`, `queue_position`, `requested_at`, `ready_at`, `expires_at`. A build is
addressed by the digest of its normalised request, so the same request finds the
same row rather than starting a second build. `expires_at` is 30 days after
`ready_at`.

**`page_events`** - `id`, `route`, `occurred_at`, `query_text` nullable,
`result_rank` nullable. It carries no account, no session and no address, which is
what the privacy page states. A row older than 24 hours is discarded and only the
aggregate survives.

**Object keys.** A rendered thumbnail is stored at
`thumbnails/{example_id}/{sha256_of_bytes}.svg`, for example
`thumbnails/bump-chart-lines/a319ed61bc2c850dc1f06b05a0f22ca22876df0af2aeb72ca80283276a58a176.svg`.
A built bundle artifact is stored at `bundles/{artifact_sha256}/chartic-{format}.js`,
for example
`bundles/9f50bbd1dd7cc573d0583ffec5eb6b75506187df98b8743f9f86405ba41d2c35/chartic-esm.js`,
and its integrity hash is
`sha384-aLheSBb58TNzRBFVuFY/RHlS6/61NJMzhZGcc3VCm0NIsiUSfvsxHKXBdXCU3/3y`.
`basic-line-smooth`'s thumbnail is stored at
`thumbnails/basic-line-smooth/f7b809e012ada4d2b9afdd8464ace025532124a3c9253071e5afb429da7e6780.svg`.

**Invariants, as properties of the running portal.**

- A released row and its artifacts, once published, never change. Two attempts to
  change one published release, arriving at the same moment, both leave the stored
  record exactly as it was.
- A snippet identifier is never reused, and two shares arriving at the same instant
  produce two different addresses and two rows.
- Two identical bundle requests arriving at the same moment produce exactly one
  build and one artifact digest, and both callers are answered with that digest.
- An example's `state` moves from `proposed` to `published` once and only by its
  owner. Two publish calls for the same example arriving together leave exactly one
  published row and no second thumbnail object.
- A thumbnail object is never overwritten with different bytes at the same key,
  because the key carries the digest of the bytes.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- One portal, no tenancy: every reader sees the same published corpus.
- No spreadsheet converter, no pasted-data chart recommendation and no data
  profiling of any kind.
- No live co-editing of a snippet and no presence channel: a snippet address is
  opened by one person at a time and the portal shows no other visitor's cursor.
- No palette extraction from an uploaded image, and no image upload anywhere.
- No second language: every route is served in one language and there is no language
  segment, no language switch and no translation record.
- No handbook, no tutorial content, no frequently-asked-questions route, no cheat
  sheet, no resources index and no extension directory hosted here.
- No community section: no events route, no committer list, no mailing list and no
  contribution guide.
- No security advisory route and no machine-readable advisory feed.
- No public telemetry dashboard, no advertising, no third-party script and no
  consent banner, because nothing recorded carries an identifier.
- No schema migration engine and no configuration rewriter.
- No external network call at runtime: the portal answers every route from
  PostgreSQL, MinIO and its own published source.
- No native application and no installable app shell.
- The portal stays responsive with three retained schema versions of roughly four
  hundred property nodes each, seven examples, four themes and a ten-module graph.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment;
  never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of
  the shell. An ordinary background job dies with its shell, and the app will not be
  running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy of
  any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

Every list endpoint returns a top-level JSON array. Bearer auth is carried on
everything except `GET /api/health`, `POST /api/auth/login` and
`POST /api/auth/signup`. A successful call returns the named resource or shape; an
invalid or unauthorized call is rejected as a client error, never with a `5xx` and
never with a silent success.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `name`, `password` | `token`, `user` with `id`, `email`, `name`, `role` |
| `POST /api/auth/login` | `email`, `password` | `token`, `user` |
| `POST /api/auth/logout` | none | `{}`, and the token is retired |
| `GET /api/me` | none | `user` |
| `GET /api/releases` | none | array of `version`, `released_on`, `is_current`, `artifacts`, `mirrors` |
| `GET /api/releases/{version}` | none | one release with `artifacts`, `mirrors`, `changelog` |
| `PATCH /api/releases/{version}` | any field | rejected: a published record is immutable |
| `GET /api/schema/{version}/tree` | none | array of top-level nodes, each with `path`, `kind`, `has_children` |
| `GET /api/schema/{version}/node` | `path` | one node with `path`, `kind`, `types`, `default_kind`, `default_literal`, `default_sentence`, `default_worked_value`, `inherits_from`, `enum_values`, `since`, `deprecated`, `removed`, `replaced_by`, `shared_object`, `variants`, `description`, `fragment_id`, `children` |
| `GET /api/schema/{version}/search` | `q` | array of `path`, `types`, `default_summary`, `first_sentence`, `first_match_index`, in rank order |
| `GET /api/interface/{version}/node` | `path` | one node with `path`, `member_kind`, `signature`, `returns`, `arguments`, `description`, `since`, `cross_references` |
| `GET /api/examples` | `category`, `tag`, `q`, `external_data` | array of `id`, `title`, `category`, `tags`, `has_external_data`, `thumbnail_url`, `description` |
| `GET /api/examples/{id}` | none | one example with `code_js`, `code_ts`, `uses`, `renderer`, `state`, `description` |
| `GET /api/examples/{id}/thumbnail` | none | the stored object's bytes as `image/svg+xml` |
| `GET /api/my/examples` | none | array of the caller's own examples, `proposed` and `published` |
| `POST /api/my/examples` | `title`, `category`, `tags`, `code_js`, `website_url` | one example, `state` `proposed` |
| `PATCH /api/my/examples/{id}` | any of the above | the updated example |
| `POST /api/my/examples/{id}/validate` | none | `passed`, `checks` with one entry per named check |
| `POST /api/my/examples/{id}/publish` | none | the example with `state` `published`, or a refusal naming the failing check |
| `DELETE /api/my/examples/{id}` | none | `{}`, and the example is withdrawn |
| `POST /api/snippets` | `code`, `language`, `library_version`, `renderer`, `theme`, `decal`, `website_url` | `id`, `url`, `revision` |
| `GET /api/snippets/{id}` | none | one snippet, or gone when it was withdrawn |
| `PATCH /api/snippets/{id}` | `code` | the snippet with `revision` incremented |
| `POST /api/render` | `option`, `renderer` | `elapsed_ms`, `points_drawn`, `description`, `document`, or a typed error naming the budget |
| `GET /api/preferences` | none | `dark`, `decal`, `renderer` |
| `PUT /api/preferences` | `dark`, `decal`, `renderer` | the stored preference set |
| `GET /api/themes` | none | array of `id`, `name`, `origin`, `ground`, `series_colours`, `contrast_report` |
| `POST /api/themes/validate` | the theme document | `valid`, or a refusal naming the offending key |
| `GET /api/modules/{version}` | none | array of `module_id`, `requires`, `raw_bytes` |
| `POST /api/bundles` | `release_version`, `selection`, `renderers`, `locale`, `formats`, `minify`, `sourcemap` | `request_digest`, `closure` with one `pulled_in_by` per member, `sizes`, `status`, `queue_position` |
| `GET /api/bundles/{request_digest}` | none | the build with `status`, `artifact_sha256`, `integrity`, `manifest`, `install_snippet`, `rebuild_command` |

### No mocks

PostgreSQL and MinIO are the facts. A thumbnail the app keeps as a byte string in a
Python variable, a bundle artifact written to `/app/build/` on the container's own
disk, a `thumbnail_url` that returns a picture the app drew on the spot rather than
the stored object, a hardcoded `{"valid": true}` the theme validator returns to
itself, a list of examples held in a module-level dictionary: each of these is a
contract violation however good the page looks. The named provider is the fact - the
app's UI and its own tables can only reflect what lives in the provider, never
substitute for it.

## Definition of done

A developer can walk the option reference to a property at the version they are
running, open the example beside it in the editor, change a line, run it, and take
the result away as an address another browser opens with the same code loaded. A
property that was removed tells them which release removed it and what replaced it.
A contributor's proposed example is readable by that contributor alone until they
publish it, and its rendered thumbnail is a real object in the store either way.
