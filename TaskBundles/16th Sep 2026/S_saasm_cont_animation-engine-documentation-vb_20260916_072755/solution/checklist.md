# Checklist: Lumen.js

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 725
Unpinned values flagged: 4

## C-OV Overview

- [ ] `C-OV-01` `capability` The product serves the public site of an open-source web animation engine. `src: Overview para 1`
- [ ] `C-OV-02` `constraint` The product sells nothing. `src: Overview para 1`
- [ ] `C-OV-03` `constraint` The product carries no visitor account. `src: Overview para 2`
- [ ] `C-OV-04` `constraint` No public route carries a sign-in control. `src: Overview para 2`
- [ ] `C-OV-05` `capability` Adding an address to a mailing list is the only change a visitor can make on the server. `src: Overview para 2`
- [ ] `C-OV-06` `capability` The home route serves a scroll-driven product tour. `src: Overview para 3`
- [ ] `C-OV-07` `capability` The product serves versioned documentation of sixteen modules. `src: Overview para 3`
- [ ] `C-OV-08` `capability` The product serves a curve editor. `src: Overview para 3`
- [ ] `C-OV-09` `capability` The product serves a course waiting list. `src: Overview para 3`
- [ ] `C-OV-10` `capability` Sponsor placements run through the documentation, the tour. `src: Overview para 3`
- [ ] `C-OV-11` `constraint` The animation engine itself is out of scope. `src: Overview para 5`
- [ ] `C-OV-12` `constraint` No binary file ships with the product. `src: Overview para 5`
- [ ] `C-OV-13` `constraint` Every outside service the site leans on carries a stated degraded state. `src: Overview para 6`

## C-RL User roles

- [ ] `C-RL-01` `role` A Visitor reads every published route without signing in. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A Visitor runs every demonstration. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A Visitor uses the whole curve editor. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A Visitor submits an address to either mailing list. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A Visitor cannot read a draft version at any address. `src: User roles table row 1`
- [ ] `C-RL-06` `role` A Visitor cannot reach the studio. `src: User roles table row 1`
- [ ] `C-RL-07` `role` A Visitor cannot publish a version. `src: User roles table row 1`
- [ ] `C-RL-08` `role` A Visitor cannot read the mail outbox. `src: User roles table row 1`
- [ ] `C-RL-09` `role` A Visitor cannot read the page-view log. `src: User roles table row 1`
- [ ] `C-RL-10` `role` A Visitor cannot run a background job. `src: User roles table row 1`
- [ ] `C-RL-11` `role` A Maintainer reaches every studio surface. `src: User roles table row 2`
- [ ] `C-RL-12` `constraint` A role is read from the signed-in account's session. `src: User roles para 1`
- [ ] `C-RL-13` `constraint` A role is never read from a request body, a query parameter, a caller-supplied header. `src: User roles para 1`
- [ ] `C-RL-14` `contract` A direct call from a Visitor session to a Maintainer-only endpoint is rejected with `401` or `403`. `src: User roles, authorization paragraph`
- [ ] `C-RL-15` `constraint` The product offers no signup to a visitor. `src: User roles, signup paragraph`
- [ ] `C-RL-16` `literal` The seeded maintainer account is `maintainer@example.com`. `src: User roles, seeded account paragraph`
- [ ] `C-RL-17` `literal` The seeded maintainer display name is `Elias Marchand`. `src: User roles, seeded account paragraph`

## C-CF Core features

- [ ] `C-CF-01` `capability` The maintainer exchanges an email address plus a password for a bearer token. `src: Core features, sign-in para 1`
- [ ] `C-CF-02` `constraint` A password is stored under a memory-hard password hash. `src: Core features, sign-in para 1`
- [ ] `C-CF-03` `constraint` A password is never stored in any recoverable form. `src: Core features, sign-in para 1`
- [ ] `C-CF-04` `capability` A studio page reads the same token from an http-only cookie. `src: Core features, sign-in para 1`
- [ ] `C-CF-05` `capability` A sign-in carrying a wrong password is refused. `src: Core features, sign-in rule 1`
- [ ] `C-CF-06` `constraint` A refused sign-in does not say which of the two credentials was wrong. `src: Core features, sign-in rule 1`
- [ ] `C-CF-07` `capability` Signing out invalidates the bearer token. `src: Core features, sign-in rule 2`
- [ ] `C-CF-08` `capability` A request replaying a signed-out token is denied. `src: Core features, sign-in rule 2`
- [ ] `C-CF-09` `capability` An expired token returns the maintainer to the sign-in page. `src: Core features, sign-in rule 3`
- [ ] `C-CF-10` `constraint` No public route links to `/login`. `src: Core features, sign-in rule 4`
- [ ] `C-CF-11` `capability` The tour holds one stage fixed in the window for the whole scroll range. `src: Core features, tour rule 1`
- [ ] `C-CF-12` `capability` The tour carries exactly twelve narrative stops. `src: Core features, tour rule 2`
- [ ] `C-CF-13` `literal` The tour's stop fragments in order are `intro`, `toolbox`, `intuitive`, `composition`, `scroll`, `staggering`, `svg-utilities`, `draggable`, `clockwork`, `responsive`, `modules`, `sponsors`. `src: Core features, tour rule 2`
- [ ] `C-CF-14` `capability` The current stop is derived continuously from scroll position. `src: Core features, tour rule 3`
- [ ] `C-CF-15` `constraint` The current stop is never derived from an arrival callback alone. `src: Core features, tour rule 3`
- [ ] `C-CF-16` `capability` At a scroll position between two stops the instrument sits partway between two states. `src: Core features, tour rule 3`
- [ ] `C-CF-17` `capability` A stop boundary swaps the headline pair beside the stage. `src: Core features, tour rule 4`
- [ ] `C-CF-18` `capability` A stop boundary rebinds the colour alias to that stop's module family. `src: Core features, tour rule 4`
- [ ] `C-CF-19` `capability` A stop boundary lights that module's arc on the instrument's ring. `src: Core features, tour rule 4`
- [ ] `C-CF-20` `capability` A stop boundary swaps the object inside the ring. `src: Core features, tour rule 4`
- [ ] `C-CF-21` `ui` Scrolling the tour upwards reverses every stop transition exactly. `src: Core features, tour rule 5`
- [ ] `C-CF-22` `ui` The opening headline is split into words, characters. `src: Core features, tour rule 6`
- [ ] `C-CF-23` `ui` The opening headline assembles on load rather than on scroll. `src: Core features, tour rule 6`
- [ ] `C-CF-24` `constraint` The install line sits outside the stage. `src: Core features, tour rule 6`
- [ ] `C-CF-25` `constraint` The secondary call sits outside the stage. `src: Core features, tour rule 6`
- [ ] `C-CF-26` `capability` The install line remains usable when the scene never loads. `src: Core features, tour rule 6`
- [ ] `C-CF-27` `capability` A deep link to a stop fragment lands on that stop without playing the stops between. `src: Core features, tour rule 7`
- [ ] `C-CF-28` `capability` The tour closes with a grid of twelve module tiles above the footer. `src: Core features, tour rule 8`
- [ ] `C-CF-29` `ui` A module tile carries a colour dot in its module's brightest step. `src: Core features, tour rule 8`
- [ ] `C-CF-30` `ui` A module tile carries the module name in the monospace at uppercase. `src: Core features, tour rule 8`
- [ ] `C-CF-31` `capability` A module tile leads to that module's documentation route. `src: Core features, tour rule 8`
- [ ] `C-CF-32` `ui` Pointing at a module tile lights that module's arc on the instrument above. `src: Core features, tour rule 9`
- [ ] `C-CF-33` `ui` On a touch device the lit arc belongs to the module currently in view. `src: Core features, tour rule 10`
- [ ] `C-CF-34` `capability` The instrument renders a perspective scene carrying a camera, a ground plane, a rim light. `src: Core features, instrument rule 1`
- [ ] `C-CF-35` `capability` The instrument carries one object per module. `src: Core features, instrument rule 1`
- [ ] `C-CF-36` `constraint` The ring lives outside the scene as drawn geometry. `src: Core features, instrument rule 2`
- [ ] `C-CF-37` `constraint` The graduation marks live outside the scene as drawn geometry. `src: Core features, instrument rule 2`
- [ ] `C-CF-38` `constraint` The coloured arcs live outside the scene as drawn geometry. `src: Core features, instrument rule 2`
- [ ] `C-CF-39` `capability` The graduation marks are transformed individually from one shared parameter. `src: Core features, instrument rule 3`
- [ ] `C-CF-40` `constraint` The graduation marks are never rotated as a single group. `src: Core features, instrument rule 3`
- [ ] `C-CF-41` `capability` An arc changes only its glow as the tour reaches that module's stop. `src: Core features, instrument rule 4`
- [ ] `C-CF-42` `capability` Scroll position sets the current stop, the interpolation between stops. `src: Core features, instrument rule 5`
- [ ] `C-CF-43` `capability` The pointer adds a small bounded parallax to the instrument. `src: Core features, instrument rule 5`
- [ ] `C-CF-44` `capability` Elapsed time gives the instrument a slow idle rotation. `src: Core features, instrument rule 5`
- [ ] `C-CF-45` `capability` Elapsed time drives the particle drift. `src: Core features, instrument rule 5`
- [ ] `C-CF-46` `capability` The object for the next stop is prepared before the current object leaves the screen. `src: Core features, instrument rule 6`
- [ ] `C-CF-47` `literal` At most `2` objects are resident at any moment. `src: Core features, instrument rule 6`
- [ ] `C-CF-48` `ui` Under a reduced-motion preference the instrument holds one static frame. `src: Core features, instrument rule 7`
- [ ] `C-CF-49` `constraint` Under a reduced-motion preference the instrument is not removed. `src: Core features, instrument rule 7`
- [ ] `C-CF-50` `capability` With the scene unavailable the ring, the marks, the arcs render alone. `src: Core features, instrument rule 7`
- [ ] `C-CF-51` `capability` With the scene unavailable the headlines behave normally. `src: Core features, instrument rule 7`
- [ ] `C-CF-52` `capability` Under a sustained frame-rate drop no further object is loaded. `src: Core features, instrument rule 7`
- [ ] `C-CF-53` `capability` The scene pauses when the tab is hidden. `src: Core features, instrument rule 8`
- [ ] `C-CF-54` `capability` The scene pauses when the tour is scrolled out of view. `src: Core features, instrument rule 8`
- [ ] `C-CF-55` `data` The degradation state of the scene is recorded as an event. `src: Core features, instrument rule 9`
- [ ] `C-CF-56` `capability` The documentation shell renders three columns. `src: Core features, shell rule 1`
- [ ] `C-CF-57` `constraint` The version control appears on documentation routes only. `src: Core features, shell rule 1`
- [ ] `C-CF-58` `constraint` The search field appears on documentation routes only. `src: Core features, shell rule 1`
- [ ] `C-CF-59` `capability` The tree lists sixteen modules in one fixed order. `src: Core features, shell rule 2`
- [ ] `C-CF-60` `data` The tree order is a content property. `src: Core features, shell rule 2`
- [ ] `C-CF-61` `ui` The current module expands in place to reveal its child pages. `src: Core features, shell rule 2`
- [ ] `C-CF-62` `constraint` Only one module is expanded at a time. `src: Core features, shell rule 2`
- [ ] `C-CF-63` `literal` Exactly two modules carry the `NEW` badge. `src: Core features, shell rule 3`
- [ ] `C-CF-64` `data` A badge expires on a stored date. `src: Core features, shell rule 3`
- [ ] `C-CF-65` `constraint` A badge set with no expiry fails the publish. `src: Core features, shell rule 3`
- [ ] `C-CF-66` `capability` The demo column carries one panel per page in the current module. `src: Core features, shell rule 4`
- [ ] `C-CF-67` `ui` A demo panel carries a label strip holding the page name in the monospace at uppercase. `src: Core features, shell rule 4`
- [ ] `C-CF-68` `ui` Demo panels butt against each other with no gap. `src: Core features, shell rule 4`
- [ ] `C-CF-69` `constraint` A demo panel outside the window does not run. `src: Core features, shell rule 5`
- [ ] `C-CF-70` `ui` Scrolling the article to a page's heading makes that page current in the tree. `src: Core features, shell rule 6`
- [ ] `C-CF-71` `ui` Scrolling the article to a page's heading makes its panel current in the demo column. `src: Core features, shell rule 6`
- [ ] `C-CF-72` `ui` Activating a demo panel scrolls the article to that page. `src: Core features, shell rule 6`
- [ ] `C-CF-73` `ui` Activating a tree row scrolls the article to that page. `src: Core features, shell rule 6`
- [ ] `C-CF-74` `ui` Two header steppers move between demo panels directly. `src: Core features, shell rule 6`
- [ ] `C-CF-75` `capability` The version control reads the current version's label. `src: Core features, shell rule 7`
- [ ] `C-CF-76` `capability` The version control lists the published versions newest first. `src: Core features, shell rule 7`
- [ ] `C-CF-77` `capability` Selecting a version switches the whole documentation surface to that snapshot. `src: Core features, shell rule 7`
- [ ] `C-CF-78` `constraint` Selecting a version leaves the address unchanged. `src: Core features, shell rule 7`
- [ ] `C-CF-79` `capability` The version selection is remembered for a visitor across routes. `src: Core features, shell rule 7`
- [ ] `C-CF-80` `capability` The version selection is remembered for a visitor across sessions. `src: Core features, shell rule 7`
- [ ] `C-CF-81` `capability` Switching to a version lacking the current page lands on that module's index. `src: Core features, shell rule 8`
- [ ] `C-CF-82` `constraint` Switching to a version lacking the current page never lands on a not-found page. `src: Core features, shell rule 8`
- [ ] `C-CF-83` `capability` `/documentation` renders the sponsor wall as its article. `src: Core features, shell rule 9`
- [ ] `C-CF-84` `capability` A failing demo panel keeps its label, its ground. `src: Core features, shell rule 10`
- [ ] `C-CF-85` `constraint` A failing demo panel leaves the article unaffected. `src: Core features, shell rule 10`
- [ ] `C-CF-86` `ui` Under a reduced-motion preference a demo panel renders a static first frame. `src: Core features, shell rule 10`
- [ ] `C-CF-87` `capability` An article carries a stable anchor on every subheading. `src: Core features, page rule 1`
- [ ] `C-CF-88` `data` A subheading's anchor is derived from that subheading's own text. `src: Core features, page rule 1`
- [ ] `C-CF-89` `constraint` A subheading's anchor is unique within its page. `src: Core features, page rule 1`
- [ ] `C-CF-90` `capability` The in-section list carries every child page of the current module. `src: Core features, page rule 2`
- [ ] `C-CF-91` `data` The in-section list is generated from the content store. `src: Core features, page rule 2`
- [ ] `C-CF-92` `capability` The pager walks the whole flattened tree across module boundaries. `src: Core features, page rule 3`
- [ ] `C-CF-93` `data` The flattened sequence walks the sixteen modules in tree order. `src: Core features, page rule 3`
- [ ] `C-CF-94` `data` The flattened sequence walks each module's pages in their own order. `src: Core features, page rule 3`
- [ ] `C-CF-95` `capability` The last page of one module is followed by the first page of the next module. `src: Core features, page rule 3`
- [ ] `C-CF-96` `constraint` On the first page of the first module the previous control is absent. `src: Core features, page rule 4`
- [ ] `C-CF-97` `constraint` On the last page of the last module the next control is absent. `src: Core features, page rule 4`
- [ ] `C-CF-98` `ui` A pager control carries the target page's own name. `src: Core features, page rule 4`
- [ ] `C-CF-99` `constraint` A page with no children shows no in-section list. `src: Core features, page rule 5`
- [ ] `C-CF-100` `constraint` A page with no demo shows no placeholder panel. `src: Core features, page rule 5`
- [ ] `C-CF-101` `capability` A deep link to a missing anchor lands at the top of the page. `src: Core features, page rule 6`
- [ ] `C-CF-102` `constraint` A sponsor placement is part of the page layout rather than injected into the prose. `src: Core features, page rule 7`
- [ ] `C-CF-103` `ui` The search control carries a field, a magnifier, two steppers. `src: Core features, search rule 1`
- [ ] `C-CF-104` `ui` Focusing the search control opens the results panel beneath the field. `src: Core features, search rule 1`
- [ ] `C-CF-105` `data` The search index is built ahead of time, one per published version. `src: Core features, search rule 2`
- [ ] `C-CF-106` `contract` The search index is served as a static artifact from the object store. `src: Core features, search rule 2`
- [ ] `C-CF-107` `constraint` The search index is not a query against the database. `src: Core features, search rule 2`
- [ ] `C-CF-108` `constraint` The search index is not built in the browser from the rendered pages. `src: Core features, search rule 2`
- [ ] `C-CF-109` `capability` The search index is fetched on first use of the search control. `src: Core features, search rule 3`
- [ ] `C-CF-110` `constraint` The search index is never fetched on page load. `src: Core features, search rule 3`
- [ ] `C-CF-111` `data` The search index carries one entry per page, one per subheading. `src: Core features, search rule 4`
- [ ] `C-CF-112` `data` A search entry carries its module, its page, its heading path, its anchor, its searchable text. `src: Core features, search rule 4`
- [ ] `C-CF-113` `capability` Code specimens are indexed. `src: Core features, search rule 5`
- [ ] `C-CF-114` `literal` Searching for `remap` finds `utilities/remap-and-clamp`. `src: Core features, search rule 5`
- [ ] `C-CF-115` `capability` Search matching is prefix, substring, case-insensitive. `src: Core features, search rule 6`
- [ ] `C-CF-116` `capability` A title match outranks a heading match. `src: Core features, search rule 6`
- [ ] `C-CF-117` `capability` A heading match outranks a body-text match. `src: Core features, search rule 6`
- [ ] `C-CF-118` `ui` Search results are grouped by module with the module named once. `src: Core features, search rule 6`
- [ ] `C-CF-119` `ui` The matched span is marked within a result row. `src: Core features, search rule 6`
- [ ] `C-CF-120` `constraint` Ranking ties are resolved by the flattened tree order. `src: Core features, search rule 7`
- [ ] `C-CF-121` `constraint` Two runs of the same query return the same result order. `src: Core features, search rule 7`
- [ ] `C-CF-122` `ui` The search steppers move the highlighted result. `src: Core features, search rule 8`
- [ ] `C-CF-123` `ui` The enter key opens the highlighted search result. `src: Core features, search rule 8`
- [ ] `C-CF-124` `ui` The escape key closes the search panel, returning focus to the field. `src: Core features, search rule 8`
- [ ] `C-CF-125` `constraint` An empty search query shows nothing. `src: Core features, search rule 9`
- [ ] `C-CF-126` `ui` A query with no match shows one row stating so, with the query shown back. `src: Core features, search rule 9`
- [ ] `C-CF-127` `capability` With the index unfetchable the search control stays usable. `src: Core features, search rule 10`
- [ ] `C-CF-128` `ui` With the index unfetchable the search control states that search is unavailable. `src: Core features, search rule 10`
- [ ] `C-CF-129` `literal` A query longer than `120` characters is truncated at that bound. `src: Core features, search rule 10`
- [ ] `C-CF-130` `capability` The search index is rebuilt whenever a version is published. `src: Core features, search rule 11`
- [ ] `C-CF-131` `constraint` The curve editor reads no server data. `src: Core features, editor para 1`
- [ ] `C-CF-132` `constraint` The curve editor writes nothing to the server. `src: Core features, editor para 1`
- [ ] `C-CF-133` `capability` The curve editor computes every value in the browser. `src: Core features, editor para 1`
- [ ] `C-CF-134` `ui` The curve editor renders four panels. `src: Core features, editor rule 1`
- [ ] `C-CF-135` `literal` The preset grid carries `10` curve families. `src: Core features, editor rule 2`
- [ ] `C-CF-136` `literal` The preset grid carries `37` curve members. `src: Core features, editor rule 2`
- [ ] `C-CF-137` `literal` The spring family carries the members `default`, `snappy`, `bouncy`, `strong`. `src: Core features, editor rule 2`
- [ ] `C-CF-138` `literal` Eight families carry the members `in`, `out`, `in-out`, `out-in`. `src: Core features, editor rule 2`
- [ ] `C-CF-139` `ui` A preset tile draws its own curve as a miniature plot. `src: Core features, editor rule 2`
- [ ] `C-CF-140` `data` Each curve family binds one colour family. `src: Core features, editor rule 3`
- [ ] `C-CF-141` `ui` The selection signal for a preset tile is a change of asymmetric corner softening. `src: Core features, editor rule 4`
- [ ] `C-CF-142` `capability` The plotted curve is a dense polyline sampled at a fixed step across the domain. `src: Core features, editor rule 5`
- [ ] `C-CF-143` `constraint` The plotted curve is never a single cubic segment. `src: Core features, editor rule 5`
- [ ] `C-CF-144` `ui` Dragging a handle updates the curve continuously. `src: Core features, editor rule 6`
- [ ] `C-CF-145` `constraint` Dragging a handle issues no request. `src: Core features, editor rule 6`
- [ ] `C-CF-146` `constraint` A handle is clamped to the plot's domain. `src: Core features, editor rule 6`
- [ ] `C-CF-147` `capability` The plotted value range may exceed the domain for an overshooting curve. `src: Core features, editor rule 6`
- [ ] `C-CF-148` `constraint` A spring curve carries no draggable handle. `src: Core features, editor rule 7`
- [ ] `C-CF-149` `capability` A spring curve is driven by a bounce, a duration. `src: Core features, editor rule 7`
- [ ] `C-CF-150` `ui` Every handle is focusable from the keyboard. `src: Core features, editor rule 8`
- [ ] `C-CF-151` `ui` An arrow key nudges the focused handle. `src: Core features, editor rule 8`
- [ ] `C-CF-152` `ui` Shift with an arrow key moves the focused handle further. `src: Core features, editor rule 8`
- [ ] `C-CF-153` `ui` The home key moves the focused handle to its lower bound. `src: Core features, editor rule 8`
- [ ] `C-CF-154` `ui` The end key moves the focused handle to its upper bound. `src: Core features, editor rule 8`
- [ ] `C-CF-155` `capability` Every editor parameter carries a numeric field beside its control. `src: Core features, editor rule 8`
- [ ] `C-CF-156` `capability` The reset control returns the current family to its defaults. `src: Core features, editor rule 9`
- [ ] `C-CF-157` `ui` The preview runs four cells, one animating, three ghosted at successive offsets. `src: Core features, editor rule 10`
- [ ] `C-CF-158` `ui` The onion skin shows the trail of previous positions. `src: Core features, editor rule 10`
- [ ] `C-CF-159` `ui` A tick strip below the plot marks one mark per sampled step. `src: Core features, editor rule 10`
- [ ] `C-CF-160` `capability` The tick strip is drawn from the same sample set as the curve. `src: Core features, editor rule 10`
- [ ] `C-CF-161` `ui` Duration, loop delay, two opacity endpoints are each a slider paired with a numeric field. `src: Core features, editor rule 11`
- [ ] `C-CF-162` `ui` An editor readout is drawn in the seven-segment form. `src: Core features, editor rule 11`
- [ ] `C-CF-163` `literal` The export panel carries the tabs `CSS`, `JS`. `src: Core features, editor rule 12`
- [ ] `C-CF-164` `capability` Each export tab carries a short form naming only the curve. `src: Core features, editor rule 12`
- [ ] `C-CF-165` `capability` Each export tab carries a full form carrying the import, the call. `src: Core features, editor rule 12`
- [ ] `C-CF-166` `capability` Every export is generated in the browser from the current parameters. `src: Core features, editor rule 12`
- [ ] `C-CF-167` `constraint` No export is fetched from the server. `src: Core features, editor rule 12`
- [ ] `C-CF-168` `capability` One sampler feeds the plot, the tick strip, the preview, the exported code. `src: Core features, editor rule 13`
- [ ] `C-CF-169` `literal` A control point is exported at `3` decimal places. `src: Core features, editor rule 14`
- [ ] `C-CF-170` `literal` A bounce is exported at `2` decimal places. `src: Core features, editor rule 14`
- [ ] `C-CF-171` `literal` A duration is exported at `2` decimal places. `src: Core features, editor rule 14`
- [ ] `C-CF-172` `literal` A control-point family carries the address keys `family`, `member`, `p1x`, `p1y`, `p2x`, `p2y`. `src: Core features, editor rule 15`
- [ ] `C-CF-173` `literal` The spring family carries the address keys `family`, `member`, `bounce`, `duration`. `src: Core features, editor rule 15`
- [ ] `C-CF-174` `capability` Pasting an editor address reproduces the exact curve. `src: Core features, editor rule 15`
- [ ] `C-CF-175` `constraint` The editor address is replaced rather than pushed onto history. `src: Core features, editor rule 16`
- [ ] `C-CF-176` `capability` An absent editor address falls back to the first family's default. `src: Core features, editor rule 17`
- [ ] `C-CF-177` `capability` An invalid editor address falls back to the first family's default without an error. `src: Core features, editor rule 17`
- [ ] `C-CF-178` `ui` Under a reduced-motion preference the preview holds a static frame. `src: Core features, editor rule 18`
- [ ] `C-CF-179` `ui` Under a reduced-motion preference the onion skin still renders. `src: Core features, editor rule 18`
- [ ] `C-CF-180` `literal` The course page writes to the list `course_waitlist`. `src: Core features, subscription rule 1`
- [ ] `C-CF-181` `literal` The footer pair writes to the list `newsletter`. `src: Core features, subscription rule 1`
- [ ] `C-CF-182` `constraint` Joining one list is not consent to the other list. `src: Core features, subscription rule 1`
- [ ] `C-CF-183` `data` The same address on both lists is two rows. `src: Core features, subscription rule 1`
- [ ] `C-CF-184` `capability` The subscription form works without any third-party script. `src: Core features, subscription rule 2`
- [ ] `C-CF-185` `capability` The subscription form works with scripting disabled. `src: Core features, subscription rule 2`
- [ ] `C-CF-186` `contract` The subscription form posts form-encoded fields to the app's own endpoint. `src: Core features, subscription rule 2`
- [ ] `C-CF-187` `capability` A submitted address creates a `pending` row. `src: Core features, subscription rule 3`
- [ ] `C-CF-188` `capability` A submitted address queues a confirmation message. `src: Core features, subscription rule 3`
- [ ] `C-CF-189` `capability` Opening the confirmation link consumes the token, moving the row to `confirmed`. `src: Core features, subscription rule 3`
- [ ] `C-CF-190` `capability` The form reports that a confirmation has been sent. `src: Core features, subscription rule 4`
- [ ] `C-CF-191` `constraint` The form never reports that the visitor is subscribed. `src: Core features, subscription rule 4`
- [ ] `C-CF-192` `literal` A confirmation token carries at least `128` bits from a cryptographic source. `src: Core features, subscription rule 5`
- [ ] `C-CF-193` `constraint` A confirmation token is stored only as a digest. `src: Core features, subscription rule 5`
- [ ] `C-CF-194` `literal` A confirmation token expires `7` days after issue. `src: Core features, subscription rule 5`
- [ ] `C-CF-195` `constraint` A confirmation token works exactly once. `src: Core features, subscription rule 5`
- [ ] `C-CF-196` `capability` A second use of a consumed token reports the address as already confirmed. `src: Core features, subscription rule 5`
- [ ] `C-CF-197` `capability` An expired token lands on a page offering to send a new one. `src: Core features, subscription rule 5`
- [ ] `C-CF-198` `constraint` The confirmation link is the only place a token appears. `src: Core features, subscription rule 5`
- [ ] `C-CF-199` `capability` Re-submission is idempotent by the address together with the list. `src: Core features, subscription rule 6`
- [ ] `C-CF-200` `capability` Submitting an address already `pending` refreshes the row, sending a new confirmation. `src: Core features, subscription rule 6`
- [ ] `C-CF-201` `capability` Submitting an address already `confirmed` reports success. `src: Core features, subscription rule 6`
- [ ] `C-CF-202` `constraint` Submitting an address already `confirmed` sends no message. `src: Core features, subscription rule 6`
- [ ] `C-CF-203` `capability` Submitting an address previously `unsubscribed` begins a new pending cycle. `src: Core features, subscription rule 6`
- [ ] `C-CF-204` `constraint` Submitting an address that `complained` sends no message. `src: Core features, subscription rule 6`
- [ ] `C-CF-205` `constraint` Submitting an address that `bounced` sends no message. `src: Core features, subscription rule 6`
- [ ] `C-CF-206` `constraint` The same address submitted twice in quick succession queues one message. `src: Core features, subscription rule 6`
- [ ] `C-CF-207` `constraint` A rejection is reported identically to the submitter whatever the reason. `src: Core features, subscription rule 7`
- [ ] `C-CF-208` `capability` The server checks presence, shape of a submitted address. `src: Core features, subscription rule 8`
- [ ] `C-CF-209` `data` A submitted address is trimmed, lowercased for comparison. `src: Core features, subscription rule 8`
- [ ] `C-CF-210` `data` A submitted address is stored as submitted. `src: Core features, subscription rule 8`
- [ ] `C-CF-211` `constraint` A length bound is enforced before any parsing of a submitted address. `src: Core features, subscription rule 8`
- [ ] `C-CF-212` `constraint` A disposable address is accepted rather than blocked. `src: Core features, subscription rule 8`
- [ ] `C-CF-213` `constraint` A role address is accepted rather than blocked. `src: Core features, subscription rule 8`
- [ ] `C-CF-214` `literal` At most `3` submissions per address per hour are accepted. `src: Core features, subscription rule 9`
- [ ] `C-CF-215` `literal` At most `20` submissions per network origin per hour are accepted. `src: Core features, subscription rule 9`
- [ ] `C-CF-216` `literal` At most `2` confirmation resends per address per day are sent. `src: Core features, subscription rule 9`
- [ ] `C-CF-217` `literal` A filled decoy field named `company_website` refuses the submission. `src: Core features, subscription rule 9`
- [ ] `C-CF-218` `literal` A submission arriving less than `2` seconds after the form was served is refused. `src: Core features, subscription rule 9`
- [ ] `C-CF-219` `capability` Repeated rejection from one origin lengthens that origin's window. `src: Core features, subscription rule 9`
- [ ] `C-CF-220` `constraint` No visible puzzle is ever presented to a submitter. `src: Core features, subscription rule 9`
- [ ] `C-CF-221` `literal` A ceiling of `200` queued messages per hour raises an alert. `src: Core features, subscription rule 10`
- [ ] `C-CF-222` `capability` A delivered callback is recorded against its subscriber. `src: Core features, subscription rule 11`
- [ ] `C-CF-223` `capability` A hard-bounce callback moves the row to `bounced`. `src: Core features, subscription rule 11`
- [ ] `C-CF-224` `capability` A soft-bounce callback is retried before the row becomes `bounced`. `src: Core features, subscription rule 11`
- [ ] `C-CF-225` `capability` A complaint callback moves the row to `complained` permanently. `src: Core features, subscription rule 11`
- [ ] `C-CF-226` `capability` An unsubscribe callback moves the row to `unsubscribed`. `src: Core features, subscription rule 11`
- [ ] `C-CF-227` `contract` Every provider callback is checked against its signature. `src: Core features, subscription rule 11`
- [ ] `C-CF-228` `constraint` A callback with an invalid signature changes nothing. `src: Core features, subscription rule 11`
- [ ] `C-CF-229` `constraint` A repeated provider event identifier changes nothing the first arrival did not. `src: Core features, subscription rule 11`
- [ ] `C-CF-230` `capability` Callbacks arriving out of order are applied by the state each carries. `src: Core features, subscription rule 11`
- [ ] `C-CF-231` `capability` The unsubscribe link works once. `src: Core features, subscription rule 12`
- [ ] `C-CF-232` `data` A `pending` row never confirmed is deleted after its token expiry plus a grace period. `src: Core features, subscription rule 13`
- [ ] `C-CF-233` `data` An `unsubscribed` row keeps the address as a digest only. `src: Core features, subscription rule 13`
- [ ] `C-CF-234` `data` A `complained` row keeps its digest permanently. `src: Core features, subscription rule 13`
- [ ] `C-CF-235` `data` A rate-limit fingerprint is kept only as long as its window. `src: Core features, subscription rule 13`
- [ ] `C-CF-236` `constraint` The subscription form collects one field. `src: Core features, subscription rule 14`
- [ ] `C-CF-237` `data` A sponsor tier is an ordered row rather than a hard-coded group. `src: Core features, funding rule 1`
- [ ] `C-CF-238` `data` A sponsor tier carries its slug, its display name, its rank, its placement set, its mark size. `src: Core features, funding rule 1`
- [ ] `C-CF-239` `literal` The seeded tier `upper` sits at rank `1`. `src: Core features, funding rule 2`
- [ ] `C-CF-240` `literal` The seeded tier `lower` sits at rank `2`. `src: Core features, funding rule 2`
- [ ] `C-CF-241` `capability` A sponsor card appears on a surface only when its tier's placement set names that surface. `src: Core features, funding rule 2`
- [ ] `C-CF-242` `ui` The last card in every tier group is the recruitment card. `src: Core features, funding rule 3`
- [ ] `C-CF-243` `constraint` The recruitment card is present whether or not the tier is full. `src: Core features, funding rule 3`
- [ ] `C-CF-244` `capability` Ordering within a tier follows each sponsor's stored position. `src: Core features, funding rule 4`
- [ ] `C-CF-245` `constraint` Ordering within a tier never follows the order a fetch returned. `src: Core features, funding rule 4`
- [ ] `C-CF-246` `capability` The roster is reconciled on a schedule, server-side. `src: Core features, funding rule 5`
- [ ] `C-CF-247` `constraint` The roster is never fetched from the browser at render time. `src: Core features, funding rule 5`
- [ ] `C-CF-248` `contract` Every sponsor mark is stored as a first-party object. `src: Core features, funding rule 5`
- [ ] `C-CF-249` `capability` With the roster source unavailable the last good roster is served. `src: Core features, funding rule 6`
- [ ] `C-CF-250` `data` The age of the served roster is recorded. `src: Core features, funding rule 6`
- [ ] `C-CF-251` `data` A sponsor absent from a fetch is marked inactive by its end date. `src: Core features, funding rule 7`
- [ ] `C-CF-252` `constraint` A sponsor absent from a fetch is never deleted. `src: Core features, funding rule 7`
- [ ] `C-CF-253` `ui` A sponsor with no mark renders its name in place of the mark. `src: Core features, funding rule 8`
- [ ] `C-CF-254` `constraint` A sponsor with no mark never renders a broken image. `src: Core features, funding rule 8`
- [ ] `C-CF-255` `ui` An empty tier renders the recruitment card with no tier heading above. `src: Core features, funding rule 9`
- [ ] `C-CF-256` `constraint` The site takes no payment. `src: Core features, funding rule 10`
- [ ] `C-CF-257` `ui` A filled advertising slot renders at its reserved size. `src: Core features, advertising rule 1`
- [ ] `C-CF-258` `ui` An empty advertising slot collapses to nothing. `src: Core features, advertising rule 2`
- [ ] `C-CF-259` `constraint` An empty advertising slot renders no placeholder. `src: Core features, advertising rule 2`
- [ ] `C-CF-260` `constraint` The site makes no attempt to detect a blocked advertising slot. `src: Core features, advertising rule 3`
- [ ] `C-CF-261` `ui` A slow advertising slot holds its reserved space. `src: Core features, advertising rule 4`
- [ ] `C-CF-262` `constraint` Advertising content runs in a bounded context that cannot reach the document. `src: Core features, advertising rule 5`
- [ ] `C-CF-263` `capability` A version is built in the `draft` state before promotion. `src: Core features, pipeline rule 1`
- [ ] `C-CF-264` `constraint` A visitor never sees a half-published version. `src: Core features, pipeline rule 1`
- [ ] `C-CF-265` `constraint` At most one version is current at any moment. `src: Core features, pipeline rule 2`
- [ ] `C-CF-266` `contract` A second attempt to mark a version current is refused by the database. `src: Core features, pipeline rule 2`
- [ ] `C-CF-267` `capability` A publish refuses when the flattened sequence carries a gap. `src: Core features, pipeline rule 3`
- [ ] `C-CF-268` `capability` A publish refuses when two modules share a position. `src: Core features, pipeline rule 3`
- [ ] `C-CF-269` `capability` A publish refuses when a module names a colour family outside the twenty-one. `src: Core features, pipeline rule 3`
- [ ] `C-CF-270` `capability` A publish refuses when a page's anchors are not unique within the page. `src: Core features, pipeline rule 3`
- [ ] `C-CF-271` `capability` A publish refuses when an internal link targets a missing page. `src: Core features, pipeline rule 3`
- [ ] `C-CF-272` `capability` A publish refuses when a page references a demo that does not exist. `src: Core features, pipeline rule 3`
- [ ] `C-CF-273` `capability` A publish refuses when a badge is set with no expiry. `src: Core features, pipeline rule 3`
- [ ] `C-CF-274` `capability` A publish refuses when the built index lacks a page in the version. `src: Core features, pipeline rule 3`
- [ ] `C-CF-275` `capability` A publish refuses when a module holds no page. `src: Core features, pipeline rule 3`
- [ ] `C-CF-276` `capability` A failed validation discards the draft snapshot. `src: Core features, pipeline rule 5`
- [ ] `C-CF-277` `capability` Promotion purges the caches for the promoted version. `src: Core features, pipeline rule 6`
- [ ] `C-CF-278` `capability` Promotion leaves the previous snapshot readable through the version control. `src: Core features, pipeline rule 6`
- [ ] `C-CF-279` `capability` A draft version is viewable at its own preview key. `src: Core features, pipeline rule 7`
- [ ] `C-CF-280` `constraint` A draft version appears in no sitemap. `src: Core features, pipeline rule 7`
- [ ] `C-CF-281` `constraint` A draft version appears in no search result. `src: Core features, pipeline rule 7`
- [ ] `C-CF-282` `constraint` A draft version appears in no internal link on a published page. `src: Core features, pipeline rule 7`
- [ ] `C-CF-283` `constraint` A signed-out caller reaches no part of a draft version. `src: Core features, pipeline rule 7`
- [ ] `C-CF-284` `data` The route list is derived from the content store. `src: Core features, pipeline rule 8`
- [ ] `C-CF-285` `constraint` The route list is never derived from the rendered navigation. `src: Core features, pipeline rule 8`
- [ ] `C-CF-286` `capability` Every route carries the same header, the same footer. `src: Core features, chrome rule 1`
- [ ] `C-CF-287` `constraint` The header never waits on a fetch. `src: Core features, chrome rule 1`
- [ ] `C-CF-288` `constraint` The footer never waits on a fetch. `src: Core features, chrome rule 1`
- [ ] `C-CF-289` `capability` An address that does not resolve renders the site's own not-found page. `src: Core features, chrome rule 2`
- [ ] `C-CF-290` `contract` An address that does not resolve answers not-found. `src: Core features, chrome rule 2`
- [ ] `C-CF-291` `constraint` No address renders the tour with a success status. `src: Core features, chrome rule 2`
- [ ] `C-CF-292` `ui` The not-found page carries a heading, one line of explanation, three ways out. `src: Core features, chrome rule 2`
- [ ] `C-CF-293` `capability` A failed documentation address offers the search control with the failed segment prefilled. `src: Core features, chrome rule 3`
- [ ] `C-CF-294` `contract` The server error page answers server-error. `src: Core features, chrome rule 4`
- [ ] `C-CF-295` `ui` The server error page carries a retry control. `src: Core features, chrome rule 4`
- [ ] `C-CF-296` `constraint` The server error page offers no search control. `src: Core features, chrome rule 4`
- [ ] `C-CF-297` `capability` Every internal link on every published route resolves to a route that answers. `src: Core features, chrome rule 5`
- [ ] `C-CF-298` `capability` A privacy page is reachable from the footer of every page. `src: Core features, chrome rule 6`
- [ ] `C-CF-299` `capability` The privacy page states that an address on a list plus its confirmation state is stored. `src: Core features, chrome rule 6`
- [ ] `C-CF-300` `capability` The privacy page states that a count of page views by route is stored. `src: Core features, chrome rule 6`
- [ ] `C-CF-301` `capability` The privacy page states that no name, no company, no behavioural profile is kept. `src: Core features, chrome rule 6`
- [ ] `C-CF-302` `capability` The privacy page states how a visitor asks for an address to be erased. `src: Core features, chrome rule 6`
- [ ] `C-CF-303` `capability` A first-time visitor is asked once about non-essential storage. `src: Core features, chrome rule 7`
- [ ] `C-CF-304` `ui` The storage bar is anchored to the foot of the page. `src: Core features, chrome rule 7`
- [ ] `C-CF-305` `constraint` The storage bar is never a modal. `src: Core features, chrome rule 7`
- [ ] `C-CF-306` `ui` Refusing non-essential storage is exactly as easy as accepting. `src: Core features, chrome rule 7`
- [ ] `C-CF-307` `capability` The storage answer survives a reload. `src: Core features, chrome rule 7`
- [ ] `C-CF-308` `constraint` The remembered documentation version is withheld until the storage answer is yes. `src: Core features, chrome rule 7`
- [ ] `C-CF-309` `constraint` The local page-view record is withheld until the storage answer is yes. `src: Core features, chrome rule 7`
- [ ] `C-CF-310` `constraint` An analytics event is dropped rather than queued until the storage answer is yes. `src: Core features, chrome rule 7`
- [ ] `C-CF-311` `data` A page view is recorded with its route, the moment of the view. `src: Core features, chrome rule 8`
- [ ] `C-CF-312` `role` The page-view log is readable by the maintainer alone. `src: Core features, chrome rule 8`
- [ ] `C-CF-313` `constraint` Nothing is sent to any outside address. `src: Core features, chrome rule 8`
- [ ] `C-CF-314` `data` A route-viewed event carries the route, the documentation version, the viewport class. `src: Core features, chrome rule 9`
- [ ] `C-CF-315` `data` A tour-stop event carries the stop index, the furthest stop reached in the session. `src: Core features, chrome rule 9`
- [ ] `C-CF-316` `data` A specimen-copied event carries the route, the page, the block. `src: Core features, chrome rule 9`
- [ ] `C-CF-317` `data` A search event carries the query length, the result count. `src: Core features, chrome rule 9`
- [ ] `C-CF-318` `constraint` A search event never carries the query text. `src: Core features, chrome rule 9`
- [ ] `C-CF-319` `data` A search-result-activated event carries the result rank. `src: Core features, chrome rule 9`
- [ ] `C-CF-320` `data` A curve-changed event carries the family, the member. `src: Core features, chrome rule 9`
- [ ] `C-CF-321` `constraint` A curve-changed event never carries a parameter value. `src: Core features, chrome rule 9`
- [ ] `C-CF-322` `data` An export-copied event carries the language, the form, the family. `src: Core features, chrome rule 9`
- [ ] `C-CF-323` `data` A subscription event carries the list, the source route, the outcome class. `src: Core features, chrome rule 9`
- [ ] `C-CF-324` `data` A funding-call event carries its placement. `src: Core features, chrome rule 9`
- [ ] `C-CF-325` `data` A demo-failure event carries the page, the error class. `src: Core features, chrome rule 9`
- [ ] `C-CF-326` `constraint` The text of a search query is never recorded anywhere. `src: Core features, chrome rule 10`
- [ ] `C-CF-327` `constraint` The visitor identifier is scoped to a session. `src: Core features, chrome rule 11`
- [ ] `C-CF-328` `constraint` No persistent per-visitor identifier is written. `src: Core features, chrome rule 11`
- [ ] `C-CF-329` `constraint` No cross-site identifier is written. `src: Core features, chrome rule 11`
- [ ] `C-CF-330` `constraint` Analytics never block an interaction. `src: Core features, chrome rule 12`
- [ ] `C-CF-331` `capability` Analytics are batched, flushed on a timer, flushed when the page is hidden. `src: Core features, chrome rule 12`
- [ ] `C-CF-332` `capability` A failing analytics call fails silently. `src: Core features, chrome rule 12`
- [ ] `C-CF-333` `ui` A specimen block carries its source in the monospace on a recessed ground. `src: Core features, specimen rule 1`
- [ ] `C-CF-334` `constraint` A specimen block is themed from the code palette rather than the section alias. `src: Core features, specimen rule 1`
- [ ] `C-CF-335` `ui` A long specimen line scrolls sideways inside its block. `src: Core features, specimen rule 2`
- [ ] `C-CF-336` `constraint` A long specimen line never widens the page. `src: Core features, specimen rule 2`
- [ ] `C-CF-337` `ui` A specimen block's text is selectable. `src: Core features, specimen rule 3`
- [ ] `C-CF-338` `constraint` Selecting a specimen's text does not trigger the copy control. `src: Core features, specimen rule 3`
- [ ] `C-CF-339` `constraint` A specimen is rendered as text rather than as markup. `src: Core features, specimen rule 4`
- [ ] `C-CF-340` `constraint` A specimen is never executed by the page that renders the specimen. `src: Core features, specimen rule 4`
- [ ] `C-CF-341` `ui` The copy control sits at the specimen block's top right behind a backdrop blur. `src: Core features, specimen rule 5`
- [ ] `C-CF-342` `ui` The copy control swaps to a confirmation mark, then reverts. `src: Core features, specimen rule 5`
- [ ] `C-CF-343` `capability` The copy control copies the specimen's source text. `src: Core features, specimen rule 6`
- [ ] `C-CF-344` `constraint` The copy control never copies the rendered highlight markup. `src: Core features, specimen rule 6`
- [ ] `C-CF-345` `capability` The copy control strips a trailing newline. `src: Core features, specimen rule 6`
- [ ] `C-CF-346` `capability` The copy control preserves indentation exactly. `src: Core features, specimen rule 6`
- [ ] `C-CF-347` `ui` The copy confirmation is announced to assistive technology. `src: Core features, specimen rule 7`
- [ ] `C-CF-348` `capability` A refused clipboard selects the block's text instead. `src: Core features, specimen rule 8`
- [ ] `C-CF-349` `ui` On a touch device the copy control is permanently visible. `src: Core features, specimen rule 9`
- [ ] `C-CF-350` `capability` The install line is a specimen carrying its own copy control. `src: Core features, specimen rule 10`
- [ ] `C-CF-351` `data` A demo carries its own source, its parameters, a poster seed. `src: Core features, demo rule 1`
- [ ] `C-CF-352` `data` A demo is stored with its own version. `src: Core features, demo rule 1`
- [ ] `C-CF-353` `constraint` A demo runs in a bounded context that cannot reach the host document. `src: Core features, demo rule 2`
- [ ] `C-CF-354` `constraint` A demo cannot navigate. `src: Core features, demo rule 2`
- [ ] `C-CF-355` `constraint` A demo cannot write to storage. `src: Core features, demo rule 2`
- [ ] `C-CF-356` `constraint` A demo cannot reach the network beyond its own assets. `src: Core features, demo rule 2`
- [ ] `C-CF-357` `capability` A demo exceeding a time bound is stopped. `src: Core features, demo rule 3`
- [ ] `C-CF-358` `capability` A demo exceeding a memory bound is stopped. `src: Core features, demo rule 3`
- [ ] `C-CF-359` `capability` A demo that cannot run shows its generated poster. `src: Core features, demo rule 4`
- [ ] `C-CF-360` `constraint` A poster is generated deterministically from the demo's own seed. `src: Core features, demo rule 4`
- [ ] `C-CF-361` `literal` The job set carries `10` jobs. `src: Core features, jobs rule 1`
- [ ] `C-CF-362` `literal` The job names are `send_confirmation`, `send_welcome`, `process_mail_events`, `sync_sponsor_roster`, `sweep_expired_subscriptions`, `expire_badges`, `rebuild_index`, `purge_caches`, `warm_caches`, `check_roster_freshness`. `src: Core features, jobs rule 1`
- [ ] `C-CF-363` `contract` Job delivery is at least once. `src: Core features, jobs rule 2`
- [ ] `C-CF-364` `capability` A send job is keyed by its subscription. `src: Core features, jobs rule 2`
- [ ] `C-CF-365` `capability` A callback job is keyed by the provider's event identifier. `src: Core features, jobs rule 2`
- [ ] `C-CF-366` `capability` A retry uses exponential backoff with jitter. `src: Core features, jobs rule 3`
- [ ] `C-CF-367` `literal` A job is attempted at most `5` times. `src: Core features, jobs rule 3`
- [ ] `C-CF-368` `capability` An exhausted job moves to a dead-letter store. `src: Core features, jobs rule 3`
- [ ] `C-CF-369` `constraint` An exhausted job is never discarded. `src: Core features, jobs rule 3`
- [ ] `C-CF-370` `capability` A deterministically failing job is dead-lettered rather than retried forever. `src: Core features, jobs rule 3`
- [ ] `C-CF-371` `capability` The confirmation send is enqueued within the request before the response. `src: Core features, jobs rule 5`
- [ ] `C-CF-372` `constraint` The response does not wait for the confirmation send. `src: Core features, jobs rule 5`
- [ ] `C-CF-373` `capability` With the provider unavailable the job holds in the queue, the row staying `pending`. `src: Core features, jobs rule 5`
- [ ] `C-CF-374` `constraint` No submission is lost when the provider is unavailable. `src: Core features, jobs rule 5`
- [ ] `C-CF-375` `capability` A scheduled job takes a lock. `src: Core features, jobs rule 6`
- [ ] `C-CF-376` `constraint` Two runs of one scheduled job cannot overlap. `src: Core features, jobs rule 6`
- [ ] `C-CF-377` `constraint` A missed scheduled run is not backfilled. `src: Core features, jobs rule 6`
- [ ] `C-CF-378` `capability` The expiry sweep counts what would be deleted before deleting. `src: Core features, jobs rule 7`
- [ ] `C-CF-379` `literal` The expiry sweep refuses to run when the count exceeds `500` rows. `src: Core features, jobs rule 7`
- [ ] `C-CF-380` `capability` The badge job clears a `NEW` badge whose expiry has passed. `src: Core features, jobs rule 8`
- [ ] `C-CF-381` `literal` The roster freshness job alerts when the roster is older than `24` hours. `src: Core features, jobs rule 9`
- [ ] `C-CF-382` `data` Twelve operational signals are watched. `src: Core features, jobs rule 10`
- [ ] `C-CF-383` `capability` A confirmation queue that is not draining raises the alert ranked above every other alert. `src: Core features, jobs rule 11`

## C-UF User flow

- [ ] `C-UF-01` `contract` The tour is served at `/`. `src: User flow route table row 1`
- [ ] `C-UF-02` `contract` The documentation landing route is `/documentation`. `src: User flow route table row 2`
- [ ] `C-UF-03` `contract` A module route is `/documentation/<module>`. `src: User flow route table row 3`
- [ ] `C-UF-04` `contract` A page route is `/documentation/<module>/<page>`. `src: User flow route table row 4`
- [ ] `C-UF-05` `contract` The curve editor is served at `/easing-editor`. `src: User flow route table row 5`
- [ ] `C-UF-06` `contract` The course waiting list is served at `/learn`. `src: User flow route table row 6`
- [ ] `C-UF-07` `contract` The privacy page is served at `/privacy`. `src: User flow route table row 7`
- [ ] `C-UF-08` `contract` A confirmation link lands on `/confirm`. `src: User flow route table row 8`
- [ ] `C-UF-09` `contract` An unsubscribe link lands on `/unsubscribe`. `src: User flow route table row 9`
- [ ] `C-UF-10` `contract` The sitemap is served at `/sitemap.xml`. `src: User flow route table row 10`
- [ ] `C-UF-11` `contract` The studio is served at `/studio`. `src: User flow route table row 12`
- [ ] `C-UF-12` `contract` A draft version is previewed at `/preview/<preview_key>`. `src: User flow route table row 13`
- [ ] `C-UF-13` `constraint` An address carries no trailing slash. `src: User flow, addressing rules`
- [ ] `C-UF-14` `constraint` An address is lower case, kebab within a segment. `src: User flow, addressing rules`
- [ ] `C-UF-15` `constraint` An address goes at most three segments below the origin. `src: User flow, addressing rules`
- [ ] `C-UF-16` `constraint` The documentation version is never a path segment. `src: User flow, addressing rules`
- [ ] `C-UF-17` `constraint` Fragment addressing is used by the tour alone. `src: User flow, addressing rules`
- [ ] `C-UF-18` `constraint` Query addressing is used by the curve editor alone. `src: User flow, addressing rules`
- [ ] `C-UF-19` `capability` A signed-out request for the studio is rejected, sending the caller to the sign-in page. `src: User flow, entry paragraph`
- [ ] `C-UF-20` `constraint` A rejected studio request does not serve the protected content. `src: User flow, entry paragraph`
- [ ] `C-UF-21` `ui` A visitor copies the install line before the stage beside the line has filled. `src: User flow, install journey`
- [ ] `C-UF-22` `ui` A visitor reads the whole manual front to back using the pager alone. `src: User flow, read journey`
- [ ] `C-UF-23` `ui` A visitor reaches a search result using the stepper rather than the pointer. `src: User flow, find journey`
- [ ] `C-UF-24` `ui` A visitor lands on a search result page with its module current in the tree. `src: User flow, find journey`
- [ ] `C-UF-25` `ui` A visitor switching version keeps the address unchanged. `src: User flow, older version journey`
- [ ] `C-UF-26` `ui` A visitor finds a spring preset carrying no handle. `src: User flow, curve journey`
- [ ] `C-UF-27` `ui` A visitor dragging a bezier handle sees the plot, the tick strip, the preview, the export change together. `src: User flow, curve journey`
- [ ] `C-UF-28` `ui` A visitor submitting a third time is thanked, with nothing sent. `src: User flow, list journey`
- [ ] `C-UF-29` `ui` The maintainer publishes a corrected draft, switching the documentation surface in one step. `src: User flow, publish journey`
- [ ] `C-UF-30` `capability` The content store falling back to a cached copy records the age of that copy. `src: User flow, degraded states paragraph`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The first moment reads as a precision instrument for making things move. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The documentation reads quiet, dense, organised. `src: UI/UX notes para 2`
- [ ] `C-UX-03` `ui` The editor shows a result beside its cause with nothing waiting. `src: UI/UX notes para 2`
- [ ] `C-UX-04` `ui` The palette carries twenty-one families of eight steps each. `src: UI/UX notes para 3`
- [ ] `C-UX-05` `ui` Step one of a family is its most saturated, lightest form. `src: UI/UX notes para 3`
- [ ] `C-UX-06` `ui` Step eight of a family reads as absence against the page ground. `src: UI/UX notes para 3`
- [ ] `C-UX-07` `ui` Two structural families carry surfaces, text separately. `src: UI/UX notes para 3`
- [ ] `C-UX-08` `ui` A documentation section rebinds one alias of eight steps to one family. `src: UI/UX notes para 4`
- [ ] `C-UX-09` `constraint` No component below a section boundary names a colour family directly. `src: UI/UX notes para 4`
- [ ] `C-UX-10` `ui` Code blocks are themed outside the family system. `src: UI/UX notes para 5`
- [ ] `C-UX-11` `ui` Everything that is not code is set in a variable grotesque carrying a wide axis of stroke thickness. `src: UI/UX notes para 6`
- [ ] `C-UX-12` `ui` Code labels are set in a monospace carrying a true italic. `src: UI/UX notes para 6`
- [ ] `C-UX-13` `ui` A numeric readout in the editor is drawn as seven strokes per digit. `src: UI/UX notes para 6`
- [ ] `C-UX-14` `ui` Every headline sets at a line height below its own font size. `src: UI/UX notes para 6`
- [ ] `C-UX-15` `ui` Space, type are separate ladders. `src: UI/UX notes para 7`
- [ ] `C-UX-16` `ui` A preset tile's asymmetric corner softening is the grid's selection signal. `src: UI/UX notes para 7`
- [ ] `C-UX-17` `ui` The joined field pair is softened only on its outer edges. `src: UI/UX notes para 7`
- [ ] `C-UX-18` `ui` Motion runs on five curves with no sixth. `src: UI/UX notes para 8`
- [ ] `C-UX-19` `ui` A colour change runs about twice as fast as anything that travels. `src: UI/UX notes para 8`
- [ ] `C-UX-20` `constraint` No blanket rule transitions every property. `src: UI/UX notes para 8`
- [ ] `C-UX-21` `ui` Under a preference against movement nothing is scroll-driven, nothing staggers. `src: UI/UX notes para 9`
- [ ] `C-UX-22` `ui` The layout archetype is a top navigation carrying the wordmark on the left. `src: UI/UX notes para 10`
- [ ] `C-UX-23` `ui` Each page leads with one primary action, visually distinct from every secondary one. `src: UI/UX notes para 10`
- [ ] `C-UX-24` `ui` A control draws resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes para 11`
- [ ] `C-UX-25` `ui` The escape key closes any open panel, returning focus to the control that opened the panel. `src: UI/UX notes para 11`
- [ ] `C-UX-26` `ui` The focus state is louder than the pointed-at state. `src: UI/UX notes para 11`
- [ ] `C-UX-27` `ui` Every hover effect carries a non-hover equivalent on a touch device. `src: UI/UX notes para 12`
- [ ] `C-UX-28` `ui` A split headline carries the intact original string as its accessible name. `src: UI/UX notes para 13`
- [ ] `C-UX-29` `ui` Every stop's text sits in the document at all times. `src: UI/UX notes para 13`
- [ ] `C-UX-30` `ui` A stop change is not announced. `src: UI/UX notes para 13`
- [ ] `C-UX-31` `ui` Every editor handle carries a role, a value, a name. `src: UI/UX notes para 13`
- [ ] `C-UX-32` `ui` A value change is announced on the numeric field rather than on every drag frame. `src: UI/UX notes para 13`
- [ ] `C-UX-33` `ui` A skip link sits first in the document. `src: UI/UX notes para 13`
- [ ] `C-UX-34` `ui` The tree, the demo column, the article are distinct named landmarks. `src: UI/UX notes para 13`
- [ ] `C-UX-35` `ui` The current page is marked as current rather than merely coloured. `src: UI/UX notes para 13`
- [ ] `C-UX-36` `ui` Body text meets the WCAG AA contrast bar against its background. `src: UI/UX notes para 13`
- [ ] `C-UX-37` `ui` Every foreground pairing is measured rather than assumed. `src: UI/UX notes para 13`
- [ ] `C-UX-38` `ui` The layout holds at one primary turning point with refinements above, below. `src: UI/UX notes para 14`
- [ ] `C-UX-39` `ui` At a narrow viewport the current demonstration survives as a pinned panel. `src: UI/UX notes para 14`
- [ ] `C-UX-40` `ui` At every width the document never scrolls sideways. `src: UI/UX notes para 14`
- [ ] `C-UX-41` `ui` Every touch target stays at least a comfortable fingertip across. `src: UI/UX notes para 14`
- [ ] `C-UX-42` `ui` Vertical sizing follows the dynamic viewport height. `src: UI/UX notes para 14`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Documentation routes are rendered ahead of time, served as complete documents. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The frontend is SvelteKit. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The backend is FastAPI. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` The datastore is PostgreSQL at `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` The object store is MinIO at `STORAGE_ENDPOINT`. `src: Technical requirements para 1`
- [ ] `C-TR-06` `literal` The object store bucket is named by `STORAGE_BUCKET`. `src: Technical requirements para 1`
- [ ] `C-TR-07` `literal` The object store is reached with `STORAGE_ACCESS_KEY`. `src: Technical requirements para 1`
- [ ] `C-TR-08` `literal` The object store is reached with `STORAGE_SECRET_KEY`. `src: Technical requirements para 1`
- [ ] `C-TR-09` `constraint` Every host, port, credential is read from the environment. `src: Technical requirements para 1`
- [ ] `C-TR-10` `constraint` No second database, cache, queue, object store, identity provider, mail vendor is introduced. `src: Technical requirements para 2`
- [ ] `C-TR-11` `capability` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements para 3`
- [ ] `C-TR-12` `constraint` The scene code is fetched on the tour alone. `src: Technical requirements para 4`
- [ ] `C-TR-13` `constraint` The editor computation is fetched on the editor alone. `src: Technical requirements para 4`
- [ ] `C-TR-14` `capability` One controller derives the current stop, every other tour component reading from that controller. `src: Technical requirements para 5`
- [ ] `C-TR-15` `capability` One sampler produces the point set the plot, the tick strip, the preview, the export consume. `src: Technical requirements para 5`
- [ ] `C-TR-16` `constraint` A documentation article is readable before any demonstration has run. `src: Technical requirements para 6`
- [ ] `C-TR-17` `constraint` The editor shows a correct static plot before the editor's own code has run. `src: Technical requirements para 6`
- [ ] `C-TR-18` `capability` Every static asset is addressed by a digest of its own content. `src: Technical requirements para 7`
- [ ] `C-TR-19` `capability` A publish purges the rendered routes for the affected version, that version's index. `src: Technical requirements para 7`
- [ ] `C-TR-20` `capability` A warm pass after a purge fetches the tour, the documentation landing route, the most-read pages. `src: Technical requirements para 7`
- [ ] `C-TR-21` `capability` The index artifact is immutable per version. `src: Technical requirements para 8`
- [ ] `C-TR-22` `capability` An index exceeding its size bound is split per module. `src: Technical requirements para 8`
- [ ] `C-TR-23` `constraint` Scroll work is driven from a frame loop reading a cached scroll position. `src: Technical requirements, rendering rules`
- [ ] `C-TR-24` `constraint` An element transform is composed from individually addressable channels. `src: Technical requirements, rendering rules`
- [ ] `C-TR-25` `constraint` Whatever is promoted for a motion is un-promoted when the motion ends. `src: Technical requirements, rendering rules`
- [ ] `C-TR-26` `constraint` Nothing shifts after first paint on any route. `src: Technical requirements, rendering rules`
- [ ] `C-TR-27` `capability` Authored content is rendered through a sanitising pipeline at publish time. `src: Technical requirements, security paragraph`
- [ ] `C-TR-28` `capability` An external link carries no referrer, opening in a new context. `src: Technical requirements, security paragraph`
- [ ] `C-TR-29` `contract` Every response carries a strict transport policy, a no-sniff content-type policy. `src: Technical requirements, security paragraph`
- [ ] `C-TR-30` `contract` Every response denies frame ancestors. `src: Technical requirements, security paragraph`
- [ ] `C-TR-31` `contract` Every response carries a strict-origin-when-cross-origin referrer policy. `src: Technical requirements, security paragraph`
- [ ] `C-TR-32` `contract` Every response denies camera, microphone, geolocation, payment. `src: Technical requirements, security paragraph`
- [ ] `C-TR-33` `contract` The content policy restricts form actions to the app's own origin. `src: Technical requirements, security paragraph`
- [ ] `C-TR-34` `constraint` No credential, key, token appears in anything the browser downloads. `src: Technical requirements, security paragraph`
- [ ] `C-TR-35` `contract` Logs are structured as one line of JSON per request on standard output. `src: Technical requirements, logging paragraph`
- [ ] `C-TR-36` `data` A log line carries the method, the route, the status, the elapsed milliseconds, a request identifier. `src: Technical requirements, logging paragraph`
- [ ] `C-TR-37` `capability` The request identifier is returned in the body of every error response. `src: Technical requirements, logging paragraph`
- [ ] `C-TR-38` `constraint` No subscriber address is logged in full. `src: Technical requirements, logging paragraph`
- [ ] `C-TR-39` `constraint` No confirmation token is logged in any form. `src: Technical requirements, logging paragraph`
- [ ] `C-TR-40` `constraint` No search query text is logged. `src: Technical requirements, logging paragraph`
- [ ] `C-TR-41` `constraint` An error carries a stable machine code, a human sentence, never a stack trace. `src: Technical requirements, conventions paragraph`
- [ ] `C-TR-42` `constraint` No request changes state on a read except the single-use confirmation. `src: Technical requirements, errors paragraph`
- [ ] `C-TR-43` `capability` Search ranking ties resolve by tree order. `src: Technical requirements, determinism paragraph`
- [ ] `C-TR-44` `capability` The flattened sequence is recomputed for a whole version whenever a page moves. `src: Technical requirements, determinism paragraph`
- [ ] `C-TR-45` `literal` The app stays responsive with `48` pages in one published version. `src: Technical requirements, scale paragraph`
- [ ] `C-TR-46` `literal` The app stays responsive with `20000` page-view rows. `src: Technical requirements, scale paragraph`
- [ ] `C-TR-47` `literal` The app stays responsive with `5000` subscriber rows. `src: Technical requirements, scale paragraph`

## C-DM Data model

- [ ] `C-DM-01` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model, password paragraph`
- [ ] `C-DM-02` `contract` The seeded password is written into `/app/USER_README.md`. `src: Data model, password paragraph`
- [ ] `C-DM-03` `data` An account row carries an identifier, an address unique case-insensitively, a display name, a password hash, a creation moment. `src: Data model, identity paragraph`
- [ ] `C-DM-04` `data` A session row carries an identifier, an account reference, a token hash, an expiry, a creation moment. `src: Data model, identity paragraph`
- [ ] `C-DM-05` `data` A version row carries a unique label, a sort key, a state, a current flag, a publication moment, an index object key, a unique preview key. `src: Data model, content paragraph`
- [ ] `C-DM-06` `data` A version state is one of `draft`, `published`, `archived`. `src: Data model, content paragraph`
- [ ] `C-DM-07` `data` A module row carries a slug, a name, a colour family, a position, an optional tile position, an object name, a badge, a badge expiry. `src: Data model, content paragraph`
- [ ] `C-DM-08` `constraint` A module slug is unique within its version. `src: Data model, content paragraph`
- [ ] `C-DM-09` `constraint` A module position is unique within its version. `src: Data model, content paragraph`
- [ ] `C-DM-10` `constraint` A module tile position is unique within its version. `src: Data model, content paragraph`
- [ ] `C-DM-11` `data` A page row carries a slug, a title, a body, a position, a flattened position, an optional demo reference. `src: Data model, content paragraph`
- [ ] `C-DM-12` `constraint` A page slug is unique within its version, module, parent together. `src: Data model, content paragraph`
- [ ] `C-DM-13` `constraint` A flattened position is unique within its version. `src: Data model, content paragraph`
- [ ] `C-DM-14` `data` The flattened position is stored rather than computed at request time. `src: Data model, flattened paragraph`
- [ ] `C-DM-15` `data` A page anchor row carries an anchor, its text, a position. `src: Data model, anchors paragraph`
- [ ] `C-DM-16` `data` A demo row carries a kind, a source, parameters, a poster seed, a poster object key. `src: Data model, demos paragraph`
- [ ] `C-DM-17` `data` A demo kind is one of `inline`, `scene`. `src: Data model, demos paragraph`
- [ ] `C-DM-18` `data` A sponsor tier row carries a unique slug, a name, a unique rank, a placement list, a mark scale. `src: Data model, sponsorship paragraph`
- [ ] `C-DM-19` `data` A sponsor row carries a name, an optional mark object key, a destination, a position, a unique external identifier, an active-from date, an optional active-to date, a sync moment. `src: Data model, sponsorship paragraph`
- [ ] `C-DM-20` `data` A roster source row carries an object key, an availability flag, a fetch moment, a last-good fetch moment. `src: Data model, sponsorship paragraph`
- [ ] `C-DM-21` `data` A subscriber row carries an address, a list, a state, a token digest, a token expiry, a confirmation moment, an unsubscribe moment, a source route, a request fingerprint. `src: Data model, mailing list paragraph`
- [ ] `C-DM-22` `data` A subscriber state is one of `pending`, `confirmed`, `unsubscribed`, `bounced`, `complained`. `src: Data model, mailing list paragraph`
- [ ] `C-DM-23` `constraint` A subscriber row is unique on the lowercased address together with the list. `src: Data model, mailing list paragraph`
- [ ] `C-DM-24` `constraint` The subscriber table holds no name, no company, no marketing attribute, no behavioural profile. `src: Data model, absent paragraph`
- [ ] `C-DM-25` `data` An outbox message row carries a kind, a state, an attempt count, a next attempt moment, a unique idempotency key. `src: Data model, mailing list paragraph`
- [ ] `C-DM-26` `data` A mail event row carries a unique provider event identifier, a type, a signature-validity flag, a receipt moment. `src: Data model, mailing list paragraph`
- [ ] `C-DM-27` `data` A job run row carries a job name, a state, a lock token, a start moment, a finish moment, a detail. `src: Data model, operations paragraph`
- [ ] `C-DM-28` `data` A dead-letter row carries a job name, a payload, a reason, a creation moment. `src: Data model, operations paragraph`
- [ ] `C-DM-29` `data` An analytics event row carries a kind, attributes, a session key, a creation moment. `src: Data model, operations paragraph`
- [ ] `C-DM-30` `data` A storage choice row carries the choice, a fingerprint, a decision moment. `src: Data model, operations paragraph`
- [ ] `C-DM-31` `data` A rate limit counter row carries a scope, a key, a window start, a count. `src: Data model, operations paragraph`
- [ ] `C-DM-32` `literal` A version's search index lives at `index/<version_label>/search-index.json`. `src: Data model, object keys paragraph`
- [ ] `C-DM-33` `literal` A sponsor's mark lives at `sponsors/<external_id>/mark.svg`. `src: Data model, object keys paragraph`
- [ ] `C-DM-34` `literal` A demo's poster lives at `posters/<version_label>/<module_slug>/<page_slug>.svg`. `src: Data model, object keys paragraph`
- [ ] `C-DM-35` `literal` The sponsor roster document lives at `roster/current.json`. `src: Data model, object keys paragraph`
- [ ] `C-DM-36` `contract` Every object key names a real object in the object store rather than a row. `src: Data model, object keys paragraph`
- [ ] `C-DM-37` `data` A page's readability is derived from its version's state. `src: Data model, derived paragraph`
- [ ] `C-DM-38` `data` Which sponsor cards a surface carries is derived from each tier's placement set. `src: Data model, derived paragraph`
- [ ] `C-DM-39` `data` Whether a badge shows is derived from its expiry against the clock. `src: Data model, derived paragraph`
- [ ] `C-DM-40` `constraint` The flattened position runs from `1` to the page count with no gap. `src: Data model, invariants paragraph`
- [ ] `C-DM-41` `constraint` A module's colour family is one of the twenty-one named families. `src: Data model, invariants paragraph`
- [ ] `C-DM-42` `constraint` Every internal link in a published version resolves within that version. `src: Data model, invariants paragraph`
- [ ] `C-DM-43` `constraint` A confirmation token's plaintext is nowhere at rest. `src: Data model, invariants paragraph`
- [ ] `C-DM-44` `literal` The seeded published version is `4.5.0`. `src: Data model, seed paragraph`
- [ ] `C-DM-45` `literal` The seeded archived version is `4.4.0`. `src: Data model, seed paragraph`
- [ ] `C-DM-46` `literal` The seeded draft version is `4.6.0`. `src: Data model, seed paragraph`
- [ ] `C-DM-47` `literal` The seeded draft version's preview key is `pv_9f2c41be`. `src: Data model, seed paragraph`
- [ ] `C-DM-48` `literal` The published version carries `16` modules. `src: Data model, seed paragraph`
- [ ] `C-DM-49` `literal` The first module is `getting-started`, bound to the family `red`. `src: Data model, module table row 1`
- [ ] `C-DM-50` `literal` The module `utilities` is bound to the family `king`. `src: Data model, module table row 12`
- [ ] `C-DM-51` `literal` The module `adapters` is bound to the family `purple`. `src: Data model, module table row 16`
- [ ] `C-DM-52` `literal` Twelve modules carry a tile position, `getting-started` carrying none. `src: Data model, module table`
- [ ] `C-DM-53` `literal` The modules `text`, `adapters` carry the `NEW` badge. `src: Data model, seed paragraph`
- [ ] `C-DM-54` `literal` Both seeded badges expire on `2026-12-01`. `src: Data model, seed paragraph`
- [ ] `C-DM-55` `literal` The published version carries `48` pages. `src: Data model, page table`
- [ ] `C-DM-56` `literal` The first page in the flattened sequence is `getting-started/installation`. `src: Data model, seed paragraph`
- [ ] `C-DM-57` `literal` The page after `getting-started/your-first-animation` is `timer/create-timer`. `src: Data model, seed paragraph`
- [ ] `C-DM-58` `literal` The last page in the flattened sequence is `adapters/adapter-limits`. `src: Data model, seed paragraph`
- [ ] `C-DM-59` `literal` `47` demos are seeded, `adapters/adapter-limits` carrying none. `src: Data model, seed paragraph`
- [ ] `C-DM-60` `literal` The three pages of `svg` carry demos of kind `scene`. `src: Data model, seed paragraph`
- [ ] `C-DM-61` `literal` The archived version `4.4.0` carries no `text` module. `src: Data model, seed paragraph`
- [ ] `C-DM-62` `literal` The draft version links to `getting-started/configuration`, which does not exist. `src: Data model, seed paragraph`
- [ ] `C-DM-63` `literal` The seeded sponsor `Ravelin` carries no mark. `src: Data model, seed paragraph`
- [ ] `C-DM-64` `literal` The seeded sponsor `Corvid` ended on `2026-08-31`. `src: Data model, seed paragraph`
- [ ] `C-DM-65` `literal` The seeded subscriber `confirmed@example.com` is confirmed on `course_waitlist`. `src: Data model, seed paragraph`
- [ ] `C-DM-66` `literal` The seeded subscriber `pending@example.com` carries an unconsumed token. `src: Data model, seed paragraph`
- [ ] `C-DM-67` `literal` The seeded subscriber `expired@example.com` carries a token that expired on `2026-09-09`. `src: Data model, seed paragraph`
- [ ] `C-DM-68` `literal` The seeded subscriber `complained@example.com` sits in the `complained` state. `src: Data model, seed paragraph`
- [ ] `C-DM-69` `literal` The seeded subscriber `unsubscribed@example.com` sits in the `unsubscribed` state. `src: Data model, seed paragraph`
- [ ] `C-DM-70` `constraint` Seeding is idempotent, so restarting the app duplicates no row. `src: Data model, final paragraph`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` One token layer is declared once at the root, consumed everywhere. `src: Front-end specification, token layer`
- [ ] `C-FE-02` `ui` Spacing is one ladder of ten steps. `src: Front-end specification, token layer`
- [ ] `C-FE-03` `ui` Type is a second ladder of ten steps. `src: Front-end specification, token layer`
- [ ] `C-FE-04` `ui` Radius is a ladder of five steps. `src: Front-end specification, token layer`
- [ ] `C-FE-05` `ui` Every transform channel defaults to identity. `src: Front-end specification, token layer`
- [ ] `C-FE-06` `ui` The demo panel gap is zero, so panels butt against each other. `src: Front-end specification, token layer`
- [ ] `C-FE-07` `ui` The inset trio carries a padding, a negative margin, a compensating width. `src: Front-end specification, token layer`
- [ ] `C-FE-08` `ui` Twenty-one ramps run eight steps in the same direction. `src: Front-end specification, ramps table`
- [ ] `C-FE-09` `ui` The ramps named cyan, sky, turquoise stay distinguishable by hue. `src: Front-end specification, ramps table`
- [ ] `C-FE-10` `ui` The rim light is the only warm value in the scene. `src: Front-end specification, scene values`
- [ ] `C-FE-11` `ui` The code palette carries seven roles outside every ramp. `src: Front-end specification, code palette`
- [ ] `C-FE-12` `ui` The alias colours the drawn axis lines inside a diagram. `src: Front-end specification, the alias`
- [ ] `C-FE-13` `ui` The wordmark alone uses the oblique axis. `src: Front-end specification, type`
- [ ] `C-FE-14` `constraint` No font binary is fetched. `src: Front-end specification, type`
- [ ] `C-FE-15` `constraint` The families `Ration Sans`, `Ration Mono`, `Ration Seven` are not reproduced. `src: Front-end specification, type`
- [ ] `C-FE-16` `ui` Six icons are drawn as geometry on one square grid. `src: Front-end specification, iconography`
- [ ] `C-FE-17` `constraint` No icon file ships, no icon font is loaded. `src: Front-end specification, iconography`
- [ ] `C-FE-18` `ui` The curve icon overshoots its own midpoint. `src: Front-end specification, iconography`
- [ ] `C-FE-19` `ui` The heart particles blend additively so an overlap brightens. `src: Front-end specification, iconography`
- [ ] `C-FE-20` `ui` The particle glow has no radius in its base state. `src: Front-end specification, iconography`
- [ ] `C-FE-21` `ui` The wordmark carries a single accent dot in the red ramp's brightest step. `src: Front-end specification, iconography`
- [ ] `C-FE-22` `ui` The header gains a blur, a hairline rule once scrolled past its own height. `src: Front-end specification, global chrome`
- [ ] `C-FE-23` `ui` Two navigation calls drop their labels through a width transition. `src: Front-end specification, global chrome`
- [ ] `C-FE-24` `ui` The mobile menu traps focus, restoring focus to the control that opened the panel. `src: Front-end specification, global chrome`
- [ ] `C-FE-25` `ui` The mobile menu locks the document scroll without shifting the layout. `src: Front-end specification, global chrome`
- [ ] `C-FE-26` `ui` The footer carries four columns, stacking to one below the primary turning point. `src: Front-end specification, global chrome`
- [ ] `C-FE-27` `ui` The scroll indicator draws a leading block, a fainter trailing block. `src: Front-end specification, global chrome`
- [ ] `C-FE-28` `ui` Five named curves carry every motion. `src: Front-end specification, motion`
- [ ] `C-FE-29` `ui` The pop pair animates scale as a property in its own right. `src: Front-end specification, motion`
- [ ] `C-FE-30` `ui` Fourteen named objects serve the sixteen modules. `src: Front-end specification, instrument table`
- [ ] `C-FE-31` `ui` The universal hover lift runs from a light neutral to a near-white. `src: Front-end specification, hover`
- [ ] `C-FE-32` `ui` The funding call moves its ground rather than its text. `src: Front-end specification, hover`
- [ ] `C-FE-33` `ui` A curve handle carries the grab cursor, the grabbing cursor during a drag. `src: Front-end specification, hover`
- [ ] `C-FE-34` `ui` The focus ring is solid, near-white, offset from the element. `src: Front-end specification, hover`
- [ ] `C-FE-35` `ui` A specimen block sits on a step of the hole ramp. `src: Front-end specification, specimen`
- [ ] `C-FE-36` `ui` The tour's module grid lays four rows of three tiles at a wide width. `src: Front-end specification, route the tour`
- [ ] `C-FE-37` `ui` The current demo panel lifts its ground to the module's dimmest step. `src: Front-end specification, route the shell`
- [ ] `C-FE-38` `ui` The editor stacks plot, preview, export, grid at a narrow width. `src: Front-end specification, route the editor`
- [ ] `C-FE-39` `ui` The preset grid clips to a rounded rectangle so a tile corner cannot escape. `src: Front-end specification, route the editor`
- [ ] `C-FE-40` `ui` Both handle primitives carry a dark drop shadow. `src: Front-end specification, route the editor`
- [ ] `C-FE-41` `ui` The success message sits in every document fully transparent at rest. `src: Front-end specification, subscription controls`
- [ ] `C-FE-42` `ui` The error message sits in every document fully transparent at rest. `src: Front-end specification, subscription controls`
- [ ] `C-FE-43` `constraint` No grain texture, no noise texture exists in the build. `src: Front-end specification, textures`
- [ ] `C-FE-44` `capability` The same poster seed produces the same still on every build. `src: Front-end specification, textures`
- [ ] `C-FE-45` `literal` The navigation labels are `DOCS`, `EASINGS`, `LEARN`, `EXAMPLES`, `SOURCE`. `src: Front-end specification, copy chrome table`
- [ ] `C-FE-46` `literal` The funding call reads `SPONSOR`. `src: Front-end specification, copy chrome table`
- [ ] `C-FE-47` `literal` The skip link reads `Skip to content`. `src: Front-end specification, copy chrome table`
- [ ] `C-FE-48` `literal` The footer headings read `SPONSORS`, `SITE`, `SOCIALS`, `STAY IN TOUCH`. `src: Front-end specification, copy chrome table`
- [ ] `C-FE-49` `ui` The footer attribution names the maintainer beneath the full-width wordmark. `src: Front-end specification, copy chrome table`
- [ ] `C-FE-50` `literal` The advertising attribution reads `ads via Carbonate`. `src: Front-end specification, copy chrome table`
- [ ] `C-FE-51` `literal` The tour headline reads `One engine for every animation.` `src: Front-end specification, copy tour table`
- [ ] `C-FE-52` `literal` The tour subheading reads `A small, fast library for moving anything on the web.` `src: Front-end specification, copy tour table`
- [ ] `C-FE-53` `literal` The install line reads `npm i lumenjs`. `src: Front-end specification, copy tour table`
- [ ] `C-FE-54` `literal` The secondary call reads `LEARN MORE`. `src: Front-end specification, copy tour table`
- [ ] `C-FE-55` `literal` The closing headline reads `Start animating`. `src: Front-end specification, copy tour table`
- [ ] `C-FE-56` `literal` The twelfth stop headline reads `Our sponsors`. `src: Front-end specification, copy stops table`
- [ ] `C-FE-57` `literal` The documentation landing title reads `Documentation`. `src: Front-end specification, copy documentation table`
- [ ] `C-FE-58` `literal` The tier headings read `Upper sponsors`, `Lower sponsors`. `src: Front-end specification, copy documentation table`
- [ ] `C-FE-59` `literal` The recruitment card reads `Become a sponsor`. `src: Front-end specification, copy documentation table`
- [ ] `C-FE-60` `ui` The in-section list carries a fixed heading above the sibling rows. `src: Front-end specification, copy documentation table`
- [ ] `C-FE-61` `literal` The pager labels read `PREVIOUS`, `NEXT`. `src: Front-end specification, copy documentation table`
- [ ] `C-FE-62` `literal` The search placeholder reads `SEARCH`. `src: Front-end specification, copy documentation table`
- [ ] `C-FE-63` `literal` The empty search result reads `No pages match that.` `src: Front-end specification, copy documentation table`
- [ ] `C-FE-64` `literal` The unavailable search message reads `Search is unavailable. Use the menu on the left.` `src: Front-end specification, copy documentation table`
- [ ] `C-FE-65` `literal` The editor panel headings read `PREVIEW`, `EXPORT`. `src: Front-end specification, copy editor table`
- [ ] `C-FE-66` `literal` The copy confirmation reads `Copied`. `src: Front-end specification, copy editor table`
- [ ] `C-FE-67` `ui` The course page carries a fixed two-line headline above the supporting copy. `src: Front-end specification, copy subscription table`
- [ ] `C-FE-68` `literal` The waiting-list label reads `Join the waiting list`. `src: Front-end specification, copy subscription table`
- [ ] `C-FE-69` `literal` The submit control reads `SUBSCRIBE`. `src: Front-end specification, copy subscription table`
- [ ] `C-FE-70` `literal` The fallback line reads `If the form fails, write to hello[at]lumenjs.example.` `src: Front-end specification, copy subscription table`
- [ ] `C-FE-71` `literal` The acceptance message reads `Check your inbox to confirm.` `src: Front-end specification, copy subscription table`
- [ ] `C-FE-72` `literal` The invalid message reads `That does not look like an email address.` `src: Front-end specification, copy subscription table`
- [ ] `C-FE-73` `literal` The rate-limited message reads `Too many attempts. Try again shortly.` `src: Front-end specification, copy subscription table`
- [ ] `C-FE-74` `literal` The confirmed page reads `You are on the list.` `src: Front-end specification, copy subscription table`
- [ ] `C-FE-75` `literal` The not-found heading reads `Nothing here`. `src: Front-end specification, copy errors table`
- [ ] `C-FE-76` `literal` The not-found body reads `That address does not exist. Try one of these.` `src: Front-end specification, copy errors table`
- [ ] `C-FE-77` `literal` The server error heading reads `Something broke`. `src: Front-end specification, copy errors table`
- [ ] `C-FE-78` `literal` The retry control reads `TRY AGAIN`. `src: Front-end specification, copy errors table`
- [ ] `C-FE-79` `ui` A curve handle's accessible name states which control point the handle is. `src: Front-end specification, accessible names table`
- [ ] `C-FE-80` `ui` A demo panel is hidden from assistive technology. `src: Front-end specification, accessible names table`
- [ ] `C-FE-81` `constraint` No exclamation mark appears in any copy. `src: Front-end specification, copy voice`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` One origin serves the whole product. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` No visitor account of any kind exists. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` No permission grid exists. `src: Constraints bullet 2`
- [ ] `C-CN-04` `constraint` No money moves anywhere in the product. `src: Constraints bullet 3`
- [ ] `C-CN-05` `constraint` No request leaves the app's own origin at run time. `src: Constraints bullet 4`
- [ ] `C-CN-06` `constraint` The source host, the playground, the package registry are named in outbound links only. `src: Constraints bullet 4`
- [ ] `C-CN-07` `constraint` No email is actually sent. `src: Constraints bullet 5`
- [ ] `C-CN-08` `constraint` A message that would be sent becomes a row in the outbox. `src: Constraints bullet 5`
- [ ] `C-CN-09` `constraint` No image file, no video file, no audio file ships. `src: Constraints bullet 6`
- [ ] `C-CN-10` `constraint` No compressed geometry file ships. `src: Constraints bullet 6`
- [ ] `C-CN-11` `constraint` Every scene object is composed from primitives. `src: Constraints bullet 6`
- [ ] `C-CN-12` `constraint` The scene is a genuine scene rather than a video, a picture. `src: Constraints bullet 8`
- [ ] `C-CN-13` `constraint` No smooth-scroll layer exists. `src: Constraints bullet 9`
- [ ] `C-CN-14` `constraint` No comment, no like, no message, no social graph exists. `src: Constraints bullet 10`
- [ ] `C-CN-15` `constraint` No third-party analytics vendor is used. `src: Constraints bullet 10`
- [ ] `C-CN-16` `constraint` No consent-requiring identifier is written before the visitor has answered. `src: Constraints bullet 11`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual step. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` A reserved `.browser_screenshots/` directory exists at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` A reserved `.downloads/` directory exists at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `contract` A production build is served behind a static server rather than a development server. `src: Deployment contract bullet 7`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-11` `contract` The server binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-12` `contract` No copy of a backing service is downloaded, installed, compiled, started. `src: Deployment contract bullet 10`
- [ ] `C-DC-13` `contract` No edge function is used. `src: Deployment contract bullet 11`
- [ ] `C-DC-14` `contract` No persistent volume, no fixed container name, no custom network is declared. `src: Deployment contract bullet 12`
- [ ] `C-DC-15` `contract` `POST /api/subscribe` accepts `email`, `list`, `company_website`, a timing token, form-encoded. `src: Deployment contract, API shapes row 1`
- [ ] `C-DC-16` `contract` `GET /api/subscribe/confirm` takes a `token`, returning a rendered confirmation page. `src: Deployment contract, API shapes row 2`
- [ ] `C-DC-17` `contract` `GET /api/search-index/<version_label>` streams the version's index artifact from the object store. `src: Deployment contract, API shapes row 4`
- [ ] `C-DC-18` `contract` `GET /api/sponsors` returns the tiers, their active sponsors for a named surface, with the roster's age. `src: Deployment contract, API shapes row 8`
- [ ] `C-DC-19` `contract` `POST /api/studio/versions/<id>/validate` returns each of the nine checks with its outcome. `src: Deployment contract, API shapes row 16`
- [ ] `C-DC-20` `contract` `POST /api/studio/versions/<id>/publish` promotes the version, naming the refusing check otherwise. `src: Deployment contract, API shapes row 17`
- [ ] `C-DC-21` `contract` `POST /api/hooks/mail` authenticates by signature rather than by a session. `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-22` `contract` Bearer auth is required on everything under `/api/studio`. `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-23` `contract` An invalid call is rejected as a client error rather than a `5xx`. `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-24` `contract` The object store is not simulated by bytes on the app container's filesystem. `src: Deployment contract, No mocks`
- [ ] `C-DC-25` `contract` The search index is not rebuilt from the database on every query. `src: Deployment contract, No mocks`
- [ ] `C-DC-26` `contract` Rows live in PostgreSQL rather than in a process. `src: Deployment contract, No mocks`

## Pinned literals

| Value | What it is | Item | Source |
|---|---|---|---|
| `maintainer@example.com` | pinned by C-RL-16 | C-RL-16 | User roles, seeded account paragraph |
| `Elias Marchand` | pinned by C-RL-17 | C-RL-17 | User roles, seeded account paragraph |
| `intro` | pinned by C-CF-13 | C-CF-13 | Core features, tour rule 2 |
| `toolbox` | pinned by C-CF-13 | C-CF-13 | Core features, tour rule 2 |
| `intuitive` | pinned by C-CF-13 | C-CF-13 | Core features, tour rule 2 |
| `composition` | pinned by C-CF-13 | C-CF-13 | Core features, tour rule 2 |
| `scroll` | pinned by C-CF-13 | C-CF-13 | Core features, tour rule 2 |
| `staggering` | pinned by C-CF-13 | C-CF-13 | Core features, tour rule 2 |
| `svg-utilities` | pinned by C-CF-13 | C-CF-13 | Core features, tour rule 2 |
| `draggable` | pinned by C-CF-13 | C-CF-13 | Core features, tour rule 2 |
| `clockwork` | pinned by C-CF-13 | C-CF-13 | Core features, tour rule 2 |
| `responsive` | pinned by C-CF-13 | C-CF-13 | Core features, tour rule 2 |
| `modules` | pinned by C-CF-13 | C-CF-13 | Core features, tour rule 2 |
| `sponsors` | pinned by C-CF-13 | C-CF-13 | Core features, tour rule 2 |
| `2` | pinned by C-CF-47 | C-CF-47 | Core features, instrument rule 6 |
| `NEW` | pinned by C-CF-63 | C-CF-63 | Core features, shell rule 3 |
| `remap` | pinned by C-CF-114 | C-CF-114 | Core features, search rule 5 |
| `utilities/remap-and-clamp` | pinned by C-CF-114 | C-CF-114 | Core features, search rule 5 |
| `120` | pinned by C-CF-129 | C-CF-129 | Core features, search rule 10 |
| `10` | pinned by C-CF-135 | C-CF-135 | Core features, editor rule 2 |
| `37` | pinned by C-CF-136 | C-CF-136 | Core features, editor rule 2 |
| `default` | pinned by C-CF-137 | C-CF-137 | Core features, editor rule 2 |
| `snappy` | pinned by C-CF-137 | C-CF-137 | Core features, editor rule 2 |
| `bouncy` | pinned by C-CF-137 | C-CF-137 | Core features, editor rule 2 |
| `strong` | pinned by C-CF-137 | C-CF-137 | Core features, editor rule 2 |
| `in` | pinned by C-CF-138 | C-CF-138 | Core features, editor rule 2 |
| `out` | pinned by C-CF-138 | C-CF-138 | Core features, editor rule 2 |
| `in-out` | pinned by C-CF-138 | C-CF-138 | Core features, editor rule 2 |
| `out-in` | pinned by C-CF-138 | C-CF-138 | Core features, editor rule 2 |
| `CSS` | pinned by C-CF-163 | C-CF-163 | Core features, editor rule 12 |
| `JS` | pinned by C-CF-163 | C-CF-163 | Core features, editor rule 12 |
| `3` | pinned by C-CF-169 | C-CF-169 | Core features, editor rule 14 |
| `family` | pinned by C-CF-172 | C-CF-172 | Core features, editor rule 15 |
| `member` | pinned by C-CF-172 | C-CF-172 | Core features, editor rule 15 |
| `p1x` | pinned by C-CF-172 | C-CF-172 | Core features, editor rule 15 |
| `p1y` | pinned by C-CF-172 | C-CF-172 | Core features, editor rule 15 |
| `p2x` | pinned by C-CF-172 | C-CF-172 | Core features, editor rule 15 |
| `p2y` | pinned by C-CF-172 | C-CF-172 | Core features, editor rule 15 |
| `bounce` | pinned by C-CF-173 | C-CF-173 | Core features, editor rule 15 |
| `duration` | pinned by C-CF-173 | C-CF-173 | Core features, editor rule 15 |
| `course_waitlist` | pinned by C-CF-180 | C-CF-180 | Core features, subscription rule 1 |
| `newsletter` | pinned by C-CF-181 | C-CF-181 | Core features, subscription rule 1 |
| `128` | pinned by C-CF-192 | C-CF-192 | Core features, subscription rule 5 |
| `7` | pinned by C-CF-194 | C-CF-194 | Core features, subscription rule 5 |
| `20` | pinned by C-CF-215 | C-CF-215 | Core features, subscription rule 9 |
| `company_website` | pinned by C-CF-217 | C-CF-217 | Core features, subscription rule 9 |
| `200` | pinned by C-CF-221 | C-CF-221 | Core features, subscription rule 10 |
| `upper` | pinned by C-CF-239 | C-CF-239 | Core features, funding rule 2 |
| `1` | pinned by C-CF-239 | C-CF-239 | Core features, funding rule 2 |
| `lower` | pinned by C-CF-240 | C-CF-240 | Core features, funding rule 2 |
| `send_confirmation` | pinned by C-CF-362 | C-CF-362 | Core features, jobs rule 1 |
| `send_welcome` | pinned by C-CF-362 | C-CF-362 | Core features, jobs rule 1 |
| `process_mail_events` | pinned by C-CF-362 | C-CF-362 | Core features, jobs rule 1 |
| `sync_sponsor_roster` | pinned by C-CF-362 | C-CF-362 | Core features, jobs rule 1 |
| `sweep_expired_subscriptions` | pinned by C-CF-362 | C-CF-362 | Core features, jobs rule 1 |
| `expire_badges` | pinned by C-CF-362 | C-CF-362 | Core features, jobs rule 1 |
| `rebuild_index` | pinned by C-CF-362 | C-CF-362 | Core features, jobs rule 1 |
| `purge_caches` | pinned by C-CF-362 | C-CF-362 | Core features, jobs rule 1 |
| `warm_caches` | pinned by C-CF-362 | C-CF-362 | Core features, jobs rule 1 |
| `check_roster_freshness` | pinned by C-CF-362 | C-CF-362 | Core features, jobs rule 1 |
| `5` | pinned by C-CF-367 | C-CF-367 | Core features, jobs rule 3 |
| `500` | pinned by C-CF-379 | C-CF-379 | Core features, jobs rule 7 |
| `24` | pinned by C-CF-381 | C-CF-381 | Core features, jobs rule 9 |
| `STORAGE_BUCKET` | pinned by C-TR-06 | C-TR-06 | Technical requirements para 1 |
| `STORAGE_ACCESS_KEY` | pinned by C-TR-07 | C-TR-07 | Technical requirements para 1 |
| `STORAGE_SECRET_KEY` | pinned by C-TR-08 | C-TR-08 | Technical requirements para 1 |
| `48` | pinned by C-TR-45 | C-TR-45 | Technical requirements, scale paragraph |
| `20000` | pinned by C-TR-46 | C-TR-46 | Technical requirements, scale paragraph |
| `5000` | pinned by C-TR-47 | C-TR-47 | Technical requirements, scale paragraph |
| `deku-demo-pw-2026` | pinned by C-DM-01 | C-DM-01 | Data model, password paragraph |
| `index/<version_label>/search-index.json` | pinned by C-DM-32 | C-DM-32 | Data model, object keys paragraph |
| `sponsors/<external_id>/mark.svg` | pinned by C-DM-33 | C-DM-33 | Data model, object keys paragraph |
| `posters/<version_label>/<module_slug>/<page_slug>.svg` | pinned by C-DM-34 | C-DM-34 | Data model, object keys paragraph |
| `roster/current.json` | pinned by C-DM-35 | C-DM-35 | Data model, object keys paragraph |
| `4.5.0` | pinned by C-DM-44 | C-DM-44 | Data model, seed paragraph |
| `4.4.0` | pinned by C-DM-45 | C-DM-45 | Data model, seed paragraph |
| `4.6.0` | pinned by C-DM-46 | C-DM-46 | Data model, seed paragraph |
| `pv_9f2c41be` | pinned by C-DM-47 | C-DM-47 | Data model, seed paragraph |
| `16` | pinned by C-DM-48 | C-DM-48 | Data model, seed paragraph |
| `getting-started` | pinned by C-DM-49 | C-DM-49 | Data model, module table row 1 |
| `red` | pinned by C-DM-49 | C-DM-49 | Data model, module table row 1 |
| `utilities` | pinned by C-DM-50 | C-DM-50 | Data model, module table row 12 |
| `king` | pinned by C-DM-50 | C-DM-50 | Data model, module table row 12 |
| `adapters` | pinned by C-DM-51 | C-DM-51 | Data model, module table row 16 |
| `purple` | pinned by C-DM-51 | C-DM-51 | Data model, module table row 16 |
| `text` | pinned by C-DM-53 | C-DM-53 | Data model, seed paragraph |
| `2026-12-01` | pinned by C-DM-54 | C-DM-54 | Data model, seed paragraph |
| `getting-started/installation` | pinned by C-DM-56 | C-DM-56 | Data model, seed paragraph |
| `getting-started/your-first-animation` | pinned by C-DM-57 | C-DM-57 | Data model, seed paragraph |
| `timer/create-timer` | pinned by C-DM-57 | C-DM-57 | Data model, seed paragraph |
| `adapters/adapter-limits` | pinned by C-DM-58 | C-DM-58 | Data model, seed paragraph |
| `47` | pinned by C-DM-59 | C-DM-59 | Data model, seed paragraph |
| `svg` | pinned by C-DM-60 | C-DM-60 | Data model, seed paragraph |
| `scene` | pinned by C-DM-60 | C-DM-60 | Data model, seed paragraph |
| `getting-started/configuration` | pinned by C-DM-62 | C-DM-62 | Data model, seed paragraph |
| `Ravelin` | pinned by C-DM-63 | C-DM-63 | Data model, seed paragraph |
| `Corvid` | pinned by C-DM-64 | C-DM-64 | Data model, seed paragraph |
| `2026-08-31` | pinned by C-DM-64 | C-DM-64 | Data model, seed paragraph |
| `confirmed@example.com` | pinned by C-DM-65 | C-DM-65 | Data model, seed paragraph |
| `pending@example.com` | pinned by C-DM-66 | C-DM-66 | Data model, seed paragraph |
| `expired@example.com` | pinned by C-DM-67 | C-DM-67 | Data model, seed paragraph |
| `2026-09-09` | pinned by C-DM-67 | C-DM-67 | Data model, seed paragraph |
| `complained@example.com` | pinned by C-DM-68 | C-DM-68 | Data model, seed paragraph |
| `complained` | pinned by C-DM-68 | C-DM-68 | Data model, seed paragraph |
| `unsubscribed@example.com` | pinned by C-DM-69 | C-DM-69 | Data model, seed paragraph |
| `unsubscribed` | pinned by C-DM-69 | C-DM-69 | Data model, seed paragraph |
| `DOCS` | pinned by C-FE-45 | C-FE-45 | Front-end specification, copy chrome table |
| `EASINGS` | pinned by C-FE-45 | C-FE-45 | Front-end specification, copy chrome table |
| `LEARN` | pinned by C-FE-45 | C-FE-45 | Front-end specification, copy chrome table |
| `EXAMPLES` | pinned by C-FE-45 | C-FE-45 | Front-end specification, copy chrome table |
| `SOURCE` | pinned by C-FE-45 | C-FE-45 | Front-end specification, copy chrome table |
| `SPONSOR` | pinned by C-FE-46 | C-FE-46 | Front-end specification, copy chrome table |
| `Skip to content` | pinned by C-FE-47 | C-FE-47 | Front-end specification, copy chrome table |
| `SPONSORS` | pinned by C-FE-48 | C-FE-48 | Front-end specification, copy chrome table |
| `SITE` | pinned by C-FE-48 | C-FE-48 | Front-end specification, copy chrome table |
| `SOCIALS` | pinned by C-FE-48 | C-FE-48 | Front-end specification, copy chrome table |
| `STAY IN TOUCH` | pinned by C-FE-48 | C-FE-48 | Front-end specification, copy chrome table |
| `ads via Carbonate` | pinned by C-FE-50 | C-FE-50 | Front-end specification, copy chrome table |
| `One engine for every animation.` | pinned by C-FE-51 | C-FE-51 | Front-end specification, copy tour table |
| `A small, fast library for moving anything on the web.` | pinned by C-FE-52 | C-FE-52 | Front-end specification, copy tour table |
| `npm i lumenjs` | pinned by C-FE-53 | C-FE-53 | Front-end specification, copy tour table |
| `LEARN MORE` | pinned by C-FE-54 | C-FE-54 | Front-end specification, copy tour table |
| `Start animating` | pinned by C-FE-55 | C-FE-55 | Front-end specification, copy tour table |
| `Our sponsors` | pinned by C-FE-56 | C-FE-56 | Front-end specification, copy stops table |
| `Documentation` | pinned by C-FE-57 | C-FE-57 | Front-end specification, copy documentation table |
| `Upper sponsors` | pinned by C-FE-58 | C-FE-58 | Front-end specification, copy documentation table |
| `Lower sponsors` | pinned by C-FE-58 | C-FE-58 | Front-end specification, copy documentation table |
| `Become a sponsor` | pinned by C-FE-59 | C-FE-59 | Front-end specification, copy documentation table |
| `PREVIOUS` | pinned by C-FE-61 | C-FE-61 | Front-end specification, copy documentation table |
| `NEXT` | pinned by C-FE-61 | C-FE-61 | Front-end specification, copy documentation table |
| `SEARCH` | pinned by C-FE-62 | C-FE-62 | Front-end specification, copy documentation table |
| `No pages match that.` | pinned by C-FE-63 | C-FE-63 | Front-end specification, copy documentation table |
| `Search is unavailable. Use the menu on the left.` | pinned by C-FE-64 | C-FE-64 | Front-end specification, copy documentation table |
| `PREVIEW` | pinned by C-FE-65 | C-FE-65 | Front-end specification, copy editor table |
| `EXPORT` | pinned by C-FE-65 | C-FE-65 | Front-end specification, copy editor table |
| `Copied` | pinned by C-FE-66 | C-FE-66 | Front-end specification, copy editor table |
| `Join the waiting list` | pinned by C-FE-68 | C-FE-68 | Front-end specification, copy subscription table |
| `SUBSCRIBE` | pinned by C-FE-69 | C-FE-69 | Front-end specification, copy subscription table |
| `If the form fails, write to hello[at]lumenjs.example.` | pinned by C-FE-70 | C-FE-70 | Front-end specification, copy subscription table |
| `Check your inbox to confirm.` | pinned by C-FE-71 | C-FE-71 | Front-end specification, copy subscription table |
| `That does not look like an email address.` | pinned by C-FE-72 | C-FE-72 | Front-end specification, copy subscription table |
| `Too many attempts. Try again shortly.` | pinned by C-FE-73 | C-FE-73 | Front-end specification, copy subscription table |
| `You are on the list.` | pinned by C-FE-74 | C-FE-74 | Front-end specification, copy subscription table |
| `Nothing here` | pinned by C-FE-75 | C-FE-75 | Front-end specification, copy errors table |
| `That address does not exist. Try one of these.` | pinned by C-FE-76 | C-FE-76 | Front-end specification, copy errors table |
| `Something broke` | pinned by C-FE-77 | C-FE-77 | Front-end specification, copy errors table |
| `TRY AGAIN` | pinned by C-FE-78 | C-FE-78 | Front-end specification, copy errors table |
| `Built and maintained by Elias Marchand` | pinned by C-FE-49 | C-FE-49 | Front-end specification, copy chrome table |
| `In this section` | pinned by C-FE-60 | C-FE-60 | Front-end specification, copy documentation table |
| `Learn how this site was built.` | pinned by C-FE-67 | C-FE-67 | Front-end specification, copy subscription table |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the default interface duration | C-UX-19 | named as around an eighth of a second, with no figure given |
| the primary responsive turning point | C-UX-38 | the arrangement is pinned, the width is the builder's |
| the search index size bound | C-TR-22 | named as a bound past which the index splits, with no figure |
| the grace period after a token expiry | C-CF-232 | named as a period after expiry, with no figure |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 13 |
| User roles | 1 | 17 |
| Core features | 40 | 383 |
| User flow | 5 | 30 |
| UI and UX notes | 8 | 42 |
| Technical requirements | 13 | 47 |
| Data model | 12 | 70 |
| Front-end specification | 21 | 81 |
| Constraints | 3 | 16 |
| Deployment contract | 13 | 26 |
