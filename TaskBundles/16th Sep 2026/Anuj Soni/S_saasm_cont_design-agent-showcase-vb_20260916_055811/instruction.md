# Design Agent Showcase

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser, scroll the home route while
the staged product replicas play and rewind under their hands, follow the site into the
answer-engine scanner, submit an address and a business email, and read a graded, sectioned
report at its own address, without hitting an error page. A different stranger must NOT be able
to read a story the team has not published, by any means, including a direct request for it by
its own address, a direct request for it by its identifier, and a direct request for its cover
image at the route the app streams covers from. The cover bytes must live in the object store at
their scheme's key; a copy on the app's own disk does not count, and neither does a row in the
database holding the bytes.

## Overview

`Kanvo` is an AI website builder: a design agent that works beside a person inside a real canvas
and a real content system, generating and refining pages in place while the person keeps the
final say. This application is the product's public marketing site and the small desk behind it.

The site's job is not to let anyone build a website in the page. It is to make the agent's
competence felt, by embedding faithful, animated replicas of the product, a canvas, a content
table, an agent chat and a page-settings panel, and advancing each one against scroll position so
that a capability plays out as the reader reaches it. When the reader is convinced, the site asks
for one thing: run the free answer-engine scan, or subscribe to the newsletter, or send a message.

Four audiences arrive with four questions. Designers ask whether the product respects their craft
or replaces it, and the home route's agent scenes and the AI route answer that. Agencies and
teams ask whether it can run real content and ship fast, and the CMS route answers that.
Marketers ask whether their pages will be found by search and by AI assistants, and the SEO route
and the scanner answer that. Founders ask whether it is safe, fast and worth standardising on,
and the platform grid answers that.

Behind the marketing surface sits the desk that keeps it alive. An author writes a customer
story, attaches a cover image, holds the story back while it is unfinished, publishes it, and may
put it behind a member wall. This is where the genuinely hard part lives: a story the team has
not published must not be readable by anyone but its own author, not in a list, not by a direct
request for the record, and not by reaching for its cover image; and a story held behind the
member wall must show its opening to a visitor and its full body only to somebody signed in.

It deliberately is not the product. No website is generated here, no model is called, and every
word the agent appears to say inside a replica is stored content played back against scroll. It
is also not a community: no comments, no likes, no followers, no sharing, no messaging, no
notifications. It sells no subscription and takes no payment. It sends no email.

## User roles

| Role | Can do |
|---|---|
| visitor (not signed in) | Read every marketing route, the customer-story index, every published open story, the opening of a published members story, the privacy page, and any scan report by its reference. Submit a scan, a newsletter subscription, a contact message and a cookie choice. **Cannot** read the full body of a members story, **cannot** see any story that is still a draft, **cannot** reach any `/studio` route, and **cannot** retrieve the cover image of a draft. |
| `reader` | Everything a visitor can do, plus read the full body of every published members story. **Cannot** write a story, **cannot** see anybody's draft, **cannot** reach any `/studio` route, and **cannot** read the leads desk. |
| `author` | Everything a reader can do, plus write, edit, publish and unpublish stories it owns, attach and replace their cover images, and read the leads desk: scan leads, contact messages, subscribers and the page-view record. **Cannot** read, edit, publish or delete another author's story while it is a draft, **cannot** see another author's draft in any list, and **cannot** create an account for anybody else. |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `reader` session to any `author`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected
state unchanged.

Signup is open: anybody may create a `reader` account from `/signup`, and a new account is always
a `reader`. There is no way to create an `author` through the interface. Author accounts are
seeded.

Seeded accounts, every one of them using the password `deku-demo-pw-2026`:

| Email | Display name | Role |
|---|---|---|
| `author@example.com` | `Marek Vantly` | `author` |
| `author2@example.com` | `Elian Brooks` | `author` |
| `reader@example.com` | `Priya Raman` | `reader` |

## Core features

### Auth

Accounts are email and password, held by the app itself. A person signs in with an email and the
password, and the app answers with an `access_token` the client sends as a bearer token on
every later call except login, signup, the health route and the public read surface. Passwords are stored hashed and
never in clear, and the exact literal `deku-demo-pw-2026` must work at login for every seeded
account. Tokens expire.

1. Signup at `/signup` takes an email, a password and a display name, and creates a `reader`. It
   never creates an `author`, whatever the request body asks for.
2. A signup using an email that already has an account is rejected as invalid and names the
   field. No second account is created.
3. A login with the wrong password is denied and returns no token.
4. A call carrying an expired token is refused, the record it aimed at is unchanged, and the
   interface returns the person to `/login` with the destination they were reaching for
   preserved, so signing in lands them there.
5. There is no password reset and no invitation flow.

### The shared chrome, on every route

Every route wears the same fixed top bar and the same tall footer, so the site always reads as
one place.

1. The top bar carries the `Kanvo` logo lockup on the left; then `Platform`, `Solutions` and
   `Resources`, each opening a full-width panel of grouped links below the bar; then the flat
   links `Enterprise` and `Pricing`; and on the right `Log in` and a filled `Sign up` pill.
2. The `Platform` panel carries a `Product` group: `AI`, `Agents`, `External Agents`, `Design`,
   `Collaborate`, `CMS`, `Hosting`, `Performance`, `SEO`, `Convert`, `Publish` and `Updates`.
   `AI`, `Agents`, `External Agents`, `Collaborate` and `Updates` each carry a `New` chip.
3. The `Solutions` panel carries a roles group (`Designers`, `Agencies`, `Marketers`, `Growth`,
   `Builders`, `Engineers`, `Site Teams`, `Founders`), a use-case group (`AI website builder`,
   `AI design agent`, `Website builder`, `Landing pages`, `Portfolio maker`, `UI/UX design`,
   `No-code`) and a `Compare` group listing seventeen competing builders by name.
4. The `Resources` panel carries `Academy`, `Guides`, `Desktop app`, `Blog`, `Newsletter`,
   `Stories`, `Developers`, `Creators`, `Experts`, `Students`, `Ambassadors`, `State of Sites`,
   `Help Articles` and `Contact`; a community group of `Marketplace`, `Templates`, `Components`,
   `Plugins`, `Vectors`, `Feed`, `Hype`, `Gallery`, `Contests`, `Members`, `Meetups` and
   `Updates`; and a tools group of `Figma to HTML`, `AEO scanner`, `Meta Tags`, `Free domains`,
   `CanvasBench` and `Shortcuts`.
5. The footer groups every secondary destination under `Product`, `Resources`, `Solutions`,
   `Community` and `Tools` headings, carries the company links `Careers`, `Brand`, `Store`,
   `Security`, `Abuse`, `Legal` and `Trust`, the controls `Trusted by`, `Follow us` and `CCPA`,
   a link to the privacy page, and the newsletter capture.
6. Only the links that this brief gives a route to lead anywhere; the rest are present as
   labels. **Every internal link that does lead somewhere resolves**: following any of them from
   any public route reaches a page, never a dead end and never the not-found page.
7. A first-time visitor is asked once about non-essential cookies, in a card that floats at the
   bottom left above everything else on the page. Its words are exactly:
   `We use cookies to personalize content, run ads, and analyze traffic. Read our Cookie Policy.`
   and it carries a single `Ok` button. The choice survives a reload and the card does not return in the same
   session.
8. `Copy logo SVG` and `Brand guidelines` are present in the `Platform` panel as labels.

### The privacy page

A privacy page at `/privacy`, reachable from the footer of every page, states in plain words what
`Kanvo` records about a visitor: the address of each page viewed and the moment it was viewed,
the name and business email submitted to the scanner, the email submitted to the newsletter, the
name, email and message submitted to the contact form, and the cookie choice itself. It states
how long each is kept and that a page view carries no account reference unless the visitor
accepted the analytics cookie choice while signed in.

### The site's own not-found page

1. Any address the site does not serve renders `Kanvo`'s own not-found page, with the full top
   bar and footer, the heading `Page not found`, the line
   `That page moved. We probably forgot to add a redirect here.`
   a filled `Back home` control returning to `/`, and a `Let us know` link opening the contact
   form.
2. That page **answers not found**, so a machine reading it is told the truth rather than being
   served a success.
3. A message sent from `Let us know` is recorded with the source `not-found`. A message sent from
   the enterprise contact route is recorded with the source `enterprise`.

### The page-view record

1. Every view of a public route is recorded with the route and the moment it happened.
2. The record carries the account reference **only** when the viewer accepted the analytics
   cookie choice and is signed in. A viewer who declined, or who is not signed in, produces a row
   naming the route and the moment and nothing that identifies anybody.
3. An `author` reads the whole record from the leads desk. Nobody else can read it, and a
   `reader` asking for it directly is denied.

### Home, at `/`

1. The route opens full height on the near-black ground. The heading reads, exactly:
   `Kanvo is the AI design agent for every step from idea to launch`
   set very large in the display face. Beneath
   it sit two controls, `Get started for free` and `Download app`, and beside them a live metric
   line reading `#15 on the open model index: 377.8B tokens this week`, whose two figures are
   emphasised against the rest of the line. That line is a live counter the app serves from its
   own origin, cached rather than recomputed on every view, and it falls back to that exact
   wording rather than leaving the heading waiting on it.
2. Below the heading sits the fluid field: a large dark panel in which colour moves continuously
   and slowly, like ink dropped in water, never reaching a visible loop point. A play triangle
   sits over it, and a caption in its lower right reads `Bloom Meadow 1.9`, which together
   present the field as a playable demo. Its behaviour is fixed: it animates continuously and
   slowly, it reaches no hard loop point a reader can notice, it sits behind the heading and the
   controls rather than over them, it stops entirely when it is scrolled out of view or the tab
   is hidden, and it dissolves into the page below it with no visible seam.
3. A customer strip follows, labelled `Meet our customers`, carrying eight wordmarks drawn by the
   browser: `Loopwork`, `Ledgera`, `Zaptask`, `Vega`, `Calday`, `Metricly`, `Mira` and
   `Dropcart`.
4. Then the agent act, under the heading `Agents that work alongside you, not instead of you`
   with a `Start with agents` link, in three scenes. `Design with an agent`: `A professional
   design agent, native to the canvas. It works directly on your site to generate and refine in
   place, with every change visible, editable, and under your control.` `Run your CMS with an
   agent`: `Manage more. Publish faster.` and `The CMS agent sets up, organizes, and updates your
   entire CMS, connecting it directly to the canvas so content and design stay in sync.` `Code
   with an agent`: `Agents turn your wildest ideas into code and put them on your site. From
   simple custom effects to complex interactions.` Each scene pairs a heading with one of the
   product replicas.
5. Then the platform grid: a dense grid of tiles, each carrying a label, a forward arrow and its
   own small live readout. `Performance`. `CMS`, showing a branch tree of `Main`, `use-cases`,
   `publishing 8m` and `content 10m`. `Hosting`, showing a giant `99.99% uptime` figure over a
   soft streak of light. `Collaboration`. `Localization`, showing `Dutch 35%`, `Italian 100%` and
   `Chinese 90%`. `Security`, showing an address bar with a padlock. `SEO`, showing a site
   settings card. `Analytics`, showing `Unique Visitors 1.7M`, `Total Pageviews 2.2M`,
   `Bounce Rate 40.9%` and a `View Home 400` variant over a brand-accent gradient block.
6. Then the display line `The heart of creative direction`, built one letter at a time so the
   words assemble themselves as the reader arrives and come apart as they leave, over a scrolling
   ticker of content rows: `Designing calmer interfaces inspired by nature` and `Organic shapes
   and natural motion in modern UI`, each carrying a `Live` or `Draft` status and a category.
7. Then `Connect to any AI`, with the body `Take action on your site from anywhere. Update copy
   from your chat tool. Trigger CMS changes from the terminal. Ship from a pull request. Drive it
   all from your terminal, your code editor, or any external AI.` and a `kanvo-agent` terminal
   token shown beside it.
8. The route closes into the footer and its newsletter capture.

### The AI route, at `/ai`

1. The heading reads `AI website builder for designers and teams`, with `Get started for free`,
   `Download app` and a `Watch demo` control.
2. Immediately below it the canvas replica appears at its fullest: a `Canvas` and `Site` toolbar,
   a `main` branch chip, `Invite` and `Publish` controls, a left rail carrying `Pages`, `Layers`,
   `Assets` and `Search...` over a page tree of `Home`, `/research`, `/commitments`, `/learn`,
   `/support`, `/news`, `/legal`, `/privacy`, `/terms` and `/try-volo`, a zoom readout reading
   `100%`, `Desktop` and `1200`, and the agent panel with its `Agent` and `Style` tabs and its
   model picker reading `Aster 5.6 Terra`.
3. This is the longest scroll on the site, and it holds one travelling soft edge of light that
   reveals the work underneath it as the reader descends.
4. Under the heading `Create with AI. Stay in control from canvas to publish.` come four
   capability scenes. `How Kanvo's AI website builder works`: `Describe the website, page, or
   update you need. Kanvo's AI agent creates editable pages, sections, copy, and visuals directly
   in your project. Keep refining in the conversation, or take over on the canvas at any point.`
   with a `Featured models` list of `Petal 3.1` (`Builds and ships`), `Ember 4.7` (`Fast and
   efficient`) and `Horizon 2.1` (`For complex work`). `Design responsive websites with AI and
   full control`, whose replica plays the prompt `Change the hero to a vertical stack layout,
   then replace the hero image with the image attached.` and recomposes the canvas into a
   vertical hero layout as the reader scrolls. `Manage website content with AI agents`, whose
   replica is the content table showing a `Documentation` and `Articles` collection. `Build
   custom code with an AI agent`: `Describe the interaction or live feature you need, and the AI
   agent can build a code component for your site. Review the result, refine it in Kanvo, and
   keep it connected to your design system.`, whose replica shows an `ImageSlider` code
   component. Each scene carries a `Start with Agents` link.
5. The route closes with a `News` panel carrying an `Announcement` chip and the heading
   `Introducing Horizon 2.1`, over the line `Horizon 2.1 is here. Our latest model for complex
   work.`

### The CMS route, at `/cms`

1. The heading reads `Create, manage, and publish dynamic sites with AI agents`, with
   `Get started for free` and `Download app`.
2. Below it the content-table replica carries a collections rail of `Careers`, `Documentation`,
   `Articles`, `Learn`, `Models`, `News` and `Research` with their item counts, a toolbar of
   `Collections`, `Fields` and `Plugins` with add, sort, filter and search controls, and a table
   of rows with `Title`, `Image` and `Category` columns.
3. The route's signature scene is the import. The reader scrolls, and the replica plays this
   sequence in this order: the prompt `Use use-cases.csv to create Use Case Articles and
   Categories collections. Populate fields and match each article to a category.`, then a
   `Thinking...` line that shimmers, then `I'll create two CMS collections from the attached
   CSV.`, then `Added 82 layers` and `44s`, then `Done - I added two linked collections:` with
   `Articles - 39 CSV rows imported.` and
   `Categories - 10 rows added and linked to Articles as multi-select tags.`
   then a `Changes` control and an `Undo` control, and finally two collection
   chips reading `Articles - 39 Items` and `Categories - 10 Items`. Scrolling back rewinds it.
4. Under the heading `Create, update and import your content. Manually or with a prompt.` a
   second replica shows an `Authors` collection with the fields `Name`, `Bio`, `Avatar` and
   `Department`, and a row reading `Marek Vantly / Design / Leads the Marketing team at Kanvo`.
5. Below that the route shows the real customer-story table, drawn from the site's own published
   stories, each row carrying its title, its category tag and its cover image. The category
   vocabulary is exactly `AI`, `Enterprise`, `Sports`, `Design`, `SaaS`, `Consumer` and
   `Startup`.

### The SEO route, at `/seo`

1. The heading reads `Built-in SEO tools with AI assistance`, with `Get started for free` and
   `Download app`.
2. Below it the page-settings replica shows a `Page Settings` panel with a `Save` control, a
   `Title` field bound to `Volo - {{Title}}`, a `URL` field reading `/resources/:slug/`, a locale
   reading `en`, a `Description` field bound to `{{Seo Description}}`, an explainer naming the
   available `CMS Variables:` as `Title, SEO Description, Intro, Slug, Quote`, a `Social Preview`
   slot labelled `1200 x 630 pixels`, and an `Automatic Locale` toggle. The doubled braces in
   `Volo - {{Title}}` and in `{{Seo Description}}` are characters the replica draws on the page,
   exactly as written; nothing substitutes a value into them.
3. Beside it a `Core Web Vitals` readout graded `GOOD` shows `LCP` `1.1s`, `INP` `95ms` and
   `CLS` `0.01`, and a `Files` panel lists `llms.txt` at `/llms.txt`, `robots.txt` at
   `/robots.txt` and `security.txt` at `/.well-known/security.txt` under the line `Upload
   well-known files like robots.txt, security.txt, or llms.txt, or serve any static file on a
   fixed URL.` An `Accessibility` panel binds an image `Alt Text` reading `Illustration of a
   stack`. These are the contents of a staged replica, not files this site serves.
4. Then `Meet our customers` over the same eight wordmarks, then the heading `Optimize every page
   with agents` over three scenes, each pairing a preview of a demo investing site called `Volo`
   (whose own navigation reads `Invest`, `How it works`, `Learn`, `Support` and `Contact sales`)
   with an agent chat. `Audit SEO with agents`: `Ask an agent to scan your page, prioritize SEO
   fixes, and apply approved updates to metadata, headings, alt text, and internal links.`
   `Generate metadata and copy with AI`: `Ask the agent to improve your title, description,
   headings, and key copy so the page is clearer, more specific, and easier to discover.` `Find
   internal link opportunities`: `Ask the agent to suggest links, anchor text, and missing
   supporting content so visitors and search engines understand what matters.`, whose chat plays
   the prompt `Scan this page for SEO issues and turn them into a prioritized list I can act on.`
5. A sample article renders inside the `Volo` preview, headed `How Agent Autopilot Is Reshaping
   Investing`, by `Elian Brooks`, `Research Lead`.

### The product replicas

Four replica archetypes recur across the marketing routes, and all four obey one contract.

1. Each replica takes a stored script: an ordered list of steps, each step carrying the point in
   the reader's passage through the section at which it lands.
2. Each replica takes one progress input: the reader's progress through its section, from the
   moment its top enters the viewport to the moment its bottom leaves, and it renders the state
   at that progress. Handing it the same progress input twice renders the same frame both times,
   including on the way back, so scrolling up rewinds the scene exactly rather than replaying it.
   Nothing else reads the raw scroll position: one owner maps an element's transit across the
   viewport to its own local progress and drives its children from that, and it detaches its work
   while the element is off screen.
3. Each replica is drawn from the same colours, faces and corner softness as the real chrome, at
   the same small chrome type size, so it reads as the product rather than as a picture of it.
4. Every word a replica shows is stored content. No model is called, nothing is generated, and
   the timing notes the agent appears to report (`2s`, `44s`, `Added 82 layers`) are content and
   appear exactly as written here.
5. The agent chat replica carries an `Agent` and `Style` tab row, a model picker reading
   `Aster 5.6 Terra`, a prompt bubble in the brand accent, a stream of agent output lines, and a
   composer whose placeholder reads `Add follow up...`. Its `Thinking...` line shimmers
   continuously while the reader is looking at it.
6. The home route's agent chat plays this script: the prompt `Create a few layout variations of
   my site. Keep the content but try some different compositions.`, then `Thinking...`, then
   `Created a design plan`, then `2s`, then `Placing layout variations side by side.`
7. The canvas replica is a framed site preview labelled `Desktop 1200` with a zoom control.
8. The content-table replica is a collections rail beside a table of rows.
9. The page-settings replica is the panel described on the SEO route.

### The customer-story desk

The site's own content is customer stories. An `author` owns the stories it writes.

1. A story carries a title, a slug, a category from `AI`, `Enterprise`, `Sports`, `Design`,
   `SaaS`, `Consumer` and `Startup`, an opening intro, a body, a state of `draft` or `published`,
   and an access of `open` or `members`.
2. Creating a story opens its own address at `/studio/stories/new` rather than a panel over the
   list, and the new story is always a `draft`, whatever the request body asks for.
3. A slug is claimed once and belongs to one story forever. Two stories can never share a slug:
   two simultaneous creates using the same slug must not both succeed, exactly one wins and the
   other is rejected as invalid naming the field, and no second row is left behind.
4. **A `draft` story is readable only by the author who owns it.** It never appears in
   `/stories`, it never appears in the story list of any other account, a direct request for it
   by its slug is answered as not found, a direct request for it by its identifier is denied, and
   a request for its cover image is denied. This holds for a signed-out visitor, for a `reader`,
   and for a second `author`; owning an author account is not owning this story.
5. A `published` story with access `open` is readable in full by anybody, signed in or not.
6. A `published` story with access `members` shows its title, its category, its cover image and
   its intro to anybody, and its body only to somebody signed in. A signed-out request for that
   story returns the story without its body; the body is withheld by the server, not hidden by
   the interface.
7. Publishing a story records the moment it was published. The story index at `/stories` lists
   published stories newest first by that moment.
8. Unpublishing returns a story to `draft`, and every rule in point 4 applies to it again at
   once.
9. An author may edit only its own story. A request to edit, publish, unpublish or attach a cover
   to another author's story is denied by the server and the underlying record must not change.

### Story cover images

1. A cover image is uploaded by the story's own author, and its bytes live in the object store,
   reached at `STORAGE_ENDPOINT` in the bucket named by `STORAGE_BUCKET` using
   `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. The store is `MinIO` and it is the only place
   those bytes exist: not on the app's filesystem, not in a database column.
2. The object key follows one fixed scheme: `stories/{story_id}/{sha256_of_bytes}.{ext}`, for
   example
   `stories/42/9f2a7c1e5b3d84a60f27ce91b40d5a8837e6c0b2d1495f7a3e8c60d29b41f5a0.png`.
   `{sha256_of_bytes}` is the lowercase hexadecimal SHA-256 of the uploaded bytes and `{ext}` is
   `png`, `jpg` or `webp`.
3. Accepted types are `image/png`, `image/jpeg` and `image/webp`. Anything else is rejected as
   invalid and nothing is written to the store.
4. Every cover carries alternative text supplied by its author, and a cover cannot be saved
   without it.
5. A story carries at most one cover. Uploading a second replaces the first; there is never more
   than one cover for a story.
6. Covers are served by the app itself, from its own route, after it has decided the caller may
   see the story. The bucket is never public, and no time-limited direct link to the store is
   ever handed out.
7. The cover of a `draft` story is denied to every caller but its owner, and the denial happens
   at the app's own route, so guessing the object key gains nobody anything.

### The answer-engine scanner, at `/aeo`

This is the site's sharpest conversion surface and its one non-trivial piece of work.

1. The route opens with the two-line heading `Can AI find your website?` over the supporting line
   `AI is changing how customers find you. Assistants now answer questions directly and most
   sites aren't ready. Scan yours in 10 seconds.`
2. One dark card holds the form: `Website`, a single field whose placeholder reads
   `yoursite.com`; `First name` and `Last name` side by side; `Business email`; and a full-width
   filled `Scan your site` control. Under it, in fine print, sits the disclaimer `This assessment
   scans one URL and uses AI - results may not be perfect. Use them as a guide, not a final
   answer. Scores reflect our own methodology and may differ from other AEO reports.`
3. The address is accepted when it names a host carrying a dot, with or without a scheme and with
   or without a path: `yoursite.com` and `https://yoursite.com/pricing` are both accepted. The
   address is refused when it names no host with a dot, when it names `localhost`, and when it is
   a bare word. A refused address is named inline as invalid and no scan and no lead is written.
4. The business email is refused when it is at `gmail.com`, `outlook.com`, `yahoo.com`,
   `hotmail.com` or `icloud.com`, because the scan captures a business contact. A refused email
   is named inline as invalid and no scan and no lead is written.
5. An accepted submission creates a scan and answers with its reference and the status `queued`.
   A reference reads `scan-` followed by twelve lowercase hexadecimal characters, for example
   `scan-4f1c9a72b0d3`.
6. The scan then advances on its own, without the visitor doing anything further: from `queued`
   to `running` to `complete`. While it runs, a thin bar fills steadily from left to right across
   the card.
7. The result the scan produces is specified here in full. A complete scan carries an overall
   grade of `strong`, `adequate` or `weak`, and exactly four sections, one for each of `discoverability`, `structure-and-metadata`, `trust-signals` and
   `answerability`. Each section carries its own grade from the same three words and at least one
   written finding. Never three sections, never five.
8. **The same address submitted twice grades identically**: the same overall word and the same
   four section words, both times, however far apart the two scans are.
9. The report is readable at `/aeo/scans/:reference` by anybody holding the reference. The name
   and the business email are kept as the lead and never appear anywhere in the report.
10. `Kanvo` never fetches the submitted address. The grade comes from the site's own published
    methodology, which is why the disclaimer says the scores reflect that methodology and may
    differ from other reports.
11. A queue holds the scans, so one submission cannot hold up another, and a single business
    email may start at most three scans in an hour; a fourth is refused as invalid and names the
    limit.
12. Below the form sits the educational band. `AI doesn't rank pages.` / `It picks answers.` over
    `Answer Engine Optimization (AEO) is the practice of making your content easy for AI systems
    to find, understand, and quote. As more people get answers directly from AI instead of
    clicking search results, being invisible to AI means being invisible to your audience.` Then
    three cards: `AI answers are replacing search clicks` / `Over 60% of searches now end without
    a click. If AI doesn't surface your site, users may never find you at all.`; `Structure and
    trust signals matter more than ever` / `AI models favor pages with clear metadata, structured
    content, and authoritative sources.`; `Most websites aren't ready - yours can be` / `Most
    sites still lack the basic signals AI needs. A few targeted fixes can move you from invisible
    to frequently cited.`

### The newsletter

1. The footer of every route carries a newsletter capture: one email field and a submit control.
2. Subscribing records the address with the status `pending` and names the confirmation step that
   turns it into a subscriber. The confirmation step is reachable from the inline banner the
   submission returns.
3. Completing the confirmation step moves the address to `confirmed`. Only a `confirmed` address
   counts as a subscriber, and the subscriber count on the leads desk counts only those.
4. Submitting the same address twice does not create a second record and does not double-count.
   The second attempt leaves the stored state exactly as the first left it and says so.
5. Completing the confirmation step twice leaves the address `confirmed` once, and the count does
   not move a second time.
6. An address that is not a well-formed email is rejected as invalid, names the field, and writes
   nothing. No account is created by subscribing.

### The contact message

1. A message carries a name, an email, a body and a source of `enterprise` or `not-found`.
2. Submitting one records it and acknowledges it inline with its reference. Nothing is emailed,
   because this site sends no mail.
3. A message missing its name, its email or its body is rejected as invalid, names the field, and
   writes nothing.

### The leads desk

1. An `author` reads the leads desk at `/studio/leads`: every scan with the name and business
   email that started it, every contact message with its source, every subscriber with its
   status, and the page-view record.
2. Nobody else can read it. A `reader` session asking for it directly, and a signed-out request
   for it, are both denied by the server.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Home: the fluid hero, the customer strip, the three agent scenes, the platform grid, the assembling display line, the connect section | public |
| `/ai` | The AI route: the canvas replica at its fullest and four capability scenes | public |
| `/cms` | The CMS route: the content-table replica, the import scene, the story table | public |
| `/seo` | The SEO route: the page-settings replica, the vitals readout, the files panel, three agent scenes | public |
| `/aeo` | The answer-engine scanner: the form and the educational band | public |
| `/aeo/scans/:reference` | One scan report: an overall grade and four graded sections | public |
| `/stories` | The customer-story index, published stories newest first | public |
| `/stories/:slug` | One customer story; a `members` story shows its body only when signed in | public |
| `/privacy` | What the site records and how long it keeps it | public |
| `/signup` | Create a reader account | public |
| `/login` | Sign in | public |
| `/studio` | The story desk: the collections rail, the story list, the selected story's detail | `author` |
| `/studio/stories/new` | Write a new story | `author` |
| `/studio/stories/:id` | Edit a story, attach its cover, publish or unpublish it | `author` |
| `/studio/leads` | Scan leads, contact messages, subscribers and the page-view record | `author` |
| any other address | The site's own not-found page, answering not found | public |

**Entry and redirects.** A person who is not signed in and opens `/studio`,
`/studio/stories/new`, `/studio/stories/:id` or `/studio/leads` is sent to `/login`, and after
signing in lands on the address they were reaching for rather than on a default page. Signing in
as an `author` with no preserved destination lands on `/studio`; signing in as a `reader` with no
preserved destination lands on `/stories`. Signing out returns to `/` and makes every `/studio`
address unreachable again. A `reader` who opens any `/studio` address is refused by the server and
shown the site's own not-found page, so the desk does not even announce itself. A token that
expires in the middle of an action refuses that action, leaves the record untouched, and returns
the person to `/login` with the destination preserved.

**Journeys.**

1. **A visitor is convinced and scans.** Open `/`. The fluid field is already moving behind the
   heading. Scroll down: the three agent scenes advance step by step under the scroll and rewind
   on the way back up, and the display line assembles itself letter by letter. In the footer,
   follow `AEO scanner` to `/aeo`. Type `yoursite.com` into `Website`, `Dana` into `First name`,
   `Whitfield` into `Last name` and `dana@northpost.co` into `Business email`, and press
   `Scan your site`. A thin bar fills. The report opens at `/aeo/scans/:reference` carrying an
   overall grade and the four sections `discoverability`, `structure-and-metadata`,
   `trust-signals` and `answerability`. The report names nobody.
2. **A visitor is refused.** On `/aeo`, submit `localhost` as the `Website` and
   `dana@gmail.com` as the `Business email`. Both fields are named inline as invalid, the page
   keeps what was typed, no scan exists and no lead was written.
3. **A reader unlocks a members story.** Open `/stories`. Four stories are listed, newest
   published first, and `How Calday ships landing pages 10x faster` is not among them. Open
   `How Vega rebuilt their community platform`: the cover, the title, the category and the intro
   are there and the body is not, with a line saying what signing in gives. Create an account at
   `/signup`, return to the story, and the body is readable.
4. **An author publishes a story.** Sign in as `author@example.com` with `deku-demo-pw-2026`.
   `/studio` opens with the collections rail on the left, the story list beside it and the
   selected story's detail beside that, all visible at once. Follow `New story` to
   `/studio/stories/new`, write the title `How Metricly rebuilt its docs in a week`, the slug
   `metricly-docs-rebuild`, the category `Design`, an intro and a body, and save. Attach a cover
   image and give it alternative text. The story is a `draft`: open
   `/stories/metricly-docs-rebuild` in a signed-out window and the site's own not-found page
   answers. Return to `/studio/stories/:id` and publish it. An inline banner confirms, and the
   story now sits first on `/stories`.
5. **A draft stays private.** Sign in as `author2@example.com` and ask for
   `How Calday ships landing pages 10x faster` by its slug and then by its identifier. Both are
   refused, its cover image is refused, and nothing about it appears anywhere in this account's
   story list.
6. **A visitor subscribes twice.** In the footer, submit `dana@northpost.co`. An inline banner
   says the subscription is pending and names the confirmation step. Submit the same address
   again: there is still exactly one record, still `pending`, and the banner says so. Complete
   the confirmation step: the record reads `confirmed`, and the subscriber count on the leads
   desk has risen by exactly one.
7. **A visitor hits a dead end.** Open `/pricing`. The site's own not-found page renders with the
   full top bar and footer, `Page not found`, `Back home` and `Let us know`. Follow `Let us know`,
   send a message, and it is recorded with the source `not-found`.
8. **An author reads the desk.** Sign in as `author@example.com` and open `/studio/leads`. The
   scan lead from journey 1, the message from journey 7, the subscriber from journey 6 and a page
   view for every public address walked above are all there.

**States.** Every list carries an empty state written for its own surface: `/stories` when
nothing is published yet, `/studio` when this author has written nothing, `/studio/leads` when
nothing has been captured, and a category filter that matches no story. Every route carries a
loading state while its records are in flight, and the fluid field holds a still frame until it
begins. A scan that is `queued` or `running` shows its progress rather than an empty report. No
error ever crashes the app: the surface keeps its shape, and an inline banner names what went
wrong and what to do next.

## UI/UX notes

**The north star.** Somebody who arrives here should understand within one screen that a capable
design agent is at work inside a real product, and should want to watch it rather than read about
it.

**The register.** This is consumer-facing editorial marketing with a working interface embedded
inside it, so the marketing surfaces may carry atmosphere and the subject is seen before anything
is read, while every product replica inside them reads as software and stays quiet, dense and
utilitarian. The two registers sit inside one page and must not blur: a replica that starts
performing like a marketing panel has stopped being convincing, and a marketing section that
adopts the replica's chrome has stopped being a page.

**The stance is show over tell.** A competing product could rationally hold the opposite, put its
claims in words and its screenshots in a gallery, and be right for a simpler tool. This one is
not that: wherever a sentence and a moving replica could carry the same claim, the replica
carries it and the sentence gets shorter.

**Mode.** Committed to dark and designed fully in dark. There is no light mode and none is
graded. The whole site reads as one continuous near-black scene from the first viewport to the
footer, and the fluid field at the top must dissolve into the ground below it with no visible
seam or edge where one section ends and the next begins.

**Palette by role.** The ground is a near-black neutral, and it is the only ground: no section
introduces a second background family. A raised surface, which is what every card and every
product replica sits on, is a near-black neutral one readable step above the ground, and a panel
sunk inside a replica is a deep neutral one step further. Depth is carried by a hairline stroke
of near-white neutral at a tenth of its strength, and by low wide shadows, never by a large soft
blur; a card that reads as floating on a cushion has left this palette. Primary text is a
near-white neutral. Secondary text, and every inactive item in the top bar, is that same
near-white neutral held back, and the difference between the two is the only weight the interface
needs to separate a label from its value. Captions and tertiary lines step down again to a light neutral, and meta
text steps down once more to a mid neutral, which is also the shade a disabled control's label
wears. A muted chrome band, a near-black neutral read one step off the
ground, runs behind the toolbars inside a product replica. Two blues do two different jobs and
never borrow each other's: a mid, vivid blue is the default link colour and means nothing except
that a word leads somewhere, while a mid, vivid cyan is the brand accent and appears only on the
product's own accent surfaces, the active branch row in a replica, the glow behind a publish
control, the bloom at the heart of the fluid field, and the focus ring. A surface that uses the
brand accent for ordinary decoration has spent the one colour the product owns. Three meanings
each own one colour and appear nowhere else: one for something refused, one for something that
worked, and one for something still running. A state that is none of those three may not borrow
any of them. Icon strokes are a mid neutral by default and only lift to near-white when the thing
they belong to is active. The exact shades are yours, so long as every exclusivity rule above
holds and text clears the contrast bar.

**Type.** `Inter` carries the interface and `Space Grotesk` carries display headings. The
personalities are deliberately far apart: interface type is small, dense and precise wherever the
page is pretending to be software, and display type is enormous and confident wherever the page
wants to make a statement. There is nothing in between, and a heading sized halfway between the
two has missed the point. Figures line up in a column wherever amounts stack, in the platform
grid readouts and on the leads desk. The exact families, sizes and line heights are in the
front-end specification below, because type is the product's identity rather than a preference.

**Shape.** Corners are consistently and gently softened everywhere, with three deliberate steps:
ordinary controls and cards are softened least, product replica panels are softened one step
more so they read as objects sitting on the page, and the primary action is a full pill. Circles
are reserved for avatars, status dots and round icon buttons. Nothing in the product has a sharp
corner, and nothing but the primary action is a pill.

**Density.** Two densities, and the boundary between them is the edge of a replica. The
marketing routes are comfortable: the subject is given room and a section reads as separate from
the one below it at a glance without needing a dividing line. Every product replica and the whole
studio are compact, where rows sit tight so a full collection fits one screen and an author scans
rather than scrolls. The gap between two marketing sections
is several times the gap beneath a heading, and it closes to roughly half on a narrow screen.
Every gap is a multiple of one base unit, which is yours to choose.

**Layout.** The public site is a top-navigation product: one fixed bar across the top of every
route, carrying three labels that each drop a full-width panel of grouped links, and one tall
footer directory at the bottom of every route. The bar is persistent and solid and does not
appear or disappear with scroll position. The studio behind the sign-in boundary is the opposite
shape: a rail of collections down the side, and beside it a split detail pane with the story list
on one side and the selected story's detail on the other, both visible at once, so an author
working through a collection never loses their place. Creating a story leaves the list and opens
its own address rather than covering the list with a panel.

**Motion.** The character is **eased**: considered entrance and exit, leaving quickly and
arriving slowly, so movement reads as a designed interface rather than as a machine reporting or
a toy bouncing. Everything moves on one speed and one curve, quick enough not to be waited for
and slow enough to be seen, and nothing uses a different speed to feel special. Motion here is
continuous rather than incidental, which is this site's whole character: one owner of smooth
scroll drives the whole page, a fluid field runs behind the first viewport, and most sections reveal by
tracking how far the reader has scrolled through them rather than by playing on a timer. Draw
every movement on the site from one small family of curves and no other, so nothing ever reads as
out of character: menus and controls glide evenly, and a big reveal leaves quickly and settles
rather than starting sharply. That distinction is
the requirement, not a detail: a reveal bound to scroll position runs backwards when the reader
scrolls back, and a reveal played on a timer does not. The recurring reveal is the mask-reveal pattern: a travelling
soft edge of light that wipes a section into view along an exact path, masking and unmasking it
as the scrubbed progress moves. What moves is the mask edge position, which is a function of how far the
reader has come through the section, together with how far the revealed part is transformed and
how opaque it is, and nothing else. The AI route is the most scroll-active surface on the site and
holds by far the longest of these masked timelines; the not-found page is the most still, and
carries a single line fading in and nothing more. The one display line on the
home route arrives one letter at a time as the reader reaches it and comes apart as they leave.
Exactly three named animations loop infinitely at runtime and nothing else does. A shimmer
sweeps across the `Thinking...` line in every agent chat, and the same sweep runs across any
placeholder text that has not arrived yet. A small sparkle animates on the `New` chips and on the
AI chips. A thin bar fills steadily and linearly from left to right wherever work is running,
which is the publish bar inside a replica and the progress bar on the scanner. Every one of those
infinite loops stops when its element is off screen, and each is a cheap movement rather than an
expensive one. Everything else animates once on arrival and then holds still.
Under `prefers-reduced-motion` the fluid field holds a still frame, all three loops stop, and
every scroll-bound reveal resolves to its finished state immediately; nothing is removed from the
page to achieve that, and the text a reveal would have uncovered is simply already visible.

**Components and their states.** Every control has a resting, pointed-at, pressed, focused and
unavailable state, and unavailable is never signalled by colour alone. There is one primary
action style and one quieter alternative, and the primary carries the strongest contrast on its
surface. The hover behaviour of the top-bar and footer links is the site's one constant small gesture:
they sit in the held-back near-white and rise to full near-white when a pointer hovers over them,
their border rising with them, and nothing else on the page does that. One control dims slightly
on hover instead of brightening, and that is the only place the site inverts the gesture. Escape closes an open menu panel. A destructive action, unpublishing a story
or replacing a cover image, confirms first. Confirmation and refusal both appear as an inline
banner at the top of the surface they belong to, which stays until it is dismissed or replaced;
nothing important is announced in a message that takes itself away.

**Accessibility floors, which are contract rather than taste.** Body text and its background meet
the WCAG AA contrast bar, in the dark mode the product commits to, and the two dimmest neutrals
never carry essential information on their own. Every interactive element is reachable and
operable by keyboard navigation, with a focus ring drawn in the brand accent glow that is clearly
visible on the near-black ground. A scrubbed reveal must not hide content from assistive technology: text
that a scroll-bound reveal has masked is always present in the document and only visually
covered, so it is readable with styles off and by a screen reader regardless of where the reader
has scrolled to. Near-white text on the near-black ground is high-contrast by construction, which
is why the white on black pairing carries the body copy and the held-back secondary text still
clears the bar against that ground. Every content image carries alternative text and
decorative images declare themselves decorative. Icon-only controls carry labels. Meaning is
never carried by colour alone. Form fields carry programmatic labels, inline error text naming
the field, and a described disclaimer where one is shown.

**Responsive.** The site is designed widest first and sheds its heaviest movement as the screen
narrows, deliberately rather than by accident. At the widest width the platform grid is a full
bento, agent chats dock beside the section they belong to, and the footer runs in several
columns. At the middle width the grid folds to two columns, each chat moves below its own
section, and the number of scroll-bound reveals drops sharply. At the narrow width everything
becomes a single column, the three menu panels become a stacked drawer, long scroll-bound
timelines become short reveals that play once, and the fluid field runs reduced or holds still.
The layout holds at every width between those tiers, nothing is scrolled sideways off the screen
without a control that reaches it, and every navigation target stays reachable at the narrow
viewport. Where each breakpoint sits is yours.

**What it must not look like.** Not a page dominated by one hue family with no second signal.
Not a wall of decoration standing in for content. Not a product replica that has been drawn as a
picture rather than built from the same tokens as the chrome around it, because a replica that
does not match the real product is the one thing this site cannot afford. Not a marketing
composition inside the studio, where a working surface belongs. Not a reveal that plays once on a
timer and refuses to run backwards.

## Front-end specification

Type is the product's identity rather than a value to echo, so the families, the sizes and the
line heights are carried exactly. `Inter` carries text and `Space Grotesk` carries display
headings. Both install from the package registry at image build time and are served from the
app's own origin; no font file is shipped with this brief and no font host is reached while the
app is running. The fallback stack is a system geometric sans, then `system-ui`, then
`sans-serif`. Two weights are enough for the whole site.

| Level | Size | Weight | Line height | Where |
|---|---|---|---|---|
| Interface chrome | `12px` | `400` | normal | replica labels, nav labels, captions, table cells |
| Emphasised chrome | `12px` | `500` | `14.4px` | active chrome, group headings, chips |
| Menu item | `13px` | `500` | `20.8px` | the three menu panels and the footer directory |
| Dense control | `14px` | `400` | `14px` | form fields, buttons, toolbar controls |
| Secondary body | `15px` | `400` | `20.25px` | supporting lines, card bodies, fine print |
| Body | `18px` | `400` | `24.3px` | section body copy, story body |
| Sub-heading | `28px` | `500` | `30.8px` | scene headings inside a section |
| Section heading | `36px` | `500` | `39.6px` | the heading that opens a section |

Display headings, which are the hero heading on every route, `Can AI find your website?` and
`The heart of creative direction`, are set from the width of their column rather than at a fixed
size, in `Space Grotesk` between weight `500` and weight `700`. They are the only type on the
site that scales with its container.

The content column is centred and the site holds one column width across every route, with the
same gutter on both sides, so a section on the home route lines up with a section on the SEO
route. The top bar is a fixed band across that full width. The stacking order runs shallow almost everywhere, with one
layer sitting above everything else on the page; that top layer is reserved for the cookie card
and any transient message, and nothing else may occupy it.

**Iconography.** Every symbol on the site is inline vector geometry drawn by the browser, never a
picture file, so it stays sharp at any size and recolours instantly. Icons are drawn on one
square grid at one stroke weight in a mid neutral, filled transparent. Corner softness inside a
replica runs one step deeper than the page around it, and an agent node carries the largest outer
radius on the site. The set the site needs: a
search glyph, a caret chevron that rotates when its menu panel opens, a circular enterprise mark, a
rounded square carrying four corner brackets which is the site's frame mark, a play triangle over
the fluid field, and a back chevron. The `Kanvo` logo lockup is a small drawn square mark beside
the product name set in the display face.

**Component architecture.** Where the module boundaries fall is yours, but the same component
architecture serves every route rather than each route bringing its own: the site is assembled
from a small set of repeated pieces: the
route shell with its shared chrome slots; the top bar, the three menu panels, the cookie card and
the footer with its newsletter capture; a section, a heading that reveals, a display line that
assembles letter by letter, the bento grid, the logo strip and the scrolling ticker; the scroll
owner and the reveals it drives; the graphics the browser draws, which are the fluid field and
its drifting sphere; the four product replicas; the scanner form and its report, which are the
only interactive islands on a page that is otherwise fixed at build time; and the primitives underneath all of them, buttons,
pill buttons, fields, chips, tags and avatars. A piece that appears twice looks and behaves the
same both times.

**Generated imagery: the zero-asset substitution rules.** No binary asset ships with this build,
so every asset class the site would have loaded has a substitution recipe instead. Where the site
shows noise or grain, that texture is generated inline at low opacity over the ground rather than
loaded, desaturated so it speckles the light and not the colour. Photographic media, which is
every customer photograph and every story thumbnail inside a replica, is replaced the same way. Customer wordmarks in the
strip are drawn from the palette, monochrome and evenly spaced. Demo thumbnails inside replicas
are drawn as soft brand-accent gradient blocks keyed by a seed, so the same row draws the same
block every time. The fluid field is composed of drifting pools of coloured light that add
together where they overlap, over the near-black base, with one soft-edged near-white sphere
carrying a faint warm specular drifting across it. The sphere is shaded with a brighter upper
half, a darker lower half, a soft horizon between them and one small hot highlight, and it is
worth the effort because it is what makes the field read as a lit object rather than a gradient.
The one image the site does not draw is a story cover, which is real content an author uploaded.

## Technical requirements

Front end: Vue 3, built with Vite and served as a production build. Back end: Flask on
Python 3.12, serving the HTTP API on the same origin under the `/api` prefix. Store: PostgreSQL,
reached at `DATABASE_URL`, which the environment also exports as `DB_URL` with the same value.
Object store: MinIO, reached at `STORAGE_ENDPOINT` in the bucket named by `STORAGE_BUCKET` using
`STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Auth: email and password held by the app, with
bearer tokens the client sends on every call except login, signup, health and the public read
surface. The browser receives an application shell on first paint and fetches every record as
JSON; nothing is rendered on the server, which is why the first thing painted is text rather than
an image. Health: `GET /api/health` returns `200` once the app is ready. Logging: one line of
structured logs per request to `stdout`, each line a single JSON object carrying a request
identifier, the method, the route, the response status and the duration in milliseconds, and never
a password or a token. The same request identifier is returned to the caller in an `X-Request-Id`
response header, so one identifier reaches from the browser to the line on `stdout`.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing
services available in this environment are PostgreSQL and MinIO, and reaching for anything else
is a contract violation.

**Both backing services are already running** and reachable at the environment variables above.
Do not download, install, compile or start a copy of either. Never hardcode a host or a port;
read every one of them from the environment.

**Contention and replay.** Two simultaneous creates of a story using the same slug must not both
succeed: exactly one wins, the other is rejected as invalid naming the field, and no second row
survives. Two simultaneous cover uploads for the same story must leave that story carrying
exactly one cover, never two. Two simultaneous subscriptions of the same address must leave
exactly one subscriber record, and the confirmed count must never rise twice for one address. A
completed scan carries exactly four sections and can never carry five, however many times its
completion is attempted. A failed create, upload or subscription leaves no partial state: no
orphaned row, no object stranded in the bucket, no half-written scan.

**Determinism.** Scanning the same address twice produces the same overall word and the same four
section words. Nothing in a scan result depends on the moment it ran or on how long it took.

**Contrast.** Body text and its background hold a contrast ratio of at least `4.5:1`, and every
interactive target is at least `44x44` in its smallest dimension.

**What the browser downloads.** Nothing the browser receives, no bundle, no document and no JSON
response, contains a credential, a store access key, a store secret key or a bearer token
belonging to somebody else. The value of `STORAGE_ACCESS_KEY` and the value of
`STORAGE_SECRET_KEY` never leave the server.

**Performance budget.** The fluid field holds a smooth frame rate on a three-year-old laptop and
pauses fully when it is off screen or the tab is hidden. The infinite loops run on many elements
at once, so each is a cheap movement rather than an expensive one, and each pauses off screen.
The many container reveals must not all resolve at once: only the ones near the viewport animate.

**Loading order.** The heading of every route is text and paints first. The fluid field starts
after that first paint, behind the heading, so nothing waits on it. A product replica begins
working only as it approaches the viewport, and its script is stored content rather than a
separate fetch. Anything moving that the reader cannot currently see is stopped.

All timestamps are UTC and are sent as ISO 8601 strings ending in `Z`.

## Data model

Nine tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not
a secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**`accounts`** - `id`, `email` (unique), `password_hash`, `display_name`, `role` which is exactly
`author` or `reader`, `created_at`. An email belongs to one account.

**`stories`** - `id`, `slug` (unique), `title`, `category` which is exactly one of `AI`,
`Enterprise`, `Sports`, `Design`, `SaaS`, `Consumer` or `Startup`, `intro`, `body`, `state` which
is exactly `draft` or `published`, `access` which is exactly `open` or `members`, `author_id`
referencing `accounts`, `published_at` which is empty until the story is first published,
`created_at`, `updated_at`. A slug belongs to exactly one story for the life of the application,
and no two stories ever hold the same slug. The reading order of the story index is derived from
`published_at` rather than stored, and whether a caller receives the `body` of a `members` story
is decided per request rather than stored.

**`story_covers`** - `id`, `story_id` referencing `stories`, `object_key`, `content_type` which is
exactly `image/png`, `image/jpeg` or `image/webp`, `byte_size`, `alt_text`, `created_at`. A story
holds at most one cover row, and an object key belongs to at most one cover row. The bytes
themselves are in the bucket at `object_key` and exist nowhere else.

**`scans`** - `id`, `reference` (unique), `target_url`, `first_name`, `last_name`,
`business_email`, `status` which is exactly `queued`, `running` or `complete`, `overall` which is
empty until completion and then exactly `strong`, `adequate` or `weak`, `created_at`,
`completed_at`.

**`scan_sections`** - `id`, `scan_id` referencing `scans`, `name` which is exactly
`discoverability`, `structure-and-metadata`, `trust-signals` or `answerability`, `grade` which is
exactly `strong`, `adequate` or `weak`, `finding`. A scan holds each section name at most once,
and a completed scan holds all four.

**`subscribers`** - `id`, `email` (unique), `status` which is exactly `pending` or `confirmed`,
`confirm_token` (unique), `created_at`, `confirmed_at`. An address belongs to one record however
many times it is submitted.

**`messages`** - `id`, `reference` (unique), `name`, `email`, `body`, `source` which is exactly
`enterprise` or `not-found`, `created_at`.

**`page_views`** - `id`, `route`, `viewed_at`, `account_id` referencing `accounts`, which is
empty unless the viewer accepted the analytics cookie choice while signed in.

**`consents`** - `id`, `choice_token` (unique), `analytics` which is true or false, `decided_at`.

**Seed data.** Three accounts: `author@example.com` as `Marek Vantly` with role `author`,
`author2@example.com` as `Elian Brooks` with role `author`, and `reader@example.com` as
`Priya Raman` with role `reader`. Five stories:

| Slug | Title | Category | State | Access | Owner |
|---|---|---|---|---|---|
| `loopwork-ai-search-brand-site` | `How Loopwork launched their AI search brand site` | `AI` | `published` | `open` | `author@example.com` |
| `ledgera-marketing-site-redesign` | `How Ledgera redesigned their marketing site` | `Enterprise` | `published` | `open` | `author2@example.com` |
| `zaptask-global-fan-experience` | `How Zaptask launched a global fan experience` | `Sports` | `published` | `open` | `author@example.com` |
| `vega-community-platform` | `How Vega rebuilt their community platform` | `Design` | `published` | `members` | `author2@example.com` |
| `calday-landing-pages` | `How Calday ships landing pages 10x faster` | `SaaS` | `draft` | `open` | `author@example.com` |

Every one of those five stories carries a cover row whose bytes sit in the bucket at the scheme's
key and whose alternative text is filled in, the draft included, so that a request for a draft's
cover has something real to be refused. One seeded subscriber, `reader@example.com`, with the
status `confirmed`. No seeded scans and no seeded messages; both are things a visitor makes.

Seeding must be idempotent - restarting the app must not duplicate rows, and must not leave a
second object in the bucket for a story that already has a cover.

## Constraints

- One tenant. There is one `Kanvo` site and one set of stories; there are no workspaces, no
  organisations and no second brand.
- No mail of any kind. Nothing is emailed: not a newsletter confirmation, not a lead
  acknowledgement, not a password reset.
- No outbound network call at run time. The scanner never fetches the address it was given, no
  font is fetched from another origin, no third-party analytics tag is loaded, and no model is called.
- No payments, no pricing checkout, no subscription and no invoice, whatever the `Pricing` label
  in the top bar suggests.
- No community surface: no comments, no likes, no followers, no sharing, no messaging, no
  notifications and no user profiles beyond a display name.
- No blog index, no help centre, no academy, no template marketplace, no desktop application
  download and no second locale. Those labels exist in the menus and lead nowhere.
- No file upload anywhere except a story cover image, and no downloaded bundle.
- No binary asset ships with the build. No image file, no video file, no font file, no audio file
  and no three-dimensional model. Every texture, icon, wordmark, thumbnail and the fluid field
  itself is drawn by the browser from the site's own tokens. The only bytes that exist are a
  story cover an author uploaded.
- No editing of the product inside the page. The canvas, the content table and the agent chat are
  staged replicas driven by stored scripts, and nothing a reader types into them changes anything.
- The app must stay responsive with a few hundred stories, a few thousand scans and a few tens of
  thousands of page views.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.** Field names are exact. A list endpoint returns a top-level JSON array. A
successful call returns the named resource or shape; an invalid or unauthorized call is rejected
as a client error, never a server error and never a silent success. Bearer auth is required on
everything except login, signup, health and the public read surface.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{email, password, display_name}` | the new reader account, without its password |
| `POST /api/auth/login` | `{email, password}` | `{access_token, role}` |
| `GET /api/health` | none | `200` once ready |
| `GET /api/stories` | optional `?category=` | an array of published stories, newest published first, each with `slug`, `title`, `category`, `intro`, `access`, `published_at` and `cover_alt_text` |
| `GET /api/stories/{slug}` | none | one published story with `slug`, `title`, `category`, `intro`, `access`, `published_at`, `cover_alt_text` and `body`; `body` is absent when the story is `members` and the caller is not signed in |
| `GET /api/stories/{id}/cover` | none | the cover image bytes with their `content_type` |
| `GET /api/studio/stories` | none | an array of the calling author's own stories, drafts included, each with `id`, `slug`, `title`, `category`, `state`, `access` and `updated_at` |
| `POST /api/studio/stories` | `{title, slug, category, intro, body, access}` | the new story with `state` `draft` |
| `PATCH /api/studio/stories/{id}` | any of `{title, category, intro, body, access}` | the updated story |
| `POST /api/studio/stories/{id}/cover` | the image bytes and `alt_text` | `{object_key, content_type, alt_text}` |
| `POST /api/studio/stories/{id}/publish` | none | the story with `state` `published` and `published_at` set |
| `POST /api/studio/stories/{id}/unpublish` | none | the story with `state` `draft` |
| `POST /api/scans` | `{url, first_name, last_name, business_email}` | `{reference, status}` |
| `GET /api/scans/{reference}` | none | `{reference, status, overall, sections}` where `sections` is an array of `{name, grade, finding}` |
| `POST /api/subscribers` | `{email}` | `{status, confirm_path}` |
| `POST /api/subscribers/confirm` | `{token}` | `{status}` |
| `POST /api/messages` | `{name, email, body, source}` | `{reference}` |
| `POST /api/consent` | `{analytics}` | `{analytics}` |
| `GET /api/metrics/hero` | none | `{headline}` |
| `GET /api/studio/leads` | none | `{scans, messages, subscribers, page_views}` |

**No mocks.** A cover image held in an in-memory dictionary, written to the app container's own
filesystem, stored as a column in the database, or answered from a hardcoded byte string the app
returns to itself, is a contract violation however correct the page looks. The same is true of a
story list assembled from a constant in the source rather than read from the database, and of a
scan whose report is a fixed object the app returns without ever recording the scan. The named
provider is the fact - the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.

## Definition of done

A stranger can scroll the marketing routes while the agent replicas play and rewind under their
hands, submit the answer-engine scanner, and read a graded report with four named sections at its
own address. An author can write a customer story, attach a cover image that lives in the object
store, and publish it onto the story index. A story nobody published stays invisible to everybody
but its author, by its address, by its identifier and by its cover image, and a members story
shows a signed-out visitor its opening and never its body.
