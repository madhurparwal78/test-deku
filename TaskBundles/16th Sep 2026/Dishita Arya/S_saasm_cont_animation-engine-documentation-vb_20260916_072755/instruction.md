# Lumen.js

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, copy the install line from the opening of the tour before the scene behind it has finished loading, scroll the tour to its twelfth stop, follow a module tile into the documentation, read from the first page of the first module to the last page of the last module using nothing but the pager, find a page by typing a call name that appears nowhere except inside a code specimen, design a curve in the editor and copy the snippet it generates, and join the course waiting list, all without hitting an error page. Four things in that sentence cannot be arranged inside the app's own screens. The search index for version `4.5.0` must exist as a real object in MinIO under the key scheme pinned below and be fetched from there on the first use of the search control: an index assembled in the browser from the rendered pages, a query run against PostgreSQL on every keystroke, or a JSON file sitting on the app container's disk are each a contract violation however good the interface looks. The pager's sequence must be a stored position in the database that has no gap and no duplicate across the whole published version, and the publish must refuse rather than let a reader discover the gap. The draft version `4.6.0` and its pages must not be readable by a signed-out caller by any address other than its own preview key, and must appear in no sitemap and in no search result. And submitting an address that is already confirmed must report success and send nothing, so that the form cannot be used to find out whether a particular person is on the list.

## Overview

Lumen.js is an open-source engine for animating things on a web page. It is installed from a package registry, it is funded entirely by sponsorship, and this is its site: its shop window, its manual, its workshop and its collection tin. It sells nothing and it has no visitor accounts.

That last sentence is the most consequential fact in this brief. Almost every specification of a product this size assumes a login and a payment, and this one must not. There is no sign-in control anywhere on the public site, no team, no seat, no invoice and no permission of any kind. The only thing a visitor can change on the server is to add an address to a mailing list, and that single fact shapes every decision below.

Five surfaces. The product tour is the home route: one continuous scroll about twenty-three window heights tall, holding a stage fixed in the window while twelve short passages take turns beside it. The documentation is a versioned manual of sixteen modules with a runnable demonstration beside every page. The curve editor is a workshop where somebody designs exactly how a movement should feel and copies the code for it. The course waiting list captures an address against a course that does not exist yet. And funding runs through the documentation and the tour as a tiered sponsor wall, because sponsorship is the only income the project has.

Behind them sits a content system with a server of record: a version lifecycle, an atomic publish with nine checks that can fail it, a search index built at publish and served as an artifact, a sponsor roster reconciled on a schedule, and one mail lifecycle that is the only irreplaceable data in the system. Everything else on this site can be rebuilt from source. The mailing list cannot.

What it deliberately is not. This is the site and the system behind it, never the animation engine itself: not its source, not its tests and not its release process. Not the course the waiting list collects for. Not the example collection. No account, role, permission or payment surface for a visitor. No real mail vendor, advertising network or sponsorship platform: each is modelled inside this app against seeded data and operator actions. And no binary file of any kind ships with it: every icon, every ground, every poster and every object in the three-dimensional scene is drawn or generated.

The genuinely hard part is that almost nothing here is allowed to be required. Every outside service the site leans on has a stated degraded state, and in every one of them the page still works with something small missing. The scene can fail and the tour keeps its ring, its colour and its narrative. The roster can fail and yesterday's sponsors keep their placements. The index can fail and search says so while the tree still navigates. A build that treats any of them as required has misunderstood the risk profile of a site whose income depends on being readable.

## User roles

Two, and one of them is anonymous. A role is read from the signed-in account's session and never from a request body, a query parameter or a header the caller controls.

| Role | Can do | Cannot do |
|---|---|---|
| Visitor | Read every published route, run every demonstration, use the whole editor, submit an address to either list, confirm or unsubscribe from a link | **Read a draft version at any address, reach the studio, publish anything, change a sponsor, read the outbox, read the page-view log, or run a job** |
| Maintainer | Everything in the studio: versions, modules, pages, demos, the sponsor roster, the mail outbox, the job runner and the page-view log | Nothing is withheld; there is one maintainer and there is no permission grid |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a Visitor session against any Maintainer-only endpoint must be rejected with `401` or `403`.

There is no signup. A visitor never creates an account, never signs in, and is never offered either, because there is nothing on this site for an account to own. One account is seeded: `maintainer@example.com`, whose display name is `Elias Marchand`, on the password named in `## Data model`. A second visitor-facing role has misread the product.

## Core features

### The maintainer's sign-in

Email and password are exchanged for a bearer token. The password is stored under a modern memory-hard password hash and never in any recoverable form. The client sends the token as a bearer credential on every studio API call, and the same token is carried in an http-only cookie so a server-rendered studio page is authorised before any script runs. Tokens expire.

1. A sign-in carrying the wrong password is turned away, and what comes back reads exactly as it does for an address nobody has heard of: nothing in the refusal tells a caller which half was wrong.
2. Signing out ends the bearer token's life, and a later request carrying that same token is turned away.
3. An expired token puts the maintainer back at the sign-in page with the pending work unwritten.
4. No sign-in control appears on any public route, and no public route links to `/login`.

### The tour

One route, one continuous scroll, no chrome below the header and no visible section breaks.

1. The tour holds one stage fixed in the window for its whole scroll range. The document scrolls; the stage does not.
2. There are exactly twelve narrative stops, addressed as fragments in this order: `intro`, `toolbox`, `intuitive`, `composition`, `scroll`, `staggering`, `svg-utilities`, `draggable`, `clockwork`, `responsive`, `modules`, `sponsors`.
3. **The current stop is derived continuously from scroll position**, never from an arrival callback alone, because it drives a continuous parameter rather than a discrete class. At any position between two stops the instrument is partway between two states rather than holding one until it snaps.
4. Each stop does four things together at its boundary: it swaps the headline and subheading pair beside the stage, it rebinds the colour alias to that stop's module family, it lights that module's arc on the instrument's ring, and it swaps the object inside the ring.
5. **Scrolling upwards reverses the tour exactly.** The headline pair leaves and enters on the two centred motions named in `## Front-end specification`, driven by scroll position rather than played on entry, so nothing is triggered once and left behind.
6. The opening headline is split into words and characters and assembles on load rather than on scroll. The install line and the secondary call sit **outside** the stage, so they are usable and copyable before the scene has loaded and remain usable when it never loads at all.
7. Deep-linking to a stop's fragment lands on that stop without playing the stops in between.
8. The tour closes with a grid of twelve module tiles above the footer. Each tile carries a colour dot in its module's brightest step, the module name in the monospace at uppercase, and a trailing arrow, and leads to that module's documentation route.
9. **Pointing at a module tile lights that module's arc on the instrument further up the page.** This is the most distinctive interaction on the site and it connects two components that are far apart on screen; a build that treats the tile grid as an isolated component will not produce it.
10. There is no hover on a touch device, so there the arc that is lit belongs to the module currently in view.

### The instrument

The stage's contents. It is the most expensive single component in the build and the one most likely to be mistaken for an illustration.

1. It is a perspective scene: a camera, a ground plane, a warm rim light and one object per module, drawn inside a ring of graduation marks and coloured arcs.
2. **The ring, its graduation marks and its coloured arcs are drawn geometry that lives outside the scene.** This is the single most important structural decision on the tour: it is what lets the tour survive losing the scene entirely, keeping its structure, its colour changes and its narrative while losing only its centrepiece. A build that puts the ring inside the scene loses everything at once.
3. The graduation marks are transformed **individually from one shared parameter**, never rotated as a group. A single rotating container cannot produce the dozens of distinct mark positions a single scroll pass requires, and the difference is a dial being turned by hand rather than a wheel going round.
4. Each arc changes only its glow, ramping between off and on as the tour reaches that module's stop.
5. Four inputs drive it, additively: scroll position sets the current stop and the interpolation between stops; the current stop selects the object and the alias binding; the pointer adds a small bounded parallax; and elapsed time gives a slow idle rotation and the particle drift.
6. The object swaps without a visible load pause, which means the next stop's object is prepared while the current one is on screen. **At most two objects are resident at a time: the current stop's and one lookahead.**
7. It degrades through four states in this order, and the ordering is not optional. Rendering normally: full behaviour. Under a reduced-motion preference: one static frame at the current stop, with no idle rotation and no drift, and it is **not** removed, because removing it leaves the headlines floating against nothing. Scene unavailable or an object failing to arrive: the ring, the marks and the arcs render alone and the headlines behave normally. A sustained frame-rate drop: the ring and marks alone, and no further objects are loaded.
8. **The scene pauses when the tab is hidden or the tour is scrolled out of view.** A live scene left rendering in a background tab is the fastest way for a site of this shape to earn a reputation for flattening batteries.
9. Which degradation state the page is in is recorded as an event, so the rate of degradation is watchable.

### The documentation shell

1. Three columns: the module tree, a column of live demonstration panels, and the article. The header sits above all three and carries the version control and the search field on these routes and on no others.
2. The tree lists sixteen modules in one fixed order, and that order is a content property rather than something written into the page. The current module expands in place to reveal its child pages, indented, and **only one module is expanded at a time**.
3. Two modules carry a `NEW` badge, on a ground of that module's dimmest step. **A badge expires on a date rather than being removed by hand**, and a badge set with no expiry fails the publish.
4. The demo column carries one panel per page in the current module, stacked in the module's own order, each with a label strip carrying the page name in the monospace at uppercase. Panels butt against each other with no gap and are square.
5. **A demo panel outside the window does not run.** A module with a dozen panels running at once is the second most common way this build becomes slow.
6. **The three columns stay in agreement, and the three-way synchronisation between them is a scroll-spy in one direction and navigation in the other.** Scrolling the article to a page's heading makes that page current in the tree and its panel current in the demo column. Activating a demo panel scrolls the article to that page. Activating a tree row scrolls the article to that page and scrolls the demo column to its panel. Two steppers in the header move between panels directly.
7. The version control sits beside the wordmark, reads the current version's label, and opens a list of the published versions newest first. Selecting one switches the **whole** documentation surface to that snapshot. The address does not change, because the version is a site-wide selection rather than a path segment, and the selection is remembered for that visitor across routes and across sessions.
8. **If the page the visitor is reading does not exist in the version they switch to, they land on that module's index in the target version with a notice, never on a not-found page.** Pages are added and removed between versions, and a naive implementation drops the visitor onto an error at the exact moment they were trying to check whether something existed yet.
9. `/documentation` with no module renders the sponsor wall as its article, with the tree and the demo column in their normal states. It is the only documentation route whose article is not reference material.
10. When a single demo fails, its panel keeps its label and its ground, shows nothing, and the article is unaffected. Under a reduced-motion preference every panel renders a static first frame and does not loop.

### A documentation page

1. An article carries its title, its body, inline code, specimen blocks with copy controls, and a stable anchor on every subheading derived from that subheading's own text and made unique within the page.
2. Below the body sits the in-section list: every child page of the current module, as a full-width row carrying the page name in the monospace at uppercase and a trailing arrow. **It is generated from the content store, not authored per page**, so a page added to a module appears in every sibling's list without anybody editing them.
3. **The pager walks the whole flattened tree.** The sequence is produced by walking the sixteen modules in tree order and, within each, its pages in their own order, so the last page of one module is followed by the first page of the next. A build that scopes the pager to the current module produces sixteen dead ends and breaks the single most useful reading behaviour the documentation supports, which is going through it front to back.
4. On the first page of the first module the previous control is **absent, not disabled**. On the last page of the last module the next control is absent. Everywhere else both are present, and each carries a direction arrow and the target page's own name.
5. A page with no children shows no in-section list at all rather than an empty one. A page with no demo leaves the demo column showing the module's other panels, with no placeholder.
6. A deep link to an anchor that no longer exists lands at the top of the page rather than failing.
7. Sponsor placements are part of the page's layout rather than injected into its prose, so an article whose tier has no sponsors configured has no empty space where they would be.

### Documentation search

1. The control sits in the documentation header: a field, a magnifier and two steppers. It is collapsed to its icon at narrow widths and open at wide. Focusing it expands the field and opens the results panel beneath it.
2. **The index is built ahead of time, one per published version, and served as a static artifact from the object store.** It is not a query against the database and it is not built in the browser from the rendered pages.
3. **The index is fetched on first use of the search control, never on page load.**
4. It carries one entry per page and one per subheading within a page, each with its module, its page, its heading path, its anchor and its searchable text.
5. **Code specimens are indexed.** The commonest documentation search is for a call name a developer half-remembers, and an index built only from prose will not contain it. Searching for `remap` finds `utilities/remap-and-clamp`, whose specimen is the only place that string occurs in version `4.5.0`.
6. Matching is prefix and substring and case-insensitive. A match in a title outranks a match in a heading, which outranks a match in body text. Results are grouped by module with the module named once, and the matched span is marked within the result row.
7. **Ties are resolved by the flattened tree order, never randomly.** Two runs of the same query return the same order.
8. The steppers move the highlighted result, the enter key opens it, and escape closes the panel and returns focus to the field. The whole control is operable from the keyboard without reaching for a pointer.
9. An empty query shows nothing, not a list of everything. A query with no matches shows a single row stating that, with the query shown back.
10. **When the index cannot be fetched the control stays usable and says search is unavailable**, and the tree remains the way to navigate. A query longer than `120` characters is truncated at that bound rather than sent.
11. The index is rebuilt whenever a version is published, and a published version whose index does not contain every page in it is a publish that should have failed.
### The curve editor

**The editor is a browser-only application.** It reads no server data and writes nothing anywhere. Every value it shows is computed in the browser from parameters held in the address bar. A build that puts its curve arithmetic behind a request has added a round trip and a failure mode to something that has neither, and has broken the editor's most valuable property, which is that dragging a handle updates the preview without waiting for anything.

1. Four panels: the preset grid, the plot, the preview and the export blocks.
2. The preset grid is organised by family. There are ten families and thirty-seven members: `spring` with `default`, `snappy`, `bouncy` and `strong`; `bezier`, `power`, `sine`, `expo`, `circ`, `back`, `elastic` and `bounce` with `in`, `out`, `in-out` and `out-in` each; and `linear` with one member. Each tile draws its own curve as a miniature plot and carries its name beneath it.
3. **Each family binds a colour family**, which is what colours its tiles, its plot and its preview together: `spring` to red, `bezier` to orange, `power` to yellow, `sine` to lime, `expo` to green, `circ` to turquoise, `back` to cyan, `elastic` to indigo, `bounce` to lavender and `linear` to pink.
4. The selection signal is the tile's asymmetric radius, which moves from a single softened corner when idle to a softened leading edge when active, inside a container that clips the grid so a tile's corner can change without escaping it.
5. **The plotted curve is a dense polyline sampled at a fixed step across the domain, never a single cubic segment**, because the spring family is not expressible as one.
6. Dragging a handle updates the curve continuously, with no request and no settling delay. Handles are clamped to the plot's domain, and the value range is allowed to exceed it so an overshooting curve is drawn honestly.
7. **Spring curves have no draggable handles.** They take a bounce and a duration rather than control points, and they are driven by their sliders and numeric fields alone. A build that assumes every curve has handles breaks on the springs, which are the first thing in the grid.
8. **Every handle is focusable and every parameter has a numeric field beside it.** Arrow keys nudge a handle, shift and arrow move it further, and home and end go to the bounds. The numeric fields are the accessible equivalent of dragging and they are what make the whole panel operable; a curve editor that can only be driven by dragging is unusable by anyone who does not use a pointer.
9. The reset control returns the current family to its defaults.
10. The preview runs four cells, one animating and three ghosted at successive offsets. **Below it the onion skin shows the trail of previous positions.** It is the panel's most useful feature and its least obvious: what a curve actually controls is where a moving thing spends its time, and a single square sliding past is too quick to show that. The trail bunches where the movement lingers. Below the plot a tick strip shows the same information in one dimension, a mark per sampled step, drawn from the same sample set as the curve.
11. Duration, loop delay and the two opacity endpoints are each a slider paired with a numeric field, and their values are shown in the drawn seven-segment readout.
12. Export carries two tabs, `CSS` and `JS`, and two blocks per tab: a short form naming only the curve, and a full form carrying the import and the call. Both have their own copy control. **Every export is generated in the browser from the current parameters on every change and is never fetched.**
13. **One sampler feeds the plot, the tick strip, the preview and the exported code.** That is what guarantees the drawn curve, the moving square and the generated snippet agree; computing them separately is how they come to disagree in the third decimal place.
14. Exported numbers are rounded to the precision the controls expose: three decimal places for a control point, two for a bounce or a duration. This is what stops a slider emitting a value like `0.5000000000000001`.
15. **The family, the member and every parameter live in the address.** The keys are `family`, `member`, `p1x`, `p1y`, `p2x` and `p2y` for a control-point family, and `family`, `member`, `bounce` and `duration` for the spring family. Pasting an address reproduces the exact curve.
16. **The address is replaced rather than pushed.** Pushing a history entry per drag frame means the back control takes several hundred presses to leave the page.
17. An absent or invalid address falls back to the first family's default, without an error.
18. Under a reduced-motion preference the preview holds a static frame and **the onion skin still renders**, because it is a diagram rather than a motion.

### The subscription lifecycle

The only thing a visitor can change. It gets full depth because it is the whole write surface of the product.

1. Two surfaces feed two separate lists through one first-party endpoint: the card on the course page writes to `course_waitlist`, and the joined field and submit pair in the footer writes to `newsletter`. **Joining one is not consent to the other**, and the same address on both lists is two rows.
2. **The form is first party and works without any third-party script**, and it works with scripting disabled entirely, because it is an ordinary form posting form-encoded fields to the app's own endpoint.
3. The flow is: the visitor submits an address; the server validates it; a `pending` row is created or an existing one refreshed; a confirmation message is queued; the form reports that a confirmation has been sent; the visitor opens the link; the token is verified and consumed; the row becomes `confirmed` and a confirmation page renders.
4. **Step five is a specific requirement: the form says a confirmation has been sent, never that the visitor is subscribed.** Reporting success before confirmation trains visitors to ignore the mail, and it makes the subscriber count a count of people who typed something rather than people who wanted it.
5. A confirmation token carries at least `128` bits from a cryptographic source, is stored only as a digest so the token itself is never at rest, expires `7` days after it is issued, and is single use. A second use of a consumed token reports that the address is already confirmed rather than an error. An expired token lands on a page offering to send a new one. **The link is the only place the token ever appears.**
6. Re-submission is idempotent by the address and the list together. An address already `pending` has its row refreshed and a new confirmation sent, subject to the resend limit. An address already `confirmed` is **reported as success and no message is sent**. An address previously `unsubscribed` begins a new pending cycle, because unsubscribing is not a permanent ban. An address that `bounced` or `complained` is reported as success and no message is sent. The same address submitted twice in quick succession produces one message, not two.
7. **Rejections are reported identically to the submitter whatever the reason.** Telling an anonymous submitter whether an address is already on a list turns the form into a way of testing whether a particular person signed up.
8. Validation: presence and shape are checked on the client as an assist and on the server as the check; the address is trimmed and lowercased for comparison and stored as submitted; a length bound is enforced before any parsing; disposable and role addresses are accepted rather than blocked, because blocking them is a support burden with no benefit here; and deliverability is not checked synchronously, because a bad address is discovered by its bounce.
9. **The form is the one genuinely dangerous surface on this site, because it makes the app send a message to an address somebody else typed.** It is defended by four controls together. At most `3` submissions per address per hour and at most `20` per network origin per hour, the address limit being the binding one. At most `2` confirmation resends per address per day. A decoy field named `company_website`, which no human fills and any filled value refuses. And a timing token issued with the form, so a submission arriving less than `2` seconds after the form was served is refused. Repeated rejection from one origin lengthens that origin's window rather than blocking it outright, and there is never a visible puzzle.
10. A global ceiling of `200` queued messages per hour trips an alert rather than silently dropping work.
11. Lifecycle events arrive as signed callbacks and set state: delivered is recorded; a hard bounce moves the row to `bounced` with no further sends; a soft bounce is retried and then becomes `bounced`; a complaint moves the row to `complained` with no further sends, permanently; and an unsubscribe moves it to `unsubscribed`. **Every one of those callbacks is verified by signature, is idempotent by the provider's own event identifier, and tolerates arriving out of order.** An unverified callback that can set a subscriber's state is an open interface for anyone who guesses the address.
12. The unsubscribe link is reachable from every message sent and works once.
13. Retention: a `pending` row never confirmed is deleted after its token expiry plus a grace period; an `unsubscribed` row keeps the address as a digest only, so the unsubscribe can be honoured; a `complained` row keeps the digest permanently, so a complaint cannot be undone by resubmitting; and a rate-limit fingerprint is kept only as long as its window.
14. The form never collects a name, a company or any other attribute. It asks for one field and the record stores one field.

### Funding and sponsorship

Sponsorship is the only income this project has and it appears on more surfaces than any other single concern, so it is specified once and referenced from each.

1. **Tiers are ordered rows, not two hard-coded groups.** A third tier is a content change and needs no code change. A tier carries its slug, its display name, its rank, the set of surfaces it appears on and the size of its mark box.
2. The seeded tiers are `upper` at rank `1`, placed on the documentation landing page, on documentation pages, on the tour's twelfth stop and at the tour's opening; and `lower` at rank `2`, placed on the documentation landing page and on the tour's twelfth stop. A card appears on a surface if and only if its tier's placement set names that surface.
3. **The last card in every tier group is the recruitment card**: the same shape, an outline mark and a label inviting the visitor to take the empty slot. It is present whether or not the tier is full, which is the point of it.
4. Ordering within a tier is stable and explicit, from the sponsor's own position, never from the order a fetch happened to return.
5. The roster is reconciled **on a schedule and server-side**, never fetched from the browser at render time, and every mark is stored as a first-party object afterwards.
6. **When the roster source is unavailable the last good roster is served and its age is recorded.** A sponsor who paid for a placement and finds it missing because a third-party interface was briefly unavailable is the worst failure this system can produce, and serving yesterday's list costs nothing.
7. A sponsor absent from a fetch is marked inactive by setting its end date. **It is never deleted**, so a resync restores it and the record of what was shown when survives.
8. **A sponsor with no mark renders its name in place of the mark, never a broken image.**
9. An empty tier renders the recruitment card alone, with no empty tier heading above it.
10. Every funding call leads outward to the sponsorship platform. **The site takes no payment itself**, which is the reason there is no payment machinery anywhere in this brief.

### The advertising slot

One slot in the footer, distinct from sponsorship, with its own attribution link that is deliberately one step dimmer than every other link on the site.

1. When it fills, it renders at its reserved size and fades in.
2. When it is empty it collapses to nothing: no placeholder, no gap and no message.
3. When it is blocked it behaves exactly as empty, and **the site makes no attempt to detect that it was blocked and says nothing about it.** A project funded by goodwill should not spend that goodwill nagging people.
4. When it is slow it holds its reserved space and fades in when it arrives, so the footer does not shift under somebody's finger.
5. Its content runs in a bounded context that cannot reach the document around it.

### The content pipeline

The maintainer is not a user of the public site. Documentation is authored outside it and published into it as a complete snapshot.

1. A version is built in the `draft` state, validated, indexed, and only then promoted. **Atomicity is the rule the whole pipeline is built around: a publish is atomic, and a visitor must never see pages from a new snapshot beside a tree from the old one, or an article whose index has not been rebuilt.**
2. **At most one version is current at any moment**, and the second attempt to mark a version current is refused by the database rather than merely absent from the code.
3. Nine checks run before promotion and any one of them fails the publish rather than producing a broken site. The flattened sequence has a gap or a duplicate. Two modules share a position. A module names a colour family that is not one of the twenty-one. A page's anchors are not unique within it. **An internal link points at a page or an anchor that does not exist in this version.** A page references a demo that does not exist. A badge is set with no expiry. The built index does not contain every page in the version. A page belongs to no module, or a module holds no pages.
4. **The internal-link check is the one that earns its cost.** Documentation cross-references break constantly as pages are renamed, and a reader who follows a link into a not-found page has been failed by the publish rather than by the site.
5. When validation fails the draft snapshot is discarded and nothing was ever visible.
6. Promotion moves the current flag in one transaction, purges the caches for that version, and leaves the previous snapshot **readable through the version control** rather than deleting it. A pipeline that deletes the previous snapshot breaks the only reason the version control exists.
7. **A draft version is viewable before promotion at its own preview key and at no other address.** That address appears in no sitemap, in no search result and in no internal link on a published page, its documents carry a directive telling indexers to leave it alone, and a signed-out caller reaches none of it.
8. The route list is derived from the content store and never from the rendered navigation, because a page the navigation does not yet link is still a real page and a navigation-derived list would miss it.
9. The sponsor roster is on its own schedule and is not part of a documentation publish.

### The chrome, the error routes and what the site stores

1. Every route carries the same header and the same footer, and both are static: neither ever waits on a fetch.
2. **An address that does not resolve renders the site's own not-found page and answers not-found.** No address ever renders the tour with a success status. The page carries a heading, one line of explanation and three ways out: the tour, the documentation and the editor.
3. **When the failed address looked like a documentation page, the not-found page offers the search control with the failed segment already filled in.** Most of those are a page that moved between versions, and a half-finished search finds it far more often than a list of links does.
4. The server error page is the same centred column without the search offer, answers server-error, and carries a retry control.
5. **Every internal link on every published route resolves to a route that exists and answers.** A link into nothing is a defect the build catches rather than a thing a reader discovers.
6. A privacy page is reachable from the footer of every page and states exactly what the site stores: an address on a list and its confirmation state, a count of page views by route, and nothing else. It states plainly that no name, no company, no behavioural profile and no cross-site identifier is kept, that a search query's text is never recorded, and how a visitor asks for their address to be exported or erased.
7. **A first-time visitor is asked once about non-essential storage**, in a bar anchored to the foot of the page and never a modal, with refusing exactly as easy as accepting. The answer survives a reload. **Until the answer is yes, nothing non-essential is written**: the remembered documentation version and the local page-view record are both held back, and the analytics events are dropped rather than queued.
8. The site records each page view with its route and the moment it happened, readable by the maintainer and by nobody else. **Nothing is sent to any outside address.**
9. The analytics it keeps are these and no others: a route viewed with its documentation version and its viewport class; a tour stop reached with its index and the furthest reached this session; a specimen copied with its route, page and block; a search performed with the query's **length and result count and never its text**; a search result activated with its rank; a curve changed with its family and member and never its parameter values; an export copied with its language, form and family; a subscription submitted with its list, source route and outcome class; a funding call activated with its placement; a demo that failed with its page and error class; and a scene degradation with its state.
10. **The search query's text is never recorded anywhere**, in analytics or in a log. It would be the single most useful field on the site and also the one most likely to contain a private project name.
11. The visitor identifier is scoped to a session and is never persisted, and there is no cross-site identifier of any kind. **What is deliberately not collected is the longer and more interesting list**: the text of a search, the address in a subscription, any cross-site identifier, any persistent per-visitor identifier, a precise location where a country class is sufficient for any decision this site makes, and scroll depth as a continuous stream where the stop index carries the same information at a fraction of the volume.
12. Analytics never block an interaction, are batched and flushed on a timer and when the page is hidden, and fail silently.

### Specimens and the clipboard

Copying a snippet is the most valuable action in the documentation and the second most valuable in the editor, so the block and its control are a component rather than a detail.

1. A specimen block carries its source in the monospace on a recessed ground, themed from the code palette and **never from the current section's colour family**, so the same snippet does not change appearance between one page and the next.
2. Long lines scroll sideways inside the block and never widen the page, and nothing wraps.
3. The block's text is selectable, and selecting it does not trigger the copy control.
4. **A specimen is rendered as text and is never executed by the page that shows it.** Documentation for an animation engine is full of code, and a build that renders a specimen as markup has turned every example into an injection.
5. The copy control sits at the block's top right over a backdrop blur so it stays legible over code, swaps to a confirmation mark when it has worked, and reverts.
6. **It copies the specimen's source text, never the rendered highlight markup**, strips a trailing newline, and preserves indentation exactly including leading tabs and spaces.
7. The confirmation is announced to assistive technology.
8. **When the clipboard is refused, the block's text is selected instead so the visitor can copy it by hand.** This is a requirement rather than a defensive courtesy: clipboard access is refused in more situations than most builds anticipate, and a control that silently does nothing is worse than no control.
9. **On a touch device the control is permanently visible rather than revealed**, because there is no pointing there and this is the action that matters most.
10. The install line at the opening of the tour is a specimen with its own copy control, and it must work before the scene has finished loading, which is why it cannot live inside the stage.

### Demonstrations and their isolation

1. A demo is content: it carries its own source, its parameters and a poster seed, and it is stored with the version it belongs to.
2. **Each demo runs in a bounded context that cannot reach the host document**, cannot navigate, cannot write to storage and cannot reach the network beyond its own assets.
3. A demo that exceeds a time or a memory bound is stopped, and a failing demo **blanks its own panel and affects nothing else**.
4. **A demo that cannot run shows its generated poster rather than an empty panel.** The poster is generated deterministically from the demo's own seed, so the same page produces the same still on every build and a rebuild does not invalidate every image on the site at once.
5. A demo failing is recorded as an event with its page and its error class, so a content defect on one page is visible rather than silent.

### Background work and what is watched

1. Ten jobs exist: `send_confirmation` when a subscription is accepted; `send_welcome` when one is confirmed; `process_mail_events` when a provider callback arrives; `sync_sponsor_roster` on a schedule; `sweep_expired_subscriptions` daily; `expire_badges` daily; `rebuild_index` when a version is published; `purge_caches` when a version is published; `warm_caches` after a purge; and `check_roster_freshness` on a schedule.
2. Delivery is at least once, so **every consumer is idempotent**: a send is keyed by its subscription, a callback by the provider's event identifier.
3. Retries use exponential backoff with jitter and a bounded attempt count of `5`. **An exhausted job moves to a dead-letter store and raises an alert; it is never discarded.** A job that fails deterministically is dead-lettered rather than retried forever.
4. Ordering is never assumed.
5. The confirmation send is enqueued within the request and before the response, and the response does not wait for it. When the provider is unavailable the job holds in the queue and retries and the row stays `pending`, so **no submission is ever lost and the visitor never sees an error belonging to a company they have never heard of.**
6. **A scheduled job takes a lock, so two runs cannot overlap.** A missed run is not backfilled; the next run reconciles from current state.
7. **The expiry sweep counts what it would delete and refuses to run when that count exceeds `500` rows.** A clock error or a migration mistake that made every row look expired would otherwise delete the entire mailing list in one go, and the mailing list is the only thing on this site that could not simply be rebuilt.
8. `expire_badges` clears a `NEW` badge whose expiry has passed, which is why a badge is a dated content property rather than a flag somebody remembers to remove.
9. `check_roster_freshness` raises an alert when the roster is older than `24` hours.
10. What is watched: the submission rate and its outcome mix, the confirmation queue depth, the dead-letter depth, the count of callbacks whose signature failed, the roster's age, the publish outcome and which check failed, the index's size and fetch time, the route error rate by status, the scene degradation rate by state, the demo failure rate by page, and the advertising fill rate.
11. **A confirmation queue that is not draining is the highest-severity alert on this site.** Every other failure degrades something a visitor can see and work around; a stuck queue silently loses the one thing that cannot be recovered.
## User flow

One origin carrying four groups of addresses: the public site, the documentation, the studio, and the two addresses a mailed link lands on.

| Route | Purpose | Auth |
|---|---|---|
| `/` | The tour: twelve stops against the pinned instrument, then the module grid | public |
| `/documentation` | The shell, with the sponsor wall as its article | public |
| `/documentation/<module>` | The shell, with that module's index as its article | public |
| `/documentation/<module>/<page>` | The shell, with one article | public |
| `/easing-editor` | The curve editor | public |
| `/learn` | The course waiting list | public |
| `/privacy` | What the site stores, and how to have it erased | public |
| `/confirm` | Where a confirmation link lands | public |
| `/unsubscribe` | Where an unsubscribe link lands | public |
| `/sitemap.xml` | Every published public route, derived from the content store | public |
| `/login`, `/logout` | The maintainer's sign-in and sign-out | public |
| `/studio` | Versions, modules, pages, demos, roster, outbox, jobs, page views | maintainer |
| `/preview/<preview_key>` | A draft version, unlisted and not indexed | maintainer |

Addressing rules, which hold everywhere. No trailing slash, and an address with one is canonical without it. Lower case, kebab within a segment. At most three segments below the origin. **The documentation version is never a path segment**, because it is a site-wide selection rather than an address. Fragment addressing is used only by the tour, for its twelve stops. Query addressing is used only by the editor.

Entry and redirects. A visitor arrives at the tour. An address that does not resolve renders the not-found page and answers not-found; a documentation address that does not resolve offers the search control with the failed segment prefilled. A signed-out request for the studio or for a preview address is rejected and the caller is sent to the sign-in page, and the protected content is not served in the rejection.

**Install.** Land on the tour. The headline assembles from its own words and characters. Copy the install line with its copy control while the stage beside it is still filling. Follow the secondary call into the second stop.

**Read the manual front to back.** Scroll the tour to the twelfth stop and reach the module grid. Point at a tile and watch that module's arc light on the instrument above. Follow the tile into the module, read the article, copy a specimen, and press the pager's next control at the end of the module's last page to arrive at the first page of the next module. Repeat to the end of the manual without ever returning to the tree.

**Find a call.** Open the search control in the documentation header. Type a call name that appears only inside a code specimen. Step to the result with the stepper rather than the pointer, press enter, and land on the page at its anchor with its module current in the tree and its demonstration current in the column.

**Read an older version.** Open the version control beside the wordmark, choose the previous published version, and watch the whole documentation surface switch to that snapshot while the address stays as it was. Where the page being read does not exist in that version, land on that module's index with a notice. Move to another route and back, and the choice is still remembered.

**Design a curve.** Open the editor. Choose a spring from the grid and find it has no handles, only its bounce and its duration. Choose a bezier and drag a handle, or type into the numeric field beside it, and watch the plot, the tick strip, the preview and the export block all change together. Copy the short export form. Copy the address, open it again, and get the same curve back.

**Join the list.** Open the course page, submit an address, and read that a confirmation has been sent rather than that you are subscribed. Open the confirmation link and land on the confirmed page. Open the same link again and be told you are already confirmed rather than shown an error. Submit the same address a third time on the form and be thanked, with nothing sent.

**Publish.** Sign in as the maintainer. Open the draft version in the studio, correct the page whose internal link points at nothing, run the validation, watch it pass, and publish. The whole documentation surface switches in one step, the previous version stays readable from the version control, and the draft's preview address stops being the only way in.

States are specified with their surfaces in `## Core features` and their appearance in `## Front-end specification`. Every one of the site's outside dependencies has a stated degraded state and **none of them can take a page down**: the content store falling back to its cached copy with its age recorded, a single demo blanking its own panel, the scene leaving the ring and the narrative behind, the roster falling back to the last good list, the advertising slot collapsing silently, and search stating that it is unavailable while the tree still navigates.

## UI/UX notes

Somebody arriving here should understand in the first moment that this is a precision instrument for making things move, built by people who measure, and should feel that the page itself is a demonstration of the thing it is selling. Every later decision resolves against that sentence.

The register is a developer tool with a point of view, and it changes deliberately between surfaces. The tour may carry atmosphere and the subject itself is the first thing seen. The documentation is the most visited surface and somebody is reading it rather than admiring it, so it reads quiet and dense but organised, with stable positions and minimal chrome. The editor exists to be manipulated directly, so its result is always visible beside its cause and nothing waits on anything. Comprehension over atmosphere inside the manual, spectacle over restraint on the tour, instantaneity over everything in the editor.

Colour is the part of this system most likely to be rebuilt wrongly, because there are no flat colours to rebuild. There are twenty-one families of eight steps each, running from most saturated and lightest at step one down to nearly the page ground at step eight, and every one of them is addressable by family and step. Two of the families are structural rather than chromatic: a ground family every surface is drawn from, and a foreground family every piece of text is drawn from. Two further neutral families exist and are not interchangeable with those, one of them very nearly flat and used where a surface must read as a hole rather than a raised panel. The seventeen chromatic families are named in `## Front-end specification` and described there by family, tone and shade. The exact values are yours, so long as step one of each is recognisably its named hue and step eight is close enough to the ground to read as absence.

**The mechanism above the values is the one thing here that must not be simplified.** A documentation section does not use its family by name. It rebinds a single alias of eight steps to one of the families, and every component inside that section asks for a step of the current alias rather than for a family. That is why a whole chapter, from its entry in the tree to the small diagram beside it and the lines drawn inside that diagram, changes personality together when the reader moves from one chapter to the next, and why adding a seventeenth module is a content change and nothing else. A component below a section boundary that names a family directly is a defect, not a shortcut.

Code blocks are the exception and they are themed from their own palette, outside the family system entirely. A build that themes code from the current section makes the same snippet change colour between pages, which reads as a bug to every developer who sees it.

Typography carries three roles and there is no fourth. Everything that is not code is set in a variable grotesque with a wide weight axis and a shallow oblique. Code and interface labels are set in a monospace with a true italic. Numeric readouts in the editor are not set in a face at all: they are drawn as seven strokes per digit, lit strokes in the current family's brightest step and unlit strokes in a deep step at the same position, which is what makes a readout look like equipment rather than text and removes an asset at the same time. Two properties of the rendered scale are load-bearing and both are easy to lose: the interface is overwhelmingly a small monospace at a semibold weight, which is what makes the site read as a measuring instrument rather than a brochure, and **every headline has a line height below its own font size**, which is what produces the tight stacked look of the tour headlines. Sizes, leading and tracking are proportions of one base rather than fixed measures. The exact families are yours, so long as the weight axis is genuinely variable and figures line up in a column wherever numbers stack.

Space is one ladder of steps and type is a separate ladder, deliberately not the same numbers. Corners come from a short radius ladder, and several components carry asymmetric radii where the asymmetry is a signal rather than a decoration: a preset tile softened on one corner when idle and along its leading edge when active, which is the grid's entire selection signal; a joined field and submit pair softened only on their outer edges, which is what makes them read as one control; and a panel header softened at the top against a body softened at the bottom. Space over dividers: sections read as separate because of the room around them.

The product is designed dark and the dark scheme is the one that must be complete; a light scheme is declared and is optional, because the reference's light values were never observed rendered. Two meanings carry their own colour and appear nowhere else: the colour of an acceptance and the colour of a refusal, both used on the two subscription surfaces and on the publish validation, and a state that is neither may not borrow either. Motion is where this product argues for itself, so it is specified as character rather than as timing. Five curves and no sixth: one that overshoots and settles like a drawer with a soft close, one perfectly symmetric, one steep through the centre and slow at both ends, one that decelerates hard and late, and one gentle in and long out. Two habits give the site its feel and both are requirements: colour changes run about twice as fast as anything that travels, so pointing at something feels immediate while movement still feels considered, and there is one default interface duration for everything, quick enough not to be waited for and slow enough to be seen. Nothing uses a different speed to feel special, and there is no blanket rule that transitions every property, because such a rule quietly animates things nobody intended. The named moments are listed in `## Front-end specification`, and a build that names none of them ships none of them.

**Motion is gated on a positive preference for movement rather than merely switched off by a preference against it.** Under a reduced-motion preference nothing is scroll-driven, nothing drifts, nothing rotates, nothing staggers, and content appears in its final state. The instrument on the tour holds one still frame rather than disappearing, because taking it away leaves the headlines hanging in empty space. Nothing is left part way.

The layout archetype is a top navigation: the wordmark on the left, the version control and the search field on documentation routes only, five calls, and the funding call on a filled ground at the right. Density is generous on the tour and compact in the manual, where three columns of different kinds of information sit side by side and stay in agreement. The working surface is a grid of cards wherever a set of comparable things is being chosen from: the preset grid in the editor, the module grid at the foot of the tour and the sponsor wall are the same idea three times. **Each page leads with one primary action, visually distinct from every secondary one.**

Every control here is described by the states it draws, never by a measurement. There are five, all present on every control: at rest, under a pointer, held down, focused from a keyboard, and unavailable. An unavailable one announces itself by more than a change of colour, because colour alone is not a signal everybody receives. The hover vocabulary for text is deliberately narrow: one two-step lift from a mid neutral to a near-white, everywhere, with both duplicate label layers moving with it. The funding call is the only thing in the chrome that moves its ground rather than its text, which is what makes it read as a button among links. Escape closes any open panel and returns focus to the control that opened it. **Focus is a separate and louder state than hover, never a weaker one**, because it is the only signal somebody driving the page from the keyboard gets, and it is never suppressed to make things look tidier.

There is no hover on a touch device, so every hover effect has a non-hover equivalent: the lit arc belongs to the module in view, the bordered demo panel is the one in view, and the copy control is permanently visible rather than revealed. That last one matters most of all, because copying a snippet is the single most valuable action in the entire documentation and a control that appears only under a pointer does not exist on a phone.

Accessibility is contract here and three features on this site are actively hostile to assistive technology if they are built naively. A split headline must carry the intact original string as its accessible name with the fragments hidden, must be reversible, and must copy with its spaces intact. The scroll narrative must have every stop's text in the document at all times rather than injected on arrival, must follow visual order, must be reachable stop by stop from a keyboard, and must **not** announce a stop change, because announcing every change during a scroll produces a stream of interruptions. The editor must give every handle a role, a value and a name, must offer arrow, shift-arrow, home and end as the equivalent of dragging, must carry a numeric field for every parameter, and must announce a value change on the field rather than on every drag frame. Beyond those: a skip link first in the document, the tree and the demo column and the article as distinct named landmarks, the current page marked as current rather than merely coloured, the pager naming its destination rather than saying previous, search as a labelled combobox, and zoom to twice the size without loss of content or function. **Body text and its background meet the WCAG AA contrast bar, and the build measures every foreground and ground pairing rather than assuming the reference's choices pass**, darkening the ground or lifting the step where a pairing fails. The two dimmest foreground steps are dim by design, so this is the most likely accessibility defect in the whole design system.

The layout is responsive around one primary turning point with refinements above and below it, and two of its decisions depend on the window being tall rather than wide, which is unusual and is deliberate: the tour's stage and the editor both need vertical room more than horizontal. Above the turning point the manual is three columns, the tour puts its headline pair beside the instrument, and the editor fits the window. Below it the manual becomes one column behind a compact bar, and **the current demonstration survives as a small panel pinned in a corner rather than being dropped**, because hiding it would quietly remove the feature that makes the manual worth reading. At every width the document never scrolls sideways, every touch target stays at least a comfortable fingertip across, vertical sizing follows the dynamic viewport height so a phone whose browser chrome slides away does not clip the stage, and text reflows rather than scaling. Where the boundaries fall is yours, so long as the arrangement holds at every width between them.

Five things to design against. Each names a failure rather than a fashion, because fashions date and failures do not. A surface where one hue family does all the work and nothing else carries meaning. Ornament taking room that the subject wanted. A code specimen that shifts colour from page to page because it took the chapter's identity instead of its own. A ring drawn inside the scene, so a visitor on an older machine is handed an empty page where a plainer one was available. And a control that appears only under a pointer, which on a phone is a control nobody has.

## Technical requirements

The stack is fixed. The rendering model is server-rendered pages with interactive islands: **documentation and marketing routes are rendered ahead of time and served as complete documents**, because their content changes only when the maintainer publishes, and the tour, the editor and the demo panels hydrate their interactive parts on top of that. The frontend is **SvelteKit**, which renders every document, serves every static asset and is the only thing bound to the container-internal port. The backend is **FastAPI**, which serves the HTTP API and is reached on that same origin under the `/api` prefix, so a browser sees exactly one origin and one port. Content, versions, subscribers and job runs live in **PostgreSQL**, whose connection string arrives as `DATABASE_URL`. The four object schemes live in **MinIO**: its address arrives as `STORAGE_ENDPOINT`, the bucket name as `STORAGE_BUCKET`, and the credential pair as `STORAGE_ACCESS_KEY` with `STORAGE_SECRET_KEY`. What the outside world calls this app arrives as `APP_PUBLIC_URL` with `APP_PUBLIC_PORT`. None of that is written into the code: every host, port and credential is read from the environment at start, and both backing services are already running and waiting at those variables.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor - the only backing services available in this environment are PostgreSQL and MinIO, and reaching for anything else is a contract violation.

Auth is app-implemented and exists only for the maintainer: email and password exchanged for a bearer token, the password under a modern memory-hard password hash, the token expiring, and the same token carried in an http-only cookie so a server-rendered studio page is authorised before any script runs. `GET /api/health` returns `200` once the app is ready.

**The site is three front ends sharing one design system and one chrome, and keeping them apart is the most valuable structural decision in the build.** The scene code is fetched, parsed and executed on the tour and nowhere else. The editor's computation is fetched on the editor and nowhere else. The documentation is the most visited surface on the site, and a build that ships one bundle makes every reader of every manual page pay for a three-dimensional engine that page never draws.

Two pieces of shared state prevent two whole classes of disagreement, and both are required. On the tour, one controller derives the current stop and the interpolation from scroll position and every other component reads from it; a build where the headline, the arc, the object and the alias each work the stop out for themselves will show them disagreeing at stop boundaries. In the editor, one sampler produces the point set that the plot, the tick strip, the preview and the exported code all consume; computing them separately is how the drawn curve and the copied snippet come to disagree in the third decimal place.

**Text arrives first and everything else catches up.** A documentation article is readable before any demonstration has run and must not wait for one. The tour's headline, subheading, install line and secondary call are present and interactive before the scene loads. The editor shows a correct static plot before its own code has run, so somebody arriving at a shared address sees the right curve immediately. The waiting-list form is usable before any media payload is fetched. The header and the footer are static on every route and never wait on a fetch.

Every static asset is addressed by a digest of its own content, so a changed asset is a new address and no cache has to be invalidated for it. That is what keeps a publish's invalidation small enough to be atomic: only the rendered routes for the affected version and that version's index need purging, because everything else changed its address. A version change purges the whole documentation surface at once, which follows from the version being a site-wide selection, and a warm pass immediately afterwards fetches the tour, the documentation landing route and the most-read pages so the first visitor after a publish does not pay for the whole cold surface.

The index artifact is immutable per version and may be cached indefinitely. It is bounded in size, and when it exceeds that bound it is split per module and fetched per module on demand, because an index that grows past a single reasonable fetch turns the first search of a session into a visible pause, which is exactly the moment a reader is least patient.

Rendering rules that are requirements rather than optimisations. A demonstration outside the window does not run. The scene pauses on a hidden tab. Scroll work is driven from a frame loop reading a cached scroll position rather than from a layout read per event, and layout reads are batched so nothing reads after a write within a frame. Element transforms are composed from individually addressable channels rather than written as one combined string, because the scroll system and the hover states drive different channels of the same element from different sources and a combined string makes one erase the other. Whatever is promoted for a motion is un-promoted when the motion ends; leaving hundreds of elements permanently promoted costs more than it saves. **Nothing shifts after first paint on any route**: the stage, the demo panels and the advertising slot all occupy their space before they fill.

Security here is not the shape a product this size usually has, because there is no login for a visitor, no payment and no private data. The risks that remain are the ones an anonymous public site actually has. The subscription form is the one genuinely dangerous surface and is defended as `## Core features` describes. Every inbound provider callback is verified by signature and is idempotent by the provider's own event identifier. Authored content is rendered through a sanitising pipeline at publish time, with raw markup permitted only from an explicit allow list, and a specimen block is escaped as text so a code example is never executed by the page that shows it. External links carry no referrer and open in a new context. Every demonstration runs in a bounded context with no navigation, no storage and no network beyond its own assets, and is stopped when it exceeds its time or memory bound. Responses carry a strict transport policy, a no-sniff content-type policy, a frame-ancestors denial, a strict-origin-when-cross-origin referrer policy, and a policy denying camera, microphone, geolocation and payment. The content policy names every origin the site loads from with no wildcard source for scripts, permits no inline script except a nonce-bound one, and **restricts form actions to this origin**, which is the reason the subscription form is first party: a policy that lets a form post to a third-party origin has given away the one thing worth protecting. No credential, key or token appears in anything the browser downloads.

Every request leaves one structured line of JSON on standard output. The line names the method, the address asked for, the status returned, how many milliseconds it took, and an identifier minted where the request entered the app. That identifier comes back in the body of every error response, so a reader with a complaint and a reader with a log are looking at the same request. **No subscriber address is ever logged in full, no confirmation token is ever logged in any form, and no search query text is ever logged**, because a log holding those is a second unmanaged copy of the only irreplaceable record on the site.

Errors carry a stable machine code and a human sentence, never a stack trace. Validation is server-side always and client-side is an assist rather than the check. No request changes state on a read except the single-use confirmation, which arrives in mail and must work as an ordinary link, and which is mitigated by being high-entropy, expiring, single use, and reported as already confirmed rather than as an error on a second use.

**Performance is a budget rather than an aspiration, and the budget is stated so it can be checked.** A documentation article is readable before any non-text asset completes. The tour is interactive before the scene completes. The editor's plot updates within one frame of the pointer with no request in the path. The scroll on the tour holds its frame budget under a sustained scroll rather than meeting it on average. And nothing shifts after first paint on any route. Three asset classes dominate and each has a rule: media is never fetched until it is asked for, images are replaced procedurally and whatever remains is loaded lazily below the fold, and scripts are split per front end.

**What is cacheable is nearly everything, because nearly everything is rendered ahead of time.** Rendered routes are cached and revalidated on publish. Content-addressed assets are immutable and cached indefinitely. A version's index artifact is immutable and cached indefinitely. The two write endpoints are never cached. Text responses are compressed, the article's text is prioritised ahead of any demonstration, and at most the asset origin is preconnected.

**Naming conventions hold across the whole interface.** A slug is lower case and kebab within a segment. A colour family, a state and a job name are lower case with underscores where they carry more than one word. An object key follows the scheme pinned in `## Data model` and nothing writes an object outside those four schemes. An error carries a stable machine code and a human sentence and never a stack trace.

**Observability, alerting and logging are part of the product rather than an afterthought.** Logging is structured as described above and carries the request identifier on every line. Operational telemetry is distinct from the product analytics and covers the twelve watched signals listed in `## Core features`. Alerting ranks a confirmation queue that is not draining and a non-empty dead-letter store highest, a repeatedly failing publish and a stale roster and a rising scene degradation rate in the middle, and a rising demo failure rate and an advertising fill of zero lowest.

**The failure handling summary is one sentence: every dependency on this site is optional at read time.** The documentation is rendered ahead of time, the tour survives without its scene, the sponsor wall survives without its roster, search survives without its index, and the footer survives without its advertisement. The only hard dependency is the one that accepts a subscription, and even that queues rather than failing. That is the whole resilience posture, and a build that treats any dependency as required has misunderstood it.

**Recovery, per scenario.** A bad publish is recovered by promoting the previous version, which is why archived snapshots are retained. A lost queue is recovered by replay, which is safe because every job is idempotent. A corrupted index is recovered by rebuilding it from its version. A wrong roster sync is recovered by syncing again, which is why a sponsor is marked inactive rather than deleted. **Subscriber data is the only irreplaceable data here**, and it is the only thing in this product that needs a backup with a stated recovery point and a restore that has actually been tried.

Determinism is a requirement rather than a quality. A generated poster is deterministic in its seed. Search ranking ties resolve by tree order. The flattened sequence is recomputed for a whole version whenever a page moves, and a gap or a duplicate fails the publish rather than reaching a reader.

The app stays responsive with `3` versions, `16` modules and `48` pages in one published version, `20000` page-view rows and `5000` subscriber rows.
## Data model

Nineteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside the account so a grader can sign in.

**Identity.** `account` holds `id`, `email` unique and compared case-insensitively, `display_name`, `password_hash` and `created_at`. `session` holds `id`, `account_id`, `token_hash`, `expires_at` and `created_at`.

**Content.** `version` holds `id`, `label` unique, `sort_key`, `state` among `draft`, `published` and `archived`, `is_current`, `published_at`, `index_object_key`, `preview_key` unique, `created_at` and `updated_at`. `sort_key` exists because version labels sort wrongly as text and a control that lists them out of order is worse than one that lists none. `is_current` is a boolean, and at most one row in the table carries it true: the database refuses the second rather than leaving it to the application to remember.

`module` holds `id`, `version_id`, `slug`, `name`, `ramp`, `position`, `tile_position` which is absent for a module that has no tile on the tour, `object`, `badge` among `none` and `new`, and `badge_expires_at`. Unique on `version_id` and `slug` together, on `version_id` and `position` together, and on `version_id` and `tile_position` together.

`page` holds `id`, `version_id`, `module_id`, `parent_page_id` which is absent for a page directly under its module, `slug`, `title`, `body`, `position`, `flat_position`, `demo_id` which may be absent, `created_at` and `updated_at`. Unique on `version_id`, `module_id`, `parent_page_id` and `slug` together, and on `version_id` and `flat_position` together. `version_id` is carried on the page as well as on its module so a page can be looked up without walking to its module first.

**`flat_position` is stored rather than computed, and that is a decision rather than an optimisation.** The pager needs the previous and next page across the whole tree; computing that at request time is a recursive traversal on every render for a value that changes only at publish. Storing it makes the pager two lookups, and the uniqueness across the version turns a broken sequence into a refused publish rather than a dead end a reader discovers.

`page_anchor` holds `id`, `page_id`, `anchor`, `text` and `position`, unique on `page_id` and `anchor` together. One row per subheading, so a deep link can be resolved and a moved anchor can be detected.

`demo` holds `id`, `version_id`, `kind` among `inline` and `scene`, `source`, `parameters`, `poster_seed` and `poster_object_key`. `poster_seed` exists so a demo that cannot run has a deterministic still rather than an empty panel, and so the same page produces the same still on every build.

**Sponsorship.** `sponsor_tier` holds `id`, `slug` unique, `name`, `rank` unique, `placements` as a list of surface names, and `mark_scale`. Tiers are rows and not an enum, which is what makes a third tier a content change. `sponsor` holds `id`, `tier_id`, `name`, `mark_object_key` which is absent when the sponsor has no mark, `destination`, `position`, `external_id` unique, `active_from`, `active_to` which is absent while the sponsorship runs, and `synced_at`. `active_from` and `active_to` exist because sponsorship lapses, and a build that deletes a lapsed sponsor loses the record of what was shown when. `roster_source` holds `id`, `object_key`, `available`, `fetched_at` and `last_good_fetched_at`.

**The mailing list.** `subscriber` holds `id`, `email`, `list` among `course_waitlist` and `newsletter`, `state` among `pending`, `confirmed`, `unsubscribed`, `bounced` and `complained`, `confirm_token_digest` unique and absent once consumed, `confirm_expires_at`, `confirmed_at`, `unsubscribed_at`, `source_route`, which records which surface captured the address, `request_fingerprint`, `created_at` and `updated_at`. Unique on the lowercased address and the list together. **The emailed token is never stored, only its digest.** The two lists are separate rows for the same address by design: joining a course waiting list is not consent to a newsletter.

**What is deliberately absent from that table**: no name, no company, no marketing attribute and no behavioural profile. The forms collect one field and the schema stores one field.

`outbox_message` holds `id`, `subscriber_id`, `kind` among `confirmation`, `welcome` and `unsubscribe`, `state` among `queued`, `delivered` and `dead`, `attempts`, `next_attempt_at`, `idempotency_key` unique, and `created_at`. `mail_event` holds `id`, `provider_event_id` unique, `subscriber_id`, `type` among `delivered`, `bounced_hard`, `bounced_soft`, `complained` and `unsubscribed`, `signature_valid` and `received_at`.

**Operations.** `job_run` holds `id`, `job_name`, `state` among `running`, `succeeded`, `failed` and `refused`, `lock_token`, `started_at`, `finished_at` and `detail`. `dead_letter` holds `id`, `job_name`, `payload`, `reason` and `created_at`. `page_view` holds `id`, `route` and `viewed_at`. `analytics_event` holds `id`, `kind`, `attributes`, `session_key` and `created_at`, where `session_key` is scoped to one session and is never carried between them. `storage_choice` holds `id`, `choice` among `yes` and `no`, `fingerprint` and `decided_at`. `ad_slot_state` holds `id`, `state` among `fills`, `empty` and `slow`, and `updated_at`. `rate_limit_counter` holds `id`, `scope` among `address` and `origin`, `key`, `window_start` and `count`.

**Object keys.** Four key schemes, and every one of them is a real object in the object store rather than a row or a file on the app's disk. A version's search index is at `index/<version_label>/search-index.json`. A sponsor's mark is at `sponsors/<external_id>/mark.svg`. A demo's generated poster is at `posters/<version_label>/<module_slug>/<page_slug>.svg`. The sponsor roster document the sync job reads is at `roster/current.json`.

**Which values are derived rather than stored.** A page's readability is derived from its version's state, never from a flag on the page. A module's colour identity is derived from its `ramp` through one alias and is never stored per component. Which sponsor cards a surface carries is derived from each tier's placement set. Whether a badge shows is derived from `badge_expires_at` against the clock. The search index is derived from a version at publish and is then fixed as an object. A poster is derived from its demo's seed.

**Invariants, as properties of the running system.** Exactly one version is current, and the database refuses a second. Within a published version `flat_position` runs from `1` to the page count with no gap and no duplicate. Two modules in one version never share a position or a tile position. A module's `ramp` is one of the twenty-one named families. A page's anchors are unique within it. Every internal link in a published version resolves to a page or an anchor in that version. A draft version is readable only at its own preview key and only by the maintainer, and appears in no sitemap and in no search result. One address on one list is exactly one row, and the same address on the other list is a different row. A confirmation token works exactly once and its plaintext is nowhere at rest. The same address submitted twice in quick succession queues one message, not two. A provider callback whose signature does not verify changes nothing, and a repeated provider event identifier changes nothing the first one did not. The expiry sweep refuses to run when the count it would delete exceeds its threshold. A sponsor absent from a roster fetch is marked inactive and never deleted.

**Seed data.**

One account: `maintainer@example.com`, display name `Elias Marchand`.

Three versions. `4.4.0`, archived, sort key `0004.0004.0000`. `4.5.0`, published and current, sort key `0004.0005.0000`, index object key `index/4.5.0/search-index.json`. `4.6.0`, draft, sort key `0004.0006.0000`, preview key `pv_9f2c41be`.

Sixteen modules in version `4.5.0`, in this order, each with its colour family, its tile position on the tour where it has one, and the object its stop shows:

| Position | Slug | Name | Family | Tile | Object |
|---|---|---|---|---|---|
| 1 | `getting-started` | `Getting started` | red | none | `renderer` |
| 2 | `timer` | `Timer` | sky | 1 | `timer` |
| 3 | `animation` | `Animation` | orange | 2 | `animate` |
| 4 | `timeline` | `Timeline` | yellow | 3 | `timeline` |
| 5 | `animatable` | `Animatable` | lavender | 4 | `spring` |
| 6 | `draggable` | `Draggable` | green | 5 | `draggable` |
| 7 | `layout` | `Layout` | lime | 6 | `scroll` |
| 8 | `scope` | `Scope` | turquoise | 7 | `scope` |
| 9 | `events` | `Events` | corail | 8 | `shield` |
| 10 | `svg` | `SVG` | cyan | 9 | `svg` |
| 11 | `text` | `Text` | magenta | 10 | `stagger` |
| 12 | `utilities` | `Utilities` | king | 11 | `engine` |
| 13 | `easings` | `Easings` | indigo | 12 | `easing` |
| 14 | `waapi` | `WAAPI` | sega | none | `waapi` |
| 15 | `engine` | `Engine` | citrus | none | `engine` |
| 16 | `adapters` | `Adapters` | purple | none | `renderer` |

Fourteen objects serve sixteen modules, so two modules may bind the same object. `text` and `adapters` carry the `NEW` badge, both expiring on `2026-12-01`. Version `4.4.0` carries the same sixteen modules without those two badges.

Three pages per module in version `4.5.0`, giving forty-eight pages whose `flat_position` runs from `1` to `48` in module order and then page order:

| Module | Pages, in order |
|---|---|
| `getting-started` | `installation`, `imports`, `your-first-animation` |
| `timer` | `create-timer`, `timer-methods`, `timer-callbacks` |
| `animation` | `create-animation`, `animation-properties`, `animation-playback` |
| `timeline` | `create-timeline`, `timeline-positions`, `timeline-playback` |
| `animatable` | `create-animatable`, `animatable-settings`, `animatable-methods` |
| `draggable` | `create-draggable`, `draggable-axes`, `draggable-callbacks` |
| `layout` | `layout-measure`, `layout-transitions`, `layout-callbacks` |
| `scope` | `create-scope`, `scope-methods`, `scope-cleanup` |
| `events` | `event-types`, `event-listeners`, `event-cleanup` |
| `svg` | `morph-to`, `motion-path`, `draw-line` |
| `text` | `split-text`, `split-options`, `split-cleanup` |
| `utilities` | `random-and-round`, `set-and-get`, `remap-and-clamp` |
| `easings` | `linear-and-power`, `spring-and-elastic`, `custom-curves` |
| `waapi` | `waapi-animate`, `waapi-convert`, `waapi-limits` |
| `engine` | `engine-settings`, `engine-timing`, `engine-lifecycle` |
| `adapters` | `adapter-overview`, `adapter-usage`, `adapter-limits` |

So `getting-started/installation` is at `flat_position` `1` and has no previous page, `getting-started/your-first-animation` is at `3` and is followed by `timer/create-timer` at `4`, and `adapters/adapter-limits` is at `48` and has no next page.

Forty-seven demos: one for every page except `adapters/adapter-limits`, which has none. The three pages of `svg` carry demos of kind `scene`; the other forty-four are `inline`.

The string `remap` occurs in version `4.5.0` only inside the specimen block on `utilities/remap-and-clamp`, and nowhere in any title, heading or body text. Version `4.4.0` carries the same sixteen modules and the same forty-eight pages, except that it has no `text` module at all, so `text/split-text` does not exist in it.

Version `4.6.0` is a draft carrying one page, `getting-started/installation`, whose body holds an internal link to `getting-started/configuration`, which does not exist. That draft therefore fails the internal-link check until the link is corrected.

Two sponsor tiers. `upper`, named `Upper`, rank `1`, placed on `documentation-landing`, `documentation-page`, `tour-stop-twelve` and `tour-opening`. `lower`, named `Lower`, rank `2`, placed on `documentation-landing` and `tour-stop-twelve`.

Six sponsors. In `upper`: `Northlight` at position `1` with external id `spn_northlight`, and `Tessera` at position `2` with external id `spn_tessera`. In `lower`: `Vantive` at position `1` with external id `spn_vantive`, `Plinth` at position `2` with external id `spn_plinth`, `Ravelin` at position `3` with external id `spn_ravelin` **and no mark, so its name renders in place of one**, and `Corvid` at position `4` with external id `spn_corvid`, whose sponsorship ended on `2026-08-31` and which is therefore inactive but still present.

One roster document at `roster/current.json`, available.

Five subscribers. `confirmed@example.com` on `course_waitlist`, confirmed. `pending@example.com` on `course_waitlist`, pending, with an unconsumed token that expires on `2026-09-23`. `expired@example.com` on `newsletter`, pending, with a token that expired on `2026-09-09`. `complained@example.com` on `newsletter`, complained. `unsubscribed@example.com` on `newsletter`, unsubscribed.

One advertising slot state, `fills`.

**Money, time and casing.** There is no money anywhere in this product. Times are UTC. A version label is stored as written. A slug is kebab-case and lower. A colour family name is lower case.

Seeding must be idempotent: restarting the app must not duplicate a row.
## Front-end specification

This section carries the visual and structural detail that `## UI/UX notes` states as intent. Everything here is a requirement on what a reader sees, never a value to copy: no colour is given as a code, no space as a measurement, no type as a size, no motion as a timing and no curve as a definition. Where a value is left out, the sentence that replaces it is the requirement, and the choice is yours so long as the sentence stays true.

### Machine-readable hooks

Everything else in this section is a requirement on appearance, and the value is yours. These are not: each attribute name below, and each value it takes, is inspected, so each one is written here letter for letter and must appear exactly as written. Where a hook takes a value, that value is given after the name.

| Attribute | Where it sits, and what it carries |
|---|---|
| `data-skip-link` | the skip link, first in the document |
| `data-primary-action` | the one primary action on a route, and no second element carries it on that route |
| `data-stop` | each of the tour's twelve stop sections, carrying that stop's fragment name |
| `data-current-stop` | the tour's stage, carrying the fragment name of the stop currently in view |
| `data-scene-state` | the tour's stage, carrying `full`, `reduced_motion`, `scene_unavailable` or `low_power` |
| `data-module-tile` | each tile in the tour's closing grid, carrying that module's slug |
| `data-arc` | each coloured arc on the instrument's ring, carrying that module's slug |
| `data-arc-lit` | each arc, carrying `true` when the arc is lit and `false` when it is dark |
| `data-tree-item` | each row of the documentation tree, carrying that module's slug |
| `data-tree-expanded` | each tree row, carrying `true` when the row is expanded and `false` when it is closed |
| `data-demo-panel` | each demonstration panel, carrying the module slug, a solidus, then the page slug |
| `data-demo-running` | each demonstration panel, carrying `true` while the demonstration is running and `false` otherwise |
| `data-current` | whichever tree row, demonstration panel or search result is current, carrying `true` |
| `data-pager` | each pager control, carrying `previous` or `next` |
| `data-in-section` | the container holding the module's sibling pages beneath an article |
| `data-search-field` | the documentation search field |
| `data-search-result` | each search result row, carrying the module slug, a solidus, then the page slug |
| `data-version-control` | the version control beside the wordmark |
| `data-version-notice` | the notice shown when a page is absent from the chosen version |
| `data-preset-tile` | each preset tile in the editor, carrying the family name, a solidus, then the member name |
| `data-preset-active` | the chosen preset tile, carrying `true` |
| `data-handle` | each draggable control point in the plot, carrying `1` or `2` |
| `data-onion-skin` | the onion skin beneath the editor's preview |
| `data-export-block` | each export block, carrying the tab name, a solidus, then `short` or `full` |
| `data-copy-control` | each copy control |
| `data-copy-state` | each copy control, carrying `idle` at rest and `copied` once the copy has worked |
| `data-specimen` | each specimen block |
| `data-sponsor-card` | each sponsor card, carrying that sponsor's external identifier |
| `data-recruitment-card` | the recruitment card closing each tier group |
| `data-ad-slot` | the advertising slot in the footer |
| `data-ad-state` | the advertising slot, carrying `fills`, `empty` or `slow` |
| `data-storage-bar` | the bar asking once about non-essential storage |
| `data-storage-accept` | the control accepting non-essential storage |
| `data-storage-refuse` | the control refusing non-essential storage |
| `data-success-message` | the success message on either subscription surface |
| `data-error-message` | the error message on either subscription surface |

Every editor handle carries a role, a current value and an accessible name saying which control point the handle is, because the same element is both a machine-readable hook and the thing a keyboard user drives.

### The token layer

One token layer, declared once at the root and consumed everywhere, in seven families: colour ramps, spacing, type, radius, transform channels, layout measures and easings.

**Colour is declared as twenty-one ramps of eight steps.** Step one of a ramp is its most saturated and lightest form and step eight is close enough to the page ground to read as absence. Nothing in the build declares a flat colour outside the ramps, and no component names a chromatic ramp directly.

**Spacing is one ladder of ten steps**, from a hairline gap through to a very large one, and every gap, margin and padding in the build is a step of it. The gap between major sections is a small multiple of the gap beneath a heading, and roughly halves on a narrow screen.

**Type is a second ladder of ten steps, deliberately not the same numbers as the spacing ladder.** It runs from the smallest caption through the dominant interface label, the article body, three headline steps and one very large display step.

**Radius is a ladder of five steps**, from barely softened to generously rounded.

**The transform channels are individually addressable and each defaults to identity**: three translations, four rotations, four scales, three skews and a perspective. **An element's transform is composed from those channels and is never written as one opaque string.** This is what lets the scroll system and the reveal motions drive different channels of the same element from different sources without overwriting each other; a build that writes a single combined transform will find its scroll-driven horizontal movement erasing its hover-driven scale.

**The layout measures that must be named tokens rather than repeated numbers**: the fixed header's height, the documentation tree column's width, the demo column's width, one demo panel's height, the label strip above a demo panel, the gap between demo panels which is zero so the panels butt against each other, the demo panel's radius which is zero so the panels are square, and the dynamic viewport height so a phone whose browser chrome slides away does not clip the tour's stage.

**The inset trio** is how a specimen block breaks out of the article measure to sit edge to edge: an inset padding, a negative margin equal to one axis of it, and a compensating width. Reproduce all three together or the block is the right colour and the wrong width.

### The ramps, by family and tone

Twenty-one ramps. Two are structural, two are neutral companions that are not interchangeable with them, and seventeen are chromatic. Every one runs eight steps in the same direction.

| Ramp | Step one | Step eight | What it is for |
|---|---|---|---|
| ground | a deep neutral, and it is the page ground itself | a deep neutral, seven steps lighter | every surface |
| foreground | a near-white neutral | a deep neutral, nearly the ground | every piece of text |
| hole | a deep neutral, and it is very nearly flat across all eight steps | the same deep neutral | a surface that must read as a hole rather than a raised panel |
| plain | a near-white neutral | a deep neutral | neutral surfaces that are not the page ground |
| citrus | a light, vivid amber | a deep warm neutral | a module identity |
| corail | a light, vivid orange | a deep warm neutral | a module identity |
| cyan | a mid, vivid teal | a deep neutral | a module identity |
| green | a light, vivid green | a deep neutral | a module identity |
| indigo | a light, soft blue | a deep neutral | a module identity |
| king | a light, vivid blue | a deep neutral | a module identity |
| lavender | a light, vivid indigo | a deep neutral | a module identity |
| lime | a light, vivid lime | a deep neutral | a module identity |
| magenta | a light, soft magenta | a deep neutral | a module identity |
| orange | a light, vivid orange | a deep warm neutral | a module identity |
| pink | a light, vivid red, warmer and softer than the red ramp | a deep neutral | a curve family identity |
| purple | a light, soft violet | a deep neutral | a module identity |
| red | a light, vivid red | a deep warm neutral | a module identity, and the wordmark's accent dot |
| sega | a light, vivid cyan | a deep neutral | a module identity |
| sky | a mid, vivid teal, cooler than cyan | a deep neutral | a module identity |
| turquoise | a mid, vivid teal, greener than cyan | a deep neutral | a module identity |
| yellow | a light, vivid amber | a deep warm neutral | a module identity |

Three of the seventeen sit close enough to one another that they must be kept distinguishable deliberately: cyan, sky and turquoise are all mid vivid teals, and the build must separate them by hue so two adjacent modules in the tree do not read as the same chapter.

Step three and step four of the foreground ramp are both light neutrals and are dim against the ground by design. **They are the most likely accessibility defect in this system**, and `## UI/UX notes` states the obligation: measure, do not assume.

### The scene and surface values outside the ramps

| Role | The colour |
|---|---|
| The page ground | a deep neutral, identical to step one of the ground ramp |
| The outline on a drawn object | a near-black neutral |
| The outline in the light scheme | pure black |
| The shadow on a drawn object | a deep neutral |
| The rim light on the scene's objects | a near-white, soft orange, and it is the only warm value in an otherwise neutral scene |
| The scene's ground plane | a deep neutral |
| The scene's ground plane in the light scheme | a near-white warm neutral |
| The funding call's ground | a deep warm neutral, moving to a deep, muted red when pointed at |

**The rim light is what separates the object from the ground.** A build that omits it produces a silhouette that reads as flat.

A light colour scheme is declared and its three counterparts above are the only part of it that was ever observed. The build declares the scheme and is not held to a palette nobody measured.

### The code palette

Independent of every ramp and of the section alias, so the same snippet never changes appearance between one page and the next.

| Role | The colour |
|---|---|
| Plain text | a near-white neutral |
| Keyword and operator | a light, vivid magenta |
| Function and class name | a mid, vivid lime |
| Number and constant | a light, soft indigo |
| String | a light, soft amber |
| Parameter and built-in | a light, soft cyan |
| Comment | a mid warm neutral |

### The alias

A documentation section, a curve family and a tour stop each rebind one alias of eight steps to one ramp, and every component below that boundary addresses a step of the alias. **That indirection is the mechanism and it is not an optimisation**: the current colour of anything on the page is always read through the alias rather than named, which is why a section's identity is one line of content and not a stylesheet.

The alias reaches further than a build usually expects, and that reach is the requirement. It colours the tree entry, the article title, the links in the prose on hover, the demo panel's current ground and label, the arc on the instrument, the curve stroke in the plot, **the axis lines drawn inside a diagram**, the endpoint dots and the handle bars, and the gradients used as section washes. All of them read one alias, which is why they cannot fall out of agreement.

### Type

Three roles and no fourth.

- **Everything that is not code** is set in a variable grotesque whose weight axis spans very light to very heavy and whose slant axis reaches a shallow oblique. The wordmark uses the oblique; nothing else does.
- **Code and interface labels** are set in a monospace with a true italic at its regular weight.
- **Numeric readouts in the editor are drawn rather than set.** Each digit is seven strokes on a tall narrow grid: three horizontal, at the top, the middle and the foot, and four vertical joining their ends, each stroke a rounded bar. A lit stroke takes the current family's brightest step and an unlit stroke takes a deep step **in the same position**, which is what produces the ghosted look of an unlit segment on a real display. This is more faithful than any substitute face and it removes an asset.

The reference's three families are commercially licensed, are named here only to be excluded, and are neither shipped nor reproduced: `Ration Sans`, `Ration Mono` and `Ration Seven`. Each role resolves instead to a freely licensed equivalent or to a face the reader's system already has, **and no font binary is fetched**, so there is no loading phase, no swap and no moment of invisible text.

The rendered scale, by what it is for rather than by size. The dominant text on the site by a wide margin is a small monospace interface label at a semibold weight, with one step above it for the same label in a more prominent position. The article body is noticeably larger and sits at a comfortable leading. There is a secondary body at a lighter weight for supporting copy, a dense label at a solid leading, a caption that is the smallest text on the site, a section headline, and two tour headline steps of which the larger is the biggest type in the build.

**Every headline's line height is below its own font size.** The tour's headline steps, the section headline and a documentation page's title all set tighter than their own size, and that is what produces the stacked, confident look of the tour. Lose it and the site still works and stops looking like itself.

Leading and tracking are proportions of the size rather than fixed measures, so optical spacing holds as the size changes and a fractional rendered leading follows from the multiplier rather than being typed.

### Iconography

Six icons, every one drawn as geometry on one square grid, at one uniform stroke weight, with round joins and caps, stroked in the current text colour so an icon inherits the alias, and filled only where the icon is a solid one. **No icon file ships and no icon font is loaded.**

| Icon | What it is | Where |
|---|---|---|
| Panel | a rounded rectangle divided by a vertical line near its left third | beside the documentation call, and in the narrow documentation bar |
| Curve | one cubic segment that races ahead and overshoots its own midpoint | beside the editor call |
| Heart | one filled symmetric form | the funding call, and at particle scale on the tour |
| Play | a triangle with all three corners rounded | beside the learn call |
| Pause | two upright bars of equal width | the editor's preview |
| Arrow | a horizontal shaft with a chevron at its end, rotated in quarter turns for four directions | the pager, the in-section list, the search steppers |

**The curve icon is a joke about what the editor is for**, and it should be preserved as one: the ease overshoots.

**The particle treatment on the heart is the single most distinctive graphic effect on the site.** The heart appears by the hundred across the tour carrying a coloured glow, blended additively so that where two particles overlap the result is brighter rather than one hiding the other, and with a base state whose glow has no radius at all so it can be animated up from nothing rather than faded in as a whole layer. Both halves are required: without the additive blend the particles read as stickers rather than embers, and without the zero-radius base the glow arrives as a sheet.

Three pieces of geometry are drawn rather than iconographic and are specified with their components: the curve plot and its handles, the module objects inside the instrument, and the four adapter marks. **The adapter marks are not trademarks and are not transcribed.** Each is a placeholder drawn on the icon grid: a rounded square, stroked in the current text colour, containing the adapter's initial letter set in the monospace and centred. The four are `Ripple`, `Kestrel`, `Vellum` and `Orbit`, and a real mark is supplied at integration time by whoever holds the right to use it.

The wordmark is not artwork. It is the product name set in the variable grotesque at its oblique with **a single accent dot at its top right in the red ramp's brightest step**. That dot is the only saturated colour in the resting header and it is the site's whole brand signature. It must be drawn, never an image.

### Global chrome

**The header** is fixed to the top of every route at the header token's height, on the page ground with a blur behind it that rests at nothing. Left to right it carries the wordmark, which returns to the tour; the version control and the search field, **on documentation routes only**; five navigation calls; and the funding call on a filled ground carrying the heart icon, a label and a ring that turns continuously.

**Navigation call states.** At rest a call is a light neutral from the middle of the foreground ramp. Pointed at, it lifts to the near-white at the top of that ramp, and its colour and its border move together. On the active route it carries the near-white plus a rule beneath it drawn in the section alias. Focused from a keyboard, it carries the focus ring described below. **Both of the call's duplicate label layers move with the base element**, which is what keeps the label and its brighter copy in register during the sweep.

**The label sweep.** Each call's label is drawn twice, once in the resting colour and once in the hover colour, and pointing at the call reveals the brighter copy **across** the label rather than cross-fading between the two. The colours of all three layers are measured; the sweep's direction and shape are a reconstruction, and the build should treat the direction as adjustable.

**Two calls are retractable.** On a narrow desktop they drop their labels and keep their icons, **through a width transition on the label rather than a display switch**, so the icon does not jump.

**The scrolled state.** Once the document has scrolled past the header's own height, the header gains a blur and a hairline rule beneath it.

**The mobile menu.** Below the primary turning point the five calls collapse behind a control in the header, and the panel slides in from the right. It opens and closes on the overshooting curve. It is dismissed by its own control, by a press outside it, by the escape key or by a route change. While it is open, **focus is trapped inside it and is restored to the control that opened it on close**, and the document's scroll is locked without the layout shifting.

**The footer** is four columns on a wide screen, stacking to one below the primary turning point, in this order: the advertising slot with its attribution and the funding call; the site links, being the tour, the documentation, the editor and the course; the social links, being two microblogs, the source host and the playground; and the subscription pair. Beneath all four sit a full-width wordmark and the maintainer attribution.

**The scroll indicator.** The site draws its own scroll position rather than relying on the browser's: a small rounded block on a track drawn as a ruled tick strip rather than a solid rail, **with a second, fainter block trailing behind it**. The trail is deliberate and is what makes the marker read as having weight rather than being glued to the wheel. A build that draws only the leading block loses the effect entirely.

**The storage bar** is anchored to the foot of the page and is never a modal. It carries one sentence, an accept control and a refuse control of equal prominence, and dismissing it re-seats whatever sits above it rather than leaving a gap.

### Motion

**Five curves and no sixth.**

| Curve | Character | Used by |
|---|---|---|
| The settling curve | overshoots its target and settles back, like a drawer with a soft close | panels, and the mobile menu |
| The standard curve | symmetric, with no overshoot | every ordinary interface transition |
| The colour curve | steep through the centre and slow at both ends | colour and ground changes |
| The reveal curve | decelerates hard and late | long reveals |
| The stop curve | gentle in and long out | the tour's stop transitions |

**Eight named moments.** A build that names none of them ships none of them.

| Moment | What a person sees |
|---|---|
| The fade in, and its reverse | something appears or leaves without moving at all |
| The pop in, and its reverse | a menu, a dialog or the version list arrives fading up from very slightly too small, and leaves the same way |
| The spin | a pending indicator turns continuously while something is in flight |
| The call ring | a ring around the funding call turns continuously, slower than the pending indicator |
| The centred rise, and its reverse | a centred element rises a short distance into place while fading up, and reverses on the way out, composed on top of a centring offset already in place rather than replacing it |

**The pop pair animates scale as a property in its own right rather than through a transform**, which is what lets it run alongside a transform-driven position change on the same element without either erasing the other. The centred pair is written to compose with a centring offset already applied; a build that centres a different way must drop the offset or the element sits half a width out.

**Durations and their relationship.** There is one default interface duration and it applies to filter, transform and opacity alike: quick enough that nobody waits for it, slow enough to be seen. **Colour changes run about twice as fast as anything that travels**, which is why the site feels responsive under a pointer without feeling twitchy. Nothing uses a different speed to feel special, and **there is no blanket rule that transitions every property**: named properties transition and nothing else does.

**Under a reduced-motion preference** nothing is scroll-driven, no particle drifts, the scene does not rotate, no reveal staggers, and all content is in its final state. The instrument holds one still frame. The editor's preview holds a static frame and its onion skin still draws, because the onion skin is a diagram rather than a motion. Nothing is left part way.

### The scroll system

The tour is the only route with a substantial scroll system and it is the most heavily scroll-driven surface in the build. The editor barely scrolls at a desktop width and is designed to fit the window.

What is driven by scroll on the tour, and what changes: each graduation mark's transform, the ring's paths, the small icons' transform and opacity, the specimen blocks' transform as they travel into view, each split character's transform and opacity, the dot beside the third stop's headline, the demonstration shapes and circles, and each module arc's glow.

**The stage stays centred in the window for the whole of the tour's scroll range**, and it is larger than the window, so it is offset rather than fitted. Its offsets are positions, not animations: the stage does not move as the tour advances, its contents do.

**The graduation marks are transformed individually from one shared parameter.** Each mark's transform is a rotation about the ring's centre plus a radial offset. The set of them is what makes the rim read as a dial being turned rather than a circle being spun, and a single rotating container cannot produce it.

**Each module arc changes only its glow**, ramping from off to on as the tour reaches that module's stop. Combined with the alias rebinding and the headline swap, this is the tour's central mechanism: arriving at a stop lights one arc, rebinds the colour, and recolours the headline, the arc and the object together.

**Headlines are split into words and characters** and each fragment is offset horizontally with a per-element delay, so a line assembles itself rather than appearing at once. The split must be reversible, must not destroy the readable text for assistive technology, and must copy as real words with their spaces.

**The tour is more animated on a narrow screen than on a wide one**, which inverts the usual assumption. On a wide screen several small demonstrations sit beside the stage and are simply present; on a narrow one they stack into the scroll and each performs as it arrives, and the scroll indicator, its track, the module list rows and a travelling shape join the driven set.

### The instrument, drawn

Inside the ring: one object per module, composed from five primitives rather than loaded as a file. The primitives are a rounded box, a capsule, a lathe-turned profile revolved about the vertical axis, a torus and a sphere.

| Object | Composition |
|---|---|
| `timer` | a lathe-turned dial body, a torus rim, two capsule hands |
| `animate` | a rounded box with a capsule travelling a visible track |
| `timeline` | three rounded boxes of graduated length, stacked with an offset |
| `draggable` | a rounded box with a sphere resting in a shallow lathe-turned cup |
| `scope` | a torus frame around a smaller sphere, offset on the depth axis |
| `svg` | a lathe-turned four-pointed form, matching the shape drawn in the demo panel |
| `easing` | a tube swept along the sampled curve from the editor's plot |
| `stagger` | five capsules in a row, each rotated a constant increment from the last |
| `spring` | a helix of capsule segments between two rounded plates |
| `engine` | a torus with radial capsule spokes |
| `renderer` | a flat rounded box with a raised inner frame |
| `waapi` | two interlocking tori at right angles |
| `scroll` | a lathe-turned roller with a ridged profile |
| `shield` | a lathe-turned convex plate with a raised rim |

**Each object is registered under the name in that table**, so everything else in the build addresses an object by name and nothing has to change if a real object is supplied later.

**The motion inside an object is a contract rather than a recovered animation**: a rotation about the vertical axis proportional to the scroll progress through the stop, plus a slow constant idle rotation. This is a reconstruction rather than a measurement, and the build should expect to adjust it once it is running.

### Hover, pointer, focus and touch

**The universal rule.** Every interactive element in the site's own chrome moves from a light neutral in the middle of the foreground ramp to the near-white at its top, with the colour and the border moving together and both duplicate layers moving with them. That is the entire hover vocabulary for text, applied to the navigation calls, the search toggle, the demo steppers and the documentation tree rows alike. **Two things start one step dimmer**: the documentation tree rows, which still rise to the top of the ramp, and the advertising attribution, which rises only to the middle because it is deliberately subordinate.

**One ground change, and only one.** The funding call moves its ground from a deep warm neutral to a deep, muted red rather than moving its text, which is what makes it read as a button among links.

**Four non-text hover targets.** A preset tile in the editor changes its asymmetric radius toward the active form and lifts its curve stroke to the family's brightest step. A demo panel lifts its border to the section alias. A copy control gains a ground where it had none. And **a module tile at the foot of the tour lights that module's arc on the instrument far above it.**

**Cursors.** Grab over the curve handles and the draggable demonstrations, and grabbing while one is held. Text over a code block. Pointer over everything else interactive. The handles and the draggable demonstration are the only two directly manipulable elements in the build and both are circular.

**Focus.** A solid near-white ring, offset from the element, following the element's own radius, shown on keyboard focus only and **never suppressed globally**. It is louder than hover, not weaker, because it is the only signal a keyboard user gets.

**Touch.** There is no hover, so every effect above has an equivalent. The lit arc belongs to the module currently in view. The bordered demo panel is the one currently in view. **The copy control is permanently visible rather than revealed**, which is the row that matters: copying a snippet is the most valuable action in the documentation, and a control that only appears under a pointer is invisible and unusable on a phone. Text needs no equivalent, because it is already legible at its resting step.

### The specimen block and the copy control

| Property | What it must be |
|---|---|
| Family | the monospace |
| Theme | the code palette above, never the section alias |
| Ground | a step of the hole ramp, so the block reads as a recess rather than a raised panel |
| Corners | softened at the foot only where the block follows a header strip, and on all four corners otherwise |
| Width | full-bleed within the article, through the inset trio |
| Overflow | scrolls horizontally inside the block and never widens the page |
| Wrapping | none; long lines scroll |
| Selection | the text is selectable and selecting it does not trigger the copy control |

The copy control sits at the block's top right behind a small backdrop blur so it stays legible over code. Its corner is softened on the one side flush with the block's own corner. At rest on a pointer device its ground is transparent and its icon sits at the middle of the foreground ramp; **at rest on a touch device its ground is visible**. Pointed at, the ground appears and the icon lifts to the top of the ramp. Pressed, the icon swaps to a confirmation mark, which holds and then reverts.

### Route: the tour

A single continuous scroll, no chrome below the header and no visible section breaks.

**The opening.** A headline of two or three lines at the largest type step, split into words and characters and assembling on load. A two-line subheading at the article size in a light neutral. The install line as a specimen with its own copy control. A labelled secondary call carrying a downward arrow. And a small sponsor attribution with one upper-tier mark at the lower right. **The install line and the secondary call sit outside the stage.**

**The twelve stops.** Each swaps a headline and subheading pair beside the instrument on the centred rise and its reverse, driven by scroll position rather than played on entry, so scrolling back reverses them exactly. The alias rebind, the arc glow and the object swap happen together at the boundary, and the interpolation between two stops is continuous.

**The demonstrations in the scroll.** Beside the instrument at a wide width, stacked into the scroll at a narrow one: a square shape and a circle shape each with a filled variant, a dot beside a headline, a track drawn as a background with a highlight above it, a shape travelling along a path, and a numeric readout. **Each is a live demonstration of its own stop, not a picture of one.**

**The module grid.** Twelve tiles closing the tour above the footer, four rows of three at a wide width, two columns at a tablet width and one below the narrowest refinement. Each tile carries a colour dot in its module's brightest step, the module name in the monospace at uppercase, and a trailing arrow. Above the grid sit a closing headline and one line of supporting copy.

**States.** While loading, the headline, subheading, install line and call render at once and the stage occupies its space and fills when ready. With the scene unavailable, the drawn ring carries the tour alone. Under a reduced-motion preference the stops become discrete and content appears in its final state. On a deep link, the tour lands on that stop without playing the ones between. In a very short window the stops are still scroll-driven, with the stage scaled to fit.

### Route: the documentation shell

**Three columns.** The tree at its token width, the demo column at its own, and the article taking the remainder.

**The tree.** Sixteen module rows in the monospace at uppercase. At rest a row sits one step dimmer than the rest of the chrome; pointed at, it lifts to the top of the foreground ramp; the current module carries its alias at its brightest step; and the current page carries the top of the foreground ramp with its module's alias on its marker. The current module expands in place through a height transition, its child pages indented and set in the monospace one step smaller. **Two modules carry a `NEW` badge**: a small uppercase label on a ground of that module's own ramp at a dim step. When the tree is hidden it translates off to the left rather than being removed.

**The version control.** Beside the wordmark, reading the current version's label with a disclosure chevron, opening the published versions newest first on the pop in.

**The demo column.** One panel per page in the current module, stacked in the module's order. Each panel carries a label strip above it with the page name in the monospace at uppercase. Panels butt against each other with no gap and no radius. The panel ground is a dotted field drawn as a repeating radial gradient rather than an image. **The current panel lifts its ground to the module's ramp at its dimmest step and its label to the brightest.** Two steppers in the header move between panels and rest at half opacity, lifting on hover like everything else.

**The narrow arrangement.** Below the primary turning point the shell becomes one column behind a compact bar carrying the panel toggle, the current section's name, the search control and the two demo steppers. The article runs full width. **The current demo panel survives as a small panel pinned in the lower corner** rather than being dropped.

### Route: a documentation page

| Element | What it must be |
|---|---|
| Title | the largest headline step below the tour's, set tighter than its own size, in the module's alias at its brightest step |
| Body | the article size at a comfortable leading, one step down the foreground ramp from white |
| Inline code | the monospace at the body size, on a ground from the hole ramp |
| Subheadings | the article size at the same weight, at the top of the foreground ramp |
| Links in prose | the top of the foreground ramp, underlined, moving to the module's alias at its brightest step when pointed at |
| Specimen blocks | as specified above |
| In-section list | full-width rows on a ground one step up the ground ramp, each carrying the page name in the monospace at uppercase and a trailing arrow that lifts on hover |
| Pager | two controls at the foot, previous on the left and next on the right, each carrying a direction arrow and the target page's own name in the monospace at uppercase |

### Route: the curve editor

**Four panels.** At a wide width: the preset grid down the left at full height, the plot in the upper centre, the preview in the upper right and the export blocks in the lower right, the whole route fitting the window. At a narrow width they stack in the order plot, preview, export, grid.

**The preset grid** is four tiles across. Each tile draws its own curve as a miniature plot, stroked in its family's brightest step, on a ground from the ground ramp, with its name beneath it in the monospace. **Its idle corner softening is on one corner and its active softening runs down its whole leading edge**, and that change is the grid's entire selection signal. The active tile's ground is its family's dimmest step. Pointed at, the stroke lifts to the brightest step and the ground toward the dimmest. The grid's container clips to a rounded rectangle, which is what lets a tile's corner change without escaping the grid. The grid fades in staggered, tile after tile.

**The plot.** A softened container over a dotted field drawn as a repeating radial gradient, with an inset border rather than an outer one. Two axis lines in a dim step of the current alias. The curve as one path, unfilled, thicker than the axes, in the current text colour. Two endpoint dots and two handle bars, both filled in the alias at its brightest step, and **both handle primitives carrying a dark drop shadow so they stay visible wherever the curve takes them**. Above it a header strip, softened at the top only, carrying the curve's name at uppercase and a reset control resting at half opacity.

**The preview.** Four cells: one running, filled in the family's brightest step, and three ghosted in a step of the ground ramp, showing the animation at successive offsets. Pause, loop and replay controls at the panel's top right. Below them the onion skin, softened at the foot only, showing the trail of previous positions. Duration, loop delay and the two opacity endpoints are each a slider paired with a numeric field, and their values are shown in the drawn seven-segment readout.

**The export panel.** Two tabs and two blocks per tab, each block a specimen with its own copy control.

**The narrowest case.** The plot keeps a square aspect and the preset grid becomes horizontally scrollable rather than reflowing into unreadable tiles.

### Route: the course waiting list

A centred single column on the page ground, with no three-column shell and no instrument. A two-line headline at the section headline step, set tighter than its own size. Two paragraphs of centred supporting copy at the article size in a light neutral. The subscription card on a ground one step up the ground ramp with a generous corner softening, carrying one labelled field and one submit control. Beneath it, the fallback line offering a written address. Below the form, figures each carrying a hairline outline and a soft drop shadow, with a caption sitting over a blur.

**The figures load no payload until somebody asks for one.** Each renders with its generated poster, its caption and a play control, and a figure with no media is absent rather than an empty frame. A route whose purpose is to capture an address must not spend a large download before the form is usable.

### The subscription controls

Two shapes for one behaviour. On the course page a card with one field above one full-width control. In the footer **a joined pair**: the field and the submit button softened only on their outer edges so the two read as a single control.

The success and the error messages are **present in every document at rest and fully transparent**, so they fade in rather than being inserted, which is what lets assistive technology be told about them without a node appearing. Both carry a small corner softening.

| State | What a person sees |
|---|---|
| Idle | the field, the control, no message, and the fallback line |
| Invalid on the client | the field marked, the reason beside it, the control still operable |
| Submitting | the control carries a pending indicator turning on the spin, and is not disabled in a way that hides it |
| Accepted | the success message fades up, stating that a confirmation has been sent |
| Rejected | the error message fades up carrying the specific reason |
| Rate limited | the same error element, with a wait hint |
| Offline | the submission is held and retried once connectivity returns, and the form says so |

### The sponsor wall

Cards in a grid, grouped by tier with the tier's heading above each group. A card is a softened container on a ground one step up the ground ramp, carrying the mark centred in a fixed box at its tier's size, the sponsor's name beneath it in the monospace in a light neutral, and lifting its ground one step when pointed at. It leads to the sponsor's destination in a new context. **The last card in every group is the recruitment card**: the same shape, the outline heart, and the label inviting the visitor to take the slot.

### The error routes

A centred single column. A heading at the section headline step, one line of explanation at the article size, and three routes out rendered as ordinary links. On a documentation address, the search control is offered beneath with the failed segment already in the field. The server error page is the same column without the search offer, with a retry control in the primary style.

### Textures and fields, all procedural

| Field | What it is |
|---|---|
| The demo panel ground | a fine dot grid, drawn as a repeating radial gradient |
| The plot ground | the same dot grid in a warm dim tone |
| The scroll track | a ruled tick strip, drawn as a repeating linear gradient of fine light lines on transparency |
| A vertical fade | a linear gradient from opaque to transparent over the lower half |
| A corner vignette | a linear gradient from a faint dark wash to solid over a short distance |
| A soft radial mask | a radial gradient opaque at the centre and clear by seven tenths of the radius |
| Hatching | a repeating diagonal gradient of very faint dark lines |
| A section wash | a linear gradient from a mid step of the current alias, in a vertical and a horizontal variant |
| A dot marker | a small radial gradient in the current text colour with a hard edge |

**No grain and no noise texture exists anywhere in this build.** None was found in the reference and adding one adds something the reference did not have.

**Generated posters.** Every demo carries a seed, and its still is generated from that seed alone: a ground in the module's ramp at its dimmest step, the dot field over it, two to four primitives drawn from that demo's own vocabulary and positioned from the seed, stroked in the module's ramp at its brightest step. **The same seed produces the same still on every build**, which is what stops a rebuild changing every poster on the site at once.

### Copy

Every string on the site. Voice: second person for instruction and never the first person plural; sentence case everywhere except interface labels in the monospace, which are uppercase; headlines at most six words; subheadings at most two lines; the module names are the vocabulary and no synonym is invented for them; plain and technical, and **no exclamation mark anywhere**.

| Slot | String |
|---|---|
| Wordmark | `Lumen.js` |
| Navigation | `DOCS`, `EASINGS`, `LEARN`, `EXAMPLES`, `SOURCE` |
| Funding call | `SPONSOR` |
| Mobile menu control | accessible name `Open menu` and `Close menu` |
| Skip link | `Skip to content` |
| Footer headings | `SPONSORS`, `SITE`, `SOCIALS`, `STAY IN TOUCH` |
| Footer attribution | `Built and maintained by Elias Marchand` |
| Advertising attribution | `ads via Carbonate` |
| Storage bar | `We keep a little to remember your version and count page views. Your choice.` with controls `ALLOW` and `NO THANKS` |

| Tour slot | String |
|---|---|
| Headline | `One engine for every animation.` |
| Subheading | `A small, fast library for moving anything on the web.` |
| Install line | `npm i lumenjs` |
| Secondary call | `LEARN MORE` |
| Sponsor attribution | `Sponsored by` |
| Closing headline | `Start animating` |
| Closing subheading | `Everything you need is in the documentation.` |

| Stop | Headline | Subheading |
|---|---|---|
| 2 | `A complete toolbox` | `Timers, timelines, springs and paths in one package.` |
| 3 | `Readable by design` | `One call, named options, sensible defaults.` |
| 4 | `Compose anything` | `Nest and sequence animations without fighting them.` |
| 5 | `Tied to the scroll` | `Drive any animation from the position of the page.` |
| 6 | `Offset in sequence` | `Move many elements a beat apart from one another.` |
| 7 | `Shape toolset` | `Morph outlines, follow paths and draw lines.` |
| 8 | `Pick things up` | `Draggable elements with real momentum.` |
| 9 | `Exact timing` | `Sequence work to the millisecond.` |
| 10 | `Adapts by itself` | `Responds to width, and to a preference for stillness.` |
| 11 | `Take only what you need` | `Import one module or the whole engine.` |
| 12 | `Our sponsors` | `Lumen.js is free, and stays free because of them.` |

| Documentation slot | String |
|---|---|
| Landing title | `Documentation` |
| Landing lead | `Written and kept current with the help of our sponsors.` |
| Tier headings | `Upper sponsors` and `Lower sponsors` |
| Recruitment card | `Become a sponsor` |
| In-section heading | `In this section` |
| Pager labels | `PREVIOUS`, `NEXT` |
| Badge | `NEW` |
| Version control accessible name | `Documentation version` |
| Version notice | `That page is not in this version. Here is the module index.` |
| Search placeholder | `SEARCH` |
| Search empty | `No pages match that.` |
| Search unavailable | `Search is unavailable. Use the menu on the left.` |

| Editor slot | String |
|---|---|
| Panel headings | `PREVIEW`, `EXPORT` |
| Plot heading | the current curve's name, uppercase |
| Reset accessible name | `Reset this curve` |
| Parameter labels | `preset`, `mode`, `bounce`, `duration`, `loopDelay`, `from opacity`, `to opacity` |
| Export tabs | `CSS`, `JS` |
| Copy accessible name | `Copy this snippet` |
| Copy confirmation | `Copied` |

| Subscription slot | String |
|---|---|
| Course headline | `Learn how this site was built.` |
| Course lead | `A course rebuilding this page from an empty file.` |
| Waiting-list label | `Join the waiting list` |
| Field label | `Email` |
| Submit | `SUBSCRIBE` |
| Fallback | `If the form fails, write to hello[at]lumenjs.example.` |
| Pending | `Sending...` |
| Success | `Check your inbox to confirm.` |
| Invalid | `That does not look like an email address.` |
| Rate limited | `Too many attempts. Try again shortly.` |
| Offline | `You appear to be offline. We will retry.` |
| Confirmed page | `You are on the list.` |
| Expired token | `That link has expired. Send another?` |
| Unsubscribed page | `You will not hear from us again.` |

| Error slot | String |
|---|---|
| Not found heading | `Nothing here` |
| Not found body | `That address does not exist. Try one of these.` |
| Not found search offer | `Search the documentation for that instead?` |
| Server error heading | `Something broke` |
| Server error body | `That is on us. Try again in a moment.` |
| Retry | `TRY AGAIN` |

| Element | Accessible name, never visible on screen |
|---|---|
| Demo panels | hidden; each page's meaning is in its prose and never only in its demonstration |
| Preview and onion skin | hidden |
| Curve handles | `Control point one`, `Control point two` |
| Plot | the curve's family, member and parameters, read as one sentence |
| Demo steppers | `Previous demonstration`, `Next demonstration` |
| Tour stops | the stop's own headline |
| Sponsor card | the sponsor's name followed by its tier, read as one phrase |

**All of that copy is written for this build.** Where a line had to be a certain length because a layout was designed around it, the length was matched rather than the wording, and the reference's own text is neither reproduced nor paraphrased.
## Constraints

- One product, one origin. No second origin for assets, for the object store or for anything else.
- **No visitor account of any kind.** No sign-up, no sign-in control on any public route, no profile, no saved state belonging to one visitor rather than another, and no permission grid. The only account in the system belongs to the maintainer, and it exists so the content pipeline has somewhere to live.
- **Nothing is bought or sold here and no money moves.** Every funding call leads outward. There is no payment machinery anywhere in this build.
- No real mail provider, advertising network or sponsorship platform. Each is modelled inside this app against seeded data and operator actions, and **no request leaves this origin at run time.** The source host, the playground and the package registry are named in outbound links only, carry no data, and are never fetched.
- No second database, cache, queue, object store, identity provider or mail vendor. No email is actually sent and no mail server is available; a message that would be sent becomes a row in the outbox.
- **No binary asset of any kind.** This is a zero-asset build and the substitution guide for every asset class is in `## Front-end specification`. No image file, no video file, no audio file, no font binary, no compressed geometry file and no icon font. Every icon is geometry, every ground is a gradient, every poster is generated from a seed, every scene object is composed from primitives, and the numeric readouts are drawn as strokes. The reference's twenty-four compressed geometry files and its large video library are the two things this constraint replaces, and the substitution is real and is accepted: the objects will be recognisably the right thing in the right place and will not be identical to the originals.
- The three commercially licensed families the reference used are not reproduced. Each type role resolves to a freely licensed face or to one the reader already has.
- The three-dimensional scene is a genuine scene rather than a video or a picture, and it is fetched on the tour and on no other route.
- No smooth-scroll layer, and no blanket rule that transitions every property.
- No comments, no likes, no messaging, no social graph and no third-party analytics or measurement vendor.
- No consent-requiring identifier is written before the visitor has answered, and no persistent per-visitor identifier is written at all.
- The app stays responsive with `3` versions, `16` modules and `48` pages in one published version, `20000` page-view rows and `5000` subscriber rows.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/subscribe/token` | | the form's timing token, as `timing_token`, valid once `2` seconds have passed |
| `POST /api/subscribe` | `email`, `list`, `company_website` which must be empty, and `timing_token`, form-encoded | the acceptance and the state named in `## Core features` |
| `GET /api/subscribe/confirm` | `token` | a rendered confirmation page, not a JSON body |
| `POST /api/unsubscribe` | `token` | the subscription ended, single use |
| `GET /api/search-index/<version_label>` | | the version's index artifact, streamed from the object store |
| `GET /api/versions` | | a top-level JSON array of the published versions, newest first by sort key |
| `GET /api/documentation/<version_label>/tree` | | the modules and their pages for that version, in tree order |
| `GET /api/pages/<version_label>/<module>/<page>` | | the page, its anchors, its demo and its previous and next page in the flattened sequence |
| `GET /api/sponsors` | `surface` | the tiers and their active sponsors for that surface, in rank then position order, with the roster's age |
| `GET /api/ad-slot` | | the slot's current state |
| `POST /api/events` | the event kind and its attributes | accepted, with no body consumed by the caller |
| `POST /api/storage-choice` | `choice` | the choice recorded |
| `POST /api/auth/login` | `email`, `password` | the bearer token as `access_token`, with its expiry |
| `POST /api/auth/logout` | | the token invalidated |
| `GET /api/studio/versions` | | every version including drafts, with its state |
| `POST /api/studio/versions` | `label`, `sort_key` | a new draft version |
| `POST /api/studio/versions/<id>/validate` | | each of the nine checks and its outcome |
| `POST /api/studio/versions/<id>/publish` | | the version promoted, or the first check that refused it |
| `POST /api/studio/modules` | `version_id`, `slug`, `name`, `ramp`, `position`, `tile_position`, `object`, `badge`, `badge_expires_at` | the module |
| `POST /api/studio/pages` | `version_id`, `module_id`, `parent_page_id`, `slug`, `title`, `body`, `position`, `demo_id` | the page, with the version's flattened sequence recomputed |
| `PATCH /api/studio/pages/<id>` | any of the same fields | the page, with the flattened sequence recomputed |
| `GET /api/studio/outbox` | `state` | a top-level JSON array of queued, delivered and dead messages |
| `POST /api/studio/outbox/<id>/deliver` | | the message delivered |
| `POST /api/studio/roster/availability` | `available` | the roster source made available or unavailable |
| `POST /api/studio/ad-slot` | `state` | the slot set to fills, empty or slow |
| `POST /api/studio/jobs/<job_name>/run` | | the run, or a refusal naming its reason |
| `GET /api/studio/jobs` | | every run with its state, its lock and its detail |
| `GET /api/studio/dead-letters` | | a top-level JSON array of exhausted jobs |
| `GET /api/studio/page-views` | `from`, `to` | the counts by route |
| `POST /api/studio/mail-events` | `event_id`, `type`, `email`, `list` | the event applied, idempotent by `event_id` and tolerant of arriving out of order |
| `POST /api/studio/outbox/<id>/deliver` handed a queued confirmation | | the message delivered, returning the confirmation `token` once |
| `POST /api/hooks/mail` | the provider event and its signature | accepted, acted on by the state it carries rather than by the order it arrived in |
| `GET /api/health` | | readiness |

Bearer auth is required on everything under `/api/studio`. Everything else on that list is public, because everything else on this site is public. The mail callback authenticates by signature and never by a session. A successful call returns the named resource or shape, and an invalid or unauthorized call is rejected as a client error, never a `5xx` and never a silent success.

### No mocks

The object store is not simulated. Bytes on the app container's filesystem, a text column in PostgreSQL, a search index assembled in the browser from the rendered pages, an index rebuilt from the database on every query, or a `{"stored": true}` the app returns to itself are each a contract violation however good the interface looks. The same holds for the datastore: rows held in a process rather than in PostgreSQL disappear when the app restarts, and a documentation tree assembled from a module-level list is not a content store. **MinIO and PostgreSQL are the fact: this app's own screens and its own tables can only reflect what lives in them, never substitute for them.**

## Definition of done

A stranger opens the tour, copies the install line before the stage beside it has filled, and reads the whole manual front to back on the pager alone, crossing every module boundary. A call name that appears only inside a code specimen is findable, and the index that answered came out of the object store. A curve designed with the keyboard alone exports a snippet that matches the drawn curve exactly. An address submitted twice is thanked rather than corrected, and the confirmation link works once. With the scene disabled the tour still tells its whole story.
