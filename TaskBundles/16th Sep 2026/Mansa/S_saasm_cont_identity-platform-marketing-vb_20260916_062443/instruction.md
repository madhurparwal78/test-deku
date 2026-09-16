# Aegis

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, compare the four plans, read a quickstart in the framework of their choice, create an account, and provision their first application instance and watch it reach a live state, without hitting an error page. A second stranger, signed in as a different author, must NOT be able to read an unpublished library entry, its plain-text rendition, or the image attached to it, by any means. The image bytes must live in the object store at their scheme's key; a copy on the app's own disk does not count, and neither does a record in the database that says an upload happened.

## Overview

Aegis is a hosted identity platform. This product is the public site that sells and documents it, and the service that assembles that site from sources rather than from hand-edited pages.

The site carries twenty-eight routes: four product routes, three framework landing routes, a pricing table, a documentation portal, a changelog, a glossary, a blog, a company set, a legal set, and two routes that are small applications rather than pages. It is written for six readers in a fixed order of priority: an engineer evaluating an identity provider, an engineer already sold and starting work, a coding agent doing the integration on that engineer's behalf, a founder comparing cost, a security or procurement reviewer, and a candidate.

The site is not the platform. The platform is a signed-in console and a set of services elsewhere. The site's job is to convince a developer to sign up and to hand them enough documentation that they never need to ask a human anything. It deliberately is not: a working identity provider, a signed-in console, a support inbox, a contact form, or a store of anybody's card details.

The genuinely hard part is that a draft is invisible in three places at once. An unpublished entry is hidden from its route, its plain-text rendition address must refuse to serve it, and the image bytes attached to it must stay unreadable in the object store, for everyone except the author who owns it. A build that hides the draft on the page and leaves its rendition or its image reachable has not done the work.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `author` | Create, edit, publish and unpublish library entries they own. Upload an image to an entry they own. Read their own drafts, their own draft renditions and their own draft images. Open the author studio. | **Cannot read, edit, publish or unpublish another author's entry, in any state.** **Cannot read another author's draft rendition or draft image.** **Cannot provision an application or an instance.** |
| `reader` | Sign up without an invitation. Read every published entry, rendition and image. Provision applications and instances on their own account. Save and share a theme. Apply to the startup programme. | **Cannot read any draft, any draft rendition or any draft image, including one they were linked to directly.** **Cannot create, edit or publish a library entry.** **Cannot read another account's applications or instances.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a `reader` session to any `author`-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Signup is open. Anyone may create a `reader` account from `/sign-up` with no invitation and no approval step. `author` accounts exist only as seeded data and cannot be created through the site.

Seeded accounts, every one with the password `deku-demo-pw-2026`:

| Email | Role | Display name |
|---|---|---|
| `author@example.com` | `author` | `Ada Renn` |
| `author2@example.com` | `author` | `Milo Vance` |
| `reader@example.com` | `reader` | `Priya Shah` |

## Core features

### Auth

Email and password, implemented in this application. Passwords are hashed and the exact literal `deku-demo-pw-2026` must work at login for every seeded account. A successful call to `POST /api/auth/login` returns a bearer token in the field `access_token`; the client sends it on every request except login, sign-up, the health route and the public read endpoints. A token that has expired mid-action leaves the page in place, shows an inline banner saying the session ended, and offers to sign in again without discarding the form the visitor was filling.

`POST /api/auth/sign-up` takes `email`, `password` and `display_name` and creates a `reader`. A second signup with an address already in use is refused as invalid and creates nothing. There is no password reset flow and no email is sent anywhere by this product.

### The library and its publication rules

One store stands behind the documentation portal, the changelog, the glossary, the blog and the legal set. An entry carries a `kind` of `doc`, `changelog`, `glossary`, `blog` or `legal`, a `slug`, a `title`, a `summary`, a `body`, and a `state` of `draft` or `published`.

1. An author creates an entry as a `draft` and it is visible to nobody but that author. Requesting a draft's public route, its plain-text rendition address, or any image attached to it, as an anonymous visitor, as a `reader`, or as a different `author`, is refused and the entry is not disclosed by the refusal.
2. Publishing an entry makes it readable at its route, writes its plain-text rendition in the same operation, and stamps `published_at`. Unpublishing reverses all three: the route stops serving it, the rendition address stops serving it, and its images stop being readable.
3. **Exactly one published entry holds a given `kind` and `slug` pair.** Two simultaneous publishes claiming the same pair must not both succeed: exactly one wins and the other is rejected as a conflict. The loser leaves nothing behind - no half-written entry, no orphan rendition row, no entry stranded between states.
4. A rendition exists for every published entry and for no draft. It is generated in the same operation that publishes, from the same source, so the page and the rendition cannot drift. Nothing on this site is typed into a page: every route that reads is a rendering of the content pipeline, and four surfaces that look like marketing pages are in fact renderings of live operational data - the pricing table from the plan document, the leaderboard from the result rows, the compliance table from the compliance register, and half the documentation from the entries themselves. Each would be wrong within a month if somebody kept it up to date by hand. Versioning is part of the pipeline: the documentation tree exists at `Core 3`, `Core 2` and `Core 1`, each a complete tree, and a reader on an older version sees a persistent notice and a link to the current one, with search scoped to the version they are on.
5. An entry the build cannot render a code sample for, in the SDK the reader has selected, says so in an explicit note. Showing a different framework's code is worse than showing none.

### Images live in the object store

Every image attached to an entry is stored in the MinIO bucket named by `STORAGE_BUCKET`, reached at `STORAGE_ENDPOINT` with `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`, and nowhere else.

6. The object key is `library/{entry_id}/{sha256_of_bytes}.{ext}` - for example `library/42/9f2a1c7d3b0e5a86c41f29d7e0b3a5c8d9f1e2a4b6c8d0e2f4a6b8c0d2e4f6a8.png`. An upload writes the bytes to that key, records the key, the content type, the byte size and the alternative text, and stores no copy anywhere else. Bytes on the app container's filesystem are a contract violation, as is a database column holding the image itself, however correct the page looks.
7. Bytes are served only through `GET /api/entries/{entry_id}/assets/{asset_id}/content`, which streams them from the bucket after checking who is asking. The bucket is never made publicly readable and no time-limited link to an object is ever issued, for a draft or for anything else.
8. Idempotency on upload: sending the same bytes to the same entry twice does not create a second object and does not create a second asset record. The second attempt is a no-op that returns the existing asset.

### The documentation portal

The portal replaces the global chrome with its own: a low, dense tool bar carrying the wordmark, a `Docs` chip, a version select reading `Core 3` with options `Core 3`, `Core 2` and `Core 1`, a search field, an `Ask AI` action and a right-aligned `Sign Up` action. It does not float and it carries no announcement bar.

9. The SDK selector sits at the top of the sidebar in its own labelled well reading `Select your SDK`, and carries thirty options in this order: `Next.js`, `React`, `Expo`, `TanStack React Start`, `React Router`, `Express`, `Android`, `Astro`, `Chrome Extension`, `C#`, `Fastify`, `Go`, `iOS`, `Java`, `JS Backend SDK`, `JavaScript`, `Nuxt`, `PHP`, `Python`, `Remix`, `Ruby / Rails / Sinatra`, `Vue`, `Angular`, `Elysia`, `Flutter`, `Hono`, `Koa`, `Rust`, `SolidJS`, `Svelte`, `Tauri`. It defaults to `Next.js`.
10. Changing the SDK rewrites every code sample in the portal without reloading the page and without losing the scroll position, and the choice survives navigation to another documentation route and a return visit later. The document element carries `data-sdk` set to the selected option lowercased with spaces and slashes collapsed to single hyphens, so `Ruby / Rails / Sinatra` reads `data-sdk="ruby-rails-sinatra"`. This is the single most important piece of state in the portal.
11. The sidebar carries two mode rows, `Guides` and `Reference`, the first selected, then a hairline, then a tree whose top-level nodes are, in order: `Getting started`, `Authentication flows`, `User management`, `Session management`, `Organization management`, `Billing management`, `Account Portal`, `Customizing Aegis`, `Securing your app`, `AI`, `CLI`, `Development`, `Aegis Dashboard`, `How Aegis works`. `CLI` is a leaf and the rest are branches whose expansion state is exposed to assistive technology.
12. Search ranks an exact symbol name above a merely related passage, and by default restricts results to the reader's current SDK and version selection, with a visible control to widen. Landing a reader on a three-year-old page is how they conclude the product is broken. A search with no results shows a plain sentence and the `Ask AI` action rather than an empty list.

### Pricing, and the one plan document

The pricing route renders from a single plan document. The comparison matrix and the plan cards read the same document; a matrix maintained separately will be wrong within one release and wrong in a way that costs money.

13. Four plan cards across, in order `Hobby`, `Pro`, `Business`, `Enterprise`, each carrying a name, a price, a qualifier, a positioning sentence, an action and a feature list under a lead-in line. `Hobby` shows `Free`, `No credit card required`, `Everything you need to start building.`, the action `Start building for free` and the lead-in `Included in Hobby:`. `Pro` shows `$20`, `per month, billed annually`, `Scale with full-featured authentication.`, `Upgrade to Pro plan` and `Everything in Hobby, plus:`. `Business` shows `$250`, `per month, billed annually`, `Tackle compliance and growing teams.`, `Upgrade to Business plan` and `Everything in Pro, plus:`. `Enterprise` shows `Custom`, `Only billed annually`, `Tailored solutions and guarantees.`, `Talk to sales` and `Everything in Business, plus:`. Each card carries `data-plan` set to `hobby`, `pro`, `business` or `enterprise`. Only the `Hobby` card carries a filled action.
14. The two middle cards carry a `Monthly` and `Annual` toggle. Flipping it recomputes the displayed price and the page carries `data-billing-period` set to `monthly` or `annual`. The digits roll rather than the whole number being replaced.
15. The comparison matrix cells are not ticks. A cell may carry a graduated ladder, and these are quoted exactly: under `Enterprise connections`, `101 - 500` at `$30/mo each` and `500+` at `$15/mo each`; under `API Keys`, `Creations` at `1,000 Included per month` then `1,001+` at `$0.001 each`, and `Verifications` at `100,000 Included per month` then `100,001+` at `$0.00001 each`; under `M2M Tokens`, `2,500 Included per month` then `2,501+` at `$0.001 each` with the same verification ladder. The `Hobby` column shows a combined summary instead: `1,000 creations & 100,000 verifications limit per month` and `2,500 creations & 100,000 verifications limit per month`.
16. `MRU` and `MRO` are rendered as buttons, not as text. Pressing one discloses its definition. A monthly retained user is a user who signed in or had a session refreshed within the calendar month, counted once per user per instance per month. A monthly retained organization is an organization with at least one such user in that month, counted once per organization per instance per month. The free allowance is `50,000` monthly retained users and `100` monthly retained orgs per application, and that number governs the whole business. The metering mechanics the ladders describe are display facts on this site, not behaviour: the page states what a metric counts, what is included, and what each additional unit costs, and it reads all three from the plan document.
17. The `Pro` list quotes `50,000 MRU included per app` with `Additional $0.02/mo each`, `1 Enterprise connection included` with `Additional $75/mo each`, and `Satellite domains` with `Additional $10/mo each`. The `Business` list quotes `10 dashboard seats included` with `Additional $20/mo each`. The matrix header row sticks beneath the chrome at reduced height on a fully opaque ground, because a blurred sticky row over a dense table is unreadable.

### The changelog, the glossary, the blog and the legal set

18. The changelog is a vertical timeline, newest first, and its structure is one entry per release note. Each entry carries a date in the gutter, a node dot on a vertical rule, a category chip, a title, a one-sentence summary, a body, a contributor list and a copy-link control. The newest dot carries the accent; the rest are faint. Three entries are seeded and published, all with the category `Product`: `Customize the reverification window` dated `Aug 28`, `Audit Dashboard activity with Admin Logs` dated `Aug 25`, and `Custom OAuth scopes` dated `Aug 21`.
19. Pressing the copy-link control copies the entry's permalink and swaps the label to `Copied!` in place, positioned over the original so the row does not resize, reverting after a short interval.
20. The glossary is a single route holding every term, with a sticky rail of twenty-six letters beneath the chrome. A letter with entries is a link; a letter without is inert, set back, not focusable, and announced as unavailable. The letters `K`, `Q`, `X` and `Y` are inert. The letter matching the current scroll position carries the accent. Each rail cell carries `data-glossary-letter` set to the lowercase letter and `data-letter-state` set to `active` or `inert`.
21. Each glossary entry is an anchor target, a heading, a permalink glyph that appears on hover, a definition body and a `Related terms` list of chips. Cross-linking is derived by the build from the terms each entry declares, never hand-authored: the build finds the mentions, produces the links, and refuses to finish if a target does not exist or an entry links only to itself. Every chip is an internal link to another entry on the same route, and the graph is dense. It reports orphan entries so nothing is quietly lost, because a hand-maintained graph of a few hundred entries decays immediately.
22. The blog index carries the eyebrow `Blog`, the headline `News, insights and more`, a category filter row reading `All categories`, `Company`, `Engineering`, `Testimonial`, `Guides`, `Insights`, and three feature cards. Seeded and published: `Adding Aegis auth to your CLI` dated `Jun 4, 2026`, `Going to production with Aegis Deploy` dated `May 29, 2026`, and `Aegis Init: The fastest way to start a new project` dated `May 11, 2026`.
23. Every article, documentation page, changelog entry and glossary entry exists in a clean plain-text rendition at `/r/{kind}/{slug}.txt`, derived from the page's own address and generated in the same build from the same source. The rendition carries the title, the canonical address, the last-updated date, and the body with code fenced and links preserved as text. A site-level index of every rendition is published at `/r/index.txt` so an automated reader can enumerate the corpus without crawling. The article sidebar's `Open in` links carry the rendition's address, never its contents.
24. The changelog and the blog each publish a feed, linked from their route, carrying full content rather than excerpts and stable identifiers so a reader does not see an entry twice after an edit.
25. The legal index splits its documents into two columns under the headings `Customers` and `Everyone else`, which separates what a paying customer needs from what any visitor needs and is a better organising principle than an alphabetical list.

### The model leaderboard

26. The matrix header reads `Model / Average` then nine task columns in this order: `Organizations`, `Billing`, `Webhooks`, `Add Auth`, `Auth`, `Quickstarts`, `UI Components`, `Upgrades`, `User Management`. Each body row is a rank ordinal that is announced but not shown, a vendor mark carrying an accessible name, a model name, an average chip, then nine score cells.
27. Each score cell carries `data-cell-band` set to `above` when the score is at or above that column's mean, `below` when it is under, `bottom-decile` when it falls in the lowest tenth, and `absent` when there is no result. A cell with no result renders as an explicit absence and never as a zero. The matrix is a real table with header associations, so a cell can be read as model by task.
28. Three controls sit above it: a framework select offering `Android`, `Next.js`, `iOS` and `React` and defaulting to `Next.js`, a provider select offering `All Providers` then the vendor names, and a three-way toggle reading `Base`, `MCP` and `Skills`. An information glyph beside the toggle discloses what the three mean: `Base` gives the model the instruction and the repository alone; `MCP` adds a live connection to the tool server so it can query current documentation; `Skills` adds a prepared instruction bundle shipped with the product. Published without those definitions, a comparison across modes misleads.
29. Every published cell names the model version, the harness version, the corpus version and the run date, and states the number of runs it averages. A single run of a non-deterministic system is not a measurement. Switching framework selects a different subset of the corpus rather than a different view of the same numbers.
    The numbers behind the matrix come from a fixed corpus of tasks grouped into the nine families. A task is a starting repository at a pinned commit, an instruction in plain words, a set of assertions and a time budget, and nothing about a task depends on the model being measured. Grading is programmatic and binary per assertion, and a task's score is the fraction of its assertions that pass: the project builds, the project runs, a scripted sign-up completes, a named file exists. No model marks another model and no person marks a run, because neither can be audited. Execution of each task happens in a fresh isolated environment with no credentials, a wall-clock budget and a memory ceiling, destroyed afterwards, which is what makes two runs comparable. Package resolution is pinned: a task whose dependency set drifts is a task whose score drifts for reasons that have nothing to do with the model. The corpus is published, a corrected score is published as a correction with its date rather than silently swapped, and every model is re-run on every corpus change so cells are never compared across corpus versions. A benchmark published by an interested party, without its corpus, is an advertisement.

### The component theme editor

30. The route fills the window exactly and never scrolls the document. It holds an infinite canvas of live component previews, each labelled with its monospace name: `<SignUp />`, `<SignIn />`, `<UserButton />`, `<UserProfile />`, `<Waitlist />`, `<PricingTable />`. The canvas pans by drag and zooms by modifier plus scroll, every preview is a live instance rather than a picture and re-renders when a value changes, type stays sharp at every zoom level, and the canvas position survives a component selection change.
31. A theme is exactly seventeen values and the mode, and nothing else. Five primary fields in order: `Primary`, `Background`, `Foreground`, `Foreground primary`, `Neutral`. Then an `Advanced` disclosure revealing twelve more: `Muted`, `Foreground muted`, `Ring`, `Input`, `Input foreground`, `Border`, `Shadow`, `Modal backdrop`, `Success`, `Warning`, `Danger`. Everything else about a component's appearance is derived from those. `Foreground` is derived from `Background` until it is explicitly set, and is shown disabled at the default for exactly that reason.
32. Derivation happens in a perceptual colour space so a hover state on a saturated ground keeps its hue, and every derived pair carries a contrast floor: a foreground that fails against its background produces a warning in the editor and is clamped when the component renders, never a silently unreadable component. The compiler is deterministic: the same seventeen inputs always produce the same output, on the server and in the browser.
33. Sharing is by address alone. `Copy URL` encodes the whole theme into the address fragment, which browsers never send to a server, so a colleague opening the link sees the same thing with no round trip and nothing stored. The encoding is versioned in its first character, so adding a field later does not break an older link. A shortened stored form may be offered as an addition and is never the only form, because a link that requires this service to be reachable is a worse link. Decoding is total: a malformed, truncated or unknown-version string falls back to the preset `Default` silently and does not error. `Copy CSS` emits the value block. Four presets ship: `Default`, `Dark`, `Simple` and `Library`, and a preset carries no powers an ordinary theme lacks.
34. A theme is untrusted input. It compiles to a fixed set of named values with validated contents and never to arbitrary style text. Somebody who could inject arbitrary style into a sign-in component could redraw that component to look like anything, inside a frame people have been taught to trust.
35. The mode toggle reads `Light mode` and `Dark mode` and the canvas carries `data-theme-mode` set to `light` or `dark`. A first-run card floats over the canvas reading `Welcome to the Aegis Theme Editor. Scroll, zoom, and click around to explore Aegis's components. Apply new themes and variables to create your own look, and share it with your team.` with a single action `Got it`.

### Accounts, applications and instances

36. A signed-in `reader` opens `/dashboard` and creates an application by name. Creating one also creates its `development` instance. An instance moves through `pending`, then `provisioning`, then `live`, and never skips a step; a failure lands it in `failed` and says why. The row carries `data-instance-state` set to the current value and the state is durable: it survives a reload and a restart.
37. Each instance carries a publishable key that is unique across the product and is shown once the instance is `live`. A development instance and a production instance of the same application share nothing: not users, not keys, not settings. That separation is why taking an application live is a real operation rather than a settings change.
38. A `reader` reading `GET /api/applications` receives only their own. A request for another account's application or instance, by id, is refused and the underlying rows do not change.

### The launch surface

39. A privacy page at `/legal/privacy`, reachable from the footer of every route, states what Aegis records about a visitor to this site, how long it is kept, and how to ask for it to be removed at `privacy@aegis.dev`. It is a published library entry of kind `legal` like the rest of the legal set.
40. A first-time visitor is asked once about non-essential cookies, through a panel opened by the footer's `Cookie manager` control and shown unprompted on a first visit. The answer survives a reload and a return visit, withdrawing consent is exactly as easy as granting it, the control is reachable from every route and operable by keyboard alone, and the document element carries `data-consent` set to `granted`, `declined` or `undecided`. Analytics loads only after the answer is `granted`, and never before the document is readable.
41. Every public route carries its own title and its own description, and no two routes share either. The description is a meta description in the document head, present on all twenty-eight routes.
42. The site serves a favicon and declares it in the document head. The favicon is the brand mark, generated from the same geometry as every other rendering of it, so there is no image file to ship.
43. The startup programme application form refuses a bot. An unattended decoy field that a person never sees and never fills, arriving filled, is refused. The same form submitted repeatedly in quick succession from one caller is refused after the second attempt within the window. A refused submission stores no company name and no application, and says so in an inline banner naming the reason.
44. An unknown address renders the site's own not-found page and answers not-found. It is a near-black ground carrying a very large `404` drawn as a dot matrix inside a dashed rectangle, the single line `Sorry, we can't find the page you're looking for.`, and one secondary action `Go to homepage`. It keeps the global chrome so a visitor is never stranded, and drops the announcement bar. No search box, no suggestions.

## User flow

### Routes

| Route | Purpose | Auth |
|---|---|---|
| `/` | home: the full band sequence, the component showcase, three feature tile grids, testimonials | public |
| `/user-authentication` | product route: the sign-in half, with the assurance strip and the component walkthrough | public |
| `/multi-tenancy` | product route: organizations, the three-step demonstration, the console section | public |
| `/billing` | product route: plan definition, the embedded commerce demonstration, unified data | public |
| `/react-authentication` | framework landing route for React | public |
| `/nextjs-authentication` | framework landing route for Next.js | public |
| `/expo-authentication` | framework landing route for Expo | public |
| `/agents` | the vendor grid, the primitives section, the embedded leaderboard | public |
| `/cli` | the command line route, with its own header and its own dark register | public |
| `/pricing` | the four plan cards, the add-on section and the comparison matrix | public |
| `/docs` | the documentation portal shell and its landing content | public |
| `/changelog` | the timeline | public |
| `/glossary` | every term on one route, with the alphabet rail | public |
| `/llm-leaderboard` | the filtered matrix | public |
| `/components/theme-editor` | the canvas and the seventeen-field panel | public |
| `/blog` | the index, with the category filter | public |
| `/blog/:slug` | one article, with the `Explore with AI` sidebar | public |
| `/company` | the investor band, the pull quote, the individual investor grid | public |
| `/careers` | the founder letter, the statistics, the benefits, the open roles | public |
| `/startups` | the programme, the application card and the testimonial band | public |
| `/security` | the compliance table and the security practices | public |
| `/contact` | two large cells and three smaller ones, and no form | public |
| `/brand-assets` | fourteen asset cells with two download formats each | public |
| `/legal` | the two-column index | public |
| `/legal/privacy` | the privacy policy | public |
| `/legal/standard-terms` | the commercial terms | public |
| `/legal/website-terms` | the website terms | public |
| `/discord` | an off-origin redirect to a community service; nothing about the destination is specified | public |
| `/sign-in` | sign in | public |
| `/sign-up` | open signup, creating a `reader` | public |
| `/dashboard` | a reader's applications and instances | `reader` |
| `/studio/library` | the author's table of every entry they own | `author` |
| `/r/{kind}/{slug}.txt` | the plain-text rendition of one published entry | public |
| `/r/index.txt` | the enumeration of every rendition | public |

The site links eight framework quickstart paths beneath the documentation root, three integration guide paths, a student programme route, six component detail routes beneath `/components`, and an external roadmap host. Build the links; their interiors are not specified here.

### Entry and redirects

An anonymous visitor reaching `/dashboard` or `/studio/library` is sent to `/sign-in` with the intended address remembered, and lands there after signing in. Signing in sends a `reader` to `/dashboard` and an `author` to `/studio/library`. Signing out returns to `/` and the chrome action pair reverts to `Sign in` and `Sign up`. A `reader` reaching `/studio/library` is refused and shown their own dashboard instead. An expired token mid-action leaves the page in place and offers to sign in again without discarding the form.

### Journeys

**Compare, read, sign up, provision.** Open `/`. Follow `Pricing` in the header. Flip the toggle on the `Pro` card from `Monthly` to `Annual` and watch the price roll digit by digit. Press `MRU` and read the definition it discloses. Follow `Docs`. Change the SDK selector from `Next.js` to `React` and watch every code sample rewrite with no reload and no loss of scroll position. Press `Sign up`, create an account, land on `/dashboard`, create an application named `Taskflow`, watch its development instance move from `pending` through `provisioning` to `live`, and read its publishable key.

**An author publishes an entry with an image.** Sign in as `author@example.com`. Open `/studio/library`, a table of every entry with its kind, slug, state and last update. Press `New entry`; a panel slides in from the right edge. Fill kind, title, slug and body, attach an image with alternative text, save as a draft. The row appears with `data-entry-state="draft"`. Press `Publish`. The entry appears on its route, its rendition appears at `/r/{kind}/{slug}.txt`, the row reads `data-entry-state="published"`, and an inline banner confirms it in place.

**A second author is refused a draft.** Sign in as `author2@example.com`. Request the draft owned by `author@example.com` by its route, by its rendition address, and by its image address. All three are refused and nothing changes.

**Two publishes contend for one slug.** Two drafts of kind `doc` both claim the slug `session-management`. Publishing both at the same moment leaves exactly one published entry holding that pair, exactly one rendition row, and one refusal that wrote nothing.

**A colleague opens a shared theme.** Open `/components/theme-editor`, dismiss the first-run card, change `Primary`, press `Copy URL`, open the copied address in a fresh session, and see the same seventeen values.

**A bot is refused.** Submit the startup programme application with the decoy field filled, or submit it repeatedly in quick succession. Both are refused, nothing is stored, and an inline banner names the reason.

### States

Every list has an empty state and every page a loading state. The careers route's empty state is designed rather than incidental: a full-width row with rules above and below reading `We don't have any open positions at the moment.`, with the standing invitation kept directly above it: `Don't see your dream role?`, `We're always looking for Staff+ engineers across the stack. Let's chat about how you can make your mark with us!`, and the arrow link `Join our team`. For most of any year that is the version of the page people see. A leaderboard filter that yields nothing keeps the matrix header and explains in one row. A theme that fails to parse falls back to `Default` silently. Errors never crash the app: a failed request leaves an inline banner and the page still usable.

## UI/UX notes

Somebody arriving here should immediately understand that this is infrastructure built by people who care about detail, and should feel they could start work in the next five minutes without asking anyone a question. The register is a developer product sold to engineers: quiet and precise, editorial composition allowed on the marketing routes and forbidden inside the documentation portal and the command line route, both of which are tools addressed to somebody already working.

It has to guide, so every route leads with one obvious primary action and everything else is quieter. It has to support exploring, so the proof sections repeat one scannable shape down the home route rather than inventing a composition each time. It has to convey trust while an engineer decides, so nothing moves while somebody is reading a price and the compliance table sets what the company does not hold in the same type as what it does.

**Ground and ink.** Two grounds, swapped per band rather than per session. The page ground is a near-white neutral on a light band and a near-black neutral on a dark one. A raised surface, which is what a card, a panel and the header pill are, is a near-white neutral on light and a deep neutral on dark, and must stay visibly separate from the ground without a shadow. A sunken surface, which is an inset well, a code block or a table's zebra row, is a near-white neutral on light and a near-black neutral on dark. A hovered row is a near-white neutral on light and a deep neutral on dark. The hairline is a near-white neutral on light and a deep cool neutral on dark, and it is the most-used colour in the product: this is a site made almost entirely of thin grey lines separating white boxes, and the eye is steered by the small amount of ink and the even smaller amount of colour. Five inks by role: display for headlines, body for prose, quiet for supporting copy and inactive rail items, faint for labels above a group and table column heads, strong for text that must survive on a busy surface.

**The accent, rationed.** One accent family, eleven steps, running from a near-white cool neutral through a light, vivid indigo at the brand step to a deep, soft indigo at the darkest. The brand step is the primary action ground, the eyebrow above a section headline, the active glossary letter and the logo mark, and it is the only saturated colour anywhere in the chrome of a marketing route. Everything else in the chrome is grey. A substitute must hold that discipline: one hue, used sparingly, against an otherwise neutral field. A second family exists only inside the embedded console caricatures, standing for the console's own palette rather than the site's, and its roles are named so they cannot drift: a console-accent primary, a console-accent-soft for the same action at rest, a console-blue informational chip with a console-blue-deep pressed state, a console-green healthy pip with a console-green-deep success chip on a light ground, a console-orange warning, a console-red destructive action with a console-red-deep pressed state, a console-ink for body text and a console-rule for hairlines. In words: a light, vivid indigo primary, a light, vivid blue informational chip, a mid, vivid green healthy pip, a light, vivid orange warning, a light, vivid red destructive action.

**Signal colours, exclusive.** Three carry meaning and appear nowhere else on a marketing route: a mid, vivid green for held, passing and above the band; a light, vivid red for not held, failing and below the band; a mid, vivid orange for partial and degraded. A mid, vivid cyan is the informational colour of the framework routes and the one coloured rule on the site; its bright step is the string colour in dark code and the one saturated colour permitted inside a headline, on the careers route only. A state that is none of these may not borrow any of them. The exact shades are yours, so long as those two rules hold.

**Type.** A grotesque for display and interface, carrying a genuine `450` weight between regular and medium, used for footer column heads, table labels and the trust strip caption, and never rounded to 400 or 500. Tabular lining numerals on a single advance width, so a price or a counter changes a digit without the line reflowing. A monospace at 400 and 500 with a full system fallback chain. A script face at one weight, on one route, for three words. The console caricatures drop deliberately to the system stack. The measured scale is one body size at `15px` on `28px`, one small size at `13px` on `24px` in two weights, a reading size at `16px` on `24px`, and the book weight at `14px` on `20px` where the labels are. A hero headline is `2.5rem` on `3rem` at the small breakpoint and above and `2rem` on `2.5rem` below it, at weight 700 with tight negative tracking and balanced wrapping.

**Shape and depth.** Corners are barely softened and the scale is short. Every shadow begins with a hairline ring and only then adds a blur; drop the ring and the whole interface reads soft, and the ring is the design. Four recipes, no scale: a raised card on a light band, a filled action, an embedded screenshot, a floating panel over a dark band.

**Density.** Comfortable on a marketing route, compact inside the documentation portal, the comparison matrix and the leaderboard, where rows sit tight so more of a table fits one screen.

**Motion is eased.** Movement reads as a designed interface rather than a machine, and the signature is an asymmetry: a control answers the pointer quickly and takes more than twice as long to settle back. Fast to answer, slow to forget. Every chrome recolour, every link and every card lift share one curve; an arrival from off-screen uses a second; a panel coming to rest uses a third; the only curve that overshoots belongs to controls that toggle. The busiest timing on the site is a slow entrance rather than a quick response, because most motion here is a diagram assembling itself while somebody reads the sentence beside it. No text moves on scroll and no headline scrubs. The named moments, each of which must exist: a blinking block cursor in a terminal; a slow float whose distance is set per instance so a field of ornaments never looks synchronised; a pulse on a placeholder; a spin on a busy indicator; a fade whose start and end are both set per instance; a headline arriving one character at a time, each character starting invisible and slightly out of focus and sharpening as it fades up; three concentric rings behind a hero offset so exactly one is at peak at any moment, reading as one slow heartbeat rather than three; a copy control whose two states cross-fade in place, the pages softening while the tick sharpens, with nothing sliding; a component deck that fans and settles, the frontmost panel rotating slightly about the horizontal axis at the midpoint of its cycle while the others recede, blur and fade back; a connector that scales from its own origin so it draws itself outward from its joint rather than sliding in; a digit column that rolls rather than being replaced. Reduced motion is honoured in three levels: a transition carries a per-element override that removes it, a loop keeps running with fixed delays so it is visually static rather than frozen mid-frame, and anything arriving on first paint renders in its final state. Nothing is hidden and no meaning is lost; every animation here is decorative.

**Bands and the notch.** Light and dark are a per-band property and not a visitor preference. There is no site-wide theme control and adding one would contradict the authored sequence. Theme must be selectable on an arbitrary ancestor rather than only the document root, because the home route stacks light and dark inside one scroll, and every band carries `data-band` set to `light` or `dark`. Every boundary between a light band and a dark one carries a wide shallow trapezoidal notch with rounded elbows at both ends, drawn in the colour of the band it belongs to, on both sides. A single one-sided wedge reads as a mistake.

**The ambient field.** Behind nearly every hero sits a faint technical drawing: a lattice, thin traces walked with right angles and diagonals, small squares and rings at the junctions, dotted runs. Over it sits a soft pool of light, brightest just above the middle of the headline and falling away at the edges, so the drawing emerges from nothing rather than stopping at a boundary. On a dark band the drawing fades down into black, computed in a perceptual space so it does not go muddy in the middle. Small round badges are not flat circles: each carries a hairline of near-white along its top edge as though a light above were catching the rim, and a soft shadow below. The one genuinely bright moment on the site is the top of the command line route, where an indigo wash over the near-black ground must brighten rather than tint; fading an indigo over black gives grey, and this has to give a glow.

**Responsive.** Three columns become two then one, five footer columns become three then two, four pricing cards become two then one with `Hobby` first. The most-used condition in the whole system is not a width: it is whether the visitor has a pointer that can hover, and every hover treatment is guarded by it, so nothing sticks in a highlighted state after a tap. The document never scrolls sideways at any viewport. Four things may scroll sideways inside their own container: the comparison matrix, the leaderboard, the second-level rail at narrow widths, and a code block whose content exceeds the measure. One route is taller at tablet than at phone because its console caricature stacks its rail above its detail pane at tablet; build the cropped phone variant showing the detail pane alone, or the phone page grows half as long again for no gain. At a narrow viewport nothing overflows sideways and every navigation target stays reachable.

**Accessibility floors.** Contrast meets WCAG AA: 4.5 to 1 for body text, 3 to 1 for a glyph carrying meaning, and a focus ring visible at 3 to 1 against both adjacent colours. Display ink against its ground is at least 12 to 1. Full keyboard navigation with a visible focus ring on every interactive element, focus order following reading order, and no positive tab index. Comfortably sized touch targets. Labels on icon-only controls. Meaning is never carried by colour alone: a leaderboard cell's ground indicates its band and its number states the value, a compliance chip's ground indicates status and its text states it. Every content image carries alternative text and decorative images declare themselves decorative. Any text broken into per-character elements carries one clean screen-reader copy, or two routes here are read out one letter at a time. The skip link reading `Skip to main content` is the first focusable element on every route. Under forced colours every structural hairline resolves to a system border colour, the notch leaves no gap, the dot-matrix ornaments are hidden rather than rendered as solid blocks, and every chip gains a border.

**Components behave, not just appear.** Every input shows its focus ring, carries a label above it and its error message directly beneath it rather than in a floating layer. Every panel that covers the page closes on Escape and on a click outside it. Every destructive action asks once before it runs, and the confirming control names what will be destroyed rather than saying yes. An inline banner reports the outcome of a request in place; nothing important is announced in a corner and then taken away on a timer.

**What it must not look like.** No page dominated by a single hue family with no second signal. No decoration standing in for content. No marketing composition inside the documentation portal or the command line route, both of which are tools. No flattening of the mark's two-tone crescents, the only thing distinguishing it from a plain letter at small sizes. No soft shadow without its hairline ring. **Space over dividers** on the marketing routes and **dividers over space** inside the tables: the comparison matrix, the compliance table and the leaderboard earn their hairlines because a reader is comparing across rows, and everything else earns its air because a reader is being led down a page.

## Technical requirements

The frontend is Nuxt 3, server-rendered with islands. The backend is Fastify, serving the JSON API under the `/api` prefix on the same origin. The datastore is PostgreSQL, reached through `DATABASE_URL`. The object store is MinIO, reached through `STORAGE_ENDPOINT` with `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Authentication is email and password implemented in this application, with bearer tokens. `GET /api/health` returns `200` once the app is ready. Requests are logged as structured records to standard output.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor - the only backing services available in this environment are PostgreSQL and MinIO, and reaching for anything else is a contract violation. Both are already running and reachable at the variables above; do not download, install, compile or start a copy of either.

**What the browser receives.** Every route except `/components/theme-editor` and `/startups` is complete in the HTML the server sends: a visitor with scripting unavailable reads the whole site. Route transitions do not repaint the chrome; the header, the rail and the footer persist across navigation. The documentation portal, the glossary and the legal set are rendered ahead of time rather than computed per request. The theme editor and the leaderboard are the only two routes permitted to wait on client code before first paint, and only for their interactive region.

**The two regions that depend on who is looking.** The chrome action pair, which is `Sign in` and `Sign up` when signed out and an avatar control when signed in, and the startup programme application card, which is a prompt and a `Sign in` action when signed out and the application form when signed in. Both resolve after first paint rather than before it, so the page is served identically to everyone and the rest of the site stays cacheable.

**State that lives outside one component.** The SDK selection belongs to the documentation portal and is restored on a return visit. The band belongs to a section rather than a session and is authored rather than stored. The theme draft belongs to the theme editor and lives in the address, never in storage. The cookie choice is site-wide, stored per visitor and withdrawable.

**The console caricatures.** Each is composed from the same pieces as the real component previews, so a value changed in the theme editor is visible in the home route's showcase. A caricature declares its own scroll timeline, and only transform, opacity, shadow, background image, filter and mask geometry may be driven from scroll; nothing that changes the shape of the page may be. Each caricature runs at most one continuously animating element and everything else is entry-only or scroll-driven. A caricature outside the visible region and its margin stops animating. This last one is not optional: the home route carries nineteen animating elements on one clock across a very long scroll, and leaving them all running is what separates a smooth page from a hot laptop.

**API versioning.** The public surface carries its version in the address and an older version keeps answering until it is withdrawn with notice. A field is added without a version change; a field is never removed or repurposed without one.

**Performance.** Largest contentful paint under 2.5 s on a mid-range phone over a slow connection. First contentful paint under 1.8 s under the same conditions. Cumulative layout shift under 0.05 on every route. Interaction to next paint under 200 ms. Total blocking time on a marketing route under 150 ms. Scrolling holds the display's own refresh rate with no frame taking longer than one and a half intervals. The long-document budget applies to the glossary and the legal set, which are long enough that they cannot be drawn all at once: content outside the visible region and one screen of margin is skipped during layout and paint, with a reserved size so the scrollbar does not jump, while staying findable by the browser's own in-page search and reachable by anchor, and with no frame over one and a half display intervals while scrolling at speed. Only transform, opacity, filter and clip-path are animated. An element hints at a change only while it is actually changing and drops the hint afterwards. The layered blur behind the chrome is the single most expensive effect here and exists exactly once, on that strip.

**Fonts and images.** At most five font resources on any route: four weights of the display family and one monospace. The numerals and the script family load only on the routes that use them. Every face declares a swap behaviour so text is readable before the face arrives, and a metric-compatible fallback with explicit size adjustment so the swap shifts nothing; layout shift from a font swap is the largest single contributor to a poor score on a text-heavy site and this site is text-heavy. The script face blocks rather than swaps, because it appears once, in a headline. Every raster carries intrinsic dimensions so its box is reserved before it arrives, and every raster below the fold loads lazily.

**No binary asset ships.** No font file, no photograph, no rendering, no texture, no video. The reference shipped its circuit field partly as raster plates named circuit-lines, circuit-components and circuit-bento, a framework mark as a raster, two large brand renderings, one hundred and twenty-two product screenshots and nine video files. None of them ships here; every asset class is drawn instead. The circuit field is generated vector geometry from a seed fixed per route, so it is identical across a rebuild, which matters because headlines were art-directed against it: lay a lattice at a fixed pitch, walk paths using only horizontal, vertical and 45 degree segments with a rounded elbow at every direction change, place a square or a ring at a fraction of the junctions and a dotted run at a smaller fraction, stroke everything with the rule colour at low alpha and fill the nodes higher. Product screenshots are built as markup rather than generated as images. The two dimensional brand renderings are inline vector plus filters over the flat mark geometry, and each is labelled where it appears as a reconstruction rather than a measurement. Third-party marks are abstract forms derived from the slot's own name string, plausible at low alpha in the trust strip and resembling no real trademark. The dot-matrix ornament is produced from a mark's own outline at build time rather than hand-placed, by rasterising the outline to a coverage grid and emitting a small rounded square per covered cell, tinted and faded from the centre outward, with a cap on the emitted count and a coarser pitch when the cap is exceeded. The brand-asset downloads are served as vector directly from the geometry and as raster by rendering that same vector at request time and caching it; nothing is stored. The overview video is replaced by the console caricature advancing through its three steps on a timed loop in the same frame, with a scrub control and captions, and the chip's stated duration matches the generated sequence's actual length.

**Third-party code.** Analytics loads after first paint, never blocking, and honours the stored consent choice. The bot challenge loads only on the routes that submit something. The embedded component previews load only on the routes that render them and always after the static content. The survey widget is deferred until idle. No third-party script runs before the document is readable, and nothing makes an outbound network call at run time.

**Data scoping.** Every row that belongs to an account carries that account's identifier and every read of such a row is scoped by it where the connection is opened rather than in each statement, so an unscoped read is refused by the store rather than caught in review. The reason is arithmetic: an application-layer check has to be right in every path forever, and a data-layer check has to be right once.

## Data model

Ten tables. All timestamps are UTC. Ids are integers, slugs are kebab-case, money is integer minor units in `usd`.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

### `app_user`

`id`, `email` unique across the product, `password_digest`, `role` in `author` or `reader`, `display_name`, `created_at`.

### `library_entry`

`id`, `kind` in `doc`, `changelog`, `glossary`, `blog` or `legal`, `slug`, `title`, `summary`, `body`, `category_label`, `author_id` referencing `app_user`, `state` in `draft` or `published`, `published_at` which is null until publication, `sdk_scope` which is null or one of the thirty SDK names, `doc_version` in `Core 3`, `Core 2` or `Core 1` for entries of kind `doc`, `created_at`, `updated_at`. At most one entry in state `published` holds any given `kind` and `slug` pair; a draft may hold a pair provisionally and publication is what claims it.

### `entry_asset`

`id`, `entry_id` referencing `library_entry`, `object_key` unique across the product, `content_type`, `byte_size`, `alt_text`, `created_at`. `object_key` always matches `library/{entry_id}/{sha256_of_bytes}.{ext}`. The bytes themselves are in the bucket and in no other place.

### `entry_rendition`

`id`, `entry_id` unique, `address`, `body_text`, `generated_at`. One row exists for every published entry and none for a draft. `body_text` is derived from the entry's own `body` in the same operation that publishes it, and is never edited independently.

### `related_term`

`from_entry_id` and `to_entry_id`, both referencing `library_entry`, plus `term_text`. The pair is the key. Every row is derived by the build from the terms each glossary entry declares. No row points an entry at itself.

### `plan`

`id`, `code` in `hobby`, `pro`, `business` or `enterprise`, `display_name`, `monthly_price_minor` which is null for the custom tier, `annual_price_minor`, `price_display`, `qualifier`, `positioning`, `action_label`, `lead_in`, `sort_order`. `plan_feature` carries `id`, `plan_id`, `group_label`, `label`, `sub_label` which may be null, and `sort_order`. `price_ladder` carries `id`, `plan_id`, `metric` in `mru`, `mro`, `enterprise_connection`, `api_key_creation`, `api_key_verification`, `m2m_token_creation`, `m2m_token_verification`, `dashboard_seat` or `satellite_domain`, plus `band_label`, `unit_price_display`, `included_quantity` and `sort_order`. The plan cards, the feature lists and the comparison matrix all read these three tables and nothing else.

### `leaderboard_result`

`id`, `model_name`, `vendor_name`, `framework` in `Android`, `Next.js`, `iOS` or `React`, `mode` in `Base`, `MCP` or `Skills`, `task_family` which is one of the nine column names, `score_percent` which is null when there is no result, `run_count`, `model_version`, `harness_version`, `corpus_version`, `run_date`. At most one row exists for a given `model_name`, `framework`, `mode` and `task_family`. A null `score_percent` is an absence and is never stored or displayed as a zero.

### `theme`

`id`, `owner_id` which is null for a preset, `name`, `mode` in `light` or `dark`, and seventeen colour columns named `primary`, `background`, `foreground`, `foreground_primary`, `neutral`, `muted`, `foreground_muted`, `ring`, `input`, `input_foreground`, `border`, `shadow`, `modal_backdrop`, `success`, `warning` and `danger`. Four preset rows ship: `Default`, `Dark`, `Simple` and `Library`.

### `application` and `app_instance`

`application` carries `id`, `owner_id` referencing `app_user`, `name`, `slug` which is unique within an owner, and `created_at`. `app_instance` carries `id`, `application_id`, `environment` in `development` or `production`, `state` in `pending`, `provisioning`, `live` or `failed`, `publishable_key` which is unique across the product, and `created_at`. An instance reaches `live` only after passing through `pending` and then `provisioning`. A development instance and a production instance of one application share no users, no keys and no settings.

### `startup_application`, `consent_choice` and `compliance_row`

`startup_application` carries `id`, `applicant_id`, `company_name`, `funding_raised_display`, `launched_within_year`, `state` in `received` or `refused`, and `created_at`. A row in state `refused` stores no company name. `consent_choice` carries `id`, `visitor_token`, `analytics_allowed` and `decided_at`, one row per visitor token. `compliance_row` carries `id`, `requirement`, `status` in `Held`, `Not applicable` or `Not offered`, `detail`, `evidence` and `sort_order`.

### Derived rather than stored

Whether an entry is publicly readable is derived from its `state` together with the caller, and is never a column. A rendition's `body_text` is derived from the entry's `body` at publication and is never edited on its own. Every `related_term` row is derived by the build from the terms each glossary entry declares, and the set is rewritten whole on each build. A leaderboard column mean, and so each cell's band, is computed on read from `score_percent` and is never stored. The price a plan card shows for the selected billing period is computed on read from `monthly_price_minor` and `annual_price_minor`. A theme's twelve derived values are computed from the seventeen stored ones. No count that can be computed from rows is kept in a column of its own.

### Seed data

Three accounts as named in `## User roles`. Library entries, all owned by `author@example.com` unless stated: the three changelog entries, the ten glossary entries carrying 41 related-term declarations between them, the three blog articles, nine legal documents matching the legal index, and fourteen documentation entries, one per top-level sidebar node, all published. Then five drafts: one each of kind `doc`, `changelog`, `glossary` and `blog` owned by `author@example.com`, and one blog draft titled `Rotating a signing key without downtime` owned by `author2@example.com`. One published `doc` entry and one draft `doc` entry both hold the slug `session-management`, which is the seeded conflict the contended publish path meets.

Four plans with their feature lists and ladders exactly as `## Core features` quotes them. Six compliance rows: `SOC 2 Type 2` at `Held` since `May 6, 2022`; `HIPAA` at `Held` since `May 6, 2022`; `GDPR / Data Privacy Framework` at `Held`, self-certified under the EU-U.S. DPF, its UK Extension and the Swiss-U.S. DPF, effective `Feb 22, 2024`; `CCPA` at `Held` with a supplemental notice published; `PCI DSS` at `Not applicable` because Aegis never stores cardholder data; `Regional data residency` at `Not offered`, US-hosted with EU, UK and Swiss data transferred under the DPF. Keep the last two rows. A compliance page listing only what a company holds is an advertisement; one listing what it does not hold, in the same table and the same typography, is evidence.

Four theme presets. Leaderboard results for four models across the nine task families, three modes and four frameworks, including one deliberate null cell so the absence rendering is exercised and one model whose average falls in the bottom decile so the negative cell ground is exercised.

Seeding is idempotent. Restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual detail the routes need. Nothing here restates a rule from `## Core features` or `## UI/UX notes`.

### The chrome

A full-bleed announcement bar at the very top, dark ground on every route regardless of band, white ink, one centred line carrying a truncating message and a link with a play-triangle glyph. Measured copy: `Aegis raises $50m Series C` and `Learn more`. It scrolls away with the page and does not stick.

Beneath it a floating header pill on a raised surface with a hairline ring, sticky from the top of the scroll and offset by the announcement bar's height. Left to right it holds the wordmark lockup, a hairline divider, six navigation items, a flexible gap, then `Sign in` as a quiet link and `Sign up` as the only filled action in the chrome. Five of the six items are disclosure menus and the sixth, `Pricing`, is a plain link. The menus in order are `Products`, `Docs`, `Changelog`, `Company` and `AI`. `Products` contains User Authentication, Enterprise Authentication, Multi-tenancy, Billing, CLI and Agents. `Docs` contains the documentation root plus a framework grid linking eight quickstarts. `Changelog` contains the changelog route. `Company` contains About, Careers, Blog, Contact and Brand assets. `AI` contains Agents, LLM Leaderboard and the agent instruction line.

Behind the pill sits a strip that blurs whatever passes beneath it with a gradient of strength rather than a uniform value, ramping from nothing at the top to full at the bottom with no visible banding, and transparent to the pointer. A stack of masked layers of increasing softness is one way; any method with an equivalent result is acceptable.

Every item in the pill transitions its colour, ground, border, underline, fill, stroke and shadow together, and the recovery is more than twice as long as the response. While any menu is open **the other five items dim** from display ink to quiet ink and recover on the slower leg. That is the detail that makes the bar feel considered rather than assembled.

Five routes carry a second-level rail directly beneath the pill, on a raised ground, separated by a hairline, with radius on the two lower corners only so it reads as an extension of the pill rather than a second object. Items carry a leading glyph; the active one is filled and in display ink, the rest outlined and in quiet ink.

| Route | Left items | Right items |
|---|---|---|
| `/user-authentication` | User Authentication, Enterprise Authentication, Multi-tenancy, Billing | Components, Docs, Waitlist |
| `/multi-tenancy` | the same four | Components, Docs, Watch introduction |
| `/billing` | the same four | Components, Docs |
| `/agents` | Agents | Docs |
| `/components/theme-editor` | Components | UI component docs |

The footer is five columns of links under faint headings at the book weight, then a rule, then a copyright line and a social row.

| Column | Items |
|---|---|
| Product | Authentication, Multi-tenancy, Billing, CLI, Agents |
| SDKs | React, Next.js, Expo, View all |
| Resources | Documentation, Changelog, Glossary, Feature requests, Startups, Students, LLM Leaderboard |
| Company | About, Careers, Blog, Contact, Brand assets |
| Legal | Terms and conditions, Privacy policy, Website terms of use, Security, Legal Resources, Do not sell/share my info, Cookie manager |

The last item in the Legal column is a button that opens the consent manager, not a link. `Do not sell/share my info` is a link to a request form. The copyright line reads `© 2026 Aegis, Inc.`, set as three separate inline elements so the year can be substituted without touching the rest. The social row carries five marks, right-aligned, each lifting from quiet ink to display ink on hover. A `Support` label is present as screen-reader-only text at the end of the footer, attached to the persistent help control: a fixed dark circle at the bottom right carrying the brand mark on a floating shadow, above everything, present on all twenty-seven first-party routes.

### The type scale and the families

Type is carried exactly, because a family is an identity a builder cannot guess and a scale a builder invents is the fastest way to lose a design's character.

Four roles. The display and interface role is one grotesque loaded at 400, 450, 500, 600 and 700. Numerals are tabular lining figures on a single advance width, enabled as a font feature rather than by loading a second family; verify by rendering a counter and checking that the line does not reflow. The monospace role is loaded at 400 and 500 and declares the full fallback chain `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace`. The script role is one weight on one route. The embedded console caricatures declare `ui-sans-serif, system-ui, sans-serif` and load nothing: thirty screens of dense product interface is where a loaded family costs the most and helps the least, and a family break between the site and the caricature is accepted to avoid it.

The three licensed typefaces the reference loaded are replaced by open ones from a public font service, named with their licence. A substitute must preserve all three capabilities: a variable or five-weight grotesque with a true 450, tabular lining numerals, and a monospace with a 500.

Thirteen named steps, each with its own line height, five of them carrying a baked weight and tracking. Where a step inherits, it takes the weight and tracking of its context.

| Step | Size | Line height | Weight | Tracking |
|---|---|---|---|---|
| `--text-2xs` | `0.6875rem` | `1.25rem` | inherit | inherit |
| `--text-xs` | `0.75rem` | `1.25rem` | inherit | inherit |
| `--text-sm` | `0.8125rem` | `1.5rem` | inherit | inherit |
| `--text-base` | `0.9375rem` | `1.75rem` | inherit | inherit |
| `--text-lg` | `1.125rem` | `1.75rem` | inherit | inherit |
| `--text-xl` | `1.25rem` | `1.75rem` | inherit | inherit |
| `--text-2xl` | `1.5rem` | `2rem` | inherit | inherit |
| `--text-3xl` | `2rem` | `2.5rem` | inherit | inherit |
| `--text-4xl` | `2.25rem` | `2.5rem` | `600` | tight |
| `--text-4_5xl` | `2.5rem` | `3rem` | `700` | tighter |
| `--text-5xl` | `3rem` | `3.5rem` | `600` | tight |
| `--text-5_5xl` | `3.5rem` | `4rem` | `700` | tighter |
| `--text-6xl` | `4rem` | `4.5rem` | `700` | tighter |

What is actually rendered, in descending order of use across the site: the reading size at `16px` on `24px` at weight 400 by a very wide margin, then the small size at `13px` on `24px` at 400, then the same at 500, then the body size at `15px` on `28px` at 400, then the book weight at `14px` on `20px`. Read that as the real scale: one body size, one small size in two weights, one reading size, and the book weight appearing where the labels are.

### The module map

The front end divides into twelve modules, which is the shape a reviewer should be able to see in the source without being told:

| Module | Responsibility |
|---|---|
| tokens | the design values as named properties, both bands |
| chrome | announcement bar, header, rail, footer, help control, skip link |
| motion | the curve set, the duration ladder, the named loops, the reduced-motion contract |
| field | the circuit background, the washes, the glows, the bubbles, the squircle |
| primitives | the twenty-two components |
| marketing | hero, band, tile grid, testimonial, trust strip |
| console-preview | the embedded product caricatures and their scroll drivers |
| docs | the portal shell, sidebar tree, SDK selector, search entry |
| longform | changelog, glossary, blog and legal, with the skipped-render behaviour |
| leaderboard | controls, matrix, cell scale |
| theme-editor | canvas, panel, value encoder |
| agent-pill | the copyable instruction and its bubbles |

### Iconography

Every icon is inline vector geometry taking its colour from the text around it, so one ink value recolours the whole set. Nothing is a font glyph and nothing is a raster.

The brand mark is a broken ring around a filled dot: the ring is open at the lower right and its upper arc is drawn at half strength, so the ring reads as one continuous stroke that fades as it comes round. That two-tone treatment must survive every variant, including the monochrome ones, because at small sizes it is the only thing distinguishing the mark from a plain letter. The wordmark lockup is the mark plus five letterform paths.

The chrome set is: a menu disclosure caret, two mobile menu bars, a small chevron and a large chevron, a close cross, a play triangle, a thin check, a check inside a positive chip, an external-link arrow, a user silhouette, a shield with a tick, an information circle, a grid of four squares, a rounded square outline, a sparkle, and an upload arrow.

The copy control is two icons cross-faded in one cell: a pair of overlapping pages at rest with no blur, full alpha and no scale change, and a tick at rest blurred, slightly reduced and at zero alpha. On copy the two states swap. Nothing moves; one shape sharpens in while the other blurs out. Both carry a reduced-motion override that removes the transition entirely.

The band notch is drawn as geometry rather than as a border: a trapezoidal wedge cut out of the boundary, formed from two mirrored corner pieces at either end of a straight filled run, each corner a 45 degree diagonal with a rounded elbow at both ends, filled with the colour of the band it belongs to.

Two decorative stroke sets appear in the diagrams: a vertical fork and a staircase rail, both stroked with the rule colour at low alpha and both animating their dash offset on entry.

Twelve slots hold third-party marks: six coding-agent vendors, eight customer logos in the trust strip, three investor logos, nine framework logos and two card-scheme marks inside the embedded checkout. Every one is a generated placeholder.

Icons are sized in exactly three ways: beside text in a sentence they match the cap height of the line they sit in rather than the font size, so they stay optically aligned at any size in any family with no per-instance tuning; inside a control they are fixed small; as a section ornament they are fixed large.

### The dashed rule and the inline code pill

The dashed rule is a motif on nine routes and it is not a border: it is a hairline drawn as a small repeating tile, one axis at a time, at low alpha, with a mask fading the first and last part of the run to nothing so it never ends in an abrupt stub, and it renders identically at every pixel ratio. A second, coarser variant draws the connector lines in the home route's diagrams and the rectangles that make up the startup programme's layout grid and the brand-asset gallery, which is the only place the dashed rule is used as a layout device rather than as a divider.

Inline code inside body copy is not a coloured box. It is a three-layer background: a vertical gradient painting a hairline rule at the top and bottom of the line box, plus two inline vector caps drawing the rounded left and right ends. The effect is a pill that wraps correctly across a line break, which a border cannot do.

### The code theme

Two complete syntax palettes, one per band, because a code block appears on eleven routes. On a dark band: a near-white neutral foreground, a light cool neutral comment, a near-white soft blue keyword and function, a light, vivid cyan string and interpolation, a light, soft green constant, link and parameter, and a light cool neutral punctuation. On a light band the same roles resolve to a near-black neutral foreground, a mid cool neutral comment and a deep cool neutral punctuation; the keyword, string and constant inks come from the accent and signal families at a darkness that clears 4.5 to 1 against the sunken surface. Those three are a substitution rather than a measurement and are labelled as such.

### The circuit field and ambient surfaces

Three layers back to front: a grid drawn as the dashed rule on both axes at a fixed pitch and low alpha, traces drawn as stroked paths with rounded rectangles at the junctions, and nodes drawn as small squares with a barely-softened corner and rings, at varying alpha. Above the field and below the content sits a single radial wash lifting the centre of the hero and letting the field fall away at the edges, pointer-transparent; on a dark band it is a top-anchored fade into the dark ground computed in a perceptual space.

On four routes a second decorative sheet sits behind the hero at a fixed horizontal skew, with its mirror, translated horizontally as the page scrolls and carrying a gradient at low alpha.

Four glows: a soft halo behind a product icon, a wide halo behind a hero ornament, a card halo behind a hovered card, and an edge bloom behind the terminal frame. Blend modes carry the glows rather than alpha alone.

The bubble is a recurring ornament: a circle carrying an icon, drawn with an inner top highlight rather than a flat fill, its size set per instance and its icon a fixed fraction of it. A larger variant deepens the shadow and a third carries a warm gradient marking one specific vendor slot. Both the ground gradient and the shadow are scrubbed by scroll on the home route.

The squircle chip is used for the command names on the command line route and for the tab tray on the leaderboard. It is not a rounded rectangle: an asymmetric shoulder lets a tab grow out of the panel below it along a continuous curve rather than meeting it at a corner, and the inner fill is the same shape inset slightly with each radius reduced to match.

The hero of the command line route carries a monochrome noise field over an indigo-to-navy gradient, generated as an inline turbulence filter with a fine base frequency, several octaves for tonal variation, and its colour speckle removed, composited at low alpha.

### The components

Twenty-two carry the site, and every route in this brief is an arrangement of them.

**Action.** Four variants. Primary is the accent ground with white ink and the action shadow, at most one per route. Primary on dark inverts to a near-white ground with near-black ink. Secondary is transparent with display ink, gaining a faint ink ground and a border on hover. Quiet has no ground and lifts from quiet ink to display ink, and belongs inside a rail or a footer. Three heights: a chip, a control and a hero action.

**The arrow link.** The most-used interactive element here. Two copies of one triangle occupy the same slot. At rest the first sits after the label at reduced alpha; on hover it travels right and fades away while the second arrives from the left and fades in, so the arrow reads as passing through the label rather than nudging.

**Card.** A raised ground, a soft radius, a hairline ring at rest, the card shadow, and generous padding. On hover the ring strengthens and the ground moves to the hover surface. Three subtypes: a link card whose whole area is the target, a static card carrying a diagram, and a numbered card carrying a monospace ordinal in its top left.

**Code block.** A sunken ground, a hairline ring, an optional header row carrying a package-manager tab set and a copy control, and monospace content at the small size. The tab set on the command line route reads `npm`, `bun`, `pnpm`, `yarn`, `Homebrew`, `curl`, drawn as squircle chips.

**Terminal frame.** A dark panel with a title bar carrying three dots and a path, then a monospace body using a box-drawing gutter of `┌`, `│` and `└` and a status glyph of `◇` for a step in progress and `✓` for a completed one. The cursor is a filled block that blinks.

**Product screenshot frame.** A browser chrome caricature: three dots at the left, a pill carrying a hostname, and a content area built from real markup rather than an image, which is what allows its interior to respond to scroll.

**Accordion.** Rows at the small size in the medium weight with a leading ring glyph that fills when open and a trailing chevron that rotates half a turn. The body expands to its own natural height with the opacity following.

**Disclosure menu.** A trigger button and a panel carrying the floating shadow, a soft radius and a backdrop blur.

**Select.** A button showing the current value, a chevron and a listbox, built over an accessible listbox with a native control retained beneath for form semantics.

**Toggle group.** Two or three segments in a track with an indicator that springs between them, overshooting slightly and settling. Used for `Monthly` and `Annual`, for `Light mode` and `Dark mode`, and for `Base`, `MCP` and `Skills`.

**Status chip.** An inline pill with a signal ground at low alpha, matching ink, a small radius and the smallest size in the medium weight.

**Eyebrow.** A small label in the medium weight in the accent, sitting above a section headline with a small gap beneath, stepping to a paler accent on dark bands. It appears above every major section on every marketing route and is the site's main structural signal.

**Section headline block.** Eyebrow, headline, a body paragraph in body ink at a constrained measure, then optionally an arrow link. Centred on the home route, left-aligned on product routes.

**Trust strip.** A full-width row of customer marks separated by vertical hairlines, with a caption in the first cell at the book weight. Marks sit back at low alpha and lift to full on hover; four cells at desktop and two at phone. That alpha is below any text threshold and is acceptable only because the marks are decorative and each carries an accessible name.

**Testimonial.** A quotation glyph, a quote in body ink, then an avatar, a name, a role and an organisation. Two layouts: a wide single quote, and a masonry column of short social posts each carrying body text, an avatar, a display name and a handle.

**Feature tile.** A card whose upper two thirds is a diagram and whose lower third is a heading and a body at the small size. Three across at desktop and one at phone, and tiles are deliberately unequal in height: a tall diagram pushes its tile taller rather than being cropped.

**Comparison table.** A sticky header row, hairline rows, a first column left-aligned in the medium weight and the rest centred, and rows that may carry a nested sub-row at the smallest size in quiet ink for a qualifier such as an overage price.

**Definition entry.** An anchor target, a heading, a permalink glyph appearing on hover, a body, and a `Related terms` list of chips.

**Timeline entry.** A left gutter carrying a date at the book weight and a node dot on a vertical rule, then a category chip, a title, a summary, a body and a contributor list.

**Alphabet rail.** A sticky horizontal row of twenty-six letters.

**The agent prompt pill.** The most repeated component here, appearing on eight route heroes. A tab carrying a row of overlapping vendor bubbles and the label `Build with agents`, drawn with the squircle geometry so it grows out of the body, and a body carrying a chevron glyph, the monospace string `Add Aegis auth to my app: <SITE_ORIGIN>/SKILL.md` where `<SITE_ORIGIN>` is this app's own public origin, and the copy control. The string is duplicated as screen-reader-only text. There is no button in the home hero at all: the primary action is a copyable string, and that is this site's most important single decision.

**Video chip.** A pill above a hero carrying a play glyph, a label and a duration in a lighter weight, for example `Watch Multi-tenancy overview` and `1 min`.

### Route: home

Seven bands down one scroll, alternating ground: light for the hero and the trust strip, light for the component showcase, dark for user authentication, light for multi-tenancy, light for billing, dark for frameworks and integrations, light for testimonials and the footer. Four light-to-dark boundaries, each carrying the notch, both halves present.

The hero sits on the circuit field with the light wash and three rings. Headline `More than authentication, Complete User Management`, centred, balanced wrapping, at a constrained measure. Body `Need more than sign-in? Aegis gives you full stack auth and user management - so you can launch faster, scale easier, and stay focused on building your business.` Then the agent prompt pill.

The trust strip runs full-bleed immediately after, four cells separated by vertical hairlines. The first cell reads `Trusted by fast-growing companies around the world.` The rest carry eight customer marks, two rows of four at desktop and four rows of two at phone.

The component showcase is the most intricate composition on the route. Left column: the eyebrow `Aegis Components`, the headline `Pixel-perfect UIs, embedded in minutes`, the body `Drop-in UI components for authentication, profile management, organization management, and billing. Match to your brand with any CSS library, then deploy to your own domain.`, the arrow link `Explore all components`, then a three-row accordion whose labels are monospace with wide tracking:

| Row | Body | Component chips |
|---|---|---|
| `USER AUTHENTICATION` | `Add user <SignUp/> and <SignIn/>, provide account access through a dropdown menu, and manage profile and security settings.` | `<SignUp />`, `<SignIn />`, `<UserButton />`, `<UserProfile />`, `<Waitlist />` |
| `MULTI-TENANCY` | `Allow your users to create new organizations, switch between accounts, manage settings and billing, and view memberships and invitations.` | `<CreateOrganization />`, `<OrganizationSwitcher />`, `<OrganizationProfile />`, `<OrganizationList />` |
| `BILLING` | `Display pricing plans with feature comparisons and subscription options to help your users choose the right plan for their needs.` | `<PricingTable />` |

Right column: a stack of live component previews on one shared clock. The selected chip drives which preview is frontmost; the others recede, blur and fade back. Every preview is built from real markup, never an image, because parts of them respond to scroll and because they double as the specification for the theme editor's canvas. The measured previews include a complete sign-up card carrying `Create your account`, `Welcome! Please fill in the details to get started.`, `Continue with Google`, `Continue with GitHub`, a `Last used` badge, an `or` divider, `Email address` with the placeholder `Enter your email address`, `Password` with `Enter your password`, a `Continue` action, `Already have an account?` with `Sign in`, and a `Secured by Aegis` footer; a user menu carrying two accounts, `Add account` and `Sign out of all accounts`; a profile panel carrying `Account`, `Manage your account info.`, `Profile`, `Security`, `Billing`, `API keys`, `Profile details`, `Update profile`, `Email Addresses`, `Add email address`, `Phone number`, `Add phone number`, `Connected accounts` and `Connect account`; an organization creation form carrying `Create Organization`, `Logo`, `Upload`, `Recommended size 1:1, up to 10MB.`, `Name`, `Organization name`, `Slug URL`, `my-org` and `Create organization`; an organization profile panel carrying `Organization`, `Manage your organization`, `General`, `Members`, `Billing`, `Security`, `API keys`, `General details`, `Organization profile`, `Verified domains`, `Add domain`, `Allow users to join the organization automatically or request to join based on a verified email domain.`, `Leave organization` and `Delete organization`; a pricing card; a session device row carrying `Device`, `Browser`, `Location` and `Sign out of device`; and a waitlist card carrying `Join the waitlist`, `Enter your email address and we'll let you know when your spot is ready.`, `Already have access?` and its success state `Thanks for joining the waitlist` with `We'll be in touch when your spot is ready`.

Three feature tile grids follow, one per product band, three columns at desktop.

The user authentication band carries the eyebrow `User authentication`, the headline `Everything you need for authentication`, the body `Ever feel like authentication requirements change with the season? Aegis keeps up with the latest trends and security best practices.` and the arrow link `Explore user authentication`. Its tiles, with their measured copy: `Multifactor Authentication`, `Each user's self-serve multifactor settings are enforced automatically during sign-in.`; `Session Management`, `Aegis manages the full session lifecycle, including critical security functionality like active device monitoring and session revocation.`; `Email and SMS one-time passcodes`, `Fast and reliable one-time passcode delivery with built-in brute force prevention.`; `Fraud and Abuse Prevention`, `Reduce fraudulent sign-ups and free trial abuse by blocking high-risk disposable email domains and restricting the use of email subaddresses with the "+" separator.`; `Magic Links`, `Improve sign-up conversion rates and filter out spam/fraud with Magic Links.`; `Social Sign-On`, `Add high-conversion Social Sign-on (SSO) to your application in minutes. 20+ options and growing.`; `Advanced security`, `Aegis is SOC 2 type 2 compliant and CCPA compliant. We conduct regular third-party audits and penetration tests.`; `Bot Detection`, `Dramatically reduce fraudulent sign-ups with built-in, continually updated machine learning.`; `Passwords`, `Simple and secure password authentication, complete with breach detection and recovery options.`; `API Keys`, `Give every user secure, production-ready API keys without building any of the underlying infrastructure yourself.`; and `Aegis CLI`, `Empower your AI agents to set up Aegis with the CLI.`

The multi-tenancy band carries the eyebrow `Multi-tenancy`, the headline `Everything your B2B SaaS needs`, the body `Aegis has all the features you need to onboard and manage the users and organizations of your multi-tenant SaaS application.` and the arrow link `Explore Multi-tenancy`. Its tiles: `Custom roles and permissions`, `Powerful primitives to fully customize your app's authorization story.`; `Organization UI Components`, `Aegis's UI components add turn-key simplicity to complex Organization management tasks.`; `Auto-join`, `Let your users discover and join organizations based on their email domain.`; `Invitations`, `Fuel your application's growth by making it simple for your customers to invite their team.`; plus two diagram-only tiles.

The billing band carries the eyebrow `Billing`, the headline `Subscription billing, without the headache`, the body `Add subscriptions to your B2C or B2B application without having to write payment code, custom UI, or wrangle webhooks. Just drop in React components and start capturing recurring revenue.`, the lead-in `Here's what you can do out of the box:`, three checked outcome lines reading `Define and manage plans`, `Unify user and subscription data` and `Gate access to content`, and the arrow link `Explore Billing features`.

The frameworks and integrations band is two centred columns followed by a logo grid of two blocks, each cell a hairline-bounded square holding a framework mark stroked rather than filled at low alpha. The first column: eyebrow `Frameworks`, headline `Build with SDKs for modern frameworks`, body `Aegis keeps developer experience front-and-center by providing helpful SDKs for most modern frameworks on web and mobile.`, link `All frameworks`. The second: eyebrow `Integrations`, headline `Integrate with the tools you love`, body `Leverage Aegis as the source of truth for your user data and integrate with the tools that you already depend on.`, link `All integrations`.

The testimonial band carries `Trusted around the world` and `Join the customers and champions who trust Aegis. Free for your first 50,000 monthly retained users and 100 monthly retained orgs.`, then a wide pull quote on the left with an avatar, name, role and organisation, a masonry column of nine short social posts on the right, and a second copy of the agent prompt pill.

Only three things move as the page scrolls: the background field, the diagrams, and the shadows. No text moves and no headline scrubs; the restraint is deliberate. At phone width the diagrams stack and each becomes individually scroll-driven, which is why there is roughly four times as much movement there.

### Route: user authentication

Headline `The easiest way to build user authentication`, body `Increase conversions, secure users, and easily manage your authentication flow. All out-of-the-box.`, the agent prompt pill beneath, the circuit field behind with the light wash.

An assurance strip of four hairline-separated cells sits immediately below the hero, each a glyph, a heading and a body: `SOC 2`, `Your customer data is protected to the highest security and compliance standards.`; `HIPAA`, `HIPAA-compliant for safely storing your most sensitive user data.`; `Brute force detection`, `Aegis automatically detects and blocks brute force attacks, so you don't have to.`; `Password leak protection`, `Set password rules and detect leaked passwords with a public breach corpus.`

Then the component walkthrough: headline `Pixel-perfect UIs, embedded in minutes`, body `Start shipping customizable components built for modern frontend frameworks.`, then five rows, each a monospace component name, a sentence built by interleaving prose with inline code pills, and an arrow link.

| Component | Sentence |
|---|---|
| `<SignUp/>` | `The <SignUp/> component provides a fast, simple, and secure experience that converts visitors into users.` |
| `<SignIn/>` | `<SignIn/> centralizes every authentication flow - from the basics of passwords and Google SSO, to the complexities of multi-factor, passkeys, and enterprise SSO.` |
| `<Waitlist/>` | `The <Waitlist/> component collects interest before launch, capturing sign-ups and managing early access without building forms or backend logic.` |
| `<UserButton/>` | `The <UserButton/> component displays the signed-in user's avatar and opens a menu for account management and sign out.` |
| `<UserProfile/>` | `The <UserProfile/> component provides a full profile management experience for users to update their account details and security settings.` |

Beside them a live sign-up card types its email field in character by character, then fills the password field, then presses the action, and loops. It is the only continuously running animation on the route; everything else is entry-only.

The single sign-on section: headline `Add high-conversion Social SSO to your application`, a sentence with its statistic emphasised, `When available, 53% of users choose to sign in with SSO instead of the alternatives.`, a provider button demonstration carrying `Sign in with` and a rotating provider name, then four cells: `Convert faster with SSO`, `Social SSO averages 1.3 times faster than passwords, and 5.2 times faster than magic links.`; `One-click integration`, `Aegis handles the edge cases of SSO, so users get instant access.`; `Pick your providers`, `Aegis supports a growing range of Social SSO providers. If you need one that's not listed, ask here.`; `Automatic account linking`, `If a user signs in with SSO after creating their account a different way, their accounts are automatically linked.`

The multi-factor section: headline `Stop 99.9% of account takeovers`, body `Keep your users safe with a range of MFA options.`, four cells reading `SMS Passcodes`, `Authenticator apps (TOTP)`, `Hardware keys` and `Recovery codes`. The passwordless section: headline `Convert your users to your product in seconds`, body `Eliminate forgotten passwords and credential stuffing attacks.`, four cells reading `Social SSO`, `Magic Links`, `One-time passwords` and `Passkeys`.

### Route: multi-tenancy

The rail carries `Watch introduction` in its right group and a video chip sits above the headline reading `Watch Multi-tenancy overview` and `1 min`. Headline `One user. Multiple teams.` Body `Manage organizations, invite teammates, and assign roles and permissions with RBAC - all compatible with Enterprise Authentication out of the box.` Agent prompt pill beneath.

The three-step demonstration is an embedded browser frame carrying the hostname pill `acme.app`, an organization switcher showing `Acme Corp`, and a skeleton application beneath. Beside it three numbered steps, each a monospace ordinal, a heading and a body: `Organization creation made easy`, `Aegis detects the user's email domain and prefills their organization name and logo.`; `Built-in invitations`, `Users can invite team members manually or auto-recognize them by email.`; `RBAC out-of-the-box`, `Users can be assigned to any role with permissions defined for the organization.` The frame's contents change as each step becomes active, and the switcher opens to reveal `Brightside AI` with the role `Admin`, then `Acme Corp`, `Cameron Design Studio` and `Create Organization`.

The enterprise connection section: headline `Self-serve enterprise setup`, body `When a customer needs SSO, their IT admin sets it up themselves - choosing their identity provider and activating the connection without a ticket to your team. The connection attaches to their organization, with members, roles, and invitations already in place.`, arrow link `Explore Enterprise Authentication`. It is the boldest claim the site makes and here it is copy, not behaviour.

The console section: headline `Do more with your dashboard`, with the first three words emphasised against the rest of `Configure and grow every organization from the Aegis dashboard - profiles, settings, roles, and the revenue each one drives.` Four checked outcomes read `Manage organization profiles`, `Configure settings and membership`, `Set roles and permissions` and `Track revenue and growth`. Beside them an embedded console frame carrying a hostname pill of `dashboard.aegis.dev/organizations/brightside` and a complete console caricature: an application switcher reading `Acme` with a `Pro` chip, an environment chip reading `Production`, an `Invite` action, an avatar, a left rail of `Overview`, `Users`, `Organizations`, `Billing`, `Logs` and `Configure`, and a detail pane with tabs `Profile`, `Members`, `Invitations`, `Subscriptions`, `Payments` and `Settings`. The detail pane carries a contribution heatmap headed `Member activity` and `Sign-ins and actions by members this year`, a year selector and a seven-row day grid whose cells are scroll-driven, plus two header controls reading `Show JSON` and `Actions`.

This route carries more hover-sensitive elements than any other: every console rail item, every tab and both header controls.

### Route: billing

Headline `Subscription billing, without the headache`. Body `Aegis Billing is the easiest way to implement subscriptions for B2C and B2B applications. No payment integration code to write, no UI work, nothing to keep in sync. Simply drop-in React components and start capturing recurring revenue.` Agent prompt pill beneath.

Plan definition section: headline `Define and manage plans directly in Aegis`, body with an inline code pill reading `Set up plans in Aegis's dashboard, create a pricing page with the <PricingTable /> component, and let customers manage their subscriptions through Aegis's profile components.`

The embedded commerce demonstration is a three-state walkthrough inside one browser frame with the hostname `acme.app`. **The three states are one component in three phases, not three components:** the frame does not change size between them and the panel cross-fades in place, which is what makes the sequence read as a single flow.

State one is a pricing table headed `Tailor made pricing from Acme, Inc` with the subtitle `Free 14-day trial, no credit card required.` and two plan cards. `Starter`: `For personal use`, `$9`, `/mo`, `Billed annually`, then `Unlimited projects`, `Mobile app integration`, `Standard templates`, `Basic analytics`, `Weekly backups`, `Email support`, and the action `Start 14-day trial`. `Pro`: `For professionals`, `$19`, `/mo`, `Billed annually`, `Everything in Starter and:`, then `Custom branding`, `Collaboration tools`, `Advanced analytics`, `AI assistant`, `Daily backups`, `24/7 priority support`, and the same action.

State two is a checkout panel carrying `Checkout`, `Starter plan`, `Free trial`, `Billed annually`, `$9.00`, `per month`, `Subtotal $9.00`, `Total Due after trial ends in 14 days $9.00`, `Total Due Today USD $0.00`, an express action `Secure, 1-click checkout with Link`, then a card form with `Card number` placeholder `1234 1234 1234 1234`, `Expiration date` placeholder `MM / YY`, `Security code` placeholder `CVC`, `Country` defaulting to `United States`, `Postal code` placeholder `12345`, the mandate sentence `By providing your card information, you allow Acme to charge your card for future payments in accordance with their terms.`, and the action `Start free trial`. Two card-scheme marks appear in the form as generated placeholders. Nothing here is a real payment surface: no card is accepted, no charge is made, no card details are stored anywhere.

State three is a confirmation carrying `Free trial successfully started!`, `Your new subscription is all set.`, `Total paid $0.00`, `Trial ends on Nov 12, 2026`, `Payment method Visa ⋯ 4242` and the action `Continue`.

The unified data section: headline `Access user and subscription data in one place`, body `Aegis automatically updates and stores your customer's subscription status alongside their user data, eliminating the need for complex synchronization code and the ongoing maintenance it requires.` Beside it two panels side by side: a subscription card showing `Starter`, an `Active` chip, `$9`, `/ month`, `Billed annually` and eight entitlement lines, and a user record showing `User`, a person name, `Email address`, a monospace `User ID` and `Joined August 5, 2024`. The pairing is the argument: one record, two faces.

### Route: framework landing pages

One template, three fills, at `/react-authentication`, `/nextjs-authentication` and `/expo-authentication`. These are the only routes that open dark and stay dark through the hero. The eyebrow is the framework name in monospace with wide tracking inside a hairline chip. The headline is `Authentication optimized for <FRAMEWORK>`. The body is one sentence naming that framework's own idioms. The action is the agent prompt pill. The ornament is the framework mark rendered as a dot matrix in the informational cyan, right-aligned, large, at low alpha, generated from the mark's own outline at build time so substituting a mark substitutes the ornament. The trust strip reads `Trusted by fast-growing companies around the world` over seven marks in one row.

The React fill reads `Authentication optimized for React` with the body `Implement authentication and user management the React way - with hooks and components.` The Next.js fill carries the page title `Next.js Authentication - Best Auth Middleware for your Next app!` The Expo fill reads `Expo Authentication`. The last two bodies were not fully captured and are yours to write in the same register.

Below the hero each runs, in order: a `UI BUILDING BLOCKS` eyebrow and a component grid, a framework-idiomatic code sample, a feature tile grid, a testimonial, and a closing action band. The code sample is the only part that differs materially between the three. These routes are deliberately long. They exist to be found by somebody searching for exactly this combination, and length is what makes them findable. Do not shorten them.

### Route: agents

Dark from top to bottom. Headline `Ship auth faster with agents`, where the word `with` is followed inline by five overlapping vendor bubbles and then the word `agents`, revealing character by character. Body `Point your agent at Aegis. It does the rest.` Agent prompt pill beneath. Arrow link `Or follow a step-by-step guide for your agent`.

Then the heading `Agents` over six cards, three across at desktop, each a bubble, a product name, a vendor name in quiet ink, a body and a `View Guide` arrow link. Their bodies read: `Hand <AGENT_1> the Aegis docs and it scaffolds sign-in, sessions, and orgs.`; `<AGENT_2> reads the Aegis docs and wires auth straight into your app.`; `<AGENT_3>'s agent pulls in Aegis to add sign-in without leaving the editor.`; `<AGENT_4> wires up Aegis auth and user management as you build.`; `The assistant in <AGENT_5> connects to the Aegis tool server to scaffold auth.`; `<AGENT_6> takes the Aegis docs and builds the whole integration end to end.`

The primitives section: headline `Start with the components or build directly with the primitives`, body `The same API endpoints, without the prebuilt UI.`, arrow link `See how Aegis works`, then four numbered rows at a narrow measure reading `Review the routes, proxy code, and components your agent proposes.`; `Build custom sign-in and sign-up flows with Aegis APIs or supported SDK hooks.`; `Define Roles and Permissions, then enforce authorization checks in application code.`; `Add custom session claims that your backend reads.`

The route closes with the headline `Compare how different models work with Aegis`, the arrow link `View full leaderboard`, and a truncated copy of the leaderboard showing the top rows only. Its framework select, provider select and mode toggle all function here. The embedded copy and the full route share one component and one data source; two copies drift apart within a month.

### Route: command line interface

The only route with its own header and the only one that drops the marketing chrome entirely: no pill, no menus, no announcement bar, just the wordmark at the left and three quiet links at the right reading `agents.txt`, `docs` and `github`. Dark end to end. This is a deliberate register change addressed to a developer already at a terminal, and it is preserved.

Headline `Put your agent in control.` across two lines, the first revealing character by character with its leading letter arriving separately and the second arriving as a block. Body `Ask your agent to use the Aegis CLI to add auth to your app. No need to leave your terminal or copy and paste API keys.` Then an install block: a six-tab row reading `npm`, `bun`, `pnpm`, `yarn`, `Homebrew`, `curl` in squircle chips, and a body showing `npm install -g aegis` with the package manager in the pale accent, the subcommand in default ink and the package name in the medium weight. Below it the line `or read the docs` with `docs` underlined.

Below the hero a full-width panel carries the indigo-to-navy gradient and its grain, with a terminal frame floating at its centre carrying the login flow:

```
steve@MacBook-Pro taskflow-web % aegis login
┌  aegis auth login
◇  Checking session
│  Waiting for authentication (timeout in 2m)...
◇  Completing authentication
│
│  Logged in as steve@aegis.dev
└  Done
steve@MacBook-Pro taskflow-web % aegis
```

The command reference carries the eyebrow `Developers` and the headline `Set up and manage authentication from your terminal.` Left column: six rows, each a squircle chip carrying a monospace command and a body beneath, the active row in a hairline box and the rest bare.

| Command | Body |
|---|---|
| `aegis init` | `Start in the repo you already have. Aegis detects the framework, links an app, and adds the auth files your project needs.` |
| `aegis config` | `Manage your settings from code.` |
| `aegis webhooks listen` | `Relay webhook deliveries to your local handler and verify their signatures offline, with no public tunnel service.` |
| `aegis impersonate` | `Create a short-lived sign-in URL to reproduce and debug a specific user session, stamped with your account.` |
| `aegis deploy` | `Ship your auth to production from the CLI. Aegis helps you set up your domain, OAuth providers, and DNS records with confidence.` |
| `aegis mcp install` | `Connect the Aegis tool server to your AI clients in one command, so your agent works with up-to-date Aegis SDK snippets.` |

Right column: a terminal frame with a six-tab header matching the six commands, the selected tab rendering that command's transcript. The `init` transcript reads:

```
$ aegis init
◇  Detecting framework
◇  Logging in if needed
◇  Linking this repo to a Aegis application
◇  Installing the right Aegis package
✓  Aegis has been set up in your project
```

The agent section carries the eyebrow `Agents`, the headline `Let your agent handle the setup.` and a terminal frame showing an agent prompt: a path, a chevron, the truncated instruction `Use Aegis CLI to add auth to this Next.js app`, and the hint line `? for shortcuts`. Then the headline `From prompt to production` over the body `Give your agent everything it needs to set up authentication, automate tenant onboarding with the Aegis API, and carry your app all the way to production handoff.`, followed by six labelled stages: `Tell your agent what to build`, `Configure authentication`, `Set up organizations`, `Onboard the first customer`, `Test webhooks locally` and `Go live with confidence`. The first carries the body `Instruct your agent to use the Aegis CLI. Bring in an existing project or start fresh.`

The closing band reads `One CLI for agents and developers.` in display ink over `Purpose-built for developers using AI to ship fast and securely.` in quiet ink, repeats the six-tab install block, then offers `or read the CLI announcement`, then the standard footer.

### Route: pricing

Dark from top to bottom. Headline `Plans for every stage`, body `Clear pricing that scales. Every plan supports unlimited applications.`, circuit field behind with the dark wash.

Feature lists, quoted. `Hobby`: `Up to 3 dashboard seats`; `Unlimited applications`; `50,000 MRU limit per app`; `Up to 5 user impersonations`; `APIs and prebuilt UIs for sign-up, sign-in, and user profile` with the sub-line `+ most authentication features`; `Custom domain`; `Fixed, 7 day session lifetime`; `Application Logs` with `1 day retention`; `Machine Authentication`; `API Keys & M2M Tokens` with `limit per month`; closing with a `Show limitations` disclosure. `Pro`: `50,000 MRU included per app` with `Additional $0.02/mo each` and a `Show volume discounts` disclosure; `1 Enterprise connection included` with `Additional $75/mo each` and its own volume disclosure; `Remove Aegis branding`; `Multi-factor authentication (MFA)`; `Satellite domains` with `Additional $10/mo each`; `Custom session lifetime`; `Application Logs` with `7 day retention`; `SMS Authentication available`; `Machine Authentication`; `API Keys & M2M Tokens` with `included per month + extra` and a `Show pricing details` disclosure. `Business`: `10 dashboard seats included` with `Additional $20/mo each`; `SOC2 Report`; `Enhanced dashboard roles`; `Priority support`; `Application and Admin Logs` with `30 day retention`. `Enterprise`: `Annual committed use discounts`; `99.99% Uptime SLA`; `Enterprise SSO for workspace`; `Premium support SLA + dedicated slack channel`; `Application and Admin Logs` with `Custom retention`; `Log sink destinations` with `Stream logs to your SIEM`; `HIPAA compliance available with BAA`; `Onboarding & migration support`; `Custom security questionnaires`.

The add-on section carries the eyebrow `Add-ons`, the headline `More than authentication`, and the bodies `B2B Authentication, Billing, and Administration. Included in all plans.` and `Add-ons apply to all of your applications.` Then `B2B Authentication`, `The easy solution to multi-tenancy with a full suite of B2B SaaS features.`, action `Start now`, over two levels: `Included`, `Free in all plans`, carrying `100 MRO included per app`, `Up to 20 members per Organization`, `Includes Admin & Member roles`, `Custom permissions` and `Invitations`; and `Enhanced add-on` at `$100 /mo` or `$85 /mo billed annually`, carrying a raised MRO allowance and the enhanced feature set.

The comparison matrix groups its rows under section headings, of which `Machine Authentication` and `Security features` are captured, and each column header carries a `Get started` action.

The `Hobby` card is the only one with a filled action and the only one with an accent glow behind it.

### Route: documentation shell

Three columns at desktop: a fixed-width sidebar, a content column and a table-of-contents column. The sidebar and the header are fixed and only the content column scrolls.

The landing content carries the headline `Welcome to Aegis Docs` and the body, with two inline links, `Aegis provides full-stack authentication and user management with products such as Organizations, Billing, and more. Have your agent use Aegis's CLI and Skills to get started, or explore the resources below.`, then the agent prompt pill. Then a four-card row reading `Quickstarts & Tutorials`, `UI Components`, `SDK Reference` and `Customizing Aegis`, each a glyph, a title and a body. Then `Explore by feature`, a two-column list of `Authentication`, `User management`, `Organizations` and `Billing`. Then a framework grid split into two headed groups, the second being `Build with community-maintained SDKs`, whose entries share the phrasing `Visit the community-maintained ... to learn how to integrate Aegis into your ... application.` Marks are full colour here, unlike the stroked low-alpha marks on the home route. Then `Beyond the basics`, a two-column list carrying `Securing your application`, `Enhance the security of your application with access control, authorization checks, session options, MFA, password policies, bot protection, and compliance tools.` and `Database integrations`, `Enable Aegis-managed users to authenticate and interact directly with your database with Aegis's integrations.`

The search field carries the placeholder `Search documentation`, a keyboard hint chip showing the platform modifier and `K`, and the screen-reader label `Search documentation`.

At phone width the sidebar becomes a sheet behind a control, the version select moves into it, and the search field collapses to a glyph.

### Route: changelog

A screen-reader-only heading, then a right-aligned `Subscribe to RSS` link carrying a feed glyph, then the timeline. It is the only route where a three-level heading hierarchy appears inside prose; lists use a hanging marker in faint ink, inline code uses the pill, and a zero-width joiner after a bolded run keeps a following punctuation mark from being pulled onto the next line.

The three seeded entries carry their bodies in full. `Customize the reverification window`, summary `Control how recently users must have authenticated before performing sensitive actions.`, body `You can now customize how long a successful sign-in or reverification remains valid for Aegis-protected sensitive actions. Set the reverification window between 1 and 10 minutes. The default remains 10 minutes.` and `A shorter window can prompt users to verify their credentials more often before actions such as changing a password, adding and removing an email address, revoking a session, or deleting an account.` and `To configure the window, open the Sessions page in the Aegis Dashboard. Under Session lifetime, set Reverification window to the number of minutes you want, between 1 and 10.` and `This setting applies to sensitive actions protected by Aegis. For sensitive actions unique to your application, define the required window in your application. See the reverification guide for details.`

`Audit Dashboard activity with Admin Logs`, summary `An audit trail of admin actions across your workspace`, body `The Aegis Dashboard now has Admin Logs: an audit trail of the configuration changes made across your workspace - from the Dashboard, the Backend API, or the Platform API. Admin Logs track actions like creating OAuth applications, updating instance settings, rotating secrets, and managing Roles and Permissions, and more.`, then the sub-heading `Filtering and search` over `The logs page shows a reverse-chronological feed of events. Each entry lists a description of what happened, the application it happened in (when applicable), the originating IP address with a country flag (when available), and the timestamp. Select any entry to see its full details.` and `You can narrow the feed with filters:` over `Event type - Filter by event type. Supports trailing wildcards.`, `Instance - Filter by the instance the action targeted.`, `Application - Filter by the application the action targeted.`, `Actor - Filter by the actor that triggered the event.`, `IP address - Filter by the IP address the action originated from.`, `Time range - Scope results to a specific time window.`, then `Get started` over `Admin Logs are available on the Business and Enterprise plans - see the pricing page for details.`, then `Going forward` over `Admin Logs join Application Logs and Email Logs in Aegis's ongoing observability work.`

`Custom OAuth scopes`, summary `Give MCP clients precise, discoverable access to your API with custom OAuth scopes.`, body `Aegis now gives you finer control over the access that MCP clients can request from your API. Define custom OAuth scopes in the Aegis Dashboard to match the actions and resources your API supports.` and `For example: messages:read, tools:execute, resources/files:read, mcp_all` and `Assign only the scopes that each OAuth application needs. Separately, choose which scopes to advertise through Aegis's OAuth metadata so MCP clients can discover what your application supports.` and `Open the Scopes tab on the OAuth applications page to get started.` and `To enforce scopes in your API, verify each OAuth access token and check its granted scopes.`

### Route: glossary

Headline `Glossary`, body `Learn the key terms and concepts in authentication and user management.` Then the alphabet rail, then a section heading per letter with a full-width rule beneath, then the entries. Two columns at desktop: the definition body on the left at a reading measure, a `Related terms` block on the right at a narrow measure carrying a heading and a set of chips. At phone width the related terms sit beneath the body.

The definitions are technically precise rather than marketing copy, and the ten seeded entries carry their full text.

`Access Control List (ACL)`: `An access control list (ACL) is a resource-scoped policy that lists which principals (users, groups, service accounts) have which permissions on that resource. Each access control entry (ACE) grants or denies a verb such as read, write, execute or delete, optionally with inheritance. At request time, the system resolves the caller and evaluates ACEs in a defined order with default-deny. ACLs are fine-grained but resource-scoped and hard to audit at scale, which is why most systems layer RBAC or ABAC above them.` Related: `Role Based Access Control (RBAC)`, `Custom Permissions`, `Authorization`, `Custom Roles`.

`Access Token`: `An Access Token is a credential used to access protected resources in an API, typically issued by an authorization server and used in OAuth and OpenID Connect protocols.` Related: `API Key`, `OAuth`, `JSON Web Token`, `Authentication`.

`Account Linking`: `Account Linking is the process of connecting multiple user accounts from different services or platforms, allowing users to access various services with a single set of credentials.` Related: `Single Sign-On (SSO)`, `User Management`, `User Profile`, `OAuth`.

`Account Portal`: `An Account Portal is a user interface that allows users to manage their account settings, personal information, and preferences within an application.` Related: `User Management`, `User Profile`, `Authentication`, `Single Sign-On (SSO)`, `User Experience`.

`Account Protection`: `Account protection encompasses the security measures and strategies used to prevent unauthorized access to user accounts, including multi-factor authentication, bot detection, brute force prevention and more.` Related: `Multi-factor Authentication (MFA)`, `Account Recovery`, `Account Takeover`, `Brute Force Detection`, `Bot Detection`, `Credential Stuffing`.

`Account Recovery`: `Account recovery refers to controlled verification flows that let a legitimate user regain access to their account when primary factors are lost or unavailable, typically via OTP, email link, or recovery codes.` Related: `Email Links`, `One-Time Passcodes (Email / SMS)`, `Recovery Codes`, `Passkeys`.

`Account Security`: an entry under the same letter, with its own related terms.

`Authentication Context`: `In Aegis, authentication context includes session information like user ID, organization, and factor verification freshness. The fva (factor verification age) array tracks how long since each factor was verified. Aegis supports reverification policies (strict, moderate, lax) to require re-authentication before sensitive actions based on time since last verification. Note: Aegis uses proprietary claims instead of standard OIDC amr / acr / auth_time or SAML AuthnContextClassRef.` Related: `Authentication`, `Multi-factor Authentication (MFA)`, `Session`, `Authorization Code Flow`. That entry is a specification rather than a definition, and stating a proprietary choice in public is the kind of detail that tells an engineer whether to trust the rest.

`Authentication Methods`: `Authentication methods are the factors and protocols used to verify a user's identity. They fall into five categories: knowledge ("something you know" - passwords, security questions), possession ("something you have" - passcodes, hardware keys), inherence ("something you are" - biometrics), location, and behavior. Modern apps combine methods (MFA) for stronger security. Aegis supports passwords, passkeys, OAuth, magic links, SMS, TOTP, and biometrics in a single auth flow.` Related: `Multi-factor Authentication (MFA)`, `Passkeys`, `OAuth`, `Magic Link`, `Biometric Authentication`.

`Authenticator Apps (TOTP)`: `Authenticator Apps using TOTP (Time-Based One-Time Password) generate temporary, time-sensitive passcodes used for two-factor authentication (2FA). These apps provide an additional layer of security by requiring users to enter a code from the app in addition to their password.` Related: `One-Time Passcodes (Email / SMS)`, `Multi-factor Authentication (MFA)`, `Email Links`, `Recovery Codes`.

### Route: model leaderboard

Dark end to end. An announcement strip above the headline reads `Best-in-class authentication solutions for the AI native landscape` with a `Learn more` arrow link. Headline `LLM Leaderboard`, body `Compare how different large language models perform at writing Aegis code and select the one that best fits your requirements.`

Rows are separated by the dashed rule rather than a solid one. Column separators are absent and the cells are separated by gap alone. At phone width the matrix scrolls sideways inside its own container with the model column pinned; the page itself never scrolls sideways.

A cell at or above its column's mean takes the informational cyan at low alpha with the bright cyan ink. A cell below takes the raised surface with body ink. A cell in the bottom decile takes the negative red at low alpha with matching ink. A cell with no result carries no ground and shows an en-rule glyph in faint ink.

### Route: component theme editor

The marketing chrome is retained plus a components rail; everything below the rail is the application. Each preview on the canvas is labelled with its monospace name and named components carry an `Overview` link beneath. The editor panel is fixed to the right on a raised ground with the floating shadow and a generous radius, carrying a title with a leading glyph reading `Theme Editor`, the body `Build and share custom themes for Aegis's components.`, a `Component` select plus a side-by-side toggle offering `Sign Up`, `Sign In`, `User Button`, `User Profile`, `Waitlist` and `Pricing Table`, a `Theme` select offering the four presets, the mode toggle, the colour fields, and three actions reading `Copy URL`, `Copy CSS` and `Reset to default`. Each field is a swatch button beside a monospace value.

Every colour field is a text input accepting a typed value as well as a swatch. The canvas exposes each preview as a labelled region and is operable by keyboard: arrow keys pan, modifier plus arrow zooms, and tab moves between previews. Changing a value announces the change politely once rather than once per keystroke. At phone width the canvas collapses to a single centred preview frame with a dashed outline and ordinary scrolling replaces pan and zoom, and the panel becomes a sheet from the bottom edge at half height by default, expandable to full, with the colour fields in a scrolling list and the canvas visible above. Leaving the advanced fields unreachable at phone width is a gap rather than a design, and this sheet is a deliberate addition to what was measured.

### Routes: blog, company, careers, startups, security, contact, brand assets, legal

**Blog.** Below the feature row sits a denser list carrying a category, a date and an author set per entry. The article is a single measure column with a lead paragraph at the reading size, a hero illustration, then body prose whose emphasis is a weight change rather than a colour. The article sidebar is right-aligned and sticky, in three parts: a filled dark category chip, the heading `Explore with AI`, and a link list of eleven rows each reading `Open in <ASSISTANT_n>` with a vendor mark and a trailing external-link glyph, then a twelfth row reading `Copy as markdown` with a document glyph. The captured article carries the lead `Funding will be used to advance Agent Identity, expand products, and elevate developer experience.` and body prose including `We're excited to share that Aegis has raised a $50 million Series C, led by <INVESTOR_4> and <INVESTOR_5>, alongside <INVESTOR_6> and previous investors.` and the claim `scaled to manage over 200 million users for over 15,000 applications`.

**Company.** Dark from the top through the hero, which carries a large dimensional rendering of the brand mark, centred, lit from the upper left with a specular highlight along the upper edge of the ring and a soft shadow beneath the dot, over the circuit field. Headline `It all starts with the user`, body `Aegis is on a mission to solve user management once and for all. We are a globally distributed team dedicated to providing the best developer experience with obsessive attention to every detail.` The investor band runs a cyan hairline across its top, the only coloured rule on the site, under the headline `Funded by industry-leading investors` and the body `Aegis is backed by investors with decades of experience building the world's best developer tools.` Then a caption cell and three investor cells, each a mark, a name, a positioning line and a smaller line naming prior investments: `Northgate`, `Backing bold entrepreneurs building the future through technology.`; `Rill`, `Investing with conviction since 1970.`; `Cedarline`, `Backing founding teams in seed, early, and acceleration stages in the Pacific Northwest and beyond.` Then a wide pull quote reading `We're big admirers of what the @aegis team are building and looking forward to working more closely with them.` with screen-reader-only `Name` and `Role` labels on the attribution. Then `Individual investors` over `Built with the trust of world-class founders, industry leaders, and dreamers working to make the web a better place.` and a grid of twelve people, each an avatar, a name, and a role and organisation, all carrying screen-reader-only field labels.

**Careers.** A pale, glowing rendering of the brand mark over a faint lattice in a wash of cyan and indigo with a dotted arc through it. The headline sits in three lines: `We're solving`, `user management`, then, in the script family and in the informational cyan, `once and for all.` Primary action `See open positions`. That script line is the only place on the site where a second family and a saturated colour appear in a headline; it is the site's one moment of warmth and it is not normalised into the display family. The founder letter is headed `Help Aegis help builders.` and makes its argument with a definition list: `Want to bill your users?` `Integrate <VENDOR_1>.`; `Want to email them?` `Integrate <VENDOR_2>.`; `Offer them support?` `Integrate <VENDOR_3>.`; `Analyze their behavior?` `Integrate <VENDOR_4>.`; `Track their contracts?` `Integrate <VENDOR_5>.` Then `Yet, integrating a complete stack of providers is infamously tedious, and builders are clamoring for a better way.` and `Aegis started with a simple insight: these integrations are often abstracted onto the User object, like user.subscribe() and user.email(). We imagined a service could offer a User object with the extensions built-in.` with the two method names as inline code pills, then `Today, that solution manages users for over 10,000 applications, and our customers are asking for extensions every day.`, signed `Dana Ruiz`, `CEO at Aegis`, with a portrait. The team section carries the eyebrow `The team`, the headline `Join a global team dedicated to their craft`, the body `We work with incredible talent from all around the world, each offering unique skills and perspectives.` and a four-cell statistics row rendered through the digit counter: `Year founded` `2019`, `Total funding` `$105M`, `Team` `~100`, `Companies served` `15K+`. Benefits carries the eyebrow `Perks and benefits`, the body `Bring your ideas and passion, and we'll offer you flexibility, growth, and a team that cares.`, the action `See open positions`, six cells reading `Competitive salary`, `Equity ownership`, `Health coverage`, `Work equipment`, `Flexible vacation policy` and `Remote and diverse team`, and a centred footnote reading `Benefits may vary by country. Benefits listed above currently apply to our US based employees.` Open roles carries the eyebrow `Open roles` and the body `Join a team where you can be you, make an impact, and thrive, without compromise.`

**Startups.** Two columns from the top. Left: the eyebrow `Aegis for Startups`, the headline `Start with user management that scales`, then `Aegis was built for founders like you to focus on your business, not authentication.`; `You always get 50,000 monthly retained users and 100 monthly retained organizations free with our developer-first pricing. Aegis Pro unlocks SMS codes, allowlist and blocklists, RBAC, custom session duration, device tracking and revocation, and more.`; and `Apply to get Aegis Pro features at a discount for your early-stage startup. Your team is eligible up to 1 year after launch with up to $5 million in venture funding.` Right: an application card in a dashed-outlined cell headed `Apply now`, reading `You must be signed in to Aegis to apply.` with a `Sign in` action when signed out, and the application form when signed in. This is the only place on the public site where the signed-in and signed-out states differ in content rather than only in chrome. The testimonial band is headed `Top YC startups build with Aegis` and marks its highlighted phrases with a semantic highlight element carrying a pale accent ground rather than a styled span, so it survives being read aloud and being copied into plain text. Highlighted phrases include `a world class developer experience`, `scale usage seamlessly`, `ship secure, multi-tenant auth`, `we can focus on building`, `Quality and consistency in design`, `Release now`, `Slack support is superfast` and `took the pain out of auth`. Each attribution carries a name, a role, an organisation with its accelerator batch, and where available a funding line such as `Raised $22m from <INVESTOR_7>`.

**Security.** Headline `Security & compliance at a glance`, a body naming certifications, frameworks and published artefacts and ending `Each item below links to a source you can check.`, then two hero actions side by side, `Visit the trust portal` as primary and `Read the security article` as secondary. It is the only route with two hero actions. The compliance table is headed `Compliance at a glance` over `The status of each framework, including the ones Aegis does not hold. Each row links to the relevant legal, pricing, or trust center document.` with the screen-reader-only caption `Aegis compliance status by framework` and four columns: `Requirement`, `Exact status`, `Detail`, `Access & evidence`. Column heads are the smallest size, uppercase, widely tracked, in faint ink. The evidence column carries `Report on the Business plan and above, via support@aegis.dev` for the first row and `Business Associate Agreement (BAA) on the Enterprise plan` for the second. Then four cells headed `SOC 2 report`, `HIPAA BAA`, `Public notices` and `Trust portal`, each with inline links, and the closing line `Aegis's audited platform controls are the same on every plan. Plans gate access to the reports and agreements, not the controls themselves.` Then `Security practices` over six cells: `Secure by default`, `60-second session tokens with server-side verification, refreshed in the background.`; `Breached-password detection`, `Passwords are checked against a public corpus of over ten billion compromised credentials, aligned with NIST SP 800-63B.`; `Abuse protection built in`, `Bot protection, account lockout, rate limiting, and user-enumeration protection.`; `MFA enforcement`, `Enforce multi-factor authentication application-wide with a single Dashboard toggle.`; `Independent audits`, `Third-party penetration testing and external code audits of the SDKs.`; `Coordinated disclosure`, `A published Vulnerability Disclosure Policy with safe harbor, a public status page, and full outage postmortems.` Then the closing paragraph `To report a vulnerability, email security@aegis.dev. The Vulnerability Disclosure Policy covers coordinated disclosure, response targets, and safe harbor for good-faith researchers.`

**Contact.** The shortest route, and its structure is two large cells over three small ones. Eyebrow `Contact`, headline `How can we help?`, body `Get in touch with our sales and support teams for demos, onboarding support, or product questions.` Then two large cells: `Sales`, `Connect with our sales team to talk about pricing, enterprise contracts, or to request a demo`, `Talk to sales`; and `Help and support`, `Submit a ticket to our support team or email support@aegis.dev directly`, `Submit a ticket`. Then three smaller cells: `Join the community`, `Connect with other developers and become a part of the Aegis community`, `Join Discord`; `Documentation`, `Gain deeper understanding of Aegis's features, APIs, and SDKs`, `Aegis Docs`; `Follow us on X`, `Find @aegis on X - or is it still called Twitter?`, `Follow on X`. **There is no contact form on this route** and every path leads elsewhere, which is deliberate and removes a whole class of spam handling from the build.

**Brand assets.** A grid of asset cells on the dashed grid, four across at desktop and one at phone, which is the largest desktop-to-phone expansion on the site. Each cell is a preview area showing the asset on its intended ground and a two-row action list reading `Download as PNG` and `Download as SVG` beside a monospace format label. Fourteen cells: the full lockup in four ground and colour combinations, the mark alone in four, the mark in a filled circle in four, and two further variants. The lockup in colour puts the accent on the mark and near-black on the wordmark over near-white; reversed is near-white throughout over near-black; monochrome is a mid cool neutral mark with a near-black wordmark over near-white. The mark in colour uses the accent and its pale step for the two crescent weights over near-black; monochrome uses a mid cool neutral and near-black over near-white; reversed uses a mid cool neutral and near-white over near-black. The badge in colour sets a near-white and pale-accent mark inside an accent disc over near-white; reversed sets an accent and pale-accent mark inside a near-white disc over near-black.

**Legal.** The index carries the headline `Legal Resources` and two columns under headings in the medium weight. **Customers**: `Standard Terms & Conditions`, `Commercial terms that govern purchases and use of Aegis services.`; `Data Processing Agreement`, `Processing terms, data handling roles, and obligations under privacy laws.`; `Subprocessors`, `Third-party service providers that may process customer data on our behalf.`; `Data Privacy Framework`, `Our certification and commitments for eligible international data transfers.`; `CCPA Supplemental Notice`, `California-specific rights, disclosures, and how to submit related requests.`; `GDPR Supplemental Notice`, `EEA and UK privacy rights, legal bases, and processing information.` **Everyone else**: `Privacy Policy`, `How Aegis collects, uses, and shares personal information.`; `Website Terms & Conditions`, `Terms that apply when using the Aegis website and related content.`; `Telemetry`, `Details on product usage signals collected to improve Aegis services.` Each title is an underlined link and each body sits in quiet ink; the circuit field is present behind the head and fades before the list begins. Each document is a single measure column with headings at three levels, numbered lists with hanging markers, tables for subprocessor and data-category listings, and a `Last updated` line, plus a sticky table of contents at desktop. Thirty screens of terms with no navigation is a defect rather than a design, and that table of contents is a deliberate addition to what was measured.

### The document depth

The site is two levels deep everywhere except the documentation portal and the legal set. Breadcrumbs do not exist: the second-level rail does that job on the five routes that need it, and the documentation sidebar does it inside the portal.

## Constraints

Single tenancy for the site itself: one Aegis site, one library, one plan document. Nothing in this build is multi-tenant, whatever the multi-tenancy route describes.

Every angle-bracket name in this brief is a SLOT, not an unfilled blank. `<SITE_ORIGIN>` is this app's own public origin, read from `APP_PUBLIC_URL`. `<FRAMEWORK>` is the framework a given landing route is written for. `<AGENT_1>` to `<AGENT_6>`, `<VENDOR_1>` to `<VENDOR_5>`, `<ASSISTANT_n>`, `<INVESTOR_4>` to `<INVESTOR_7>` and every customer, person, portfolio and framework mark are third-party identities the build names for itself: invent a short plausible name per slot, keep it stable across every route that shows it, and draw its mark as the generated abstract form described above. No real company, product or person is named anywhere in the build.

Not built, and not to be built: the identity platform itself. No token is minted, no session is federated, no enterprise connection is brokered, no signing key is rotated, no card is charged. Every claim the marketing routes make about those is content on a page, not behaviour in this application. The signed-in console is not built; it appears only as a caricature assembled from markup. Outbound webhooks, the local relay, impersonation, admin logs, log sinks and the machine-authentication key store are named in copy on the pricing and command-reference routes and are not implemented. Organizations, roles, permissions and invitations are described and not implemented. The generated-answer surface behind `Ask AI` is not built: the control exists and the search index behind it exists, and the answer generation does not.

No email is sent by this product and no mail service is available. No payments provider, no cache, no queue, no search service and no realtime service is available; the only backing services are PostgreSQL and MinIO. No outbound network call at run time. No native application, no browser extension, no command line binary: the command line route is a page describing one, not a shipped tool.

No binary asset of any kind ships with the build. Every third-party mark is a generated placeholder resembling no real trademark. Every reconstruction is labelled as one where it appears: the two dimensional brand renderings and the three light-band code inks are proposals rather than measurements.

The site must stay responsive with the glossary at tens of screens of content, the standard terms at a comparable length at phone width, and the leaderboard holding a result for every model, framework, mode and task family combination.

The acceptance checklist for this build is the set of numbered rules in `## Core features` together with the accessibility floors and the performance targets stated above. Each is written so that a disagreement about whether something is finished is a disagreement about a stated rule rather than about taste. Two things were deliberately not attempted and are not defects: no interaction on a touch device was measured, so every phone specification here derives from layout at a narrow viewport rather than from touch behaviour, and the interiors of four surfaces were never opened - the persistent help control, the consent panel, the search results and the answer surface - so what each must do is specified from its trigger and its context rather than reproduced. Three things are deliberately better than the reference and are labelled as additions rather than measurements: the sticky table of contents beside the long legal documents, the sheet holding the advanced colour fields at phone width, and keyboard operation of the theme editor canvas and table semantics on the leaderboard matrix.

The manual, the diary, the dictionary, the blog and the legal set all come from the one library, are all cross-linked, and are all searchable from the documentation portal.

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
| `POST /api/auth/sign-up` | `email`, `password`, `display_name` | `access_token`, `user` with `id`, `email`, `role`, `display_name` |
| `POST /api/auth/login` | `email`, `password` | `access_token`, `user` |
| `GET /api/entries` | `kind`, `state` | a top-level JSON array of entries |
| `GET /api/entries/{kind}/{slug}` | none | one entry |
| `POST /api/entries` | `kind`, `slug`, `title`, `summary`, `body`, `category_label` | the created entry in state `draft` |
| `PATCH /api/entries/{id}` | any writable field | the updated entry |
| `POST /api/entries/{id}/publish` | none | the entry in state `published` with `published_at` set |
| `POST /api/entries/{id}/unpublish` | none | the entry in state `draft` |
| `POST /api/entries/{id}/assets` | the file bytes, `alt_text` | `id`, `object_key`, `content_type`, `byte_size`, `alt_text` |
| `GET /api/entries/{entry_id}/assets/{asset_id}/content` | none | the bytes, streamed from the bucket |
| `GET /api/renditions/{kind}/{slug}` | none | the plain-text rendition |
| `GET /api/renditions` | none | a top-level JSON array of every rendition address |
| `GET /api/plans` | none | a top-level JSON array of plans with their features and ladders |
| `GET /api/leaderboard` | `framework`, `provider`, `mode` | a top-level JSON array of result rows |
| `GET /api/glossary/graph` | none | a top-level JSON array of `from_slug`, `to_slug`, `term_text` |
| `GET /api/compliance` | none | a top-level JSON array of compliance rows |
| `POST /api/applications` | `name` | the application and its `development` instance |
| `GET /api/applications` | none | a top-level JSON array of the caller's own applications |
| `POST /api/applications/{id}/instances` | `environment` | the created instance |
| `GET /api/instances/{id}` | none | one instance with its `state` and `publishable_key` |
| `POST /api/startup-applications` | `company_name`, `funding_raised_display`, `launched_within_year`, and the decoy field | the stored application, or a refusal |
| `GET /api/consent` | none | `analytics_allowed` or an undecided marker |
| `POST /api/consent` | `analytics_allowed` | the stored choice |
| `GET /api/search` | `q`, `sdk`, `version` | a top-level JSON array of results |
| `GET /api/health` | none | `200` |

Field names are exact. A list endpoint returns a top-level JSON array. A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as a client error, never as a server error and never as a silent success. Bearer auth is required on everything except login, sign-up, health and the public read endpoints.

### No mocks

The named provider is the fact. Any of the following is a contract violation: an in-memory array standing in for the entries table, image bytes written to the app container's filesystem, a database column holding an image instead of an object key, a hardcoded plan list in the page instead of a read from the plan tables, a leaderboard whose numbers are written into the markup, a rendition typed by hand rather than generated from the entry it belongs to, or an asset endpoint that reports success without an object existing in the bucket. The app's UI and its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A visitor can compare the four plans, read a quickstart in their own framework, create an account, and provision an application instance that reaches a live state with a publishable key. An author can draft an entry with an image, publish it, and see it and its plain-text rendition appear together. An unpublished entry stays unreadable to everyone but its own author, on its route, at its rendition address and in the object store alike. Two publishes claiming one slug leave exactly one published entry and nothing half-written.
