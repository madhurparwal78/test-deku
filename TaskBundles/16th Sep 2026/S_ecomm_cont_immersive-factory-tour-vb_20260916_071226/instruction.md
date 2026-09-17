# Marlowe Workshop Experience

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, take the published workshop tour through its three stations, and submit a prize-draw entry that is actually stored, without hitting an error page. The tour content is real published content, not a hardcoded page: each station's poster image must live as an object in the object store, and a draft chapter that the maker has not published yet must NOT be readable by a stranger by any means, including a direct request for its object. A green tick the app shows itself does not count; the poster must exist in the bucket at its key, and the draft's poster must be refused.

## Overview

Marlowe is a small apparel maker, and this is its branded workshop experience: a playful, gamified marketing site that turns the story of how a polo shirt is made into a guided tour of a stylised virtual workshop, and converts that attention into one action, a prize-draw entry. The maker publishes the tour as content: three workshop chapters, one per production station (knitting, dyeing and embroidering), and three signature prize garments, each carrying its own stored poster image. Visitors sign up, walk the tour collecting points at glowing hotspots, and enter a draw for a chance to win one of three shirts.

Its audiences are brand fans after a playful moment, prospective buyers looking for a reason to want the shirt, and prize hunters after the draw. The product is deliberately small. It is not a shop: there is no cart, no checkout, no payment and no catalogue browsing. It publishes a fixed, curated experience and captures one lead per visitor. Everything a visitor sees on the tour is content the maker has published; anything still in draft is private to the maker.

The product opens onto the workshop title screen. The genuinely hard part is that publishing is real: a chapter's poster image must be written to the object store and a draft chapter's poster must never be readable by someone who is not the maker. The second hard part is that a visitor may enter the draw only once: two entries from the same visitor, even submitted at the same moment, must resolve to exactly one stored entry.

## User roles

Signup is open: a visitor may create a reader account. The maker account is seeded.

| Role | Can read | Can write | Cannot |
|---|---|---|---|
| `author` | every chapter and prize including drafts; every prize-draw entry | create, edit, publish and unpublish chapters and prizes; read the entry list | **cannot** submit a prize-draw entry as the maker's own promotional act is out of scope |
| `reader` | every **published** chapter and prize; its own single prize-draw entry | sign up, take the tour, record a score, submit one prize-draw entry | **cannot** create or publish content; **cannot** read a draft chapter or its poster; **cannot** read another reader's entry |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a control in the UI is not authorization: a direct API call from a `reader` session to any `author`-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged. A request by a stranger or a `reader` for a draft chapter's stored poster is refused; only a published chapter's poster is publicly readable.

Seeded accounts, every one using the password `deku-demo-pw-2026`:

- `author@example.com` is the maker, the `author`.
- `reader@example.com` is a seeded `reader` who has taken the tour.
- `reader2@example.com` is a second seeded `reader`.

## Core features

### Auth

Accounts are email and password. Signing in is `POST /api/auth/login` with `{"email", "password"}`, which returns an `access_token`. Signup is open at `POST /api/auth/signup`, which creates a `reader`. The app hashes the password with a standard password hashing scheme; the plaintext is never stored. The client sends the returned bearer token on every later request; an expired or missing token on a protected route is rejected as unauthorized. A refused sign-in does not reveal which of the email or the password was wrong.

### Publishing a workshop chapter

1. The `author` creates a chapter with a station name from `knitting`, `dyeing`, `embroidering`, a title, a body, and a poster image. The poster bytes are written to the object store at the key scheme `chapters/{chapter_id}/{sha256_of_bytes}.{ext}`, for example `chapters/1/9f2a1c...d0.webp`. The bytes live only in the object store: never on the app's own filesystem, never as a database blob.
2. A chapter is created as a `draft` and becomes visible on the public tour only when the `author` publishes it. Publishing sets its state to `published`.
3. A `draft` chapter, and its stored poster object, are readable only by the `author`. A stranger or a `reader` requesting a draft chapter, or fetching its poster object directly, is refused. A `published` chapter's poster is publicly readable.
4. The `author` may unpublish a chapter, returning it to `draft`, after which its poster is no longer publicly readable.

### Publishing the prize garments

1. The `author` publishes three prize garments, `Signature Green`, `Sunbeam Yellow` and `Sky Blue`, each with a title and a stored image object at the key scheme `prizes/{prize_id}/{sha256_of_bytes}.{ext}`.
2. Only published prizes appear in the promo and on the prize-draw surface.

### The guided tour and score

1. A signed-in `reader` takes the tour: the three published chapters are presented in the fixed order `knitting`, `dyeing`, `embroidering`, each with its own tint and hotspots.
2. Triggering a hotspot increments the reader's running score. The score is held per reader and persists, so it survives a reload and is available at the tour's end.
3. Only published chapters appear on the tour; a draft chapter is absent from it.

### The prize-draw entry

This is the one action that touches stored state for a reader, and it is graded hardest.

1. A signed-in `reader` submits one prize-draw entry with a civility from `MR`, `MRS`, `Other`, `Prefer not to say`, a first name, a last name, an email, a birthdate, a country from the country list (for example `Australia`, `Canada`, `France`, `Germany`, `Ireland`, `United Kingdom`), and the two consent flags: `consent_terms` and `consent_marketing`.
2. The entry is stored only when `consent_terms` is true; a submission without it is refused as invalid and nothing is stored.
3. A `reader` may hold at most one entry. A second submission by the same reader, whether it arrives later or at the same moment as the first, does not create a second entry: exactly one entry exists for that reader afterwards, and the duplicate is refused as a `409 Conflict`.
4. On success the reader sees the confirmation `If you are selected, we will contact you by email. Stay tuned.`

### Cookie consent

1. A first-time visitor is asked once about non-essential cookies before any non-essential storage or analytics is set, and the answer survives a reload.

### Privacy page

1. A privacy page, reachable from the footer of every page, states what the experience stores about a visitor and how long a prize-draw entry is kept.
2. The footer of every page also links the legal prize-draw terms and the brand's social profiles on Instagram and TikTok.

## User flow

### Routes

| Route | Purpose | Auth |
|---|---|---|
| `/` | the title screen and the start of the tour | public |
| `/login` | credential entry | public |
| `/signup` | reader registration | public |
| `/tour` | the guided tour of published chapters | reader |
| `/chapter/1` | one published chapter (`/chapter/<id>`) | reader |
| `/prizes` | the published prize garments and the promo | public |
| `/enter` | the prize-draw entry form (`dedicated-route`) | reader |
| `/studio` | the maker's content studio, chapters and prizes and entries | author |
| `/privacy` | the privacy policy | public |

### Entry and redirects

- An unauthenticated visitor on a reader route is sent to `/login`; on an author route, also to `/login`.
- A successful sign-in lands a `reader` on `/tour` and the `author` on `/studio`.
- Signing out returns to `/` and invalidates the client's token for later requests.
- A token that expires mid-action causes the next request to be rejected as unauthorized, and the interface returns the visitor to `/login`.
- A `reader` that opens `/studio` is returned to `/tour`; the redirect is a courtesy and the underlying endpoint denies the request regardless.

### Journeys

1. **Take the tour and enter.** `reader@example.com` signs in, lands on `/tour`, moves through the three published chapters triggering hotspots so the score rises, reaches the end, opens `/enter`, fills the form, ticks the terms consent, and submits. The confirmation appears and the entry is stored.
2. **Publish a chapter.** `author@example.com` signs in, opens `/studio`, creates a knitting chapter with a poster, and publishes it. The poster object now exists in the store and the chapter appears on the public tour.
3. **Draft stays private.** A stranger requests a draft chapter's poster object directly and is refused; the same object becomes readable only after the author publishes the chapter.
4. **Enter once.** `reader2@example.com` submits an entry, then submits again; the second is refused and exactly one entry remains.

### States

Every list has an empty state: a tour with no published chapters, a studio with no chapters, a prize list with none. Every page has a loading state while its data is in flight. A failed panel replaces only that panel, with a way to retry, and never takes down the rest of the screen. A refused submission rolls back the optimistic row and shows the reason; a submission is applied optimistically and reconciled with the server, and reverts with a message if the server refuses. An unknown address renders the experience's own not-found page with a way back.

## UI/UX notes

Marlowe's workshop experience is loud, tactile and brand-forward, and its design is carried over from the reference this brief was built against. The north star is delight: a visitor should feel they have stepped inside a playful, living workshop rather than landing on a marketing page. The register is consumer and expressive, so the title screen carries atmosphere and motion where a back-office tool would stay quiet. Motion is continuous and physical: the backdrop turns, mascots drift, the central emblem tilts and shivers, and hotspots bounce in.

**Palette by role, stated in words, never as a colour code.** The exact shade is yours as long as each role reads as described. The experience is anchored on a deep, near-black green as the primary brand colour against a bright, vivid yellow used for large display type and decoration only, never for small body text on a light ground. A saturated mid green carries the primary action and appears on nothing else that competes with it. Three soft pastel machine tints, one per station, key the three rooms: a pale, soft blue for knitting, a pale, soft yellow for dyeing, and a pale, near-white green for embroidering. Warm neutral creams and off-whites carry backgrounds; a vivid red carries alerts and one preloader colourway. Body text meets its contrast bar: the deep green on white and white on deep green both pass, and the bright yellow is reserved for large display type. No page is dominated by a single hue with no second signal.

**Typography is exact, because a typeface is an identity rather than a value to echo.** Headings use a wide display family (a wide geometric sans fallback stack where the licensed family is absent); interface text, buttons and form fields use the open-licence `Mona Sans` with a platform sans-serif fallback. The whole type scale derives from one root measure: a large display size for the title, a `16px` body, `15px` secondary, `14px` small labels, `13px` fine print, `12px` finest, and a `26px` bold sub-heading, with figures aligning wherever amounts stack.

**Shape, density, motion.** Corners are round and soft throughout: pill buttons, oval emblems and large radii, with form fields on a small radius, the primary call to action on a medium radius, and the registration modal on a large radius. Density is comfortable and spacious on the title screen, tightening only in the studio. Motion character is physical and continuous: a small, reusable family of eased curves covers hovers and panel entrances, an overshoot curve gives the springy hotspot pop and the call-to-action settle, and a continuous spin turns the backdrop. State a single transition family and reuse it. The registration form rises from below the screen and rests on a deep, soft, layered shadow. Every animation respects a reduced-motion preference, dropping the continuous spins, the mascot drift and the station shiver to a single settle while the tour stays completable, and cross-fading the hotspot pops rather than bouncing them.

**Components and states.** Every interactive element has a resting, pointed-at, pressed, focused and unavailable state, and an unavailable control is never signalled by colour alone. Escape closes any open menu or modal; the destructive unpublish confirms first. Icon-only controls carry text labels for assistive technology, and every icon is drawn as inline vector geometry rather than loaded from an image or icon font. A persistent sound toggle sits top right because the experience ships with sound on, and a persistent prize-draw promo card sits bottom right.

**Accessibility floors, which are contract and not taste.** Body text and its background meet WCAG AA contrast at a ratio of at least `4.5:1`. The tour is fully operable by keyboard, with a visible focus ring on every control and keyboard navigation across stations and hotspots, and the three-station story is available as readable text so a screen-reader user gets the same content. Nothing important is carried by sound or colour alone; the score and the current station are always shown as text. Every content image, including a published poster, carries alternative text.

**Responsive behaviour that holds at every width between the named tiers.** On a wide viewport the tour is a landscape scene with the promo card in the corner; below the desktop breakpoint the menu becomes a full-screen panel, tap targets grow, and the entry form fills the width. A phone held in portrait is gently asked to turn to landscape. At a narrow viewport nothing overflows sideways and every navigation target stays reachable. Full-height regions size from a scripted live height rather than raw viewport units, so mobile browser chrome appearing does not resize the scene.

## Technical requirements

The application is a server-rendered island app: pages are rendered on the server with Express and SvelteKit and hydrated as interactive islands, so the browser receives complete pages on first paint with the heavy tour surface hydrating in place. The same server exposes a JSON HTTP API on the same origin under the `/api` prefix, which is the contract the rest of this brief pins. Serve a production build behind a production server, never a development server. Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, identity provider or object store: the only backing services available in this environment are `PostgreSQL` and `MinIO`, and reaching for anything else is a contract violation.

Persist all application data in `PostgreSQL`, read from the `DATABASE_URL` environment variable. Store every poster and prize image as an object in `MinIO`, read from `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`; the bucket is private, so a draft chapter's poster is served only through the app to an entitled caller or a short-lived link, never as a public object URL. These backing services are already running and reachable at those variables; do not download, install, compile or start a copy of either. Never hardcode a host or a port; read them from the environment. Authentication is app-implemented email and password with bearer tokens. `GET /api/health` returns `200` once the app is ready.

The experience must stay correct when a visitor acts twice at once. Two entry submissions from the same reader, arriving together, must produce exactly one stored entry, and the loser is rejected with a `409 Conflict`. At most one entry exists for a reader afterwards, so a second submission is refused rather than creating a second entry. A submission that carries the same client request id as an earlier one must not create a second entry, and there is no second write. These guarantees must hold under real simultaneous requests.

No credential, access key, bearer token or object-store secret appears in anything the browser downloads: not in a page, a script, a template or an API response body meant for the client. Every HTTP response carries the standard security headers, including a strict transport policy and a content-type nosniff policy, so a response is never interpreted as a type it did not declare. The document head declares a favicon that the site serves.

## Data model

Six entities. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

- **account** - id, email, name, role in `author`, `reader`, password hash. Signup creates a `reader`.
- **chapter** - id, station in `knitting`, `dyeing`, `embroidering`, title, body, poster object key, state in `draft`, `published`, created at, updated at. The poster key follows `chapters/{chapter_id}/{sha256_of_bytes}.{ext}`. A chapter's poster object lives in the object store, never on the app disk and never as a database blob.
- **prize** - id, name in `Signature Green`, `Sunbeam Yellow`, `Sky Blue`, title, image object key, state in `draft`, `published`. The image key follows `prizes/{prize_id}/{sha256_of_bytes}.{ext}`.
- **entry** - id, reader id, civility, first name, last name, email, birthdate, country, consent terms, consent marketing, client request id, created at. At most one entry exists per reader; this is an invariant of the stored data, true even when two submissions from one reader race, not merely a check in the request handler.
- **score** - id, reader id, points, updated at. One score row per reader, accumulated across the tour.
- **hotspot** - id, chapter id, points. The scoring targets belonging to a chapter.

Derived rather than stored: whether a chapter is on the public tour (it is `published`); the reader's total score (accumulated as hotspots are triggered).

**Seed data.** One `author` account `author@example.com` and two `reader` accounts `reader@example.com` and `reader2@example.com`. Three published chapters, one per station `knitting`, `dyeing`, `embroidering`, each with a stored poster object and at least one hotspot. At least one `draft` chapter whose poster object exists in the store but is not publicly readable, so the protected-content rule is observable. Three published prizes `Signature Green`, `Sunbeam Yellow`, `Sky Blue`, each with a stored image. `reader@example.com` already holds a score. Seeding must be idempotent: restarting the app must not duplicate rows or objects.

## Build plan

1. Shell and tokens: routing, the entry-mode title screen, the preloader, the cookie-consent gate, the privacy page, and the design-system tokens.
2. Data and auth: every entity above, the migrations and the idempotent seed, email-and-password auth with bearer tokens, and the `author` and `reader` roles.
3. Publishing: the studio, chapter and prize creation writing the poster bytes to the object store at their key scheme, the draft-to-published transition, and the server-side rule that a draft's object is readable only by the author.
4. The tour: the three published chapters in order, the hotspots and the running score, presented as the gamified scene.
5. The prize draw: the entry form and its validation, the consent gate, the one-entry-per-reader invariant under concurrency, and the confirmation.
6. Hardening: the empty, loading and failed states, the optimistic-row rollback, the security headers, the favicon, and the reduced-motion and keyboard passes.
7. Deploy and self-check: the production build, the detached start, and a walk through every journey.

## Constraints

- No shop: no cart, no checkout, no payment, no product catalogue, no order.
- One prize-draw entry per reader; the maker does not enter.
- No public sign-up for authors; the maker account is seeded.
- No external network calls at runtime beyond the named backing services; no third-party analytics endpoint beyond the consent-gated measurement identifier, and no external asset host.
- No native application; the product is a web app only.
- No font file, image file, video file, three-dimensional model, environment map or audio file is served; every asset class is substituted procedurally, and posters uploaded by the author are the only binary objects, and they live in the object store.
- The experience does not scroll as a page; progression is by state transition through the tour.
- The scene must stay responsive on a three-year-old laptop; performance is a loading strategy first.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
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

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | email, password, name | an `access_token` and the reader |
| `POST /api/auth/login` | email, password | an `access_token` and the account |
| `GET /api/health` | (none) | `200` when ready |
| `GET /api/tour` | (bearer, reader) | a top-level array of published chapters in station order |
| `GET /api/chapters` | (bearer, author) | a top-level array of every chapter including drafts |
| `POST /api/chapters` | station, title, body, poster | the created draft chapter with its poster key |
| `POST /api/chapters/<id>/publish` | (bearer, author) | the chapter, now published |
| `POST /api/chapters/<id>/unpublish` | (bearer, author) | the chapter, now draft |
| `GET /api/chapters/<id>/poster` | (bearer) | the poster bytes for a published chapter, or for a draft only to the author |
| `GET /api/prizes` | (none) | a top-level array of published prizes |
| `POST /api/prizes` | name, title, image | the created prize with its image key |
| `POST /api/score` | points | the reader's updated running score |
| `POST /api/entries` | civility, first name, last name, email, birthdate, country, consent terms, consent marketing, optional client request id | the created entry |
| `GET /api/entries` | (bearer, author) | a top-level array of every prize-draw entry |

Every list endpoint returns a top-level JSON array. A successful call returns the named resource; an invalid or unauthorized call is rejected as a client error, never as a server error and never as a silent success; the agent chooses conventional status codes and the graders accept the class. Bearer auth is required on everything except `POST /api/auth/signup`, `POST /api/auth/login`, `GET /api/health`, `GET /api/prizes` and a published chapter's poster.

**No mocks.** A poster or prize image must exist as a real object in `MinIO` at its key; bytes on the app container's filesystem, or an in-memory map the app answers from, do not count. A prize-draw entry must be a real row in `PostgreSQL`; an in-memory list does not count. The named provider is the fact: the app's UI and its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A visitor can sign up, take the published three-station tour with a score that survives a reload, and submit a single prize-draw entry that is stored and confirmed. The maker can publish a chapter whose poster becomes a real object in the store, and a draft chapter's poster stays unreadable to anyone but the maker until it is published. A reader who submits twice ends with exactly one entry, never two. The app is deployed, healthy, reachable in a browser, and ships no image, font or media file, with every list showing an empty, loading and populated state.
