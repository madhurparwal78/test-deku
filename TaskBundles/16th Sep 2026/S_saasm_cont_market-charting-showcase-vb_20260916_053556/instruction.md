# Marketscope

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, watch the live market summary move without reloading the page, create a free account from the sign-up form, and read a published trading idea with its chart snapshot, without hitting an error page. The hard part is the boundary around unpublished work: an idea that is still a draft, and the snapshot image attached to it, must be readable by its own author and by nobody else, and the snapshot bytes must live in the MinIO bucket at the key scheme pinned below. A copy of those bytes on the app container's own filesystem, or a row in PostgreSQL holding the image itself, is not the object store and does not count.

## Overview

Marketscope is the public storefront for a multi-market charting and analysis platform, and it carries the community surface that storefront advertises. Its audience is in four parts: retail traders and investors asking whether they can watch and analyse their markets here, strategy builders asking whether they can write and test their own tools, futures traders after real-time exchange data, and the community that comes for other people's ideas. Returning users arrive to sign in and resume.

The home route opens on a near-black orbital hero, drops into a live market summary of world indices, crypto, currencies and rates, runs on into a river of community trading ideas and market news, and closes on a sign-up call to action. A second route sells real-time CXE Group futures data. A third states the six product capabilities the platform is built on. Authors publish ideas: a title, a thesis, a symbol, a long or short bias, tags and a chart snapshot. Readers sign up free, read, and boost what they like.

What it deliberately is not: there is no brokerage and no order routing, no money movement, no in-browser script editor, no backtest runner, no chart drawing tools, no direct messaging, no follower graph, no email of any kind, no third-party analytics and no video.

The genuinely hard part is that a draft idea is private property. The idea row, the idea page and the snapshot object are all closed until the author publishes, and publishing is the single act that opens all three.

## User roles

| Role | Can do |
|---|---|
| Visitor (signed out) | Read the home, markets, futures, platform and ideas routes; read any published idea and its snapshot; answer the cookie question; sign up; sign in. **Cannot boost, cannot compose, cannot read any draft idea or any draft snapshot, cannot reach the studio.** |
| `reader` | Everything a visitor can do, plus boost a published idea once and see the boosted ideas on the account route. **Cannot compose, publish, or read another account's draft; cannot reach the studio.** |
| `author` | Everything a reader can do, plus compose ideas in the studio, attach a snapshot, save a draft, read and edit their own drafts, and publish them. **Cannot read, edit, publish or delete an idea owned by another account.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a `reader` session to any `author`-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Signup is open. Anyone may create an account from `/signup` and choose whether it is a `reader` or an `author` account; no invitation and no approval step exists. The seeded accounts below already exist and every one of them uses the password `deku-demo-pw-2026`:

| Email | Role | Display name |
|---|---|---|
| `author@example.com` | `author` | `Dana Holt` |
| `author2@example.com` | `author` | `Priya Raman` |
| `reader@example.com` | `reader` | `Sam Okafor` |

## Core features

### Auth

Accounts are email and password, implemented by this app. A successful sign in returns a bearer token the client sends on every later request; the token expires after twelve hours and an expired token is refused. Passwords are stored hashed, never in clear text. Signup takes an email, a password and a role, lowercases the email, and rejects a second account on an email already taken with a message naming the field. There is no password-reset flow and no email is ever sent.

1. Signing up with an unused email succeeds and returns a usable token. Signing up again with the same email is rejected as invalid with a message naming the email field, and no second account row exists.
2. Every form on the site rejects invalid input inline, names the field that is wrong, and writes nothing: a sign-up submitted with an empty password, a compose form submitted with no title, and a sign-in submitted with an unknown email all leave the database exactly as it was.

### Live market summary

The home route's centrepiece, under the title `Market summary`. It carries the primary `S&P 500` (`SPX`) area chart, a `Major indices` list, and three sparkline cards for crypto, the US dollar and yields. Every value on this surface arrives as a subscription to the app's own market feed, not as a page-load snapshot.

3. A ticker card updates its value, its signed change and its direction colour in place as ticks arrive, without reloading the page and without re-laying out its neighbouring cards. Rising values render in the rising signal colour, falling values in the falling signal colour, and the two are never transposed.
4. `GET /api/markets/summary` returns a top-level JSON array, one entry per seeded symbol, each carrying `symbol`, `value`, `unit`, `change`, `direction`, `session` and `timestamp`. `direction` is `up` or `down` and drives the signal colour; `session` is `open`, `closed` or `holiday` and drives the market-status glyph; `timestamp` is the authoritative server time the client aligns the value to, never the browser clock. An entry missing any of those seven names, or carrying a `direction` that disagrees with the sign of its `change`, is a broken surface.
5. The primary chart preview is a filled area series over a time axis, drawn in the session's direction colour, and it pans its visible window as new ticks arrive rather than redrawing the whole series. A preview that redraws the page, or that holds one fixed window while the feed moves, is not this chart.

### Publishing an idea

An `author` composes an idea from the studio. Composing opens a dialog over the studio table rather than navigating away. An idea carries a title, a thesis, a symbol, a bias of `long` or `short`, up to five tags and exactly one chart snapshot image.

6. `POST /api/ideas` creates the idea with status `draft`, derives a unique kebab-case slug from the title, and returns it. The snapshot is attached by `POST /api/ideas/<slug>/snapshot`, which writes the image bytes into the MinIO bucket at `ideas/{idea_id}/{sha256_of_bytes}.{ext}`, for example `ideas/42/9f2a1c7e0b4d8a63f5e2904c7b1d6a8e3f0c95b27d4e81a6c3f97b0d25e4a1d0.png`. The idea row stores the key, never the bytes. Attaching a snapshot to an idea owned by another account is denied and no object is written.
7. `POST /api/ideas/<slug>/publish` moves the idea to status `published`, stamps `published_at`, and makes both the idea page and its snapshot publicly readable. Publishing an idea that has no snapshot is rejected as invalid with a message naming the snapshot. Publishing an idea owned by another account is denied and the idea stays a draft.
8. **Draft protection, the rule this product is built around.** While an idea is a draft, `GET /api/ideas/<slug>` and `GET /api/ideas/<slug>/snapshot` answer only the owning author's session. An anonymous request, a `reader` request and a request from a second author are all denied and return no bytes and no idea body. The draft never appears in `GET /api/ideas`, which returns published ideas only, newest first. Once published, the same two endpoints answer anyone.
9. Publishing the same draft twice does not create a second idea, a second slug or a second stored object: the second call leaves exactly one published idea, and the stored key is unchanged. Two publish requests for the same draft arriving at the same moment must not both be accepted; exactly one succeeds and the other is rejected with a message naming the conflict.

### Reading and boosting

10. `GET /api/ideas` returns a top-level JSON array of published ideas, newest first, each with `slug`, `title`, `symbol`, `bias`, `tags`, `author_display_name`, `comment_count`, `boost_count` and `published_at`. The ideas river on the home route and the `/ideas` route both read from it. A listing that carries a draft, that omits a published idea, or that orders oldest first is wrong on all three counts.
11. `POST /api/ideas/<slug>/boost` from a signed-in account raises that idea's boost count by exactly one. The same account boosting the same idea again is a no-op: the count does not move and no second boost row exists. An anonymous boost is denied. An idea's boost count always equals the number of accounts that have boosted it.

### The futures route

12. `/futures` carries the CXE Group real-time futures landing: the hero words `Explore` and `real-time futures`, the lead `If you're looking to uncover the vast opportunities that futures trading offers, then you've come to the right place.`, the price `591 INR per month` shown with `for non-professional subscribers only`, and a `Subscribe` action reading `to real-time CXE Group futures`. The price is held as integer minor units in `inr`; `591 INR` is `59100`, not `591.00` and not `591`. A page missing any of those four strings, or showing the price in major units, fails the route.
13. The asset-class matrix under the title `Track and trade all major asset classes` carries nine tabs: `Equity indices`, `Metals`, `Micro futures and options`, `Interest rates`, `Energy`, `Cryptocurrency`, `FX`, `Agriculture` and `ESG`. Each tab shows representative symbols and the two metric labels `Average daily volume` and `Average daily notional volume`, plus `Open Interest` where the symbol has it. Selecting a tab swaps the card without navigating away and without losing the reader's place on the page.
14. The closing data-access band states that CXE Group data is free with a ten-minute delay and that the subscription unlocks real-time global commodities, and repeats the `Subscribe` action beside a `See every market in real time` link into `/markets`. A band that states the delay without repeating the action, or that links nowhere, leaves the offer unfinished.

### The platform capability page

15. `/platform` states the six capabilities the storefront sells, each in its own block, each linking out to the application: the high-performance charting engine that draws very large series smoothly while the user zooms and pans; `Beamscript`, the custom scripting language in which users write their own indicators and strategies; real-time global market data that streams live prices across world markets; the backtesting engine that runs a strategy against historical data and reports how it would have performed; the social and sharing layer that lets millions of users publish, discover and discuss; and cross-device and cross-session sync that keeps layouts, drawings and settings identical everywhere a user signs in. None of the marketing routes hard-codes a price, a value or a count that should be live.

### Cookie choice

16. A first-time visitor is asked once, in a dismissible band above the footer, whether non-essential cookies are allowed. The answer, accept or refuse, survives a reload and every later route: the band does not appear a second time for a visitor who has answered. Refusing is as easy to press as accepting and neither is hidden behind the other.

### Not-found chrome

17. An unknown address renders the product's own not-found page and answers not found: the word `coordinates` set as the last word of the headline, the line `Could you have found the void? Let's chart a safer course for home.`, and a round button reading `Set course for home` that returns to `/`. The global header and footer wrap it unchanged, so a lost visitor is never stranded on a bare error screen.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Home: orbital hero, feature chips, market summary, ideas river, top stories, closing call to action | public |
| `/markets` | Every tracked symbol, grouped by asset class | public |
| `/futures` | CXE Group real-time futures landing | public |
| `/platform` | The six product capabilities | public |
| `/ideas` | Published ideas, newest first | public |
| `/ideas/<slug>` | One idea and its chart snapshot | public when published, owner only while draft |
| `/studio` | Author workspace: a table of the author's own ideas, draft and published | `author` |
| `/studio/published/<slug>` | Confirmation page after a publish | `author` |
| `/signup` | Create a free account | public |
| `/login` | Sign in | public |
| `/account` | The signed-in account: boosted ideas and the cookie answer | `reader` or `author` |
| any other path | Not-found chrome | public |

**Entry and redirects.** A signed-out request for `/studio` or `/account` lands on `/login`, and a successful sign in returns to the route that was asked for. A sign in with no pending destination lands an `author` on `/studio` and a `reader` on `/account`. Signing out returns to `/`. A token that expires mid-action returns the visitor to `/login` with the form contents preserved, and nothing is written. A `reader` who reaches `/studio` is refused with a message saying the studio belongs to author accounts, not redirected quietly into it. A signed-out request for a draft idea's page renders the not-found chrome rather than revealing that the idea exists.

**Journeys.**

1. A visitor opens `/`, scans the `Market summary` while the values move, opens the `Products` menu in the header, follows it to `/platform`, presses `Get started for free`, submits the sign-up form on `/signup` with a fresh email and the password `deku-demo-pw-2026`, and lands signed in on `/account` with the header now showing their account.
2. `author@example.com` signs in, opens `/studio`, presses the compose action, fills the dialog with a title, a thesis, the symbol and a `long` bias, saves it as a draft, attaches a chart snapshot, and sees the row appear in the studio table marked as a draft.
3. The same author presses publish on that row and lands on `/studio/published/<slug>`, a full page confirming the publish and offering the public idea link. The idea now appears at the top of `/ideas` and in the home ideas river.
4. `reader@example.com` signs in, opens `/ideas`, opens `Gold Breakout Watch`, presses boost, and the count rises by exactly one. Pressing boost again leaves the count where it is.
5. A signed-out visitor requests the snapshot of `Copper Squeeze Setup`, which is still a draft, and is refused; no image bytes are returned.
6. A visitor opens `/markets`, narrows the list to one asset class, follows the header back to `/`, and finds the same symbols streaming in the `Market summary` there.

**States.** Every list has an empty state that says what would appear there and offers the action that creates it: an author with no ideas sees an empty studio table inviting a first idea, and a reader who has boosted nothing sees an empty account list. Every route has a loading state, and the hero paints before the market feed has connected, with the ticker cards filling in afterwards rather than the page waiting on them. Errors render inside the page chrome with a plain sentence and a way onward; nothing ever renders a blank screen or a raw error dump.

## UI/UX notes

**North star.** Somebody arriving should understand within one screen that these markets are actually moving, and should feel they are looking at a professional instrument rather than a brochure.

**Register.** A consumer storefront standing in front of an operational instrument. The marketing routes may carry atmosphere, and the subject, the moving market, must be the first thing seen; the studio table and the market surface read quiet, dense and work-focused. Calm over expressive on the data surfaces, atmosphere over restraint on the two heroes.

**Two-faced by design.** The marketing routes are near-black: the home hero sits over a night-side Earth with an aurora, and the dominant painted surface is a near-black neutral with body copy in a near-white neutral. The data surfaces invert to near-white neutral cards with the ground's own near-black neutral for copy. A page must never read as half-committed between the two: a section is either a dark marketing surface or a light data surface, and the change happens at a section boundary.

**Colour by role, and by exclusivity.** One brand blue, a light and vivid blue, carries every primary action on every route and appears nowhere else; its hover is the same blue a shade deeper, a mid and vivid blue. Inline links on dark are a lighter cut of that vivid blue and move a step deeper on hover. Two colours and only two carry price direction: a light, vivid red for falling and a mid, soft teal that reads as green for rising, with a deeper mid, vivid red for the pressed down-state. They mean direction and nothing else, and they are never transposed. A mid, vivid orange means warning and carries the notification dot. Secondary copy on dark is a mid neutral and timestamps a darker mid neutral; raised surfaces and control hovers on dark are a deep neutral, the pressed state a lighter deep neutral, and control borders a lighter deep neutral again; the hover fill on light controls is a hairline near-white neutral. The accent set, a vivid cyan, a vivid violet, a vivid indigo, a vivid teal, a second vivid blue, a vivid red, a vivid orange and a light, soft green, appears only inside gradients on headline words and card titles, never as a flat fill. The exact values are yours, so long as they hold the roles and the exclusivity rules above.

**Against the default.** No page dominated by a single hue family with no second signal. No decoration standing in for content on the data surfaces. No marketing composition where the working interface belongs: the studio is a table, not a landing page.

**Typography.** `Onest`, one geometric grotesque, in a regular and a semibold weight only, over a system sans-serif fallback stack. Size and colour do all the work a second family would do. The rendered scale is `14px` over `18px` regular for body copy as the default; `16px` over `24px` medium for emphasised body and menu items; `12px` over `16px` regular for captions and ticker units; `16px` over `24px` semibold for card titles and lead-ins; `18px` over `24px` semibold for section sub-headings; `11px` over `16px` semibold for tags and eyebrow labels; `28px` over `36px` semibold for a card headline; `36px` over `44px` semibold for a route sub-hero; `48px` over `56px` semibold for a section title; and `24px` over `24px` regular for a large price readout. The two heroes are fluid display sizes anchored at the `48px` step and growing with the viewport. Figures line up in a column wherever prices stack, so a list of indices scans down its decimal point.

**Shape and density.** Corner radius is the most expressive token in the system and it tells the reader what a thing is: text buttons and footer link items are barely softened, tags and light buttons a little more, card tabs and editors-picks blocks more again, idea cards and the crypto container are generously rounded, search and language and primary round buttons are full pills, and avatars, notification counters and circular icons are true circles. The base unit is yours; the ordering is not. Space over dividers: sections read as separate at a glance without a rule between them. Shadows barely exist, and where one appears it is shallow and close rather than a soft cloud. Density is comfortable on the marketing routes and compact on the market surface and the studio table, where rows sit tight enough that a full list of indices fits one screen.

**Motion.** One duration and one easing govern almost everything: the house ease is slow-in and slow-out, about half a second, and it is the default transition applied to anything that expands or reveals. A gentler ease-out that settles gently carries small discrete transforms; a springy ease with a slight overshoot belongs to toggles, and a stronger overshoot to the boost control alone; one ease-in that accelerates away carries things leaving. Nothing uses a different speed to feel special. The named moments, and only these, animate on a loop: a gradient title sweep slides horizontally across one headline word; the partner card glow breathes between two extents; an arrow bubble drifts up and down around its centre; a spinner turns once per iteration, linear, while something loads. Sections fade and translate in on enter, once, then stay arrived. Boosting launches a flame glyph away while a filled twin lands in its place. A reduced-motion preference stills every one of them, including the reveal, and leaves the state change itself intact. The exact timings are yours so long as everything shares one character.

**Accessibility.** A `Skip to main content` control is the first focusable element on every route. Body text meets WCAG AA contrast against both the near-black ground and the near-white cards. Every interactive control is reachable and operable by keyboard navigation with a visible focus ring, and icon-only controls carry a text label for assistive technology. Colour is never the sole carrier of meaning: a price pairs its signal colour with a sign, and a market-status icon pairs it with a distinct glyph for open, closed and holiday. Every content image carries alternative text describing what it shows, and a decorative image declares itself decorative rather than repeating its caption. Forced-colours rendering is preserved.

**Responsive.** The layout is fluid and holds at every width between its tiers, not only at them. On a wide screen the market summary runs chart beside list; on a tablet the two stack; on a narrow viewport nothing overflows sideways, every navigation target stays reachable, the header collapses its five menu entries into a hamburger, the search pill collapses to its glyph, and the card shelves become a single swipeable column. Hover affordances are gated behind a hover-capable pointer and do not fire on touch. Where the breakpoints sit is yours; the behaviour at each is not.

**One primary action per view.** Each route leads with exactly one primary action, visually distinct from every secondary one: `Get started for free` on the home route, `Subscribe` on the futures route, publish in the studio, boost on an idea page. A secondary action never wears the brand blue.

**Mode.** The product commits to dark: the marketing routes and every shared control are designed for the near-black ground, and the light data surfaces are inversions inside that one committed mode rather than a second theme. A light mode is optional and is not part of what the product owes; nothing should read as half-built in either direction.

**Component states.** Every control has a resting, pointed-at, pressed, focused and unavailable state, and unavailable is never signalled by colour alone. Escape closes the compose dialog and the cookie band; a destructive action confirms first.

## Technical requirements

Frontend: SolidStart, rendering each public route on the server with interactive islands hydrating the market surface, the ideas carousel, the compose dialog, the asset-class tabs and the cookie band. Backend: Hono, serving the HTTP API on the same origin under the `/api` prefix. Datastore: PostgreSQL, read from `DATABASE_URL`. Object store: MinIO, read from `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Auth: this app's own email and password with bearer tokens. Health: `GET /api/health` returns `200` once the app is ready. Logging: one line per request to standard output.

Read every host, port and credential from the environment. Never hardcode any of them. The backing services named in this brief, PostgreSQL and MinIO, are already running and reachable at those environment variables; do not download, install, compile or start a copy of either.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor - the only backing services available in this environment are PostgreSQL and MinIO, and reaching for anything else is a contract violation.

**Content and market data are two different things.** The marketing copy, the route structure, the footer link map and the card text are static and may be served from the application's own build. Market values are a subscription: the browser asks the app for a set of symbols and receives timestamped updates carrying value, change, direction and session state, and those updates arrive without the page reloading. Each update carries the server's own time, and the client places the value by that time rather than by the browser clock.

**No secret reaches the browser.** No credential, no object-store access key, no admin token and no database address appears in anything the browser downloads: not in the served HTML, not in a script bundle, not in a JSON response. The object store is reached by the server only. A snapshot is served to the browser through the application's own endpoint, which decides whether the requester may have it; the browser is never handed the store's address or its keys.

**Performance.** The first view of the home route paints before the market feed connects, and the ticker cards hydrate afterwards. The market surface holds a steady frame rate while many cards update at once and the primary chart pans. No binary asset ships: the hero backdrop, the section illustrations, the idea-card chart previews and the product demo are all drawn procedurally or replaced by the live market surface itself.

## Data model

Six tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

`accounts` - `id` integer, `email` text unique and stored lowercase, `password_hash` text, `display_name` text, `role` text and one of `reader` or `author`, `created_at` timestamp.

`ideas` - `id` integer, `slug` text unique and kebab-case, `title` text, `thesis` text, `symbol` text, `bias` text and one of `long` or `short`, `tags` a list of at most five text entries, `status` text and one of `draft` or `published`, `author_id` referencing `accounts`, `snapshot_key` text holding the object key and never the bytes, `comment_count` integer, `created_at` timestamp, `published_at` timestamp and null while the idea is a draft. An idea's boost count is derived on read from `boosts` rather than trusted as a stored counter.

`boosts` - `id` integer, `idea_id` referencing `ideas`, `account_id` referencing `accounts`, `created_at` timestamp. At most one row per account per idea at any time, and that must hold when two boost requests for the same idea from the same account arrive together.

`symbols` - `id` integer, `ticker` text unique, `name` text, `asset_class` text, `unit` text, `session` text and one of `open`, `closed` or `holiday`, `sort_order` integer.

`ticks` - `id` integer, `symbol_id` referencing `symbols`, `value` numeric, `change` numeric and signed, `direction` text and one of `up` or `down`, `server_time` timestamp. `direction` agrees with the sign of `change` on every row.

`cookie_choices` - `id` integer, `visitor_token` text unique, `accepted` boolean, `decided_at` timestamp.

**Invariants, stated as properties of the running system.** A draft idea and the object at its `snapshot_key` are readable by the owning author and by nobody else. Publishing the same draft twice leaves exactly one published idea and one stored object; two publishes of the same draft arriving together are not both accepted. An idea's boost count equals the number of boost rows for that idea, and a repeated boost from the same account does not change it. A failed publish or a failed snapshot attach leaves no partial state: no orphaned object in the bucket, no idea half-moved to `published`.

**Seed data.** Three accounts as listed in `## User roles`. Three ideas: `Gold Breakout Watch`, published, owned by `author@example.com`, symbol `XAUUSD`, bias `long`; `Yen Carry Unwind`, published, owned by `author2@example.com`, symbol `NI225`, bias `short`; and `Copper Squeeze Setup`, still a draft, owned by `author@example.com`, symbol `HG1!`, bias `long`. Each of the three carries a snapshot object in the bucket at the pinned key scheme. Symbols are seeded across the asset classes the futures matrix names, each with its unit and its session. The seeded market values are the captured snapshot the storefront opened on, and the feed moves them from there: `S&P 500` `SPX` at `7,711.76` `POINT` and `-0.25%`; `Nasdaq 100` `NDX` at `29,433.43` and `-0.70%`; `Japan 225` `NI225` at `66,311.71` and `-0.14%`; `Shanghai Composite` `000001` at `3,986.30` and `+0.86%`; `FTSE 100` `UKX` at `10,824.26` and `+0.29%`; `DAX` at `26,390.69` and `-0.67%`; `CAC 40` `PX1` at `8,400.92` and `0.00%`; `Crypto market cap` `TOTAL` at `2.61 T USD` and `+21.97%` over `1 month`; `Bitcoin` `BTCUSD` at `78,348 USD` and `+0.83%`; `Ethereum` `ETHUSD` at `2,442.2 USD` and `+1.04%`; a dominance split of `Bitcoin 60.24%`, `Ethereum 11.29%` and `Others 28.47%`; `US Dollar index` `DXY` at `99.524` and `-0.50%`; `Light crude oil` `CL1!` at `86.55 USD / barrel` and `+3.78%`; `Natural gas` `NG1!` at `2.888 USD / million BTUs` and `0.00%`.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

This section carries the full visual and structural specification. Nothing here changes a rule stated above.

### Global chrome

**Header.** A sticky header spanning the full width, present on every route, in the layer band that sits above the page and below the overlays. Left to right: the wordmark; a search control styled as a full pill with a leading magnifier glyph and the placeholder `Search`; the five primary menu entries `Products`, `Community`, `Markets`, `Brokers` and `More`; then, right-aligned, a globe language button reading `EN`, an anonymous user-menu button, and the get-started offer button. The header stays fixed to the top, condenses once the page has scrolled past the first viewport, and blurs whatever passes beneath it, so the page keeps showing through without competing with the menus. On the light home sections the language and user buttons hover to a translucent white; on the dark routes they hover to the raised deep neutral.

**Search.** A full pill with a leading magnifier and the placeholder `Search`, plus a keyboard hint. Its resting text is the mid neutral, warming to the near-white neutral body colour on hover; on the dark futures and not-found routes it rests a step brighter. Below the primary width it collapses to the glyph alone.

**Offer button.** The get-started control is a filled pill labelled `Get started`, wearing the brand blue with a cyan-to-violet accent wash drawn from the gradient set. It is the single most repeated call to action on the site, and it is the only control allowed to carry that wash.

**Footer.** One global footer on every route, a multi-column link map on the near-black ground, and the fullest map of the wider platform this storefront sits in front of. Column titles are the eyebrow size, semibold and uppercase; link items are body size, resting at the near-white neutral and moving to pure white on a raised deep-neutral fill on hover. A `Made by humans` badge with the hand-drawn heart glyph and a language selector reading `English` sit above the legal band. The column titles are `More than a product`, `Screeners`, `Heatmaps`, `Calendars`, `More products`, `Apps`, `Community`, `Ideas`, `Beamscript`, `Tools & subscriptions`, `Trading`, `Special offers`, `About company`, `Merch`, `Policies & security`, `Business solutions` and `Growth opportunities`. Their link items are labels for the wider platform and read: `Powercharts`, `Stocks`, `ETFs`, `Bonds`, `Crypto coins`, `Economic`, `Earnings`, `Dividends`, `IPOs`, `Portfolios`, `Options`, `Mobile`, `Desktop`, `Social network`, `Wall of Love`, `Refer a friend`, `Creator program`, `House Rules`, `Moderators`, `Indicators & strategies`, `Wizards`, `Freelancers`, `Features`, `Pricing`, `Market data`, `Who we are`, `Blog`, `Help Center`, `Careers`, `Terms of Use`, `Privacy Policy`, `Cookies Policy`, `Accessibility Statement`, `Status page`, `Widgets`, `Charting libraries`, `Trading Platform`, `Advertising` and `Partner program`.

**Legal band.** Below the link map, in the faint tertiary colour, carrying the market-data, reference-data and filings-data attributions: `Select market data provided by Meridian Data Services.`, `Select reference data provided by Factbase Research Systems.`, `SEC filings and other documents provided by Quartznote.`, `Made by humans`, `English` and `2026 Marketscope, Inc.`.

### Iconography

Every symbol on the site is an inline SVG drawn from points, not an icon font and not a bitmap, so it stays sharp at any size and recolours from the surrounding text colour with a single instruction. The load-bearing glyphs are: a hamburger menu of three equal horizontal bars; a search magnifier drawn as a ring with a diagonal handle; a small chevron pointing down, rotated for the other three directions; a narrow forward chevron for the carousel; the wordmark, drawn as one compound path so it inherits the text colour the way a letterform should; and a small heart with a hand-drawn quality beside the `Made by humans` badge. Draw each from its own geometry rather than reaching for a set, and give every icon-only control a text label.

### Elevation and layer order

Shadows are rare and shallow: a close, soft drop under the floating action button and the skip-navigation wrapper, a lighter one under a round floating button at rest, and a faint grey halo on the third-party badge. Hidden media controls carry a drop-shadow on the glyph itself rather than a box behind it. Layer order is a small, fixed ladder: everything in normal flow sits at the bottom, the header and its backdrop occupy one band above it, and overlays and the mobile menu occupy the band above that. Nothing invents a new layer to win a fight.

### Gradients

Accent gradients are a signature and appear only on headline words, card titles and the offer wash, never as a flat fill. Four of them carry the site: a cool headline sweep running left to right from a mid, vivid blue through a mid, vivid cyan to a mid, vivid teal, used on the futures hero word; a cool card title from a light, vivid indigo through a mid, vivid cyan to a light, vivid teal; a warm card title from a light, vivid red through a mid, vivid orange to the warning orange; and the offer and call-to-action wash, a diagonal from a mid, vivid cyan through the brand blue to a mid, vivid violet. The glow-card fill is a diagonal from a warm magenta-pink to a deep blue, paired with the two-tone glow described below.

### Scroll system

The page scrolls the way an ordinary page does; nothing hijacks the wheel and there is no full-page scrubbed timeline. Scroll powers two local effects and no more. The market-status icon swaps its mask glyph as its card moves through the viewport. The futures glow-card's two-tone coloured shadow, pink on one side and blue on the other, tracks scroll position between two measured extents, swelling slightly as the card enters, so it reads as attached to the movement of the page rather than played on a timer. The home route and the futures route are both tall, multi-section pages; the sign-in route does not scroll.

### Home route

**Hero.** Full viewport on the near-black ground over a night-side view of Earth with an aurora, built procedurally: a near-black field, a soft radial planet-limb glow at the bottom left, and vertical aurora streaks in the accent indigo, violet and cyan at low opacity with a slow drift. A very large two-line display headline sits centred over it, with the sub-headline `The best trades require research, then commitment.` beneath, a white filled pill reading `Get started for free`, and under that the reassurance `$0 forever, no credit card needed`. Bottom right, a small brand-film strip reads `See our space story` with `With astronaut Cmdr. Dana Reyes` and a `Space mission` button. A down chevron marks the scroll affordance.

**Feature chips.** A single row of pill chips naming the tracked markets: `US stocks`, `Crypto`, `Futures`, `Forex`, `Economy` and `Brokers`. Above them the section title `Where the world does markets`, the subtitle `Join 100 million traders and investors taking the future into their own hands.` and an `Explore features` link.

**Market summary.** The streaming surface. A large primary area chart for `S&P 500`, filled and stroked in the session's direction colour, beside a `Major indices` list streaming `Nasdaq 100`, `Japan 225`, `Shanghai Composite`, `FTSE 100`, `DAX` and `CAC 40`, each with a value, its unit and a signed percentage. Below sit three sparkline cards, `Crypto market cap`, `US Dollar index` and a yield card, each a one-month sparkline drawn in the rising teal or the falling red. `See all major indices` and `See all crypto coins` links close the block.

**Ticker card anatomy.** Each card carries a circular symbol avatar, a name, a short exchange ticker, a live value with its unit, a data-mode marker reading `D`, a market-status icon for open, closed or holiday, and a signed change coloured by direction. A tick changes only that card's value, its change and its colour; no neighbour so much as shifts.

**Ideas and stories.** A carousel of community idea cards, each a generously rounded candlestick chart preview, a title, a one-line description, an author byline, a comment count and a boost count with a rocket glyph. The previews are drawn procedurally as a seeded series of rising-teal and falling-red candles over a faint grid, so every card has a distinct chart without a photograph. Below, a `Top stories` grid of market-news headlines, each with a source badge and a relative timestamp.

**Closing call to action.** A final full-width panel repeating `Get started for free` with the line `The best trades require research, then commitment.` restated, closing the descent the hero opened.

### Futures route

**Hero.** On the deepest near-black. The word `Explore` in white above `real-time futures` set in the cool headline gradient, with the sub-line `Highly liquid futures markets mean oh-so-many more possibilities.` Two glowing cards, a Marketscope card and a CXE Group card, sit below at a slight tilt, carrying the breathing scroll-tracked glow.

**Value proposition and price.** The lead paragraph, then a price block reading `591 INR per month` with `for non-professional subscribers only`, and a `Subscribe` button reading `to real-time CXE Group futures`.

**Product cards.** Three titled cards, each with a `See how` link where one is present: `Unlock insights with our supercharged Powercharts`, whose body reads `Understand how futures prices affect the markets, in real-time. These charts have so many extra options - like data just for regular trading hours, and settlement or last price for the daily closing price.`; `Improve your analysis with Open Interest data`, whose body reads `Open Interest is the total number of outstanding derivative contracts that have not been settled. You can apply it for CXE Group futures as an indicator in one click.`; and `Gain more flexibility with continuous futures`, whose body reads `The "continuous futures" contracts we build for our charts allow us to construct a normalized historical data series for proper technical analysis, backtesting, and historical insights.`

**Asset-class matrix.** The nine tabs, each listing representative symbols and the two metric labels, with these sample metrics: `Equity indices` at `7.1 M` and `1.1 T`; `Metals` at `517.5 K` and `68.7 B`; `Interest rates` at `10.2 M` and `7.3 T`; `Energy` at `2.3 M` and `170.7 B`.

**Closing band.** `See every market in real time`, with `Track stocks, crypto, forex, and more from a single platform.` and a `View markets` action.

### Authentication routes

A narrow, centred card on the light ground. `/login` is titled `Sign in`, offers a `Show more options` control that expands the remaining fields, an `or` divider, and an `Email` field with its password; below it `Do not have an account?` and a `Sign up` link in the brand blue, whose hover moves to the deeper blue. `/signup` mirrors it and adds the account-type choice. Both are small on purpose: everything interesting happens once the visitor is through the door, because this is the entry to the account the whole workspace hangs from.

### Module and component architecture

Build as scoped components with no global class leakage; one component's styling can never reach another's. The shared components the routes compose from are the header with its condensing backdrop, the search pill, the offer button and the footer link-map, all on every route; the ticker card and the primary chart preview on the home and market surfaces; the idea card and the story card on the home route; the glow card and the asset-class tab card on the futures route; the auth card; and the not-found panel. Top-level state is surfaced once on the document root rather than threaded through every component: whether the visitor is authenticated, whether the account is a paying one, which of the two surface families the current section belongs to, and whether the pointer is a touch pointer. Every component reads those switches rather than deciding for itself.

### Responsive behaviour

Fluid from a single-column narrow layout up through several large-screen steps. The header collapses its five-entry menu into the hamburger glyph below the primary breakpoint and the search pill collapses to an icon-only button. The market-summary block reflows from chart-plus-list side by side to stacked. Idea and story grids reflow from multi-column to a single swipeable column. Hover affordances are suppressed entirely on coarse pointers, where they would only get in the way.

### Zero-asset substitution

No binary asset ships: no image file, no video file, no font file and no vector-animation file. The Earth hero backdrop is a layered canvas drawing as described above. Section illustrations are a canvas gradient placeholder keyed by a seed, using the palette stops already named, masked with a linear fade so it dissolves at top and bottom. The product-demo video is not replaced by another video: the live market surface itself is the demo, and an animated poster built from ticker cards stands in where a still is needed. Idea-card media is the seeded candlestick preview described above, a distinct chart per card and never a photo. The display typeface is loaded from a font host rather than shipped, with the fallback stack named above; naming a hosted font is not an asset dependency. The market-status mask glyphs are inline vector geometry, three distinct shapes for open, closed and holiday.

## Constraints

Single tenant: every account sees the same public catalogue of markets and published ideas, and ownership applies only to ideas.

Absent by design: no brokerage, no order routing and no money movement, so the futures subscription price is displayed copy and nothing charges a card; no in-browser script editor, compiler or sandbox for `Beamscript`; no backtest runner; no chart drawing tools; no comment threads, so an idea's comment count is seeded and read-only; no follower graph and no direct messaging; no moderation queue; no search results page behind the header search control, which scopes and filters the markets list only; no password reset; no email, no SMS and no push of any kind; no third-party analytics and no advertising network; no native mobile or desktop application; no external network call at runtime beyond the font host and the two named backing services.

The six platform capabilities are stated and linked, not rebuilt: the charting engine, `Beamscript`, the real-time global data layer, the backtesting engine, the social layer and cross-device sync all live in the separate application the storefront points at.

No binary file ships with the build, and nothing on a marketing route hard-codes a value that should be live.

The app must stay responsive with `2000` ideas, `200` symbols, `50000` tick rows and `20000` boost rows in the database.

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

**API shapes.**

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password`, `role` | the account and a bearer `token` |
| `POST /api/auth/login` | `email`, `password` | the account and a bearer `token` |
| `GET /api/auth/me` | none | the signed-in account |
| `GET /api/health` | none | `200` |
| `GET /api/markets/summary` | none | a top-level JSON array of `symbol`, `value`, `unit`, `change`, `direction`, `session`, `timestamp` |
| `GET /api/markets` | optional `asset_class` | a top-level JSON array of the same shape |
| `GET /api/ideas` | optional `tag`, `symbol` | a top-level JSON array of published ideas, newest first |
| `POST /api/ideas` | `title`, `thesis`, `symbol`, `bias`, `tags` | the created draft idea with its `slug` |
| `GET /api/ideas/<slug>` | none | the idea; a draft answers the owning author only |
| `POST /api/ideas/<slug>/snapshot` | the image bytes | the idea with its `snapshot_key` |
| `GET /api/ideas/<slug>/snapshot` | none | the image bytes; a draft answers the owning author only |
| `POST /api/ideas/<slug>/publish` | none | the published idea with `published_at` |
| `POST /api/ideas/<slug>/boost` | none | the idea with its new `boost_count` |
| `GET /api/cookie-choice` | none | the recorded answer, or that none was given |
| `POST /api/cookie-choice` | `accepted` | the recorded answer |

A successful call returns the named resource or shape. An invalid or unauthorized call is rejected as a client error, never a `5xx` and never a silent success, with a message naming the reason. Every endpoint that touches an account's own data requires a bearer token; login, signup, health and the public read endpoints answer without one.

**No mocks.** The snapshot bytes live in the MinIO bucket at the pinned key and nowhere else. An in-memory snapshot map, a base64 column in PostgreSQL, a file written under the app container's own directory, a hardcoded response the app returns to itself, or an image inlined into the served HTML are each a contract violation however convincing the page looks. The named provider is the fact - the app's UI and its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A stranger can open Marketscope, watch the market summary tick without reloading, create a free account from the sign-up form, and read a published idea with the chart snapshot its author attached. An author can save a draft, attach a snapshot and publish it, and until that publish the draft and its image answer nobody but its author. Publishing the same draft twice still leaves exactly one published idea and one stored image, and a reader who boosts an idea twice moves the count once.
