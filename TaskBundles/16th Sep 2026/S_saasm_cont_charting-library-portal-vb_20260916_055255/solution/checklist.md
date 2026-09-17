# Checklist: Chartic

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, technical, datamodel, constraints, deployment
Sections absent: buildplan
Items: 739
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` A reader walks an option path into the editor, then takes the round trip away as a shared snippet address another browser opens with the same code loaded. `src: Overview para 1; opening paragraph, para 1`
- [ ] `C-OV-02` `constraint` A proposed thumbnail stream stays forbidden to every caller but the owning contributor. `src: Overview para 3; opening paragraph, para 2`
- [ ] `C-OV-03` `constraint` The proposed thumbnail bytes land in the object store at the key scheme, never as a copy on the app container's own disk. `src: Overview para 3; opening paragraph, para 2`
- [ ] `C-OV-04` `capability` An older release version keeps the extracted schema permanently, so a reader reads the reference for the release being run. `src: Overview para 2`
- [ ] `C-OV-05` `capability` A removed property names the removal version plus the replacement path. `src: Overview para 2`
- [ ] `C-OV-06` `constraint` No signup wall stands in front of a public listing, so a reader reaches every published example unsigned. `src: Overview para 1`
- [ ] `C-OV-07` `constraint` A nonsense address reads the portal own not-found page rather than a comment thread, a forum, an advertisement, a spreadsheet converter or a co-editing cursor, none of which the portal carries. `src: Overview para 4; Constraints`
- [ ] `C-OV-08` `ui` The portal chrome stays light even when the DARK MODE chart ground is on. `src: Overview para 4; Core features rule 20`

## C-RL User roles

- [ ] `C-RL-01` `role` A reader reads the option reference at an older version without signing in. `src: User roles table, reader row`
- [ ] `C-RL-02` `role` A reader shares a snippet whose identifier is well formed without signing in. `src: User roles table, reader row`
- [ ] `C-RL-03` `role` A reader requests a bundle selection whose closure resolves without signing in. `src: User roles table, reader row`
- [ ] `C-RL-04` `role` A reader calling a contributor endpoint cannot write a row. `src: User roles table, reader row`
- [ ] `C-RL-05` `role` A reader cannot publish, because a contributor endpoint refuses the reader session. `src: User roles table, reader row`
- [ ] `C-RL-06` `role` A reader never sees a proposed example in a public listing. `src: User roles table, reader row`
- [ ] `C-RL-07` `role` A reader asking for a proposed thumbnail stream is forbidden. `src: User roles table, reader row`
- [ ] `C-RL-08` `role` A contributor proposes an example, whose publish is refused until the named validation checks pass. `src: User roles table, contributor row`
- [ ] `C-RL-09` `role` A contributor edits a proposed example, whose revision bumps for the owner alone. `src: User roles table, contributor row`
- [ ] `C-RL-10` `role` A contributor publishes an example once every named validation check passes. `src: User roles table, contributor row`
- [ ] `C-RL-11` `role` A contributor withdraws an example, leaving one published example row behind. `src: User roles table, contributor row`
- [ ] `C-RL-12` `role` Another contributor asking for the example is answered as though the example is absent. `src: User roles table, contributor row`
- [ ] `C-RL-13` `role` A contributor whose validation has not passed is refused a publish. `src: User roles table, contributor row`
- [ ] `C-RL-14` `constraint` Authorization runs server-side, so a reader calling a contributor endpoint cannot reach a write. `src: User roles para 2`
- [ ] `C-RL-15` `constraint` A reader's direct call to a contributor endpoint writes no row. `src: User roles para 2`
- [ ] `C-RL-16` `constraint` Signup creates a contributor from an email plus a password, refusing a duplicate email. `src: User roles para 3`
- [ ] `C-RL-17` `ui` The footer on every route reaches the privacy page, whose statement names what is collected. `src: User roles para 3; Front-end specification, Global chrome`
- [ ] `C-RL-18` `literal` The seeded account `contributor@example.com`, named `Noor Haddad`, is stored once with the role `contributor`. `src: User roles, seeded accounts table`
- [ ] `C-RL-19` `literal` The seeded account `contributor2@example.com`, named `Teo Vargas`, is stored once with the role `contributor`. `src: User roles, seeded accounts table`
- [ ] `C-RL-20` `literal` The seeded account `reader@example.com`, named `Lior Sand`, is stored once with the role `reader`. `src: User roles, seeded accounts table`
- [ ] `C-RL-21` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`, stored as a hash. `src: User roles para 3; Data model, opening`
- [ ] `C-RL-22` `data` `contributor@example.com` owns the proposed example `bump-chart-lines`, absent from every public listing. `src: User roles, closing para`
- [ ] `C-RL-23` `data` The gallery search over `uses` returns only `stacked-bar-margin`, one of the examples `contributor@example.com` owns. `src: User roles, closing para`
- [ ] `C-RL-24` `data` The external data filter narrows the corpus to `world-population-map`, leaving the examples `contributor2@example.com` owns out. `src: User roles, closing para`

## C-CF Core features

- [ ] `C-CF-01` `capability` `POST /api/auth/signup` takes `email`, `name`, `password`, creating a contributor. `src: Core features, Auth`
- [ ] `C-CF-02` `capability` `POST /api/auth/login` takes `email` plus `password`, returning a bearer `token` beside the signed-in `user`. `src: Core features, Auth`
- [ ] `C-CF-03` `contract` Every later call carries `Authorization: Bearer <token>`, so a missing token is refused. `src: Core features, Auth`
- [ ] `C-CF-04` `constraint` A token expires 24 hours after being issued, so an unknown or expired token is refused. `src: Core features, Auth`
- [ ] `C-CF-05` `literal` A wrong password is refused with the message `Sign in failed`. `src: Core features rule 1`
- [ ] `C-CF-06` `constraint` An unknown email is refused with the same message as a wrong password, so neither answer reveals whether the account exists. `src: Core features rule 1`
- [ ] `C-CF-07` `constraint` A missing token is refused as unauthenticated. `src: Core features rule 1`
- [ ] `C-CF-08` `constraint` An unknown token is refused as unauthenticated. `src: Core features rule 1`
- [ ] `C-CF-09` `constraint` A signed-out token is refused as unauthenticated, leaving unchanged whatever the call asked to change. `src: Core features rule 1`
- [ ] `C-CF-10` `constraint` The literal `deku-demo-pw-2026` works at login for a seeded account, never appearing in a stored record. `src: Core features rule 2`
- [ ] `C-CF-11` `constraint` Signup refuses a duplicate email, naming the field, writing no second account row. `src: Core features rule 3`
- [ ] `C-CF-12` `ui` The tree heading reads `setOption({` above the property rows. `src: Core features rule 4`
- [ ] `C-CF-13` `ui` A foldable object row in the tree reads `name: {...}`. `src: Core features rule 4`
- [ ] `C-CF-14` `ui` A foldable array-of-objects row in the tree reads `name: [{...}]`. `src: Core features rule 4`
- [ ] `C-CF-15` `ui` A leaf row in the tree reads the name followed by the default in a quieter tone. `src: Core features rule 4`
- [ ] `C-CF-16` `ui` Every tree row ends in a comma. `src: Core features rule 4`
- [ ] `C-CF-17` `ui` A leaf whose default is too long to show ends the row in an ellipsis. `src: Core features rule 4`
- [ ] `C-CF-18` `capability` A property block carries the parent path in a quiet tone ending in a dot, then the property name. `src: Core features rule 5`
- [ ] `C-CF-19` `capability` A property block carries a type badge after the property name. `src: Core features rule 5`
- [ ] `C-CF-20` `capability` A property block carries the version the property was introduced in. `src: Core features rule 5`
- [ ] `C-CF-21` `capability` A property block carries the deprecation version where one applies. `src: Core features rule 5`
- [ ] `C-CF-22` `literal` The property block of `title.show` carries the fragment identifier `doc-content-title-show`. `src: Core features rule 5`
- [ ] `C-CF-23` `constraint` A property block's fragment identifier is built from the document name plus the dotted parent path with the dots replaced by hyphens. `src: Core features rule 5`
- [ ] `C-CF-24` `capability` A literal default is served as data. `src: Core features rule 6`
- [ ] `C-CF-25` `capability` A computed default is served as a generated sentence naming what the value depends on beside one worked value for a stated common case. `src: Core features rule 6`
- [ ] `C-CF-26` `capability` An inherited default is never served as a literal default, naming instead the property inherited from. `src: Core features rule 6`
- [ ] `C-CF-27` `capability` An absent default is served as absent, never as a literal default. `src: Core features rule 6`
- [ ] `C-CF-28` `constraint` A computed default is never served as a literal default. `src: Core features rule 6`
- [ ] `C-CF-29` `capability` A shared property object is stored once, expanded at every path the object appears at. `src: Core features rule 7`
- [ ] `C-CF-30` `literal` The shared object at `legend.textStyle` expands `fontSize`, `fontFamily`, `fontWeight` in place, never as a link to a definition elsewhere. `src: Core features rule 7`
- [ ] `C-CF-31` `constraint` `series.data` holds one variant per series type, because some properties are meaningful only in combination with a sibling. `src: Core features rule 7`
- [ ] `C-CF-32` `capability` Where a property's meaning depends on a sibling's value the schema holds one variant per relevant value. `src: Core features rule 8`
- [ ] `C-CF-33` `ui` A property block whose schema holds variants shows a selector naming which variant is being described. `src: Core features rule 8`
- [ ] `C-CF-34` `literal` `series.data` holds a variant for a line series plus a variant for a tree series, rather than the union. `src: Core features rule 8`
- [ ] `C-CF-35` `capability` A removed property answers with a page naming the version that removed the path, at the current version, rather than a not-found. `src: Core features rule 9`
- [ ] `C-CF-36` `literal` The removed property `series.hoverAnimation` names `5.2.1` as the deprecation version. `src: Core features rule 9`
- [ ] `C-CF-37` `literal` The removed property `series.hoverAnimation` names `5.3.0` as the removal version. `src: Core features rule 9`
- [ ] `C-CF-38` `literal` The removed property `series.hoverAnimation` names `series.emphasis.disabled` as the replacement. `src: Core features rule 9`
- [ ] `C-CF-39` `capability` Reading an older version returns that version's schema, naming which version the reader is on. `src: Core features rule 10`
- [ ] `C-CF-40` `constraint` A property introduced later is absent from an earlier version's tree. `src: Core features rule 10`
- [ ] `C-CF-41` `constraint` A property introduced later is absent from an earlier version's search index. `src: Core features rule 10`
- [ ] `C-CF-42` `literal` The later property `legend.selectorLabel` arrived in `5.4.3`, so the older version `5.3.0` omits the path. `src: Core features rule 10`
- [ ] `C-CF-43` `capability` The aside search matches on path segments, case-insensitively. `src: Core features rule 11`
- [ ] `C-CF-44` `capability` The aside search orders results by the zero-based index of the first matching segment ascending, then by the whole path ascending. `src: Core features rule 11`
- [ ] `C-CF-45` `literal` For the query `title`, the search orders `title` plus every path under the branch before `toolbox.feature.saveAsImage.title`. `src: Core features rule 11`
- [ ] `C-CF-46` `ui` Choosing a suggestion expands the tree along the path, selects the row, moves the content pane to that property's fragment. `src: Core features rule 11`
- [ ] `C-CF-47` `constraint` The document search orders its matching segments from data already in the page rather than from a network call. `src: Core features rule 11`
- [ ] `C-CF-48` `ui` Arriving with a fragment expands the tree along the path, selects the row, positions the content pane, in that order. `src: Core features rule 12`
- [ ] `C-CF-49` `ui` Scrolling the content pane past a property heading selects that property's row in the tree, scrolling the tree alone to bring the row into view. `src: Core features rule 12`
- [ ] `C-CF-50` `ui` The back control returns the reader to the previously selected property rather than to a previous scroll position. `src: Core features rule 12`
- [ ] `C-CF-51` `literal` The interface reference carries four top-level nodes, `chartic`, `charticInstance`, `action`, `events`. `src: Core features feature 2 preamble`
- [ ] `C-CF-52` `capability` An interface signature block carries each argument beside the parent path plus the name. `src: Core features rule 13`
- [ ] `C-CF-53` `ui` A function block carries a kind badge reading `Function`. `src: Core features rule 13`
- [ ] `C-CF-54` `capability` A signature block carries one argument per line with each argument's type after a colon. `src: Core features rule 13`
- [ ] `C-CF-55` `capability` An optional argument in a signature is marked with a question mark. `src: Core features rule 13`
- [ ] `C-CF-56` `capability` A signature block carries a trailing arrow before the return type. `src: Core features rule 13`
- [ ] `C-CF-57` `capability` A signature block carries the version each argument was introduced in. `src: Core features rule 13`
- [ ] `C-CF-58` `ui` A function page carries a `Parameters` list with one entry per argument after the prose description. `src: Core features rule 13`
- [ ] `C-CF-59` `contract` The interface signature of `chartic.init` reads `init(dom: HTMLElement | null, theme?: string | object, opts?: object) => ChartInstance`. `src: Core features rule 14`
- [ ] `C-CF-60` `literal` The signature argument `opts` of `chartic.init` carries `5.2.1` as its since version. `src: Core features rule 14`
- [ ] `C-CF-61` `capability` A mention of another interface node inside a description resolves as a link to that node. `src: Core features rule 15`
- [ ] `C-CF-62` `capability` A mention of an option property inside an interface description resolves as a link into the option reference at the same version. `src: Core features rule 15`
- [ ] `C-CF-63` `constraint` Every interface cross-reference resolves to a generated link rather than a typed one. `src: Core features rule 15`
- [ ] `C-CF-64` `ui` Each gallery card draws the example's real configuration against its real data rather than a picture. `src: Core features feature 3 preamble`
- [ ] `C-CF-65` `ui` Clicking anywhere on a gallery card opens that example in the editor with the same configuration loaded. `src: Core features rule 16`
- [ ] `C-CF-66` `capability` The gallery search matches an example's title. `src: Core features rule 17`
- [ ] `C-CF-67` `capability` The gallery search matches the set of property paths the example uses. `src: Core features rule 17`
- [ ] `C-CF-68` `literal` A gallery search over `uses` for `xAxis.axisLabel.rotate` returns only `stacked-bar-margin`. `src: Core features rule 17`
- [ ] `C-CF-69` `capability` A gallery filter narrows the corpus to examples whose data is a separate file. `src: Core features rule 17`
- [ ] `C-CF-70` `literal` The gallery tag row narrows the corpus by `animation`, `interaction`, `large data`, `accessibility`, `dark`. `src: Core features rule 17`
- [ ] `C-CF-71` `capability` The `uses` set is recorded by running the example, so a gallery search over `uses` returns the matching example. `src: Core features rule 18`
- [ ] `C-CF-72` `constraint` A gallery search over `uses` still returns the matching example whose property path was set inside a loop, because `uses` is never read off the source text. `src: Core features rule 18`
- [ ] `C-CF-73` `ui` The category rail names a family beside the slug a developer types, `Line` beside `line`, `GEO/Map` beside `map`. `src: Core features rule 19`
- [ ] `C-CF-74` `ui` The active category rail row is the only row wearing the accent. `src: Core features rule 19`
- [ ] `C-CF-75` `capability` A dark chart ground, a decal pattern per series, plus the renderer choice form one preference set shared by the reference, the gallery, the editor. `src: Core features rule 20`
- [ ] `C-CF-76` `capability` Setting the preference set in the gallery changes the reference plus the editor. `src: Core features rule 20`
- [ ] `C-CF-77` `constraint` The one preference set shared by the reference, the gallery, the editor survives a reload plus a move to another route. `src: Core features rule 20`
- [ ] `C-CF-78` `ui` The editor's left pane offers `Edit Code`, the option object alone. `src: Core features rule 21`
- [ ] `C-CF-79` `ui` The editor's left pane offers `Full Code`, the option object wrapped in everything needed to run standalone. `src: Core features rule 21`
- [ ] `C-CF-80` `ui` The editor's left pane offers `Option Preview`, the object the chart received after every expression was evaluated. `src: Core features rule 21`
- [ ] `C-CF-81` `capability` A render evaluates the code, redrawing the chart, reporting its elapsed milliseconds. `src: Core features rule 22`
- [ ] `C-CF-82` `literal` The status area reads `Chart has been generated in ` followed by the elapsed milliseconds to exactly two decimal places plus `ms`. `src: Core features rule 22`
- [ ] `C-CF-83` `capability` The status area reads the wall-clock time of the render before the elapsed milliseconds. `src: Core features rule 22`
- [ ] `C-CF-84` `capability` The status area reads the count of drawn point marks beside the elapsed milliseconds. `src: Core features rule 22`
- [ ] `C-CF-85` `ui` The editor's Run control carries a keyboard shortcut in its accessible name, beside the status area that reports the render. `src: Core features rule 22`
- [ ] `C-CF-86` `constraint` A syntax error is refused with the line marked inline in the editor, leaving the last chart on screen. `src: Core features rule 23`
- [ ] `C-CF-87` `constraint` A runtime error is refused with the message plus the line in the status area, leaving the last chart on screen. `src: Core features rule 23`
- [ ] `C-CF-88` `constraint` Neither a broken option nor a runtime error replaces the last chart with an error. `src: Core features rule 23`
- [ ] `C-CF-89` `constraint` An evaluation is stopped once 5 seconds of wall clock have passed. `src: Core features rule 24`
- [ ] `C-CF-90` `constraint` An evaluation that never ends is stopped once 256 megabytes of memory have been taken. `src: Core features rule 24`
- [ ] `C-CF-91` `literal` An evaluation stopped by the budget names `wall clock` or `memory` in the status area. `src: Core features rule 24`
- [ ] `C-CF-92` `constraint` An evaluation exceeding a budget is reported as stopped rather than as a result. `src: Core features rule 24`
- [ ] `C-CF-93` `constraint` An untrusted evaluation runs inside a framed document granted script execution alone, stopped by the same budget. `src: Core features rule 25`
- [ ] `C-CF-94` `constraint` No stored credential reaches the framed document, which has no access to the portal's storage nor to the page around the frame. `src: Core features rule 25`
- [ ] `C-CF-95` `constraint` The security headers on every response deny the framed document a form submission, a top-level navigation, a popup, a download, a spawned process. `src: Core features rule 25`
- [ ] `C-CF-96` `constraint` The content security policy riding on the framed document's response denies every network request but the library the frame needs. `src: Core features rule 25`
- [ ] `C-CF-97` `ui` The editor's chart frame is visibly contained under a label naming the content as a visitor's, which the frame's own drawing cannot cover. `src: Core features rule 25`
- [ ] `C-CF-98` `capability` Share writes the editor's current code to a snippet, returning a short address. `src: Core features rule 26`
- [ ] `C-CF-99` `constraint` A shared snippet needs no account, so an unsigned caller still receives a well-formed identifier. `src: Core features rule 26`
- [ ] `C-CF-100` `literal` A shared snippet identifier is 26 characters drawn from the lowercase letters plus the digits `2` to `7`, at the address `/s/<id>`. `src: Core features rule 26`
- [ ] `C-CF-101` `constraint` A snippet identifier carries at least 128 bits of entropy, so the identifier is unguessable rather than a counter. `src: Core features rule 26`
- [ ] `C-CF-102` `constraint` A snippet identifier is never derived from the snippet's own content. `src: Core features rule 26`
- [ ] `C-CF-103` `capability` Opening a snippet address loads the editor with that snippet's code, language, library version plus the preferences saved with the snippet. `src: Core features rule 26`
- [ ] `C-CF-104` `constraint` A snippet saved without an account is unlisted, immutable once the editing window has closed. `src: Core features rule 27`
- [ ] `C-CF-105` `capability` A snippet saved by a signed-in contributor is listed in the owner's own snippet list. `src: Core features rule 27`
- [ ] `C-CF-106` `capability` An edit to an owned snippet bumps the `revision`. `src: Core features rule 27`
- [ ] `C-CF-107` `constraint` A snippet edit by anyone but the owner is refused, leaving the revision alone. `src: Core features rule 27`
- [ ] `C-CF-108` `constraint` Deletion of a withdrawn snippet is immediate in the serving path, so the address answers gone at once. `src: Core features rule 28`
- [ ] `C-CF-109` `literal` The withdrawn snippet `d4pv2sx6mhk3zrqt7nwy5bgj2f` answers gone, which differs from the answer for an unknown address. `src: Core features rule 28`
- [ ] `C-CF-110` `capability` A snippet address served to a crawler declares a preview image generated from the snippet's own chart. `src: Core features rule 29`
- [ ] `C-CF-111` `capability` Every public route declares a description, so a snippet address served to a crawler declares one generated from the snippet's own chart. `src: Core features rule 29`
- [ ] `C-CF-112` `constraint` A snippet's preview image is rendered once, held against the snippet's `revision`, rather than drawn again for every request. `src: Core features rule 29`
- [ ] `C-CF-113` `constraint` A snippet saved without an account, never opened by anyone but its creator, is gone from the serving path after 90 days. `src: Core features rule 29`
- [ ] `C-CF-114` `constraint` An owned snippet is gone from the serving path once withdrawn, which is when retention ends. `src: Core features rule 29`
- [ ] `C-CF-115` `ui` The theme panel leads with a Functions block holding `Download`, `Import`, `Export`, `Refresh`, `Reset`, `Help`, `Source Code`. `src: Core features rule 30`
- [ ] `C-CF-116` `ui` The theme panel shows a read-only `Name` row defaulting to `Customised`. `src: Core features rule 30`
- [ ] `C-CF-117` `ui` The theme panel shows a read-only `Series` row defaulting to `3`. `src: Core features rule 30`
- [ ] `C-CF-118` `ui` The theme tile grid shows five colour chips per tile against that theme's own ground, with the selected tile outlined. `src: Core features rule 30`
- [ ] `C-CF-119` `ui` The theme designer's accordion carries the setting groups `Basic Configuration`, `Visual Map`, `Grid (Cartesian)`, `Axes`, `Legend` below the tile grid. `src: Core features rule 30`
- [ ] `C-CF-120` `ui` Choosing a theme tile loads that theme into every control below, redrawing every preview. `src: Core features rule 31`
- [ ] `C-CF-121` `capability` Changing any theme control redraws every preview, coalesced to one redraw per animation frame. `src: Core features rule 31`
- [ ] `C-CF-122` `constraint` A theme redraw recolours the existing charts rather than tearing the charts down to build again. `src: Core features rule 31`
- [ ] `C-CF-123` `constraint` Dragging a colour control queues no full redraw per pointer move. `src: Core features rule 31`
- [ ] `C-CF-124` `ui` `Refresh` redraws every preview over new random data, so a theme is judged against more than one dataset. `src: Core features rule 32`
- [ ] `C-CF-125` `ui` `Reset` returns every control to the selected tile after a confirmation. `src: Core features rule 32`
- [ ] `C-CF-126` `constraint` The theme accordion's open sections survive a reload. `src: Core features rule 32`
- [ ] `C-CF-127` `constraint` The theme work in progress survives a reload. `src: Core features rule 32`
- [ ] `C-CF-128` `constraint` `Import` refuses a document that is not a theme. `src: Core features rule 33`
- [ ] `C-CF-129` `constraint` A theme import refuses a value that is a function. `src: Core features rule 33`
- [ ] `C-CF-130` `constraint` A theme import refuses a colour value that does not parse as a colour. `src: Core features rule 33`
- [ ] `C-CF-131` `constraint` A theme import refuses a number value that is not finite. `src: Core features rule 33`
- [ ] `C-CF-132` `constraint` A theme import refuses a key outside the theme schema. `src: Core features rule 33`
- [ ] `C-CF-133` `constraint` A theme import refuses a string the app would evaluate. `src: Core features rule 33`
- [ ] `C-CF-134` `constraint` A theme import refuses a reference to anything outside the document. `src: Core features rule 33`
- [ ] `C-CF-135` `constraint` A theme import refuses a document past the size limit or the nesting limit. `src: Core features rule 33`
- [ ] `C-CF-136` `constraint` A refused theme import names the offending key, changing no control. `src: Core features rule 33`
- [ ] `C-CF-137` `capability` Every registered theme carries a contrast report of each series colour against that theme's own ground. `src: Core features rule 34`
- [ ] `C-CF-138` `capability` A theme's contrast report carries the smallest perceptual distance between any pair of series colours. `src: Core features rule 34`
- [ ] `C-CF-139` `capability` A theme's contrast report recomputes both figures under each of the three common forms of colour vision deficiency. `src: Core features rule 34`
- [ ] `C-CF-140` `literal` The theme `sandstone` fails its contrast report, staying listed with the colliding pairs named. `src: Core features rule 34`
- [ ] `C-CF-141` `constraint` A theme failing the contrast report is labelled rather than removed. `src: Core features rule 34`
- [ ] `C-CF-142` `capability` A bundle selection is a seed for a closure rather than a list. `src: Core features rule 35`
- [ ] `C-CF-143` `literal` Selecting `chart/bar` resolves the closure `chartic/core`, `chart/bar`, `coord/cartesian`, `component/axis`, `scale/interval`, `util/format`. `src: Core features rule 35`
- [ ] `C-CF-144` `capability` The bundle interface shows the resolved closure, naming what pulled each member in, rather than the selection alone. `src: Core features rule 35`
- [ ] `C-CF-145` `capability` The estimated total names the raw size summed from the closure, the minified size plus the compressed size. `src: Core features rule 35`
- [ ] `C-CF-146` `literal` The estimated total for the `chart/bar` closure sums the raw bytes to `242400`. `src: Core features rule 35`
- [ ] `C-CF-147` `constraint` A selection naming a module outside the published module graph is refused before any compilation begins. `src: Core features rule 36`
- [ ] `C-CF-148` `constraint` A refused bundle selection names the unknown module. `src: Core features rule 36`
- [ ] `C-CF-149` `constraint` A selection is refused before any build where the requester supplies source, a configuration file, a plugin or a path rather than choosing an offered module. `src: Core features rule 36`
- [ ] `C-CF-150` `ui` A bundle build is queued rather than answered inline, with the interface showing the queue position then the progress. `src: Core features rule 37`
- [ ] `C-CF-151` `constraint` A bundle build exceeding its budget returns a failed status rather than a ready one carrying an integrity hash, a manifest, an install snippet or a recipe. `src: Core features rule 37`
- [ ] `C-CF-152` `constraint` The same bundle request produces a byte-identical artifact. `src: Core features rule 38`
- [ ] `C-CF-153` `capability` A bundle artifact is addressed by the digest of its own bytes. `src: Core features rule 38`
- [ ] `C-CF-154` `constraint` A second identical bundle request is answered from what was already built, sharing one artifact digest. `src: Core features rule 38`
- [ ] `C-CF-155` `capability` A ready bundle returns the bundle file for each requested format. `src: Core features rule 38`
- [ ] `C-CF-156` `capability` A ready bundle returns an integrity hash per file in the form a page can use. `src: Core features rule 38`
- [ ] `C-CF-157` `capability` A ready bundle returns a manifest naming the resolved closure plus the sizes before, after minification, after compression. `src: Core features rule 38`
- [ ] `C-CF-158` `capability` A ready bundle returns an install snippet with the integrity hash already filled in. `src: Core features rule 38`
- [ ] `C-CF-159` `capability` A ready bundle returns the exact command that reproduces the artifact locally. `src: Core features rule 38`
- [ ] `C-CF-160` `constraint` A published release record refuses every edit, so a correction is a new release. `src: Core features rule 39`
- [ ] `C-CF-161` `constraint` An attempt to change a published release leaves the stored record unchanged. `src: Core features rule 39`
- [ ] `C-CF-162` `capability` The download table lists the version per release. `src: Core features rule 40`
- [ ] `C-CF-163` `literal` The download table formats a release date year, month then day separated by slashes, so `5.4.3` reads `2026/02/18`. `src: Core features rule 40`
- [ ] `C-CF-164` `ui` The download table carries a link to the source archive beside a link to the signature. `src: Core features rule 40`
- [ ] `C-CF-165` `ui` The download table carries a link to the built artifacts. `src: Core features rule 40`
- [ ] `C-CF-166` `ui` A link to the archive of previous versions sits under the download table. `src: Core features rule 40`
- [ ] `C-CF-167` `constraint` The download table states only a hash the portal computed from the artifact the portal published. `src: Core features rule 41`
- [ ] `C-CF-168` `constraint` A mirror whose recorded hash differs from the record is dropped from the download table rather than flagged. `src: Core features rule 41`
- [ ] `C-CF-169` `constraint` A mirror serving an older release is marked stale in the download table. `src: Core features rule 41`
- [ ] `C-CF-170` `capability` The download table shows when each mirror was last verified. `src: Core features rule 41`
- [ ] `C-CF-171` `literal` A changelog entry carries a kind in square brackets, an area in square brackets, a sentence, its reference, its credit in parentheses. `src: Core features rule 42`
- [ ] `C-CF-172` `constraint` The changelog version rail carries the complete release history rather than a window on the history. `src: Core features rule 42`
- [ ] `C-CF-173` `ui` A new example is proposed as a row added inline at the top of the contributor's own list, edited in place rather than on a separate page. `src: Core features feature 9 preamble`
- [ ] `C-CF-174` `ui` A proposed row appears the moment the row is added, under a message confirming the save. `src: Core features feature 9 preamble`
- [ ] `C-CF-175` `ui` A proposed row reverts when the save is refused. `src: Core features feature 9 preamble`
- [ ] `C-CF-176` `literal` A proposed thumbnail is stored under the key scheme `thumbnails/{example_id}/{sha256_of_bytes}.svg`. `src: Core features rule 43`
- [ ] `C-CF-177` `literal` The proposed example `bump-chart-lines` keeps its thumbnail object at `thumbnails/bump-chart-lines/a319ed61bc2c850dc1f06b05a0f22ca22876df0af2aeb72ca80283276a58a176.svg`. `src: Core features rule 43`
- [ ] `C-CF-178` `capability` A proposed thumbnail stream at `GET /api/examples/<id>/thumbnail` serves the stored bytes to the owning contributor alone. `src: Core features rule 43`
- [ ] `C-CF-179` `constraint` The proposed thumbnail stream is forbidden to `contributor2@example.com`. `src: Core features rule 43`
- [ ] `C-CF-180` `constraint` The proposed thumbnail stream is forbidden to `reader@example.com`. `src: Core features rule 43`
- [ ] `C-CF-181` `constraint` The proposed thumbnail stream is forbidden to a caller carrying no token. `src: Core features rule 43`
- [ ] `C-CF-182` `constraint` A proposed thumbnail object is reachable by no unauthenticated address of any kind. `src: Core features rule 43`
- [ ] `C-CF-183` `constraint` A proposed example is absent from the gallery listing. `src: Core features rule 43`
- [ ] `C-CF-184` `constraint` A proposed example is absent from the gallery search. `src: Core features rule 43`
- [ ] `C-CF-185` `constraint` A proposed example is absent from the public example listing. `src: Core features rule 43`
- [ ] `C-CF-186` `capability` Once published, the same thumbnail stream answers for everybody. `src: Core features rule 43`
- [ ] `C-CF-187` `constraint` Publish is refused until the example's named validation checks pass. `src: Core features rule 44`
- [ ] `C-CF-188` `constraint` A validation check requires the example to run without error. `src: Core features rule 44`
- [ ] `C-CF-189` `constraint` A validation check requires the example to produce at least one series. `src: Core features rule 44`
- [ ] `C-CF-190` `constraint` A validation check requires the declared category to match the series the example creates. `src: Core features rule 44`
- [ ] `C-CF-191` `constraint` A validation check requires the example to render the same under both renderers within the stated tolerance unless one renderer is declared. `src: Core features rule 44`
- [ ] `C-CF-192` `constraint` A refused publish names the failing validation check, leaving the example proposed. `src: Core features rule 44`
- [ ] `C-CF-193` `constraint` Another contributor reading the example of an owner is answered as though the example is absent. `src: Core features rule 45`
- [ ] `C-CF-194` `constraint` Another contributor editing the example of an owner is answered as though the example is absent. `src: Core features rule 45`
- [ ] `C-CF-195` `constraint` A publish by anyone but the owner is refused before the named validation checks are reached. `src: Core features rule 45`
- [ ] `C-CF-196` `constraint` A withdrawal by anyone but the owner leaves the published example row in place. `src: Core features rule 45`
- [ ] `C-CF-197` `constraint` A request from another contributor is answered as though the example is absent, so the list of who is working on what never leaks. `src: Core features rule 45`
- [ ] `C-CF-198` `constraint` Publishing is always an explicit act by the owning contributor, never a consequence of a validation run. `src: Core features rule 46`
- [ ] `C-CF-199` `constraint` Two simultaneous publishes of one example leave one published example row. `src: Core features rule 46; Data model invariants`
- [ ] `C-CF-200` `constraint` Two simultaneous publishes of one example leave no second thumbnail object. `src: Core features rule 46; Data model invariants`
- [ ] `C-CF-201` `capability` An unknown address renders the portal's own not-found page, answering not-found. `src: Core features rule 47`
- [ ] `C-CF-202` `ui` The not-found page quotes the address that was asked for above a way back to the reference. `src: Core features rule 47`
- [ ] `C-CF-203` `capability` The not-found page names the version that removed a path, plus the path that replaced the removed one, where the last segment matches an earlier version's property. `src: Core features rule 47`
- [ ] `C-CF-204` `capability` The privacy page at `/privacy` is linked from the footer of every page, stating what is collected. `src: Core features rule 48`
- [ ] `C-CF-205` `capability` The privacy page states what is collected about a visitor plus for how long. `src: Core features rule 48`
- [ ] `C-CF-206` `literal` What is collected is a search's query text plus the rank of the result opened, carrying no identifier of any kind, no stitched session, no address. `src: Core features rule 48`
- [ ] `C-CF-207` `constraint` An individual record of what is collected is discarded within 24 hours, leaving the aggregation alone. `src: Core features rule 48`
- [ ] `C-CF-208` `constraint` No third party receives any of what is collected. `src: Core features rule 48`
- [ ] `C-CF-209` `literal` Every form carries an unattended decoy field named `website_url` a person never fills. `src: Core features rule 49`
- [ ] `C-CF-210` `constraint` A submission arriving with the decoy field filled is refused, writing nothing. `src: Core features rule 49`
- [ ] `C-CF-211` `constraint` A visitor submitting the same form repeatedly, more than 10 times inside 60 seconds, is refused for the rest of the window under a message to wait. `src: Core features rule 49`

## C-UF User flow

- [ ] `C-UF-01` `contract` `/` is a public route whose front door declares its own title plus description. `src: User flow route table`
- [ ] `C-UF-02` `contract` `/login` is a public route whose sign-in page declares its own title plus description. `src: User flow route table`
- [ ] `C-UF-03` `contract` `/signup` serves the contributor signup page publicly. `src: User flow route table`
- [ ] `C-UF-04` `contract` `/option` is a public route whose option reference declares its own title plus description. `src: User flow route table`
- [ ] `C-UF-05` `contract` `/option/<version>` serves an older version's reference, omitting a later property from its tree. `src: User flow route table`
- [ ] `C-UF-06` `contract` `/api-reference` serves the interface reference publicly. `src: User flow route table`
- [ ] `C-UF-07` `contract` `/gallery` narrows the corpus by the tag filter plus the external data filter. `src: User flow route table`
- [ ] `C-UF-08` `contract` `/editor` is a public route whose editor declares its own title plus description. `src: User flow route table`
- [ ] `C-UF-09` `contract` `/s/<id>` answers with a snippet, gone where the snippet was withdrawn, absent where unknown. `src: User flow route table`
- [ ] `C-UF-10` `contract` `/theme` is a public route whose theme designer declares its own title plus description. `src: User flow route table`
- [ ] `C-UF-11` `contract` `/themes` serves the theme registry with each theme's contrast report publicly. `src: User flow route table`
- [ ] `C-UF-12` `contract` `/releases` serves the release archive, the download table plus the changelog publicly. `src: User flow route table`
- [ ] `C-UF-13` `contract` `/bundle` resolves a bundle selection into a closure naming what pulled each member in. `src: User flow route table`
- [ ] `C-UF-14` `contract` `/my/examples` serves a contributor's own examples to a contributor session alone. `src: User flow route table`
- [ ] `C-UF-15` `contract` `/privacy` serves what is collected about a visitor publicly. `src: User flow route table`
- [ ] `C-UF-16` `contract` `/sitemap.xml` serves every public route as a sitemap. `src: User flow route table`
- [ ] `C-UF-17` `contract` `/robots.txt` serves the crawler file, pointing at the sitemap. `src: User flow route table`
- [ ] `C-UF-18` `ui` Every route sits behind one fixed sidebar that never scrolls away. `src: User flow, sidebar para`
- [ ] `C-UF-19` `ui` The sidebar groups Option reference, Interface reference plus Gallery under `Reference`. `src: User flow, sidebar para`
- [ ] `C-UF-20` `ui` The sidebar groups Editor, Theme designer plus Bundle builder under `Tools`. `src: User flow, sidebar para`
- [ ] `C-UF-21` `ui` The sidebar groups Releases plus Privacy under `Project`. `src: User flow, sidebar para`
- [ ] `C-UF-22` `ui` The signed-in contributor's own list is the sidebar's last item. `src: User flow, sidebar para`
- [ ] `C-UF-23` `capability` An unauthenticated caller reaching the contributor endpoint at `/my/examples` cannot write a row, landing on `/login` in the browser. `src: User flow, Entry and redirects`
- [ ] `C-UF-24` `capability` A login with no destination in mind lands on `/option`, refusing neither the password nor the email. `src: User flow, Entry and redirects`
- [ ] `C-UF-25` `capability` Signing out returns to `/`, so a later call with the retired token is refused as unauthenticated. `src: User flow, Entry and redirects`
- [ ] `C-UF-26` `constraint` An expired token is refused like a missing one, leaving the row as the row was under a message that the session ended. `src: User flow, Entry and redirects`
- [ ] `C-UF-27` `constraint` A reader opening the contributor endpoint cannot write, seeing an empty list rather than another account's row. `src: User flow, Entry and redirects`
- [ ] `C-UF-28` `literal` `/option/9.9.9`, a version the portal never published, renders the not-found page. `src: User flow, Entry and redirects`
- [ ] `C-UF-29` `ui` Turning on DARK MODE, the Decal Pattern toggle plus the SVG renderer choice in the gallery leaves all three already set in the option example strip, in the editor chart frame, plus after a reload. `src: User flow, journeys; Core features rule 20`
- [ ] `C-UF-30` `ui` Creating an account from the signup form, then submitting the same email again, reads the refusal naming the email field. `src: User flow, route table; Core features rule 3`
- [ ] `C-UF-31` `ui` The footer link to the privacy statement reads the same collected-data statement from three different routes. `src: User flow, route table; Core features rule 48`
- [ ] `C-UF-32` `ui` Choosing `5.2.1` in the version selector reads the reference for that release, where the pinned Preview tab reads the example for the current property. `src: User flow, journey 8; Front-end specification, the option reference`
- [ ] `C-UF-33` `ui` Pressing the Render button offers the other renderer, where returning to `5.4.3` lands at the top of the new document. `src: User flow, journey 8; Front-end specification, the documentation shell`
- [ ] `C-UF-34` `ui` The sign-in card carries the Email plus Password fields with no password reset link, showing `Sign in failed` above the action for a wrong password. `src: User flow, journeys; Core features rule 1`
- [ ] `C-UF-35` `ui` Opening the withdrawn snippet address reads that the snippet is gone rather than missing, where the live address loads the editor with that snippet's code. `src: User flow, journeys; Core features rule 28`
- [ ] `C-UF-36` `ui` Ticking a module that is not in the graph on the bundle route reads the refusal naming the module, where ticking `chart/bar` grows the closure. `src: User flow, journey 5; Core features rule 36`
- [ ] `C-UF-37` `ui` Journey one walks the option landing state at `title` into the aside search, into the selected row, then into the editor. `src: User flow, journey 1`
- [ ] `C-UF-38` `ui` Journey two finds `Stacked Bar with Margins` by the property path used, then narrows by the `large data` tag, then by the external data filter. `src: User flow, journey 2`
- [ ] `C-UF-39` `ui` Journey three reads the evaluated object, runs a changed chart, then opens the shared address in a second browser. `src: User flow, journey 3`
- [ ] `C-UF-40` `ui` Journey four presses Run over a missing closing brace, then over a loop that never ends. `src: User flow, journey 4`
- [ ] `C-UF-41` `ui` Journey five ticks `chart/bar`, reads the grown closure, requests the build, then copies the install snippet. `src: User flow, journey 5`
- [ ] `C-UF-42` `ui` Journey six proposes a row inline, reads the refusal naming the category check, then finds the published card in the gallery. `src: User flow, journey 6`
- [ ] `C-UF-43` `ui` Journey seven signs in as the other contributor to find `bump-chart-lines` unlisted, then asks for the example directly. `src: User flow, journey 7`
- [ ] `C-UF-44` `ui` Journey eight opens `/option/5.3.0` to find `legend.selectorLabel` unmatched, then reads the removed property page. `src: User flow, journey 8`
- [ ] `C-UF-45` `ui` Journey nine reads the download table row for `5.4.3`, the mirror rows, then the changelog entries in the version rail. `src: User flow, journey 9`
- [ ] `C-UF-46` `ui` Journey ten reads `Sandstone`'s contrast report, chooses the `Dark Slate` tile, presses Refresh, then takes the document away. `src: User flow, journey 10`
- [ ] `C-UF-47` `literal` The contributor's own list with nothing in the list reads `No examples yet` above `Propose your first example`. `src: User flow, States`
- [ ] `C-UF-48` `literal` The gallery filtered to nothing reads `No examples match` above `Clear filters`. `src: User flow, States`
- [ ] `C-UF-49` `literal` The aside search with no match reads `No property matches`. `src: User flow, States`
- [ ] `C-UF-50` `ui` Every page holds a loading state occupying the exact space the content will occupy, so nothing moves when the content arrives. `src: User flow, States`
- [ ] `C-UF-51` `ui` A gallery card holds its chart's height from the first paint. `src: User flow, States`
- [ ] `C-UF-52` `ui` Every error is shown in place with what failed plus what to do next, never as a stack trace nor an empty screen. `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The portal reads quiet, with the words as the subject, so the only saturated colour on screen is a chart. `src: UI/UX notes, north star`
- [ ] `C-UX-02` `ui` The portal carries no oversized hero, no editorial composition, no atmosphere layered over the content. `src: UI/UX notes, register`
- [ ] `C-UX-03` `ui` A fixed aside on the left carries the navigation on every route. `src: UI/UX notes, layout archetype`
- [ ] `C-UX-04` `ui` The property tree scrolls inside the reference aside independently of the document beside the tree. `src: UI/UX notes, layout archetype`
- [ ] `C-UX-05` `ui` The editor plus the theme designer each put two panes side by side, scrolling each pane on its own. `src: UI/UX notes, layout archetype`
- [ ] `C-UX-06` `ui` Tree rows plus property headings sit tight, so a reader sees a whole branch at once. `src: UI/UX notes, density`
- [ ] `C-UX-07` `ui` Sections read as separate because of the room around them, so a hairline appears only under a heading or between list items. `src: UI/UX notes, density`
- [ ] `C-UX-08` `ui` The gallery card sits on a near-white neutral page ground covering almost the whole page. `src: UI/UX notes, palette`
- [ ] `C-UX-09` `ui` A document route adds one cool neutral band at the top plus one deep cool neutral strip at the foot, neither of which carries a gradient. `src: UI/UX notes, palette`
- [ ] `C-UX-10` `ui` A property block's body text is a deep neutral, its supporting text a mid cool neutral used almost twice as often. `src: UI/UX notes, palette`
- [ ] `C-UX-11` `ui` The brand accent is a light, vivid red wearing the brand mark, the active sidebar row plus the route loading bar alone. `src: UI/UX notes, palette`
- [ ] `C-UX-12` `ui` Inside a generated reference document the accent is a mid, soft red carrying the page title, the selected tree row plus a property name. `src: UI/UX notes, palette`
- [ ] `C-UX-13` `ui` A property's parent path drops to a light, muted red so the eye lands on the leaf. `src: UI/UX notes, palette`
- [ ] `C-UX-14` `ui` A link inside body copy is a mid, soft cyan. `src: UI/UX notes, palette`
- [ ] `C-UX-15` `ui` A link inside the front door's own sections is a light, soft blue. `src: UI/UX notes, palette`
- [ ] `C-UX-16` `ui` The control that starts a new example is a light, vivid blue worn by nothing else on the contributor's own list. `src: UI/UX notes, palette`
- [ ] `C-UX-17` `ui` A secondary control beside the row a contributor edits in place is a mid cool neutral. `src: UI/UX notes, palette`
- [ ] `C-UX-18` `ui` A selected control in the row a contributor edits is a light, vivid blue, accepted input a mid, soft green, a recoverable problem a light, vivid orange, a refused save a light, soft red. `src: UI/UX notes, palette`
- [ ] `C-UX-19` `ui` Every one of the four control states carries a word beside the colour, so meaning never rides on colour alone. `src: UI/UX notes, palette`
- [ ] `C-UX-20` `literal` The default theme's registered series colours run light vivid blue, mid vivid lime, mid cool neutral, light vivid orange, mid vivid cyan, mid vivid amber, light vivid red, mid soft indigo. `src: UI/UX notes, palette`
- [ ] `C-UX-21` `constraint` The first series palette entry is the primary action colour, the third the secondary action colour, a relationship a substitute palette keeps. `src: UI/UX notes, palette`
- [ ] `C-UX-22` `constraint` Outside a reference document the rendered font stack is `"Open Sans", "PingFang SC", Helvetica, Arial, sans-serif`, loaded at 400 plus 800. `src: UI/UX notes, type`
- [ ] `C-UX-23` `literal` A generated reference document uses the system stack, loading nothing. `src: UI/UX notes, type`
- [ ] `C-UX-24` `constraint` A rendered code span sits outside the system font stack, in `"Source Code Pro", monospace`. `src: UI/UX notes, type`
- [ ] `C-UX-25` `constraint` The second family in the rendered system font stack is a locale fallback, preserved rather than dropped. `src: UI/UX notes, type`
- [ ] `C-UX-26` `ui` Figures align wherever amounts stack. `src: UI/UX notes, type`
- [ ] `C-UX-27` `ui` A navigation panel is square where the panel meets the sidebar, rounded where the panel leaves the sidebar. `src: UI/UX notes, shape`
- [ ] `C-UX-28` `ui` Shadow is an even halo with no vertical offset, so nothing carries a shadow falling down to the right. `src: UI/UX notes, shape and depth`
- [ ] `C-UX-29` `ui` No gradient appears in the chrome nor in the content, leaving the colour picker's tracks plus the loading skeleton's sweep. `src: UI/UX notes, shape and depth`
- [ ] `C-UX-30` `ui` One signature ease-out carries anything that arrives, opens, expands or slides in. `src: UI/UX notes, motion`
- [ ] `C-UX-31` `ui` One symmetric in-out carries a change in place on the front door, so a third curve never arrives. `src: UI/UX notes, motion`
- [ ] `C-UX-32` `ui` A selection colour, a control ground plus a tree row all settle rather than snap on arrival. `src: UI/UX notes, motion`
- [ ] `C-UX-33` `constraint` Nothing on the front door scrubs to the scroll position, so a revealed element stays revealed. `src: UI/UX notes, motion`
- [ ] `C-UX-34` `ui` On the front door the reveal runs in a three-step stagger inside a group, the heading, then the mark beside the heading, then the paragraph under the mark. `src: UI/UX notes, motion`
- [ ] `C-UX-35` `ui` An element already in the window on arrival reveals immediately in the same stagger. `src: UI/UX notes, motion`
- [ ] `C-UX-36` `constraint` An element that has revealed never un-reveals on scrolling back. `src: UI/UX notes, motion`
- [ ] `C-UX-37` `ui` The front door mark's eight wedges unfold one after another, replayable from the control at the mark's centre. `src: UI/UX notes, motion`
- [ ] `C-UX-38` `constraint` A narrow viewport shows no sideways overflow from a blanket transition, so the properties that move are named. `src: UI/UX notes, motion`
- [ ] `C-UX-39` `ui` Under a reduced-motion preference the reveal does not animate, leaving every element present at full strength on arrival. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-40` `ui` Under a reduced-motion preference the mark does not play on arrival, leaving the play control available. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-41` `ui` Under a reduced-motion preference the pulse on the play control does not run. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-42` `ui` Under a reduced-motion preference the route loading bar keeps animating, because the bar carries information. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-43` `ui` Under a reduced-motion preference every transition collapses to a non-zero minimum rather than to nothing. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-44` `ui` A gallery card has a resting, a pointed-at, a pressed, a focused plus an unavailable border state. `src: UI/UX notes, components`
- [ ] `C-UX-45` `constraint` An unavailable decal control is announced rather than signalled by colour alone. `src: UI/UX notes, components`
- [ ] `C-UX-46` `ui` Escape closes a sidebar navigation panel, returning focus to the row that opened the panel. `src: UI/UX notes, components`
- [ ] `C-UX-47` `ui` Reset on the theme designer confirms first, naming the tile every control returns to. `src: UI/UX notes, components`
- [ ] `C-UX-48` `ui` A gallery card lifts its border to the link tone, gaining the halo when pointed at. `src: UI/UX notes, components`
- [ ] `C-UX-49` `ui` A toggle shows its label beside the track, exposing its state rather than implying the state. `src: UI/UX notes, components`
- [ ] `C-UX-50` `ui` A sidebar destination that leaves the portal is marked as leaving, rather than dressed to look like a neighbouring row. `src: UI/UX notes, components`
- [ ] `C-UX-51` `ui` A save, a publish, a copy plus a withdraw each raise a short message naming what happened, clearing itself afterwards. `src: UI/UX notes, feedback`
- [ ] `C-UX-52` `ui` The row a message belongs to shows the new value at once, reverting under that message when the save is refused. `src: UI/UX notes, feedback`
- [ ] `C-UX-53` `constraint` Body text plus its background meet WCAG AA contrast. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-54` `constraint` The quiet supporting tone meets WCAG AA contrast against its background. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-55` `constraint` The dimmed inactive row in a topic list meets WCAG AA contrast against its background. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-56` `ui` A visible focus indicator on the decal control holds 3 to 1 against both the control plus its surroundings. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-57` `constraint` A narrow viewport keeps every navigation target comfortably sized, showing no sideways overflow. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-58` `constraint` A narrow viewport permits zoom rather than restricting the scale, showing no sideways overflow of small base text. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-59` `ui` A skip link announced before every chart description is the first focusable element, moving focus to the main region. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-60` `ui` The property tree is a single tab stop where up plus down move between visible rows, right expands, left collapses then moves to the parent, enter selects. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-61` `ui` The search suggestion list moves with up plus down, chooses with enter, dismisses with escape, announcing how many suggestions there are. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-62` `ui` The editor's code pane, whose chart carries a generated description, can be left with escape followed by tab. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-63` `ui` Every icon-only control carries a text label. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-64` `ui` One banner region, one navigation region inside the banner, one main region per route, one content-info region for the footer plus a complementary region announced to assistive technology for the reference aside. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-65` `ui` Exactly one first-level heading per route, announced to assistive technology, with levels descending without skipping. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-66` `ui` Every embedded chart carries a text description generated from its own data, naming the chart family, the series count, each axis span, the highest value plus the lowest value with their labels. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-67` `ui` A gallery card's chart is decorative because the caption names the chart, so the chart is hidden from assistive technology. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-68` `ui` The decal control is exposed as a labelled preference with its state. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-69` `constraint` The arrangement holds from the widest viewport down to the tablet width, with one real switch at a phone width below. `src: UI/UX notes, responsive behaviour`
- [ ] `C-UX-70` `ui` At the switch the sidebar collapses to a control at the right, turning its panels into an inline list. `src: UI/UX notes, responsive behaviour`
- [ ] `C-UX-71` `ui` At the switch the reference aside becomes a full-width strip above the content carrying the tab strip, then a row holding a tree control beside the search field. `src: UI/UX notes, responsive behaviour`
- [ ] `C-UX-72` `ui` At the switch the property tree sits behind the tree control, opening as a full-height overlay that closes when a row is chosen. `src: UI/UX notes, responsive behaviour`
- [ ] `C-UX-73` `ui` At the switch a document route's topic rail moves above the content as a collapsed list. `src: UI/UX notes, responsive behaviour`
- [ ] `C-UX-74` `ui` At the switch the gallery rail becomes a horizontally scrolling strip, with the grid falling to one column. `src: UI/UX notes, responsive behaviour`
- [ ] `C-UX-75` `ui` At the switch the editor plus the theme designer stack, code above chart, controls above previews. `src: UI/UX notes, responsive behaviour`
- [ ] `C-UX-76` `constraint` The gallery's column count steps down the widths rather than flowing, so a card keeps its chart height at every count. `src: UI/UX notes, responsive behaviour`
- [ ] `C-UX-77` `constraint` Focus order follows the visual order at every width, the phone width included. `src: UI/UX notes, responsive behaviour`
- [ ] `C-UX-78` `constraint` Nothing overflows sideways at the narrowest viewport, leaving every navigation target reachable there. `src: UI/UX notes, responsive behaviour`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The front door shell puts full-width stacked sections on the ground behind the fixed sidebar. `src: Front-end specification, the five shells`
- [ ] `C-FE-02` `ui` The document shell puts a tinted page header band above a two-column body of a topic rail beside a content column. `src: Front-end specification, the five shells`
- [ ] `C-FE-03` `ui` The documentation shell puts a fixed aside holding a tab strip, a search field plus a tree beside a scrolling content pane. `src: Front-end specification, the five shells`
- [ ] `C-FE-04` `ui` The gallery shell puts a fixed category rail on the left beside a card grid filling the rest. `src: Front-end specification, the five shells`
- [ ] `C-FE-05` `ui` The application shell puts two panes divided near the half, scrolling each independently. `src: Front-end specification, the five shells`
- [ ] `C-FE-06` `ui` A shell is a server-rendered template, so the property tree rows arrive drawn rather than built by a client-side layout component. `src: Front-end specification, the five shells`
- [ ] `C-FE-07` `ui` A route loading bar sits at the very top edge, running for as long as a route is being fetched. `src: Front-end specification, Global chrome`
- [ ] `C-FE-08` `ui` The route loading bar's leading edge carries a double glow in the brand accent, the only glow in the portal. `src: Front-end specification, Global chrome`
- [ ] `C-FE-09` `ui` The brand mark is a ring with a gap in the brand accent, an arc of roughly fifty degrees removed at its upper right, a filled dot centred in the gap. `src: Front-end specification, Global chrome`
- [ ] `C-FE-10` `ui` The wordmark sits beside the brand ring, set solid plus uppercase in the interface family at 800. `src: Front-end specification, Global chrome`
- [ ] `C-FE-11` `ui` The brand link is named for the product rather than for the image inside the link. `src: Front-end specification, Global chrome`
- [ ] `C-FE-12` `ui` A sidebar group heading is a quiet caption above its destination rows. `src: Front-end specification, Global chrome`
- [ ] `C-FE-13` `ui` A sidebar destination row takes the surface-hover tone when pointed at. `src: Front-end specification, Global chrome`
- [ ] `C-FE-14` `ui` Five sidebar destinations open a panel listing their own sub-destinations. `src: Front-end specification, Global chrome`
- [ ] `C-FE-15` `ui` A navigation panel opens on focus rather than on hover alone. `src: Front-end specification, Global chrome`
- [ ] `C-FE-16` `ui` A navigation panel changes its ground plus its halo when opening, rather than transforming. `src: Front-end specification, Global chrome`
- [ ] `C-FE-17` `ui` On the panel matching the current route, pointing at the panel lightens the label plus both pseudo-elements, leaving the top rule unlightened. `src: Front-end specification, Global chrome`
- [ ] `C-FE-18` `ui` A foundation banner naming the software foundation that holds the trademark sits below the sidebar destinations. `src: Front-end specification, Global chrome`
- [ ] `C-FE-19` `ui` The footer sits on the one deep cool neutral surface in the portal, carrying the licence line. `src: Front-end specification, Global chrome`
- [ ] `C-FE-20` `ui` The footer carries a row of icon targets each of which carries a text name. `src: Front-end specification, Global chrome`
- [ ] `C-FE-21` `ui` The trademark mark is set as a superscript beside the product name. `src: Front-end specification, Global chrome`
- [ ] `C-FE-22` `constraint` The chrome carries no global search field, no account menu for an unsigned reader, no language switch, no chrome theme switch, no announcement strip. `src: Front-end specification, Global chrome`
- [ ] `C-FE-23` `ui` A hero action is tall plus fully rounded on the primary action ground with white ink, carrying a glyph inset from its left edge in the label's colour. `src: Front-end specification, Components`
- [ ] `C-FE-24` `ui` A standard action is content height, lightly rounded, on the primary action ground with white ink. `src: Front-end specification, Components`
- [ ] `C-FE-25` `ui` A tertiary action is transparent with link-tone ink under a soft offset halo. `src: Front-end specification, Components`
- [ ] `C-FE-26` `ui` A pill pressed on a document route is fully rounded at its own height on the front-door link tone, settling its ground. `src: Front-end specification, Components`
- [ ] `C-FE-27` `ui` A control-library action pressed on a document route is short plus barely rounded on the state colours with control ink. `src: Front-end specification, Components`
- [ ] `C-FE-28` `ui` Every button variant settles its ground rather than snapping the ground. `src: Front-end specification, Components`
- [ ] `C-FE-29` `ui` A topic rail carries a caption reading `Topics` above a narrow list of rows. `src: Front-end specification, Components`
- [ ] `C-FE-30` `ui` A topic rail's active row wears the brand accent, an inactive row the body tone at reduced strength still at the contrast floor. `src: Front-end specification, Components`
- [ ] `C-FE-31` `ui` A topic rail marks a row with a bullet outside the row's text column. `src: Front-end specification, Components`
- [ ] `C-FE-32` `ui` A topic rail tracks the content column in both directions, the row matching the heading nearest the top of the window being active. `src: Front-end specification, Components`
- [ ] `C-FE-33` `ui` The page header band carries the route title at 40px over 44px at 700 in the body tone. `src: Front-end specification, Components`
- [ ] `C-FE-34` `ui` The page header band carries a subtitle at 16px over 22.8571px in a muted cool neutral. `src: Front-end specification, Components`
- [ ] `C-FE-35` `ui` The page header band carries a trademark line under the subtitle in a lighter cool neutral. `src: Front-end specification, Components`
- [ ] `C-FE-36` `ui` A subtitle running to several lines grows the band, so the trademark line follows the subtitle down. `src: Front-end specification, Components`
- [ ] `C-FE-37` `ui` Inline code is the code family at 14.4px over 22px on a very light warm ground with a deep red ink, barely rounded under a little padding. `src: Front-end specification, Components`
- [ ] `C-FE-38` `ui` A preformatted block uses the code family at 13px on a light neutral ground, a touch more rounded. `src: Front-end specification, Components`
- [ ] `C-FE-39` `ui` The reference search field is an input on the ground with control ink at 13px, rounded on its left edge alone. `src: Front-end specification, Components`
- [ ] `C-FE-40` `ui` The reference search field's appended button sits on a sunken neutral with quiet ink, rounded on its right edge alone, carrying a small magnifier glyph centred in the button. `src: Front-end specification, Components`
- [ ] `C-FE-41` `ui` The search suggestion list sits on the ground under a soft halo. `src: Front-end specification, Components`
- [ ] `C-FE-42` `ui` A tree row carries a fold triangle in a quiet control tone at its left, then the label at 13px over 17px. `src: Front-end specification, Components`
- [ ] `C-FE-43` `ui` A tree row's label is indented one level per depth, the indent applied to the label rather than to the row. `src: Front-end specification, Components`
- [ ] `C-FE-44` `ui` A selected tree row takes the document accent as its ground with white ink, an unselected row a transparent ground with body-tone ink. `src: Front-end specification, Components`
- [ ] `C-FE-45` `ui` A toolbox at the right of the tree's heading row carries one action reading `Collapse All` in the link tone. `src: Front-end specification, Components`
- [ ] `C-FE-46` `constraint` The tree renders only expanded nodes, so a collapsed branch has no rows in the page. `src: Front-end specification, Components`
- [ ] `C-FE-47` `ui` A toggle is a short fully rounded track on the control border tone when off plus the selected-control tone when on, with a round white knob travelling its length. `src: Front-end specification, Components`
- [ ] `C-FE-48` `ui` A tab strip's selected item is full height with near-black ink under a rule in the brand accent, an unselected item near-black at reduced strength. `src: Front-end specification, Components`
- [ ] `C-FE-49` `ui` A tab strip item that leaves the portal is in the link tone, carrying the outbound marker. `src: Front-end specification, Components`
- [ ] `C-FE-50` `ui` The outbound marker is decorative plus hidden from assistive technology, so that a link leaves the portal is said in the link's own name. `src: Front-end specification, Components`
- [ ] `C-FE-51` `ui` Every chrome icon is drawn geometry or a font glyph, so the brand ring, its gap plus its centred dot need no image. `src: Front-end specification, Iconography`
- [ ] `C-FE-52` `ui` The home mark is eight wedges around a centre, each wedge's corner radius plus outer radius shrinking together with the wedge. `src: Front-end specification, Iconography`
- [ ] `C-FE-53` `ui` The home mark's wedges are drawn in the eight chart series colours in their palette order, with a round play control at the centre. `src: Front-end specification, Iconography`
- [ ] `C-FE-54` `ui` The outbound marker is a small square with an arrow leaving its upper right. `src: Front-end specification, Iconography`
- [ ] `C-FE-55` `ui` The repository glyph, the play control, the front door's two action glyphs, the loading spinner, the close control plus the category rail's per-family glyphs come from one icon font at a single cut, needing no image in the chrome. `src: Front-end specification, Iconography`
- [ ] `C-FE-56` `constraint` A favicon is served plus declared in the head of every route. `src: Front-end specification, Iconography`
- [ ] `C-FE-57` `constraint` The portal supplies no binary asset beyond the compressed font format, drawing every mark, glyph, chip plus composite from geometry or that font. `src: Front-end specification, Assets`
- [ ] `C-FE-58` `constraint` The portal serves no contributor portrait, no event poster, no texture anywhere. `src: Front-end specification, Assets`
- [ ] `C-FE-59` `ui` Any image the portal renders carries alternative text, with a decorative one declaring itself decorative. `src: Front-end specification, Assets`
- [ ] `C-FE-60` `ui` The reference aside is fixed, sitting above the page on an even halo, never scrolling with the document. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-61` `literal` The reference tab strip carries four items, `Option`, `API`, `GL`, `Tutorial`. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-62` `constraint` The first three reference tabs swap both the document in the content pane plus the tree in the aside, the fourth leaving the portal. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-63` `constraint` Switching between the first three reference tabs is a route change rather than a filter, with a different tree, a different search index, a disjoint fragment space. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-64` `constraint` A reader switching reference tabs arrives at the top of the new document rather than at a preserved position. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-65` `ui` The tree scrolls independently of the aside around the tree. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-66` `ui` The content pane runs from the aside's right edge to the window's right edge, scrolling with the window, with the body copy inset from the pane's left edge. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-67` `ui` The content pane carries the document title at 34px over 46px at 400 in the document accent. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-68` `ui` The content pane carries the description as body copy in the document body tone after the title. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-69` `ui` The content pane carries an embedded example in a framed chart after the description. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-70` `literal` The content pane carries the word `Properties` at 28px over 31px in a light neutral under a hairline. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-71` `ui` A property block's heading row carries the parent path at 16px over 20px in the quiet document accent ending in a dot. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-72` `ui` A property block's heading row carries the property name at 20px over 25px in the document accent. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-73` `ui` A property block carries a bordered type pill carrying the type name. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-74` `ui` A property block carries the description at 14px in the document body tone. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-75` `ui` A property block's heading row carries a fold chevron at its right. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-76` `ui` The example strip above a property list carries a `Dark Mode` toggle, a `Decal Pattern` toggle beside that, a `Render` button carrying a settings glyph, an `Edit` link aligned right, then the framed example. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-77` `literal` A tab pinned to the right edge of the content pane, vertically centred, reads `Preview`, opening a panel showing the example for the current property. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-78` `constraint` The whole reference document is present in the page, so the browser's own find-in-page searches the entire reference. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-79` `constraint` A property block below the window in the content pane is rendered, with its embedded example unstarted until the block approaches the window. `src: Front-end specification, the documentation shell`
- [ ] `C-FE-80` `literal` The option tree's top level runs `title`, `legend`, `grid`, `xAxis`, `yAxis`, `polar`, `radiusAxis`, `angleAxis`, `radar`, `dataZoom`, `visualMap`, `tooltip`, `axisPointer`, `toolbox`, `brush`, `geo`, `parallel`, `parallelAxis`, `singleAxis`, `timeline`, `graphic`, `calendar`, `matrix`, `thumbnail`, `dataset`, `aria`, `series`, `darkMode`, `color`, `backgroundColor`, `textStyle`, `animation`, `animationThreshold`, `animationDuration`. `src: Front-end specification, the option reference`
- [ ] `C-FE-81` `constraint` The option tree runs between three plus seven levels deep depending on the branch. `src: Front-end specification, the option reference`
- [ ] `C-FE-82` `ui` At a narrow width the reference tab strip reorders its four items to `Option`, `API`, `Tutorial`, `GL`, promoting the outbound item above the three-dimensional one. `src: Front-end specification, per-route surfaces; UI/UX notes, responsive behaviour`
- [ ] `C-FE-83` `ui` A version selector sits above the reference tab strip, defaulting to the current release, listing every retained release. `src: Front-end specification, the option reference`
- [ ] `C-FE-84` `literal` The interface reference carries four top-level nodes rather than thirty-four, `chartic` the global object, `charticInstance` a chart instance, `action` the messages sent to a chart, `events` the set emitted. `src: Front-end specification, the interface reference`
- [ ] `C-FE-85` `literal` The gallery category rail lists `Line`, `Bar`, `Pie`, `Scatter`, `GEO/Map`, `Candlestick`, `Radar`, `Boxplot`, `Heatmap`, `Graph`, `Lines`, `Tree`, `Treemap`, `Sunburst`, `Parallel`, `Sankey`, `Funnel`, `Gauge`, `PictorialBar`. `src: Front-end specification, the gallery`
- [ ] `C-FE-86` `ui` A gallery rail row is a glyph in a small box followed by a label. `src: Front-end specification, the gallery`
- [ ] `C-FE-87` `ui` The gallery header row carries the category name at 26px at 400 in the body tone with the slug immediately after at 16px in the muted tone. `src: Front-end specification, the gallery`
- [ ] `C-FE-88` `ui` The gallery header row carries the search field, the tag row, the external-data filter plus a `DARK MODE` pill at its right edge under a hairline. `src: Front-end specification, the gallery`
- [ ] `C-FE-89` `constraint` A gallery chart renders as the card approaches the window, torn down once the card is more than two screens past the window. `src: Front-end specification, the gallery`
- [ ] `C-FE-90` `constraint` Scrolling the gallery fast cancels the renders queued for cards that have already left. `src: Front-end specification, the gallery`
- [ ] `C-FE-91` `ui` A gallery card that has not rendered shows the loading skeleton's sweep at the exact height its chart will occupy. `src: Front-end specification, the gallery`
- [ ] `C-FE-92` `constraint` The gallery renderer is chosen per card, the vector renderer for a small static thumbnail plus the raster renderer for a chart carrying more than a thousand marks. `src: Front-end specification, the gallery`
- [ ] `C-FE-93` `constraint` Above sixteen cards in the render window the gallery serves a pre-rendered vector still, upgrading a card to a live chart when the pointer enters or the card takes focus. `src: Front-end specification, the gallery`
- [ ] `C-FE-94` `constraint` On a device reporting reduced processing capability or a preference for saving data every gallery card serves the still rather than a chart drawn live. `src: Front-end specification, the gallery`
- [ ] `C-FE-95` `ui` The editor's left tab strip selected tab takes the link tone on the ground under a rule in the same tone, an unselected tab the body tone on a light neutral. `src: Front-end specification, the editor`
- [ ] `C-FE-96` `ui` The editor's tool row holds a language toggle of two chips, one reading `JS` on an amber ground plus one reading `TS`. `src: Front-end specification, the editor`
- [ ] `C-FE-97` `ui` The editor's tool row holds three named controls, a dependency picker, a runtime switch between the two-dimensional plus three-dimensional runtimes, a view of the generated standalone document. `src: Front-end specification, the editor`
- [ ] `C-FE-98` `ui` The editor's `Run` button sits on the link tone in white, carrying a play glyph. `src: Front-end specification, the editor`
- [ ] `C-FE-99` `ui` The editor's code pane carries line numbers in a gutter, fold markers plus syntax colouring. `src: Front-end specification, the editor`
- [ ] `C-FE-100` `ui` The editor's right toolbar holds the `Dark Mode` toggle, the `Decal Pattern` toggle plus a `Render` button. `src: Front-end specification, the editor`
- [ ] `C-FE-101` `ui` The editor's chart frame sits on the ground inside a hairline border. `src: Front-end specification, the editor`
- [ ] `C-FE-102` `ui` The editor's footer bar holds `Download`, `Screenshot` plus `Share`, with the status area aligned right carrying the render report at 13px in the muted tone. `src: Front-end specification, the editor`
- [ ] `C-FE-103` `ui` The divider between the editor's two panes is a hairline that can be dragged. `src: Front-end specification, the editor`
- [ ] `C-FE-104` `capability` `Download` gives the chart as a vector document at the size displayed with fonts converted to outlines. `src: Front-end specification, the editor`
- [ ] `C-FE-105` `capability` `Screenshot` gives the chart as a raster image at twice the display resolution on the current ground. `src: Front-end specification, the editor`
- [ ] `C-FE-106` `constraint` `Download` plus `Screenshot` are produced in the page from the live chart rather than by a round trip, leaving the snippet preview image as the one server case. `src: Front-end specification, the editor`
- [ ] `C-FE-107` `ui` The theme control panel is a fixed column on the left scrolling on its own, with the preview pane beside the panel headed `Chart Preview`. `src: Front-end specification, the theme designer`
- [ ] `C-FE-108` `ui` The theme `Functions` block is collapsible under a chevron at its right, holding its seven controls in a grid. `src: Front-end specification, the theme designer`
- [ ] `C-FE-109` `ui` The theme tile grid is two columns wide. `src: Front-end specification, the theme designer`
- [ ] `C-FE-110` `ui` A theme accordion header carries its label at the left plus a chevron at the right over a hairline divider. `src: Front-end specification, the theme designer`
- [ ] `C-FE-111` `ui` A theme accordion body holds labelled colour pickers, numeric fields, select fields plus toggles. `src: Front-end specification, the theme designer`
- [ ] `C-FE-112` `ui` The theme preview wall is two columns of cards on the ground inside a hairline border, barely rounded. `src: Front-end specification, the theme designer`
- [ ] `C-FE-113` `ui` A theme preview card carries a centred title at 20px cut 700 plus a centred subtitle at 13px in the muted tone. `src: Front-end specification, the theme designer`
- [ ] `C-FE-114` `ui` A theme preview card carries five glyph controls at its top right for restore, save, data view, zoom region, zoom reset. `src: Front-end specification, the theme designer`
- [ ] `C-FE-115` `literal` The theme preview cards run `Line Chart`, `Stacked Area Chart`, `Bar Chart`, `Stacked Bar Chart`, `Scatter Chart`, `Pie Chart`. `src: Front-end specification, the theme designer`
- [ ] `C-FE-116` `ui` The colour picker carries a hue track running the full spectrum, a saturation plus lightness square, an alpha track, a field for a typed value plus a set of recently used swatches. `src: Front-end specification, the theme designer`
- [ ] `C-FE-117` `ui` `/themes` lists the ready-made themes as a three-column grid of preview cards, each a composite of six miniature charts drawn in that theme with the name beneath plus the contrast report beside. `src: Front-end specification, the theme designer`
- [ ] `C-FE-118` `constraint` A theme composite preview is pre-rendered rather than served from a route fetching the charting library. `src: Front-end specification, the theme designer`
- [ ] `C-FE-119` `literal` The download table's columns read `Version`, `Release Date`, `Download Source from a Mirror`, `Dist files`. `src: Front-end specification, the release archive`
- [ ] `C-FE-120` `ui` Two numbered procedures sit under the download table, one for signature verification plus one for checksum verification, each naming its command with its arguments, with a note paragraph between them. `src: Front-end specification, the release archive`
- [ ] `C-FE-121` `constraint` An archive filename inside a verification procedure carries the version as a placeholder rather than as a literal. `src: Front-end specification, the release archive`
- [ ] `C-FE-122` `ui` A licence block closes the release route, naming the licence plus linking its full text. `src: Front-end specification, the release archive`
- [ ] `C-FE-123` `ui` The release route leads with a tab strip of three copyable one-line install commands, then the archive path beneath. `src: Front-end specification, the release archive`
- [ ] `C-FE-124` `literal` The release route carries the bundle builder entry point reading `build a bundle with only what you need` beside a sentence saying what the bundle saves. `src: Front-end specification, the release archive`
- [ ] `C-FE-125` `ui` The changelog's version rail carries a caption reading `Versions` above one row per release carrying the version plus its date, with the current row in the brand accent. `src: Front-end specification, the release archive`
- [ ] `C-FE-126` `ui` The changelog content carries a version heading at 26px in the document accent with the release date aligned right on the same line, then the entry bullets. `src: Front-end specification, the release archive`
- [ ] `C-FE-127` `constraint` A changelog entry's kind plus area sit in the body tone, its sentence as body copy with property names as inline code spans, its references as issue numbers prefixed with a hash plus commit identifiers linking out, its credits as handles comma separated in parentheses linking out. `src: Front-end specification, the release archive`
- [ ] `C-FE-128` `ui` The front door hero carries the brand line at 75px over 90px at 800 in the display tone. `src: Front-end specification, the front door`
- [ ] `C-FE-129` `ui` The front door hero carries the subtitle beneath the brand line at 21px over 30px in the subtitle tone. `src: Front-end specification, the front door`
- [ ] `C-FE-130` `ui` The front door hero carries two fully rounded actions under the subtitle, with the animated mark to their right at the desktop widths. `src: Front-end specification, the front door`
- [ ] `C-FE-131` `ui` At the narrow width the front door mark sits beneath the copy, overlapping nothing. `src: Front-end specification, the front door`
- [ ] `C-FE-132` `ui` A release banner on the front door names the newest release, updating with the record rather than by hand. `src: Front-end specification, the front door`
- [ ] `C-FE-133` `ui` The front door features section carries cards each with a drawn icon, a heading at 16px cut 700 plus a paragraph at 14px over 24.5px. `src: Front-end specification, the front door`
- [ ] `C-FE-134` `constraint` The front door feature cards are generated from the same source as the feature copy rather than authored twice. `src: Front-end specification, the front door`
- [ ] `C-FE-135` `ui` The front door citation section carries its headline at 25px over 36px beside a fully rounded citation action. `src: Front-end specification, the front door`
- [ ] `C-FE-136` `ui` The front door follow section's heading is 35px over 38.5px at 600, with buttons carrying the one offset shadow in the portal. `src: Front-end specification, the front door`
- [ ] `C-FE-137` `constraint` Only the compressed font format is served, subset, with two faces preloaded. `src: Front-end specification, Performance`
- [ ] `C-FE-138` `constraint` No image is served at more than twice its rendered size. `src: Front-end specification, Performance`
- [ ] `C-FE-139` `constraint` A route that renders no chart never loads the charting library. `src: Front-end specification, Performance`
- [ ] `C-FE-140` `constraint` First contentful paint stays under 1.2 seconds on a mid-range phone over a slow connection on every route. `src: Front-end specification, Performance`
- [ ] `C-FE-141` `constraint` Largest contentful paint stays under 2.5 seconds on the front door plus the document routes. `src: Front-end specification, Performance`
- [ ] `C-FE-142` `constraint` Largest contentful paint stays under 4 seconds on the two references, whose looser budget follows from shipping the whole document. `src: Front-end specification, Performance`
- [ ] `C-FE-143` `constraint` Cumulative layout shift stays under 0.05 on every route, so nothing on a card shifts as the charts arrive. `src: Front-end specification, Performance`
- [ ] `C-FE-144` `constraint` Interaction to next paint stays under 200 milliseconds, so the preview wall neither stalls nor flickers as a control changes. `src: Front-end specification, Performance`
- [ ] `C-FE-145` `constraint` The first chart is on screen within 2 seconds in the gallery plus the editor. `src: Front-end specification, Performance`
- [ ] `C-FE-146` `constraint` Expanding a tree node paints its rows within 100 milliseconds. `src: Front-end specification, Performance`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The portal is served as server-rendered pages progressively enhanced in the browser rather than as a client-side application fetching its own HTML. Declared for the one process serving every page. `src: Technical requirements, para 1`
- [ ] `C-TR-02` `literal` The backend is FastAPI with Jinja templates. Declared for the one process serving every page. `src: Technical requirements, para 1`
- [ ] `C-TR-03` `literal` The browser layer is Alpine.js over those server templates. Declared for the one process serving every page. `src: Technical requirements, para 1`
- [ ] `C-TR-04` `constraint` The first paint a browser receives is the complete document for the route, rendered on the server from the schema, the example corpus plus the release records. Declared for the one process serving every page. `src: Technical requirements, para 1`
- [ ] `C-TR-05` `constraint` A route's content is never a skeleton that JavaScript fills in from a second request. Declared for the one process serving every page. `src: Technical requirements, para 1`
- [ ] `C-TR-06` `literal` The datastore is PostgreSQL, read from `DATABASE_URL`. Declared for the one process serving every page. `src: Technical requirements, para 2`
- [ ] `C-TR-07` `literal` Object bytes live in MinIO, read from `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`. Stored under its declared key scheme. `src: Technical requirements, para 2`
- [ ] `C-TR-08` `literal` The app's own address plus port come from `APP_PUBLIC_URL` plus `APP_PUBLIC_PORT`. Declared for the one process serving every page. `src: Technical requirements, para 2`
- [ ] `C-TR-09` `constraint` No host nor port is hardcoded, every one being read from the environment. Declared for the one process serving every page. `src: Technical requirements, para 2`
- [ ] `C-TR-10` `constraint` PostgreSQL plus MinIO are already running, never downloaded, installed, compiled nor started by the app. Declared for the one process serving every page. `src: Technical requirements, para 2`
- [ ] `C-TR-11` `constraint` Only the libraries named plus their direct dependencies are used, with no second database, cache, queue, object store, identity provider nor mail vendor introduced. `src: Technical requirements, para 3`
- [ ] `C-TR-12` `constraint` No account is required to read anything, to run anything, to build anything nor to receive a well-formed shared snippet identifier. `src: Technical requirements, identity`
- [ ] `C-TR-13` `constraint` An account exists for one job, letting an owner manage the examples plus snippets the owner created. `src: Technical requirements, identity`
- [ ] `C-TR-14` `constraint` An account holds an identifier, an authentication method, a display name plus the list of things owned, with no profile, no stored preferences, no history of what was read. `src: Technical requirements, identity`
- [ ] `C-TR-15` `literal` Authentication is app-implemented email plus password with bearer tokens. `src: Technical requirements, identity`
- [ ] `C-TR-16` `constraint` Passwords are stored hashed, never in a recoverable form. `src: Technical requirements, identity`
- [ ] `C-TR-17` `constraint` Authorisation is by role plus by ownership, so a reader calling a contributor endpoint cannot write a row. `src: Technical requirements, identity`
- [ ] `C-TR-18` `constraint` Per-address rate limiting refuses a repeated submission on every write plus every evaluation, with a low burst plus a low sustained rate. `src: Technical requirements, rate limiting`
- [ ] `C-TR-19` `constraint` Reading is refused by no rate limit beyond ordinary network protection, unlike a repeated submission. `src: Technical requirements, rate limiting`
- [ ] `C-TR-20` `constraint` The evaluation surface refuses a repeated submission far more strictly than any read surface, with a signed-in caller getting a higher limit rather than no limit. `src: Technical requirements, rate limiting`
- [ ] `C-TR-21` `constraint` An evaluation stopped by a budget leaves no output persisted nor addressable afterwards, so the portal cannot be used as free hosting. `src: Technical requirements, rate limiting`
- [ ] `C-TR-22` `constraint` A caller whose repeated submission hits a budget from the same address is refused for longer. `src: Technical requirements, rate limiting`
- [ ] `C-TR-23` `capability` A report control on every snippet route, a withdrawn snippet included, sends the address to a review queue. `src: Technical requirements, rate limiting`
- [ ] `C-TR-24` `literal` `GET /api/health` returns `200` once the app is ready to serve. `src: Technical requirements, health`
- [ ] `C-TR-25` `contract` Each request is logged as one structured line carrying the method, the path, the status plus the elapsed milliseconds, to standard output. Declared for the one process serving every page. `src: Technical requirements, logging`
- [ ] `C-TR-26` `constraint` Every response carries a strict transport policy, a nosniff content-type policy, a frame policy, a referrer policy plus a content security policy. `src: Technical requirements, headers`
- [ ] `C-TR-27` `constraint` The content security policy riding on every response for the framed document that evaluates visitor code denies every network destination but the app's own origin. `src: Technical requirements, headers`
- [ ] `C-TR-28` `constraint` The security headers riding on that framed document's response deny form submission, top-level navigation plus popups. `src: Technical requirements, headers`
- [ ] `C-TR-29` `constraint` No stored credential such as a database URL appears in any document, script, stylesheet nor JSON the browser downloads. `src: Technical requirements, credentials`
- [ ] `C-TR-30` `constraint` No object store access key appears in anything the browser downloads. `src: Technical requirements, credentials`
- [ ] `C-TR-31` `constraint` No object store secret appears in anything the browser downloads. `src: Technical requirements, credentials`
- [ ] `C-TR-32` `constraint` No bearer token belonging to another account appears in anything the browser downloads. `src: Technical requirements, credentials`
- [ ] `C-TR-33` `constraint` The object store's key material stays server-side, so a caller reaches a proposed thumbnail only through the app's own stream. `src: Technical requirements, credentials`
- [ ] `C-TR-34` `literal` A favicon is served at `/favicon.ico`, declared in the document head of every route. `src: Technical requirements, favicon`
- [ ] `C-TR-35` `constraint` Every public route declares its own title plus description, with no two routes sharing either. `src: Technical requirements, meta`
- [ ] `C-TR-36` `literal` `/option` plus `/option/5.3.0` declare different titles, because the version is part of what the route is about. `src: Technical requirements, meta`
- [ ] `C-TR-37` `constraint` Every public route declares a social preview title plus a preview image that resolves to real bytes. `src: Technical requirements, preview`
- [ ] `C-TR-38` `constraint` A snippet route's preview image is the rendered chart for that snippet's own code, produced once, held against the snippet's `revision`. `src: Technical requirements, preview`
- [ ] `C-TR-39` `constraint` A snippet route's preview image is never rendered inside the crawler's own request. `src: Technical requirements, preview`
- [ ] `C-TR-40` `literal` A sitemap at `/sitemap.xml` lists every public route, one entry per retained option-reference version plus one per published example. `src: Technical requirements, sitemap`
- [ ] `C-TR-41` `literal` `/robots.txt` names the sitemap, which lists every public route. `src: Technical requirements, sitemap`
- [ ] `C-TR-42` `constraint` A bundle build for one request produces the same bytes every time, pinning the bundler version, the compiler target, the minifier plus its options. `src: Technical requirements, determinism`
- [ ] `C-TR-43` `constraint` Every timestamp plus absolute path is kept out of a bundle artifact's bytes. `src: Technical requirements, determinism`
- [ ] `C-TR-44` `constraint` The rendered thumbnail for one example's configuration is the same bytes every time, which is what lets the object be addressed by the digest of those bytes. `src: Technical requirements, determinism`
- [ ] `C-TR-45` `constraint` An evaluation of visitor code is stopped by the surrounding process once 5 seconds of wall clock have passed. `src: Technical requirements, budgets`
- [ ] `C-TR-46` `constraint` A bundle build stopped once 30 seconds or 1 gigabyte have passed returns no manifest, no install snippet, no recipe. `src: Technical requirements, budgets`
- [ ] `C-TR-47` `constraint` A rendered thumbnail lives in the bucket under its key scheme rather than on the app container's filesystem. Stored under its declared key scheme. `src: Technical requirements, object store`
- [ ] `C-TR-48` `constraint` A built bundle artifact lives in the bucket under its key scheme rather than as a column in a table. Stored under its declared key scheme. `src: Technical requirements, object store`
- [ ] `C-TR-49` `constraint` Neither a thumbnail nor an artifact is held in the app's memory between requests. Stored under its declared key scheme. `src: Technical requirements, object store`
- [ ] `C-TR-50` `constraint` What the portal shows plus what its own tables record can only reflect what is in the bucket, never stand in for the bucket. Stored under its declared key scheme. `src: Technical requirements, object store`

## C-DM Data model

- [ ] `C-DM-01` `data` The portal carries eleven tables whose timestamps are all UTC. Stored once in the seeded corpus. `src: Data model, opening`
- [ ] `C-DM-02` `literal` `users` carries `id`, `email` unique, `name`, `role` in `reader` or `contributor`, `password_hash`, `created_at`. `src: Data model, users`
- [ ] `C-DM-03` `literal` `releases` carries `version` unique, `released_on`, `commit`, `is_current`, `published_at`. Seeded once in the release records. `src: Data model, releases`
- [ ] `C-DM-04` `literal` The release `5.4.3` was released on `2026-02-18`, carrying `is_current` true. Seeded once in the release records. `src: Data model, releases table`
- [ ] `C-DM-05` `literal` The release `5.3.0` was released on `2025-11-05`, carrying `is_current` false. Seeded once in the release records. `src: Data model, releases table`
- [ ] `C-DM-06` `literal` The release `5.2.1` was released on `2025-07-22`, carrying `is_current` false. Seeded once in the release records. `src: Data model, releases table`
- [ ] `C-DM-07` `literal` `release_artifacts` carries `release_version`, `filename`, `size_bytes`, `sha256`, `sha512`, `signature_filename`, `attestation`. `src: Data model, release_artifacts`
- [ ] `C-DM-08` `literal` The artifact `chartic-5.4.3.tar.gz` carries the `sha256` `7d8968eb8880d7605fda3b6af5eaac8bac52c01423eb7d1f862ab732e9e82787`. Seeded once in the release records. `src: Data model, release_artifacts table`
- [ ] `C-DM-09` `literal` The artifact `chartic-5.3.0.tar.gz` carries the `sha256` `68ae5dcb7020eeebfe4f65558278857872e42d7da87979b884c4b5e5beb65c88`. Seeded once in the release records. `src: Data model, release_artifacts table`
- [ ] `C-DM-10` `literal` The artifact `chartic-5.2.1.tar.gz` carries the `sha256` `a47ad78a060a73e0347e48d4f425f31169ab858bd302bb4c71d05b9b95d74efe`. Seeded once in the release records. `src: Data model, release_artifacts table`
- [ ] `C-DM-11` `literal` The `5.4.3` archive carries the `sha512` `264915ce0335931833e3d3230344e2b1534f09ae6c179c7ffab856e44eff0e5e16c4299fe9c5be69c89a77664b8065c26374fefdada2c82aeb2ce04d136913ee`. Seeded once in the release records. `src: Data model, release_artifacts`
- [ ] `C-DM-12` `literal` The `5.4.3` archive's signature file is `chartic-5.4.3.tar.gz.asc`. Seeded once in the release records. `src: Data model, release_artifacts`
- [ ] `C-DM-13` `data` An artifact's `attestation` names the source revision built from, the builder plus the toolchain, signed by the build system rather than by a person. Seeded once in the release records. `src: Data model, release_artifacts`
- [ ] `C-DM-14` `literal` `mirrors` carries `host`, `release_version`, `recorded_sha256`, `serves_version`, `status` in `active`, `stale` or `removed`, `last_verified_at`. `src: Data model, mirrors`
- [ ] `C-DM-15` `constraint` A mirror's `status` in the download table is derived from the other columns rather than typed. `src: Data model, mirrors`
- [ ] `C-DM-16` `constraint` A mismatching mirror whose `recorded_sha256` differs from its artifact's `sha256` is `removed`. `src: Data model, mirrors`
- [ ] `C-DM-17` `constraint` A mirror whose `serves_version` is older than the release listed under is `stale`. `src: Data model, mirrors`
- [ ] `C-DM-18` `constraint` A mirror matching on both columns is `active` in the download table. `src: Data model, mirrors`
- [ ] `C-DM-19` `literal` `mirror-alpha.chartic-portal.example` is seeded `active` against `5.4.3`, serving `5.4.3` with a matching hash. Seeded once in the release records. `src: Data model, mirrors table`
- [ ] `C-DM-20` `literal` `mirror-beta.chartic-portal.example` is seeded `removed`, whose `recorded_sha256` is `aec03af8d255a240eaff00776dd6a087c7a87a63faf0449357a3f179406c574b`. Seeded once in the release records. `src: Data model, mirrors table`
- [ ] `C-DM-21` `literal` `mirror-gamma.chartic-portal.example` is seeded `stale`, serving `5.3.0` under the `5.4.3` release. `src: Data model, mirrors table`
- [ ] `C-DM-22` `literal` `changelog_entries` carries `release_version`, `position`, `kind`, `area`, `sentence`, `references`, `credits`. Seeded once in the release records. `src: Data model, changelog_entries`
- [ ] `C-DM-23` `literal` A seeded `5.4.3` changelog entry is a `Feature` in the area `legend` reading `Added legend.selectorLabel for the inverse selector`, referencing `#9142`, crediting `nhaddad`. `src: Data model, changelog_entries`
- [ ] `C-DM-24` `literal` A seeded `5.4.3` changelog entry is a `Fix` in the area `series` reading `Restored emphasis scaling on a single-point series`, referencing `#9107` plus `#9118`, crediting `tvargas`. `src: Data model, changelog_entries`
- [ ] `C-DM-25` `literal` `schema_nodes` carries `release_version`, `path`, `kind`, `types`, `default_kind`, `default_literal`, `default_sentence`, `default_worked_value`, `inherits_from`, `enum_values`, `applies_to`, `since`, `deprecated`, `removed`, `replaced_by`, `shared_object`, `variant_of`, `variant_value`, `description`, `position`. `src: Data model, schema_nodes`
- [ ] `C-DM-26` `constraint` The pair of `release_version` plus `path` is unique in `schema_nodes`, so one node's row is never shared between two versions. `src: Data model, schema_nodes`
- [ ] `C-DM-27` `literal` `title.show` is a boolean leaf whose literal default is `true`, since `5.0.0`. Seeded as one declared schema node. `src: Data model, schema_nodes table`
- [ ] `C-DM-28` `literal` `title.text` is a string leaf whose literal default is `''`, since `5.0.0`. Seeded as one declared schema node. `src: Data model, schema_nodes table`
- [ ] `C-DM-29` `literal` `tooltip.trigger` is a string leaf enumerating `item`, `axis`, `none`, whose literal default is `item`. Seeded as one declared schema node. `src: Data model, schema_nodes table`
- [ ] `C-DM-30` `literal` `xAxis.axisLabel.rotate` is a number leaf whose literal default is `0`, since `5.0.0`. Seeded as one declared schema node. `src: Data model, schema_nodes table`
- [ ] `C-DM-31` `literal` `xAxis.axisLabel.margin` is a number leaf whose literal default is `8`, since `5.0.0`. Seeded as one declared schema node. `src: Data model, schema_nodes table`
- [ ] `C-DM-32` `literal` `yAxis.axisLabel.rotate` is a number leaf whose literal default is `0`, since `5.0.0`. Seeded as one declared schema node. `src: Data model, schema_nodes table`
- [ ] `C-DM-33` `literal` `dataZoom.filterMode` is a string leaf enumerating `filter`, `weakFilter`, `empty`, `none`, whose literal default is `filter`. Seeded as one declared schema node. `src: Data model, schema_nodes table`
- [ ] `C-DM-34` `literal` `toolbox.feature.saveAsImage.title` is a string leaf whose literal default is `'Save as image'`. Seeded as one declared schema node. `src: Data model, schema_nodes table`
- [ ] `C-DM-35` `literal` `series.emphasis.scale` is a boolean leaf whose literal default is `true`, since `5.3.0`. Seeded as one declared schema node. `src: Data model, schema_nodes table`
- [ ] `C-DM-36` `literal` `legend.selectorLabel` is an object with an absent default, since `5.4.3`. Seeded as one declared schema node. `src: Data model, schema_nodes table`
- [ ] `C-DM-37` `literal` The shared object `textStyle` holds the leaves `color`, `fontSize` defaulting to `12`, `fontFamily` defaulting to `'sans-serif'`, `fontWeight` defaulting to `'normal'`. Seeded as one declared schema node. `src: Data model, shared object`
- [ ] `C-DM-38` `constraint` The shared object `textStyle` is stored once, expanded at `title.textStyle`, `legend.textStyle`, `tooltip.textStyle`. `src: Data model, shared object`
- [ ] `C-DM-39` `literal` `series.barWidth`'s generated default sentence is worked out from the width of the axis band, plus the number of bar series sharing that band. Seeded as one declared schema node. `src: Data model, computed case`
- [ ] `C-DM-40` `literal` `series.barWidth`'s worked value is `31` for one bar series on a category axis of six categories in a plot area 720 wide. Seeded as one declared schema node. `src: Data model, computed case`
- [ ] `C-DM-41` `literal` `series.label.position` inherits its default from `label.position`. Seeded as one declared schema node. `src: Data model, schema_nodes table`
- [ ] `C-DM-42` `literal` `series.data` carries a `line` variant whose entry is a number or a two-member array. Seeded as one declared schema node. `src: Data model, variants`
- [ ] `C-DM-43` `literal` `series.data` carries a `tree` variant whose entry is an object carrying `name`, `value`, `children`. Seeded as one declared schema node. `src: Data model, variants`
- [ ] `C-DM-44` `constraint` `series.hoverAnimation` is present under `5.2.1` with no `removed`, present under `5.3.0` plus `5.4.3` with `removed` set. Seeded as one declared schema node. `src: Data model, removal case`
- [ ] `C-DM-45` `constraint` `legend.selectorLabel` exists only under `5.4.3`. Seeded as one declared schema node. `src: Data model, removal case`
- [ ] `C-DM-46` `constraint` `series.emphasis.scale` exists under `5.3.0` plus `5.4.3`, absent from `5.2.1`. Seeded as one declared schema node. `src: Data model, removal case`
- [ ] `C-DM-47` `literal` `interface_nodes` carries `release_version`, `path`, `member_kind`, `signature`, `returns`, `arguments`, `description`, `since`, `position`. `src: Data model, interface_nodes`
- [ ] `C-DM-48` `literal` `charticInstance.setOption` carries the signature `setOption(option: object, notMerge?: boolean, lazyUpdate?: boolean) => void`. Seeded as one declared schema node. `src: Data model, interface_nodes`
- [ ] `C-DM-49` `literal` `examples` carries `id`, `title`, `category`, `tags`, `code_js`, `code_ts`, `data_inline`, `data_file`, `difficulty`, `since`, `uses`, `renderer`, `thumbnail_key`, `description`, `origin`, `state`, `owner_id`, `validated_at`, `created_at`. Stored once in the seeded corpus. `src: Data model, examples`
- [ ] `C-DM-50` `literal` `basic-line-smooth` is the published `Line` example `Smoothed Line` whose data is inline. Stored once in the seeded corpus. `src: Data model, examples table`
- [ ] `C-DM-51` `literal` `stacked-bar-margin` is the published `Bar` example `Stacked Bar with Margins` whose data is inline. Stored once in the seeded corpus. `src: Data model, examples table`
- [ ] `C-DM-52` `literal` `world-population-map` is the published `GEO/Map` example `World Population Map` whose data file is `population-2026.json`. Stored once in the seeded corpus. `src: Data model, examples table`
- [ ] `C-DM-53` `literal` `candle-volume-overlay` is the published `Candlestick` example `Candlestick with Volume` whose data is inline. Stored once in the seeded corpus. `src: Data model, examples table`
- [ ] `C-DM-54` `literal` `sunburst-nested-budget` is the published `Sunburst` example `Nested Budget Sunburst` whose data is inline. Stored once in the seeded corpus. `src: Data model, examples table`
- [ ] `C-DM-55` `literal` `radar-skills-compare` is the published `Radar` example `Skill Comparison Radar` whose data is inline. Stored once in the seeded corpus. `src: Data model, examples table`
- [ ] `C-DM-56` `literal` `bump-chart-lines` is the proposed `Lines` example `Bump Chart` whose data is inline. Stored once in the seeded corpus. `src: Data model, examples table`
- [ ] `C-DM-57` `constraint` `stacked-bar-margin` is the only seeded example whose `uses` carries `xAxis.axisLabel.rotate`. `src: Data model, examples notes`
- [ ] `C-DM-58` `constraint` The gallery tag filter narrows the corpus to `world-population-map` plus `candle-volume-overlay`, the only two carrying `large data`. `src: Data model, examples notes`
- [ ] `C-DM-59` `constraint` The gallery external data filter narrows the corpus to `world-population-map`, the only example with a `data_file`. `src: Data model, examples notes`
- [ ] `C-DM-60` `literal` The gallery tag filter narrows the corpus by `dark` to `radar-skills-compare`, by `animation` to `basic-line-smooth`, by `interaction` to `stacked-bar-margin` plus `sunburst-nested-budget`. `src: Data model, examples notes`
- [ ] `C-DM-61` `data` `bump-chart-lines` belongs to `contributor@example.com`, carrying no `validated_at`, absent from every public listing. `src: Data model, examples notes`
- [ ] `C-DM-62` `constraint` `bump-chart-lines` declares the category `Lines` against code creating a line series, the mismatch a first publish attempt is refused for. `src: Data model, examples notes`
- [ ] `C-DM-63` `literal` `basic-line-smooth`'s description, reported beside the render's elapsed milliseconds, reads `Line chart with 1 series. The category axis runs Mon to Sun. Values run from 120 to 260, highest on Sat, lowest on Mon.` `src: Data model, examples notes`
- [ ] `C-DM-64` `literal` `basic-line-smooth` reports a render count of `7` point marks, one per category. `src: Data model, examples notes`
- [ ] `C-DM-65` `literal` `snippets` carries `id`, `code`, `language`, `library_version`, `renderer`, `theme`, `decal`, `created_at`, `updated_at`, `owner_id`, `visibility`, `forked_from`, `revision`, `withdrawn_at`. Stored once in the seeded corpus. `src: Data model, snippets`
- [ ] `C-DM-66` `literal` The snippet `qkzm4p2vx7hd3nzr6tsw5bjy4c` is seeded at `revision` `1`, unlisted, owned by `contributor@example.com`. `src: Data model, snippets`
- [ ] `C-DM-67` `literal` The snippet `d4pv2sx6mhk3zrqt7nwy5bgj2f` is seeded withdrawn, whose address answers gone. Stored once in the seeded corpus. `src: Data model, snippets`
- [ ] `C-DM-68` `literal` `themes` carries `id`, `name`, `origin`, `values`, `series_colours`, `ground`, `contrast_report`, `preview_key`, `since`. Stored once in the seeded corpus. `src: Data model, themes`
- [ ] `C-DM-69` `literal` The theme `default` named `Default` is light, whose `series_colours` are the eight chart series colours in their palette order. Stored once in the seeded corpus. `src: Data model, themes`
- [ ] `C-DM-70` `literal` The theme `dark-slate` named `Dark Slate` is dark. Stored once in the seeded corpus. `src: Data model, themes`
- [ ] `C-DM-71` `literal` The theme `vintage` named `Vintage` is light. Stored once in the seeded corpus. `src: Data model, themes`
- [ ] `C-DM-72` `literal` The theme `sandstone` named `Sandstone` is light, whose `contrast_report` fails, naming its colliding pairs. Stored once in the seeded corpus. `src: Data model, themes`
- [ ] `C-DM-73` `literal` `modules` carries `release_version`, `module_id`, `requires`, `raw_bytes`. `src: Data model, modules`
- [ ] `C-DM-74` `literal` `chartic/core` requires nothing, at `118500` raw bytes. Stored once in the seeded corpus. `src: Data model, modules table`
- [ ] `C-DM-75` `literal` `chart/bar` requires `coord/cartesian`, at `41200` raw bytes. Stored once in the seeded corpus. `src: Data model, modules table`
- [ ] `C-DM-76` `literal` `chart/line` requires `coord/cartesian`, at `38600` raw bytes. Stored once in the seeded corpus. `src: Data model, modules table`
- [ ] `C-DM-77` `literal` `chart/pie` requires nothing, at `22400` raw bytes. Stored once in the seeded corpus. `src: Data model, modules table`
- [ ] `C-DM-78` `literal` `coord/cartesian` requires `component/axis`, at `33800` raw bytes. Stored once in the seeded corpus. `src: Data model, modules table`
- [ ] `C-DM-79` `literal` `component/axis` requires `scale/interval` plus `util/format`, at `27600` raw bytes. Stored once in the seeded corpus. `src: Data model, modules table`
- [ ] `C-DM-80` `literal` `scale/interval` requires nothing, at `11900` raw bytes. Stored once in the seeded corpus. `src: Data model, modules table`
- [ ] `C-DM-81` `literal` `util/format` requires nothing, at `9400` raw bytes. Stored once in the seeded corpus. `src: Data model, modules table`
- [ ] `C-DM-82` `literal` `component/legend` requires `util/format`, at `15300` raw bytes. Stored once in the seeded corpus. `src: Data model, modules table`
- [ ] `C-DM-83` `literal` `component/tooltip` requires `util/format`, at `24700` raw bytes. Stored once in the seeded corpus. `src: Data model, modules table`
- [ ] `C-DM-84` `constraint` `chartic/core` is always in a closure a bundle selection resolves. `src: Data model, modules`
- [ ] `C-DM-85` `literal` `bundle_builds` carries `request_digest` unique, `release_version`, `selection`, `renderers`, `locale`, `formats`, `minify`, `sourcemap`, `closure`, `artifact_key`, `artifact_sha256`, `integrity`, `sizes`, `status`, `queue_position`, `requested_at`, `ready_at`, `expires_at`. Stored once in the seeded corpus. `src: Data model, bundle_builds`
- [ ] `C-DM-86` `constraint` A build is addressed by the digest of its normalised request, so the same request finds the same row rather than starting a second build. `src: Data model, bundle_builds`
- [ ] `C-DM-87` `constraint` A ready build's `expires_at` is 30 days after its `ready_at`, whose manifest names the closure. `src: Data model, bundle_builds`
- [ ] `C-DM-88` `literal` `page_events` carries `id`, `route`, `occurred_at`, `query_text`, `result_rank`. Stored once in the seeded corpus. `src: Data model, page_events`
- [ ] `C-DM-89` `constraint` `page_events` states what is collected without an account, a session or an address. `src: Data model, page_events`
- [ ] `C-DM-90` `constraint` A row of what is collected older than 24 hours is discarded, leaving the aggregation the privacy page states. `src: Data model, page_events`
- [ ] `C-DM-91` `literal` A rendered thumbnail is stored at `thumbnails/{example_id}/{sha256_of_bytes}.svg`. Stored under its declared key scheme. `src: Data model, object keys`
- [ ] `C-DM-92` `literal` A built bundle artifact is stored at `bundles/{artifact_sha256}/chartic-{format}.js`. Stored under its declared key scheme. `src: Data model, object keys`
- [ ] `C-DM-93` `literal` The bundle artifact key `bundles/9f50bbd1dd7cc573d0583ffec5eb6b75506187df98b8743f9f86405ba41d2c35/chartic-esm.js` carries the integrity hash `sha384-aLheSBb58TNzRBFVuFY/RHlS6/61NJMzhZGcc3VCm0NIsiUSfvsxHKXBdXCU3/3y`. Stored under its declared key scheme. `src: Data model, object keys`
- [ ] `C-DM-94` `literal` `basic-line-smooth`'s thumbnail is stored at `thumbnails/basic-line-smooth/f7b809e012ada4d2b9afdd8464ace025532124a3c9253071e5afb429da7e6780.svg`. Stored under its declared key scheme. `src: Data model, object keys`
- [ ] `C-DM-95` `constraint` A published release row plus its artifacts never change once published, so two simultaneous edits both leave the stored record exactly as the record was. `src: Data model, invariants`
- [ ] `C-DM-96` `constraint` A snippet identifier is never reused, so two simultaneous shares store two different addresses in two rows. `src: Data model, invariants`
- [ ] `C-DM-97` `constraint` Two identical bundle requests arriving together produce exactly one build plus one artifact digest, both callers being answered with that digest. `src: Data model, invariants`
- [ ] `C-DM-98` `constraint` An example's `state` moves from `proposed` to `published` once, by its owner alone. `src: Data model, invariants`
- [ ] `C-DM-99` `constraint` A thumbnail object is never overwritten with different bytes at one key, because the key carries the digest of the bytes. `src: Data model, invariants`
- [ ] `C-DM-100` `constraint` Seeding is idempotent, so restarting the app duplicates no row. Stored once in the seeded corpus. `src: Data model, closing`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` One portal carries no tenancy, so every public listing shows one reader the same published example set. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` A nonsense address reaches the portal's own not-found page rather than a spreadsheet converter, a pasted-data chart recommendation or any data profiling. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` A snippet edit bumps its revision for the owner alone, with no co-editing, no presence channel, no other visitor's cursor. `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` A theme import refuses an uploaded image value, because palette extraction from an image is offered nowhere. `src: Constraints bullet 4`
- [ ] `C-CN-05` `constraint` Every public route declares its own title in one language, with no language segment, no language switch, no translation record. `src: Constraints bullet 5`
- [ ] `C-CN-06` `constraint` The sitemap lists no handbook, no tutorial content, no frequently-asked-questions route, no cheat sheet, no resources index, no extension directory. `src: Constraints bullet 6`
- [ ] `C-CN-07` `constraint` The sitemap lists no community section, no events route, no committer list, no mailing list, no contribution guide. `src: Constraints bullet 7`
- [ ] `C-CN-08` `constraint` The sitemap lists no security advisory route, with no machine-readable advisory feed anywhere. `src: Constraints bullet 8`
- [ ] `C-CN-09` `constraint` What the privacy page states is collected reaches no telemetry dashboard, no advertising, no third-party script, no consent banner. `src: Constraints bullet 9`
- [ ] `C-CN-10` `constraint` A removed property names its replacement version without any migration engine or configuration rewriter. `src: Constraints bullet 10`
- [ ] `C-CN-11` `constraint` A ready bundle artifact is read from the object store rather than over an external network call at runtime. `src: Constraints bullet 11`
- [ ] `C-CN-12` `constraint` Every public route declares its own title as a page rather than as a native application or an installable app shell. `src: Constraints bullet 12`
- [ ] `C-CN-13` `constraint` The portal stays responsive over three retained schema versions of roughly four hundred property nodes each. `src: Constraints bullet 13`
- [ ] `C-CN-14` `constraint` A bundle selection resolves its closure at speed over seven examples, four themes plus a ten-module graph. `src: Constraints bullet 13`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`, whose health returns 200 on one origin. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`, whose `4173` is the container-internal port the pages plus the health share as one origin. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` `APP_PUBLIC_PORT` is what the outside world uses, read from the environment by the one declared process serving every page. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The HTTP API is served under the `/api` prefix on the one origin the health shares with the pages. `src: Deployment contract bullet 2`
- [ ] `C-DC-05` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-06` `contract` The declared stack starts from the environment image with no manual steps, serving every page from one process. `src: Deployment contract bullet 4`
- [ ] `C-DC-07` `contract` The seeded account credentials are written to `/app/USER_README.md`, stored hashed in the users table. `src: Deployment contract bullet 5`
- [ ] `C-DC-08` `contract` A reserved `.browser_screenshots/` directory exists at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `contract` A reserved `.downloads/` directory exists at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-10` `contract` A production build of the declared stack is served behind a static or preview server rather than a dev server, from one process. `src: Deployment contract bullet 7`
- [ ] `C-DC-11` `contract` The server keeps running after the session ends, never as a child of the shell, so health still returns 200 on the same origin. `src: Deployment contract bullet 8`
- [ ] `C-DC-12` `contract` The app binds `0.0.0.0` rather than `127.0.0.1` or `localhost`, so the pages answer on the reachable origin. `src: Deployment contract bullet 9`
- [ ] `C-DC-13` `contract` The backing services the declared stack reads are already running, reachable at their environment variables from the one process. `src: Deployment contract bullet 10`
- [ ] `C-DC-14` `contract` The one declared process starts no copy of a backing service, downloading, installing nor compiling any. `src: Deployment contract bullet 10`
- [ ] `C-DC-15` `contract` Only the named providers are used, so a bundle artifact is uploaded to the object store rather than to an edge function. `src: Deployment contract bullet 11`
- [ ] `C-DC-16` `contract` The declared process serving every page carries no persistent volume, no fixed container name, no custom network. `src: Deployment contract bullet 12`
- [ ] `C-DC-17` `contract` Every list endpoint returns a top-level JSON array over the seeded corpus stored once. `src: Deployment contract, API shapes`
- [ ] `C-DC-18` `contract` A missing token is refused everywhere but `GET /api/health`, `POST /api/auth/login`, `POST /api/auth/signup`. `src: Deployment contract, API shapes`
- [ ] `C-DC-19` `constraint` An unauthorized call from a reader to a contributor endpoint is refused as a client error rather than with a `5xx` or a silent success. `src: Deployment contract, API shapes`
- [ ] `C-DC-20` `literal` `POST /api/auth/signup` takes `email`, `name`, `password`, returning `token` beside a `user` carrying `id`, `email`, `name`, `role`. `src: Deployment contract, API shapes`
- [ ] `C-DC-21` `literal` `POST /api/auth/login` takes `email`, `password`, returning `token` beside `user`. `src: Deployment contract, API shapes`
- [ ] `C-DC-22` `literal` `POST /api/auth/logout` leaves a signed-out token refused, returning an empty object. `src: Deployment contract, API shapes`
- [ ] `C-DC-23` `literal` `GET /api/me` returns the signed-in `user`, refused where the token is missing. `src: Deployment contract, API shapes`
- [ ] `C-DC-24` `literal` `GET /api/releases` returns an array of `version`, `released_on`, `is_current`, `artifacts`, `mirrors`. `src: Deployment contract, API shapes`
- [ ] `C-DC-25` `literal` `GET /api/releases/{version}` returns one release whose `changelog` entries carry a kind, an area, a sentence, a reference plus a credit. `src: Deployment contract, API shapes`
- [ ] `C-DC-26` `literal` `PATCH /api/releases/{version}` is refused, because a published record is immutable. `src: Deployment contract, API shapes`
- [ ] `C-DC-27` `literal` `GET /api/schema/{version}/tree` returns an array of top-level nodes carrying `path`, `kind`, `has_children`. `src: Deployment contract, API shapes`
- [ ] `C-DC-28` `literal` `GET /api/schema/{version}/node` takes `path`, returning one node carrying `default_kind`, `default_literal`, `default_sentence`, `default_worked_value`, `inherits_from`, `enum_values`, `since`, `deprecated`, `removed`, `replaced_by`, `shared_object`, `variants`, `fragment_id`, `children`. `src: Deployment contract, API shapes`
- [ ] `C-DC-29` `literal` `GET /api/schema/{version}/search` takes `q`, returning an array of `path`, `types`, `default_summary`, `first_sentence`, `first_match_index`, in rank order. `src: Deployment contract, API shapes`
- [ ] `C-DC-30` `literal` `GET /api/interface/{version}/node` takes `path`, returning `member_kind`, `signature`, `returns`, `arguments`, `since`, `cross_references`. `src: Deployment contract, API shapes`
- [ ] `C-DC-31` `literal` `GET /api/examples` takes `category`, `tag`, `q`, `external_data`, returning an array of `id`, `title`, `category`, `tags`, `has_external_data`, `thumbnail_url`, `description`. `src: Deployment contract, API shapes`
- [ ] `C-DC-32` `literal` `GET /api/examples/{id}` returns one example with `code_js`, `code_ts`, `uses`, `renderer`, `state`, `description`. `src: Deployment contract, API shapes`
- [ ] `C-DC-33` `literal` `GET /api/examples/{id}/thumbnail` returns the stored bytes as `image/svg+xml`, forbidden to a caller who owns no proposed example. `src: Deployment contract, API shapes`
- [ ] `C-DC-34` `literal` `GET /api/my/examples` answers as though another contributor's example is absent, returning the caller's own rows. `src: Deployment contract, API shapes`
- [ ] `C-DC-35` `literal` `POST /api/my/examples` takes `title`, `category`, `tags`, `code_js`, plus the decoy field `website_url`, which when filled is refused. `src: Deployment contract, API shapes`
- [ ] `C-DC-36` `literal` `PATCH /api/my/examples/{id}` takes any proposal field, returning the updated example. `src: Deployment contract, API shapes`
- [ ] `C-DC-37` `literal` `POST /api/my/examples/{id}/validate` returns `passed` beside `checks` carrying one entry per named check. `src: Deployment contract, API shapes`
- [ ] `C-DC-38` `literal` `POST /api/my/examples/{id}/publish` returns the example whose `state` is `published`, or a refusal naming the failing check. `src: Deployment contract, API shapes`
- [ ] `C-DC-39` `literal` `DELETE /api/my/examples/{id}` withdraws the example, returning an empty object. `src: Deployment contract, API shapes`
- [ ] `C-DC-40` `literal` `POST /api/snippets` takes `code`, `language`, `library_version`, `renderer`, `theme`, `decal`, `website_url`, returning a well-formed shared identifier, a `url` plus a `revision`. `src: Deployment contract, API shapes`
- [ ] `C-DC-41` `literal` `GET /api/snippets/{id}` returns one snippet, gone where the snippet was withdrawn. `src: Deployment contract, API shapes`
- [ ] `C-DC-42` `literal` `PATCH /api/snippets/{id}` takes `code`, returning the snippet with `revision` incremented. `src: Deployment contract, API shapes`
- [ ] `C-DC-43` `literal` `POST /api/render` takes `option` plus `renderer`, returning `elapsed_ms`, `points_drawn`, `description`, `document`, or a typed error naming the budget. `src: Deployment contract, API shapes`
- [ ] `C-DC-44` `literal` `GET /api/preferences` returns the one preference set of `dark`, `decal`, `renderer` shared by the reference, the gallery plus the editor. `src: Deployment contract, API shapes`
- [ ] `C-DC-45` `literal` `PUT /api/preferences` takes `dark`, `decal`, `renderer`, returning the stored preference set. `src: Deployment contract, API shapes`
- [ ] `C-DC-46` `literal` `GET /api/themes` returns an array of `id`, `name`, `origin`, `ground`, `series_colours`, `contrast_report`. `src: Deployment contract, API shapes`
- [ ] `C-DC-47` `literal` `POST /api/themes/validate` takes a theme document, returning `valid` or a refusal naming the offending key. `src: Deployment contract, API shapes`
- [ ] `C-DC-48` `literal` `GET /api/modules/{version}` returns an array of `module_id`, `requires`, `raw_bytes`, whose sum is the estimated total for a closure. `src: Deployment contract, API shapes`
- [ ] `C-DC-49` `literal` `POST /api/bundles` takes `release_version`, `selection`, `renderers`, `locale`, `formats`, `minify`, `sourcemap`, returning `request_digest`, `closure` with one `pulled_in_by` per member, `sizes`, `status`, `queue_position`. `src: Deployment contract, API shapes`
- [ ] `C-DC-50` `literal` `GET /api/bundles/{request_digest}` returns the build with `status`, `artifact_sha256`, `integrity`, `manifest`, `install_snippet`, `rebuild_command`. `src: Deployment contract, API shapes`
- [ ] `C-DC-51` `constraint` A thumbnail the app keeps as a byte string in a variable stands in for no stored object. `src: Deployment contract, No mocks`
- [ ] `C-DC-52` `constraint` A bundle artifact written to the container's own disk stands in for no uploaded object. `src: Deployment contract, No mocks`
- [ ] `C-DC-53` `constraint` A `thumbnail_url` returning a picture the app drew on the spot stands in for no stored object. `src: Deployment contract, No mocks`
- [ ] `C-DC-54` `constraint` A hardcoded valid answer the theme validator returns to itself stands in for no real theme import. `src: Deployment contract, No mocks`
- [ ] `C-DC-55` `constraint` A list of examples held in a module-level dictionary stands in for no stored corpus. `src: Deployment contract, No mocks`
- [ ] `C-DC-56` `constraint` The app's own pages plus tables can only reflect the rows plus the stored object keys that follow their declared schemes, never substitute for either. `src: Deployment contract, No mocks`

## Pinned literals

| Value | Meaning | Item | Where |
|---|---|---|---|
| `contributor@example.com` | value pinned by C-RL-18 | C-RL-18 | User roles, seeded accounts table |
| `Noor Haddad` | value pinned by C-RL-18 | C-RL-18 | User roles, seeded accounts table |
| `contributor` | value pinned by C-RL-18 | C-RL-18 | User roles, seeded accounts table |
| `contributor2@example.com` | value pinned by C-RL-19 | C-RL-19 | User roles, seeded accounts table |
| `Teo Vargas` | value pinned by C-RL-19 | C-RL-19 | User roles, seeded accounts table |
| `reader@example.com` | value pinned by C-RL-20 | C-RL-20 | User roles, seeded accounts table |
| `Lior Sand` | value pinned by C-RL-20 | C-RL-20 | User roles, seeded accounts table |
| `reader` | value pinned by C-RL-20 | C-RL-20 | User roles, seeded accounts table |
| `deku-demo-pw-2026` | value pinned by C-RL-21 | C-RL-21 | User roles para 3; Data model, opening |
| `Sign in failed` | value pinned by C-CF-05 | C-CF-05 | Core features rule 1 |
| `title.show` | value pinned by C-CF-22 | C-CF-22 | Core features rule 5 |
| `doc-content-title-show` | value pinned by C-CF-22 | C-CF-22 | Core features rule 5 |
| `legend.textStyle` | value pinned by C-CF-30 | C-CF-30 | Core features rule 7 |
| `fontSize` | value pinned by C-CF-30 | C-CF-30 | Core features rule 7 |
| `fontFamily` | value pinned by C-CF-30 | C-CF-30 | Core features rule 7 |
| `fontWeight` | value pinned by C-CF-30 | C-CF-30 | Core features rule 7 |
| `series.data` | value pinned by C-CF-34 | C-CF-34 | Core features rule 8 |
| `series.hoverAnimation` | value pinned by C-CF-36 | C-CF-36 | Core features rule 9 |
| `5.2.1` | value pinned by C-CF-36 | C-CF-36 | Core features rule 9 |
| `5.3.0` | value pinned by C-CF-37 | C-CF-37 | Core features rule 9 |
| `series.emphasis.disabled` | value pinned by C-CF-38 | C-CF-38 | Core features rule 9 |
| `legend.selectorLabel` | value pinned by C-CF-42 | C-CF-42 | Core features rule 10 |
| `5.4.3` | value pinned by C-CF-42 | C-CF-42 | Core features rule 10 |
| `title` | value pinned by C-CF-45 | C-CF-45 | Core features rule 11 |
| `toolbox.feature.saveAsImage.title` | value pinned by C-CF-45 | C-CF-45 | Core features rule 11 |
| `chartic` | value pinned by C-CF-51 | C-CF-51 | Core features feature 2 preamble |
| `charticInstance` | value pinned by C-CF-51 | C-CF-51 | Core features feature 2 preamble |
| `action` | value pinned by C-CF-51 | C-CF-51 | Core features feature 2 preamble |
| `events` | value pinned by C-CF-51 | C-CF-51 | Core features feature 2 preamble |
| `opts` | value pinned by C-CF-60 | C-CF-60 | Core features rule 14 |
| `chartic.init` | value pinned by C-CF-60 | C-CF-60 | Core features rule 14 |
| `uses` | value pinned by C-CF-68 | C-CF-68 | Core features rule 17 |
| `xAxis.axisLabel.rotate` | value pinned by C-CF-68 | C-CF-68 | Core features rule 17 |
| `stacked-bar-margin` | value pinned by C-CF-68 | C-CF-68 | Core features rule 17 |
| `animation` | value pinned by C-CF-70 | C-CF-70 | Core features rule 17 |
| `interaction` | value pinned by C-CF-70 | C-CF-70 | Core features rule 17 |
| `large data` | value pinned by C-CF-70 | C-CF-70 | Core features rule 17 |
| `accessibility` | value pinned by C-CF-70 | C-CF-70 | Core features rule 17 |
| `dark` | value pinned by C-CF-70 | C-CF-70 | Core features rule 17 |
| `Chart has been generated in ` | value pinned by C-CF-82 | C-CF-82 | Core features rule 22 |
| `ms` | value pinned by C-CF-82 | C-CF-82 | Core features rule 22 |
| `wall clock` | value pinned by C-CF-91 | C-CF-91 | Core features rule 24 |
| `memory` | value pinned by C-CF-91 | C-CF-91 | Core features rule 24 |
| `2` | value pinned by C-CF-100 | C-CF-100 | Core features rule 26 |
| `7` | value pinned by C-CF-100 | C-CF-100 | Core features rule 26 |
| `/s/<id>` | value pinned by C-CF-100 | C-CF-100 | Core features rule 26 |
| `d4pv2sx6mhk3zrqt7nwy5bgj2f` | value pinned by C-CF-109 | C-CF-109 | Core features rule 28 |
| `sandstone` | value pinned by C-CF-140 | C-CF-140 | Core features rule 34 |
| `chart/bar` | value pinned by C-CF-143 | C-CF-143 | Core features rule 35 |
| `chartic/core` | value pinned by C-CF-143 | C-CF-143 | Core features rule 35 |
| `coord/cartesian` | value pinned by C-CF-143 | C-CF-143 | Core features rule 35 |
| `component/axis` | value pinned by C-CF-143 | C-CF-143 | Core features rule 35 |
| `scale/interval` | value pinned by C-CF-143 | C-CF-143 | Core features rule 35 |
| `util/format` | value pinned by C-CF-143 | C-CF-143 | Core features rule 35 |
| `242400` | value pinned by C-CF-146 | C-CF-146 | Core features rule 35 |
| `2026/02/18` | value pinned by C-CF-163 | C-CF-163 | Core features rule 40 |
| `thumbnails/{example_id}/{sha256_of_bytes}.svg` | value pinned by C-CF-176 | C-CF-176 | Core features rule 43 |
| `bump-chart-lines` | value pinned by C-CF-177 | C-CF-177 | Core features rule 43 |
| `thumbnails/bump-chart-lines/a319ed61bc2c850dc1f06b05a0f22ca22876df0af2aeb72ca80283276a58a176.svg` | value pinned by C-CF-177 | C-CF-177 | Core features rule 43 |
| `website_url` | value pinned by C-CF-209 | C-CF-209 | Core features rule 49 |
| `/option/9.9.9` | value pinned by C-UF-28 | C-UF-28 | User flow, Entry and redirects |
| `No examples yet` | value pinned by C-UF-47 | C-UF-47 | User flow, States |
| `Propose your first example` | value pinned by C-UF-47 | C-UF-47 | User flow, States |
| `No examples match` | value pinned by C-UF-48 | C-UF-48 | User flow, States |
| `Clear filters` | value pinned by C-UF-48 | C-UF-48 | User flow, States |
| `No property matches` | value pinned by C-UF-49 | C-UF-49 | User flow, States |
| `Option` | value pinned by C-FE-61 | C-FE-61 | Front-end specification, the documentation shell |
| `API` | value pinned by C-FE-61 | C-FE-61 | Front-end specification, the documentation shell |
| `GL` | value pinned by C-FE-61 | C-FE-61 | Front-end specification, the documentation shell |
| `Tutorial` | value pinned by C-FE-61 | C-FE-61 | Front-end specification, the documentation shell |
| `Properties` | value pinned by C-FE-70 | C-FE-70 | Front-end specification, the documentation shell |
| `Preview` | value pinned by C-FE-77 | C-FE-77 | Front-end specification, the documentation shell |
| `legend` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `grid` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `xAxis` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `yAxis` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `polar` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `radiusAxis` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `angleAxis` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `radar` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `dataZoom` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `visualMap` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `tooltip` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `axisPointer` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `toolbox` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `brush` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `geo` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `parallel` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `parallelAxis` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `singleAxis` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `timeline` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `graphic` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `calendar` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `matrix` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `thumbnail` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `dataset` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `aria` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `series` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `darkMode` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `color` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `backgroundColor` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `textStyle` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `animationThreshold` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `animationDuration` | value pinned by C-FE-80 | C-FE-80 | Front-end specification, the option reference |
| `Line` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Bar` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Pie` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Scatter` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `GEO/Map` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Candlestick` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Radar` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Boxplot` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Heatmap` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Graph` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Lines` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Tree` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Treemap` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Sunburst` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Parallel` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Sankey` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Funnel` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Gauge` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `PictorialBar` | value pinned by C-FE-85 | C-FE-85 | Front-end specification, the gallery |
| `Line Chart` | value pinned by C-FE-115 | C-FE-115 | Front-end specification, the theme designer |
| `Stacked Area Chart` | value pinned by C-FE-115 | C-FE-115 | Front-end specification, the theme designer |
| `Bar Chart` | value pinned by C-FE-115 | C-FE-115 | Front-end specification, the theme designer |
| `Stacked Bar Chart` | value pinned by C-FE-115 | C-FE-115 | Front-end specification, the theme designer |
| `Scatter Chart` | value pinned by C-FE-115 | C-FE-115 | Front-end specification, the theme designer |
| `Pie Chart` | value pinned by C-FE-115 | C-FE-115 | Front-end specification, the theme designer |
| `Version` | value pinned by C-FE-119 | C-FE-119 | Front-end specification, the release archive |
| `Release Date` | value pinned by C-FE-119 | C-FE-119 | Front-end specification, the release archive |
| `Download Source from a Mirror` | value pinned by C-FE-119 | C-FE-119 | Front-end specification, the release archive |
| `Dist files` | value pinned by C-FE-119 | C-FE-119 | Front-end specification, the release archive |
| `build a bundle with only what you need` | value pinned by C-FE-124 | C-FE-124 | Front-end specification, the release archive |
| `DATABASE_URL` | value pinned by C-TR-06 | C-TR-06 | Technical requirements, para 2 |
| `STORAGE_ENDPOINT` | value pinned by C-TR-07 | C-TR-07 | Technical requirements, para 2 |
| `STORAGE_BUCKET` | value pinned by C-TR-07 | C-TR-07 | Technical requirements, para 2 |
| `STORAGE_ACCESS_KEY` | value pinned by C-TR-07 | C-TR-07 | Technical requirements, para 2 |
| `STORAGE_SECRET_KEY` | value pinned by C-TR-07 | C-TR-07 | Technical requirements, para 2 |
| `APP_PUBLIC_URL` | value pinned by C-TR-08 | C-TR-08 | Technical requirements, para 2 |
| `APP_PUBLIC_PORT` | value pinned by C-TR-08 | C-TR-08 | Technical requirements, para 2 |
| `GET /api/health` | value pinned by C-TR-24 | C-TR-24 | Technical requirements, health |
| `200` | value pinned by C-TR-24 | C-TR-24 | Technical requirements, health |
| `/favicon.ico` | value pinned by C-TR-34 | C-TR-34 | Technical requirements, favicon |
| `/option` | value pinned by C-TR-36 | C-TR-36 | Technical requirements, meta |
| `/option/5.3.0` | value pinned by C-TR-36 | C-TR-36 | Technical requirements, meta |
| `/sitemap.xml` | value pinned by C-TR-40 | C-TR-40 | Technical requirements, sitemap |
| `/robots.txt` | value pinned by C-TR-41 | C-TR-41 | Technical requirements, sitemap |
| `users` | value pinned by C-DM-02 | C-DM-02 | Data model, users |
| `id` | value pinned by C-DM-02 | C-DM-02 | Data model, users |
| `email` | value pinned by C-DM-02 | C-DM-02 | Data model, users |
| `name` | value pinned by C-DM-02 | C-DM-02 | Data model, users |
| `role` | value pinned by C-DM-02 | C-DM-02 | Data model, users |
| `password_hash` | value pinned by C-DM-02 | C-DM-02 | Data model, users |
| `created_at` | value pinned by C-DM-02 | C-DM-02 | Data model, users |
| `releases` | value pinned by C-DM-03 | C-DM-03 | Data model, releases |
| `version` | value pinned by C-DM-03 | C-DM-03 | Data model, releases |
| `released_on` | value pinned by C-DM-03 | C-DM-03 | Data model, releases |
| `commit` | value pinned by C-DM-03 | C-DM-03 | Data model, releases |
| `is_current` | value pinned by C-DM-03 | C-DM-03 | Data model, releases |
| `published_at` | value pinned by C-DM-03 | C-DM-03 | Data model, releases |
| `2026-02-18` | value pinned by C-DM-04 | C-DM-04 | Data model, releases table |
| `2025-11-05` | value pinned by C-DM-05 | C-DM-05 | Data model, releases table |
| `2025-07-22` | value pinned by C-DM-06 | C-DM-06 | Data model, releases table |
| `release_artifacts` | value pinned by C-DM-07 | C-DM-07 | Data model, release_artifacts |
| `release_version` | value pinned by C-DM-07 | C-DM-07 | Data model, release_artifacts |
| `filename` | value pinned by C-DM-07 | C-DM-07 | Data model, release_artifacts |
| `size_bytes` | value pinned by C-DM-07 | C-DM-07 | Data model, release_artifacts |
| `sha256` | value pinned by C-DM-07 | C-DM-07 | Data model, release_artifacts |
| `sha512` | value pinned by C-DM-07 | C-DM-07 | Data model, release_artifacts |
| `signature_filename` | value pinned by C-DM-07 | C-DM-07 | Data model, release_artifacts |
| `attestation` | value pinned by C-DM-07 | C-DM-07 | Data model, release_artifacts |
| `chartic-5.4.3.tar.gz` | value pinned by C-DM-08 | C-DM-08 | Data model, release_artifacts table |
| `7d8968eb8880d7605fda3b6af5eaac8bac52c01423eb7d1f862ab732e9e82787` | value pinned by C-DM-08 | C-DM-08 | Data model, release_artifacts table |
| `chartic-5.3.0.tar.gz` | value pinned by C-DM-09 | C-DM-09 | Data model, release_artifacts table |
| `68ae5dcb7020eeebfe4f65558278857872e42d7da87979b884c4b5e5beb65c88` | value pinned by C-DM-09 | C-DM-09 | Data model, release_artifacts table |
| `chartic-5.2.1.tar.gz` | value pinned by C-DM-10 | C-DM-10 | Data model, release_artifacts table |
| `a47ad78a060a73e0347e48d4f425f31169ab858bd302bb4c71d05b9b95d74efe` | value pinned by C-DM-10 | C-DM-10 | Data model, release_artifacts table |
| `264915ce0335931833e3d3230344e2b1534f09ae6c179c7ffab856e44eff0e5e16c4299fe9c5be69c89a77664b8065c26374fefdada2c82aeb2ce04d136913ee` | value pinned by C-DM-11 | C-DM-11 | Data model, release_artifacts |
| `chartic-5.4.3.tar.gz.asc` | value pinned by C-DM-12 | C-DM-12 | Data model, release_artifacts |
| `mirrors` | value pinned by C-DM-14 | C-DM-14 | Data model, mirrors |
| `host` | value pinned by C-DM-14 | C-DM-14 | Data model, mirrors |
| `recorded_sha256` | value pinned by C-DM-14 | C-DM-14 | Data model, mirrors |
| `serves_version` | value pinned by C-DM-14 | C-DM-14 | Data model, mirrors |
| `status` | value pinned by C-DM-14 | C-DM-14 | Data model, mirrors |
| `active` | value pinned by C-DM-14 | C-DM-14 | Data model, mirrors |
| `stale` | value pinned by C-DM-14 | C-DM-14 | Data model, mirrors |
| `removed` | value pinned by C-DM-14 | C-DM-14 | Data model, mirrors |
| `last_verified_at` | value pinned by C-DM-14 | C-DM-14 | Data model, mirrors |
| `mirror-alpha.chartic-portal.example` | value pinned by C-DM-19 | C-DM-19 | Data model, mirrors table |
| `mirror-beta.chartic-portal.example` | value pinned by C-DM-20 | C-DM-20 | Data model, mirrors table |
| `aec03af8d255a240eaff00776dd6a087c7a87a63faf0449357a3f179406c574b` | value pinned by C-DM-20 | C-DM-20 | Data model, mirrors table |
| `mirror-gamma.chartic-portal.example` | value pinned by C-DM-21 | C-DM-21 | Data model, mirrors table |
| `changelog_entries` | value pinned by C-DM-22 | C-DM-22 | Data model, changelog_entries |
| `position` | value pinned by C-DM-22 | C-DM-22 | Data model, changelog_entries |
| `kind` | value pinned by C-DM-22 | C-DM-22 | Data model, changelog_entries |
| `area` | value pinned by C-DM-22 | C-DM-22 | Data model, changelog_entries |
| `sentence` | value pinned by C-DM-22 | C-DM-22 | Data model, changelog_entries |
| `references` | value pinned by C-DM-22 | C-DM-22 | Data model, changelog_entries |
| `credits` | value pinned by C-DM-22 | C-DM-22 | Data model, changelog_entries |
| `Feature` | value pinned by C-DM-23 | C-DM-23 | Data model, changelog_entries |
| `Added legend.selectorLabel for the inverse selector` | value pinned by C-DM-23 | C-DM-23 | Data model, changelog_entries |
| `#9142` | value pinned by C-DM-23 | C-DM-23 | Data model, changelog_entries |
| `nhaddad` | value pinned by C-DM-23 | C-DM-23 | Data model, changelog_entries |
| `Fix` | value pinned by C-DM-24 | C-DM-24 | Data model, changelog_entries |
| `Restored emphasis scaling on a single-point series` | value pinned by C-DM-24 | C-DM-24 | Data model, changelog_entries |
| `#9107` | value pinned by C-DM-24 | C-DM-24 | Data model, changelog_entries |
| `#9118` | value pinned by C-DM-24 | C-DM-24 | Data model, changelog_entries |
| `tvargas` | value pinned by C-DM-24 | C-DM-24 | Data model, changelog_entries |
| `schema_nodes` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `path` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `types` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `default_kind` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `default_literal` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `default_sentence` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `default_worked_value` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `inherits_from` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `enum_values` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `applies_to` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `since` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `deprecated` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `replaced_by` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `shared_object` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `variant_of` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `variant_value` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `description` | value pinned by C-DM-25 | C-DM-25 | Data model, schema_nodes |
| `true` | value pinned by C-DM-27 | C-DM-27 | Data model, schema_nodes table |
| `5.0.0` | value pinned by C-DM-27 | C-DM-27 | Data model, schema_nodes table |
| `title.text` | value pinned by C-DM-28 | C-DM-28 | Data model, schema_nodes table |
| `''` | value pinned by C-DM-28 | C-DM-28 | Data model, schema_nodes table |
| `tooltip.trigger` | value pinned by C-DM-29 | C-DM-29 | Data model, schema_nodes table |
| `item` | value pinned by C-DM-29 | C-DM-29 | Data model, schema_nodes table |
| `axis` | value pinned by C-DM-29 | C-DM-29 | Data model, schema_nodes table |
| `none` | value pinned by C-DM-29 | C-DM-29 | Data model, schema_nodes table |
| `0` | value pinned by C-DM-30 | C-DM-30 | Data model, schema_nodes table |
| `xAxis.axisLabel.margin` | value pinned by C-DM-31 | C-DM-31 | Data model, schema_nodes table |
| `8` | value pinned by C-DM-31 | C-DM-31 | Data model, schema_nodes table |
| `yAxis.axisLabel.rotate` | value pinned by C-DM-32 | C-DM-32 | Data model, schema_nodes table |
| `dataZoom.filterMode` | value pinned by C-DM-33 | C-DM-33 | Data model, schema_nodes table |
| `filter` | value pinned by C-DM-33 | C-DM-33 | Data model, schema_nodes table |
| `weakFilter` | value pinned by C-DM-33 | C-DM-33 | Data model, schema_nodes table |
| `empty` | value pinned by C-DM-33 | C-DM-33 | Data model, schema_nodes table |
| `'Save as image'` | value pinned by C-DM-34 | C-DM-34 | Data model, schema_nodes table |
| `series.emphasis.scale` | value pinned by C-DM-35 | C-DM-35 | Data model, schema_nodes table |
| `12` | value pinned by C-DM-37 | C-DM-37 | Data model, shared object |
| `'sans-serif'` | value pinned by C-DM-37 | C-DM-37 | Data model, shared object |
| `'normal'` | value pinned by C-DM-37 | C-DM-37 | Data model, shared object |
| `series.barWidth` | value pinned by C-DM-39 | C-DM-39 | Data model, computed case |
| `31` | value pinned by C-DM-40 | C-DM-40 | Data model, computed case |
| `series.label.position` | value pinned by C-DM-41 | C-DM-41 | Data model, schema_nodes table |
| `label.position` | value pinned by C-DM-41 | C-DM-41 | Data model, schema_nodes table |
| `line` | value pinned by C-DM-42 | C-DM-42 | Data model, variants |
| `tree` | value pinned by C-DM-43 | C-DM-43 | Data model, variants |
| `value` | value pinned by C-DM-43 | C-DM-43 | Data model, variants |
| `children` | value pinned by C-DM-43 | C-DM-43 | Data model, variants |
| `interface_nodes` | value pinned by C-DM-47 | C-DM-47 | Data model, interface_nodes |
| `member_kind` | value pinned by C-DM-47 | C-DM-47 | Data model, interface_nodes |
| `signature` | value pinned by C-DM-47 | C-DM-47 | Data model, interface_nodes |
| `returns` | value pinned by C-DM-47 | C-DM-47 | Data model, interface_nodes |
| `arguments` | value pinned by C-DM-47 | C-DM-47 | Data model, interface_nodes |
| `charticInstance.setOption` | value pinned by C-DM-48 | C-DM-48 | Data model, interface_nodes |
| `setOption(option: object, notMerge?: boolean, lazyUpdate?: boolean) => void` | value pinned by C-DM-48 | C-DM-48 | Data model, interface_nodes |
| `examples` | value pinned by C-DM-49 | C-DM-49 | Data model, examples |
| `category` | value pinned by C-DM-49 | C-DM-49 | Data model, examples |
| `tags` | value pinned by C-DM-49 | C-DM-49 | Data model, examples |
| `code_js` | value pinned by C-DM-49 | C-DM-49 | Data model, examples |
| `code_ts` | value pinned by C-DM-49 | C-DM-49 | Data model, examples |
| `data_inline` | value pinned by C-DM-49 | C-DM-49 | Data model, examples |
| `data_file` | value pinned by C-DM-49 | C-DM-49 | Data model, examples |
| `difficulty` | value pinned by C-DM-49 | C-DM-49 | Data model, examples |
| `renderer` | value pinned by C-DM-49 | C-DM-49 | Data model, examples |
| `thumbnail_key` | value pinned by C-DM-49 | C-DM-49 | Data model, examples |
| `origin` | value pinned by C-DM-49 | C-DM-49 | Data model, examples |
| `state` | value pinned by C-DM-49 | C-DM-49 | Data model, examples |
| `owner_id` | value pinned by C-DM-49 | C-DM-49 | Data model, examples |
| `validated_at` | value pinned by C-DM-49 | C-DM-49 | Data model, examples |
| `basic-line-smooth` | value pinned by C-DM-50 | C-DM-50 | Data model, examples table |
| `Smoothed Line` | value pinned by C-DM-50 | C-DM-50 | Data model, examples table |
| `Stacked Bar with Margins` | value pinned by C-DM-51 | C-DM-51 | Data model, examples table |
| `world-population-map` | value pinned by C-DM-52 | C-DM-52 | Data model, examples table |
| `World Population Map` | value pinned by C-DM-52 | C-DM-52 | Data model, examples table |
| `population-2026.json` | value pinned by C-DM-52 | C-DM-52 | Data model, examples table |
| `candle-volume-overlay` | value pinned by C-DM-53 | C-DM-53 | Data model, examples table |
| `Candlestick with Volume` | value pinned by C-DM-53 | C-DM-53 | Data model, examples table |
| `sunburst-nested-budget` | value pinned by C-DM-54 | C-DM-54 | Data model, examples table |
| `Nested Budget Sunburst` | value pinned by C-DM-54 | C-DM-54 | Data model, examples table |
| `radar-skills-compare` | value pinned by C-DM-55 | C-DM-55 | Data model, examples table |
| `Skill Comparison Radar` | value pinned by C-DM-55 | C-DM-55 | Data model, examples table |
| `Bump Chart` | value pinned by C-DM-56 | C-DM-56 | Data model, examples table |
| `Line chart with 1 series. The category axis runs Mon to Sun. Values run from 120 to 260, highest on Sat, lowest on Mon.` | value pinned by C-DM-63 | C-DM-63 | Data model, examples notes |
| `snippets` | value pinned by C-DM-65 | C-DM-65 | Data model, snippets |
| `code` | value pinned by C-DM-65 | C-DM-65 | Data model, snippets |
| `language` | value pinned by C-DM-65 | C-DM-65 | Data model, snippets |
| `library_version` | value pinned by C-DM-65 | C-DM-65 | Data model, snippets |
| `theme` | value pinned by C-DM-65 | C-DM-65 | Data model, snippets |
| `decal` | value pinned by C-DM-65 | C-DM-65 | Data model, snippets |
| `updated_at` | value pinned by C-DM-65 | C-DM-65 | Data model, snippets |
| `visibility` | value pinned by C-DM-65 | C-DM-65 | Data model, snippets |
| `forked_from` | value pinned by C-DM-65 | C-DM-65 | Data model, snippets |
| `revision` | value pinned by C-DM-65 | C-DM-65 | Data model, snippets |
| `withdrawn_at` | value pinned by C-DM-65 | C-DM-65 | Data model, snippets |
| `qkzm4p2vx7hd3nzr6tsw5bjy4c` | value pinned by C-DM-66 | C-DM-66 | Data model, snippets |
| `1` | value pinned by C-DM-66 | C-DM-66 | Data model, snippets |
| `themes` | value pinned by C-DM-68 | C-DM-68 | Data model, themes |
| `values` | value pinned by C-DM-68 | C-DM-68 | Data model, themes |
| `series_colours` | value pinned by C-DM-68 | C-DM-68 | Data model, themes |
| `ground` | value pinned by C-DM-68 | C-DM-68 | Data model, themes |
| `contrast_report` | value pinned by C-DM-68 | C-DM-68 | Data model, themes |
| `preview_key` | value pinned by C-DM-68 | C-DM-68 | Data model, themes |
| `default` | value pinned by C-DM-69 | C-DM-69 | Data model, themes |
| `Default` | value pinned by C-DM-69 | C-DM-69 | Data model, themes |
| `dark-slate` | value pinned by C-DM-70 | C-DM-70 | Data model, themes |
| `Dark Slate` | value pinned by C-DM-70 | C-DM-70 | Data model, themes |
| `vintage` | value pinned by C-DM-71 | C-DM-71 | Data model, themes |
| `Vintage` | value pinned by C-DM-71 | C-DM-71 | Data model, themes |
| `Sandstone` | value pinned by C-DM-72 | C-DM-72 | Data model, themes |
| `modules` | value pinned by C-DM-73 | C-DM-73 | Data model, modules |
| `module_id` | value pinned by C-DM-73 | C-DM-73 | Data model, modules |
| `requires` | value pinned by C-DM-73 | C-DM-73 | Data model, modules |
| `raw_bytes` | value pinned by C-DM-73 | C-DM-73 | Data model, modules |
| `118500` | value pinned by C-DM-74 | C-DM-74 | Data model, modules table |
| `41200` | value pinned by C-DM-75 | C-DM-75 | Data model, modules table |
| `chart/line` | value pinned by C-DM-76 | C-DM-76 | Data model, modules table |
| `38600` | value pinned by C-DM-76 | C-DM-76 | Data model, modules table |
| `chart/pie` | value pinned by C-DM-77 | C-DM-77 | Data model, modules table |
| `22400` | value pinned by C-DM-77 | C-DM-77 | Data model, modules table |
| `33800` | value pinned by C-DM-78 | C-DM-78 | Data model, modules table |
| `27600` | value pinned by C-DM-79 | C-DM-79 | Data model, modules table |
| `11900` | value pinned by C-DM-80 | C-DM-80 | Data model, modules table |
| `9400` | value pinned by C-DM-81 | C-DM-81 | Data model, modules table |
| `component/legend` | value pinned by C-DM-82 | C-DM-82 | Data model, modules table |
| `15300` | value pinned by C-DM-82 | C-DM-82 | Data model, modules table |
| `component/tooltip` | value pinned by C-DM-83 | C-DM-83 | Data model, modules table |
| `24700` | value pinned by C-DM-83 | C-DM-83 | Data model, modules table |
| `bundle_builds` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `request_digest` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `selection` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `renderers` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `locale` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `formats` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `minify` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `sourcemap` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `closure` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `artifact_key` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `artifact_sha256` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `integrity` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `sizes` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `queue_position` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `requested_at` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `ready_at` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `expires_at` | value pinned by C-DM-85 | C-DM-85 | Data model, bundle_builds |
| `page_events` | value pinned by C-DM-88 | C-DM-88 | Data model, page_events |
| `route` | value pinned by C-DM-88 | C-DM-88 | Data model, page_events |
| `occurred_at` | value pinned by C-DM-88 | C-DM-88 | Data model, page_events |
| `query_text` | value pinned by C-DM-88 | C-DM-88 | Data model, page_events |
| `result_rank` | value pinned by C-DM-88 | C-DM-88 | Data model, page_events |
| `bundles/{artifact_sha256}/chartic-{format}.js` | value pinned by C-DM-92 | C-DM-92 | Data model, object keys |
| `bundles/9f50bbd1dd7cc573d0583ffec5eb6b75506187df98b8743f9f86405ba41d2c35/chartic-esm.js` | value pinned by C-DM-93 | C-DM-93 | Data model, object keys |
| `sha384-aLheSBb58TNzRBFVuFY/RHlS6/61NJMzhZGcc3VCm0NIsiUSfvsxHKXBdXCU3/3y` | value pinned by C-DM-93 | C-DM-93 | Data model, object keys |
| `thumbnails/basic-line-smooth/f7b809e012ada4d2b9afdd8464ace025532124a3c9253071e5afb429da7e6780.svg` | value pinned by C-DM-94 | C-DM-94 | Data model, object keys |
| `POST /api/auth/signup` | value pinned by C-DC-20 | C-DC-20 | Deployment contract, API shapes |
| `password` | value pinned by C-DC-20 | C-DC-20 | Deployment contract, API shapes |
| `token` | value pinned by C-DC-20 | C-DC-20 | Deployment contract, API shapes |
| `user` | value pinned by C-DC-20 | C-DC-20 | Deployment contract, API shapes |
| `POST /api/auth/login` | value pinned by C-DC-21 | C-DC-21 | Deployment contract, API shapes |
| `POST /api/auth/logout` | value pinned by C-DC-22 | C-DC-22 | Deployment contract, API shapes |
| `GET /api/me` | value pinned by C-DC-23 | C-DC-23 | Deployment contract, API shapes |
| `GET /api/releases` | value pinned by C-DC-24 | C-DC-24 | Deployment contract, API shapes |
| `artifacts` | value pinned by C-DC-24 | C-DC-24 | Deployment contract, API shapes |
| `GET /api/releases/{version}` | value pinned by C-DC-25 | C-DC-25 | Deployment contract, API shapes |
| `changelog` | value pinned by C-DC-25 | C-DC-25 | Deployment contract, API shapes |
| `PATCH /api/releases/{version}` | value pinned by C-DC-26 | C-DC-26 | Deployment contract, API shapes |
| `GET /api/schema/{version}/tree` | value pinned by C-DC-27 | C-DC-27 | Deployment contract, API shapes |
| `has_children` | value pinned by C-DC-27 | C-DC-27 | Deployment contract, API shapes |
| `GET /api/schema/{version}/node` | value pinned by C-DC-28 | C-DC-28 | Deployment contract, API shapes |
| `variants` | value pinned by C-DC-28 | C-DC-28 | Deployment contract, API shapes |
| `fragment_id` | value pinned by C-DC-28 | C-DC-28 | Deployment contract, API shapes |
| `GET /api/schema/{version}/search` | value pinned by C-DC-29 | C-DC-29 | Deployment contract, API shapes |
| `q` | value pinned by C-DC-29 | C-DC-29 | Deployment contract, API shapes |
| `default_summary` | value pinned by C-DC-29 | C-DC-29 | Deployment contract, API shapes |
| `first_sentence` | value pinned by C-DC-29 | C-DC-29 | Deployment contract, API shapes |
| `first_match_index` | value pinned by C-DC-29 | C-DC-29 | Deployment contract, API shapes |
| `GET /api/interface/{version}/node` | value pinned by C-DC-30 | C-DC-30 | Deployment contract, API shapes |
| `cross_references` | value pinned by C-DC-30 | C-DC-30 | Deployment contract, API shapes |
| `GET /api/examples` | value pinned by C-DC-31 | C-DC-31 | Deployment contract, API shapes |
| `tag` | value pinned by C-DC-31 | C-DC-31 | Deployment contract, API shapes |
| `external_data` | value pinned by C-DC-31 | C-DC-31 | Deployment contract, API shapes |
| `has_external_data` | value pinned by C-DC-31 | C-DC-31 | Deployment contract, API shapes |
| `thumbnail_url` | value pinned by C-DC-31 | C-DC-31 | Deployment contract, API shapes |
| `GET /api/examples/{id}` | value pinned by C-DC-32 | C-DC-32 | Deployment contract, API shapes |
| `GET /api/examples/{id}/thumbnail` | value pinned by C-DC-33 | C-DC-33 | Deployment contract, API shapes |
| `image/svg+xml` | value pinned by C-DC-33 | C-DC-33 | Deployment contract, API shapes |
| `GET /api/my/examples` | value pinned by C-DC-34 | C-DC-34 | Deployment contract, API shapes |
| `POST /api/my/examples` | value pinned by C-DC-35 | C-DC-35 | Deployment contract, API shapes |
| `PATCH /api/my/examples/{id}` | value pinned by C-DC-36 | C-DC-36 | Deployment contract, API shapes |
| `POST /api/my/examples/{id}/validate` | value pinned by C-DC-37 | C-DC-37 | Deployment contract, API shapes |
| `passed` | value pinned by C-DC-37 | C-DC-37 | Deployment contract, API shapes |
| `checks` | value pinned by C-DC-37 | C-DC-37 | Deployment contract, API shapes |
| `POST /api/my/examples/{id}/publish` | value pinned by C-DC-38 | C-DC-38 | Deployment contract, API shapes |
| `published` | value pinned by C-DC-38 | C-DC-38 | Deployment contract, API shapes |
| `DELETE /api/my/examples/{id}` | value pinned by C-DC-39 | C-DC-39 | Deployment contract, API shapes |
| `POST /api/snippets` | value pinned by C-DC-40 | C-DC-40 | Deployment contract, API shapes |
| `url` | value pinned by C-DC-40 | C-DC-40 | Deployment contract, API shapes |
| `GET /api/snippets/{id}` | value pinned by C-DC-41 | C-DC-41 | Deployment contract, API shapes |
| `PATCH /api/snippets/{id}` | value pinned by C-DC-42 | C-DC-42 | Deployment contract, API shapes |
| `POST /api/render` | value pinned by C-DC-43 | C-DC-43 | Deployment contract, API shapes |
| `option` | value pinned by C-DC-43 | C-DC-43 | Deployment contract, API shapes |
| `elapsed_ms` | value pinned by C-DC-43 | C-DC-43 | Deployment contract, API shapes |
| `points_drawn` | value pinned by C-DC-43 | C-DC-43 | Deployment contract, API shapes |
| `document` | value pinned by C-DC-43 | C-DC-43 | Deployment contract, API shapes |
| `GET /api/preferences` | value pinned by C-DC-44 | C-DC-44 | Deployment contract, API shapes |
| `PUT /api/preferences` | value pinned by C-DC-45 | C-DC-45 | Deployment contract, API shapes |
| `GET /api/themes` | value pinned by C-DC-46 | C-DC-46 | Deployment contract, API shapes |
| `POST /api/themes/validate` | value pinned by C-DC-47 | C-DC-47 | Deployment contract, API shapes |
| `valid` | value pinned by C-DC-47 | C-DC-47 | Deployment contract, API shapes |
| `GET /api/modules/{version}` | value pinned by C-DC-48 | C-DC-48 | Deployment contract, API shapes |
| `POST /api/bundles` | value pinned by C-DC-49 | C-DC-49 | Deployment contract, API shapes |
| `pulled_in_by` | value pinned by C-DC-49 | C-DC-49 | Deployment contract, API shapes |
| `GET /api/bundles/{request_digest}` | value pinned by C-DC-50 | C-DC-50 | Deployment contract, API shapes |
| `manifest` | value pinned by C-DC-50 | C-DC-50 | Deployment contract, API shapes |
| `install_snippet` | value pinned by C-DC-50 | C-DC-50 | Deployment contract, API shapes |
| `rebuild_command` | value pinned by C-DC-50 | C-DC-50 | Deployment contract, API shapes |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 1 | 8 |
| User roles | 1 | 24 |
| Core features | 25 | 211 |
| User flow | 6 | 52 |
| UI/UX notes | 7 | 78 |
| Front-end specification | 10 | 146 |
| Technical requirements | 14 | 50 |
| Data model | 7 | 100 |
| Constraints | 1 | 14 |
| Deployment contract | 13 | 56 |
