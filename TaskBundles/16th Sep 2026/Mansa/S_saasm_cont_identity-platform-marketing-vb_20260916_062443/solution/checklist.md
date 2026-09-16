# Checklist: Aegis

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 367
Unpinned values flagged: 4

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public marketing site for the Aegis identity platform. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app serves twenty-eight routes described in the brief. `src: Overview para 2`
- [ ] `C-OV-03` `constraint` The app is not a working identity provider. `src: Overview para 3`
- [ ] `C-OV-04` `constraint` The app hides an unpublished entry on its route. `src: Overview para 4`
- [ ] `C-OV-05` `constraint` The app hides an unpublished entry at its rendition address. `src: Overview para 4`
- [ ] `C-OV-06` `constraint` The app hides an unpublished entry's stored image bytes. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` An author creates a library entry. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An author edits a library entry owned by that same author. `src: User roles table row 1`
- [ ] `C-RL-03` `role` An author publishes a library entry owned by that same author. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An author unpublishes a library entry owned by that same author. `src: User roles table row 1`
- [ ] `C-RL-05` `role` An author uploads an image to an entry owned by that same author. `src: User roles table row 1`
- [ ] `C-RL-06` `role` An author reads a draft owned by that same author. `src: User roles table row 1`
- [ ] `C-RL-07` `role` The app denies an author access to another author's entry in any state. `src: User roles table row 1`
- [ ] `C-RL-08` `role` The app denies an author access to another author's draft rendition. `src: User roles table row 1`
- [ ] `C-RL-09` `role` The app denies an author access to another author's draft image. `src: User roles table row 1`
- [ ] `C-RL-10` `role` The app denies an author the ability to provision an application. `src: User roles table row 1`
- [ ] `C-RL-11` `role` A reader signs up without an invitation. `src: User roles table row 2`
- [ ] `C-RL-12` `role` A reader reads every published entry. `src: User roles table row 2`
- [ ] `C-RL-13` `role` A reader provisions applications on that reader's own account. `src: User roles table row 2`
- [ ] `C-RL-14` `role` The app denies a reader access to any draft. `src: User roles table row 2`
- [ ] `C-RL-15` `role` The app denies a reader access to any draft rendition. `src: User roles table row 2`
- [ ] `C-RL-16` `role` The app denies a reader access to any draft image. `src: User roles table row 2`
- [ ] `C-RL-17` `role` The app denies a reader the ability to create a library entry. `src: User roles table row 2`
- [ ] `C-RL-18` `role` The app denies a reader access to another account's applications. `src: User roles table row 2`
- [ ] `C-RL-19` `role` The app rejects a direct API call from a reader session to an author-only endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-20` `role` A rejected authorization attempt leaves the protected state unchanged. `src: User roles, authorization paragraph`
- [ ] `C-RL-21` `constraint` Signup is open to anyone with no approval step. `src: User roles, signup paragraph`
- [ ] `C-RL-22` `constraint` The app refuses to create an author account through the site. `src: User roles, signup paragraph`
- [ ] `C-RL-23` `literal` The app seeds the account `author@example.com` with the role author. `src: User roles, seeded accounts table row 1`
- [ ] `C-RL-24` `literal` The app seeds the account `author2@example.com` with the role author. `src: User roles, seeded accounts table row 2`
- [ ] `C-RL-25` `literal` The app seeds the account `reader@example.com` with the role reader. `src: User roles, seeded accounts table row 3`

## C-CF Core features

- [ ] `C-CF-01` `literal` The password `deku-demo-pw-2026` works at login for every seeded account. `src: Core features, Auth para 1`
- [ ] `C-CF-02` `capability` The app stores a password as a hash. `src: Core features, Auth para 1`
- [ ] `C-CF-03` `capability` A successful sign-in returns a bearer token. `src: Core features, Auth para 1`
- [ ] `C-CF-04` `capability` The client sends the bearer token on every request outside the public read surface. `src: Core features, Auth para 1`
- [ ] `C-CF-05` `ui` An expired token leaves the current page in place. `src: Core features, Auth para 1`
- [ ] `C-CF-06` `ui` An expired token shows an inline banner saying the session ended. `src: Core features, Auth para 1`
- [ ] `C-CF-07` `ui` An expired token preserves the form the visitor was filling. `src: Core features, Auth para 1`
- [ ] `C-CF-08` `literal` `POST /api/auth/sign-up` creates an account with the role reader. `src: Core features, Auth para 2`
- [ ] `C-CF-09` `constraint` The app refuses a signup with an email address already in use. `src: Core features, Auth para 2`
- [ ] `C-CF-10` `constraint` A refused signup creates no account. `src: Core features, Auth para 2`
- [ ] `C-CF-11` `constraint` The app sends no email to any address. `src: Core features, Auth para 2`
- [ ] `C-CF-12` `data` A library entry carries a kind of doc, changelog, glossary, blog or legal. `src: Core features, library para 1`
- [ ] `C-CF-13` `data` A library entry carries a state of draft or published. `src: Core features, library para 1`
- [ ] `C-CF-14` `capability` An author creates an entry in the draft state. `src: Core features rule 1`
- [ ] `C-CF-15` `constraint` The app denies an anonymous visitor a draft entry's public route. `src: Core features rule 1`
- [ ] `C-CF-16` `constraint` The app denies a reader a draft entry's public route. `src: Core features rule 1`
- [ ] `C-CF-17` `constraint` The app denies a second author a draft entry's public route. `src: Core features rule 1`
- [ ] `C-CF-18` `constraint` A refusal for a draft entry does not disclose the entry. `src: Core features rule 1`
- [ ] `C-CF-19` `capability` Publishing an entry makes the entry readable at its route. `src: Core features rule 2`
- [ ] `C-CF-20` `capability` Publishing an entry writes the plain-text rendition in the same operation. `src: Core features rule 2`
- [ ] `C-CF-21` `data` Publishing an entry stamps `published_at`. `src: Core features rule 2`
- [ ] `C-CF-22` `capability` Unpublishing an entry stops the route serving the entry. `src: Core features rule 2`
- [ ] `C-CF-23` `capability` Unpublishing an entry stops the rendition address serving the entry. `src: Core features rule 2`
- [ ] `C-CF-24` `capability` Unpublishing an entry stops the images of that entry being readable. `src: Core features rule 2`
- [ ] `C-CF-25` `constraint` At most one published entry holds a given kind with a given slug. `src: Core features rule 3`
- [ ] `C-CF-26` `constraint` Two simultaneous publishes for one kind with one slug do not both succeed. `src: Core features rule 3`
- [ ] `C-CF-27` `constraint` A rejected publish leaves no orphan rendition row. `src: Core features rule 3`
- [ ] `C-CF-28` `constraint` A rejected publish leaves no entry stranded between states. `src: Core features rule 3`
- [ ] `C-CF-29` `constraint` A rendition exists for no entry in the draft state. `src: Core features rule 4`
- [ ] `C-CF-30` `capability` The rendition body derives from the entry body in the publishing operation. `src: Core features rule 4`
- [ ] `C-CF-31` `capability` A documentation entry with no sample for the selected SDK shows an explicit note. `src: Core features rule 5`
- [ ] `C-CF-32` `constraint` The app never shows a different framework's code sample in place of the selected one. `src: Core features rule 5`
- [ ] `C-CF-33` `literal` An entry image is stored in the bucket named by `STORAGE_BUCKET`. `src: Core features, images para 1`
- [ ] `C-CF-34` `literal` An object key matches `library/{entry_id}/{sha256_of_bytes}.{ext}`. `src: Core features rule 6`
- [ ] `C-CF-35` `data` An upload records the object key with the content type. `src: Core features rule 6`
- [ ] `C-CF-36` `data` An upload records the byte size with the alternative text. `src: Core features rule 6`
- [ ] `C-CF-37` `constraint` The app stores no image bytes on the container filesystem. `src: Core features rule 6`
- [ ] `C-CF-38` `constraint` The app stores no image bytes in a database column. `src: Core features rule 6`
- [ ] `C-CF-39` `literal` `/api/entries/{entry_id}/assets/{asset_id}/content` streams image bytes from the bucket. `src: Core features rule 7`
- [ ] `C-CF-40` `constraint` The bucket is never made publicly readable. `src: Core features rule 7`
- [ ] `C-CF-41` `constraint` The app issues no time-limited link to a stored object. `src: Core features rule 7`
- [ ] `C-CF-42` `constraint` Uploading identical bytes twice to one entry creates no second object. `src: Core features rule 8`
- [ ] `C-CF-43` `constraint` Uploading identical bytes twice to one entry creates no second asset record. `src: Core features rule 8`
- [ ] `C-CF-44` `ui` The documentation portal replaces the global chrome with a dense tool bar. `src: Core features, portal para 1`
- [ ] `C-CF-45` `literal` The version select offers `Core 3`, `Core 2`, `Core 1`. `src: Core features, portal para 1`
- [ ] `C-CF-46` `ui` The SDK selector sits at the top of the sidebar in a labelled well. `src: Core features rule 9`
- [ ] `C-CF-47` `literal` The SDK selector carries thirty options in the order the brief gives. `src: Core features rule 9`
- [ ] `C-CF-48` `literal` The SDK selector defaults to `Next.js`. `src: Core features rule 9`
- [ ] `C-CF-49` `capability` Changing the SDK rewrites every code sample without reloading the page. `src: Core features rule 10`
- [ ] `C-CF-50` `capability` Changing the SDK preserves the scroll position. `src: Core features rule 10`
- [ ] `C-CF-51` `capability` The SDK choice survives navigation to another documentation route. `src: Core features rule 10`
- [ ] `C-CF-52` `capability` The SDK choice survives a return visit. `src: Core features rule 10`
- [ ] `C-CF-53` `literal` The document element carries `data-sdk` set to the selected option. `src: Core features rule 10`
- [ ] `C-CF-54` `literal` Selecting Ruby sets `data-sdk` to `ruby-rails-sinatra`. `src: Core features rule 10`
- [ ] `C-CF-55` `ui` The sidebar carries the two mode rows Guides with Reference. `src: Core features rule 11`
- [ ] `C-CF-56` `literal` The sidebar tree carries the fourteen top-level nodes in the order the brief gives. `src: Core features rule 11`
- [ ] `C-CF-57` `ui` The sidebar exposes each branch expansion state to assistive technology. `src: Core features rule 11`
- [ ] `C-CF-58` `capability` Search ranks an exact symbol name above a related passage. `src: Core features rule 12`
- [ ] `C-CF-59` `capability` Search restricts results to the reader's SDK selection by default. `src: Core features rule 12`
- [ ] `C-CF-60` `ui` Search offers a visible control to widen beyond the current selection. `src: Core features rule 12`
- [ ] `C-CF-61` `ui` A search with no results shows a plain sentence with the Ask AI action. `src: Core features rule 12`
- [ ] `C-CF-62` `capability` The pricing route renders from a single plan document. `src: Core features, pricing para 1`
- [ ] `C-CF-63` `literal` The four plan cards appear in the order Hobby, Pro, Business, Enterprise. `src: Core features rule 13`
- [ ] `C-CF-64` `literal` The Pro card shows the price `$20`. `src: Core features rule 13`
- [ ] `C-CF-65` `literal` The Business card shows the price `$250`. `src: Core features rule 13`
- [ ] `C-CF-66` `literal` Each plan card carries `data-plan` set to its own code. `src: Core features rule 13`
- [ ] `C-CF-67` `constraint` Only the Hobby card carries a filled action. `src: Core features rule 13`
- [ ] `C-CF-68` `capability` The billing toggle recomputes the displayed price. `src: Core features rule 14`
- [ ] `C-CF-69` `literal` The pricing page carries `data-billing-period` set to `monthly` or `annual`. `src: Core features rule 14`
- [ ] `C-CF-70` `ui` The price digits roll rather than the whole number being replaced. `src: Core features rule 14`
- [ ] `C-CF-71` `literal` The matrix shows `1,000 Included per month` for API key creations. `src: Core features rule 15`
- [ ] `C-CF-72` `literal` The matrix shows `$0.00001 each` for API key verifications past the allowance. `src: Core features rule 15`
- [ ] `C-CF-73` `capability` The Hobby column shows a combined summary in place of a ladder. `src: Core features rule 15`
- [ ] `C-CF-74` `ui` MRU renders as a button rather than as text. `src: Core features rule 16`
- [ ] `C-CF-75` `ui` MRO renders as a button rather than as text. `src: Core features rule 16`
- [ ] `C-CF-76` `capability` Pressing MRU discloses the monthly retained user definition. `src: Core features rule 16`
- [ ] `C-CF-77` `literal` The free allowance is `50,000` monthly retained users per application. `src: Core features rule 16`
- [ ] `C-CF-78` `literal` The Pro list quotes `Additional $0.02/mo each` beneath the included allowance. `src: Core features rule 17`
- [ ] `C-CF-79` `ui` The matrix header row sticks beneath the chrome on a fully opaque ground. `src: Core features rule 17`
- [ ] `C-CF-80` `capability` The changelog presents entries newest first. `src: Core features rule 18`
- [ ] `C-CF-81` `ui` The newest changelog dot carries the accent. `src: Core features rule 18`
- [ ] `C-CF-82` `literal` The seeded changelog entry `Custom OAuth scopes` is dated `Aug 21`. `src: Core features rule 18`
- [ ] `C-CF-83` `capability` The copy-link control copies the entry permalink. `src: Core features rule 19`
- [ ] `C-CF-84` `literal` The copy-link control swaps its label to `Copied!` in place. `src: Core features rule 19`
- [ ] `C-CF-85` `ui` The copy-link confirmation does not resize the row. `src: Core features rule 19`
- [ ] `C-CF-86` `ui` The alphabet rail sticks beneath the chrome. `src: Core features rule 20`
- [ ] `C-CF-87` `literal` The letters `K`, `Q`, `X`, `Y` render inert on the alphabet rail. `src: Core features rule 20`
- [ ] `C-CF-88` `constraint` An inert alphabet letter is not focusable. `src: Core features rule 20`
- [ ] `C-CF-89` `literal` Each rail cell carries `data-letter-state` set to `active` or `inert`. `src: Core features rule 20`
- [ ] `C-CF-90` `capability` The build derives the related-term graph from the terms each entry declares. `src: Core features rule 21`
- [ ] `C-CF-91` `constraint` The build refuses to finish when a related-term target does not exist. `src: Core features rule 21`
- [ ] `C-CF-92` `constraint` The build refuses to finish when an entry links only to itself. `src: Core features rule 21`
- [ ] `C-CF-93` `capability` The build reports an orphan entry nothing links to. `src: Core features rule 21`
- [ ] `C-CF-94` `literal` The blog index carries the category filter row the brief quotes. `src: Core features rule 22`
- [ ] `C-CF-95` `literal` The seeded article `Adding Aegis auth to your CLI` is dated `Jun 4, 2026`. `src: Core features rule 22`
- [ ] `C-CF-96` `literal` Every published entry has a rendition at `/r/{kind}/{slug}.txt`. `src: Core features rule 23`
- [ ] `C-CF-97` `data` A rendition carries the title with the canonical address. `src: Core features rule 23`
- [ ] `C-CF-98` `data` A rendition carries the last-updated date with the body. `src: Core features rule 23`
- [ ] `C-CF-99` `literal` The app publishes an index of every rendition at `/r/index.txt`. `src: Core features rule 23`
- [ ] `C-CF-100` `constraint` An Open in link carries the rendition address rather than the contents. `src: Core features rule 23`
- [ ] `C-CF-101` `capability` The changelog publishes a feed linked from its own route. `src: Core features rule 24`
- [ ] `C-CF-102` `capability` The blog publishes a feed linked from its own route. `src: Core features rule 24`
- [ ] `C-CF-103` `constraint` A feed carries full content rather than an excerpt. `src: Core features rule 24`
- [ ] `C-CF-104` `constraint` A feed entry keeps a stable identifier across an edit. `src: Core features rule 24`
- [ ] `C-CF-105` `capability` The legal index splits documents under Customers with Everyone else. `src: Core features rule 25`
- [ ] `C-CF-106` `literal` The leaderboard header carries the nine task columns in the order the brief gives. `src: Core features rule 26`
- [ ] `C-CF-107` `literal` A leaderboard cell carries `data-cell-band` set to one of four values. `src: Core features rule 27`
- [ ] `C-CF-108` `constraint` A cell with no result renders as an absence rather than a zero. `src: Core features rule 27`
- [ ] `C-CF-109` `constraint` The matrix is a table with header associations. `src: Core features rule 27`
- [ ] `C-CF-110` `literal` The framework select defaults to `Next.js`. `src: Core features rule 28`
- [ ] `C-CF-111` `literal` The mode toggle offers Base, MCP, Skills. `src: Core features rule 28`
- [ ] `C-CF-112` `data` Every published cell names the model version with the harness version. `src: Core features rule 29`
- [ ] `C-CF-113` `data` Every published cell names the corpus version with the run date. `src: Core features rule 29`
- [ ] `C-CF-114` `data` Every published cell states the number of runs averaged. `src: Core features rule 29`
- [ ] `C-CF-115` `capability` Switching framework selects a different subset of the corpus. `src: Core features rule 29`
- [ ] `C-CF-116` `constraint` The theme editor route never scrolls the document. `src: Core features rule 30`
- [ ] `C-CF-117` `capability` The canvas pans by drag. `src: Core features rule 30`
- [ ] `C-CF-118` `capability` The canvas zooms by modifier plus scroll. `src: Core features rule 30`
- [ ] `C-CF-119` `constraint` Canvas type stays sharp at every zoom level. `src: Core features rule 30`
- [ ] `C-CF-120` `capability` The canvas position survives a component selection change. `src: Core features rule 30`
- [ ] `C-CF-121` `literal` A theme carries seventeen values with the mode. `src: Core features rule 31`
- [ ] `C-CF-122` `literal` The five primary fields appear in the order the brief gives. `src: Core features rule 31`
- [ ] `C-CF-123` `capability` The Advanced disclosure reveals twelve further fields. `src: Core features rule 31`
- [ ] `C-CF-124` `capability` Foreground derives from Background until a value is entered. `src: Core features rule 31`
- [ ] `C-CF-125` `ui` The Foreground field renders disabled at the default theme. `src: Core features rule 31`
- [ ] `C-CF-126` `capability` Derivation happens in a perceptual colour space. `src: Core features rule 32`
- [ ] `C-CF-127` `capability` A foreground failing its contrast floor produces a warning in the editor. `src: Core features rule 32`
- [ ] `C-CF-128` `capability` A foreground failing its contrast floor is clamped when the component renders. `src: Core features rule 32`
- [ ] `C-CF-129` `constraint` The same seventeen inputs always produce the same compiled output. `src: Core features rule 32`
- [ ] `C-CF-130` `capability` Copy URL encodes the whole theme into the address fragment. `src: Core features rule 33`
- [ ] `C-CF-131` `constraint` Sharing a theme link stores nothing on the server. `src: Core features rule 33`
- [ ] `C-CF-132` `data` The theme encoding carries a version in its first character. `src: Core features rule 33`
- [ ] `C-CF-133` `capability` A malformed theme string falls back to the Default preset silently. `src: Core features rule 33`
- [ ] `C-CF-134` `literal` The app ships the four presets `Default`, `Dark`, `Simple`, `Library`. `src: Core features rule 33`
- [ ] `C-CF-135` `constraint` A theme compiles to a fixed set of named values. `src: Core features rule 34`
- [ ] `C-CF-136` `constraint` A theme never compiles to arbitrary style text. `src: Core features rule 34`
- [ ] `C-CF-137` `literal` The canvas carries `data-theme-mode` set to `light` or `dark`. `src: Core features rule 35`
- [ ] `C-CF-138` `ui` The first-run card carries the welcome copy above one dismissing action. `src: Core features rule 35`
- [ ] `C-CF-139` `capability` A signed-in reader creates an application by name. `src: Core features rule 36`
- [ ] `C-CF-140` `capability` Creating an application also creates its development instance. `src: Core features rule 36`
- [ ] `C-CF-141` `constraint` An instance never reaches live without passing through provisioning. `src: Core features rule 36`
- [ ] `C-CF-142` `literal` An instance row carries `data-instance-state` set to the current state. `src: Core features rule 36`
- [ ] `C-CF-143` `constraint` An instance state survives a restart of the app. `src: Core features rule 36`
- [ ] `C-CF-144` `data` Each instance carries a publishable key unique across the product. `src: Core features rule 37`
- [ ] `C-CF-145` `capability` The publishable key is shown once the instance is live. `src: Core features rule 37`
- [ ] `C-CF-146` `constraint` A development instance shares no users with a production instance. `src: Core features rule 37`
- [ ] `C-CF-147` `literal` `GET /api/applications` returns only the caller's own applications. `src: Core features rule 38`
- [ ] `C-CF-148` `constraint` The app refuses a request for another account's instance by id. `src: Core features rule 38`
- [ ] `C-CF-149` `literal` A privacy page is reachable from the footer of every route at `/legal/privacy`. `src: Core features rule 39`
- [ ] `C-CF-150` `capability` The privacy page states what the site records about a visitor. `src: Core features rule 39`
- [ ] `C-CF-151` `capability` The privacy page states how long a visitor record is kept. `src: Core features rule 39`
- [ ] `C-CF-152` `literal` The privacy page names `privacy@aegis.dev` for a removal request. `src: Core features rule 39`
- [ ] `C-CF-153` `capability` A first-time visitor is asked once about non-essential cookies. `src: Core features rule 40`
- [ ] `C-CF-154` `capability` The cookie answer survives a reload. `src: Core features rule 40`
- [ ] `C-CF-155` `capability` Withdrawing cookie consent is as easy as granting consent. `src: Core features rule 40`
- [ ] `C-CF-156` `ui` The cookie control is reachable from every route by keyboard alone. `src: Core features rule 40`
- [ ] `C-CF-157` `literal` The document element carries `data-consent` set to one of three values. `src: Core features rule 40`
- [ ] `C-CF-158` `constraint` Analytics loads only after the cookie answer is granted. `src: Core features rule 40`
- [ ] `C-CF-159` `capability` Every public route carries its own title. `src: Core features rule 41`
- [ ] `C-CF-160` `capability` Every public route carries its own meta description. `src: Core features rule 41`
- [ ] `C-CF-161` `constraint` No two public routes share a title. `src: Core features rule 41`
- [ ] `C-CF-162` `constraint` No two public routes share a description. `src: Core features rule 41`
- [ ] `C-CF-163` `capability` The site serves a favicon declared in the document head. `src: Core features rule 42`
- [ ] `C-CF-164` `constraint` The favicon is generated from the brand mark geometry. `src: Core features rule 42`
- [ ] `C-CF-165` `capability` The application form refuses a submission with the decoy field filled. `src: Core features rule 43`
- [ ] `C-CF-166` `capability` The application form refuses repeated submissions from one caller in quick succession. `src: Core features rule 43`
- [ ] `C-CF-167` `constraint` A refused application stores no company name. `src: Core features rule 43`
- [ ] `C-CF-168` `ui` A refused application shows an inline banner naming the reason. `src: Core features rule 43`
- [ ] `C-CF-169` `capability` An unknown address renders the site's own not-found page. `src: Core features rule 44`
- [ ] `C-CF-170` `capability` An unknown address answers with a not-found response. `src: Core features rule 44`
- [ ] `C-CF-171` `literal` The not-found page shows the line `Sorry, we can't find the page you're looking for.` `src: Core features rule 44`
- [ ] `C-CF-172` `literal` The not-found page offers the single action `Go to homepage`. `src: Core features rule 44`
- [ ] `C-CF-173` `constraint` The not-found page keeps the global chrome. `src: Core features rule 44`
- [ ] `C-CF-174` `constraint` The not-found page drops the announcement bar. `src: Core features rule 44`

## C-UF User flow

- [ ] `C-UF-01` `capability` The app serves every route named in the User flow route table. `src: User flow, routes table`
- [ ] `C-UF-02` `contract` `/discord` redirects off origin to a community service. `src: User flow, routes table row 28`
- [ ] `C-UF-03` `capability` An anonymous visitor reaching `/dashboard` is redirected to `/sign-in`. `src: User flow, entry para 1`
- [ ] `C-UF-04` `capability` An anonymous visitor reaching `/studio/library` is redirected to `/sign-in`. `src: User flow, entry para 1`
- [ ] `C-UF-05` `capability` The app remembers the intended address across a sign-in redirect. `src: User flow, entry para 1`
- [ ] `C-UF-06` `capability` Signing in sends a reader to `/dashboard`. `src: User flow, entry para 1`
- [ ] `C-UF-07` `capability` Signing in sends an author to `/studio/library`. `src: User flow, entry para 1`
- [ ] `C-UF-08` `capability` Signing out returns the visitor to `/`. `src: User flow, entry para 1`
- [ ] `C-UF-09` `role` A reader reaching `/studio/library` is shown the reader dashboard instead. `src: User flow, entry para 1`
- [ ] `C-UF-10` `ui` The studio library is a table of every entry the author owns. `src: User flow, journey 2`
- [ ] `C-UF-11` `literal` A studio row carries `data-entry-state` set to `draft` or `published`. `src: User flow, journey 2`
- [ ] `C-UF-12` `ui` Publishing an entry shows an inline banner confirming the change in place. `src: User flow, journey 2`
- [ ] `C-UF-13` `ui` Every list carries an empty state. `src: User flow, states para 1`
- [ ] `C-UF-14` `ui` Every page carries a loading state. `src: User flow, states para 1`
- [ ] `C-UF-15` `literal` The careers empty state shows `We don't have any open positions at the moment.` `src: User flow, states para 1`
- [ ] `C-UF-16` `capability` The careers empty state keeps the standing invitation directly above. `src: User flow, states para 1`
- [ ] `C-UF-17` `ui` A leaderboard filter yielding nothing keeps the matrix header. `src: User flow, states para 1`
- [ ] `C-UF-18` `ui` A failed request leaves an inline banner with the page still usable. `src: User flow, states para 1`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The page ground is a near-white neutral on a light band. `src: UI/UX notes, ground para 1`
- [ ] `C-UX-02` `ui` The page ground is a near-black neutral on a dark band. `src: UI/UX notes, ground para 1`
- [ ] `C-UX-03` `ui` A raised surface stays visibly separate from the ground without a shadow. `src: UI/UX notes, ground para 1`
- [ ] `C-UX-04` `ui` The hairline is the most-used colour in the product. `src: UI/UX notes, ground para 1`
- [ ] `C-UX-05` `ui` The accent brand step is the primary action ground. `src: UI/UX notes, accent para 1`
- [ ] `C-UX-06` `constraint` The accent is the only saturated colour in the chrome of a marketing route. `src: UI/UX notes, accent para 1`
- [ ] `C-UX-07` `constraint` A state that is none of the three signals borrows no signal colour. `src: UI/UX notes, signal para 1`
- [ ] `C-UX-08` `ui` The display family carries a genuine `450` step above the regular step. `src: UI/UX notes, type para 1`
- [ ] `C-UX-09` `constraint` The `450` step is never rounded to 400 or 500. `src: UI/UX notes, type para 1`
- [ ] `C-UX-10` `ui` Numerals are tabular lining figures on a single advance width. `src: UI/UX notes, type para 1`
- [ ] `C-UX-11` `constraint` Every shadow begins with a hairline ring before any blur. `src: UI/UX notes, shape para 1`
- [ ] `C-UX-12` `ui` Motion character is eased across the whole product. `src: UI/UX notes, motion para 1`
- [ ] `C-UX-13` `ui` A control answers the pointer faster than the same control settles back. `src: UI/UX notes, motion para 1`
- [ ] `C-UX-14` `constraint` No text moves on scroll. `src: UI/UX notes, motion para 1`
- [ ] `C-UX-15` `ui` A headline arrives one character at a time on the two routes that use the reveal. `src: UI/UX notes, motion para 1`
- [ ] `C-UX-16` `ui` Three hero rings are offset so exactly one is at peak at any moment. `src: UI/UX notes, motion para 1`
- [ ] `C-UX-17` `ui` A reduced-motion preference removes each element transition. `src: UI/UX notes, motion para 1`
- [ ] `C-UX-18` `constraint` A reduced-motion preference hides no content. `src: UI/UX notes, motion para 1`
- [ ] `C-UX-19` `literal` Every band carries `data-band` set to `light` or `dark`. `src: UI/UX notes, bands para 1`
- [ ] `C-UX-20` `constraint` The site offers no site-wide light or dark preference control. `src: UI/UX notes, bands para 1`
- [ ] `C-UX-21` `ui` Every light to dark boundary carries a notch drawn on both sides. `src: UI/UX notes, bands para 1`
- [ ] `C-UX-22` `ui` Every hover treatment is guarded by a hover-capable pointer condition. `src: UI/UX notes, responsive para 1`
- [ ] `C-UX-23` `constraint` The document never scrolls sideways at any viewport. `src: UI/UX notes, responsive para 1`
- [ ] `C-UX-24` `constraint` Body text meets a contrast ratio of `4.5 to 1` against its ground. `src: UI/UX notes, accessibility para 1`
- [ ] `C-UX-25` `constraint` A focus ring is visible at `3 to 1` against both adjacent colours. `src: UI/UX notes, accessibility para 1`
- [ ] `C-UX-26` `constraint` No positive tab index appears anywhere. `src: UI/UX notes, accessibility para 1`
- [ ] `C-UX-27` `constraint` Meaning is never carried by colour alone. `src: UI/UX notes, accessibility para 1`
- [ ] `C-UX-28` `constraint` Every content image carries alternative text. `src: UI/UX notes, accessibility para 1`
- [ ] `C-UX-29` `ui` Per-character animated text carries one clean screen-reader copy. `src: UI/UX notes, accessibility para 1`
- [ ] `C-UX-30` `literal` The skip link reading `Skip to main content` is the first focusable element. `src: UI/UX notes, accessibility para 1`
- [ ] `C-UX-31` `ui` Forced colours resolve every structural hairline to a system border colour. `src: UI/UX notes, accessibility para 1`
- [ ] `C-UX-32` `ui` Forced colours hide the dot-matrix ornaments. `src: UI/UX notes, accessibility para 1`

## C-TR Technical requirements

- [ ] `C-TR-01` `literal` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements para 1`
- [ ] `C-TR-02` `constraint` Every route outside the two applications is complete in the served HTML. `src: Technical requirements, browser para`
- [ ] `C-TR-03` `constraint` A route transition does not repaint the chrome. `src: Technical requirements, browser para`
- [ ] `C-TR-04` `capability` The chrome action pair resolves after first paint. `src: Technical requirements, regions para`
- [ ] `C-TR-05` `capability` The startup application card resolves after first paint. `src: Technical requirements, regions para`
- [ ] `C-TR-06` `constraint` The theme draft lives in the address rather than in storage. `src: Technical requirements, state para`
- [ ] `C-TR-07` `constraint` Nothing that changes page shape is driven from scroll. `src: Technical requirements, caricatures para`
- [ ] `C-TR-08` `constraint` A caricature outside the visible region stops animating. `src: Technical requirements, caricatures para`
- [ ] `C-TR-09` `constraint` Only transform, opacity, filter or clip-path are animated. `src: Technical requirements, performance para`
- [ ] `C-TR-10` `constraint` The layered blur behind the chrome exists exactly once. `src: Technical requirements, performance para`
- [ ] `C-TR-11` `constraint` Content outside the visible region of a long document is skipped during paint. `src: Technical requirements, performance para`
- [ ] `C-TR-12` `constraint` Skipped content in a long document stays findable by in-page search. `src: Technical requirements, performance para`
- [ ] `C-TR-13` `constraint` The build ships no binary asset of any kind. `src: Technical requirements, assets para`
- [ ] `C-TR-14` `capability` The circuit field is generated from a seed fixed per route. `src: Technical requirements, assets para`
- [ ] `C-TR-15` `constraint` Product screenshots are built as markup rather than generated as images. `src: Technical requirements, assets para`
- [ ] `C-TR-16` `constraint` Every third-party mark resembles no real trademark. `src: Technical requirements, assets para`
- [ ] `C-TR-17` `constraint` Every account-owned row carries the owning account identifier. `src: Technical requirements, scoping para`

## C-DM Data model

- [ ] `C-DM-01` `data` Every timestamp is stored in UTC. `src: Data model para 1`
- [ ] `C-DM-02` `literal` `app_user.email` is unique across the product. `src: Data model, app_user`
- [ ] `C-DM-03` `data` `app_user.role` holds author or reader. `src: Data model, app_user`
- [ ] `C-DM-04` `data` `library_entry.published_at` is null until publication. `src: Data model, library_entry`
- [ ] `C-DM-05` `data` `library_entry.doc_version` holds one of the three documentation versions. `src: Data model, library_entry`
- [ ] `C-DM-06` `literal` `entry_asset.object_key` is unique across the product. `src: Data model, entry_asset`
- [ ] `C-DM-07` `data` `entry_rendition.entry_id` is unique. `src: Data model, entry_rendition`
- [ ] `C-DM-08` `data` `related_term` uses the entry pair as its key. `src: Data model, related_term`
- [ ] `C-DM-09` `constraint` No `related_term` row links an entry to itself. `src: Data model, related_term`
- [ ] `C-DM-10` `data` `plan.monthly_price_minor` is null for the custom tier. `src: Data model, plan`
- [ ] `C-DM-11` `data` The plan cards read the three plan tables rather than any other source. `src: Data model, plan`
- [ ] `C-DM-12` `data` At most one `leaderboard_result` row exists per model, framework, mode, family. `src: Data model, leaderboard_result`
- [ ] `C-DM-13` `constraint` A null `score_percent` is never stored as a zero. `src: Data model, leaderboard_result`
- [ ] `C-DM-14` `data` `theme` carries seventeen colour columns with a mode. `src: Data model, theme`
- [ ] `C-DM-15` `data` `application.slug` is unique within an owner. `src: Data model, application`
- [ ] `C-DM-16` `data` `app_instance.publishable_key` is unique across the product. `src: Data model, app_instance`
- [ ] `C-DM-17` `constraint` A `startup_application` row in the refused state stores no company name. `src: Data model, startup_application`
- [ ] `C-DM-18` `data` `consent_choice` holds one row per visitor token. `src: Data model, consent_choice`
- [ ] `C-DM-19` `literal` `compliance_row.status` holds `Held`, `Not applicable` or `Not offered`. `src: Data model, compliance_row`
- [ ] `C-DM-20` `literal` The seed creates the account `author@example.com` for Ada Renn. `src: Data model, seed para 1`
- [ ] `C-DM-21` `literal` The seed creates ten glossary entries carrying `41` related-term declarations. `src: Data model, seed para 1`
- [ ] `C-DM-22` `literal` The seed creates the draft `Rotating a signing key without downtime` for the second author. `src: Data model, seed para 1`
- [ ] `C-DM-23` `literal` The seed gives one published entry with one draft the slug `session-management`. `src: Data model, seed para 1`
- [ ] `C-DM-24` `literal` The seed creates six compliance rows the brief quotes. `src: Data model, seed para 2`
- [ ] `C-DM-25` `constraint` The seed keeps the two negative compliance rows. `src: Data model, seed para 2`
- [ ] `C-DM-26` `data` The seed includes one leaderboard cell with no result. `src: Data model, seed para 2`
- [ ] `C-DM-27` `constraint` Restarting the app duplicates no seeded row. `src: Data model, seed para 3`
- [ ] `C-DM-28` `literal` `/app/USER_README.md` carries the password `deku-demo-pw-2026` beside each account. `src: Data model, password paragraph`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The header pill is sticky from the top of the scroll. `src: Front-end specification, chrome para 2`
- [ ] `C-FE-02` `ui` The second-level rail appears on the five routes the brief names. `src: Front-end specification, chrome para 5`
- [ ] `C-FE-03` `ui` The active rail item uses a filled glyph with display ink. `src: Front-end specification, chrome para 5`
- [ ] `C-FE-04` `literal` The footer carries the five columns the brief names. `src: Front-end specification, footer table`
- [ ] `C-FE-05` `ui` The persistent help control is fixed at the bottom right of every route. `src: Front-end specification, footer para`
- [ ] `C-FE-06` `literal` The type scale carries thirteen named steps. `src: Front-end specification, type scale table`
- [ ] `C-FE-07` `ui` The brand mark draws its upper crescent at half the strength of the lower. `src: Front-end specification, iconography para 2`
- [ ] `C-FE-08` `ui` The copy control cross-fades two icons in one cell without movement. `src: Front-end specification, iconography para 4`
- [ ] `C-FE-09` `ui` The dashed rule is a repeating tile with both ends faded out. `src: Front-end specification, dashed rule para`
- [ ] `C-FE-10` `ui` Inline code renders as a top rule with a bottom rule plus two end caps. `src: Front-end specification, dashed rule para 2`
- [ ] `C-FE-11` `ui` Inline code survives being split across a line break. `src: Front-end specification, dashed rule para 2`
- [ ] `C-FE-12` `ui` The code theme carries one syntax palette per band. `src: Front-end specification, code theme para`
- [ ] `C-FE-13` `ui` The circuit field is drawn as a grid with traces plus nodes. `src: Front-end specification, field para 1`
- [ ] `C-FE-14` `ui` The arrow link sends one triangle out as a second arrives from the left. `src: Front-end specification, components, arrow link`
- [ ] `C-FE-15` `ui` A feature tile grows taller rather than cropping a tall diagram. `src: Front-end specification, components, feature tile`
- [ ] `C-FE-16` `constraint` The agent prompt pill string is duplicated as screen-reader-only text. `src: Front-end specification, components, agent pill`
- [ ] `C-FE-17` `constraint` The home route runs seven bands with four notched boundaries. `src: Front-end specification, home para 1`
- [ ] `C-FE-18` `literal` The home hero headline reads `More than authentication, Complete User Management`. `src: Front-end specification, home para 2`
- [ ] `C-FE-19` `literal` The trust strip caption reads `Trusted by fast-growing companies around the world.` `src: Front-end specification, home para 3`
- [ ] `C-FE-20` `ui` The typing sign-up card is the only continuously running animation on its route. `src: Front-end specification, user authentication para 4`
- [ ] `C-FE-21` `ui` The commerce demonstration keeps one frame size across its three states. `src: Front-end specification, billing para 3`
- [ ] `C-FE-22` `ui` The three framework routes open dark through the hero. `src: Front-end specification, framework para 1`
- [ ] `C-FE-23` `ui` The dot-matrix ornament is generated from the mark outline at build time. `src: Front-end specification, framework para 1`
- [ ] `C-FE-24` `ui` The command line route drops the marketing chrome for a bare row. `src: Front-end specification, cli para 1`
- [ ] `C-FE-25` `ui` The command reference lists the six commands the brief names. `src: Front-end specification, cli command table`
- [ ] `C-FE-26` `literal` The pricing hero headline reads `Plans for every stage`. `src: Front-end specification, pricing para 1`
- [ ] `C-FE-27` `ui` The documentation shell runs three columns at desktop width. `src: Front-end specification, docs para 1`
- [ ] `C-FE-28` `ui` Leaderboard rows are separated by the dashed rule. `src: Front-end specification, leaderboard para 2`
- [ ] `C-FE-29` `ui` Every theme editor colour field accepts a typed value. `src: Front-end specification, theme editor para 2`
- [ ] `C-FE-30` `ui` The theme editor panel becomes a sheet from the bottom edge at phone width. `src: Front-end specification, theme editor para 3`
- [ ] `C-FE-31` `ui` The compliance table keeps the two rows Aegis does not hold. `src: Front-end specification, security para`
- [ ] `C-FE-32` `constraint` The contact route carries no form. `src: Front-end specification, contact para`
- [ ] `C-FE-33` `ui` The brand assets route shows fourteen asset cells. `src: Front-end specification, brand assets para`
- [ ] `C-FE-34` `capability` Each brand asset cell offers a vector download with a raster download. `src: Front-end specification, brand assets para`
- [ ] `C-FE-35` `ui` Each legal document carries a sticky table of contents at desktop width. `src: Front-end specification, legal para`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The site holds one library with one plan document. `src: Constraints para 1`
- [ ] `C-CN-02` `constraint` The app mints no token. `src: Constraints para 2`
- [ ] `C-CN-03` `constraint` The app brokers no enterprise connection. `src: Constraints para 2`
- [ ] `C-CN-04` `constraint` The app charges no card. `src: Constraints para 2`
- [ ] `C-CN-05` `constraint` The signed-in console is not built. `src: Constraints para 2`
- [ ] `C-CN-06` `constraint` Outbound webhooks are not implemented. `src: Constraints para 2`
- [ ] `C-CN-07` `constraint` Organizations are described rather than implemented. `src: Constraints para 2`
- [ ] `C-CN-08` `constraint` The generated-answer surface behind Ask AI is not built. `src: Constraints para 2`
- [ ] `C-CN-09` `constraint` No mail service is available to the app. `src: Constraints para 3`
- [ ] `C-CN-10` `constraint` No payments provider is available to the app. `src: Constraints para 3`
- [ ] `C-CN-11` `constraint` No native application is shipped. `src: Constraints para 3`
- [ ] `C-CN-12` `constraint` The two brand renderings are labelled as reconstructions. `src: Constraints para 4`
- [ ] `C-CN-13` `constraint` The three light-band code inks are labelled as proposals. `src: Constraints para 4`
- [ ] `C-CN-14` `constraint` The site stays responsive with the glossary at tens of screens of content. `src: Constraints para 5`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-05` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-06` `contract` The directories `.browser_screenshots/` with `.downloads/` exist at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-07` `contract` The app serves a production build behind a static or preview server. `src: Deployment contract bullet 7`
- [ ] `C-DC-08` `contract` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-09` `contract` The server binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-10` `contract` The app starts no copy of a backing service. `src: Deployment contract bullet 10`
- [ ] `C-DC-11` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes para`
- [ ] `C-DC-12` `contract` An invalid call is rejected as a client error. `src: Deployment contract, API shapes para`
- [ ] `C-DC-13` `contract` An unauthorized call is never answered with a silent success. `src: Deployment contract, API shapes para`
- [ ] `C-DC-14` `constraint` An in-memory array standing in for the entries table is a contract violation. `src: Deployment contract, No mocks para`
- [ ] `C-DC-15` `constraint` A hardcoded plan list in the page is a contract violation. `src: Deployment contract, No mocks para`
- [ ] `C-DC-16` `constraint` A leaderboard number written into the markup is a contract violation. `src: Deployment contract, No mocks para`
- [ ] `C-DC-17` `constraint` A rendition typed by hand is a contract violation. `src: Deployment contract, No mocks para`
- [ ] `C-DC-18` `constraint` An asset endpoint reporting success without an object in the bucket is a violation. `src: Deployment contract, No mocks para`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `author@example.com` | pinned by the brief at the citation beside it | C-RL-23 | User roles, seeded accounts table row 1 |
| `author2@example.com` | pinned by the brief at the citation beside it | C-RL-24 | User roles, seeded accounts table row 2 |
| `reader@example.com` | pinned by the brief at the citation beside it | C-RL-25 | User roles, seeded accounts table row 3 |
| `deku-demo-pw-2026` | pinned by the brief at the citation beside it | C-CF-01 | Core features, Auth para 1 |
| `POST /api/auth/sign-up` | pinned by the brief at the citation beside it | C-CF-08 | Core features, Auth para 2 |
| `STORAGE_BUCKET` | pinned by the brief at the citation beside it | C-CF-33 | Core features, images para 1 |
| `library/{entry_id}/{sha256_of_bytes}.{ext}` | pinned by the brief at the citation beside it | C-CF-34 | Core features rule 6 |
| `/api/entries/{entry_id}/assets/{asset_id}/content` | pinned by the brief at the citation beside it | C-CF-39 | Core features rule 7 |
| `Core 3` | pinned by the brief at the citation beside it | C-CF-45 | Core features, portal para 1 |
| `Core 2` | pinned by the brief at the citation beside it | C-CF-45 | Core features, portal para 1 |
| `Core 1` | pinned by the brief at the citation beside it | C-CF-45 | Core features, portal para 1 |
| `Next.js` | pinned by the brief at the citation beside it | C-CF-48 | Core features rule 9 |
| `data-sdk` | pinned by the brief at the citation beside it | C-CF-53 | Core features rule 10 |
| `ruby-rails-sinatra` | pinned by the brief at the citation beside it | C-CF-54 | Core features rule 10 |
| `$20` | pinned by the brief at the citation beside it | C-CF-64 | Core features rule 13 |
| `$250` | pinned by the brief at the citation beside it | C-CF-65 | Core features rule 13 |
| `data-plan` | pinned by the brief at the citation beside it | C-CF-66 | Core features rule 13 |
| `data-billing-period` | pinned by the brief at the citation beside it | C-CF-69 | Core features rule 14 |
| `monthly` | pinned by the brief at the citation beside it | C-CF-69 | Core features rule 14 |
| `annual` | pinned by the brief at the citation beside it | C-CF-69 | Core features rule 14 |
| `1,000 Included per month` | pinned by the brief at the citation beside it | C-CF-71 | Core features rule 15 |
| `$0.00001 each` | pinned by the brief at the citation beside it | C-CF-72 | Core features rule 15 |
| `50,000` | pinned by the brief at the citation beside it | C-CF-77 | Core features rule 16 |
| `Additional $0.02/mo each` | pinned by the brief at the citation beside it | C-CF-78 | Core features rule 17 |
| `Custom OAuth scopes` | pinned by the brief at the citation beside it | C-CF-82 | Core features rule 18 |
| `Aug 21` | pinned by the brief at the citation beside it | C-CF-82 | Core features rule 18 |
| `Copied!` | pinned by the brief at the citation beside it | C-CF-84 | Core features rule 19 |
| `K` | pinned by the brief at the citation beside it | C-CF-87 | Core features rule 20 |
| `Q` | pinned by the brief at the citation beside it | C-CF-87 | Core features rule 20 |
| `X` | pinned by the brief at the citation beside it | C-CF-87 | Core features rule 20 |
| `Y` | pinned by the brief at the citation beside it | C-CF-87 | Core features rule 20 |
| `data-letter-state` | pinned by the brief at the citation beside it | C-CF-89 | Core features rule 20 |
| `active` | pinned by the brief at the citation beside it | C-CF-89 | Core features rule 20 |
| `inert` | pinned by the brief at the citation beside it | C-CF-89 | Core features rule 20 |
| `Adding Aegis auth to your CLI` | pinned by the brief at the citation beside it | C-CF-95 | Core features rule 22 |
| `Jun 4, 2026` | pinned by the brief at the citation beside it | C-CF-95 | Core features rule 22 |
| `/r/{kind}/{slug}.txt` | pinned by the brief at the citation beside it | C-CF-96 | Core features rule 23 |
| `/r/index.txt` | pinned by the brief at the citation beside it | C-CF-99 | Core features rule 23 |
| `data-cell-band` | pinned by the brief at the citation beside it | C-CF-107 | Core features rule 27 |
| `Default` | pinned by the brief at the citation beside it | C-CF-134 | Core features rule 33 |
| `Dark` | pinned by the brief at the citation beside it | C-CF-134 | Core features rule 33 |
| `Simple` | pinned by the brief at the citation beside it | C-CF-134 | Core features rule 33 |
| `Library` | pinned by the brief at the citation beside it | C-CF-134 | Core features rule 33 |
| `data-theme-mode` | pinned by the brief at the citation beside it | C-CF-137 | Core features rule 35 |
| `light` | pinned by the brief at the citation beside it | C-CF-137 | Core features rule 35 |
| `dark` | pinned by the brief at the citation beside it | C-CF-137 | Core features rule 35 |
| `data-instance-state` | pinned by the brief at the citation beside it | C-CF-142 | Core features rule 36 |
| `GET /api/applications` | pinned by the brief at the citation beside it | C-CF-147 | Core features rule 38 |
| `/legal/privacy` | pinned by the brief at the citation beside it | C-CF-149 | Core features rule 39 |
| `privacy@aegis.dev` | pinned by the brief at the citation beside it | C-CF-152 | Core features rule 39 |
| `data-consent` | pinned by the brief at the citation beside it | C-CF-157 | Core features rule 40 |
| `Sorry, we can't find the page you're looking for.` | pinned by the brief at the citation beside it | C-CF-171 | Core features rule 44 |
| `Go to homepage` | pinned by the brief at the citation beside it | C-CF-172 | Core features rule 44 |
| `data-entry-state` | pinned by the brief at the citation beside it | C-UF-11 | User flow, journey 2 |
| `draft` | pinned by the brief at the citation beside it | C-UF-11 | User flow, journey 2 |
| `published` | pinned by the brief at the citation beside it | C-UF-11 | User flow, journey 2 |
| `We don't have any open positions at the moment.` | pinned by the brief at the citation beside it | C-UF-15 | User flow, states para 1 |
| `data-band` | pinned by the brief at the citation beside it | C-UX-19 | UI/UX notes, bands para 1 |
| `Skip to main content` | pinned by the brief at the citation beside it | C-UX-30 | UI/UX notes, accessibility para 1 |
| `GET /api/health` | pinned by the brief at the citation beside it | C-TR-01 | Technical requirements para 1 |
| `200` | pinned by the brief at the citation beside it | C-TR-01 | Technical requirements para 1 |
| `app_user.email` | pinned by the brief at the citation beside it | C-DM-02 | Data model, app_user |
| `entry_asset.object_key` | pinned by the brief at the citation beside it | C-DM-06 | Data model, entry_asset |
| `compliance_row.status` | pinned by the brief at the citation beside it | C-DM-19 | Data model, compliance_row |
| `Held` | pinned by the brief at the citation beside it | C-DM-19 | Data model, compliance_row |
| `Not applicable` | pinned by the brief at the citation beside it | C-DM-19 | Data model, compliance_row |
| `Not offered` | pinned by the brief at the citation beside it | C-DM-19 | Data model, compliance_row |
| `41` | pinned by the brief at the citation beside it | C-DM-21 | Data model, seed para 1 |
| `Rotating a signing key without downtime` | pinned by the brief at the citation beside it | C-DM-22 | Data model, seed para 1 |
| `session-management` | pinned by the brief at the citation beside it | C-DM-23 | Data model, seed para 1 |
| `/app/USER_README.md` | pinned by the brief at the citation beside it | C-DM-28 | Data model, password paragraph |
| `More than authentication, Complete User Management` | pinned by the brief at the citation beside it | C-FE-18 | Front-end specification, home para 2 |
| `Trusted by fast-growing companies around the world.` | pinned by the brief at the citation beside it | C-FE-19 | Front-end specification, home para 3 |
| `Plans for every stage` | pinned by the brief at the citation beside it | C-FE-26 | Front-end specification, pricing para 1 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the eight customer marks in the trust strip | C-FE-01 | named as a count with no individual names given |
| the six coding-agent vendor names | C-FE-01 | referenced by slot with no literal names given |
| the eleven reading-assistant names in the article sidebar | C-FE-01 | referenced by count with no literal names given |
| the exact colour value behind every named role | C-UX-01 | carried as family, tone and shade rather than as a value |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 6 |
| User roles | 1 | 25 |
| Core features | 20 | 174 |
| User flow | 3 | 18 |
| UI and UX notes | 11 | 32 |
| Technical requirements | 9 | 17 |
| Data model | 6 | 28 |
| Front-end specification | 23 | 35 |
| Constraints | 3 | 14 |
| Deployment contract | 9 | 18 |

`## Definition of done` produces no items. Every clause in it restates an ask already
carried by `## Core features`, and section 3.5 folds a restatement into the item it
restates rather than minting a second one.

38 asks were extracted and then withdrawn because no channel can observe them:
the framework and library names, the structured log destination, the absence of a second
datastore, the layout-shift figure, the font fallback metrics, the absence of an edge
function or a persistent volume, the table count, and the visual details of the chrome
that leave no trace a browser, an HTTP call or a reader of one criterion could settle.
Each is a real requirement of the brief and none of them is graded, so none of them
appears here. Recorded rather than carried, per OPEN-DECISIONS D-H.

