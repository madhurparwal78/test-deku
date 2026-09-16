# Costa Serena Residences

Build Costa Serena Residences, a marketing and availability site for a boutique gated development of twenty-five Mediterranean apartments on the Spanish coast. Visitors read the location and architecture story, browse the released apartments, filter and sort them by typology, bedroom count and interior area, open an apartment to study its floor plans and terrace, and submit a callback request that records the apartment they chose and the contact details they entered. A small sales back-office reads the callback requests and manages which apartments are released to the public. The one end-to-end outcome that defines "working": a signed-out visitor filters the released apartments, opens one to read its floor plan streamed from the object store, and submits a callback request that a signed-in sales user then reads back exactly as it was entered; an apartment that is still coming soon, and its floor plan, are never served to the public, and only a sales user may read the callback requests or change an apartment's availability.

## Overview

Costa Serena is a public marketing site over one apartment catalogue, with a thin sales back-office behind it. The public half is open to anyone with no account: an editorial home that tells the location and architecture story, the apartment index where the released units are browsed, filtered and sorted, an apartment detail page carrying the unit's record and its floor plans, and a callback form that records an enquiry against a chosen apartment. The private half is a sales console where a seeded sales user reads the callback requests and moves an apartment through its availability states.

What a visitor sees in the index and on a detail page is compiled on read from the apartment rows, never from a figure the app keeps for itself, and the live count on the index is always the number of apartments the current filter matches. The catalogue holds twenty-five apartments; the ones a visitor can see are the released ones, and an apartment that is coming soon is not listed, is not readable at its own address, and its floor plan is not served, until a sales user releases it.

The genuinely hard part is the line between a released apartment and a coming-soon one, and the fidelity of a callback request. A coming-soon apartment and its stored floor plan must never reach the public, releasing it is what opens both, and a callback request a sales user reads back must carry the exact apartment reference and contact details the visitor entered, surviving a reload with no second place kept in step.

## User roles

There is a public visitor with no account, and one seeded `sales` role that signs in. The public site needs no account at all: browsing, filtering, opening an apartment and submitting a callback are all open to anyone. Signing in is only for the sales console. Every seeded sales account signs in with the password `deku-demo-pw-2026`; it is benchmark fixture data, not a secret, and it is written into `/app/USER_README.md` beside the account so a reviewer can sign in.

| Role | Can read | Can write |
|---|---|---|
| public visitor | the released apartments, their floor plans and the typologies | one callback request, from the public form |
| `sales` | everything, including the coming-soon apartments and the callback requests | change an apartment's availability |

Authorization is enforced server-side on every sales endpoint. Hiding a control in the interface is not authorization: a direct request from a signed-out visitor to any sales endpoint must be refused by the server, leaving the protected state unchanged. A signed-out request for a sales endpoint is refused with the `not-signed-in` kind.

## Core features

- Browse the released apartments. Anyone may read the released apartments, each carrying its identifier, typology, bedroom count, block, floor, interior area, terrace area, completion and availability. A coming-soon apartment is never listed.
- Filter and sort the apartments. Anyone narrows the released apartments by typology and by bedroom count, and sorts them by interior area, ascending or descending; the filters combine so that an apartment appears only when it matches every active filter, and the count shown is the number of apartments returned.
- Open an apartment. Anyone opens a released apartment at its own address to read its full record and its ordered floor plans. A coming-soon apartment, or an unknown identifier, is refused as `no-such-thing`.
- Read an apartment floor plan. Anyone may read a released apartment's floor plan image, streamed from the object store under that plan's key; the floor plan of a coming-soon apartment is not public and is refused as `no-such-thing`.
- Submit a callback request. A visitor submits the callback form with a name, an email, an optional telephone, an optional apartment of interest, a preferred time window and a consent flag, and the request is recorded with the apartment reference and the contact details entered. A submission missing a required field is refused as `something-missing-or-wrong` and nothing is written.
- Choose a cookie preference. A first-time visitor is asked once whether non-essential cookies are allowed, and the choice they make survives a reload so the notice is not shown again.
- Read the callback requests. A signed-in sales user reads the callback requests, each carrying the apartment reference and the contact details a visitor entered; a signed-out visitor is refused.
- Manage availability. A signed-in sales user changes an apartment's availability, releasing a coming-soon apartment so it joins the public index and its floor plan opens to the public, or marking a released apartment reserved or sold; a signed-out visitor is refused, and an availability change that is not a legal step is refused as `the-rules-dont-allow-that`.

The API routes:

| Route | Who | Purpose |
|---|---|---|
| `GET /api/health` | anyone | readiness |
| `GET /api/typologies` | anyone | the three apartment typologies |
| `GET /api/units` | anyone | list the released apartments, filtered and sorted |
| `GET /api/units/{id}` | anyone | read one released apartment in full |
| `GET /api/units/{id}/plans/{index}/image` | anyone | read a released apartment's floor plan image |
| `POST /api/callbacks` | anyone | record one callback request |
| `POST /api/auth/login` | anyone | sign in a sales account |
| `GET /api/me` | `sales` | the caller's own email and role |
| `GET /api/sales/callbacks` | `sales` | read the callback requests |
| `PATCH /api/sales/units/{id}/availability` | `sales` | change an apartment's availability |

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the editorial home telling the location and architecture story | public |
| `/apartments` | the apartment index with filtering and sorting | public |
| `/apartments/{id}` | one apartment detail page with floor plans | public |
| `/contact` | the contact page with the sales office details | public |
| `/privacy` | the privacy page, linked from every footer | public |
| `/sign-in` | sign in to the sales console | public |
| `/sales` | the sales console with the callback requests | `sales` |

**Entry and redirects.** An unauthenticated request for the sales console lands on the sign-in; a signed-in sales user opening the sign-in lands on the console; a token that expires mid-action returns to the sign-in changing nothing. An unknown address renders the site's own not-found page with a way back to the home, and answers not-found.

A visitor lands on the home and reads the location and architecture story, then opens the apartment index. The index lists the released apartments with a live count, and the visitor narrows them by typology and bedroom count and sorts them by interior area; the address carries the active filter so the view can be shared, and the count always equals the number of apartments shown. The visitor opens an apartment to read its record and study its floor plans, then submits the callback form, which is prefilled with that apartment when opened from a detail page; on success the form is replaced in place by a confirmation, and a submission missing a required field is refused in place with the field named. The first visit asks once about non-essential cookies and remembers the answer.

A sales user signs in and opens the console. They read the callback requests, each showing the apartment a visitor chose and the contact details entered, and they change an apartment's availability, releasing a coming-soon apartment so a fresh visitor now finds it in the index and can open its floor plan, or marking one reserved or sold. A signed-out visitor who opens the console is sent to the sign-in.

## UI/UX notes

North star: a visitor should feel, from the first view, that Costa Serena is a considered, photography-first architectural sales piece rather than a listings grid, and should be able to read the story, narrow the apartments and open one without ever losing the calm editorial register. The character is luxury Mediterranean-editorial over a near-neutral palette: a warm off-white ground, a near-black ink for type on light surfaces, and white type over photography, with the only saturated colours reserved for the callback form, where one green marks a success, one orange marks an alert, and one red marks a rejected field. Type is a three-family contrast: a high-contrast serif for the display headlines and numerals, a formal script for the occasional place-name accent, and a wide grotesque with generous tracking for every functional label and data value, so a bedroom count and an area read as data while a headline reads as an image.

Motion is smoothed and scroll-coupled: photography is uncovered rather than faded as it arrives, headlines animate in from their own offsets, and the whole page reads as one continuously scaling drawing; every transition and reveal eases at one considered speed and nothing overshoots or loops. The one exception is the left-edge scroll meter, an exact unsmoothed hairline with a two-digit percentage readout. Under a reduced-motion preference every reveal and the scroll-coupled motion collapse to a still change of state and the apartments stay reachable without motion.

Colour is by role, never decoration: one warm neutral ground, one ink for type, one accent used only on the primary action, and the three reserved form-status colours that appear nowhere else. The apartment index leads with one clear primary action set apart from the secondary controls, the filter controls read as a quiet row, and the count numeral is the loud element. Every apartment photograph and every floor plan image carries descriptive alternative text naming what it shows, and any purely decorative flourish declares itself decorative so a screen reader passes over it.

Accessibility is a contract: body text and its background meet WCAG AA contrast against the ground, touch targets are comfortably sized, keyboard navigation reaches every filter control, every apartment link and the callback form with a visible focus ring that is never removed, and each page carries exactly one first-level heading. The layout stays responsive and holds at every viewport width: at a narrow viewport, on a phone, nothing overflows sideways, every navigation target stays reachable, and the apartment grid reflows to a single readable column, up to a wide desktop. Not this: a floor plan image with no alternative text, or the form-status green carrying meaning with no word beside it.

## Constraints

- Ship no binary assets in the repository: no image, video or font binary, and no charting library. Every interface icon and the brand mark are drawn in code as inline vector geometry, and typography comes from a named open family with a system fallback stack or from system fonts. An apartment floor plan is the object stored for that plan in the object store, and any seeded floor plan image is generated into the store at startup rather than shipped as a file.
- What the index and a detail page show is compiled on read from the apartment rows and their stored floor plans. An in-memory copy of the apartments, a count the app caches instead of counting the filtered rows, or a floor plan served from anywhere other than the stored object under that plan's key are contract violations however good the page looks.
- A coming-soon apartment is private: it is not listed, not readable at its address, and its floor plan is not served, until a sales user releases it.
- The filters combine with logical and, the count shown is always the length of the filtered set, and sorting by area orders by interior area alone so a large terrace never lifts an apartment above one with a larger interior.
- A callback request records the exact apartment reference and contact details entered, and a sales user reads them back unchanged after a reload.
- No second database, cache, queue, identity provider, mail vendor or search service: the only backing services in this environment are PostgreSQL and the MinIO object store, and reaching for anything else is a contract violation.
- No clock-driven scheduler and no runtime network calls beyond PostgreSQL and the object store. No native app, offline mode or push notifications.
- The site stays responsive with the twenty-five seeded apartments and 5000 callback requests.

## Technical requirements

The application is implemented in Python. The app is a server-rendered site whose pages are produced on the server and returned as a fully formed document on first paint, enhanced with plain vanilla progressive-enhancement JavaScript over it, with no single-page framework. The JSON API is served by the same application on the same origin under the `/api` prefix. Persistence is PostgreSQL. Object storage is the MinIO object store, S3-compatible, into which each apartment floor plan is written under that plan's key. Sales auth is app-implemented email and password with bearer tokens; passwords are hashed. A bearer token is required on every sales endpoint; `POST /api/auth/login`, `GET /api/health`, and the public reads and the public callback form need none.

The floor plan for an apartment is stored in the object store under a fixed key scheme with the shape `plans/{unit_id}/{index}/{sha256_of_bytes}.{ext}`, for example `plans/111/1/9f2a1c.png`. The bytes live only in the object store, never on the local filesystem and never inside a database row. A public floor plan read streams the stored object for a released apartment, with the stored content type, and a public floor plan read for a coming-soon or unknown apartment returns the `no-such-thing` kind with an HTTP `404`.

The apartment list read accepts three query parameters and reflects them so a filtered view can be shared by its address: `type` is one of `all`, `ground-floor`, `ground-floor-basement` or `penthouse-duplex`; `bedrooms` is one of `all`, `2` or `3`; and `sort` is one of `relevant`, `area-asc` or `area-desc`. The parameters combine with logical and, `relevant` keeps the catalogue's own stable order, `area-asc` and `area-desc` order by interior area alone, and the response carries the released apartments the filter matches so the rendered count equals the response length. A coming-soon apartment never appears in this list.

Every public route carries its own document title and its own description, and no two public routes share a title or a description, so the home, the apartment index, a detail page, the contact page and the privacy page each announce themselves distinctly. No credential, bearer token or object-store key appears in anything the browser downloads.

The cookie preference is remembered in a cookie named `cookie_choice`: a first visit carrying no such cookie shows the notice asking whether non-essential cookies are allowed, and a request carrying the `cookie_choice` cookie does not show the notice again.

Every failure returns a body of the shape `{ "error": { "kind": ..., "message": ... } }`, where `message` is written for a human and never exposes internal detail. The six failure kinds are exactly: `not-signed-in`, `not-allowed-for-you`, `something-missing-or-wrong`, `no-such-thing`, `that-clashes`, and `the-rules-dont-allow-that`. A list endpoint returns a top-level JSON array. Field names are exactly as written in this brief. A business-rule violation is a client error carrying a reason, never a server error and never a silent success.

Endpoints and their observable contracts:

- `GET /api/health` returns `200` once the app is ready.
- `GET /api/typologies` returns an array of the three typologies, each with `slug`, `name` and `bedrooms`.
- `GET /api/units` returns an array of the released apartments, each with `id`, `typology`, `bedrooms`, `block`, `floor`, `interior_area`, `terrace_area`, `completion` and `availability`. The `type`, `bedrooms` and `sort` query parameters narrow and order the array; a coming-soon apartment never appears.
- `GET /api/units/{id}` returns a released apartment with `id`, `typology`, `bedrooms`, `block`, `floor`, `interior_area`, `terrace_area`, `completion`, `availability` and an ordered `plans` array, each plan with `index` and `image_url`. An identifier that is unknown or still coming soon returns the `no-such-thing` kind with an HTTP `404`.
- `GET /api/units/{id}/plans/{index}/image` returns the floor plan image bytes of a released apartment, streamed from the object store under the plan's key, with the stored content type. A coming-soon or unknown apartment returns `no-such-thing` with an HTTP `404`.
- `POST /api/callbacks` accepts `name`, `email`, `telephone`, `unit_id`, `preferred_time_window` and `consent`, records one callback request with the apartment reference and contact details, and returns `201` with the created request. A payload missing `name`, `email`, `preferred_time_window` or `consent`, or carrying a `preferred_time_window` outside its set or a `consent` that is not true, is refused with `something-missing-or-wrong` and an HTTP `400` or `422`, and nothing is written. A `unit_id` naming a coming-soon or unknown apartment is refused with `no-such-thing`.
- `POST /api/auth/login` accepts `email` and `password` and returns an `access_token` and the caller's `email` and `role`. A wrong email or password is refused with `not-signed-in`.
- `GET /api/me` returns the caller's `email` and `role` to a valid-token caller.
- `GET /api/sales/callbacks` returns the callback requests, each with `id`, `name`, `email`, `telephone`, `unit_id`, `preferred_time_window` and `created_at`, to a sales caller; a signed-out caller is refused with `not-signed-in`.
- `PATCH /api/sales/units/{id}/availability` accepts `availability` and moves the apartment to that state, returning the apartment. Releasing a coming-soon apartment sets it available and opens its public read and its floor plan; a released apartment may be moved to reserved or sold. An availability that is not a legal next state is refused with `the-rules-dont-allow-that` and an HTTP `409`, unchanged. A signed-out caller is refused with `not-signed-in`.

## Data model

The application stores these entities. Field names below are the contract. All timestamps are UTC.

- `users`: `id`, `email` (unique, lowercase), `password_hash`, `role` (always `sales`), `created_at`. Seeded sales accounts only.
- `typologies`: `id`, `slug` (unique, one of `ground-floor`, `ground-floor-basement` or `penthouse-duplex`), `name`, `bedrooms` (a whole number), `note`. Three rows.
- `units`: `id` (a three-character identifier keeping its leading zero, the route segment), `typology_slug` (the typology), `bedrooms` (a whole number, `2` or `3`), `block` (`B1`, `B2` or `B3`), `floor` (a whole number), `interior_area` (a whole number of square metres), `terrace_area` (a whole number of square metres), `completion` (a quarter and year), `availability` (`coming_soon`, `available`, `reserved` or `sold`), `created_at`. The `availability` state controls the public read: an apartment is released when its state is not `coming_soon`.
- `unit_plans`: `id`, `unit_id`, `index` (a whole number contiguous from 1, the plan order), `object_key` (the object-store key of the plan image), `content_type`. The plan bytes live in the object store under `object_key`, never inside the row.
- `callbacks`: `id`, `name`, `email` (lowercase), `telephone` (null when not given), `unit_id` (the chosen apartment, null when none), `preferred_time_window` (`morning`, `midday`, `afternoon` or `evening`), `consent` (true), `created_at`. One row per submitted request.

The apartment index and a detail page are compiled on read from the `units` rows whose `availability` is not `coming_soon`, so releasing an apartment changes what the public reads on the very next request with no second place to keep in step. A floor plan is public only when its apartment is released.

**Seed data.**

- Sales account, with the password `deku-demo-pw-2026`: `sales@example.com` as `sales`.
- Typologies: `ground-floor` "Ground Floor", `2` bedrooms; `ground-floor-basement` "Ground floor and basement", `3` bedrooms; `penthouse-duplex` "Penthouse duplex", `3` bedrooms.
- Apartments, twenty-five in total, each with one seeded floor plan image generated into the store under `plans/{unit_id}/1/...`. The `ground-floor-basement` apartments are `011` (B1, floor 0, interior 132, terrace 29, `sold`), `012` (B1, floor 0, interior 132, terrace 29, `available`), `031` (B3, floor 0, interior 134, terrace 44, `available`), `032` (B3, floor 0, interior 134, terrace 44, `available`), `033` (B3, floor 0, interior 134, terrace 44, `available`) and `034` (B3, floor 0, interior 134, terrace 45, `available`). The `ground-floor` apartments are `111`, `112`, `113`, `121`, `122`, `123`, `131`, `132`, `133` and `134`, each B1 to B3, floor 0 or 1, interior 75, terrace 29, `available`, and `124` (B2, floor 0, interior 75, terrace 29, `reserved`). The `penthouse-duplex` apartments are `114` (B1, floor 1, interior 89, terrace 151, `reserved`), `211`, `212`, `213` and `224`, each B1 or B2, floor 2, interior 120 or 140, terrace 44 or 60, `available`, and `221`, `222` and `223` (B2, floor 2, interior 140, terrace 60, `coming_soon`). Twenty-two apartments are released and three are coming soon.
- Callback requests: none seeded.

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
- The backing services named in this brief are already running and reachable at their environment variables. This app uses two backing services: `postgres`, reached through `DATABASE_URL` and `DB_URL` (the same value); and a MinIO object store, reached through `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`, into which each apartment floor plan is written. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

## Definition of done

The build is done when: a signed-out visitor reads the released apartments with a live count equal to the number shown, narrows them by typology and bedroom count and sorts them by interior area so a large terrace never lifts an apartment above one with a larger interior, and opens a released apartment to read its floor plan streamed from the stored object, while a coming-soon apartment and its floor plan return `no-such-thing` and `404`; a callback request submitted with a chosen apartment and contact details is recorded and read back unchanged by a signed-in sales user, while a submission missing a required field is refused with `something-missing-or-wrong` and writes nothing; a signed-out request for the callback requests or for an availability change is refused with `not-signed-in` and changes nothing; a sales user releases a coming-soon apartment so a fresh visitor finds it in the index and opens its floor plan, and an illegal availability step is refused with `the-rules-dont-allow-that` and `409`; the first visit asks once about non-essential cookies and the answer survives a reload; every public route answers with its own title and description; and the accessibility and responsiveness floors above hold under a manual keyboard and reduced-motion pass.
