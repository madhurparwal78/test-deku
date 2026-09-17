# Checklist: Northform Immersive Studio Showcase

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 297
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The site presents the studio portfolio work to prospective clients. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The site collects a contact enquiry from a visitor. `src: Overview para 1`
- [ ] `C-OV-03` `capability` The site collects a newsletter subscription from a visitor. `src: Overview para 1`
- [ ] `C-OV-04` `capability` The site opens on a loading sequence in which a mascot runs inside a filling ring. `src: Overview para 2`
- [ ] `C-OV-05` `capability` The site composites a full-viewport real-time three-dimensional layer behind the page. `src: Overview para 2`
- [ ] `C-OV-06` `capability` A headline assembles letter by letter out of depth. `src: Overview para 2`
- [ ] `C-OV-07` `capability` Each project carries its own accent colour family. `src: Overview para 2`
- [ ] `C-OV-08` `constraint` A record stays non-public until publication. `src: Overview para 4`
- [ ] `C-OV-09` `constraint` A draft case study hero image sits in the same bucket as a published one. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` An account holds the role `author` or the role `reader`. `src: User roles table`
- [ ] `C-RL-02` `role` An author reads every case study in either publication state. `src: User roles table row 1`
- [ ] `C-RL-03` `role` An author creates a case study. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An author publishes a record. `src: User roles table row 1`
- [ ] `C-RL-05` `role` An author unpublishes a record. `src: User roles table row 1`
- [ ] `C-RL-06` `role` An author uploads media. `src: User roles table row 1`
- [ ] `C-RL-07` `role` An author reads the page-view log. `src: User roles table row 1`
- [ ] `C-RL-08` `role` A reader reads every published case study. `src: User roles table row 2`
- [ ] `C-RL-09` `role` A reader sends an enquiry. `src: User roles table row 2`
- [ ] `C-RL-10` `role` A reader is denied a draft record. `src: User roles para 2`
- [ ] `C-RL-11` `role` A reader is denied the author desk. `src: User roles para 2`
- [ ] `C-RL-12` `role` A reader is denied an upload. `src: User roles para 2`
- [ ] `C-RL-13` `role` A reader is denied the page-view log. `src: User roles para 2`
- [ ] `C-RL-14` `role` An anonymous visitor reads every published case study. `src: User roles table row 3`
- [ ] `C-RL-15` `role` An anonymous visitor signs up as a reader. `src: User roles table row 3`
- [ ] `C-RL-16` `role` The server rejects a mutating request from a reader session to an author-only endpoint. `src: User roles para 3`
- [ ] `C-RL-17` `constraint` A rejected author-only request leaves the protected state unchanged. `src: User roles para 3`
- [ ] `C-RL-18` `constraint` A denial that would reveal existence returns what an absent slug returns. `src: User roles para 4`
- [ ] `C-RL-19` `constraint` A refusal for an already visible resource names the missing grant. `src: User roles para 4`
- [ ] `C-RL-20` `role` Signup always creates an account holding the role `reader`. `src: User roles para 5`
- [ ] `C-RL-21` `constraint` No route creates an account holding the role `author`. `src: User roles para 5`

## C-CF Core features

- [ ] `C-CF-01` `capability` `POST /api/auth/signup` creates a reader account. `src: Core features, Auth para 1`
- [ ] `C-CF-02` `literal` `POST /api/auth/signup` returns a bearer token named `access_token`. `src: Core features, Auth para 1`
- [ ] `C-CF-03` `literal` `POST /api/auth/login` returns a bearer token named `access_token`. `src: Core features, Auth para 1`
- [ ] `C-CF-04` `constraint` The app stores a password as a slow modern hash. `src: Core features, Auth para 1`
- [ ] `C-CF-05` `constraint` The app rejects an expired bearer token as unauthorized. `src: Core features, Auth para 1`
- [ ] `C-CF-06` `capability` An HTML route carries a session cookie set at login. `src: Core features, Auth para 1`
- [ ] `C-CF-07` `capability` Repeated wrong passwords against one address attract a progressive backoff. `src: Core features, Auth para 1`
- [ ] `C-CF-08` `constraint` A backoff never becomes a permanent lockout. `src: Core features, Auth para 1`
- [ ] `C-CF-09` `literal` Signing in with a seeded email plus the password `deku-demo-pw-2026` succeeds. `src: Core features item 1`
- [ ] `C-CF-10` `constraint` An unknown email refusal matches a wrong password refusal in wording. `src: Core features item 1`
- [ ] `C-CF-11` `constraint` A signup asking for the role `author` still creates a reader. `src: Core features item 2`
- [ ] `C-CF-12` `constraint` A request without a valid token to a protected endpoint changes nothing. `src: Core features item 3`
- [ ] `C-CF-13` `literal` The primary navigation carries `The Studio`, `Our Cases`, `Careers`, `Our Values`, `Contact` in that order. `src: Core features item 4`
- [ ] `C-CF-14` `literal` The three offices are `Detroit`, `Rotterdam`, `Lyon`. `src: Core features item 5`
- [ ] `C-CF-15` `literal` The contact address is `hello@northform.co`. `src: Core features item 5`
- [ ] `C-CF-16` `literal` The footer line above the contact address reads `We'd love to hear from you`. `src: Core features item 5`
- [ ] `C-CF-17` `capability` Choosing `Español` sets the Spanish locale prefix. `src: Core features item 6`
- [ ] `C-CF-18` `capability` The locale choice persists across a return visit carrying no prefix. `src: Core features item 6`
- [ ] `C-CF-19` `constraint` A route with no translation still renders in English. `src: Core features item 6`
- [ ] `C-CF-20` `ui` A fixed header carries the wordmark, the five primary links, a showreel link, a sound control, a menu control. `src: Core features, the public site para 1`
- [ ] `C-CF-21` `ui` The menu control opens a full-screen overlay carrying the full navigation. `src: Core features, the public site para 1`
- [ ] `C-CF-22` `ui` The footer carries the newsletter form. `src: Core features, the public site para 1`
- [ ] `C-CF-23` `ui` A cookie banner asks once about functional cookies. `src: Core features, the public site para 1`
- [ ] `C-CF-24` `constraint` The cookie banner answer survives a reload. `src: Core features, the public site para 1`
- [ ] `C-CF-25` `capability` `/cases` lists published case studies as a card grid, newest first. `src: Core features, case studies para 1`
- [ ] `C-CF-26` `capability` `/cases` filters the card grid by discipline. `src: Core features, case studies para 1`
- [ ] `C-CF-27` `ui` `/cases/<slug>` binds that project accent to the page links, rules, captions, caret marks. `src: Core features, case studies para 1`
- [ ] `C-CF-28` `constraint` `GET /api/cases` returns only published cases to an anonymous visitor. `src: Core features item 7`
- [ ] `C-CF-29` `constraint` `GET /api/cases` returns only published cases to a reader. `src: Core features item 7`
- [ ] `C-CF-30` `capability` `GET /api/cases` returns drafts to an author who asks for drafts. `src: Core features item 7`
- [ ] `C-CF-31` `constraint` Filtering by discipline returns only cases of that discipline. `src: Core features item 8`
- [ ] `C-CF-32` `constraint` Filtering to a discipline with no published case returns an empty top-level array. `src: Core features item 8`
- [ ] `C-CF-33` `literal` Seven published case studies are seeded, the first being `lumenfest`. `src: Core features item 9`
- [ ] `C-CF-34` `constraint` A case study sits in the state `draft` or the state `published`. `src: Core features, publication state para 1`
- [ ] `C-CF-35` `capability` A published record is readable by an anonymous visitor. `src: Core features item 10`
- [ ] `C-CF-36` `constraint` A draft record is readable by an author alone. `src: Core features item 11`
- [ ] `C-CF-37` `constraint` `/cases/harbour-line-rebrand` answers an anonymous visitor as an absent slug answers. `src: Core features item 11`
- [ ] `C-CF-38` `constraint` `/cases/harbour-line-rebrand` answers a signed-in reader as an absent slug answers. `src: Core features item 11`
- [ ] `C-CF-39` `capability` `/cases/harbour-line-rebrand` renders in full for an author. `src: Core features item 11`
- [ ] `C-CF-40` `capability` Publishing stamps the publication time once. `src: Core features item 12`
- [ ] `C-CF-41` `constraint` Two simultaneous publishes of one case leave exactly one published row. `src: Core features item 12`
- [ ] `C-CF-42` `capability` Unpublishing moves the state back to `draft`. `src: Core features item 13`
- [ ] `C-CF-43` `constraint` Unpublished media becomes unreadable on the next request. `src: Core features item 13`
- [ ] `C-CF-44` `constraint` Every image lives in the MinIO bucket alone. `src: Core features, media para 1`
- [ ] `C-CF-45` `literal` A case asset object key takes the shape `cases/{case_slug}/{sha256_of_bytes}.{ext}`. `src: Core features item 14`
- [ ] `C-CF-46` `literal` A post asset object key takes the shape `posts/{post_slug}/{sha256_of_bytes}.{ext}`. `src: Core features item 14`
- [ ] `C-CF-47` `constraint` Uploading identical bytes to one case twice leaves exactly one object. `src: Core features item 15`
- [ ] `C-CF-48` `constraint` Uploading identical bytes to one case twice leaves exactly one asset row. `src: Core features item 15`
- [ ] `C-CF-49` `constraint` Two simultaneous uploads of identical bytes leave one stored object. `src: Core features item 15`
- [ ] `C-CF-50` `constraint` A draft record media is unreachable by object key. `src: Core features item 16`
- [ ] `C-CF-51` `constraint` A draft record media is unreachable by listing the bucket. `src: Core features item 16`
- [ ] `C-CF-52` `constraint` A link minted during publication stops reading after unpublishing. `src: Core features item 16`
- [ ] `C-CF-53` `data` Every asset carries alternative text stored with the asset. `src: Core features item 17`
- [ ] `C-CF-54` `capability` `/news` lists published posts newest first. `src: Core features item 18`
- [ ] `C-CF-55` `capability` `/news/<slug>` renders one journal article. `src: Core features item 18`
- [ ] `C-CF-56` `constraint` A draft post answers as a draft case study answers. `src: Core features item 18`
- [ ] `C-CF-57` `capability` `/careers` lists each open role with an office. `src: Core features item 19`
- [ ] `C-CF-58` `capability` `POST /api/enquiries` stores an enquiry. `src: Core features item 20`
- [ ] `C-CF-59` `ui` The contact route replaces the form in place with a success banner. `src: Core features item 20`
- [ ] `C-CF-60` `constraint` A submission missing a required field stores nothing. `src: Core features item 20`
- [ ] `C-CF-61` `constraint` A malformed address is rejected as a client error naming the field. `src: Core features item 20`
- [ ] `C-CF-62` `capability` `POST /api/subscribers` stores a subscriber. `src: Core features item 21`
- [ ] `C-CF-63` `constraint` Subscribing one address twice leaves exactly one subscriber row. `src: Core features item 21`
- [ ] `C-CF-64` `constraint` A repeat subscription reports success rather than an error. `src: Core features item 21`
- [ ] `C-CF-65` `ui` Both forms carry an idle state, a success state, a failure state. `src: Core features item 22`
- [ ] `C-CF-66` `ui` The success banner replaces the form without a page reload. `src: Core features item 22`
- [ ] `C-CF-67` `capability` `/desk` shows one table row per case study, post, open role. `src: Core features item 23`
- [ ] `C-CF-68` `ui` The desk table shows the title, the type, the state, the discipline or office, the accent, the publication date. `src: Core features item 23`
- [ ] `C-CF-69` `constraint` `/desk` gives a reader the not-found page. `src: Core features item 23`
- [ ] `C-CF-70` `capability` `/desk/cases/new` is a real address carrying a case creation form. `src: Core features item 24`
- [ ] `C-CF-71` `capability` `/desk/posts/new` is a real address carrying a post creation form. `src: Core features item 24`
- [ ] `C-CF-72` `capability` `/desk/roles/new` is a real address carrying a role creation form. `src: Core features item 24`
- [ ] `C-CF-73` `capability` A browser back from a creation route returns to the desk table. `src: Core features item 24`
- [ ] `C-CF-74` `constraint` A slug is unique within its collection. `src: Core features item 25`
- [ ] `C-CF-75` `constraint` A duplicate slug is rejected as a client error naming the conflict. `src: Core features item 25`
- [ ] `C-CF-76` `constraint` A slug is never reused after a delete. `src: Core features item 25`
- [ ] `C-CF-77` `ui` The loader holds a mascot running inside a ring on a near-black ground. `src: Core features item 26`
- [ ] `C-CF-78` `ui` The loader progress stroke fills clockwise from twelve o'clock. `src: Core features item 26`
- [ ] `C-CF-79` `constraint` The loader progress binds to real load fraction rather than to a timer. `src: Core features item 26`
- [ ] `C-CF-80` `ui` The three-dimensional layer holds the studio mascot as a lit model. `src: Core features item 27`
- [ ] `C-CF-81` `capability` The mascot pose tracks scroll progress on the home route. `src: Core features item 27`
- [ ] `C-CF-82` `ui` A display headline assembles letter by letter on a short stagger. `src: Core features item 28`
- [ ] `C-CF-83` `capability` An ambient bed plays under the experience. `src: Core features item 29`
- [ ] `C-CF-84` `capability` A header control mutes the ambient bed. `src: Core features item 29`
- [ ] `C-CF-85` `constraint` The mute choice persists across routes. `src: Core features item 29`
- [ ] `C-CF-86` `ui` The sound control pulses during live sound. `src: Core features item 29`
- [ ] `C-CF-87` `capability` A showreel opens as a full-screen takeover from the header. `src: Core features item 30`
- [ ] `C-CF-88` `ui` The showreel carries play, pause, a scrubbable progress bar, a current-time readout, mute, captions, a settings menu. `src: Core features item 30`
- [ ] `C-CF-89` `capability` The showreel closes back to the page. `src: Core features item 30`
- [ ] `C-CF-90` `ui` An unknown address renders the studio own not-found page. `src: Core features item 31`
- [ ] `C-CF-91` `literal` The not-found page carries the heading `Ooh shit!`. `src: Core features item 31`
- [ ] `C-CF-92` `literal` The not-found page carries the line `You're lost...`. `src: Core features item 31`
- [ ] `C-CF-93` `literal` The not-found page carries a `Back to homepage` link. `src: Core features item 31`
- [ ] `C-CF-94` `constraint` The not-found page answers as not found rather than as success. `src: Core features item 31`
- [ ] `C-CF-95` `contract` The site serves a favicon declared in every route document head. `src: Core features item 32`
- [ ] `C-CF-96` `constraint` Every public route carries a unique page title. `src: Core features item 33`
- [ ] `C-CF-97` `constraint` Every public route carries a unique meta description. `src: Core features item 33`
- [ ] `C-CF-98` `contract` `/sitemap.xml` lists every published public route. `src: Core features item 34`
- [ ] `C-CF-99` `contract` `/robots.txt` names the sitemap address. `src: Core features item 34`
- [ ] `C-CF-100` `constraint` A draft case study route never appears in the sitemap. `src: Core features item 34`
- [ ] `C-CF-101` `ui` Every page leads with exactly one primary action. `src: Core features item 35`
- [ ] `C-CF-102` `capability` The app records each page view with a route, a locale, a time. `src: Core features item 36`
- [ ] `C-CF-103` `constraint` A reader calling the page-view endpoint is denied. `src: Core features item 36`
- [ ] `C-CF-104` `capability` `/terms` carries the studio terms of use. `src: Core features item 32`
- [ ] `C-CF-105` `ui` The footer links to the terms route beside the privacy policy. `src: Core features item 32`

## C-UF User flow

- [ ] `C-UF-01` `capability` An unauthenticated request for `/desk` redirects to `/login`. `src: User flow, entry and redirects`
- [ ] `C-UF-02` `capability` A sign-in from that redirect returns to the remembered address. `src: User flow, entry and redirects`
- [ ] `C-UF-03` `constraint` A signed-in reader requesting `/desk` receives the not-found page. `src: User flow, entry and redirects`
- [ ] `C-UF-04` `capability` Signing out clears the session, returning to `/`. `src: User flow, entry and redirects`
- [ ] `C-UF-05` `capability` A half-filled form survives a token expiry without retyping. `src: User flow, entry and redirects`
- [ ] `C-UF-06` `capability` The app serves `/studio` as a public route. `src: User flow route table`
- [ ] `C-UF-07` `capability` The app serves `/values` as a public route. `src: User flow route table`
- [ ] `C-UF-08` `capability` The app serves `/privacy` as a public route. `src: User flow route table`
- [ ] `C-UF-09` `capability` The app serves `/signup` as a public route. `src: User flow route table`
- [ ] `C-UF-10` `ui` Every list carries an empty state naming the filter that produced the list. `src: User flow, states`
- [ ] `C-UF-11` `ui` Every empty list state offers one action. `src: User flow, states`
- [ ] `C-UF-12` `ui` A loading state keeps the chrome, replacing only the content region. `src: User flow, states`
- [ ] `C-UF-13` `ui` An error replaces the failed region, keeping the chrome. `src: User flow, states`
- [ ] `C-UF-14` `ui` An error offers a retry. `src: User flow, states`
- [ ] `C-UF-15` `ui` An error carries the request identifier. `src: User flow, states`
- [ ] `C-UF-16` `constraint` Forbidden is indistinguishable from not found. `src: User flow, states`
- [ ] `C-UF-17` `capability` The app serves `/terms` as a public route. `src: User flow route table`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The site commits to a dark mode alone. `src: UI/UX notes, mode and surface`
- [ ] `C-UX-02` `ui` The ground is a near-black neutral. `src: UI/UX notes, mode and surface`
- [ ] `C-UX-03` `ui` An inverted panel uses an off-white neutral rather than pure paper. `src: UI/UX notes, mode and surface`
- [ ] `C-UX-04` `ui` White carries almost all the reading text. `src: UI/UX notes, palette by role`
- [ ] `C-UX-05` `ui` A label uses a mid cool neutral. `src: UI/UX notes, palette by role`
- [ ] `C-UX-06` `ui` A divider uses a near-white muted indigo at low strength. `src: UI/UX notes, palette by role`
- [ ] `C-UX-07` `ui` A link uses a deep vivid blue. `src: UI/UX notes, palette by role`
- [ ] `C-UX-08` `ui` The focus ring uses the deep vivid blue of a link. `src: UI/UX notes, palette by role`
- [ ] `C-UX-09` `ui` The studio mark uses a light vivid red. `src: UI/UX notes, palette by role`
- [ ] `C-UX-10` `ui` One project accent is active at a time. `src: UI/UX notes, palette by role`
- [ ] `C-UX-11` `literal` Editorial headings use the family `GT Sectra Display`. `src: UI/UX notes, typography`
- [ ] `C-UX-12` `literal` The loudest display words use the family `Gilroy`. `src: UI/UX notes, typography`
- [ ] `C-UX-13` `literal` Interface, body, caption text uses the family `Heebo`. `src: UI/UX notes, typography`
- [ ] `C-UX-14` `literal` Body text is `14px` over a `29.4px` line. `src: UI/UX notes, typography`
- [ ] `C-UX-15` `literal` The primary display headline is `120px` over `107px`. `src: UI/UX notes, typography`
- [ ] `C-UX-16` `ui` Corners are barely softened across buttons, inputs, small controls. `src: UI/UX notes, shape, spacing and rules`
- [ ] `C-UX-17` `ui` Motion resolves on one of three recurring durations. `src: UI/UX notes, motion`
- [ ] `C-UX-18` `ui` The entrance cascade settles siblings one after another on a short stagger. `src: UI/UX notes, motion`
- [ ] `C-UX-19` `ui` A letter title starts tilted away from the reader, pushed back in depth. `src: UI/UX notes, motion`
- [ ] `C-UX-20` `ui` The menu control bars morph when pointed at. `src: UI/UX notes, motion`
- [ ] `C-UX-21` `ui` The sound control ripple grows a ring from nothing to full. `src: UI/UX notes, motion`
- [ ] `C-UX-22` `ui` A navigation link hover mark is built from a shadow copy of the glyph. `src: UI/UX notes, motion`
- [ ] `C-UX-23` `ui` A reduced-motion preference sets the cascade instantly. `src: UI/UX notes, motion`
- [ ] `C-UX-24` `ui` A reduced-motion preference pins parallax. `src: UI/UX notes, motion`
- [ ] `C-UX-25` `ui` A scroll position drives every reveal rather than the native scrollbar. `src: UI/UX notes, scroll`
- [ ] `C-UX-26` `ui` Scrolling back un-plays a reveal. `src: UI/UX notes, scroll`
- [ ] `C-UX-27` `ui` Every mark is inline vector geometry. `src: UI/UX notes, iconography`
- [ ] `C-UX-28` `ui` Every control carries resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes, components and states`
- [ ] `C-UX-29` `constraint` An unavailable state is never signalled by colour alone. `src: UI/UX notes, components and states`
- [ ] `C-UX-30` `capability` `Escape` closes one overlay level. `src: UI/UX notes, components and states`
- [ ] `C-UX-31` `ui` Desktop uses a multi-column grid. `src: UI/UX notes, responsive`
- [ ] `C-UX-32` `ui` Below the tablet boundary the layout collapses to one column. `src: UI/UX notes, responsive`
- [ ] `C-UX-33` `ui` The header primary links move into the menu overlay below the tablet boundary. `src: UI/UX notes, responsive`
- [ ] `C-UX-34` `constraint` Nothing overflows sideways at the narrowest viewport. `src: UI/UX notes, responsive`
- [ ] `C-UX-35` `constraint` Text meets a contrast ratio of at least `4.5:1`. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-36` `constraint` Large text meets a contrast ratio of at least `3:1`. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-37` `constraint` Every control is operable from the keyboard. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-38` `ui` A visible focus state is never removed. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-39` `literal` An icon-only control carries a visually hidden label such as `Toggle menu`. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-40` `constraint` Meaning is never carried by colour alone. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-41` `constraint` Every interactive target is at least `44px` on touch. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-42` `ui` Each route carries one first-level heading. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-43` `ui` A skip link is the first thing on every page. `src: UI/UX notes, accessibility floors`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The frontend is Alpine.js over server templates. `src: Technical requirements para 1`
- [ ] `C-TR-02` `constraint` The app carries no client-side router. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The backend is NestJS with Handlebars views on Node 20. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` Every route is a real address the server answers with a complete document. `src: Technical requirements para 1`
- [ ] `C-TR-05` `constraint` Every route still renders with script disabled. `src: Technical requirements para 1`
- [ ] `C-TR-06` `constraint` Both forms still submit with script disabled. `src: Technical requirements para 1`
- [ ] `C-TR-07` `contract` The app reads `DATABASE_URL` for PostgreSQL. `src: Technical requirements para 1`
- [ ] `C-TR-08` `contract` The app reads `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY` for MinIO. `src: Technical requirements para 1`
- [ ] `C-TR-09` `contract` The app reads `APP_PUBLIC_URL` for its public address. `src: Technical requirements para 1`
- [ ] `C-TR-10` `contract` The app reads `APP_PUBLIC_PORT` for its public port. `src: Technical requirements para 1`
- [ ] `C-TR-11` `constraint` The app introduces no second database, cache, queue, object store, identity provider, mail vendor. `src: Technical requirements para 2`
- [ ] `C-TR-12` `contract` `GET /api/health` returns a success once PostgreSQL plus the bucket are reachable. `src: Technical requirements para 3`
- [ ] `C-TR-13` `capability` One structured log line per request carries a request identifier, the route, the locale, the principal, the outcome. `src: Technical requirements para 3`
- [ ] `C-TR-14` `constraint` No password, token, storage credential reaches a log line. `src: Technical requirements para 3`
- [ ] `C-TR-15` `constraint` Nothing the browser can fetch contains a credential. `src: Technical requirements para 3`
- [ ] `C-TR-16` `contract` Every response carries a nosniff content-type policy. `src: Technical requirements para 4`
- [ ] `C-TR-17` `constraint` An invalid value is rejected as a client error naming the offending field. `src: Technical requirements para 5`
- [ ] `C-TR-18` `capability` The signup, login, enquiry, subscriber endpoints are rate limited per source address. `src: Technical requirements para 5`
- [ ] `C-TR-19` `constraint` A limited caller is told plainly rather than silently dropped. `src: Technical requirements para 5`
- [ ] `C-TR-20` `constraint` Every state-changing request carries a token a plain cross-site navigation cannot supply. `src: Technical requirements para 5`
- [ ] `C-TR-21` `constraint` No service account, support login, back door carries a system-level privilege invisible from the interface. `src: Technical requirements, privileges`
- [ ] `C-TR-22` `capability` The three-dimensional layer drops its post-processing pass under load. `src: Technical requirements, delivery and degradation`
- [ ] `C-TR-23` `constraint` A page still renders when the object store is unreachable. `src: Technical requirements, delivery and degradation`
- [ ] `C-TR-24` `constraint` No error surface shows a stack trace, an internal service name, a raw error string. `src: Technical requirements, delivery and degradation`
- [ ] `C-TR-25` `capability` A caller submitting repeatedly from one address is slowed rather than served. `src: Technical requirements para 5`

## C-DM Data model

- [ ] `C-DM-01` `data` The schema carries twelve tables. `src: Data model para 1`
- [ ] `C-DM-02` `constraint` Every timestamp is UTC. `src: Data model para 1`
- [ ] `C-DM-03` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model, password paragraph`
- [ ] `C-DM-04` `contract` Each seeded account is written into `/app/USER_README.md`. `src: Data model, password paragraph`
- [ ] `C-DM-05` `data` The `account` table carries a unique `email`. `src: Data model, account row`
- [ ] `C-DM-06` `data` The `case_study` table carries a unique `slug`. `src: Data model, case_study row`
- [ ] `C-DM-07` `data` The `case_band` table orders bands by `position`. `src: Data model, case_band row`
- [ ] `C-DM-08` `data` The `asset` table carries a unique `object_key`. `src: Data model, asset row`
- [ ] `C-DM-09` `data` The `subscriber` table carries a unique `email`. `src: Data model, subscriber row`
- [ ] `C-DM-10` `data` The `page_view` table carries a `route`, a `locale`, an `occurred_at`. `src: Data model, page_view row`
- [ ] `C-DM-11` `constraint` `discipline` is `Web`, `Strategy`, or `Design`. `src: Data model, closed enums`
- [ ] `C-DM-12` `constraint` `office` is `Detroit`, `Rotterdam`, or `Lyon`. `src: Data model, closed enums`
- [ ] `C-DM-13` `constraint` `state` is `draft` or `published`. `src: Data model, closed enums`
- [ ] `C-DM-14` `constraint` Restarting the app duplicates no row. `src: Data model, idempotent seeding`
- [ ] `C-DM-15` `constraint` Restarting the app re-uploads no object. `src: Data model, idempotent seeding`
- [ ] `C-DM-16` `literal` The studio name is `Northform`. `src: Data model, seed data`
- [ ] `C-DM-17` `literal` The seeded locales are `en` labelled `English` plus `es` labelled `Español`. `src: Data model, seed data`
- [ ] `C-DM-18` `literal` The seeded social set is `Facebook`, `Instagram`, `Dribbble`, `Twitter`. `src: Data model, seed data`
- [ ] `C-DM-19` `literal` The seeded draft case study slug is `harbour-line-rebrand`. `src: Data model, seed table row 8`
- [ ] `C-DM-20` `literal` The seeded case `grand-opera-of-verdal` is published. `src: Data model, seed table row 7`
- [ ] `C-DM-21` `data` Each published case carries a hero asset plus two ordered bands. `src: Data model, seed data closing paragraph`
- [ ] `C-DM-22` `data` The draft case carries a hero asset stored in the same bucket. `src: Data model, seed data closing paragraph`
- [ ] `C-DM-23` `literal` The seeded published posts are `studio-turns-ten` plus `on-motion-as-argument`. `src: Data model, seed data closing paragraph`
- [ ] `C-DM-24` `literal` The seeded draft post is `the-quiet-rebrand`. `src: Data model, seed data closing paragraph`
- [ ] `C-DM-25` `literal` The seeded open roles are `senior-creative-developer`, `motion-designer`, `producer`. `src: Data model, seed data closing paragraph`
- [ ] `C-DM-26` `data` The enquiry table seeds empty. `src: Data model, seed data closing paragraph`
- [ ] `C-DM-27` `data` The subscriber table seeds empty. `src: Data model, seed data closing paragraph`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The home route reads as one continuous descent rather than a stack of blocks. `src: Front-end specification, the home route`
- [ ] `C-FE-02` `ui` The hero carries a three-line studio statement beneath the display headline. `src: Front-end specification, the hero`
- [ ] `C-FE-03` `ui` The hero carries a social row of four networks. `src: Front-end specification, the hero`
- [ ] `C-FE-04` `ui` The featured band carries seven projects. `src: Front-end specification, the featured band`
- [ ] `C-FE-05` `literal` A featured project carries a caret link reading `Discover`. `src: Front-end specification, the featured band`
- [ ] `C-FE-06` `ui` A case card carries media, a title, a year range, a discipline tag. `src: Front-end specification, the cases index`
- [ ] `C-FE-07` `ui` A pointed-at case card tints with that project accent. `src: Front-end specification, the cases index`
- [ ] `C-FE-08` `ui` The case study page carries previous links plus next links to sibling cases. `src: Front-end specification, the case study`
- [ ] `C-FE-09` `ui` A value statement is numbered with an oversized light numeral. `src: Front-end specification, the values route`
- [ ] `C-FE-10` `ui` A careers row lifts when pointed at. `src: Front-end specification, the careers list`
- [ ] `C-FE-11` `ui` The desk state column reads as a word rather than a colour alone. `src: Front-end specification, the desk`
- [ ] `C-FE-12` `ui` A long title truncates to one line, revealing full text only when truncated. `src: Front-end specification, text and images`
- [ ] `C-FE-13` `constraint` The build ships no image file, video file, font file, three-dimensional model, audio file. `src: Front-end specification, the zero-asset rule`
- [ ] `C-FE-14` `capability` The mascot is composed from primitives. `src: Front-end specification, the zero-asset rule`
- [ ] `C-FE-15` `capability` The ambient bed is generated live from detuned tones. `src: Front-end specification, the zero-asset rule`
- [ ] `C-FE-16` `capability` A photographic slot is a seeded gradient in the owning project accent. `src: Front-end specification, the zero-asset rule`
- [ ] `C-FE-17` `ui` The privacy route carries numbered clauses beneath a last-updated line. `src: Front-end specification, the privacy and terms routes`
- [ ] `C-FE-18` `ui` The terms route carries one primary action back to the home route. `src: Front-end specification, the privacy and terms routes`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product serves a single studio tenant. `src: Constraints, one studio`
- [ ] `C-CN-02` `constraint` The product carries no analytics vendor. `src: Constraints, not built`
- [ ] `C-CN-03` `constraint` The product carries no video hosting surface. `src: Constraints, not built`
- [ ] `C-CN-04` `constraint` The product carries no comments, likes, ratings, follows. `src: Constraints, not built`
- [ ] `C-CN-05` `constraint` The product carries no payments, subscriptions, invoices, commerce surface. `src: Constraints, not built`
- [ ] `C-CN-06` `constraint` The product carries no client portal. `src: Constraints, not built`
- [ ] `C-CN-07` `constraint` The product sends no email. `src: Constraints, not built`
- [ ] `C-CN-08` `constraint` The product carries no scheduled publication. `src: Constraints, not built`
- [ ] `C-CN-09` `constraint` The product carries no revision history. `src: Constraints, not built`
- [ ] `C-CN-10` `constraint` The product carries no search surface. `src: Constraints, not built`
- [ ] `C-CN-11` `constraint` The product carries no third language. `src: Constraints, not built`
- [ ] `C-CN-12` `constraint` The app makes no runtime outbound call beyond PostgreSQL plus MinIO. `src: Constraints, not built`
- [ ] `C-CN-13` `constraint` A card grid renders incrementally rather than all at once past a screenful. `src: Constraints, scale`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `literal` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` A reserved `.browser_screenshots/` directory exists empty at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` A reserved `.downloads/` directory exists empty at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `contract` The app serves a production build rather than a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-11` `constraint` The server process is not a child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-12` `contract` The server binds `0.0.0.0` rather than a loopback address. `src: Deployment contract bullet 9`
- [ ] `C-DC-13` `constraint` The build downloads, installs, compiles, starts no copy of a backing service. `src: Deployment contract bullet 10`
- [ ] `C-DC-14` `constraint` The deployment uses no persistent volume, fixed container name, custom network. `src: Deployment contract bullet 12`
- [ ] `C-DC-15` `contract` Bearer authentication is required on every endpoint outside the named public set. `src: Deployment contract, API shapes closing paragraph`
- [ ] `C-DC-16` `constraint` An in-memory list standing in for stored cases is a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-17` `constraint` A file on the app own disk standing in for the object store is a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-18` `constraint` Image bytes inlined into a template are a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-19` `constraint` A hardcoded success response replacing a bucket write is a contract violation. `src: Deployment contract, no mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | seeded password for every account | C-DM-03 | Data model, password paragraph |
| `access_token` | the bearer token field name | C-CF-02 | Core features, Auth paragraph |
| `POST /api/auth/signup` | signup endpoint | C-CF-01 | Core features, Auth paragraph |
| `POST /api/auth/login` | login endpoint | C-CF-03 | Core features, Auth paragraph |
| `author` | the privileged role name | C-RL-01 | User roles table |
| `reader` | the ordinary role name | C-RL-01 | User roles table |
| `The Studio` | first primary navigation link | C-CF-13 | Core features item 4 |
| `Our Cases` | second primary navigation link | C-CF-13 | Core features item 4 |
| `Careers` | third primary navigation link | C-CF-13 | Core features item 4 |
| `Our Values` | fourth primary navigation link | C-CF-13 | Core features item 4 |
| `Contact` | fifth primary navigation link | C-CF-13 | Core features item 4 |
| `Detroit` | first seeded office | C-CF-14 | Core features item 5 |
| `Rotterdam` | second seeded office | C-CF-14 | Core features item 5 |
| `Lyon` | third seeded office | C-CF-14 | Core features item 5 |
| `hello@northform.co` | studio contact address | C-CF-15 | Core features item 5 |
| `We'd love to hear from you` | footer line above the contact address | C-CF-16 | Core features item 5 |
| `Español` | the Spanish language switch label | C-CF-17 | Core features item 6 |
| `lumenfest` | first seeded published case slug | C-CF-33 | Core features item 9 |
| `cases/{case_slug}/{sha256_of_bytes}.{ext}` | case asset object key scheme | C-CF-45 | Core features item 14 |
| `posts/{post_slug}/{sha256_of_bytes}.{ext}` | post asset object key scheme | C-CF-46 | Core features item 14 |
| `Ooh shit!` | not-found page heading | C-CF-91 | Core features item 31 |
| `You're lost...` | not-found page line | C-CF-92 | Core features item 31 |
| `Back to homepage` | not-found page link label | C-CF-93 | Core features item 31 |
| `GT Sectra Display` | editorial heading family | C-UX-11 | UI/UX notes, typography |
| `Gilroy` | display word family | C-UX-12 | UI/UX notes, typography |
| `Heebo` | interface family | C-UX-13 | UI/UX notes, typography |
| `14px` | body size | C-UX-14 | UI/UX notes, typography |
| `29.4px` | body line height | C-UX-14 | UI/UX notes, typography |
| `120px` | primary display headline size | C-UX-15 | UI/UX notes, typography |
| `107px` | primary display headline line height | C-UX-15 | UI/UX notes, typography |
| `4.5:1` | text contrast floor | C-UX-35 | UI/UX notes, accessibility floors |
| `3:1` | large text contrast floor | C-UX-36 | UI/UX notes, accessibility floors |
| `44px` | touch target floor | C-UX-41 | UI/UX notes, accessibility floors |
| `Toggle menu` | hidden label on the menu control | C-UX-39 | UI/UX notes, accessibility floors |
| `DATABASE_URL` | PostgreSQL connection variable | C-TR-07 | Technical requirements paragraph 1 |
| `STORAGE_ENDPOINT` | object store address variable | C-TR-08 | Technical requirements paragraph 1 |
| `STORAGE_BUCKET` | object store bucket variable | C-TR-08 | Technical requirements paragraph 1 |
| `STORAGE_ACCESS_KEY` | object store access key variable | C-TR-08 | Technical requirements paragraph 1 |
| `STORAGE_SECRET_KEY` | object store secret variable | C-TR-08 | Technical requirements paragraph 1 |
| `APP_PUBLIC_URL` | public address variable | C-TR-09 | Technical requirements paragraph 1 |
| `APP_PUBLIC_PORT` | public port variable | C-TR-10 | Technical requirements paragraph 1 |
| `Web` | first discipline enum member | C-DM-11 | Data model, closed enums |
| `Strategy` | second discipline enum member | C-DM-11 | Data model, closed enums |
| `Design` | third discipline enum member | C-DM-11 | Data model, closed enums |
| `draft` | unpublished state name | C-DM-13 | Data model, closed enums |
| `published` | published state name | C-DM-13 | Data model, closed enums |
| `Northform` | the studio name | C-DM-16 | Data model, seed data |
| `en` | English locale code | C-DM-17 | Data model, seed data |
| `English` | English locale label | C-DM-17 | Data model, seed data |
| `es` | Spanish locale code | C-DM-17 | Data model, seed data |
| `Facebook` | first seeded social network | C-DM-18 | Data model, seed data |
| `Instagram` | second seeded social network | C-DM-18 | Data model, seed data |
| `Dribbble` | third seeded social network | C-DM-18 | Data model, seed data |
| `Twitter` | fourth seeded social network | C-DM-18 | Data model, seed data |
| `harbour-line-rebrand` | the seeded draft case slug | C-DM-19 | Data model, seed table row 8 |
| `grand-opera-of-verdal` | a seeded published case slug | C-DM-20 | Data model, seed table row 7 |
| `studio-turns-ten` | first seeded published post slug | C-DM-23 | Data model, seed data |
| `on-motion-as-argument` | second seeded published post slug | C-DM-23 | Data model, seed data |
| `the-quiet-rebrand` | the seeded draft post slug | C-DM-24 | Data model, seed data |
| `senior-creative-developer` | first seeded open role slug | C-DM-25 | Data model, seed data |
| `motion-designer` | second seeded open role slug | C-DM-25 | Data model, seed data |
| `producer` | third seeded open role slug | C-DM-25 | Data model, seed data |
| `Discover` | featured project caret link label | C-FE-05 | Front-end specification, featured band |
| `${APP_PUBLIC_PORT}:4173` | the port mapping | C-DC-02 | Deployment contract bullet 1 |
| `GET /api/health` | readiness route | C-DC-04 | Deployment contract bullet 3 |
| `200` | readiness status | C-DC-04 | Deployment contract bullet 3 |
| `/app/USER_README.md` | credentials file path | C-DC-06 | Deployment contract bullet 5 |
| `Escape` | the key that closes one overlay level | C-UX-30 | UI/UX notes, components and states |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the nine accent colour families | C-OV-07 | named as families with no per-family literal given |
| the source the environment provides for the showreel | C-CF-87 | referenced by description with no address given |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 9 | 9 |
| User roles | 18 | 21 |
| Core features | 96 | 105 |
| User flow | 14 | 17 |
| UI and UX notes | 38 | 43 |
| Technical requirements | 21 | 25 |
| Data model | 24 | 27 |
| Front-end specification | 14 | 18 |
| Constraints | 11 | 13 |
| Deployment contract | 17 | 19 |

Items exceed sentences in most rows because a single sentence often carries two asks; the
Overview row matches because each of its obligation sentences yielded exactly one item.
