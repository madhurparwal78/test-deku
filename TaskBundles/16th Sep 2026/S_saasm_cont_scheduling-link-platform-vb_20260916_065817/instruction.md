# Meetline

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser and read the whole published marketing site, then sign up for a trial and land on their own booking page at this app's own origin, without hitting an error page.

A different stranger must NOT be able to reach a page that is still a draft, or the image that draft page carries, by any means: not by typing its route, not by asking the interface for it, and not by requesting its object key from the store. The bytes of every image on this site must live in the object store at the key scheme below; a copy on the app container's own filesystem does not count as an upload, however good the page looks.

## Overview

Meetline is a scheduling product, and this is the site that sells it. A visitor arrives knowing nothing, sees the product working on the first screen, reads the page written for their industry or their objection, and leaves by starting a trial. One short personal link is the whole promise: publish it, and other people book time without any back-and-forth.

The site is a content product, not a brochure that ships in a deploy. A marketing editor signs in, composes a page out of bands, uploads the media it carries, keeps it in draft until it reads right, and publishes it. Fifteen public routes render from that one content model, so the home page, the teams page, the voice sub-brand page, the embed page, the companion-app page, the six light editorial pages, the help desk, the developer documentation and the personal booking page all share the same primitives.

It deliberately is not the scheduling application. There are no event types to edit, no weekly availability to set, no bookings to confirm, no team round-robin, no reminders, no webhooks, no payments. The booking card on the home page is a demonstration: it responds to a click, and it confirms nothing.

The genuinely hard part is the visibility boundary. A draft page and its media are invisible to everyone who is not signed in as an author, and that has to hold at the interface and at the object store, not only in the pages the site renders.

## User roles

| Role | Can do |
|---|---|
| `author` | Read every page in any state. Create, edit, publish and unpublish a page. Upload media and attach it to a page. Read the page-view totals for every public route. **Cannot** change another account's role, and **cannot** remove a recorded page view. |
| `reader` | Read published pages and their media. Sign up, sign in, and hold one booking page of their own. **Cannot** open the studio, **cannot** create, edit, publish or unpublish any page, **cannot** upload media, and **cannot** read the page-view totals. |
| anonymous | Read published pages and their media. Sign up. **Cannot** do anything a `reader` cannot do. |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a `reader` session to any `author`-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Signup is open. Anyone may create an account, and a new account is always a `reader`; the role is never read from the signup body. Two accounts are seeded for convenience:

- `author@example.com`, role `author`, username `editor`
- `reader@example.com`, role `reader`, username `visitor`

Every seeded account uses the password `deku-demo-pw-2026`.

## Core features

### Auth

Accounts are email and password, implemented by this app. `POST /api/auth/login` takes `{"email", "password"}` and returns `{"access_token"}`; the client sends it back as a bearer token on every request that needs a session. `POST /api/auth/signup` takes `{"email", "password", "username", "display_name"}` and creates a `reader`. Passwords are stored hashed, never in readable form. A token expires, and an expired token is refused.

1. A signup whose `username` is already taken is rejected as invalid and creates no account.
2. A signup body carrying a `role` field still creates a `reader`.
3. A login with the wrong password is denied and returns no token.

### The page model and the studio

A page has a `slug`, a `route`, a `kind`, a `title`, a `standfirst`, a `state` of `draft` or `published`, and an ordered list of bands. A band has a `kind`, an `eyebrow`, a `headline`, a `body` and an ordered list of cards. This is the only way a public page exists; no route is hand-laid one-off markup.

1. An author creates a page through three steps, each at its own address: details, then bands, then review. Leaving a step and returning to it keeps what was entered.
2. A new page is created in state `draft`.
3. Publishing sets the state to `published` and records the moment it happened.
4. Unpublishing returns the state to `draft`, and the route stops resolving for everyone except an author.
5. Two pages in state `published` may not share a `route`. The second attempt is rejected as invalid and changes nothing.
6. Band positions are unique within a page and run from one upward with no gaps; card positions do the same within a band.
7. A `reader` session asking to create, edit, publish or unpublish a page is denied by the server, and the page's state does not change.

### Draft visibility, the rule this product turns on

1. A request for the public route of a page in state `draft` renders the not-found page for anonymous visitors and for a `reader`.
2. `GET /api/pages/{slug}` returns a page in state `draft` only to an `author` session. To everyone else that page is simply absent.
3. `GET /api/pages` returns only pages in state `published` to an anonymous caller and to a `reader`, and every page to an `author`.
4. A media object belonging to a page in state `draft` is not readable by anyone without an `author` session, at any address the app offers.
5. Publishing a page makes its route, its record and its media readable to everyone at once. Unpublishing takes all three away again.

### Media

Every image the site shows that is not drawn in the page is an uploaded object. `POST /api/media` takes the bytes and the owning page, stores them in the object store, and records the key.

1. The object key is `pages/{page_id}/{sha256_of_bytes}.{ext}`, for example `pages/42/9f2a7c4b1e6d0a3f5c2b8e9d4a1f7c0b6e3d9a2f5c8b1e4d7a0f3c6b9e2d5a8.png`.
2. The same bytes uploaded twice to the same page produce one object, not two, and the second attempt does not create a second row.
3. Bytes live only in the object store. The app's own filesystem and the database hold the key and the metadata, never the image itself.
4. Media belonging to a page in state `published` is served to anyone through an address the app owns, which streams the object out of the store. The store is never opened to anonymous callers.
5. Every uploaded image carries alternative text, and an image with no alternative text is rejected as invalid.

### The fifteen public routes

`/` home, `/teams` teams marketing with the avatar-wall hero, `/ai` the voice sub-brand on its dark launch theme, `/embed` the developer-facing embed tour, `/app` the companion apps page, `/about` the company story, `/jobs` the careers and mission page, `/open` the metrics page headed "The most public private company.", `/faq` the accordion list, `/terms` the long-form legal document with its sticky table of contents, `/font` the type specimen with its serif and typewriter specimen faces, `/help` the searchable help-desk article index, `/docs` the developer documentation with sidebar, search and code samples, `/USERNAME` a personal booking page, and the not-found page at any unknown address.

1. Every internal link on every public route resolves to a page that exists. An internal link is one whose address starts with a single slash.
2. An unknown address renders the product's own not-found page, carrying the figure "404", the line "This page could not be found.", and a recommended-links card whose entries dim on hover. It answers as not found, not as success.
3. Each page view of a public route is recorded with the route and the moment it happened, and an author reads the totals per route at `/studio/views`. The log is only ever added to.

### The home page, twelve bands in this order

Hero, trusted-by, how it works, benefits, more-features grid, testimonial carousel, app store, wall of love, FAQ, trusted-by reprise, closing band, footer.

1. The hero carries a launch chip reading "Meetline launches v6.8", the headline "The better way to schedule your meetings", the standfirst "A fully customizable scheduling software for individuals, businesses taking calls and developers building scheduling platforms where users meet users.", a dark pill "Sign up with Google", a light pill "Sign up with email", and the reassurance line "No credit card required".
2. The hero's right half is a live-looking booking card: a profile column with an avatar, an organiser name, an event title, a three-line description, a duration control of pills "15m 30m 45m 1h" with one selected, a conferencing row and a timezone row; beside it a month grid labelled "May 2025" with weekday headers "SUN MON TUE WED THU FRI SAT", available days filled, the selected day a dark square with a white digit, and a dot on today. Hovering a day raises its fill, clicking selects it, the duration control switches, and confirmation is disabled. The card cycles two seeded demo personas: "Ethan Taylor", "Academic Counseling", "Virtual counseling session for university students to discuss academic progress and well-being.", "Google Meet", "America/California"; and "Marcus van der Linden", "Partnerships Meeting", "Meetline Video", "Europe/Amsterdam". Review-platform badges sit below as drawn star rows.
3. The trusted-by band reads "Trusted by fast-growing companies around the world" beside a continuous marquee of eight wordmarks set in the display face: Nimbus, Forgeline, Beacon, Quantik, Northwind, Alloy, Lumon, Vantage.
4. How it works carries the eyebrow "How it works", the headline "With us, appointment scheduling is easy", the standfirst "Effortless scheduling for business and individuals, powerful solutions for fast-growing modern companies.", the CTA pair "Get started" and "Book a demo", and three numbered cards: 01 "Connect your calendar" with "We'll handle all the cross-referencing, so you don't have to worry about double bookings."; 02 "Set your availability" with "Want to block off weekends? Set up any buffers? We make that easy." over a mini weekly editor reading Mon 8:30 am to 5:00 pm, Tue 9:00 am to 6:30 pm, Wed 10:00 am to 7:00 pm; 03 "Choose how to meet" with "It could be a video chat, phone call, or a walk in the park!".
5. Benefits carries the eyebrow "Benefits", the headline "Your all-purpose scheduling app", the standfirst "Discover a variety of our advanced features. Unlimited and free for individuals.", and four feature rows, each a copy block beside a product-chrome mock. "Avoid meeting overload" sits beside a notice-and-buffers panel reading Minimum notice, Buffer before event 30 mins, Buffer after event 30 mins, Time-slot intervals "Use event length (default)". "Stand out with a custom booking link" sits beside a link card that rotates a German-lessons variant and a partnerships variant, each with its duration pills and conferencing row. "Streamline your bookers' experience" sits beside an overlay-calendar mock with the toggle "Overlay my calendar", a "12h" and "24h" switch, a week strip "Mon 04" through "Sun 10", and busy blocks Lunch date 12 PM to 1 PM, Coffee 11 AM to 12 PM, Design conference 1 PM to 3 PM, Hiring call 11:30 AM to 1 PM and Company meeting 11 AM to 2:30 PM. "Reduce no-shows with automated meeting reminders" sits beside three notification cards reading "Meeting starts in 15 mins", "Booking rescheduled" and "New booking confirmed".
6. The more-features grid is headed "...and so much more!" and carries eight tiles, each a glyph, a title and one line: Accept payments, Built-in video conferencing, Short booking links, Privacy first, 65+ languages, Easy embeds, All your favorite apps, Simple customization.
7. Testimonials carry the eyebrow "Testimonials", the headline "Don't just take our word for it", the standfirst "Our users are our best ambassadors. Discover why we're the top choice for scheduling meetings.", and a two-row marquee of quote cards drifting in opposite directions, with back and next arrow controls so a keyboard or touch visitor can page it. The six seeded quote cards and their attributions are: "Just gave it a go and it's definitely the easiest meeting I've ever scheduled!" from Nora Feld, CEO, Kinetic Labs; "I finally made the move to Meetline after I couldn't find how to edit events in the Meetwise dashboard." from Ben Carter, Co-Founder and CTO, DataForge; "At CarePath, protecting personal health information is a non-negotiable, so choosing Meetline for scheduling just makes sense." from Sam Okafor, CEO and Founder, CarePath; "More elegant than Meetwise, more open than Bookrite, Meetline works and it feels just right." from Jules Marin, Product Marketing, Docsmith; "I think Meetline has a very good chance of creating a new category around being both great and well designed." from Marco Reyes, CEO, DeployHub; and "I just migrated from Meetwise to Meetline." from Evan Ross, Founder of WebCraft.dev. The wall of love reprises with "See why our users love Meetline".
8. The app store band is headed "All your key tools in sync with your meetings" over a grid of labelled glyph chips.
9. The home FAQ is headed "Frequently asked questions" over the standfirst "These are some of our most frequently asked questions." and three accordion items, the first of which asks "How much does Meetline cost and what's included in each plan?". Their answers name the plan prices: Teams at 16 dollars per user per month, Organizations at 37 dollars per user per month, and Enterprise on custom pricing.
10. The closing band reads "Smarter, simpler scheduling" over the CTA pair and a wide procedural product image.

### The other marketing routes

1. `/teams` opens with the chip "We now offer a 14-day free trial", the headline "Simple scheduling for teams", the standfirst "Every meeting gets booked with the right person, every time." and one dark CTA "Get started free", over an avatar wall of rounded tiles, most empty, a scattered minority carrying seeded procedural portraits, fading toward the edges. Below it: the trusted-by marquee; "Key benefits" with three numbered problem cards Eliminate no shows, Stop wasting time on scheduling and Get leads into calls faster; a capability ticker headed "Meetline doesn't miss on" cycling instant meetings, restriction schedules, custom domains, requires confirmation, custom variable routing, round-robin scheduling, managed events, booking analytics and role-based permissions; an "Additional features" grid headed "Designed for maximum efficiency" over the standfirst "Boost team performance with our advanced collaboration features and automated workflows.", carrying six cards Round robin scheduling, Collective events, Lead routing software, Dynamic meetings, Workflow automation and Accept payments; the app-store band; a "Use cases" grid of six cards Startups, Sales, Recruiting, Marketing, Customer success and Education; the testimonial wall; and the closing band.
2. `/ai` is the one dark page, and it sells Meetline Voice, the AI phone-agent sub-brand. Eyebrow "Book a sales call with our team"; the two-line headline "Supercharged scheduling with AI-powered calls" whose second line carries a violet-to-lavender text treatment; a standfirst about lifelike agents that book meetings, send reminders and follow up through natural phone calls; the CTA "Try AI scheduling"; the helper line "Try calling the phone number above to test Meetline Voice!". The hero object is a phone mock showing the status time "9:41", a number line and an agent transcript opening "Hi, Alex. This is Sally from Arlo.". Then a video card "Introducing AI-powered calls" with a centred play triangle; a three-step band "Set up your Agent in minutes without a PhD degree" reading Set your trigger, Add a phone number, Set up your AI agent; prompt-editor mocks for Personality, Prompt style and Tone; a workflows band reading Trigger "24 hours before" and Action "Call attendee with the voice agent"; a call-log mock of four rows, Call with Alison Carter, Call with Peter Jones, Call with Karen Bridges unanswered, and Call with Carl Brand, each with a Play control; a price band carrying the enormous figure "$0.29/minute"; a benefits grid; a features-you-also-get grid; and an FAQ accordion. The voice agent is marketing surface: no telephone rings anywhere in this build.
3. `/embed` carries the eyebrow "Embed", the headline "Embed a scheduling widget on your website with Meetline", a standfirst naming the four embedding options inline embed, floating pop-up button, pop-up via element click and email embed, and the CTA pair "Get started" and "Talk to sales". Then the trusted-by band; a three-step how-to Make your event type, Choose the embed type and Adjust your embed and publish; a four-card solutions grid, one card per embed mode, each containing a miniature of the same booking card in demonstration mode; a white-label band showing a code editor mock with line numbers and syntax tinting, headed "White-label the scheduling widget by using our booker atom"; and a closing booking card.
4. `/app` is titled "Meetline Companion for iOS, Android and Chrome" and presents the phone application with a floating install button, a store-badge row and a device frame carrying product screens, then bands on booking on the go, on notifications, and on the browser extension. The device frame is the only object on the whole site that follows the scroll.
5. `/about` is headed "Learn More About Meetline's Story" over an editorial column, a portrait band and a values grid. `/jobs` is headed "Work With Us and Connect a Billion People by 2031" over mission copy, an open-roles list rendered from data, and a values band. `/open` is headed "The most public private company." over an intro naming the open-startup policy and a dashboard of chart cards for monthly bookings, revenue and team size, drawn from seeded fixtures with the chart ramp. `/faq` is an accordion list. `/terms` is a long-form legal document with a sticky in-page table of contents. `/font` is a type specimen with glyph grids, weights and paragraphs set in the two specimen families.
6. `/help` is a searchable article index of category cards. `/docs` shares a different shell: a top bar with a search entry, a left sidebar tree, a content column and a right-hand on-this-page rail. The search entry opens a command palette on click or on the slash key, with rows grouped by section. Sidebar rows wash on hover and their glyphs recolour with state. Code blocks carry a dark ground, a monospace face, a copy button and a language tab row. The documentation covers a quickstart, an embed guide, a webhook guide, key management and one reference page per public resource.

### Global chrome

1. A floating white pill bar, inset from the top, sits on every page and stays while the page scrolls beneath it. It holds the wordmark at left, then Solutions, Enterprise, Meetline Voice, Developer, Resources and Pricing, then a "Sign in" text link and a dark "Get started" pill with a chevron. On the dark page it renders on the night ground with white text.
2. Solutions, Developer and Resources open dropdown panels on hover and close on leave. The Developer panel carries "Scheduling Components" with "Use our react atoms to add scheduling to your app", and "Create OAuth Client" with "Integrate Meetline using OAuth". The Resources panel carries twelve entries, Font, App Store, Collective Events, Help Docs, Embed, Out Of Office, Payments, Workflows, Blog, Instant Meetings, Dynamic Group Links and Webhooks, each with a one-line description. The Solutions panel mirrors the footer's Solutions and Use Cases columns.
3. Below the tablet breakpoint the centre links collapse behind a menu control and the drawer drops in from the top.
4. The footer carries four link columns, Solutions, Use Cases, Resources and Company, over a left identity block: the wordmark, the trademark line "Meetline and Slot are registered trademarks of Meetline, Inc. All rights reserved.", five compliance seals drawn as labelled circles reading ISO, SOC2, CCPA, GDPR and HIPAA, the mission line "Our mission is to connect a billion people by 2031 through calendar scheduling.", a language selector offering English, German, French, Dutch, Portuguese, Spanish and Italian, a status pill reading "All Systems Operational" beside a green dot, a Downloads grid of chips for Android, Chrome, Safari, Edge, Firefox, macOS, Windows and Linux, and two review-platform badges. The Company column carries Jobs, About, Open Startup, Support, Privacy, Terms, License, Security, Changelog, Get a demo and Talk to sales.
5. Toasts appear bottom-centre. A cookie-consent sheet rises from the bottom on a first visit, and its preferences dialog scales in.

### The trial

1. From any public page a visitor may sign up. Signing up takes an email, a password, a username and a display name.
2. A successful signup creates the account and creates one booking page for it at `/USERNAME` on this app's own origin, and the visitor lands on that page.
3. A username is unique, compared case-folded, and appears in the booking page's address exactly as it was stored.
4. A visitor who already holds an account and signs up again with the same email is refused; one account holds one booking page.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | home, the twelve bands and the booking demo | none |
| `/teams` | teams marketing | none |
| `/ai` | voice sub-brand, dark theme | none |
| `/embed` | embed tour | none |
| `/app` | companion apps | none |
| `/about` | company story | none |
| `/jobs` | careers and mission | none |
| `/open` | public metrics | none |
| `/faq` | questions accordion | none |
| `/terms` | terms of service | none |
| `/font` | type specimen | none |
| `/help` | help-desk article index | none |
| `/docs` | developer documentation | none |
| `/USERNAME` | a personal booking page | none |
| `/signup`, `/login` | account entry | none |
| `/studio` | page list beside the page editor | `author` |
| `/studio/new/details`, `/studio/new/bands`, `/studio/new/review` | the three creation steps | `author` |
| `/studio/media` | the media library | `author` |
| `/studio/views` | page-view totals per route | `author` |

**Entry and redirects.** An anonymous request for `/studio` or any address beneath it lands on `/login` and, after a successful sign-in, continues to the address first asked for. A `reader` session asking for `/studio` is refused and lands on `/`. Signing out returns to `/`. A token that expires mid-action returns the studio to `/login` and leaves the row that was being edited unchanged. A request for the route of a page in state `draft` renders the not-found page.

**Journeys.**

1. Open `/`. The twelve bands render in order. Click a day in the booking card and it becomes the selected day. Click the "45m" pill and the duration control moves. Nothing confirms.
2. Sign in as `author@example.com` with `deku-demo-pw-2026`. Open `/studio`. The left side lists every page with its state; the right side shows the selected page. Start a new page, fill in the details step, add two bands, review, and save. The new row appears in the list in state `draft`.
3. Still as the author, upload an image to that page from `/studio/media`, give it alternative text, then press Publish on the list row. The row shows `published` at once, ahead of the save answering; if the save fails the row returns to `draft` and a message says why.
4. Sign out. Ask for the draft page's route `/blog/scheduling-links-that-convert`. The not-found page renders. Ask the interface for that page by slug. It is absent.
5. From `/` press "Sign up with email", enter an email, a password, a username and a display name. The account is created and the booking page at that username opens.
6. Sign in as the author and open `/studio/views`. Every public route carries the number of times it has been viewed.

**States.** Every list has an empty state that says what to do next, never a blank panel. Every page has a loading state, which is the shimmer skeleton. An error never blanks the page: the band that failed carries the message and the rest of the page stands. The month grid on a month with nothing available shows the month rather than an error.

## UI/UX notes

The site is white cards on a faint grey page: a card-in-frame arrangement where every band sits inside a rounded panel inset from the page edges, so the page reads as a stack of large cards with the ground showing between them. Small crosshair glyphs sit at the panel corners as a deliberate blueprint motif. The register is consumer-marketing with an operational core: the pages may carry atmosphere, the booking card inside them may not. Somebody should understand in the first moment that this product books meetings, because they can see it working rather than read that it does.

**Colour by role, and no value.** The page ground is a near-white neutral; cards sit on it in near-white neutral; inset panels and hover fills a near-white neutral one step down; pressed and selected fills a near-white neutral again. The darkest ink is a near-black neutral. The primary action and the selected day wear a deep cool neutral, which deepens on hover, and nothing else on a page wears it. Default borders are a near-white cool neutral, a focused or hovered border a light cool neutral, hairlines inside cards a near-white neutral. Meaning is the only thing colour is spent on: attention is a near-white warm neutral wash under a mid, soft red ink; error a near-white warm neutral wash under a deep, soft red ink; information a near-white cool neutral wash under a deep, soft blue ink; success a near-white neutral wash under a mid, vivid teal ink. Charts, and nothing else, use a ramp of seven hues, each with a wash and an ink: light, vivid magenta; light, vivid indigo; light, vivid blue; mid, vivid teal; mid, vivid amber; mid, vivid orange; light, vivid red. The exact shades are yours, so long as they hold the roles above and the contrast bar below. `/ai` is the one dark page: a near-black cool neutral ground under white text, with faint drifting specks in the hero.

**Type, exactly.** Manrope at 700 carries headlines and the wordmark, and loads blocking. Inter, variable 100 to 900, carries everything else and loads with swap. The specimen page alone adds Latin Modern at 400 and 700, roman and italic, and CMU Typewriter Text at 500; documentation code samples use the default monospace stack. Every face falls back to -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif. Reproduce this scale: 90px at 700 over 90px for the home hero headline on desktop; 70px at 700 over 70px for section headlines; 24px at 600 over 32px for card titles; 20px at 600 over 28px for sub-card titles; 18px at 300 over 27px for the hero standfirst; 16px at 300 over 24px for marketing body; 16px at 400 over 24px for body inside the studio; 14px at 500 over 20px for buttons and labels; 14px at 400 over 20px for secondary body; 12px at 400 for metadata and calendar digits; 11px at 600 over 13.2px for uppercase eyebrows. The hero carries no added tracking.

**Shape and depth.** Buttons and chips are full pills; cards are softly rounded, outer panels a little more so, small controls a little less, avatars and dots fully round; where a panel meets a neighbour flush it keeps its rounding on the outer edge only. Shadows read like paper resting on paper: a resting card lifts barely off the ground, buttons carry a single hairline drop, dark buttons and dark cards catch a thin top sheen along their upper edge, which is what makes them look pressed from metal rather than painted, the floating install button lifts further, demo panels are inset rather than raised, and quiet link cards gain their shadow only on hover. The voice page hero card wears a triple ring. A flat placeholder wash sits behind every media frame. The focus ring is the conventional blue and expands on focus; an error ring takes the error ink.

**Motion, by character.** Nothing drifts while you scroll. Things arrive: as a band enters, its children rise and fade, staggered a beat apart, and every element has exactly two states, hidden and shown, so a scroll-scrubbed timeline is wrong here however smooth it looks. Menus and accordions open with a springy overshoot that pushes past rest and settles back. Toasts slide up from the bottom; a success toast squashes and settles, an error toast shakes twice. Skeletons carry a shimmer sweep and a slow pulse. The trusted-by strip and the wall of quotes are continuous marquees at a slow walking pace, rows alternating direction, pausing the moment a cursor touches them. The voice page hero ring and backdrop swap once as the video card enters. Every one of these must animate through transform and fade alone, so nothing stutters, and every transition respects a reduced-motion request: marquees freeze, reveals become plain appearances, springs become fades, and the drifting specks stand still.

**Accessibility floors, which are requirements rather than taste.** Body text and its background meet WCAG AA contrast, on the light pages and on the dark page alike. Keyboard navigation reaches everything: the month grid is a grid widget walked with the arrow keys, home and end to the week edges, and the page keys across months; the slot list, the accordions, the dropdown panels and the command palette all operate without a pointer; the drawer and every dialog trap focus and restore it on close. The focus ring is always visible. Icon-only controls carry labels. Every content image carries alternative text, and every decorative image declares itself decorative. Under forced colours the selected day keeps a drawn border rather than a fill alone. Colour is never the only carrier: availability, selection, errors and chart series each pair colour with a shape, a weight or a word. Live regions announce toast content.

**Responsive.** The arrangement holds at every width between a phone, a tablet and a desktop viewport, not only at those three. The header pill keeps its shape at every width; below the tablet breakpoint its centre links fold behind a menu control and the drawer drops from the top. The hero splits: the booking card drops below the copy at tablet and the headline steps down the scale to a phone size that keeps three lines at most. Numbered card rows become single-column stacks, feature rows alternate copy above mock, the testimonial marquee drops to one row, and the booking card reflows so the month grid runs full width and the slot column becomes a bottom sheet. The docs sidebar becomes a slide-in drawer and the on-this-page rail disappears below the desktop breakpoint. At a narrow viewport nothing overflows sideways and every navigation target stays reachable, with touch targets in the month grid and the slot list comfortably finger-sized. Whatever is revealed only by a hovering pointer has a visible twin where there is no pointer.

What this must not look like: a page dominated by one hue family with no second signal; decoration standing where content belongs; a marketing composition where the working booking card belongs. Space over dividers, and calm over expressive, everywhere except the one dark page, which is allowed its theatre.

## Technical requirements

Build the front end with **SvelteKit** and the JSON interface with **Fastify**, both served on one origin. The rendering model is server-rendered with islands: the first paint carries each page's text and arrangement from the server, and only the interactive objects take over in the browser, which are the booking demo card, the dropdown panels, the accordions, the command palette and the studio. Node 20 is the runtime. Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor - the only backing services available in this environment are **PostgreSQL** and **MinIO**, and reaching for anything else is a contract violation.

PostgreSQL is reached at `DATABASE_URL`. MinIO is reached at `STORAGE_ENDPOINT`, with the bucket named by `STORAGE_BUCKET` and the credentials `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Both are already running and reachable at those variables. Read every value from the environment and never hardcode a host, a port or a credential.

Authentication is email and password implemented by this app, with bearer tokens; there is no external identity provider. `GET /api/health` returns `200` once the app is ready. Every response carries a generated request id in a header, and that same id appears on the structured log line for the request, so one request can be followed end to end.

Every public route declares its own title and its own description, and no two public routes share them. Every public route also declares a social preview title and a preview image, and every preview image resolves to a real object rather than a dead address.

Marketing media below the first screen loads lazily. No third-party script blocks the first paint. Fonts load with the behaviour named in the UI/UX notes. Movement runs on compositor-friendly properties so scrolling never stutters.

Ship no binary asset. Faces load from the hosted font service. Portraits, compliance seals, star rows, provider glyphs, video posters and the drifting specks on the dark page are all drawn procedurally from a seed, and the same seed yields the same portrait everywhere it appears. Icons are inline vector geometry that inherits the current colour, never an image file; brand wordmarks in the trusted-by band and the footer are the company names set in the display face. Where a video would play, a drawn poster with a play badge stands in and a modal says the media is stubbed.

Design tokens are the only source of colour anywhere in the front end; a component quoting a raw value is a defect. The seven light editorial pages share one set of primitives: eyebrow chip, headline block, CTA pair, numbered card, feature row, marquee row and accordion. One booking-card component serves the home hero, the miniature demonstrations on the embed page and the personal booking page; the mode it runs in is a property of that component, never a second copy of it. That sharing is the module and component architecture this site needs, and a second copy of any of those primitives is a defect rather than a shortcut.

Performance is part of the specification, not a hope. The home page must become interactive quickly on a mid-range laptop. Marquees and reveals move on compositor-friendly properties only, so scrolling causes no layout thrash. The page list in the studio must answer within 300 milliseconds against the seeded data volume named in the constraints.

## Data model

Nine tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

- `users`: `id`, `email`, `username`, `display_name`, `role`, `password_hash`, `created_at`. `email` and `username` are each unique and compared case-folded. `role` is `author` or `reader`.
- `pages`: `id`, `slug`, `route`, `kind`, `title`, `standfirst`, `preview_title`, `preview_image_key`, `state`, `published_at`, `updated_at`. `slug` is unique. `state` is `draft` or `published`. No two pages in state `published` share a `route`, and that holds under simultaneous requests: two publishes that would collide on one route must not both succeed, exactly one wins and the other is rejected.
- `bands`: `id`, `page_id`, `position`, `kind`, `eyebrow`, `headline`, `body`, `media_key`. `position` is unique within a page.
- `cards`: `id`, `band_id`, `position`, `title`, `body`, `media_key`, `alt_text`. `position` is unique within a band.
- `media`: `id`, `page_id`, `object_key`, `content_type`, `byte_size`, `sha256`, `alt_text`, `created_at`. `object_key` is unique and is the only address the bytes have.
- `links`: `id`, `page_id`, `href`, `label`.
- `page_views`: `id`, `route`, `viewed_at`. Rows are only ever added.
- `booking_pages`: `id`, `user_id`, `username`, `headline`, `created_at`. One row per user.
- `sessions`: `id`, `user_id`, `token_hash`, `expires_at`. A session is revocable on the server.

`published_at` is stored; the view total per route is computed on read from `page_views` rather than stored. A failed publish leaves no partial state: no half-written page, no orphaned media row.

All times persist in universal time, and user-facing rendering happens with an explicit zone every time. The uniqueness this product depends on, an account's username and a published page's route, is what the store holds. Deletes are soft where history refers to the row, so removing a page leaves its recorded views intact. Every state-changing action is authorised by ownership or by role, and a request forging another owner's id must fail even when the interface never offers it.

Seed data: the two accounts above; fifteen pages at the fifteen public routes, all in state `published`; one page in state `draft` at route `/blog/scheduling-links-that-convert`, titled "Scheduling links that convert", carrying one media object with alternative text; and one booking page for `author@example.com` at `/editor`. Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

This carries the visual detail that will not fit in the UI/UX notes. It specifies appearance only; every graded behaviour lives above.

**Grid and widths.** The arrangement is measured at a desktop width of 1440 by 900, a tablet width of 990 by 800 and a phone width of 390 by 844. Width steps sit at 640, 768, 1024 and 1280 pixels, and the documentation shell adds steps at 40rem, 48rem and 60em. Hover styling is gated behind a hover-capable pointer with a fallback for devices without one; reduced motion, forced colours and print each have their own block.

**Header detail.** The Get started chevron slides a few pixels to the right on hover. Marketing text links fade to half strength on hover rather than changing hue; on the dark page they brighten instead. The light pill button solidifies from translucent white to solid on hover; on the dark page it lifts to a lighter indigo.

**Dropdown panels.** Each is a white card, softly rounded, wearing the resting-card shadow, laid out as columns of labelled links with small stroke icons and a one-line description each.

**Footer detail.** Chips raise from no shadow to the quiet link-card shadow on hover. The status dot takes the success ink.

**Shared furniture.** Seven pieces of shared furniture recur on every page and are built once: the eyebrow chip, a small white pill above a section headline carrying an uppercase label beside a small stroke icon; the headline block; the section CTA pair, a dark pill beside a ghost pill; the numbered card; the feature row; the marquee row; and the accordion. Toasts sit bottom-centre. Skeletons stand in for content that has not arrived. The cookie consent sheet is a bottom sheet entering with a rise and a fade, and its preferences dialog scales in from just under full size.

**Colour steps in detail.** The booking-panel border is its own step, one shade lighter than the default border, so the booking card reads as a panel inside a card rather than a card inside a card. The info wash sits under an informational message and nowhere else; the attention wash, the error wash and the success wash each behave the same way.

**Iconography.** Every icon is inline vector geometry, never an image file, and the structural ones are drawn to these shapes: a chevron right in a 7 by 10 box as a two-unit stroke, a plus in a 24 by 24 box at one and a half units, a small chevron in a circle in a 14 by 14 box, a filled play triangle, a video play badge with a rounded rectangle and a white triangle, an external-link arrow leaving a box, and a toggle pill with an inner track. Stroke icons inherit the current colour so state changes recolour them; decorative icons are hidden from assistive technology.

**The easing vocabulary.** It is small and spring-flavoured: a default easing for colour and transform; a long settle for entrances; a decelerating exit that arrives into place; a slide for drawers and sheets; a playful overshoot on chips and badges; a cursor-following highlight; a symmetric in-out for anything that loops; and a lift for card hover.

**Named moments, every one of which must ship.** A slide up for toasts and sheets. A rise with fade whose pointer-events gate stays shut until it lands. A drop with fade for the mobile drawer. A short rise with fade for list items. A plain fade. A spinner turning through a full rotation, linear and infinite. A pulse that dips its opacity at the midpoint and repeats infinitely. A shimmer sweep across a skeleton. A skeleton crawl. A caret that blinks, holding its opacity in a pattern inside an input. Typing dots that dip at the start of their bounce. A hop that rises and falls across two split curves. A block loader that rotates while its inner bar fills. A success toast that squashes and settles. An error toast that shakes twice.

**Zero-asset substitution.** The build ships no binary asset, and every image, face, badge and seal in the reference is replaced procedurally; this is the substitution guide for all of them. Avatars and the teams portrait wall are seeded radial gradients in two ramp tones with initials in the display face. Compliance seals are five circles with a hairline stroke carrying abbreviated uppercase labels. Review badges are star rows drawn from a five-point star path with the fractional star clipped horizontally, labelled "4.5" beside a count. The four-colour provider glyph is four quarter-squares in ramp hues one, three, four and five. The dark page carries 120 drifting particles, each one to two units across, rising slowly with a sinusoidal sway and twinkling on its own phase, frozen under reduced motion. Chart fixtures are seeded walks, one seed per chart, committed so the same chart draws the same way twice.

**Accordion and palette.** Accordion items expand with the springy overshoot. The FAQ page alone uses a brighter link ink that darkens on hover. The documentation search entry darkens its ring on hover and opens the command palette on click or on the slash key, with rows grouped by section under small labels.

## Constraints

- One site, one tenant. There are no organisations, no workspaces and no per-customer subdomains.
- No scheduling application. No event types, no weekly availability, no date overrides, no bookings, no holds, no seats, no waitlist, no team round-robin, no routing forms and no insights dashboard beyond the seeded charts on `/open`.
- No email of any kind, and no SMS. Nothing in this build sends a message.
- No payments. Prices are copy on a page; nothing charges.
- No real telephony behind the voice sub-brand page.
- No external network call at runtime beyond the two backing services and the hosted font service.
- No native application. The companion-apps page describes one; this build does not ship one.
- No background job, no cron, no scheduler and no task queue.
- Translation ships in English only. The language selector is a real control and the document language follows it.
- The site must stay responsive with 60 pages, 600 bands, 2,000 media objects and 200,000 recorded page views.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.**

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{"email", "password", "username", "display_name"}` | the created account and its booking page |
| `POST /api/auth/login` | `{"email", "password"}` | `{"access_token"}` |
| `GET /api/pages` | optional `state` | a top-level JSON array of pages |
| `POST /api/pages` | `{"slug", "route", "kind", "title", "standfirst"}` | the created page in state `draft` |
| `GET /api/pages/{slug}` | none | one page with its bands and cards |
| `PATCH /api/pages/{slug}` | `{"state"}`, or any editable field | the updated page |
| `POST /api/media` | the bytes, `page_id`, `alt_text` | `{"object_key"}` |
| `GET /api/media/{object_key}` | none | the object bytes, streamed out of the store |
| `GET /api/page-views` | none | a top-level JSON array of `{"route", "views"}` |
| `GET /api/health` | none | `200` |

Field names are exact. A list endpoint returns a top-level JSON array. A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as a client error, never a `5xx` and never a silent success.

**No mocks.** The uploaded bytes must live in the MinIO bucket at their scheme's key: a copy on the app container's filesystem does not count, an image written into the page record as a data URI does not count, and a hardcoded list of object keys the app hands back to itself does not count. PostgreSQL is where the pages, the bands, the media rows and the page views live; an in-memory array that survives only until restart does not count. The named provider is the fact - the app's UI and its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A stranger can open the site, read all fifteen published routes, and sign up for a trial that gives them a booking page at their own username. A marketing editor can compose a page, upload an image to it, and publish it, and until they do, nobody else can reach that page or its image. Every content image carries alternative text, every internal link resolves, and every public route records the fact that it was viewed.
