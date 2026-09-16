# Monolith Scroll Archive

Build Monolith Scroll Archive, a cinematic scroll experience for a studio that does real-time 3D work, with a personal frame archive over it. A visitor scrolls a published ten-chapter story, each chapter a lit scene with a poster image. A signed-in member captures a frame from any published chapter into a personal archive, titles it and saves it, finds the archive and their reading place waiting on the next device, reorders the frames and publishes an ordered set as a guided route other visitors can follow. A curator, the studio, publishes chapters to the public story and features or hides the routes members build. The one end-to-end outcome that defines "working": a signed-out visitor reads the published chapters and their posters, while a member signs in, captures a frame, sees the same archive and reading position on a fresh session, reorders the captures and publishes a route another visitor can open; a chapter that is still a draft, and its poster, are never served to the public, and only a curator may publish a chapter or feature a route.

## Overview

Monolith is a public scroll story over one chapter catalogue, with a personal archive and a small curator back-office behind it. The public half is open to anyone with no account: the published chapters in their story order, each chapter's poster image, and the published routes members have made. The private half has two signed-in roles: a member who captures frames from the chapters into a personal archive and publishes ordered sets of them as routes, and a curator, the studio, who publishes chapters to the public story and features or hides the routes.

What a visitor sees in the story is the set of published chapters, compiled on read from the chapter rows, never from a list the app keeps for itself, and a chapter's poster is public only when that chapter is published. A captured frame is a member's own record of a moment in a chapter, carrying the chapter it came from and a title the member gives it; the frame image itself is not stored on the server, so a member's archive travels by the record, and the poster a card shows is the published chapter's stored poster.

The genuinely hard part is the line between a draft chapter and a published one, and the fidelity of a member's archive across devices. A draft chapter and its stored poster must never reach the public, publishing is what opens both, a member's captures and their last reading position must read back unchanged on a fresh session, and a route is readable by other visitors only once its owner publishes it.

## User roles

There is a public visitor with no account, a signed-in `visitor` who is a member, and a `curator` who is the studio. Signup is open: anyone may create a `visitor` account. A `curator` account exists only as a seeded record. Every seeded account signs in with the password `deku-demo-pw-2026`; it is benchmark fixture data, not a secret, and it is written into `/app/USER_README.md` beside each account so a reviewer can sign in.

| Role | Can read | Can write |
|---|---|---|
| public visitor | the published chapters, their posters, and the published routes | nothing |
| `visitor` | the public story, plus their own archive of captures and routes | capture a frame, reorder the captures in a route they own, and publish a route they own |
| `curator` | everything, including the draft chapters and every member's captures | publish a chapter to the public story, and feature or hide any route |

Authorization is enforced server-side on every member endpoint and on every curator endpoint. Hiding a control in the interface is not authorization: a request from a signed-out visitor to any member or curator endpoint, a request from a `visitor` to a curator endpoint, or a write from a `visitor` against a route they do not own, must be refused by the server, leaving the protected state unchanged. A signed-out request is refused with the `not-signed-in` kind; a signed-in request that its role or ownership does not permit is refused with the `not-allowed-for-you` kind.

## Core features

- Read the published story. Anyone may read the published chapters in their story order, each carrying its slug, act, title, caption, position and poster reference. A draft chapter is never listed.
- Read a chapter poster. Anyone may read the poster image of a published chapter, streamed from the object store under that chapter's poster key; the poster of a draft chapter is not public and is refused as `no-such-thing`.
- Publish a chapter. A curator publishes a draft chapter, which opens the chapter and its poster to the public story. A member or a signed-out visitor is refused.
- Capture a frame. A signed-in member captures a frame from a published chapter into their archive, giving it a title and recording the chapter and the scroll position; a capture missing its title is refused as `something-missing-or-wrong` and nothing is written.
- Find the archive and the reading place. A member reads their own archive of captures and routes, and their last reading position; the captures, routes and position are held server-side, so a fresh session on another device reads the same archive and the same reading position.
- Reorder the captures in a route. A member sets the order of the captures in a route they own; the order is the sequence a follower reads.
- Publish a route. A member publishes a route they own that holds at least two captures, which opens it on the public routes index; a route with fewer than two captures is refused as `the-rules-dont-allow-that`, and a draft route is private to its owner.
- Feature or hide a route. A curator features a published route, promoting it on the public index, or hides a route so it leaves the public index; a member is refused.
- Choose a cookie preference. A first-time visitor is asked once whether non-essential cookies are allowed, and the choice they make survives a reload so the notice is not shown again.

The API routes:

| Route | Who | Purpose |
|---|---|---|
| `GET /api/health` | anyone | readiness |
| `GET /api/chapters` | anyone | list the published chapters in story order |
| `GET /api/chapters/{id}` | anyone | read one published chapter |
| `GET /api/chapters/{id}/poster` | anyone | read a published chapter's poster image |
| `GET /api/routes` | anyone | list the published routes |
| `GET /api/routes/{id}` | anyone | read one published route |
| `POST /api/auth/signup` | anyone | create one member account |
| `POST /api/auth/login` | anyone | sign in an account |
| `GET /api/me` | signed in | the caller's own email, role and reading position |
| `PUT /api/me/position` | `visitor` | set the caller's reading position |
| `GET /api/me/archive` | `visitor` | the caller's own captures and routes |
| `POST /api/captures` | `visitor` | capture a frame into the archive |
| `POST /api/routes` | `visitor` | create a route from the caller's captures |
| `POST /api/routes/{id}/order` | `visitor` | set the order of a route's captures |
| `POST /api/routes/{id}/publish` | `visitor` | publish a route the caller owns |
| `POST /api/chapters/{id}/publish` | `curator` | publish a draft chapter |
| `POST /api/routes/{id}/feature` | `curator` | feature a published route |
| `POST /api/routes/{id}/hide` | `curator` | hide a route |

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the scroll story of the published chapters | public |
| `/routes` | the published routes index | public |
| `/routes/{id}` | one published route | public |
| `/privacy` | the privacy page, linked from every footer | public |
| `/sign-in` | sign in | public |
| `/sign-up` | create a member account | public |
| `/archive` | the member's own captures and routes | `visitor` |
| `/curator` | the curator feature queue | `curator` |

**Entry and redirects.** An unauthenticated request for the archive or the curator queue lands on the sign-in; a signed-in member opening the sign-in lands on their archive, and a curator on the feature queue; a token that expires mid-action returns to the sign-in changing nothing. A member who opens the curator queue is refused, not shown an empty version. An unknown address renders the site's own not-found page with a way back to the story, and answers not-found.

A visitor lands on the story and scrolls the published chapters in order, each a lit scene with a poster, then opens the routes index to read a published route another member built. A member signs in, captures a frame from a chapter, gives it a title and saves it, and on success sees the frame join their archive; signing in again on another device, the member finds the same archive and the same reading position waiting. The member reorders the captures in a route and publishes it, and now another visitor opens that route from the index. A curator signs in, publishes a draft chapter so it joins the public story, and features a member's route so it is promoted on the index, or hides one so it leaves the index.

## UI/UX notes

North star: a visitor should feel, from the first scroll, that Monolith is one continuous cinematic film wound back and forth by the scrollbar rather than a page of sections, and a member should be able to keep a frame and find it again without ever losing that calm, dark register. The character is austere and reverent over a near-neutral palette: a dark stage fills the window behind everything, a warm cream chrome ink carries essentially every label and heading, and the one red accent is spent only on the loading counter and a featured route mark so it stays meaningful. The 3D stage carries its own scene palette of sky blue, cyan, moss green and deep neutral, kept off the chrome, and the giant act headings dissolve edge-lit in warm orange and amber rather than fading. Type is two families: a very heavy display face for the act headings and the loading counter, and a rounded strip face for the act marks, so a heading reads as an image while a label reads as chrome.

Motion is almost entirely scroll-driven: the chapters dissolve through the scene itself as the visitor scrolls, the act marks glide rather than jump, and nothing plays on its own except the chrome fading in once and the loading counter. The archive keeps the same register: a captured frame joins the grid with a quiet confirmation, and a reorder is its own feedback with no toast. Under a reduced-motion preference every animation collapses to an instant change of state and the story stays readable without motion.

Colour is by role, never decoration: one dark ground, one cream ink, and the single red accent on the featured mark alone; a rejected form field is the one place a warning colour appears, and it always sits beside a word so meaning never rests on colour alone. Each page leads with one clear primary action set apart from the secondary controls, and the archive grid and the routes index read as calm sections drawn from the same system. Every chapter poster and every frame image carries descriptive alternative text naming what the scene shows, and any purely decorative flourish declares itself decorative so a screen reader passes over it.

Accessibility is a contract: body text and its background meet WCAG AA contrast against the ground, touch targets are comfortably sized, keyboard navigation reaches every act mark, every route link and the capture and route forms with a visible focus ring that is never removed, and each page carries exactly one first-level heading. The layout stays responsive and holds at every viewport width: at a narrow viewport, on a phone, nothing overflows sideways, every navigation target stays reachable, and the archive grid reflows to a single readable column, up to a wide desktop. Not this: a chapter poster with no alternative text, or the featured red carrying meaning with no word beside it.

## Constraints

- Ship no binary assets in the repository: no image, video, audio or font binary, and no charting library. Every interface icon and the studio mark are drawn in code as inline vector geometry, and typography comes from a named open family with a system fallback stack or from system fonts. A chapter poster is the object stored for that chapter in the object store, and any seeded poster image is generated into the store at startup rather than shipped as a file.
- What the story and the routes index show is compiled on read from the chapter and route rows and their stored posters. An in-memory copy of the chapters, a count the app caches instead of reading the rows, or a poster served from anywhere other than the stored object under the chapter's poster key are contract violations however good the page looks.
- A draft chapter, and the poster of any unpublished chapter, are private: neither is listed nor served to the public, and publishing is the only thing that opens them.
- A captured frame image is not stored on the server: a capture records the chapter and the scroll position and a title, and the frame a card shows is the published chapter's stored poster; there is no image upload endpoint.
- A member's captures, routes and last reading position are held server-side, so a fresh session reads them back unchanged. A member owns at most one archive; a route is readable by another visitor only once its owner publishes it.
- No second database, cache, queue, identity provider, mail vendor or search service: the only backing services in this environment are PostgreSQL and the MinIO object store, and reaching for anything else is a contract violation.
- No clock-driven scheduler and no runtime network calls beyond PostgreSQL and the object store. No native app, offline mode or push notifications.
- The site stays responsive with the twelve seeded chapters, 500 routes and 5000 captures.

## Technical requirements

The application is implemented in Python. The app is a server-rendered site whose pages are produced on the server and returned as a fully formed document on first paint, enhanced with plain vanilla progressive-enhancement JavaScript over it, with no single-page framework. The JSON API is served by the same application on the same origin under the `/api` prefix. Persistence is PostgreSQL. Object storage is the MinIO object store, S3-compatible, into which each chapter poster is written under that chapter's key. Auth is app-implemented email and password with bearer tokens; passwords are hashed. A bearer token is required on every member endpoint and every curator endpoint; `POST /api/auth/login`, `POST /api/auth/signup`, `GET /api/health`, and the public reads need none.

The poster for a chapter is stored in the object store under a fixed key scheme with the shape `posters/{chapter_id}/{sha256_of_bytes}.{ext}`, for example `posters/solar/9f2a1c.png`. The bytes live only in the object store, never on the local filesystem and never inside a database row. A public poster read streams the stored object for a published chapter, with the stored content type, and a public poster read for a draft or unknown chapter returns the `no-such-thing` kind with an HTTP `404`.

Every public route carries its own document title and its own description, and no two public routes share a title or a description, so the story, the routes index, a route page, the sign-in and the privacy page each announce themselves distinctly. Every public route also declares a social preview title and a social preview image, and the preview image resolves. Every response carries the standard security headers, including a strict transport policy and a nosniff content-type policy. No credential, bearer token or object-store key appears in anything the browser downloads.

The cookie preference is remembered in a cookie named `cookie_choice`: a first visit carrying no such cookie shows the notice asking whether non-essential cookies are allowed, and a request carrying the `cookie_choice` cookie does not show the notice again.

Every failure returns a body of the shape `{ "error": { "kind": ..., "message": ... } }`, where `message` is written for a human and never exposes internal detail. The six failure kinds are exactly: `not-signed-in`, `not-allowed-for-you`, `something-missing-or-wrong`, `no-such-thing`, `that-clashes`, and `the-rules-dont-allow-that`. A list endpoint returns a top-level JSON array. Field names are exactly as written in this brief. A business-rule violation is a client error carrying a reason, never a server error and never a silent success.

Endpoints and their observable contracts:

- `GET /api/health` returns `200` once the app is ready.
- `GET /api/chapters` returns an array of the published chapters in story order, each with `id`, `act`, `title`, `caption` and `position`. A draft chapter never appears.
- `GET /api/chapters/{id}` returns a published chapter with `id`, `act`, `title`, `caption`, `position` and `state`. A slug that is unknown or still a draft returns the `no-such-thing` kind with an HTTP `404`.
- `GET /api/chapters/{id}/poster` returns the poster image bytes of a published chapter, streamed from the object store under the chapter's key, with the stored content type. A draft or unknown chapter returns `no-such-thing` with an HTTP `404`.
- `GET /api/routes` returns an array of the published routes, each with `id`, `name`, `status` and `owner_name`. A draft or hidden route never appears.
- `GET /api/routes/{id}` returns a published route with `id`, `name`, `status` and an ordered `captures` array, each capture with `id`, `title`, `chapter_id` and `ordinal`. A route that is a draft or hidden returns `no-such-thing` with an HTTP `404` to a caller who does not own it.
- `POST /api/auth/signup` accepts `email`, `password` and `name` and creates one member account with the role `visitor`, returning `201`. An email that already has an account is refused with `that-clashes` and an HTTP `409`.
- `POST /api/auth/login` accepts `email` and `password` and returns an `access_token` and the caller's `email` and `role`. A wrong email or password is refused with `not-signed-in`.
- `GET /api/me` returns the caller's `email`, `role` and `last_position` to a valid-token caller.
- `PUT /api/me/position` accepts `position`, a number between 0 and 1, sets the caller's reading position, and returns `200`.
- `GET /api/me/archive` returns the caller's own `captures` and `routes`, each capture with `id`, `title`, `chapter_id` and `position`, and each route with `id`, `name` and `status`. This endpoint is member-only.
- `POST /api/captures` accepts `title`, `chapter_id` and `position`, records one capture owned by the caller, and returns `201` with the created capture. A missing `title`, or a `chapter_id` naming a draft or unknown chapter, is refused with `something-missing-or-wrong` or `no-such-thing`. This endpoint is member-only.
- `POST /api/routes` accepts `name` and a `capture_ids` array of at least one of the caller's captures, creates a draft route, and returns `201`. A name shorter than the pinned minimum, or an empty `capture_ids`, is refused with `something-missing-or-wrong`. A route holds at least two captures only once it is published. This endpoint is member-only.
- `POST /api/routes/{id}/order` accepts an ordered `capture_ids` array and sets the order of a route the caller owns, returning `200`. A route the caller does not own is refused with `not-allowed-for-you`.
- `POST /api/routes/{id}/publish` publishes a route the caller owns and returns it with `status` `published`; a route holding fewer than two captures is refused with `the-rules-dont-allow-that` and an HTTP `409`, unchanged. A route the caller does not own is refused with `not-allowed-for-you`.
- `POST /api/chapters/{id}/publish` publishes a draft chapter and returns it with `state` `published`; the chapter and its poster are now public. This endpoint is curator-only; a member or signed-out caller is refused.
- `POST /api/routes/{id}/feature` features a published route and returns it with `status` `featured`. This endpoint is curator-only.
- `POST /api/routes/{id}/hide` hides a route and returns it with `status` `hidden`, and the route leaves the public index. This endpoint is curator-only.

## Data model

The application stores these entities. Field names below are the contract. All timestamps are UTC.

- `users`: `id`, `email` (unique, lowercase), `password_hash`, `name`, `role` (`visitor` or `curator`), `last_position` (a number between 0 and 1, default 0), `created_at`. Seeded accounts, and open member signup.
- `chapters`: `id` (a slug, the story identifier), `act` (one of the five act names), `title`, `caption`, `position` (a whole number, the story order), `state` (`draft` or `published`), `poster_object_key` (the object-store key of the chapter's poster), `poster_content_type`, `created_at`. A chapter is public only when its `state` is `published`.
- `captures`: `id`, `owner_id` (the capturing member), `title` (1 to 80 characters), `chapter_id` (a published chapter), `position` (a number between 0 and 1, the scroll fraction), `created_at`. One row per captured frame; the frame image is not stored.
- `routes`: `id`, `owner_id` (the owning member), `name` (3 to 80 characters), `status` (`draft`, `published`, `featured` or `hidden`), `created_at`, `updated_at`.
- `route_items`: `route_id`, `capture_id`, `ordinal` (a whole number contiguous from 0, the follow order).

The story and the routes index are compiled on read from the `chapters` rows whose `state` is `published` and the `routes` rows whose `status` is `published` or `featured`, so publishing a chapter or a route changes what the public reads on the very next request with no second place to keep in step. A chapter poster is public only when its chapter is published.

**Seed data.**

- Accounts, each with the password `deku-demo-pw-2026`: `curator@example.com` as `curator`; `visitor@example.com` as `visitor`, with captures and routes; `visitor2@example.com` as `visitor`, with an empty archive.
- Chapters, twelve in total, each with one seeded poster generated into the store under `posters/{chapter_id}/...`. The published chapters, in story order, are `solar` "Cosmic Origins", `standing-stone` "The Discovery", `history` "What We Make", `device` "Framed In Glass", `fall` "The Descent", `desert` "New Horizons", `swamp` "Transformation", `winter-landscape` "New Worlds", `world` "Infinite Canvas" and `ending` "Keep What You Saw". The draft chapters, not public, are `bone` "The Turning" and `forest-landscape` "We Build Realities".
- Captures owned by `visitor@example.com`: "Opening Light" on `solar`; "The Descent" on `fall`; "Infinite" on `world`.
- Routes owned by `visitor@example.com`: "First Light", `published`, holding the `solar` and `world` captures; "Working Set", `draft`, holding the `fall` and `solar` captures.
- The reading position of `visitor@example.com` is `0.42`.

Seeding must be idempotent: restarting the app must not duplicate a row or a stored object.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`; `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. This app uses two backing services: `postgres`, reached through `DATABASE_URL` and `DB_URL` (the same value); and a MinIO object store, reached through `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`, into which each chapter poster is written. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

## Definition of done

The build is done when: a signed-out visitor reads the published chapters in story order and reads each chapter poster streamed from the stored object, while the draft chapters `bone` and `forest-landscape` and their posters return `no-such-thing` and `404`; a curator publishes a draft chapter so it joins the public story, and a member or signed-out caller who tries is refused; a member captures a frame with a title, and a capture missing its title is refused with `something-missing-or-wrong` and writes nothing; a member reads the same archive and the same reading position `0.42` on a fresh session after setting a new position, proving the archive travels server-side; a member reorders the captures in a route and publishes a route holding at least two captures so another visitor opens it from the index, while a route with fewer than two captures is refused with `the-rules-dont-allow-that` and `409`; a curator features a published route and hides a route so it leaves the index, while a member who tries is refused with `not-allowed-for-you`; a signed-out request for a member or curator endpoint is refused with `not-signed-in`; the first visit asks once about non-essential cookies and the answer survives a reload; and every public route answers with its own title and description and a social preview whose image resolves.
