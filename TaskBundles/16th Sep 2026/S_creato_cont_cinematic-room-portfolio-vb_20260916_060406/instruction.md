# Atrium

Build Atrium, a cinematic single-page portfolio for an independent creator-musician. The public site is a vertical stack of full-height rooms, each a lit scene with a short label, a large name, a sentence, an optional paragraph and up to three glass buttons, and a small music player in the page header that plays the creator's releases in order. A signed-in visitor signs the guest book once. The creator owns the back-of-house studio: they write the rooms, upload each room's scene image, add releases to the player, reorder the rooms, and publish. The one end-to-end outcome that defines "working": a signed-out visitor reads the published rooms in order with their scene images and plays the releases, while the creator signs in, rewrites a room and uploads its scene, sees the change on their own working copy while a fresh visitor still sees the last published version, and only after the creator publishes again does a fresh visitor read the new room; a draft site and its scene images are never served to the public, and a signed-out visitor cannot sign the guest book.

## Overview

Atrium is a personal site presented as a set of rooms rather than a scrolling article: each room fills the window as one lit scene, a visitor moves a whole room at a time, and the record plays from a small player in the header. What a visitor sees on the public site is the last published version of the site, compiled on read from the published snapshot, never from whatever the creator happens to be editing.

The public half is open to anyone with no account: the rooms in their published order, each room's scene image, the header player that steps through the published releases, and the guest book beneath the last room. A signed-in visitor may sign the guest book once. The private half is the creator's studio: the owner writes and edits the rooms, uploads a scene image for each, manages the releases that feed the player, reorders the rooms, and publishes; the owner also moderates the guest book on their own site.

The genuinely hard part is the line between what the creator is editing and what a visitor sees. A site has three states: a draft site has never been published and its public address returns nothing; a published site serves its last snapshot; a site edited after publishing is dirty and still serves the last snapshot to visitors while the owner sees the working copy. Publishing is the only thing that moves an edit onto the public site, and a room's scene image is public only when that room is part of the published snapshot: the image a public page shows is the object that actually sits in the store under that room's key, not bytes the app kept for itself.

## User roles

There is a public reader with no account, a signed-in `visitor`, and the site owner, a `creator`. Signup is open: anyone may create a `visitor` account, and a `creator` account is created for the seeded site owners. Every seeded account signs in with the password `deku-demo-pw-2026`; it is benchmark fixture data, not a secret, and it is written into `/app/USER_README.md` beside each account so a reviewer can sign in.

| Role | Can read | Can write |
|---|---|---|
| public reader | the published site: the rooms in order, their scene images, the releases, and the standing guest-book notes | nothing |
| `visitor` | the published site, plus their own guest-book note | one standing guest-book note per site |
| `creator` | the published site of anyone, plus the full working copy of their own site | write and reorder their own rooms, upload their own scene images, manage their own releases, publish their own site, and hide or restore a note on their own guest book |

Authorization is enforced server-side on every studio endpoint and on every write. Hiding a control in the interface is not authorization: a studio request from a signed-out reader, a studio request from a `visitor`, or any write from a `creator` against a site they do not own must be refused by the server, leaving the protected state unchanged. A signed-out request for a studio endpoint is refused with the `not-signed-in` kind; a signed-in request that its role or ownership does not permit is refused with the `not-allowed-for-you` kind.

## Core features

- Read the published site. Anyone may read a published site: its rooms in their published order, each room with its label, name, sentence, optional paragraph, alignment and up to three buttons, and the releases that feed the header player. A draft site returns nothing to the public.
- Read a room's scene image. Anyone may read the scene image of a room in the published snapshot, streamed from the object store under that room's key; the scene image of a draft site, or of a room not in the published snapshot, is not public and is refused as `no-such-thing`.
- Play the record. The header player lists the published releases in their position order, each with its title, artist and track title, so a visitor can step through them. A site with no releases has no player at all.
- Sign the guest book. A signed-in visitor leaves one standing note carrying the note text and the room they were in; the same visitor signing the same site again is refused as `that-clashes` and keeps their existing note. A signed-out reader who tries to sign is refused as `not-signed-in`, and the note is never written.
- Write a room. The creator creates a room and edits its label, name, sentence, paragraph, alignment and buttons, and uploads one scene image for it, which is written to the object store under that room's key. Editing a room on a site that is already published moves the site to the dirty state, and the edit stays off the public site until the next publish.
- Reorder the rooms. The creator sets the order of the rooms on their own site; the public site keeps showing the last published order until the creator publishes again.
- Publish the site. Publishing copies the working copy of every room and release into the published snapshot and records the moment of publication; from then on the public read serves that snapshot, the owner reading their own site still sees the working copy, and a fresh visitor reads a change only after a second publish.
- Moderate the guest book. On their own site the creator hides a standing note, which removes it from the public guest book, and restores a hidden note, which returns it to the book; hiding a note does not free the note author's one-note slot, so the author still cannot sign a second time.
- A privacy footer note. A privacy page, reachable from the footer of every page, states what Atrium stores about a visitor who signs the guest book and how long a note is kept.

The API routes:

| Route | Who | Purpose |
|---|---|---|
| `GET /api/health` | anyone | readiness |
| `GET /api/sites/{handle}` | anyone | read the published snapshot of a site by its handle |
| `GET /api/sites/{handle}/rooms/{room_id}/scene` | anyone | read a published room's scene image |
| `GET /api/sites/{handle}/guestbook` | anyone | read the standing notes on a published site |
| `POST /api/sites/{handle}/guestbook` | `visitor` | sign one standing note |
| `POST /api/auth/signup` | anyone | create one visitor account |
| `POST /api/auth/login` | anyone | sign in an account |
| `GET /api/me` | signed in | the caller's own email and role |
| `GET /api/studio/site` | `creator` | the working copy of the caller's own site |
| `POST /api/studio/rooms` | `creator` | create a room on the caller's own site |
| `PATCH /api/studio/rooms/{room_id}` | `creator` | edit a room the caller owns |
| `PUT /api/studio/rooms/{room_id}/scene` | `creator` | upload a room's scene image |
| `POST /api/studio/rooms/order` | `creator` | set the order of the caller's rooms |
| `POST /api/studio/releases` | `creator` | add a release to the caller's own player |
| `POST /api/studio/publish` | `creator` | publish the caller's own site |
| `POST /api/studio/guestbook/{note_id}/hide` | `creator` | hide a note on the caller's own guest book |
| `POST /api/studio/guestbook/{note_id}/restore` | `creator` | restore a hidden note on the caller's own guest book |

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the rooms page for the owner's own published site | public |
| `/s/{handle}` | the rooms page for a site read by its handle | public |
| `/privacy` | the privacy page, linked from every footer | public |
| `/sign-in` | sign in | public |
| `/sign-up` | create a visitor account | public |
| `/studio` | the creator's studio dashboard | `creator` |
| `/studio/rooms` | the room list and ordering | `creator` |
| `/studio/room/{room_id}` | the room editor | `creator` |
| `/studio/releases` | the release manager | `creator` |

**Entry and redirects.** An unauthenticated request for a studio route lands on the sign-in; a signed-in creator opening the studio lands on their dashboard; a token that expires mid-action returns to the sign-in changing nothing. A visitor who opens the studio is refused, not shown an empty version. An unknown address renders Atrium's own not-found page with a way back to the rooms, and answers not-found.

A visitor lands on the rooms page and moves through the rooms a whole room at a time, by scrolling, by the up and down arrow keys, or by the markers in the rail down the right edge; the marker for the room they have reached is lit. The header player steps through the published releases, starting only when the visitor presses play. Beneath the last room the visitor reads the standing guest-book notes. A signed-in visitor signs the book once, giving the note text and the room they were in, and on success sees the note join the book in place; signing the same site again is refused in place and keeps the first note.

The creator signs in and opens the studio. They open a room in the editor, rewrite its sentence and upload a new scene image; on success the room shows the change on the creator's own working copy, and the site moves to the dirty state. A fresh visitor opening the site still reads the last published version, not the edit. The creator reorders the rooms, then publishes, and now a fresh visitor reads the new room in its new place with its new scene, while the guest-book note that visitor left earlier is still standing. The creator opens the guest book, hides a note that breaks the house rules so it leaves the public book, and restores it.

## UI/UX notes

North star: a visitor should feel, within the first room, that Atrium is one creator's nocturnal, classical, slightly-absurd world, and should be able to move through the whole site a room at a time without ever reaching for a menu. The character is a near-monochrome night gallery: the page ground is a near-black neutral, each room is one dim lit scene of marble statuary filling the window, and white engraved capitals sit over the scene without a panel because the type is shadowed rather than boxed. The interface is glass rather than paint: buttons are a blurred layer over the scene with a hairline near-white border, and they respond to hover by brightening the border to solid white and lifting a soft glow rather than by filling. The only saturated colours in the whole product are a burnt red and a brass orange, which appear together in a single accent, with a cool blue and a rose red reserved for one signal each; every other surface is a neutral.

Motion is the room-at-a-time feeling: scenes hold still and fill the window while each room's text eases up and lifts into place on arrival, and the label, the name, the sentence and the buttons animate in a short staggered sequence at one considered speed across the whole site, and nothing overshoots or loops. The transition into a room and the guest-book note joining the book both settle in and out at that same eased speed. Under a reduced-motion preference every transition and reveal collapses to a still change of state and the rooms stay reachable without motion.

Colour is by role, never decoration: one near-black ground, one plainer surface a shade off it for the studio cards, one white ink, one muted ink, one hairline border, and the single burnt-red-and-brass accent on the one primary action alone. Two guest-book note states, standing and hidden, each carry one meaning that appears nowhere else and always sit beside a word, so meaning never rests on colour alone. The studio deliberately inverts the public look, using opaque dark cards on a plain ground rather than glass over a scene, so the owner always knows which side of the site they are on.

Every page leads with one clear primary action set apart from every secondary one: on a room it is the room's own first button, in the guest book it is Sign the book, and in the studio it is Publish; a page never presents two actions of equal weight competing to be first. Every scene image carries descriptive alternative text naming what the scene shows, and any purely decorative flourish declares itself decorative so a screen reader passes over it.

Accessibility is a contract: body text and its background meet WCAG AA contrast against the ground in both the dark theme and the light theme, touch targets are comfortably sized, keyboard navigation reaches every room, every button and the guest-book form with a visible focus ring that is never removed, each page carries exactly one first-level heading, and the arrow keys alone carry a visitor from the first room to the last. The layout stays responsive and holds at every viewport width from a narrow phone breakpoint, where the rail collapses and the rooms stack to a single readable column with the page body never scrolling sideways, up to a wide desktop. Commit to a dark theme and a light theme and design both fully. Not this: a scene image with no alternative text, or one hue carrying both note states with no second signal.

## Constraints

- Ship no binary assets in the repository: no image, video, audio or font binary, and no charting library. Every interface icon and the rail markers are drawn in code as inline vector geometry, and typography comes from a named open family with a system fallback stack or from system fonts. A room's scene image is the object stored for that room in the object store, and any seeded scene image is generated into the store at startup rather than shipped as a file.
- What a public page shows is the last published snapshot, compiled on read from the published rows and their stored objects. An in-memory copy of the rooms, a count the app caches instead of reading the rows, or a scene image served from anywhere other than the stored object under the room's key are contract violations however good the page looks.
- A draft site, and the scene image of any room not in the published snapshot, are private: neither is served to the public, and publishing is the only thing that opens them.
- A visitor signs at most one standing note per site: a second attempt on the same site keeps the first note and writes nothing. Hiding a note does not free its author's slot.
- No scheduled or timed publishing and no preview address: the owner previews by reading their own signed-in site, which serves the working copy while every other reader gets the snapshot.
- No second database, cache, queue, identity provider, mail vendor or search service: the only backing services in this environment are PostgreSQL and the MinIO object store, and reaching for anything else is a contract violation.
- No clock-driven scheduler and no runtime network calls beyond PostgreSQL and the object store. No native app, offline mode or push notifications.
- The site stays responsive with 20 rooms, 40 releases and 5000 guest-book notes.

## Technical requirements

The application is implemented in Python. The app is a server-rendered site whose pages are produced on the server and returned as a fully formed document on first paint, enhanced with plain vanilla progressive-enhancement JavaScript over it, with no single-page framework. The JSON API is served by the same application on the same origin under the `/api` prefix. Persistence is PostgreSQL. Object storage is the MinIO object store, S3-compatible, into which each room's scene image is written under that room's key. Auth is app-implemented email and password with bearer tokens; passwords are hashed. A bearer token is required on every studio endpoint and on signing the guest book; `POST /api/auth/login`, `POST /api/auth/signup`, `GET /api/health`, and the public reads need none.

The scene image for a room is stored in the object store under a fixed key scheme with the shape `scenes/{site_id}/{room_id}/{sha256_of_bytes}.{ext}`, for example `scenes/7/42/9f2a1c.png`. The bytes live only in the object store, never on the local filesystem and never inside a database row. A public scene read streams the stored object for a room that is part of the published snapshot, with the stored content type, and a public scene read for a draft site or a room outside the published snapshot returns the `no-such-thing` kind with an HTTP `404`.

Every public route carries its own document title and its own description, and no two public routes share a title or a description, so a room page, the privacy page and the sign-in each announce themselves distinctly. The site serves a sitemap that lists every public route, and a robots file that points at that sitemap. No credential, bearer token or object-store key appears in anything the browser downloads.

Every failure returns a body of the shape `{ "error": { "kind": ..., "message": ... } }`, where `message` is written for a human and never exposes internal detail. The six failure kinds are exactly: `not-signed-in`, `not-allowed-for-you`, `something-missing-or-wrong`, `no-such-thing`, `that-clashes`, and `the-rules-dont-allow-that`. A list endpoint returns a top-level JSON array. Field names are exactly as written in this brief. A business-rule violation is a client error carrying a reason, never a server error and never a silent success.

Endpoints and their observable contracts:

- `GET /api/health` returns `200` once the app is ready.
- `GET /api/sites/{handle}` returns a published site with `handle`, `name`, `theme_default`, an ordered `rooms` array and an ordered `releases` array. Each room carries `id`, `label`, `name`, `sentence`, `paragraph`, `align`, `marker`, `scene_url` and an ordered `buttons` array, each button with `label`, `glyph` and `destination`. Each release carries `id`, `title`, `artist`, `track_title` and `position`. A handle that is unknown, or a site that is still a draft, returns the `no-such-thing` kind with an HTTP `404`, except that the owner reading their own site receives the working copy with a `viewer` object whose `working_copy` is `true`.
- `GET /api/sites/{handle}/rooms/{room_id}/scene` returns the scene image bytes of a room in the published snapshot, streamed from the object store under the room's key, with the stored content type. A draft site, or a room outside the published snapshot, returns `no-such-thing` with an HTTP `404`.
- `GET /api/sites/{handle}/guestbook` returns an array of the standing notes on a published site, each with `id`, `text`, `display_name`, `room_id` and `created_at`; a hidden note never appears.
- `POST /api/sites/{handle}/guestbook` accepts `text` and `room_id` and returns `201` with the created note. A signed-out caller is refused with `not-signed-in`. A visitor who already has a standing note on that site is refused with `that-clashes` and an HTTP `409`, and no second note is written. A payload missing `text`, or a `text` longer than the pinned limit, is refused with `something-missing-or-wrong`.
- `POST /api/auth/signup` accepts `email`, `password` and `display_name` and creates one visitor account, returning `201`. An email that already has an account is refused with `that-clashes` and an HTTP `409`.
- `POST /api/auth/login` accepts `email` and `password` and returns an `access_token` and the caller's `email` and `role`. A wrong email or password is refused with `not-signed-in`.
- `GET /api/me` returns the caller's `email` and `role` to a valid-token caller.
- `GET /api/studio/site` returns the working copy of the caller's own site, with the same shape as the public read plus each room's `scene_url` and the site `state`. A caller who owns no site is refused with `no-such-thing`.
- `POST /api/studio/rooms` accepts `label`, `name`, `sentence`, `paragraph`, `align` and `buttons`, creates a room at the end of the caller's own site, and returns `201`. This endpoint is `creator`-only.
- `PATCH /api/studio/rooms/{room_id}` edits a room the caller owns and returns it; editing a room on a published site moves the site to `dirty`. A creator editing a room on a site they do not own is refused with `not-allowed-for-you` and an HTTP `403`, unchanged.
- `PUT /api/studio/rooms/{room_id}/scene` accepts a base64 `image` and its `content_type`, writes the bytes to the object store under the room's key, and returns `200` with the room's `object_key`. This endpoint is `creator`-only and owner-scoped.
- `POST /api/studio/rooms/order` accepts an ordered array of the caller's room ids and sets their order, returning `200`; the public order does not change until the next publish. An id belonging to another owner's site is refused with `not-allowed-for-you`.
- `POST /api/studio/releases` accepts `title`, `artist`, `track_title` and adds a release at the end of the caller's player, returning `201`.
- `POST /api/studio/publish` copies the caller's working copy into the published snapshot, sets the site `state` to `published` and records `published_at`, and returns the published site. Publishing a site with no complete room is refused with `the-rules-dont-allow-that`.
- `POST /api/studio/guestbook/{note_id}/hide` hides a standing note on the caller's own guest book and returns it with `state` `hidden`; the note leaves the public book and the author's one-note slot stays taken. A creator hiding a note on a site they do not own is refused with `not-allowed-for-you`.
- `POST /api/studio/guestbook/{note_id}/restore` restores a hidden note on the caller's own guest book and returns it with `state` `standing`.

## Data model

The application stores these entities. Field names below are the contract. All timestamps are UTC.

- `users`: `id`, `email` (unique, lowercase), `password_hash`, `display_name`, `role` (`creator` or `visitor`), `created_at`. Seeded creators and visitors, and open visitor signup.
- `sites`: `id`, `owner_id` (the owning user, one site per owner), `handle` (unique, kebab-case), `name`, `state` (`draft`, `published` or `dirty`), `theme_default` (`dark` or `light`), `published_at` (null until first publish), `created_at`, `updated_at`.
- `rooms`: `id`, `site_id`, `position` (a whole number contiguous from 1, the visitor order), `label`, `name`, `sentence`, `paragraph`, `align` (`left`, `centre` or `right`), `marker` (a short room marker unique within the site), `scene_object_key` (the object-store key of the room's scene image, null until one is uploaded), `scene_content_type`, `created_at`, `updated_at`. The scene bytes live in the object store under `scene_object_key`, never inside the row.
- `room_buttons`: `id`, `room_id`, `position` (1 to 3), `label`, `glyph` (a named icon), `destination` (a room marker or an absolute address).
- `releases`: `id`, `site_id`, `position` (a whole number contiguous from 1, the playback order), `title`, `artist`, `track_title`, `created_at`.
- `notes`: `id`, `site_id`, `author_id` (the signing visitor), `room_id` (the room the visitor was in), `text`, `state` (`standing` or `hidden`), `created_at`. One standing note per author per site.
- `snapshots`: `id`, `site_id`, `published_at`, `body` (the published copy of the site's rooms, room buttons and releases at the moment of publication, with each room's scene object key). The public read of a site is served from the latest snapshot for that site; there is no second place the public content is kept.

The public site is served from the latest `snapshots` row for that site, so publishing a site changes what the public reads on the very next request with no second place to keep in step. A room's scene image is public only when that room's key is part of the latest snapshot.

**Seed data.**

- Users, each with the password `deku-demo-pw-2026`: `creator@example.com` as `creator`, owner of the published site; `creator2@example.com` as `creator`, owner of the draft site; `visitor@example.com` as `visitor`, who has signed one note; `visitor2@example.com` as `visitor`, who has signed none.
- Sites: `atrium` "Atrium", owned by `creator@example.com`, `published`, `theme_default` `dark`; `nightshift` "Nightshift", owned by `creator2@example.com`, `draft`, never published.
- Rooms on `atrium`, in order, each with one seeded scene image generated into the store under its key: position 1, `label` "Who I am", `name` "Lord Vinyl", `marker` "who"; position 2, `label` "The guitar", `name` "Long Wave", `marker` "guitar"; position 3, `label` "The band", `name` "Iron Monk", `marker` "band". The `nightshift` site has one room, position 1, `label` "Coming soon", `name` "Nightshift", and is not published, so neither the site nor its scene is public.
- Releases on `atrium`, in order: position 1, "Long Wave" by "Lord Vinyl"; position 2, "Thundersnow" by "Iron Monk"; position 3, "Monkcore" by "Iron Monk".
- Guest-book notes: one standing note on `atrium` by `visitor@example.com`, room 1, text "The first room stopped me cold."

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
- The backing services named in this brief are already running and reachable at their environment variables. This app uses two backing services: `postgres`, reached through `DATABASE_URL` and `DB_URL` (the same value); and a MinIO object store, reached through `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`, into which each room's scene image is written. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

## Definition of done

The build is done when: a signed-out visitor reads the published `atrium` site with its rooms in order and reads each room's scene image streamed from the stored object, while the draft `nightshift` site and its scene return `no-such-thing` and `404`; the header player lists the three published releases in order; a signed-in visitor signs one guest-book note and a second attempt on the same site is refused with `that-clashes` and `409` and keeps the first note, while a signed-out attempt is refused with `not-signed-in` and writes nothing; the creator edits a room and uploads its scene so the site moves to dirty and a fresh visitor still reads the last published version, then publishes so a fresh visitor reads the new room while the earlier guest-book note still stands; a creator writing against a site they do not own is refused with `not-allowed-for-you` and `403` and changes nothing; the creator hides a note so it leaves the public guest book and restores it, and hiding does not free the author's one-note slot; every public route answers with its own title and description and the sitemap lists every public route; and the accessibility and responsiveness floors above hold under a manual keyboard and reduced-motion pass.
