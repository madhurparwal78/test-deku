# Checklist: Meetline

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, techrequirements, datamodel, frontend, constraints, contract
Sections absent: buildplan
Items: 124
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The product presents a public marketing site whose pages are composed inside the product rather than shipped in a deploy. `src: Overview para 2`
- [ ] `C-OV-02` `constraint` The product omits the scheduling application, so no event type, no availability, no booking, no reminder, no webhook, no payment exists. `src: Overview para 3`
- [ ] `C-OV-03` `capability` A page in state `draft` stays invisible to anyone without an author session, at the interface as well at the object store. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` An author reads every page in any state. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An author creates, edits, publishes, unpublishes a page. `src: User roles table row 1`
- [ ] `C-RL-03` `role` An author uploads media, attaching the upload to a page. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An author reads the page-view totals for every public route. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A reader is denied every page mutation by the server. `src: User roles table row 2`
- [ ] `C-RL-06` `role` A reader is denied the page-view totals. `src: User roles table row 2`
- [ ] `C-RL-07` `role` An anonymous caller reads published pages, their media too. `src: User roles table row 3`
- [ ] `C-RL-08` `capability` Signup is open, so anyone may create an account. `src: User roles, signup paragraph`
- [ ] `C-RL-09` `literal` The seeded author account is `author@example.com`. `src: User roles, seeded accounts`
- [ ] `C-RL-10` `literal` The seeded reader account is `reader@example.com`. `src: User roles, seeded accounts`
- [ ] `C-RL-11` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles, seeded accounts`

## C-CF Core features

- [ ] `C-CF-01` `literal` `POST /api/auth/login` takes an email with a password, returning `{"access_token"}`. `src: Core features, Auth para 1`
- [ ] `C-CF-02` `literal` `POST /api/auth/signup` creates an account whose role is `reader`. `src: Core features, Auth para 1`
- [ ] `C-CF-03` `capability` A password is stored hashed, never in readable form. `src: Core features, Auth para 1`
- [ ] `C-CF-04` `constraint` An expired token is refused. `src: Core features, Auth para 1`
- [ ] `C-CF-05` `constraint` A signup whose username is already taken is rejected as invalid, creating no account. `src: Core features, Auth rule 1`
- [ ] `C-CF-06` `constraint` A signup body carrying a `role` field still creates a `reader`. `src: Core features, Auth rule 2`
- [ ] `C-CF-07` `constraint` A login with the wrong password is denied, returning no token. `src: Core features, Auth rule 3`
- [ ] `C-CF-08` `capability` An author creates a page through three steps, each at its own address. `src: Core features, page model rule 1`
- [ ] `C-CF-09` `capability` Leaving a creation step, then returning to the step, keeps what was entered. `src: Core features, page model rule 1`
- [ ] `C-CF-10` `data` A new page is created in state `draft`. `src: Core features, page model rule 2`
- [ ] `C-CF-11` `data` Publishing sets the state to `published`, recording the moment the change happened. `src: Core features, page model rule 3`
- [ ] `C-CF-12` `data` Unpublishing returns the state to `draft`, so the route stops resolving for everyone except an author. `src: Core features, page model rule 4`
- [ ] `C-CF-13` `constraint` Two pages in state `published` may not share a route, so the second attempt is rejected as invalid. `src: Core features, page model rule 5`
- [ ] `C-CF-14` `data` Band positions are unique within a page, running from one upward with no gaps. `src: Core features, page model rule 6`
- [ ] `C-CF-15` `role` A reader asking to publish a page is denied by the server, leaving the page state unchanged. `src: Core features, page model rule 7`
- [ ] `C-CF-16` `capability` A request for the public route of a page in state `draft` renders the not-found page for an anonymous visitor. `src: Core features, draft visibility rule 1`
- [ ] `C-CF-17` `capability` `GET /api/pages/{slug}` returns a page in state `draft` only to an author session. `src: Core features, draft visibility rule 2`
- [ ] `C-CF-18` `capability` `GET /api/pages` returns only pages in state `published` to an anonymous caller. `src: Core features, draft visibility rule 3`
- [ ] `C-CF-19` `capability` A media object belonging to a page in state `draft` is unreadable without an author session at every address the app offers. `src: Core features, draft visibility rule 4`
- [ ] `C-CF-20` `capability` Publishing a page makes the route, the record, the media readable to everyone at once. `src: Core features, draft visibility rule 5`
- [ ] `C-CF-21` `literal` The object key is `pages/{page_id}/{sha256_of_bytes}.{ext}`. `src: Core features, media rule 1`
- [ ] `C-CF-22` `constraint` The same bytes uploaded twice to one page produce a single object, never a second row. `src: Core features, media rule 2`
- [ ] `C-CF-23` `data` Bytes live only in the object store, so the database holds the key with the metadata alone. `src: Core features, media rule 3`
- [ ] `C-CF-24` `capability` Media belonging to a page in state `published` is streamed to anyone from an address the app owns. `src: Core features, media rule 4`
- [ ] `C-CF-25` `constraint` An uploaded image with no alternative text is rejected as invalid. `src: Core features, media rule 5`
- [ ] `C-CF-26` `capability` Every internal link on every public route resolves to a page that exists. `src: Core features, public routes rule 1`
- [ ] `C-CF-27` `capability` An unknown address renders the product not-found page, answering as not found. `src: Core features, public routes rule 2`
- [ ] `C-CF-28` `data` Each page view of a public route is recorded with the route beside the moment the view happened. `src: Core features, public routes rule 3`
- [ ] `C-CF-29` `capability` An author reads the per-route view totals at `/studio/views`. `src: Core features, public routes rule 3`
- [ ] `C-CF-30` `ui` The home page renders twelve bands in the stated order, opening on the hero, closing on the footer. `src: Core features, home page band order`
- [ ] `C-CF-31` `ui` The home hero carries the launch chip, the headline, the standfirst, two sign-up pills, the reassurance line. `src: Core features, home rule 1`
- [ ] `C-CF-32` `ui` The home hero right half is a booking card whose day cells respond to a click, leaving confirmation disabled. `src: Core features, home rule 2`
- [ ] `C-CF-33` `ui` The trusted-by band carries eight wordmarks in a continuous marquee. `src: Core features, home rule 3`
- [ ] `C-CF-34` `ui` The testimonial band carries six seeded quote cards with their attributions. `src: Core features, home rule 7`
- [ ] `C-CF-35` `ui` The home FAQ names the two plan prices in whole dollars per user per month. `src: Core features, home rule 9`
- [ ] `C-CF-36` `ui` The teams route opens on an avatar wall, carrying the capability ticker, the six additional-feature cards, the six use-case cards. `src: Core features, other routes rule 1`
- [ ] `C-CF-37` `ui` The voice sub-brand route renders on a dark ground, carrying the phone mock, the call log, the price band. `src: Core features, other routes rule 2`
- [ ] `C-CF-38` `ui` The embed route carries four solution cards, one per embedding option. `src: Core features, other routes rule 3`
- [ ] `C-CF-39` `ui` The six light editorial routes carry the headlines pinned for them. `src: Core features, other routes rule 5`
- [ ] `C-CF-40` `ui` The help route indexes articles as category cards; the docs route carries a sidebar tree beside a section rail. `src: Core features, other routes rule 6`
- [ ] `C-CF-41` `ui` A floating pill bar sits on every page, staying put as the page scrolls beneath. `src: Core features, chrome rule 1`
- [ ] `C-CF-42` `ui` Three header items open dropdown panels on hover, closing on leave. `src: Core features, chrome rule 2`
- [ ] `C-CF-43` `ui` The footer carries four link columns over the identity block, the seals, the status pill, the download chips. `src: Core features, chrome rule 4`
- [ ] `C-CF-44` `capability` A successful signup creates one booking page for the account at `/USERNAME` on the app origin. `src: Core features, trial rule 2`
- [ ] `C-CF-45` `data` A username is unique, compared case-folded. `src: Core features, trial rule 3`

## C-UF User flow

- [ ] `C-UF-01` `capability` Fifteen public routes answer without a session. `src: User flow route table`
- [ ] `C-UF-02` `role` The studio routes answer only to an author session. `src: User flow route table`
- [ ] `C-UF-03` `capability` An anonymous request for a studio address lands on `/login`, continuing afterwards to the address first asked for. `src: User flow, entry paragraph`
- [ ] `C-UF-04` `role` A reader session asking for `/studio` is refused, landing on `/`. `src: User flow, entry paragraph`
- [ ] `C-UF-05` `capability` A token expiring mid-action returns the studio to `/login`, leaving the edited row unchanged. `src: User flow, entry paragraph`
- [ ] `C-UF-06` `ui` The studio lists pages on the left beside the selected page on the right. `src: User flow, journey 2`
- [ ] `C-UF-07` `ui` A published row shows the new state ahead of the save answering, returning to `draft` with a message when the save fails. `src: User flow, journey 3`
- [ ] `C-UF-08` `ui` Every list carries an empty state saying what to do next, never a blank panel. `src: User flow, states paragraph`
- [ ] `C-UF-09` `ui` Every page carries a loading state drawn as the shimmer skeleton. `src: User flow, states paragraph`
- [ ] `C-UF-10` `ui` An error leaves the rest of the page standing, carrying the message on the band that failed. `src: User flow, states paragraph`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Every band sits inside a rounded panel inset from the page edges, so the page reads as a stack of large cards. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The primary action wears the deep cool neutral, worn by nothing else on a page. `src: UI/UX notes, colour paragraph`
- [ ] `C-UX-03` `ui` Feedback washes carry meaning, one wash apiece for attention, error, information, success. `src: UI/UX notes, colour paragraph`
- [ ] `C-UX-04` `ui` Headlines are set in Manrope at 700; body copy is set in Inter. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-05` `ui` Motion arrives rather than drifts, so a band entering raises its children with a fade, staggered a beat apart. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-06` `ui` A reduced-motion request freezes the marquees, turning reveals into plain appearances. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-07` `ui` Body text meets WCAG AA contrast on the light pages, on the dark page too. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-08` `ui` Every content image carries alternative text; a decorative image declares itself decorative. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-09` `ui` Keyboard navigation reaches every control, with the focus ring always visible. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-10` `ui` At a narrow viewport nothing overflows sideways; every navigation target stays reachable. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-11` `ui` Below the tablet breakpoint the header centre links fold behind a menu control whose drawer drops from the top. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-12` `ui` At a phone width the booking card month grid runs full width, its slot column rising as a bottom sheet. `src: UI/UX notes, responsive paragraph`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The front end is built with SvelteKit; the JSON interface is built with Fastify. `src: Technical requirements para 1`
- [ ] `C-TR-02` `constraint` PostgreSQL with MinIO are the only backing services, so reaching for another is a contract violation. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` Every provider address is read from the environment, never hardcoded. `src: Technical requirements para 2`
- [ ] `C-TR-04` `contract` Every response carries a generated request id in a header, repeated on the structured log line. `src: Technical requirements para 3`
- [ ] `C-TR-05` `capability` Every public route declares its own title beside its own description, shared with no other route. `src: Technical requirements para 4`
- [ ] `C-TR-06` `capability` Every public route declares a social preview title beside a preview image that resolves. `src: Technical requirements para 4`
- [ ] `C-TR-07` `constraint` No binary asset ships, so portraits, seals, star rows, glyphs, posters are drawn procedurally from a seed. `src: Technical requirements para 6`
- [ ] `C-TR-08` `constraint` One booking-card component serves the hero, the embed miniatures, the personal booking page. `src: Technical requirements para 7`

## C-DM Data model

- [ ] `C-DM-01` `data` The store carries nine tables whose timestamps are held in universal time. `src: Data model para 1`
- [ ] `C-DM-02` `literal` The seeded password `deku-demo-pw-2026` works at login, appearing in `/app/USER_README.md` beside each account. `src: Data model, password paragraph`
- [ ] `C-DM-03` `data` A page slug is unique; a page state is either `draft` or `published`. `src: Data model, pages row`
- [ ] `C-DM-04` `data` Two publishes colliding on one route must not both succeed, so exactly one wins. `src: Data model, pages row`
- [ ] `C-DM-05` `data` A media object key is unique, being the only address the bytes have. `src: Data model, media row`
- [ ] `C-DM-06` `data` Page-view rows are only ever added. `src: Data model, page_views row`
- [ ] `C-DM-07` `data` One booking page row belongs to one account. `src: Data model, booking_pages row`
- [ ] `C-DM-08` `data` A failed publish leaves no partial state, so no orphaned media row survives. `src: Data model, derived paragraph`
- [ ] `C-DM-09` `data` Fifteen pages are seeded at the fifteen public routes in state `published`. `src: Data model, seed paragraph`
- [ ] `C-DM-10` `data` One page is seeded in state `draft` at `/blog/scheduling-links-that-convert`, carrying one media object. `src: Data model, seed paragraph`
- [ ] `C-DM-11` `data` Seeding is idempotent, so restarting the app duplicates no row. `src: Data model, seed paragraph`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Seven pieces of shared furniture recur on every page, built once apiece. `src: Front-end specification, shared furniture`
- [ ] `C-FE-02` `ui` Every icon is inline vector geometry inheriting the current colour, never an image file. `src: Front-end specification, iconography`
- [ ] `C-FE-03` `ui` Fifteen named motion moments ship, from the toast slide to the shimmer sweep. `src: Front-end specification, named moments`
- [ ] `C-FE-04` `ui` Avatars are seeded radial gradients in two ramp tones under initials in the display face. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-05` `ui` The documentation search entry opens a command palette on a click, on the slash key too. `src: Front-end specification, accordion and palette`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product holds one tenant, so no organisation, no workspace, no per-customer subdomain exists. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` Nothing in the build sends a message, so no email, no SMS leaves the product. `src: Constraints bullet 3`
- [ ] `C-CN-03` `constraint` Nothing charges, so the plan prices stay copy on a page. `src: Constraints bullet 4`
- [ ] `C-CN-04` `constraint` No background job, no cron, no scheduler, no task queue runs. `src: Constraints bullet 8`
- [ ] `C-CN-05` `constraint` The site stays responsive at the seeded volume of pages, bands, media objects, recorded page views. `src: Constraints bullet 10`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`, both read from the environment. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP interface is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual step. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` Reserved `.browser_screenshots/` directories exist at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` Reserved `.downloads/` directories exist at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `contract` A production build is served behind a static or preview server, never a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends, never as a child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-11` `contract` The server binds `0.0.0.0`, never `127.0.0.1` or `localhost`. `src: Deployment contract bullet 9`
- [ ] `C-DC-12` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes note`
- [ ] `C-DC-13` `constraint` An invalid or unauthorized call is rejected as a client error, never a `5xx`, never a silent success. `src: Deployment contract, API shapes note`
- [ ] `C-DC-14` `constraint` Uploaded bytes live in the MinIO bucket, so a copy on the app filesystem counts for nothing. `src: Deployment contract, no mocks block`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `author@example.com` | seeded author account | C-RL-09 | User roles, seeded accounts |
| `reader@example.com` | seeded reader account | C-RL-10 | User roles, seeded accounts |
| `deku-demo-pw-2026` | seeded password for every account | C-RL-11 | User roles, seeded accounts |
| `POST /api/auth/login` | login endpoint | C-CF-01 | Core features, Auth |
| `{"access_token"}` | login response key | C-CF-01 | Core features, Auth |
| `POST /api/auth/signup` | signup endpoint | C-CF-02 | Core features, Auth |
| `reader` | role created by signup | C-CF-02 | Core features, Auth |
| `GET /api/pages/{slug}` | one-page endpoint | C-CF-17 | Core features, draft visibility |
| `GET /api/pages` | page-list endpoint | C-CF-18 | Core features, draft visibility |
| `pages/{page_id}/{sha256_of_bytes}.{ext}` | object-key scheme | C-CF-21 | Core features, media |
| `/studio/views` | page-view totals route | C-CF-29 | Core features, public routes |
| `/USERNAME` | personal booking page route | C-CF-44 | Core features, trial |
| `/login` | sign-in route | C-UF-03 | User flow, entry |
| `/studio` | authoring surface route | C-UF-04 | User flow, entry |
| `draft` | unpublished page state | C-DM-03 | Data model, pages |
| `published` | live page state | C-DM-03 | Data model, pages |
| `/blog/scheduling-links-that-convert` | seeded draft route | C-DM-10 | Data model, seed |
| `/app/USER_README.md` | credential file path | C-DM-02 | Data model, password paragraph |
| `APP_PUBLIC_URL` | app origin variable | C-DC-01 | Deployment contract |
| `${APP_PUBLIC_PORT}:4173` | port mapping | C-DC-02 | Deployment contract |
| `/api` | interface prefix | C-DC-03 | Deployment contract |
| `GET /api/health` | health route | C-DC-04 | Deployment contract |
| `200` | health response status | C-DC-04 | Deployment contract |
| `.browser_screenshots/` | reserved directory | C-DC-07 | Deployment contract |
| `.downloads/` | reserved directory | C-DC-08 | Deployment contract |
| `0.0.0.0` | bind address | C-DC-11 | Deployment contract |
| `127.0.0.1` | forbidden bind address | C-DC-11 | Deployment contract |
| `localhost` | forbidden bind address | C-DC-11 | Deployment contract |
| `5xx` | forbidden rejection class | C-DC-13 | Deployment contract |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the exact shade of every named colour role | C-UX-02 | named by family, tone, shade, with the value left open |
| the duration of every named motion moment | C-FE-03 | named by character only, with no timing given |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 3 | 3 |
| User roles | 11 | 11 |
| Core features | 45 | 45 |
| User flow | 10 | 10 |
| UI and UX notes | 12 | 12 |
| Technical requirements | 8 | 8 |
| Data model | 11 | 11 |
| Front-end specification | 5 | 5 |
| Constraints | 5 | 5 |
| Deployment contract | 14 | 14 |
