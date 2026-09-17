# Checklist: Reactive Notebook Showcase

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, constraints, deployment
Sections absent: buildplan, frontend
Items: 265
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a marketing surface for a reactive data-notebook platform. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app routes a visitor toward creating a free account. `src: Overview para 1`
- [ ] `C-OV-03` `role` An author composes each route from ordered section blocks. `src: Overview para 2`
- [ ] `C-OV-04` `constraint` The app builds no part of the notebook application the pages advertise. `src: Overview para 4`
- [ ] `C-OV-05` `constraint` The app keeps a page row in agreement with the object in the bucket. `src: Overview para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` A reader reads every published page. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A reader browses the community listing. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A reader creates a free account. `src: User roles table row 1`
- [ ] `C-RL-04` `constraint` The app denies a reader every studio address. `src: User roles table row 1`
- [ ] `C-RL-05` `constraint` The app denies a reader a draft page. `src: User roles table row 1`
- [ ] `C-RL-06` `constraint` The app denies a reader the media of a draft page. `src: User roles table row 1`
- [ ] `C-RL-07` `role` An author composes the pages the author owns. `src: User roles table row 2`
- [ ] `C-RL-08` `role` An author uploads media to a page the author owns. `src: User roles table row 2`
- [ ] `C-RL-09` `constraint` The app denies one author another author's draft page. `src: User roles table row 2`
- [ ] `C-RL-10` `constraint` The app denies one author another author's draft media. `src: User roles table row 2`
- [ ] `C-RL-11` `constraint` The app enforces authorization server-side on every mutating endpoint. `src: User roles para 2`
- [ ] `C-RL-12` `constraint` The app leaves protected state unchanged after a denied request. `src: User roles para 2`
- [ ] `C-RL-13` `capability` The app opens reader signup to anybody. `src: User roles para 3`
- [ ] `C-RL-14` `constraint` The app offers no author signup. `src: User roles para 3`
- [ ] `C-RL-15` `literal` The app seeds an author `author@example.com`. `src: User roles accounts table`
- [ ] `C-RL-16` `literal` The app seeds an author `author2@example.com`. `src: User roles accounts table`
- [ ] `C-RL-17` `literal` The app seeds a reader `reader@example.com`. `src: User roles accounts table`

## C-CF Core features

- [ ] `C-CF-01` `literal` The app accepts an email with a password at `/api/auth/login`. `src: Core features, Auth`
- [ ] `C-CF-02` `capability` The app issues a bearer token at login. `src: Core features, Auth`
- [ ] `C-CF-03` `capability` The app stores every password hashed. `src: Core features, Auth`
- [ ] `C-CF-04` `capability` The app holds a page as an ordered list of section blocks. `src: Core features, The composed page rule 1`
- [ ] `C-CF-05` `literal` The app accepts a block of kind `hero`. `src: Core features, The composed page rule 2`
- [ ] `C-CF-06` `literal` The app accepts a block of kind `color_panel`. `src: Core features, The composed page rule 2`
- [ ] `C-CF-07` `constraint` The app refuses a block whose kind is outside the eight named ones. `src: Core features, The composed page rule 2`
- [ ] `C-CF-08` `constraint` The app numbers block positions contiguously from `1` within a page. `src: Core features, The composed page rule 3`
- [ ] `C-CF-09` `constraint` The app closes the gap in block positions when a block is removed. `src: Core features, The composed page rule 3`
- [ ] `C-CF-10` `capability` The app renders a page's blocks in position order. `src: Core features, The composed page rule 4`
- [ ] `C-CF-11` `literal` The app creates a page in state `draft`. `src: Core features, Draft and publish rule 1`
- [ ] `C-CF-12` `literal` The app moves a page to state `published` when the owning author publishes. `src: Core features, Draft and publish rule 1`
- [ ] `C-CF-13` `constraint` The app answers not-found at the route of a draft page. `src: Core features, Draft and publish rule 2`
- [ ] `C-CF-14` `constraint` The app omits a draft page from the sitemap. `src: Core features, Draft and publish rule 2`
- [ ] `C-CF-15` `constraint` The app refuses a signed-out request for the media of a draft page. `src: Core features, Draft and publish rule 3`
- [ ] `C-CF-16` `capability` The app stores a draft page's image as a real object in the bucket. `src: Core features, Draft and publish rule 3`
- [ ] `C-CF-17` `capability` The app makes a published page's media readable at the same key. `src: Core features, Draft and publish rule 4`
- [ ] `C-CF-18` `constraint` The app moves no object when a page publishes. `src: Core features, Draft and publish rule 4`
- [ ] `C-CF-19` `constraint` The app changes no timestamp when an already-published page is published again. `src: Core features, Draft and publish rule 5`
- [ ] `C-CF-20` `constraint` The app writes no second row when an already-published page is published again. `src: Core features, Draft and publish rule 5`
- [ ] `C-CF-21` `constraint` The app denies a publish request for a page another author owns. `src: Core features, Draft and publish rule 6`
- [ ] `C-CF-22` `literal` The app reads its object store location from `STORAGE_ENDPOINT`. `src: Core features, Media rule 1`
- [ ] `C-CF-23` `literal` The app reads its bucket name from `STORAGE_BUCKET`. `src: Core features, Media rule 1`
- [ ] `C-CF-24` `literal` The app stores an object at the key scheme `media/{page_slug}/{sha256_of_bytes}.{ext}`. `src: Core features, Media rule 2`
- [ ] `C-CF-25` `constraint` The app writes uploaded bytes nowhere but the bucket. `src: Core features, Media rule 3`
- [ ] `C-CF-26` `constraint` The app yields one object when identical bytes are uploaded to one page twice. `src: Core features, Media rule 4`
- [ ] `C-CF-27` `constraint` The app serves protected media by one of the two named mechanisms. `src: Core features, Media rule 5`
- [ ] `C-CF-28` `constraint` The app issues no presigned URL to a signed-out visitor for a draft page's object. `src: Core features, Media rule 5`
- [ ] `C-CF-29` `literal` The app lists an author's own pages at `/studio`. `src: Core features, The authoring studio rule 1`
- [ ] `C-CF-30` `capability` The app shows each studio page's state beside its name. `src: Core features, The authoring studio rule 1`
- [ ] `C-CF-31` `capability` The app composes one page at its own studio address. `src: Core features, The authoring studio rule 2`
- [ ] `C-CF-32` `capability` The app opens a new block at its own address. `src: Core features, The authoring studio rule 3`
- [ ] `C-CF-33` `ui` The app reports a save in a transient message. `src: Core features, The authoring studio rule 4`
- [ ] `C-CF-34` `constraint` The app denies a reader every studio endpoint called directly. `src: Core features, The authoring studio rule 5`
- [ ] `C-CF-35` `literal` The app shows the banner copy `Notebooks 2.0 is now live on the web.` `src: Core features, The home route rule 1`
- [ ] `C-CF-36` `capability` The app labels the banner button with the try-now copy. `src: Core features, The home route rule 1`
- [ ] `C-CF-37` `ui` The app dismisses the announcement banner on request. `src: Core features, The home route rule 1`
- [ ] `C-CF-38` `constraint` The app takes no focus with the announcement banner when a page loads. `src: Core features, The home route rule 1`
- [ ] `C-CF-39` `literal` The app shows the home headline `Not your typical notebook`. `src: Core features, The home route rule 2`
- [ ] `C-CF-40` `capability` The app labels the hero's solid button with the free-trial copy. `src: Core features, The home route rule 2`
- [ ] `C-CF-41` `literal` The app labels the hero's outlined button `Explore the docs`. `src: Core features, The home route rule 2`
- [ ] `C-CF-42` `literal` The app shows the value line `The shortest path from idea to live code`. `src: Core features, The home route rule 3`
- [ ] `C-CF-43` `literal` The app shows a feature card headed `Literate programming`. `src: Core features, The home route rule 4`
- [ ] `C-CF-44` `literal` The app shows a feature card headed `Connect to any data`. `src: Core features, The home route rule 4`
- [ ] `C-CF-45` `literal` The app shows a feature card headed `Built-in reactivity`. `src: Core features, The home route rule 4`
- [ ] `C-CF-46` `literal` The app shows the eyebrow `MULTIPLAYER EDITING` on a blue panel. `src: Core features, The home route rule 5`
- [ ] `C-CF-47` `capability` The app shows the collaboration headline on the first blue panel. `src: Core features, The home route rule 5`
- [ ] `C-CF-48` `literal` The app shows the eyebrow `EMBEDDING` on a second blue panel. `src: Core features, The home route rule 6`
- [ ] `C-CF-49` `literal` The app shows the headline `Ready for production`. `src: Core features, The home route rule 6`
- [ ] `C-CF-50` `literal` The app shows the community headline `Join the community`. `src: Core features, The home route rule 7`
- [ ] `C-CF-51` `ui` The app advances a rail of community cards continuously. `src: Core features, The home route rule 7`
- [ ] `C-CF-52` `literal` The app closes the home route with `Get started today`. `src: Core features, The home route rule 8`
- [ ] `C-CF-53` `literal` The app labels the closing home button `Sign up for notebooks`. `src: Core features, The home route rule 8`
- [ ] `C-CF-54` `literal` The app shows the AI headline `Supercharge your data workflow with AI`. `src: Core features, The AI route rule 1`
- [ ] `C-CF-55` `literal` The app labels the AI hero button `Watch the demo`. `src: Core features, The AI route rule 1`
- [ ] `C-CF-56` `capability` The app shows the second AI panel's headline about checkable answers. `src: Core features, The AI route rule 2`
- [ ] `C-CF-57` `literal` The app shows the AI panel headed `Pair with AI`. `src: Core features, The AI route rule 2`
- [ ] `C-CF-58` `capability` The app lists exactly eight use-case headings on the AI route. `src: Core features, The AI route rule 3`
- [ ] `C-CF-59` `literal` The app lists the use case `Define a metric with natural language`. `src: Core features, The AI route rule 3`
- [ ] `C-CF-60` `literal` The app attributes a testimonial to `Alex Rivera`. `src: Core features, The AI route rule 4`
- [ ] `C-CF-61` `literal` The app attributes a testimonial to `Sam Okafor`. `src: Core features, The AI route rule 4`
- [ ] `C-CF-62` `literal` The app labels each testimonial link `See their work`. `src: Core features, The AI route rule 4`
- [ ] `C-CF-63` `literal` The app offers the sort tab `Trending`. `src: Core features, The community listing rule 1`
- [ ] `C-CF-64` `literal` The app offers the sort tab `Most stars all time`. `src: Core features, The community listing rule 1`
- [ ] `C-CF-65` `constraint` The app selects `Most stars all time` as the default sort. `src: Core features, The community listing rule 1`
- [ ] `C-CF-66` `literal` The app orders the default listing with `D3 Gallery` first at `1000` stars. `src: Core features, The community listing rule 2`
- [ ] `C-CF-67` `literal` The app places `Collapsible Tree` ninth at `399` stars. `src: Core features, The community listing rule 2`
- [ ] `C-CF-68` `literal` The app pages the listing at `30` per page. `src: Core features, The community listing rule 3`
- [ ] `C-CF-69` `capability` The app reads a count line naming the range with the total. `src: Core features, The community listing rule 3`
- [ ] `C-CF-70` `constraint` The app leaves `Prev` unavailable on the first listing page. `src: Core features, The community listing rule 3`
- [ ] `C-CF-71` `capability` The app advances to the second listing page from `Next`. `src: Core features, The community listing rule 3`
- [ ] `C-CF-72` `ui` The app switches between a grid presentation with a list presentation, leaving the order alone. `src: Core features, The community listing rule 4`
- [ ] `C-CF-73` `literal` The app marks `Zoomable Sunburst` as forked from another notebook. `src: Core features, The community listing rule 5`
- [ ] `C-CF-74` `capability` The app shows a star count on each listing card. `src: Core features, The community listing rule 5`
- [ ] `C-CF-75` `constraint` The app keeps every star count at zero or above. `src: Core features, The community listing rule 6`
- [ ] `C-CF-76` `constraint` The app lets no notebook be forked from itself. `src: Core features, The community listing rule 6`
- [ ] `C-CF-77` `literal` The app heads the sign-up card `Sign up`. `src: Core features, Sign up rule 1`
- [ ] `C-CF-78` `literal` The app offers the account method `GitHub`. `src: Core features, Sign up rule 1`
- [ ] `C-CF-79` `literal` The app offers the account method `Email`. `src: Core features, Sign up rule 1`
- [ ] `C-CF-80` `literal` The app shows the fine print `By continuing you agree to our Terms of Service.` `src: Core features, Sign up rule 2`
- [ ] `C-CF-81` `capability` The app creates a free reader account from the email method. `src: Core features, Sign up rule 3`
- [ ] `C-CF-82` `constraint` The app creates no second account for an address that already has one. `src: Core features, Sign up rule 4`
- [ ] `C-CF-83` `capability` The app leads every call to action to the sign-up card. `src: Core features, Sign up rule 5`
- [ ] `C-CF-84` `constraint` The app refuses a submission that fills the unattended decoy field. `src: Core features, Sign up rule 6`
- [ ] `C-CF-85` `constraint` The app refuses the same form submitted repeatedly in quick succession. `src: Core features, Sign up rule 6`
- [ ] `C-CF-86` `constraint` The app creates no account from a refused submission. `src: Core features, Sign up rule 6`
- [ ] `C-CF-87` `capability` The app renders one not-found screen for every address naming no published page. `src: Core features, The not-found chrome rule 1`
- [ ] `C-CF-88` `literal` The app shows the not-found copy `Sorry, but we can't find that page right now.` `src: Core features, The not-found chrome rule 2`
- [ ] `C-CF-89` `capability` The app links `browse through popular notebooks` to the listing. `src: Core features, The not-found chrome rule 2`
- [ ] `C-CF-90` `capability` The app renders full header with footer around the not-found screen. `src: Core features, The not-found chrome rule 1`
- [ ] `C-CF-91` `literal` The app lists the footer column `Platform`. `src: Core features, The footer rule 2`
- [ ] `C-CF-92` `literal` The app lists the footer column `Company`. `src: Core features, The footer rule 2`
- [ ] `C-CF-93` `literal` The app shows the legal line `© 2026 Datalume, Inc.` `src: Core features, The footer rule 3`
- [ ] `C-CF-94` `literal` The app shows the footer legal link `Vulnerability Disclosure`. `src: Core features, The footer rule 3`
- [ ] `C-CF-95` `capability` The app records a newsletter subscriber from an address. `src: Core features, The footer rule 4`
- [ ] `C-CF-96` `constraint` The app records no second subscriber for an address already subscribed. `src: Core features, The footer rule 4`
- [ ] `C-CF-97` `capability` The app asserts reactive computation on the home route. `src: Core features, What the site claims rule 1`
- [ ] `C-CF-98` `capability` The app asserts real-time multiplayer on a blue panel. `src: Core features, What the site claims rule 3`
- [ ] `C-CF-99` `capability` The app asserts sandboxed execution through its footer posture links. `src: Core features, What the site claims rule 4`
- [ ] `C-CF-100` `literal` The app serves a terms page at `/terms-of-service`. `src: Core features, The launch surface rule 1`
- [ ] `C-CF-101` `capability` The app links the terms page from the footer of every page. `src: Core features, The launch surface rule 1`
- [ ] `C-CF-102` `literal` The app serves a sitemap at `/sitemap.xml`. `src: Core features, The launch surface rule 2`
- [ ] `C-CF-103` `constraint` The app omits every draft page from the sitemap. `src: Core features, The launch surface rule 2`
- [ ] `C-CF-104` `literal` The app serves a robots file at `/robots.txt` pointing at the sitemap. `src: Core features, The launch surface rule 2`
- [ ] `C-CF-105` `constraint` The app carries a strict transport policy on every response. `src: Core features, The launch surface rule 3`
- [ ] `C-CF-106` `constraint` The app carries a nosniff content-type policy on every response. `src: Core features, The launch surface rule 3`
- [ ] `C-CF-107` `constraint` The app leaks no credential into anything the browser downloads. `src: Core features, The launch surface rule 4`

## C-UF User flow

- [ ] `C-UF-01` `literal` The app serves the home page at `/`. `src: User flow route table row 1`
- [ ] `C-UF-02` `literal` The app serves the AI route at `/ai`. `src: User flow route table row 2`
- [ ] `C-UF-03` `literal` The app serves the listing at `/top`. `src: User flow route table row 3`
- [ ] `C-UF-04` `literal` The app serves the sign-up card at `/new`. `src: User flow route table row 4`
- [ ] `C-UF-05` `literal` The app serves author sign-in at `/studio/login`. `src: User flow route table row 8`
- [ ] `C-UF-06` `capability` The app sends an unauthenticated visitor from a studio address to sign-in. `src: User flow, Entry and redirects`
- [ ] `C-UF-07` `capability` The app preserves a destination across a sign-in redirect. `src: User flow, Entry and redirects`
- [ ] `C-UF-08` `capability` The app lands an author on the studio after a sign-in with no destination. `src: User flow, Entry and redirects`
- [ ] `C-UF-09` `capability` The app returns a visitor to the home page after signing out. `src: User flow, Entry and redirects`
- [ ] `C-UF-10` `capability` The app keeps unsaved block text across an expired token. `src: User flow, Entry and redirects`
- [ ] `C-UF-11` `capability` The app shows an empty state on a listing tab holding no notebooks. `src: User flow, States`
- [ ] `C-UF-12` `capability` The app shows an empty state on a studio holding no pages. `src: User flow, States`
- [ ] `C-UF-13` `capability` The app renders chrome around a page holding no blocks. `src: User flow, States`
- [ ] `C-UF-14` `capability` The app shows a loading state on every route. `src: User flow, States`
- [ ] `C-UF-15` `constraint` The app leaves a page standing after a rejected action. `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The app grounds its editorial bands in a near-white neutral. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-02` `literal` The app sets body text in a `near-black neutral`. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-03` `literal` The app grounds the hero in a `near-black neutral`. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-04` `ui` The app carries a vivid mint teal as its primary accent. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-05` `literal` The app fills its feature panels with a `mid, soft blue`. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-06` `literal` The app ornaments the feature cards with a `mid, soft indigo`. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-07` `ui` The app carries one gradient, falling from magenta to orange, on the AI panels alone. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-08` `ui` The app renders code output in a terminal palette on a dark ground. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-09` `literal` The app sets the UI in `Inter`. `src: UI/UX notes, Typography`
- [ ] `C-UX-10` `literal` The app sets display headlines in `Spline Sans Mono`. `src: UI/UX notes, Typography`
- [ ] `C-UX-11` `literal` The app sets notebook titles in `Source Serif Pro`. `src: UI/UX notes, Typography`
- [ ] `C-UX-12` `ui` The app sets its largest headlines in the monospaced face rather than a sans. `src: UI/UX notes, Typography`
- [ ] `C-UX-13` `literal` The app sets captions with metadata at `12px`. `src: UI/UX notes, Typography`
- [ ] `C-UX-14` `ui` The app paints text immediately with a fallback stack behind each family. `src: UI/UX notes, Typography`
- [ ] `C-UX-15` `ui` The app caps the measure of its centred column. `src: UI/UX notes, Grid and shape`
- [ ] `C-UX-16` `ui` The app breaks its colour panels out to the viewport edge. `src: UI/UX notes, Grid and shape`
- [ ] `C-UX-17` `ui` The app rounds pills fully. `src: UI/UX notes, Grid and shape`
- [ ] `C-UX-18` `ui` The app lifts a card softly so the card reads as floating. `src: UI/UX notes, Grid and shape`
- [ ] `C-UX-19` `ui` The app draws every glyph as a line shape in the current text colour. `src: UI/UX notes, Iconography`
- [ ] `C-UX-20` `ui` The app draws the brand mark as concentric rings around a filled centre dot. `src: UI/UX notes, Iconography`
- [ ] `C-UX-21` `ui` The app sets the footer wordmark as live type. `src: UI/UX notes, Iconography`
- [ ] `C-UX-22` `ui` The app sticks the header above everything else on the page. `src: UI/UX notes, Chrome`
- [ ] `C-UX-23` `ui` The app recolours the header by interpolating as the hero passes. `src: UI/UX notes, Chrome`
- [ ] `C-UX-24` `ui` The app keeps the measure comfortable rather than airy on the listing. `src: UI/UX notes, Density`
- [ ] `C-UX-25` `ui` The app eases movement with considered entrance with exit. `src: UI/UX notes, Motion character`
- [ ] `C-UX-26` `ui` The app pulses a recomputing cell amber before settling back to the ground. `src: UI/UX notes, Motion character`
- [ ] `C-UX-27` `constraint` The app declares transitions per property rather than as one blanket rule. `src: UI/UX notes, Motion character`
- [ ] `C-UX-28` `ui` The app advances the community rail on a fixed one-minute loop. `src: UI/UX notes, Scroll`
- [ ] `C-UX-29` `ui` The app animates the hero visualization on its own rather than replaying a clip. `src: UI/UX notes, Scroll`
- [ ] `C-UX-30` `ui` The app scripts a second cursor in the multiplayer preview variant. `src: UI/UX notes, The notebook preview`
- [ ] `C-UX-31` `ui` The app frames the embed preview variant with an attribution badge. `src: UI/UX notes, The notebook preview`
- [ ] `C-UX-32` `ui` The app stacks the three feature cards into one column at a narrow width. `src: UI/UX notes, Responsive behaviour`
- [ ] `C-UX-33` `ui` The app collapses the resources menu to a hamburger at a narrow width. `src: UI/UX notes, Responsive behaviour`
- [ ] `C-UX-34` `constraint` The app gates hover affordances so a touch device inherits none. `src: UI/UX notes, Responsive behaviour`
- [ ] `C-UX-35` `constraint` The app meets the WCAG AA contrast bar in both header states. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-36` `constraint` The app shows a visible focus ring on every keyboard-reachable control. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-37` `constraint` The app labels every icon-only control. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-38` `constraint` The app carries no meaning by colour alone. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-39` `constraint` The app stills the marquee under a reduced-motion preference. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-40` `constraint` The app stops the scripted cursor under a reduced-motion preference. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-41` `constraint` The app keeps the site usable zoomed to twice its size. `src: UI/UX notes, Accessibility floors`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app renders complete HTML on the server for every route. `src: Technical requirements para 1`
- [ ] `C-TR-02` `literal` The app reads its datastore location from `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-03` `literal` The app reads its object store credentials from `STORAGE_ACCESS_KEY`. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` The app authenticates the JSON API with bearer tokens. `src: Technical requirements para 1`
- [ ] `C-TR-05` `constraint` The app introduces no backing service beyond the two named providers. `src: Technical requirements para 2`
- [ ] `C-TR-06` `constraint` The app hardcodes no host, no port, no credential. `src: Technical requirements para 3`
- [ ] `C-TR-07` `constraint` The app settles visibility on the server whatever a listing shows. `src: Technical requirements para 4`
- [ ] `C-TR-08` `capability` The app serves marketing content from its own store as ordered blocks. `src: Technical requirements para 5`
- [ ] `C-TR-09` `capability` The app reads the listing as a paginated sortable query. `src: Technical requirements para 5`

## C-DM Data model

- [ ] `C-DM-01` `data` The app stores every timestamp in UTC. `src: Data model para 1`
- [ ] `C-DM-02` `literal` The app accepts `deku-demo-pw-2026` at login for every seeded account. `src: Data model, password paragraph`
- [ ] `C-DM-03` `data` The app keeps a unique email per author. `src: Data model, authors`
- [ ] `C-DM-04` `data` The app keeps a unique email per reader. `src: Data model, readers`
- [ ] `C-DM-05` `data` The app records which method created a reader account. `src: Data model, readers`
- [ ] `C-DM-06` `data` The app keeps a unique slug per page. `src: Data model, pages`
- [ ] `C-DM-07` `constraint` The app leaves a draft page's published timestamp empty. `src: Data model, pages`
- [ ] `C-DM-08` `constraint` The app keeps a page slug unchanged once the page has published. `src: Data model, pages`
- [ ] `C-DM-09` `constraint` The app keeps block positions unique within a page. `src: Data model, blocks`
- [ ] `C-DM-10` `data` The app keeps a unique object key per media row. `src: Data model, media`
- [ ] `C-DM-11` `data` The app keeps a unique digest per media row. `src: Data model, media`
- [ ] `C-DM-12` `data` The app derives media visibility from the state of the pages referencing the object. `src: Data model, media`
- [ ] `C-DM-13` `data` The app keeps a unique slug per notebook. `src: Data model, notebooks`
- [ ] `C-DM-14` `constraint` The app keeps every comment count at zero or above. `src: Data model, notebooks`
- [ ] `C-DM-15` `data` The app stores the AI route's testimonials as rows. `src: Data model, testimonials`
- [ ] `C-DM-16` `data` The app stores the AI route's use cases as rows. `src: Data model, use_cases`
- [ ] `C-DM-17` `data` The app stores the footer's links as rows. `src: Data model, footer_links`
- [ ] `C-DM-18` `data` The app keeps a unique email per newsletter subscriber. `src: Data model, newsletter_subscribers`
- [ ] `C-DM-19` `constraint` The app leaves exactly one published page after two simultaneous publishes. `src: Data model, concurrency invariants`
- [ ] `C-DM-20` `constraint` The app leaves exactly one reader row after two simultaneous signups with one address. `src: Data model, concurrency invariants`
- [ ] `C-DM-21` `constraint` The app leaves one media row after two simultaneous uploads of identical bytes. `src: Data model, concurrency invariants`
- [ ] `C-DM-22` `constraint` The app leaves no page carrying one position twice after two simultaneous insertions. `src: Data model, concurrency invariants`
- [ ] `C-DM-23` `constraint` The app duplicates no row when the app restarts. `src: Data model, seed data`
- [ ] `C-DM-24` `literal` The app seeds a published page `home`. `src: Data model, seed pages table`
- [ ] `C-DM-25` `literal` The app seeds a published page `ai`. `src: Data model, seed pages table`
- [ ] `C-DM-26` `literal` The app seeds a published page `top`. `src: Data model, seed pages table`
- [ ] `C-DM-27` `literal` The app seeds a draft page `field-guide`. `src: Data model, seed pages table`
- [ ] `C-DM-28` `literal` The app seeds a notebook `d3-gallery` at `1000` stars. `src: Data model, seed notebook table`
- [ ] `C-DM-29` `literal` The app seeds a notebook `inputs` at `991` stars. `src: Data model, seed notebook table`
- [ ] `C-DM-30` `literal` The app seeds a notebook `learn-d3-introduction` at `755` stars. `src: Data model, seed notebook table`
- [ ] `C-DM-31` `literal` The app seeds a notebook `datalume-and-creative-coding` at `603` stars. `src: Data model, seed notebook table`
- [ ] `C-DM-32` `literal` The app seeds a notebook `zoomable-sunburst` at `511` stars. `src: Data model, seed notebook table`
- [ ] `C-DM-33` `literal` The app seeds a notebook `datalume-plot` at `450` stars. `src: Data model, seed notebook table`
- [ ] `C-DM-34` `literal` The app seeds a notebook `force-directed-graph-component` at `418` stars. `src: Data model, seed notebook table`
- [ ] `C-DM-35` `literal` The app seeds a notebook `enigma-machine` at `417` stars. `src: Data model, seed notebook table`
- [ ] `C-DM-36` `literal` The app seeds a notebook `collapsible-tree` at `399` stars. `src: Data model, seed notebook table`
- [ ] `C-DM-37` `data` The app seeds thirty-three notebooks in all. `src: Data model, seed data`
- [ ] `C-DM-38` `data` The app seeds one media object per page. `src: Data model, seed data`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app builds no reactive engine. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The app builds no execution sandbox. `src: Constraints bullet 1`
- [ ] `C-CN-03` `constraint` The app offers no payment. `src: Constraints bullet 2`
- [ ] `C-CN-04` `constraint` The app offers no search index. `src: Constraints bullet 3`
- [ ] `C-CN-05` `constraint` The app offers no comment thread. `src: Constraints bullet 4`
- [ ] `C-CN-06` `constraint` The app offers no starring by a visitor. `src: Constraints bullet 4`
- [ ] `C-CN-07` `constraint` The app offers no role beyond author with reader. `src: Constraints bullet 5`
- [ ] `C-CN-08` `constraint` The app reproduces no real customer identity. `src: Constraints bullet 6`
- [ ] `C-CN-09` `constraint` The app makes no external network call beyond the two named backing services. `src: Constraints bullet 7`
- [ ] `C-CN-10` `constraint` The app ships no video. `src: Constraints bullet 8`
- [ ] `C-CN-11` `constraint` The app ships no native application. `src: Constraints bullet 9`
- [ ] `C-CN-12` `constraint` The app stays responsive at a few thousand notebooks. `src: Constraints bullet 10`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app reads its public address from `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The app listens on container-internal port `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The app reads its outside port from `APP_PUBLIC_PORT`. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The app serves the HTTP API under the `/api` prefix on the same origin. `src: Deployment contract bullet 2`
- [ ] `C-DC-05` `contract` The app serves `/api/health` with status `200` once ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-07` `contract` The app binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-08` `literal` The app accepts an email with a password at `/api/auth/signup`. `src: Deployment contract, API shapes`
- [ ] `C-DC-09` `literal` The app returns one published page with its blocks at `/api/pages/`. `src: Deployment contract, API shapes`
- [ ] `C-DC-10` `literal` The app returns the signed-in author's own pages at `/api/pages`. `src: Deployment contract, API shapes`
- [ ] `C-DC-11` `literal` The app publishes a page at `/api/pages/{slug}/publish`. `src: Deployment contract, API shapes`
- [ ] `C-DC-12` `literal` The app creates a block at `/api/blocks`. `src: Deployment contract, API shapes`
- [ ] `C-DC-13` `literal` The app removes a block at `/api/blocks/{id}`. `src: Deployment contract, API shapes`
- [ ] `C-DC-14` `literal` The app uploads media at `/api/media`. `src: Deployment contract, API shapes`
- [ ] `C-DC-15` `literal` The app serves an object at `/api/media/{id}`. `src: Deployment contract, API shapes`
- [ ] `C-DC-16` `literal` The app returns a sortable paginated listing at `/api/notebooks`. `src: Deployment contract, API shapes`
- [ ] `C-DC-17` `literal` The app creates a reader at `/api/signups`. `src: Deployment contract, API shapes`
- [ ] `C-DC-18` `literal` The app records a subscriber at `/api/newsletter`. `src: Deployment contract, API shapes`
- [ ] `C-DC-19` `constraint` The app rejects an invalid call as a client error rather than a server error. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-20` `constraint` The app requires bearer auth on every endpoint outside the named public ones. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-21` `constraint` The app keeps no stand-in for an object in the bucket. `src: Deployment contract, No mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `author@example.com` | seeded author, owns the published pages | C-RL-15 | User roles, accounts table |
| `author2@example.com` | seeded author, owns the draft page | C-RL-16 | User roles, accounts table |
| `reader@example.com` | seeded reader | C-RL-17 | User roles, accounts table |
| `deku-demo-pw-2026` | password for every seeded account | C-DM-02 | Data model, password paragraph |
| `draft` | page state before publication | C-CF-11 | Core features, Draft and publish rule 1 |
| `published` | page state after publication | C-CF-12 | Core features, Draft and publish rule 1 |
| `hero` | block kind | C-CF-05 | Core features, The composed page rule 2 |
| `color_panel` | block kind | C-CF-06 | Core features, The composed page rule 2 |
| `1` | first block position | C-CF-08 | Core features, The composed page rule 3 |
| `media/{page_slug}/{sha256_of_bytes}.{ext}` | object key scheme | C-CF-24 | Core features, Media rule 2 |
| `STORAGE_ENDPOINT` | object store location variable | C-CF-22 | Core features, Media rule 1 |
| `STORAGE_BUCKET` | bucket name variable | C-CF-23 | Core features, Media rule 1 |
| `STORAGE_ACCESS_KEY` | object store credential variable | C-TR-03 | Technical requirements para 1 |
| `DATABASE_URL` | datastore location variable | C-TR-02 | Technical requirements para 1 |
| `APP_PUBLIC_URL` | public address variable | C-DC-01 | Deployment contract bullet 1 |
| `APP_PUBLIC_PORT` | outside port variable | C-DC-03 | Deployment contract bullet 1 |
| `4173` | container-internal port | C-DC-02 | Deployment contract bullet 1 |
| `200` | health status | C-DC-05 | Deployment contract bullet 3 |
| `0.0.0.0` | bind address | C-DC-07 | Deployment contract bullet 9 |
| `/api` | API prefix | C-DC-04 | Deployment contract bullet 2 |
| `/api/auth/login` | sign-in endpoint | C-CF-01 | Core features, Auth |
| `/api/auth/signup` | signup endpoint | C-DC-08 | Deployment contract, API shapes |
| `/api/pages/` | one published page endpoint prefix | C-DC-09 | Deployment contract, API shapes |
| `/api/pages` | author's own pages endpoint | C-DC-10 | Deployment contract, API shapes |
| `/api/pages/{slug}/publish` | publish endpoint | C-DC-11 | Deployment contract, API shapes |
| `/api/blocks` | block creation endpoint | C-DC-12 | Deployment contract, API shapes |
| `/api/blocks/{id}` | block removal endpoint | C-DC-13 | Deployment contract, API shapes |
| `/api/media` | media upload endpoint | C-DC-14 | Deployment contract, API shapes |
| `/api/media/{id}` | object read endpoint | C-DC-15 | Deployment contract, API shapes |
| `/api/notebooks` | listing endpoint | C-DC-16 | Deployment contract, API shapes |
| `/api/signups` | reader creation endpoint | C-DC-17 | Deployment contract, API shapes |
| `/api/newsletter` | subscriber endpoint | C-DC-18 | Deployment contract, API shapes |
| `/` | home route | C-UF-01 | User flow route table |
| `/ai` | AI route | C-UF-02 | User flow route table |
| `/top` | listing route | C-UF-03 | User flow route table |
| `/new` | sign-up route | C-UF-04 | User flow route table |
| `/studio/login` | author sign-in route | C-UF-05 | User flow route table |
| `/studio` | studio route | C-CF-29 | Core features, The authoring studio rule 1 |
| `/terms-of-service` | terms route | C-CF-100 | Core features, The launch surface rule 1 |
| `/sitemap.xml` | sitemap route | C-CF-102 | Core features, The launch surface rule 2 |
| `/robots.txt` | robots route | C-CF-104 | Core features, The launch surface rule 2 |
| `home` | seeded published page slug | C-DM-24 | Data model, seed pages table |
| `ai` | seeded published page slug | C-DM-25 | Data model, seed pages table |
| `top` | seeded published page slug | C-DM-26 | Data model, seed pages table |
| `field-guide` | seeded draft page slug | C-DM-27 | Data model, seed pages table |
| `d3-gallery` | seeded notebook slug | C-DM-28 | Data model, seed notebook table |
| `inputs` | seeded notebook slug | C-DM-29 | Data model, seed notebook table |
| `learn-d3-introduction` | seeded notebook slug | C-DM-30 | Data model, seed notebook table |
| `datalume-and-creative-coding` | seeded notebook slug | C-DM-31 | Data model, seed notebook table |
| `zoomable-sunburst` | seeded notebook slug, the forked one | C-DM-32 | Data model, seed notebook table |
| `datalume-plot` | seeded notebook slug | C-DM-33 | Data model, seed notebook table |
| `force-directed-graph-component` | seeded notebook slug | C-DM-34 | Data model, seed notebook table |
| `enigma-machine` | seeded notebook slug | C-DM-35 | Data model, seed notebook table |
| `collapsible-tree` | seeded notebook slug | C-DM-36 | Data model, seed notebook table |
| `1000` | top notebook star count | C-DM-28 | Data model, seed notebook table |
| `991` | second notebook star count | C-DM-29 | Data model, seed notebook table |
| `755` | third notebook star count | C-DM-30 | Data model, seed notebook table |
| `603` | fourth notebook star count | C-DM-31 | Data model, seed notebook table |
| `511` | fifth notebook star count | C-DM-32 | Data model, seed notebook table |
| `450` | sixth notebook star count | C-DM-33 | Data model, seed notebook table |
| `418` | seventh notebook star count | C-DM-34 | Data model, seed notebook table |
| `417` | eighth notebook star count | C-DM-35 | Data model, seed notebook table |
| `399` | ninth notebook star count | C-DM-36 | Data model, seed notebook table |
| `30` | listing page size | C-CF-68 | Core features, The community listing rule 3 |
| `D3 Gallery` | top notebook title | C-CF-66 | Core features, The community listing rule 2 |
| `Collapsible Tree` | ninth notebook title | C-CF-67 | Core features, The community listing rule 2 |
| `Zoomable Sunburst` | the seeded forked notebook | C-CF-73 | Core features, The community listing rule 5 |
| `Trending` | sort tab | C-CF-63 | Core features, The community listing rule 1 |
| `Most stars all time` | default sort tab | C-CF-64 | Core features, The community listing rule 1 |
| `Notebooks 2.0 is now live on the web.` | banner copy | C-CF-35 | Core features, The home route rule 1 |
| `Try it now` | banner button | C-CF-36 | Core features, The home route rule 1 |
| `Not your typical notebook` | home headline | C-CF-39 | Core features, The home route rule 2 |
| `Try it for free` | hero solid button | C-CF-40 | Core features, The home route rule 2 |
| `Explore the docs` | hero outlined button | C-CF-41 | Core features, The home route rule 2 |
| `The shortest path from idea to live code` | value line | C-CF-42 | Core features, The home route rule 3 |
| `Literate programming` | feature card heading | C-CF-43 | Core features, The home route rule 4 |
| `Connect to any data` | feature card heading | C-CF-44 | Core features, The home route rule 4 |
| `Built-in reactivity` | feature card heading | C-CF-45 | Core features, The home route rule 4 |
| `MULTIPLAYER EDITING` | blue panel eyebrow | C-CF-46 | Core features, The home route rule 5 |
| `Collaborate and share` | blue panel headline | C-CF-47 | Core features, The home route rule 5 |
| `EMBEDDING` | second blue panel eyebrow | C-CF-48 | Core features, The home route rule 6 |
| `Ready for production` | second blue panel headline | C-CF-49 | Core features, The home route rule 6 |
| `Join the community` | community headline | C-CF-50 | Core features, The home route rule 7 |
| `Get started today` | closing headline | C-CF-52 | Core features, The home route rule 8 |
| `Sign up for notebooks` | closing button | C-CF-53 | Core features, The home route rule 8 |
| `Supercharge your data workflow with AI` | AI headline | C-CF-54 | Core features, The AI route rule 1 |
| `Watch the demo` | AI hero button | C-CF-55 | Core features, The AI route rule 1 |
| `Answers you can verify` | AI panel headline | C-CF-56 | Core features, The AI route rule 2 |
| `Pair with AI` | AI panel headline | C-CF-57 | Core features, The AI route rule 2 |
| `Define a metric with natural language` | use case | C-CF-59 | Core features, The AI route rule 3 |
| `Alex Rivera` | testimonial person | C-CF-60 | Core features, The AI route rule 4 |
| `Sam Okafor` | testimonial person | C-CF-61 | Core features, The AI route rule 4 |
| `See their work` | testimonial link | C-CF-62 | Core features, The AI route rule 4 |
| `Sign up` | sign-up card heading | C-CF-77 | Core features, Sign up rule 1 |
| `GitHub` | account method | C-CF-78 | Core features, Sign up rule 1 |
| `Email` | account method | C-CF-79 | Core features, Sign up rule 1 |
| `By continuing you agree to our Terms of Service.` | sign-up fine print | C-CF-80 | Core features, Sign up rule 2 |
| `Sorry, but we can't find that page right now.` | not-found copy | C-CF-88 | Core features, The not-found chrome rule 2 |
| `Platform` | footer column | C-CF-91 | Core features, The footer rule 2 |
| `Company` | footer column | C-CF-92 | Core features, The footer rule 2 |
| `© 2026 Datalume, Inc.` | footer legal line | C-CF-93 | Core features, The footer rule 3 |
| `Vulnerability Disclosure` | footer legal link | C-CF-94 | Core features, The footer rule 3 |
| `near-black neutral` | body text and dark ground colour words | C-UX-02 | UI/UX notes, Palette by role |
| `mid, soft blue` | feature panel colour words | C-UX-05 | UI/UX notes, Palette by role |
| `mid, soft indigo` | selection handle colour words | C-UX-06 | UI/UX notes, Palette by role |
| `Inter` | UI family | C-UX-09 | UI/UX notes, Typography |
| `Spline Sans Mono` | display family | C-UX-10 | UI/UX notes, Typography |
| `Source Serif Pro` | notebook title family | C-UX-11 | UI/UX notes, Typography |
| `12px` | caption and metadata size | C-UX-13 | UI/UX notes, Typography |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the twenty-four notebooks beyond the seeded nine | C-DM-37 | their slugs and titles are the builder's, bounded only by a star count below the ninth |
| the count line's range and total | C-CF-69 | derived from the page and the seed rather than a fixed string |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 1 | 5 |
| User roles | 1 | 17 |
| Core features | 4 | 107 |
| User flow | 4 | 15 |
| UI and UX notes | 5 | 41 |
| Technical requirements | 5 | 9 |
| Data model | 7 | 38 |
| Constraints | 3 | 12 |
| Deployment contract | 8 | 21 |
