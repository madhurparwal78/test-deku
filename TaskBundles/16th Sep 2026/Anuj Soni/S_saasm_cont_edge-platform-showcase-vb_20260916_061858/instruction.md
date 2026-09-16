# Veloce

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, open the product
menus and read the thirty-two named services in them, scroll the home route through the
turning network globe and the five live statistics, watch a capability module state its
result, and create a free trial account from the signup form, without hitting an error
page. A different stranger must NOT be able to read an article the team has not published,
by any means, including a direct request for it by its own address, a direct request for it
by its identifier, and a direct request for its cover image at the route the app streams
covers from. The cover bytes must live in the object store at their scheme's key; a copy on
the app's own disk does not count, and neither does a row in the database holding the bytes.

## Overview

`Veloce` sells a global edge cloud platform: a network that delivers, secures and computes
traffic close to the people using it. This application is the product's marketing and
product-showcase site, plus the small editorial desk that keeps its articles alive.

The site is aimed at engineering and platform teams who are evaluating content delivery,
security and edge compute, and who cannot judge a network from a feature list. So the site
argues instead of asserting. It states the promise in one line, shows who already trusts
it, tells the network story beside a turning globe, proves the claims with five live
statistics that carry their own measurement dates, lays out the whole services catalogue as
the platform's own taxonomy, segments by industry, and closes on a create-account call. Its
one commercial job is to get a visiting engineer to start a free trial.

The site's most demanding surface is not the hero and not the globe. It is the set of eight
capability modules that explain what the platform does: routing that re-chooses a path when
conditions change, a cache change that reaches every server at once, an attack absorbed at
the edge while real visitors walk through, a piece of the network dying without a dropped
request, logic running next door to the visitor, a defended perimeter, traffic data arriving
as it happens, and connections encrypted by default. Each one animates its claim and states
its outcome in words as well, so a reader who cannot see the animation still gets the fact.

Behind the marketing surface sits the desk. An author writes an article, attaches a cover
image, holds it back while it is unfinished, publishes it, and may put it behind a members
wall. This is where the genuinely hard part lives: an article the team has not published
must not be readable by anyone but its own author, not in a list, not by a direct request
for the record, and not by reaching for its cover image; and an article behind the members
wall must show its opening to a visitor and its full body only to somebody signed in.

It deliberately is not the platform. No traffic is delivered here, no cache is purged, no
attack is absorbed, and every number and every animated proof is played back from the
site's own stored content. It takes no payment and sells no plan: the pricing route
describes plans and every button on it leads to the signup. It sends no message of any
kind. It is not a community: no comments, no likes, no followers, no sharing, no
notifications. It does not translate itself: the language control lists the locales the
company publishes in and remembers the choice, and the words on the page stay as they are.

## User roles

| Role | Can do |
|---|---|
| visitor (not signed in) | Read every marketing route, the services catalogue, the article index, every open article in full, the opening of a members article, the privacy and terms routes, and the search results. Create a free trial account, and record a cookie choice. **Cannot** read the body of a members article, **cannot** see any article that is still a draft, **cannot** reach any `/desk` address, and **cannot** retrieve the cover image of a draft. |
| `reader` | Everything a visitor can do, plus read the full body of every published members article. **Cannot** write or edit an article, **cannot** see anybody's draft, **cannot** reach any `/desk` address, and **cannot** change anybody's account. |
| `author` | Everything a reader can do, plus write, edit, publish and unpublish the articles it owns, and attach or replace their cover images. **Cannot** read, edit, publish or delete another author's article while that article is a draft, **cannot** see another author's draft in any list, and **cannot** create an account for anybody else. |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in
the UI is not authorization: a direct API call from a `reader` session to any `author`-only
endpoint must be rejected by the server (an unauthorized request is denied, not served),
leaving the protected state unchanged.

Signup is open: anybody may create an account from `/signup`, and a new account is always a
`reader`. There is no way to create an `author` through the interface. Author accounts are
seeded.

Seeded accounts, every one of them using the password `deku-demo-pw-2026`:

| Email | Display name | Role |
|---|---|---|
| `author@example.com` | `Marisol Quint` | `author` |
| `author2@example.com` | `Teodor Vance` | `author` |
| `reader@example.com` | `Ingrid Salas` | `reader` |

## Core features

### Auth

Accounts are email and password, held by the app itself. A person signs in with an email and
the password, and the app answers with a bearer token in the field `access_token`. Every later call
carries that token, apart from four: the login, the signup, the health route and the public read
surface. A password is kept only as a hash and never in clear, and the exact literal
`deku-demo-pw-2026` opens every seeded account at login. A token stops working the moment its
holder signs out.

1. Signup at `/signup` takes a work email and a password and creates a `reader`. It never
   creates an `author`, whatever the request body asks for.
2. The signup form refuses a consumer mailbox. An address at `gmail.com`, `outlook.com`,
   `yahoo.com`, `hotmail.com` or `icloud.com` is rejected as invalid, the refusal names the
   email field, and no account is created. Every other well-formed address is accepted.
3. A signup using an email that already has an account is rejected as invalid and names the
   field. No second account is created.
4. A login with the wrong password is denied and returns no token.
5. A call carrying a token that is no longer valid is refused; the record it aimed at stays as
   it was, and the person is sent to `/login` carrying the destination they were reaching for,
   so the sign-in lands them on it.
6. There is no password reset, no invitation flow and no sign-in with another company.

### The shared chrome, on every route

Every route wears the same two-row bar across the top and the same deep footer, so the
site always reads as one place.

1. The upper row of the bar, right aligned, carries: a language control showing the current
   language `English` and opening a list of exactly seven, spelled `English`, `Japanese`,
   `Espanol (Espana)`, `Espanol (Latinoamerica)`, `Deutsch`, `Francais`, `Italiano`; a
   control labelled `Under Attack?` leading to `/under-attack`; the support line
   `(844) 4VELOCE`; `Support Center`; and `Log in`. When somebody is signed in, `Log in`
   becomes their display name and a `Log out` control.
2. Choosing a language records the choice and it survives a reload. The words on the page
   do not change: the control states which locale the company publishes in.
3. `Under Attack?` is the one alarm-coloured control anywhere in the chrome, and its label
   says what it is, so it never relies on its colour to be understood.
4. The lower row carries the `Veloce` wordmark at the far left; then seven menu triggers
   spelled `Why?`, `Products`, `Services`, `Solutions`, `Devs`, `Partners`, `Resources`,
   and a flat `Pricing` link; then a search trigger; then two buttons, `Talk to an expert`
   and `Try Veloce Free`.
5. `Try Veloce Free` is the primary action in the chrome and leads to `/signup`.
   `Talk to an expert` is the quieter alternative and leads to `/signup` as well, because
   nothing here sends a message.
6. Opening a menu trigger drops a full-width mega-menu panel below the bar. It opens on a pointer and
   on keyboard focus, keeps focus inside itself while it is open, closes on escape, and
   closes when another trigger opens.
7. The footer opens on the line `Get in touch or create an account`, which leads to
   `/signup`. Below it, columns of links mirror the menu taxonomy, and the closing row
   carries `Terms`, `Privacy`, the language control again, and the social marks.
8. A back-to-top control appears once the page has been scrolled and returns to the top.
9. Only the links this brief gives a route to lead anywhere; the rest are present as
   labels. **Every internal link that does lead somewhere resolves**: following any of them
   from any route reaches a page, never a dead end and never the not-found page.

### The product menus and the services catalogue

The `Products` panel is the site's primary internal linking and the visitor's first real
contact with the product surface. It carries the header `The Veloce Edge Cloud Platform`,
a `See All Products` link, and four tabs: `Network Services`, `Security`, `Compute`,
`Observability`. Choosing a tab replaces the tile list beside it. Each tile is a service
name over its one-line description.

1. The catalogue holds exactly thirty-two services in these four families, with these
   names and these descriptions:

| Family | Service | Description |
|---|---|---|
| `Network Services` | `Content Delivery (CDN)` | `Deliver fast, personalized experiences globally` |
| `Network Services` | `Live Streaming` | `Deliver seamless live streaming experiences` |
| `Network Services` | `Streaming Video (VoD)` | `Deliver exceptional on-demand video experiences` |
| `Network Services` | `Origin Shield` | `Optimize multi-network deployments` |
| `Network Services` | `On-the-Fly Packager` | `Dynamically package on-demand video content in real time` |
| `Network Services` | `Image Optimizer` | `Rapid image processing at the edge` |
| `Network Services` | `Load Balancer` | `Granular control over routing decisions` |
| `Network Services` | `TLS Encryption` | `Reduce the complexity of TLS management` |
| `Network Services` | `Origin Connect` | `Connect directly to Veloce` |
| `Network Services` | `IP Addresses` | `Easily manage IP addresses` |
| `Network Services` | `HTTP/3 and QUIC` | `Modern protocols` |
| `Network Services` | `Domain Research API` | `Instant, accurate domain name discovery` |
| `Network Services` | `Object Storage` | `Direct access to large files at the edge with zero egress fees` |
| `Security` | `Next-Gen WAF` | `Modern web app and API security, anywhere` |
| `Security` | `Bot Management` | `Detect and mitigate bot attacks` |
| `Security` | `DDoS Protection` | `Automated mitigation of disruptive and distributed attacks` |
| `Security` | `API Security` | `Secure your API endpoints` |
| `Security` | `Client-Side Protection` | `Defend against client-side attacks` |
| `Security` | `AI Bot Management` | `Stop AI bots from scraping website content` |
| `Compute` | `Edge Compute` | `Take your apps to the edge: our instant platform helps you build amazing experiences for your users` |
| `Compute` | `Key Value Store` | `The fastest key value store you can get, as easy to use as familiar database tools` |
| `Compute` | `Websockets and Fanout` | `Real-time messaging, at global scale, with complete personalization and easy setup` |
| `Compute` | `Developer SDKs` | `Program the same services we use to build Veloce products` |
| `Compute` | `Enterprise Serverless` | `The most powerful serverless platform, built on open standards` |
| `Compute` | `AI` | `Accelerate your AI workloads with semantic caching` |
| `Compute` | `Programmable Cache` | `Full programmatic access to the same caching that powers our CDN` |
| `Observability` | `Real-time Logging` | `Stream and analyze logs in real-time` |
| `Observability` | `Edge Observer` | `Explore live and historical traffic data` |
| `Observability` | `Domain Inspector` | `Assess domain level insights` |
| `Observability` | `Origin Inspector` | `View complete origin to edge insights` |
| `Observability` | `Alerts` | `Create notifications for service-related metrics` |
| `Observability` | `Log Explorer and Insights` | `Interact with actionable insights` |

2. The `Why?` and `Resources` panels carry these entries, each a title over its own line:
   `The future of business starts with developers` with a `Learn more` link;
   `Company`, `The team behind better online experiences`;
   `Network Map`, `A new architecture for the modern internet`;
   `Industry Analyst Relations`, `See what industry analysts say about Veloce`;
   `News`, `Recent updates and announcements`;
   `Platform`, `The platform behind better, faster and more secure digital experiences`;
   `Customer Stories`, `See how the best of the web succeed`;
   `Events`, `Connect with Veloce at an event`;
   `Careers`, `Join the team that is building a better internet`.
3. The same thirty-two services are listed in full on the home route's platform section,
   under the same four family headings, so the catalogue is readable without opening a
   menu and on a touch screen where there is no pointer to open one with.
4. The services catalogue is content the site stores, not markup typed into a page. It is
   read back at run time and the same rows drive the panel and the home section.

### The home route, at `/`

The home route reads top to bottom as one argument, in this order.

1. **The promise.** A dark opening band carrying the headline
   `Build, Secure, and Deliver. Instantly.` and beneath it
   `Create fast, secure, and scalable sites and apps on a programmable edge cloud platform. Start building for free.`
   Two actions sit under it: `Request a demo` as the quieter one and `Get started` as the
   primary. Both lead to `/signup`. A generated illustration sits beside the words.
2. **The announcement rail.** A row of award and news chips that moves sideways on its own,
   continuously, in one direction, and never stops to let a chip be read. Its content is
   the company's analyst recognition.
3. **The trust wall.** The line `Trusted by the world's leading digital innovators` above a
   row of customer marks that moves sideways on its own, more briskly than the rail above
   it. The marks are generated, not fetched.
4. **The platform section.** The line
   `Our platform is fully programmable. You get smarter solutions, better insights, and more control.`
   followed by the four family headings and their services, and the paragraph
   `Move to a faster, more secure network and get immediate benefits for your org and users. Step up to a better CDN for everything from ecommerce to publishing and streaming. Plan confidently with predictable pricing and no surprise overages.`
   closing on `Check out the Veloce CDN`, which leads to `/pricing`.
5. **The network section.** The heading `A more powerful global network` beside the globe,
   with the paragraph
   `We built our network with intention. By design, we run fewer points of presence than our competitors, but they are much more powerful so we can cache more and serve it faster. Our network is fully software defined. We can do anything, and do it faster.`
   and the link `Take a closer look`, which leads to `/company`.
6. **The statistics band.**
7. **The capability modules.**
8. **The flexibility section.** The heading
   `The one thing every business needs is flexibility` and the paragraph
   `Everybody needs speed, reliability, security, savings, and scale, but different industries have different needs. Veloce's powerful network and smarter solutions can be tailored to your organization. We partner with you to guarantee a smooth migration, so you can deliver the best possible user experiences.`
   Three industry cards follow: `eCommerce`, titled
   `Provide faster and more secure retail experiences`, with the body
   `You are always open for business with Veloce. We handle the crowds and load-balancing so no one is turned away. Your customers will always see accurate information with real-time updates, and all of it is protected from DDoS, bots, and other threats.`;
   `Streaming Media`, titled `Deliver stellar streaming experiences`, with the body
   `Veloce gives every viewer around the world a better experience on our modern network. Instant scaling with lower latency live streaming lets you reliably deliver engaging entertainment experiences in real-time.`;
   and `Travel and hospitality`.
9. **The reading cards.** Three cards drawn from the published articles, newest first, each
   a generated thumbnail over a category eyebrow, a title and a forward-arrow link reading
   `Read the report`. The first card is
   `What is a modern CDN and why is it important?`, whose summary is
   `Too many developers and companies are dealing with the dark ages of black-box, legacy content delivery networks that were not built to provide the real-time observability, baked-in security, and programmatic control needed to deliver the dynamic experiences today's users and developers demand.`
10. **The closing call and the footer.**

### The network globe

The globe stands for the network and is the emotional centre of the home route.

1. It is a sphere drawn from vector geometry: an outline world with meridian arcs, a group
   of location pins standing for points of presence, and one thin elliptical ring orbiting
   it. Nothing about it is a picture file.
2. It turns continuously and slowly in one direction while it is on screen.
3. Each pin arrives with a single expanding pulse that fades as it grows, once, as the
   network section comes into view.
4. Under a reduced-motion preference the globe holds still, the pins are simply present,
   and the claim beside it is unchanged.
5. The globe is decorative and carries a text alternative that states the claim rather than
   describing the drawing, so the network story survives without it.

### The live statistics band

Five proof statistics sit in a band. Each is a coloured pill carrying a qualifier above a
large value, a caption under it, and a small superscript mark leading to its measurement date.

1. The five are exactly these, in this order:

| Qualifier | Value | Caption | Measured |
|---|---|---|---|
| `On average` | `<150 ms` | `regional mean purge time to clear cached content globally` | `as of December 31, 2025` |
| `More than` | `5 trillion` | `Daily requests served` | `as of March 31, 2026` |
| `Almost` | `90%` | `Of customers run the next-gen firewall in blocking mode` | `as of March 2023` |
| `Global` | `622 Tbps` | `Edge network capacity` | `as of June 30, 2026` |
| `Up to` | `32%` | `faster time to first byte than other networks` | `as of June 30, 2026` |

2. Each value counts up from zero the first time the band comes into view, once, and then
   holds at the value above. The counting never changes the final text.
3. A link under the row reads `read about the methodology` and leads to `/trust`.
4. The band is content the site stores and reads back at run time, so the five rows and
   their measurement dates come from the same place the rest of the site's content does.
5. Under a reduced-motion preference the values are simply present at their final text with
   no count.
6. The pills carry their meaning in words. Nothing about which statistic is which depends
   on which colour its pill wears.

### The capability modules

Eight modules explain the platform, each an animated diagram of one claim. They share one structure and
differ only in their content, so they read as one family rather than eight separate
drawings. Every one of them is built from vector geometry and stored content, reaches no
other host, and holds still under a reduced-motion preference.

1. The eight, each with its title, the claim it argues, and the result line it must state
   in words, exactly as written:

| Module | Claim | Result line |
|---|---|---|
| `Real-time global routing optimization` | Traffic chooses its path from live network conditions and re-chooses when they change | `Congested region avoided. Every request took the fastest open path.` |
| `Distributed, globally-consistent caching` | One change reaches every server in the world at once | `0 nodes left on the old copy.` |
| `Absorbing large-scale attacks` | A flood of hostile traffic is soaked up at the edge while real visitors pass through untouched | `0 attack requests reached the origin.` |
| `Instant, invisible failover` | A piece of the network fails and traffic continues without a visible break | `0 requests dropped.` |
| `Programmable logic at the edge` | Custom code runs at the location nearest the visitor rather than at a distant origin | `Answered at the edge, not at the origin.` |
| `Modern web and API security` | Named threats strike a single defended perimeter and are deflected | `Blocking mode on. Every threat deflected at the perimeter.` |
| `Real-time observability` | Traffic data arrives as it happens rather than on a delay | `Live. The newest value arrives at the right edge.` |
| `Secure, modern transport` | Connections are encrypted by default over the newest protocols, and certificates are managed for the customer | `Encrypted by default. Certificates managed for you.` |

2. The result line is rendered as text on the page beside its module, always, whether the
   module has finished animating or not and whether motion is allowed or not. A reader who
   cannot see the animation gets the same fact from the same page.
3. Each module also states its claim in a sentence, so the argument survives with images
   off.
4. The routing module shows one region becoming congested on its own and then again when a
   pointer asks it to, and the traffic visibly abandons that path for the next best one.
5. The caching module shows a dense field of nodes holding an old copy, a single push
   travelling outward from the centre, and every node flipping to the new copy before the
   push reaches the edge of the field. No node is left on the old copy when it settles.
6. The attack module shows a thick hostile mass and a thin steady stream arriving at one
   bar. The hostile mass terminates inside the bar and never reaches the origin behind it;
   every part of the thin stream reaches the origin.
7. The failover module shows several locations sharing one traffic line. One goes dark, the
   others absorb its share, and the combined line neither dips nor breaks.
8. The edge-compute module shows two paths from the same starting point, a long one to a
   distant origin and a short one to a nearby location, each with its own elapsed readout,
   and the short one settles at a fraction of the long one.
9. The security module shows several labelled threats striking one perimeter and being
   turned away, with a control that switches the perimeter between watching and blocking.
10. The observability module shows a line that gains a new point at its right edge on every
    tick, with a small dot that pulses to say the feed is live. It updates without the
    chart blanking and redrawing.
11. The transport module shows a padlock closing as a connection is made, labelled with the
    protocols the platform speaks.
12. Every module runs from the site's own stored content. None of them fetches from another
    host, and none of them reports a number the site did not store.
13. A module that is off screen is not animating.

### The company route, at `/company`

Titled `About our company - Fueling the future of the web`. A narrative page: a mission
statement, a values section, a leadership section, and the network story again in a shorter
form than the home route tells it. It is built from rows that alternate a block of words
with a generated illustration, and it adds no component the rest of the site does not
already have.

### The pricing route, at `/pricing`

1. Plan cards sit side by side. The first is the free tier, headed `Try Veloce Free`, and
   the paid tiers follow. Each card lists what is included and carries one action leading
   to `/signup`.
2. The page is anchored by the message
   `Plan confidently with predictable pricing and no surprise overages.`
3. A comparison table sits below the cards, one row per included capability, one column per
   plan.
4. Nothing on this route takes a payment, records a plan choice, or creates anything other
   than the account the signup creates.

### The blog index, at `/blog`

1. A lead article sits above a grid of article cards. Each card carries a generated
   thumbnail, a category eyebrow, the title, the excerpt, and a forward-arrow link.
2. The index lists only articles that are published, newest first by published date. A
   draft never appears, for anybody, including its own author.
3. A members article appears in the index with its title, category, thumbnail and excerpt,
   and is marked as needing an account.
4. With nothing published the index reads `No articles published yet.`

### An article, at `/blog/{slug}`

1. An open article shows its category, title, author display name, published date, cover
   image and full body to anybody.
2. A members article shows its category, title, author display name, published date, cover
   image and excerpt to anybody, and its body only to a signed-in account of either role.
   To a visitor it shows the primary action `Try Veloce Free` in place of the body.
3. A draft article is not served by this route to anybody but the account that owns it. A
   request for a draft by somebody else is refused and discloses nothing about it: not its
   title, not its author, not that a draft by that name exists.
4. A request for an address that matches no article renders the site's own not-found page
   and the server answers not-found.
5. At the foot of an article a row of related articles slides sideways under a pointer or a
   touch, drawn from the same category, published only.

### The editorial desk, at `/desk`

The desk is the author's own surface and is a table, because an author's job here is to
scan a list of articles and find one, not to browse.

1. `/desk` lists every article the signed-in author owns, one row each, with columns for
   title, category, visibility, published date and cover. Rows sit tight so a full list
   fits one screen.
2. The table lists only the signed-in author's own articles. Another author's article never
   appears in it, published or not.
3. A row opens `/desk/{id}` for editing. A row for an article the signed-in author does not
   own is refused by the server, and the article is unchanged.
4. With no articles the desk reads `You have not written anything yet.`
5. The desk carries one primary action, `Write an article`, which leads to `/desk/new`.
6. Every save, every publish and every refusal on the desk appears as an inline banner at
   the top of the surface, and stays until it is dismissed or replaced.

### Writing an article, at `/desk/new`

1. Writing an article leaves the table and opens `/desk/new` at its own address, so the
   list is never covered by a panel and the browser's back control returns to the list.
2. The form takes a title, a slug, a category, an excerpt, a body and a visibility, and
   accepts a cover image.
3. Visibility is one of exactly `draft`, `open` or `members`. A new article may be saved at
   any of the three.
4. A slug that another article already uses is rejected as invalid, the refusal names the
   slug field, and no article is created.
5. A missing title or a missing body is rejected as invalid and names the field.
6. Setting an article's visibility away from `draft` records its published date. Setting it
   back to `draft` clears the published date and removes it from every public list and
   every public route at once.
7. Editing at `/desk/{id}` changes the same fields and is refused for an article the
   signed-in author does not own.

### Cover images

1. Every article may carry one cover image. The bytes live in the object store and nowhere
   else: not on the app's filesystem, not in a database column.
2. The object key follows the scheme `covers/{article_id}/{sha256_of_bytes}.{ext}`, for
   example `covers/4/2b7c9e5f8a1d4c6b0e3f7a9d2c5b8e1f4a7d0c3b6e9f2a5d8c1b4e7f0a3d6c9b.png`.
   The article's record holds that key.
3. Replacing a cover writes a new object at a new key and the article points at the new
   key. The previous key is no longer the article's cover.
4. Covers are served by the app from one route, which reads the object and streams it after
   deciding whether the caller may have it. A link straight into the object store is never
   handed to a browser, and no time-limited address into the store is ever issued.
5. The cover of an `open` or `members` article streams to anybody.
6. The cover of a `draft` article streams only to the account that owns the article. Any
   other caller is refused, including a caller who has guessed or read the key.
7. Every seeded article carries a cover, generated by the app at seed time and written to
   the store under the same scheme. No image file ships with this application.

### The free trial signup, at `/signup`

1. The form takes a work email and a password, and its one action is labelled
   `Get started`.
2. The password field carries a control that shows and hides what was typed. It is a
   button, not a second field, and it says which it does.
3. The email is checked in the page before the form is sent and again by the server. The
   two must agree: an address the page accepts and the server refuses, or the other way
   round, is a defect.
4. A successful signup creates the `reader` account, signs the person in, and lands on
   `/signup/welcome`, which greets them by the display name and offers `/blog` and
   `/pricing`.
5. A refused signup keeps every typed value except the password, names the field that was
   wrong in words beside it, and creates nothing.
6. The route also carries the quieter action `Talk to an expert` and a link back to
   `/login` for somebody who already has an account.

### Search

1. The search trigger in the bar opens a field with the placeholder `Search` and a `Clear`
   control that empties it.
2. Submitting a query goes to `/search`, which lists matching results, each a title, the
   address it leads to and a short extract.
3. Search reaches articles that are published, the services catalogue and the marketing
   routes. It never returns a draft, to anybody, including its own author.
4. With no match the route reads `Nothing matched that search.`

### The press, events, partners and trust routes

1. `/press` lists dated releases, newest first, each a date, a headline and a summary, and
   closes on a media-contact block.
2. `/events` lists upcoming events, each a name, a date, a place and a registration note.
3. `/partners` describes the partner program as three tiers, `Registered`, `Select` and
   `Premier`, and carries one primary action leading to `/signup`.
4. `/trust` states the security and compliance posture as a grid of certification badges,
   each a drawn mark with its name, and links to the sub-processor list and the status
   note. It is also where `read about the methodology` from the statistics band lands, and
   it states how each of the five statistics was measured.
5. `/under-attack` is the emergency route the alarm control leads to. It states what to do
   while an attack is under way, carries the support line `(844) 4VELOCE`, and offers
   `/signup`.

### The privacy and terms routes

1. `/privacy`, linked from the footer of every route, states in plain words what `Veloce`
   records about a visitor: the email and password used to create an account, the display
   name shown beside an article, the cookie choice itself, and the language choice. It
   states that the site sends no message and shares nothing with another company, and it
   states how long each is kept.
2. `/terms` carries the long-form terms with a table of contents that jumps to each heading
   on the same page.

### The site's own not-found page

1. Any address the app does not have renders the site's own not-found page, wearing the
   same chrome as every other route, and the server answers not-found rather than a page
   that merely looks like one.
2. The page says in the site's own words that the address does not exist and carries a way
   back: a link to `/` and a link to `/blog`.
3. It is the stillest page on the site and carries no moving part.

### The cookie choice

1. A first-time visitor is asked once about non-essential cookies, in a card that floats
   above the page near one bottom corner. Its words are exactly:
   `We use cookies to personalize content, run ads, and analyze traffic. Read our Cookie Policy.`
   `Cookie Policy` leads to `/privacy`.
2. The card carries two controls, `Ok` and `No thanks`, and neither is hidden behind the
   other.
3. The answer is recorded against an opaque key the browser keeps, survives a reload, and
   the card does not return for that visitor.
4. The card never blocks the page behind it: every route is readable and every control is
   reachable while it is showing.

## User flow

**Routes.**

| Route | Purpose | Auth |
|---|---|---|
| `/` | the network and platform pitch | public |
| `/company` | who the team is, and the network story in short | public |
| `/pricing` | plans and the free tier | public |
| `/blog` | the article index | public |
| `/blog/{slug}` | one article | public; a members body needs an account |
| `/press` | dated releases and the media contact | public |
| `/events` | upcoming events | public |
| `/partners` | the partner program | public |
| `/trust` | security posture and how each statistic was measured | public |
| `/terms` | the long-form terms | public |
| `/privacy` | what the site records | public |
| `/under-attack` | emergency onboarding | public |
| `/search` | results for a typed query | public |
| `/signup` | create a free trial account | public |
| `/signup/welcome` | the confirmation the signup lands on | signed in |
| `/login` | sign in | public |
| `/desk` | the author's own article table | `author` |
| `/desk/new` | write an article | `author` |
| `/desk/{id}` | edit an article | `author`, own article only |

Any other address renders the site's own not-found page.

**Entry and redirects.**

- An unauthenticated request for `/desk`, `/desk/new` or `/desk/{id}` goes to `/login` with
  the destination preserved; signing in lands on that destination.
- A `reader` session reaching any `/desk` address is refused, told the desk belongs to
  authors, and offered `/blog`.
- An `author` session reaching `/desk/{id}` for an article it does not own is refused and
  the article is unchanged.
- Signing out returns to `/` and discards the token.
- A token that is no longer valid mid-action is refused, the record it aimed at is
  unchanged, and the person is returned to `/login` with the destination preserved.
- `/signup/welcome` reached without a session goes to `/signup`.

**Journeys.**

*Evaluate the platform and start a free trial.*
1. Open `/`. Read `Build, Secure, and Deliver. Instantly.`
2. Open the `Products` trigger in the bar. The panel drops. Move across its four tabs and
   read the thirty-two services.
3. Close the panel with escape and scroll to `A more powerful global network`. The globe is
   turning and its pins have arrived.
4. Scroll on. The five statistics count up once and settle at `<150 ms`, `5 trillion`,
   `90%`, `622 Tbps` and `32%`.
5. Scroll to the capability modules. The routing module abandons a congested path and reads
   `Congested region avoided. Every request took the fastest open path.`
6. Press `Try Veloce Free`. Land on `/signup`.
7. Type a work email and a password and press `Get started`. Land on `/signup/welcome`,
   signed in as a `reader`.

*Write an article, hold it back, then publish it.*
1. Sign in as `author@example.com` with `deku-demo-pw-2026`. Land on `/desk`.
2. Press `Write an article`. Land on `/desk/new`.
3. Type a title, a slug, a category, an excerpt and a body. Attach a cover image. Choose
   `draft`. Save.
4. The desk table shows the new row as `draft` and an inline banner confirms the save.
5. In a signed-out browser, open `/blog`. The new article is absent.
6. Back on the desk, open the row, change visibility to `open`, save.
7. `/blog` now lists it newest first, and its cover streams to a signed-out browser.

*A draft is refused by every route into it.*
1. Signed out, request `/blog/rewriting-the-purge-path`. Refused, and nothing about the
   article is disclosed.
2. Signed out, request that article through the API by its identifier. Refused.
3. Signed out, request that article's cover. Refused.
4. Sign in as `author2@example.com`. Repeat all three. Each is refused, because the article
   belongs to `author@example.com`.
5. Sign in as `author@example.com`. All three succeed, and the desk shows the article.

*The members wall.*
1. Signed out, open `/blog/edge-security-report-2026`. The category, title, author, cover
   and excerpt are there. The body is not, and `Try Veloce Free` is offered in its place.
2. Sign in as `reader@example.com`. Open the same address. The body is there.

*The cookie choice.*
1. Arrive at `/` for the first time. The cookie card appears once, near a bottom corner.
2. Press `Ok`. Reload `/`. The card does not return.

**States.** Every list has an empty state and the exact words are given above for `/blog`,
`/desk` and `/search`. Every route shows a loading state while its content is in flight,
and a list shows placeholder rows rather than a blank frame. Every refusal and every
confirmation appears as an inline banner at the top of the surface it belongs to and stays
until it is dismissed or replaced. A failed request never blanks the page, never shows a
raw error, and leaves the person somewhere they can act from.

## UI/UX notes

**The north star.** Somebody arriving here should understand within one screen that this is
a network, not a product page: that it is very large, very fast, and already carrying other
people's traffic, and that the claims on the page are measured rather than asserted.

**The register.** This is a consumer-facing marketing site whose subject is infrastructure,
so it carries atmosphere and the subject is seen before anything is read, while every
explanatory module inside it reads as instrumentation and stays quiet, plain and factual.
The two registers sit inside one page and must not blur: a capability module that starts
performing like a marketing panel has stopped being evidence, and a marketing section that
adopts the module's chrome has stopped being a page. The author's desk behind the sign-in
boundary is wholly the second register and carries no marketing composition at all.

**The stance is proof over claim.** A competing product could rationally hold the opposite,
lead with a promise and put its evidence in a datasheet, and be right for a simpler buyer.
This one is not that: wherever a sentence and a measured number could carry the same claim,
the number carries it and the sentence gets shorter, and every number on the page says when
it was measured.

**Mode.** The site commits to a light ground and is designed fully in it. There is no dark
mode and none is graded. The one exception is the chrome: the bar at the top and the block
at the bottom are the darkest surfaces on the site, and the opening band of the home route
joins them, so the page reads as a bright sheet held between two dark edges.

**Palette by role.** The page ground is a near-white warm neutral, nearer paper than white,
and it is the only ground: no section introduces a second background family. A card on it
is a plainer, lighter near-white neutral, and the two must stay visibly separate without a
shadow doing the work. The chrome, the opening band and the module stages are a near-black
neutral. Primary text is a deep neutral, near-black but warm rather than cold. Secondary
text is a mid warm neutral, strong secondary text a deep warm neutral, and a muted label a
light warm neutral; hairlines and a disabled ground are a near-white warm neutral. One
mid, vivid lime carries every primary action on the site and appears nowhere else: not as a
background, not as a heading, not as decoration. Its hovered state is a light, soft lime
and its pressed state a deep, soft lime; text sitting on it is a near-black, muted lime,
never plain white, because that pairing is the one that clears the contrast bar. A
mid, vivid blue means a word leads somewhere and means nothing else, and the same blue is
the accent inside a capability module. A mid, vivid red is the alarm and appears in exactly
two places, the `Under Attack?` control and the text of a refusal, and nowhere else: a
control that is merely important may not borrow it. A light, vivid orange belongs to the
statistic pills and to nothing else, and a second, softer light, vivid orange alternates
with it down the band. A deep, soft magenta and a deep, muted magenta are available to the
capability modules as a third and fourth data colour and appear nowhere outside them. A
near-white, soft cyan is the focus ring and is used for nothing else. Three meanings each
own one colour and appear nowhere else: the red for something refused, the deep lime for
something that worked, and the orange for something still in progress. A state that is none
of those three may not borrow any of them. Which exact shades carry all of that is yours to
settle, provided every exclusivity rule above survives the choice and the text on each one
clears the contrast bar.

**Type.** The typography carries three personalities, kept far apart. A heavy, characterful grotesque carries
display: the home headline, section titles and the statistic values, and it is the only
face that is ever large. A plain workhorse sans carries everything that is read or operated:
body copy, navigation, menu tiles, table cells, form fields. A typewriter-style face is
reserved for three things and appears nowhere else: the small eyebrow labels above a
section, the units and elapsed readouts inside a capability module, and identifiers such as
a slug or an object key. A heading set between the display and the body personalities has
missed the point. Figures line up in a column wherever amounts stack, which is the statistic
band, the capability readouts and the pricing comparison table. The exact families, sizes
and weights are yours, so long as the three personalities stay distinguishable at a glance
and body copy reads comfortably at arm's length.

**Shape.** The corner radius is barely softened on controls, inputs and cards, with three
deliberate steps: an input is softened least, a control one step more, a card one step more again. The
only fully rounded shape on the site is the small toggle chip. The menu panel is square
where it meets the bar and softened where it leaves it, so it reads as hanging from the bar
rather than floating near it. Elevation is carried by a low, wide, offset shadow and by a
hairline, never by a large soft blur: a card that reads as floating on a cushion has left
this system.

**Density.** The marketing routes are spacious: the subject is given room, and a section
reads as separate from the one below it at a glance without needing a dividing line. The
gap between two sections is several times the gap beneath a heading, and it closes to
roughly half on a narrow screen. The author's desk is compact, where rows sit tight so a
full list fits one screen and an author scans rather than scrolls. Every gap and every spacing step on the site
is a multiple of one base unit, which is yours to choose.

**Layout.** This is a top-navigation product. One bar sits across the top of every route,
two rows wide on a large screen, carrying utilities above and navigation below, and it does
not appear and disappear with scroll position. Menu triggers drop full-width mega-menu panels below it. One deep footer closes every route. Content sits in a centred column with a maximum
width, and a capability module too wide for that column scrolls sideways inside its own
frame rather than widening the page. The desk is the one surface that is not a centred
marketing column: it is a table filling the working width with its own action above it, and
writing an article leaves it for a route of its own rather than covering it with a panel.

**Motion.** The character is **eased**. Everything leaves quickly and settles slowly, with the
entrance and the exit both considered, so movement here reads as an instrument being operated
rather than a machine clattering or a toy springing back. Everything interactive moves at one speed on one family of curves, so
every transition on the site shares one duration and one character, quick enough not to be
waited for and slow enough to be seen, and nothing uses a different speed to feel special. Nothing on this site lurches and nothing hijacks the scroll: the page
moves under the reader in the ordinary way, no section pins itself, and no timeline is tied
to scroll position. The moments that animate at runtime are these and there are no others. A mega-menu
panel arrives by sliding a short distance down while fading in, and leaves by reversing it.
Sections and cards fade up a short distance as they first cross into view, once, and then
stay arrived; a section revealed this way is never revealed again. Two strips move
continuously and sideways on their own clock, the announcement rail and the trust wall, and
the statistics band becomes a third on a narrow screen; each loops forever in one direction
at an even pace, and the trust wall moves noticeably faster than the rail above it. The
globe turns. A pin arrives with one expanding pulse that fades as it grows. A live dot
pulses, shrinking and dimming and returning. A loading ring spins while its stroke chases
itself around the circle. The statistics count up once. A padlock shackle closes. Under a
reduced-motion preference every continuous loop holds still, every reveal resolves to its
finished state immediately, the globe stops turning, the counts are simply at their values,
and nothing is removed from the page to achieve any of it: the text a reveal would have
uncovered is already there.

**Components and their states.** Five states belong to every control on the site: resting,
pointed-at, pressed, focused, and unavailable. Colour alone never carries the last of them. One control shape carries four
variants and there are no others: the filled primary in lime, the outlined alternative
carrying a thin ring of the same family on the dark chrome, the alarm control carrying a
thin ring of the alarm red, and a plain text link. Each page leads with one
clear primary action and it is visually distinct from every secondary one on that page: the
home route's is `Get started`, the pricing route's is its free-tier action, the desk's is
`Write an article`, the signup's is `Get started`, and the not-found page's is the way back
to `/`. A page with two things competing to be the primary action has failed this rule. The
navigation items on the dark bar sit in a held-back off-white and rise to full white with
an underline when a pointer reaches them, and that rise is the site's one constant small
gesture. The search trigger inverts it and mutes instead of brightening, which is the only
place the site reverses the gesture. Escape closes an open mega-menu panel and returns focus
to the trigger that opened it. A destructive action, unpublishing an article or replacing a
cover, confirms first. Confirmation and refusal both appear as an inline banner at the top
of the surface they belong to, and the banner stays put until somebody dismisses it or another
banner takes its place. An announcement that removes itself is used nowhere on this site.

**Accessibility floors, which are requirements rather than preferences.** Body text and the
surface under it clear the WCAG AA contrast bar everywhere the two meet: on the near-white
ground, on the near-black chrome and on the lime action. Every interactive element is reachable and operable by keyboard navigation in
visible source order, with a focus ring that is clearly visible on both the near-white
ground and the near-black chrome. A mega-menu panel opens on focus, keeps focus inside
itself while open, and closes on escape. Touch targets are comfortably sized. Icon-only controls
carry labels: the search trigger, the language control, the password reveal and the
back-to-top control all say what they do. Meaning is never carried by colour alone, which
is why the alarm control carries its own words and why each statistic pill carries text
rather than relying on the colour of its ground. Every content image carries alternative
text and decorative images declare themselves decorative; the globe and every capability
module carry a text alternative that states the claim rather than describing the drawing.
Every form field carries a programmatic label, and a refusal is announced as well as shown,
naming the field in words.

**Responsive.** The site is designed to hold at every width, and it sheds arrangement
deliberately rather than by accident as the viewport narrows. At the widest width the bar
runs in two full rows, card grids run three across, and the globe sits beside its copy. At
the middle width the grids fold to two across and the globe moves above its copy. At the
narrow width everything becomes a single column, the bar collapses to the wordmark plus a
menu control, the menu panels become one full-screen stacked drawer, the statistics band
becomes a sideways-moving strip, and the cards stack. At that narrow viewport nothing
overflows sideways, the page never scrolls horizontally, and every navigation target stays
reachable. Pointer and touch are told apart, so every affordance that opens on hover opens
on tap where there is no pointer, and no part of the site is reachable only by hovering.
Where each boundary sits is yours.

**What it must not look like.** A page ruled by one hue family, with no second signal beside
it, is the first failure. Decoration filling space that content should have held is the second.
A capability module drawn as a picture rather than built from the same system as the chrome
around it is the third, because a module
that does not match the rest of the site stops reading as instrumentation and starts
reading as an advertisement, which is the one thing this site cannot afford. Not a
marketing composition inside the desk, where a working surface belongs. Not a page whose
primary action has to be hunted for.

## Front-end specification

This section describes the surfaces in detail. It says what each one is made of and how it
behaves; the values that make it so are yours, within the rules above.

**The top bar.** Full width, the darkest surface on the site, and the same on every route.
It holds two rows on a wide screen. The upper row is right aligned and holds, in this order:
a globe glyph beside the current language; the `Under Attack?` control, which is outlined by
a thin alarm-coloured ring rather than filled, so the alarm reads as an alarm without
shouting; the support line; `Support Center`; and `Log in`. The lower row holds the wordmark
at the far left, then the seven menu triggers and the flat `Pricing` link, then the search
trigger, then the two buttons. Below the widest tier the two rows become one plus a menu
control, and the upper row's utilities move inside the drawer. The bar's own border and its
item labels sit in a held-back off-white and rise to full white on hover, the language
control's outline lifts from the chrome colour to the lime when it is pointed at, and the
search glyph mutes rather than brightens.

**The mega-menu panel.** A trigger drops a mega-menu panel the full width of the page, grounded in the
plain light surface so it reads as a sheet of the page pulled down over the chrome, square
where it meets the bar and softened at its lower corners, lifted by a low offset shadow. The
`Products` panel is split: a column of four family tabs on one side, and the tiles of the
selected family beside them. A tile is a service name over its description, the name set
larger and heavier than the description, the whole tile a single target. The `Why?` and
`Resources` panels use the same tile but no tabs. On a touch screen the panel is a
full-screen stacked drawer: the families become collapsible groups and the tiles stack.

**The footer.** The deepest block on the site, sharing the chrome's ground. It opens on
`Get in touch or create an account` set in display type, with the primary action beside it.
Below that, link columns mirror the menu taxonomy family by family. The closing row carries
`Terms`, `Privacy`, the language control again and the social marks, separated from the
columns above by a hairline rather than a change of ground.

**Iconography.** Six glyphs carry the interface and all six are drawn as geometry on one
grid at one stroke width, taking their colour from the text around them so one glyph serves
both the dark chrome and the light page. They are: a magnifier, a circle with a handle
running out of it at a diagonal, for search; three stacked horizontal bars, the hamburger, for the mobile menu control; a filled disc with a downward chevron knocked out of it, for a menu expander; a
right-pointing arrow with a shaft and a head, for a link forward; an outline globe, a circle
crossed by one horizontal line and two curved meridians, for the language control; and a
loading ring, a single stroked circle whose stroke chases itself around the circle while it
spins. No glyph is an image file, and none carries its own colour.

**The wordmark.** Set type, not a picture: the product name in the display face at its
heaviest, letter-spaced, white on the chrome and the deep neutral on the page. There is no
logo file anywhere in this application.

**The opening band of the home route.** The dark ground continues from the bar with no seam.
The headline is the largest type on the site and scales with the width of its column rather
than stepping between fixed sizes. The sub-line sits under it at reading size. The two
actions sit below that, the filled primary and the outlined alternative, side by side on a
wide screen and stacked on a narrow one. A generated illustration fills the other side of
the band: a motif of stacked, rounded, overlapping blocks drawn as vector shapes in the
lime, the blue and the alarm red, composed from a fixed seed so it is the same on every
load. It is decorative and declares itself so.

**The two moving strips.** The announcement rail is a row of small chips, each a short
award or news line. The trust wall is a row of customer marks, each a generated
wordmark-shaped block rather than a fetched logo. Both run continuously sideways in one
direction with an even, unchanging pace and no pause, and both loop seamlessly so no gap
ever appears at the join. Both hold still under a reduced-motion preference.

**The statistics band.** Five pills in a row across the full content width. Each pill
carries the qualifier in the small typewriter-style face along its top, the value in the
display face at the largest size on the page after the headline, the caption in reading type
below it, and a small superscript reference mark after the caption that reveals the measurement date. The
pill grounds alternate between the two oranges and the blue down the row, and the text on
each is chosen so it clears the contrast bar on the ground it sits on rather than by rule of
thumb. On a narrow screen the row becomes a strip that moves sideways on its own.

**A capability module.** All eight are diagrams and share one frame so they read as one
instrument. Each is a
monochrome stage on the near-black neutral, filling the content width, with the module title
above it in display type, its claim beside it in reading type, and its result line below it
in the typewriter-style face so the outcome reads as a readout rather than as copy. Inside
the stage, exactly one data colour is loud at a time and everything else is neutral: the
lime for the healthy path, the red for hostile traffic, the blue for the live feed, and the
two magentas where a module needs a third and fourth. Elements are dots, arcs, bars, a dense
field of small squares, a mesh of nodes, a polyline, a perimeter outline and a padlock, all
drawn as vector geometry. Where a module has a control, it is a single labelled toggle or a
single pointed-at region, never a control panel. Where a module has a counter, the counter
sits in the typewriter-style face and its digits do not shift the layout as they change. A
module too wide for the content column scrolls sideways inside its own frame.

**The globe.** An outline sphere: one circle for the limb, meridian arcs across it, a group
of small pin marks at fixed positions standing for points of presence, and one thin
elliptical ring passing in front of the sphere on one side and behind it on the other. The
sphere and its meridians are the deep neutral on the page ground, the pins are the alarm
red, and the ring is a light warm neutral hairline. The meridian group turns; the pins and
the ring do not counter-rotate independently of it.

**Cards.** Three card shapes, all sharing one softening and one hairline. An industry card
is a generated warm gradient thumbnail above a title and a body paragraph. A reading card is
a generated warm gradient thumbnail above a category eyebrow in the typewriter-style face, a
title in display type, an excerpt in reading type, and a forward-arrow link. A plan card on
the pricing route is a plan name, a price line, a list of included capabilities each with a
leading mark, and one action. Every generated thumbnail is keyed by a per-card seed so no
two cards on a page carry the same gradient, and every one of them is composed in code.

**Forms.** One field shape across the site: a label above the field, the field itself a
plain surface with a hairline that thickens on focus and gains the focus ring, and a line of
help or refusal text below it that is reserved whether or not it is showing, so a refusal
never moves the fields under it. A refusal names the field in words and marks it with more
than colour. The password field carries the reveal control inside its trailing edge, drawn
as a glyph with a label, muted at rest and lifting when the field has focus. The signup's
action is the full width of the form on a narrow screen.

**The desk table.** A header row in the small typewriter-style face over tight rows, each
row a title, a category, a visibility chip, a published date and a small indication of
whether a cover is attached. The visibility chip carries its word, `draft`, `open` or
`members`, and its shape and its word are what distinguish it, not its colour alone. The
whole row is the target that opens the article. The primary action sits above the table on
the right of its own line. The inline banner appears between the action line and the table
header, pushing the table down rather than covering its first row.

**The not-found page.** The chrome, one line of display type saying the address does not
exist, one line of reading type offering the way back, and the two links. Nothing on it
moves.

**Loading and empty states.** A list that has not arrived shows placeholder rows of the same
height as real ones, so nothing jumps when the content lands. A route that has not arrived
shows the loading ring centred in the content column. An empty list shows its exact words
from the sections above, centred, in reading type, with the surface's primary action beneath
it where the surface has one.

**The back-to-top control.** A small square-ish control with softened corners carrying an
upward arrow glyph and a label, fixed near the trailing bottom corner of the viewport, absent
until the page has been scrolled and arriving with the same eased character as everything
else.

## Technical requirements

The browser receives an application shell and fetches everything it shows as JSON from the
same origin under `/api`. Nothing is rendered on the server: the first paint is the shell's
own markup, and every route's content arrives from the API afterwards.

- **Frontend: Angular**, compiled to a production bundle at image build time and served as
  static assets by the backend process.
- **Backend: Litestar** on Python, serving the JSON API under `/api` and serving the built
  frontend for every other path, so a direct request for `/blog/modern-cdn-explained`
  returns the shell rather than a dead end.
- **Database: PostgreSQL**, reached at `DATABASE_URL`.
- **Object store: MinIO**, reached at `STORAGE_ENDPOINT` with `STORAGE_BUCKET`,
  `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. It is the only place cover bytes live.
- **Auth:** email and password held by this app, with bearer tokens that stop working at
  sign-out. No external identity provider.
- **Health:** `GET /api/health` returns `200` once the app is ready, which means the
  database answers, the bucket answers, and seeding has finished.
- **Logging:** one structured line per request on stdout carrying the method, the path, the
  status and the elapsed time. No password, no token and no object key ever appears in a
  log line.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing
services available in this environment are PostgreSQL and MinIO, and reaching for anything
else is a contract violation.

Read every host and port from the environment. Never hardcode one.

Every font the site uses is installed from the package registry at image build time and
served from this application's own origin. No font file ships with this brief and no font
host is reached while the app is running. Text is visible immediately in the fallback stack
and reflows once when the intended face arrives.

No image, icon, logo, badge or illustration is a binary file. Every one of them is drawn as
vector geometry or composed in code from a fixed seed, including the seeded articles'
cover images, which the app generates at seed time and writes into the bucket.

The application makes no outbound network call while it is running. The statistics, the
capability modules and the services catalogue are read from this app's own content, and
there is no third-party chat, consent, analytics or tag anywhere in it.

The first thing a visitor sees is text and colour with no media in front of it, so nothing
downloadable delays it. Performance is a requirement rather than an aspiration: continuous motion holds a steady
frame on an ordinary three-year-old laptop, nothing off screen is animating, and no image
below the first screen is fetched until it is needed.

## Data model

Nine tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture
data, not a secret. Hash it as normal; the exact literal must work at login, and it must be
written into `/app/USER_README.md` alongside each account so a grader can sign in.

**account** - `id`, `email` (unique, stored lowercased), `display_name`, `password_hash`,
`role` (one of `author`, `reader`), `created_at`. The password hash is returned by no
endpoint. Signup always writes `reader`.

**article** - `id`, `slug` (unique), `title`, `excerpt`, `body`, `category`, `visibility`
(one of `draft`, `open`, `members`), `author_id` referencing `account`, `cover_key`
(nullable), `published_at` (nullable), `created_at`. `published_at` is set when visibility
leaves `draft` and cleared when it returns, so it is never set on a draft. The article's
reading time, if it is shown, is computed on read rather than stored.

The visibility rules are properties of the running system, not of any one screen:
- An article whose visibility is `draft` is readable only by the account in `author_id`.
  It is absent from every public list, it is not served by its slug, it is not served by
  its identifier, it is not returned by search, and its cover is not streamed. Each of
  those is a separate route into the record and each must refuse independently.
- An article whose visibility is `members` serves its title, category, author display name,
  published date, excerpt and cover to anybody, and its body only to a signed-in account.
- An article whose visibility is `open` serves everything to anybody.
- A slug identifies exactly one article at a time. Two articles may not hold the same slug,
  and an attempt to take a slug another article holds is rejected as invalid.

**statistic** - `id`, `position` (unique, `1` to `5`), `qualifier`, `value`, `caption`,
`measured_on`. Rendered in `position` order.

**capability** - `id`, `position` (unique, `1` to `8`), `slug`, `title`, `claim`,
`result_line`. Rendered in `position` order.

**service** - `id`, `family`, `position`, `name`, `blurb`. `family` is one of
`Network Services`, `Security`, `Compute`, `Observability`, and `(family, position)` is
unique. Thirty-two rows: thirteen, six, seven and six respectively.

**press_release** - `id`, `headline`, `dated_on`, `summary`. Listed newest first.

**event** - `id`, `name`, `starts_on`, `place`, `registration_note`. Listed soonest first.

**partner_tier** - `id`, `position` (unique), `name`, `summary`.

**cookie_choice** - `id`, `visitor_key` (unique), `accepted`, `decided_at`. One row per
visitor key. A second answer from the same key replaces the first rather than adding a row.

**Seed data.**

| Email | Display name | Role |
|---|---|---|
| `author@example.com` | `Marisol Quint` | `author` |
| `author2@example.com` | `Teodor Vance` | `author` |
| `reader@example.com` | `Ingrid Salas` | `reader` |

| Slug | Title | Visibility | Author |
|---|---|---|---|
| `modern-cdn-explained` | `What is a modern CDN and why is it important?` | `open` | `author@example.com` |
| `fewer-stronger-locations` | `Fewer locations, more power` | `open` | `author2@example.com` |
| `edge-security-report-2026` | `The 2026 edge security report` | `members` | `author@example.com` |
| `rewriting-the-purge-path` | `Rewriting the purge path` | `draft` | `author@example.com` |
| `streaming-migration-diary` | `Streaming at the edge, a migration diary` | `draft` | `author2@example.com` |

Every seeded article carries a generated cover in the bucket under its scheme's key. The
five statistics are seeded exactly as listed in `## Core features`, with their qualifiers,
values, captions and measurement dates. The eight capabilities are seeded with their titles,
claims and result lines exactly as listed there. The thirty-two services are seeded with
their families, names and descriptions exactly as listed there. Three press releases, three
events and the three partner tiers `Registered`, `Select` and `Premier` are seeded.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Constraints

- One company, one site. There is no tenancy, no workspace and no organisation.
- No payment of any kind: no card, no plan purchase, no invoice, no billing record.
- No message of any kind: no email, no SMS, no push, no in-app inbox. Nothing the site does
  sends anything to anybody.
- No third-party chat launcher, no third-party consent platform, no analytics vendor, no
  tag manager, no social embed.
- No outbound network call at run time.
- No real translation. The language control lists the locales and records the choice.
- No comments, no likes, no followers, no sharing, no notifications.
- No article scheduling, no revision history, no co-authoring, no draft sharing link.
- No native application and no offline mode.
- No binary asset ships with the application. The site is zero-asset, and every image class
  has a drawn or generated substitution rather than a file.
- The site must stay responsive with thirty-two services, eight capability modules, five
  statistics and a few hundred articles.

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
successful call returns the named resource or shape; an invalid or unauthorized call is
rejected as a client error, never a server error and never a silent success. Bearer auth on
everything except login, signup, health and the public read surface, sent as the
`access_token` value the login answered with.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{ email, password }` | `{ access_token, account: { id, email, display_name, role } }` |
| `POST /api/auth/login` | `{ email, password }` | `{ access_token, account: { id, email, display_name, role } }` |
| `GET /api/me` | | `{ id, email, display_name, role }` |
| `GET /api/statistics` | | `[ { position, qualifier, value, caption, measured_on } ]` |
| `GET /api/capabilities` | | `[ { position, slug, title, claim, result_line } ]` |
| `GET /api/services` | `family` optional | `[ { family, position, name, blurb } ]` |
| `GET /api/articles` | `category` optional | `[ { id, slug, title, excerpt, category, visibility, author_name, published_at, cover_url } ]` |
| `GET /api/articles/{slug}` | | `{ id, slug, title, excerpt, body, category, visibility, author_name, published_at, cover_url }`; `body` absent for a members article read without a session |
| `POST /api/articles` | `{ slug, title, excerpt, body, category, visibility }` | the created article |
| `PATCH /api/articles/{id}` | any of the above fields | the updated article |
| `POST /api/articles/{id}/cover` | the image bytes | `{ id, cover_key, cover_url }` |
| `GET /api/articles/{id}/cover` | | the image bytes, streamed |
| `GET /api/desk/articles` | | the signed-in author's own articles, drafts included |
| `GET /api/press` | | `[ { headline, dated_on, summary } ]` |
| `GET /api/events` | | `[ { name, starts_on, place, registration_note } ]` |
| `GET /api/partner-tiers` | | `[ { position, name, summary } ]` |
| `GET /api/search` | `q` | `[ { title, path, excerpt } ]` |
| `POST /api/cookie-choice` | `{ visitor_key, accepted }` | `{ visitor_key, accepted, decided_at }` |
| `GET /api/cookie-choice` | `visitor_key` | the recorded choice, or an empty result |
| `GET /api/health` | | `200` once ready |

**No mocks.** MinIO is named in this brief because the cover bytes must actually be there.
An in-memory dictionary of images, a base64 column in the database, a folder on the app
container's filesystem, a generated data URL returned in place of a stored object, or a
cover route that answers itself without reading the store are each a contract violation
however correct the page looks. The named provider is the fact - the app's UI and its own
tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A visitor can open the product menus, read all thirty-two services, watch the globe turn
beside the network story, see the five statistics count up to their measured values, read a
capability module's result in words, and create a free trial account from the signup form.
An author can write an article with a cover image whose bytes live in the object store, hold
it back, and publish it. An article held back is invisible to everybody else by every route
into it, including its cover, and an article behind the members wall shows its opening to a
visitor and its body only to somebody signed in.
