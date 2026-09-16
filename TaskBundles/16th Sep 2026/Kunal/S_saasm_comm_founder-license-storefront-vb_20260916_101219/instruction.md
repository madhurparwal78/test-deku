# Founder License Storefront

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, register an email address for the Lumen Prompt beta, open the access link that arrives by email, and start the download of the current signed build without hitting an error page. Two registrations arriving at the same instant must never share a founder place, and no registration after the thousandth may ever receive one, however the requests are timed. Every founder place must also exist as a real billing account in `killbill`; a place that lives only in the app's own memory or its own tables does not count.

## Overview

Lumen Prompt is a native macOS prompt manager sold directly by Halyard Labs, a one-person company run by Devrim. You are building its website and the machinery behind it: a storefront and content site of sixteen content routes, a beta registration ledger with a capped and ordered founder cohort, an emailed access link, a release registry that feeds a download redirect and a signed update feed, and a small operator console. The product has two halves and both are built: a site that looks right but stubs the ledger has built a brochure, and a correct ledger behind an unstyled form has failed as well.

Visitors read the site and register. Registrants open their emailed link to reach the download and to see their founder place. The operator publishes and revokes releases and revokes access links.

The product deliberately is not: a cloud library of anyone's prompts (no endpoint accepts prompt content, because the product's central promise is that prompt work stays on the user's machine), a direct connection to any AI vendor, a system of end-user accounts, passwords, workspaces, teams or shared libraries (the unit of isolation is one email address), a subscription with recurring billing or dunning (published pricing is one-time licences), or a general permission engine, organisation chart or approval chain.

The genuinely hard part is the founder ledger: exactly one thousand places, never a duplicate, never a gap, never a thousand-and-first, with the price following the place rather than the clock, under simultaneous registrations. The product goal is to turn a stranger reading a marketing page into a registered, founder-eligible beta user running a verified build, with a scarcity ledger that cannot oversell, an access token that cannot be shared into a leak, an update feed that cannot be poisoned, and a prompt library the publisher can never read.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Visitor (no session) | Read every public route, use the command palette and the demonstrations, register on `/download`, ask for a fresh access link, file a data request, follow `/downloads/latest`, read `/appcast.xml` | **Cannot** call any operator endpoint; **cannot** read any registrant's status |
| Registrant (access session from an emailed link) | Everything a visitor can, plus read their own registration state and founder place on `/beta/status` | **Cannot** read another registrant's status; **cannot** call any operator endpoint; **cannot** check out or activate a licence before 1.0 |
| Operator (`operator@example.com`, Devrim) | Sign in on `/operator`, list registrations, publish a release, revoke a release, revoke a registrant's access links | **Cannot** change or reassign a founder place; **cannot** create a founder place past the thousandth; **cannot** read prompt content, because none exists anywhere in this system |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a visitor or registrant session to any operator-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Registration is open to anyone with an email address and uses no password: opening an emailed access link is a registrant's only way in. The operator account is seeded and there is no operator signup.

Seeded people:

- `operator@example.com`, display name `Devrim`, the operator.
- `registrant@example.com`, name `Ada Registrant`, holding founder place 1.
- `registrant2@example.com`, name `Ben Registrant`, whose only access link has expired.
- `registrant3@example.com`, name `Cy Registrant`, whose only access link has already been opened five times.

## Core features

### Founder places (the cohort ledger)

1. The founder cohort has exactly `1000` places, numbered `1` to `1000`. Places `1` to `500` are tier `1` at `2900` (`$29.00`, currency `usd`); places `501` to `1000` are tier `2` at `3900` (`$39.00`). Place 500 is tier 1 and place 501 is tier 2.
2. A registration of an address that holds no place receives the next free place in the same step that stores the registration, while places remain. The price follows the place, never the date.
3. Two registrations arriving at the same instant never receive the same place, and places are handed out with no gaps: after any number of simultaneous registrations the held places are exactly `1` to `N`. This must hold under real concurrency.
4. Once all `1000` places are held the cohort is `closed`: a new registration still succeeds with the same response but receives no place, and a thousand-and-first place never exists.
5. A place is never reassigned, released or sold again, and an address holds at most one place.
6. Every held place has exactly one billing account in `killbill` whose `externalKey` is `lumen-founder-` followed by the place number padded to four digits (place 7 is `lumen-founder-0007`), carrying the registrant's email, currency `USD`, country `US`, and the registrant's name as its name (the email when no name was given). Registering the same address again creates no second account and no invoice.
7. `GET /api/founder/allocation` reports the live cohort: `cap`, `tier_size`, `claimed`, `remaining`, `state` (`open` or `closed`), `current_tier` (`1`, `2`, or `null` when closed), `current_price_minor` (`2900`, `3900`, or `null`) and `currency` (`usd`). The numbers always equal the places actually held.

### Beta registration

1. `/download` carries the registration form. It submits and succeeds with scripting disabled, and client-side checks never block a submission the server would accept.
2. `POST /api/beta/register` takes `email` (required), `name`, `platform_version`, `role`, `primary_use`, `consent` (required, true) and `company_website` (the trap field).
3. The email is trimmed and lowercased before it is stored or compared, so `Ada.Two@Example.com` and `ada.two@example.com` are one registration.
4. Rejected as invalid, with nothing stored and no email sent: a missing or malformed email (at most `254` characters, one `@`, a non-empty local part, a dotted domain; no mail-server lookup), a missing consent, a `name` or `role` over `120` characters, or a `primary_use` over `240` characters. The response carries an `errors` object keyed by field name.
5. A `platform_version` other than empty, `26.1`, `26.2`, `26.3` or `27` is stored as empty rather than rejected.
6. A success returns `{"status": "sent", "message": "Check your inbox for your access link.", "email": "<the normalised address>"}`, with the same keys and the same wording for a first registration and for a repeat of an address already on the list.
7. When the trap field is filled, the response is that same success, and nothing is stored and nothing is sent.
8. Each successful registration emails an access link. An address receives at most `3` access emails in any rolling hour, counting registrations and re-requests together; an address submitted repeatedly past that limit still gets the same success response and nothing more is sent. Registration is limited per address only, never per network origin, because many people register from one shared network.
9. No bot-protection provider exists in this environment: the challenge box stays reserved and empty, every submission proceeds, and each stored registration records `challenge_status` as `not_run`.

### Access links

1. The email goes over SMTP through Mailpit to the registrant only, with no cc and no bcc, with the subject `Your Lumen Prompt beta access link`, and a plain-text part whose first line is the link `<APP_PUBLIC_URL>/beta/access/<token>`. Its second line reads `You are registered for the Lumen Prompt beta.` for a first registration and `You were already on the list, so this is a fresh link.` for any later link. When the registrant holds a founder place the body names it, for example `Your founder place: 7`.
2. A token is at least `32` characters drawn from letters, digits, `-` and `_`, and is stored only as a hash.
3. A link opens at most `5` times and lives `14` days. Issuing a new link to an address marks every older active link of that address `superseded`.
4. Opening a live link counts one open, records a click (at most one click per link in any `30`-minute window), sets an HttpOnly access session cookie that lasts no longer than the link's remaining life (not marked Secure, because this environment serves plain HTTP), and shows `Your access link is confirmed` with a `Download for Mac` control pointing at `/downloads/latest`.
5. A link that cannot be used shows its own page with a working next step, answers with a client-error status that is never not-found, and never shows an email address: revoked or superseded shows `This access link is no longer valid`; opened again after its fifth open shows `This access link has been used up`; past its lifetime shows `This access link has expired`; unknown or malformed shows `We do not recognise this access link` with a link to `/contact`. When more than one applies, the first in this order wins: revoked, used up, expired, superseded. Every one of these pages carries the re-request form.
6. The first time a used-up link is opened after its fifth open, a fresh link is emailed to its owner (within the hourly limit) and the page says a fresh link was sent.
7. `POST /api/beta/resend` takes `email` and always answers `{"status": "sent", "message": "If that address is registered, a fresh access link is on its way."}`. It emails a fresh link only to a registered address and creates nothing for an unknown one.
8. `GET /api/beta/status` with an access session returns `email`, `founder_position`, `founder_tier`, `founder_price_minor`, `currency` and `billing_account` (`ready` once the `killbill` account for the place reads back, `pending` before that); without a session it is denied.

### Release registry, download redirect and update feed

1. One release registry feeds `/changelog`, every `/release-notes/{version}` page, the distribution panel on `/download`, `/downloads/latest` and `/appcast.xml`. None of them hard-codes a version, size or checksum.
2. The current stable release is the `published` release with the highest `build`; from the seed it is `0.2.3`, build `4`.
3. `GET /downloads/latest` redirects to the current stable release's `download_url`, carries `Cache-Control: no-store`, and records one download event, so that release's `download_count` rises by exactly one per redirect.
4. `/appcast.xml` carries one item per `published` release and none for a `revoked` one, highest build first. Each item's enclosure carries the release's `download_url`, `size_bytes` and `ed_signature` exactly as the registry holds them.
5. Publishing a release makes it current stable at once on `/changelog`, `/download`, `/downloads/latest` and `/appcast.xml`. Revoking one removes it from the feed and the redirect at once, and `/changelog` then shows it with a revoked notice and no download control.
6. A publish is rejected as invalid, storing nothing, when its `version` is not three dot-separated numbers or already exists, its `build` is not greater than every existing build, or its `sha256` is not 64 lowercase hexadecimal characters.
7. `/release-notes/{version}` for an unknown version shows the not-found page with a link to `/changelog`.

### Operator console

1. The operator signs in with email and password at `/operator`; `POST /api/auth/login` returns `{"access_token": "..."}` and operator endpoints take `Authorization: Bearer <token>`. A wrong password is denied and returns no token.
2. `GET /api/admin/registrations` lists registrations newest first and, given `?email=<address>`, only that normalised address; `POST /api/admin/releases` publishes; `POST /api/admin/releases/{version}/revoke` revokes; `POST /api/admin/access-links/revoke` with `email` revokes that address's active links and returns `{"revoked": n}`.
3. Every operator endpoint is denied to a visitor and to a registrant session, and a denied call changes nothing.
4. The console lists registrations with their founder places and releases with their status, and offers a revoke control on each published release.

### Checkout and licences before 1.0

1. `POST /api/checkout/founder` is rejected with `{"error": "checkout_not_open"}` and creates no billing account and no invoice. `/checkout/founder` and `/checkout/return` show `Founder checkout opens at 1.0` with a link to `/download`.
2. `POST /api/licence/activate` is rejected with `{"error": "licensing_not_open"}`, and `/licence/activate` shows `Licence activation opens at 1.0`.

### Data requests

1. `/legal/data-request` takes an email and a kind (`access`, `export`, `correction` or `deletion`); `POST /api/legal/data-requests` stores it with status `open` and answers `{"status": "received", "message": "We will reply to that address within 30 days."}`.
2. A missing email or any other kind is rejected as invalid and stores nothing.

### Site-wide features

1. The command palette opens on Cmd K (Ctrl K off macOS) from every route, searches five demonstration Blueprints and seventeen destinations, and is driven entirely by keyboard.
2. A privacy page and a terms page are linked from the footer of every page.
3. Every internal link on every public route resolves: none leads to the not-found page or to an error.
4. An unknown address shows the product's own not-found page, answering not found, with links to `/`, `/download`, `/changelog` and `/contact` and a hint for the palette shortcut.

### Auth

The operator signs in with email and password and receives a bearer token; the password is stored hashed and a wrong one is refused. A request carrying an invalid or expired operator token is denied. Registrants authenticate only by opening an access link, and their session is an HttpOnly cookie. There is no password reset, no operator signup and no external identity provider.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Home, fourteen sections in a fixed order | none |
| `/download` | Join the beta: registration form and the official distribution panel | none |
| `/use-cases` | Index of five acquisition pages with the radial diagram | none |
| `/use-cases/reusable-ai-prompt-templates` | Acquisition page for reusable prompt templates | none |
| `/use-cases/prompt-version-history` | Acquisition page for prompt version history | none |
| `/use-cases/prompt-manager-for-mac` | Acquisition page for a prompt manager for Mac | none |
| `/use-cases/local-first-prompt-library` | Acquisition page for a local-first prompt library | none |
| `/use-cases/hotkey-prompt-injection-macos` | Acquisition page for the hotkey prompt launcher | none |
| `/changelog` | Release index read from the release registry | none |
| `/release-notes/{version}` | One release in full; the current one is `/release-notes/0.2.3` | none |
| `/roadmap` | Now, Next and Later, with no dates | none |
| `/blog` | Index of two articles | none |
| `/blog/prompts-are-work-product` | Article | none |
| `/blog/stop-rewriting-your-best-prompt` | Article | none |
| `/press` | Press kit | none |
| `/contact` | The single support address | none |
| `/privacy` | Privacy policy | none |
| `/terms` | Terms | none |
| `/beta/access/{token}` | Redeems an emailed access link | the link |
| `/beta/status` | Registration state and founder place | access session |
| `/legal/data-request` | Access, export, correction and deletion intake | none |
| `/checkout/founder` | Founder checkout, not open before 1.0 | none |
| `/checkout/return` | Checkout return, not open before 1.0 | none |
| `/licence/activate` | Licence activation, not open before 1.0 | none |
| `/operator` | Operator sign-in and console | operator |
| `/downloads/latest` | Redirect to the current stable binary | none |
| `/appcast.xml` | The update feed | none |
| `/sitemap.xml` | Sitemap of the sixteen content routes | none |
| `/robots.txt` | Crawl rules | none |

**Entry and redirects.** `/beta/status` without an access session shows `Open the link in your email to see your status` with the re-request form. `/operator` without an operator session shows the sign-in form; a successful sign-in shows the console; `Sign out` returns to `/`; a request with an invalid or expired operator token is denied and the console returns to the sign-in form; a registrant's access session is not an operator session and never opens the console. The four home anchors (`#features`, `#workflow`, `#pricing`, `#help`) navigate home and then scroll when followed from another route. Once `/beta/access/{token}` has set the session, the address bar reads `/beta/access` with the token dropped. An unknown address shows the not-found page.

**Journeys.**

1. Registration: open `/download`, type a new address, tick the consent box, press `Join the beta`. The form is replaced in place by a `Check your inbox` panel that names the address, suggests the spam folder, and shows `Resend link` disabled with a visible count down from 60 seconds.
2. Access: open the emailed link. `Your access link is confirmed` shows with `Download for Mac` focused, the address bar reads `/beta/access`, and `/beta/status` then shows the founder place.
3. Dead link: open `/beta/access/seed-expired-7c1e2a9b4d36`. `This access link has expired` shows with the re-request form; submitting `registrant2@example.com` shows `If that address is registered, a fresh access link is on its way.`
4. Palette: press Cmd K on `/`. The Blueprints group lists first; type `roadmap` and press Enter; `/roadmap` opens.
5. Releases: open `/changelog`. The current stable block shows `0.2.3`; follow `Read the notes` to `/release-notes/0.2.3`, which shows `Known issues`.
6. Operator: open `/operator` and sign in as `operator@example.com`. The registrations list shows `registrant@example.com` at founder place 1; the releases list shows `0.2.0` as revoked.
7. Checkout: open `/checkout/founder`. `Founder checkout opens at 1.0` shows with a link to `/download`.

**States.** Every page has a loading state. The console's registrations list has a search box; a search that matches nothing shows `No registrations match`, and `GET /api/admin/registrations?email=<address>` answers an empty array for an address that is not registered. An error never crashes a page or shows a stack trace: it renders the branded error page with a request identifier, a retry control and a direct link to `/downloads/latest`.

## UI/UX notes

The design is this product's own specification, not a house style: a visitor should understand at a glance that the product is a precise, quiet instrument made of glass. The register is consumer and editorial with working instruments: the instruments carry the argument and the copy captions them, and the operator console stays calm and dense. Depth over flatness; stillness during a decision over spectacle.

**Material.** The whole site is a stack of translucent frosted panes floating over a pale, cool ground with a faint square grid printed on it. A floating pane always carries three things together: a translucent soft vertical gradient over a base tint, a thin near-white edge, and a large soft shadow with a bright lit line along its top lip. Dropping the lit line produces a flat card with a shadow, which is wrong. Every pane stays readable with the backdrop blur switched off, because its own background is opaque enough to stand alone.

**Palette by role.** The page ground is a near-white cool neutral; panes are translucent near-white; primary text is a near-black cool neutral, supporting prose a deep cool neutral, and metadata a mid cool neutral. One accent does all the signalling for actions, selection and focus: a light, soft blue leaning towards indigo, with a darker mid, soft blue for link text and accent ink; it appears on every primary action and on nothing decorative. A mid, vivid teal marks attached material only (context files and the diagram nodes that stand for them) and never appears on a control. Success, warning and danger each have a base colour for borders and glows (a deep, soft teal; a mid, vivid orange; a mid, vivid red) and a darker text colour (deep, soft teal; deep, soft orange; deep, soft red), and text always uses the darker one. There is exactly one dark region, the injection history ledger, with near-white text and a pale mint accent. The window mockups draw a light, vivid red, a light, vivid orange and a mid, vivid green dot. The exact shades are yours, so long as these roles and the contrast bar hold.

**Type.** Display and body text use the operating system's own interface typeface; `IBM Plex Mono` is the only downloaded family and marks only what a machine reads back literally: key names, double-brace variables, version strings, checksums, routes and ledger timestamps. Body prose is never monospace. Sizes are listed in the front-end specification.

**Motion.** The motion character is eased: everything that moves under the pointer uses one house curve that starts slowly, covers most of its travel early and coasts into place, and everything that arrives at rest uses a slightly softer sibling of it. Panels arrive by rising a short distance while fading in and growing a hair to full size. Colour, border, background and shadow transition together. Under a reduced-motion preference every loop, the page-transition curtain, smooth scrolling and every sweep stop, and arrivals appear with a short fade.

**Density and layout.** Comfortable density; a floating top navigation capsule, never a full-width bar; card grids for pricing, use cases and articles; instruments sit beside their copy on wide screens and above it on narrow ones.

**Components.** Operator confirmations and the registration error summary render as inline banners in the flow of the page rather than as floating toasts. Buttons rise slightly under the pointer and settle when pressed, and their shadow shrinks with them. The focus ring shows on keyboard focus only, never on a pointer click. Escape closes every dialog and the small-width menu. A selected row carries a glow and a persistent left marker.

**Mode.** Light, designed fully. Only the release notes pages also follow a dark system appearance.

**Accessibility.** The site meets WCAG AA. Body text keeps a contrast of at least 4.5:1 against the background actually behind it, and primary text on the page ground at least 7:1, measured on the composited result. Every foreground inside the dark ledger meets 4.5:1 against that dark ground. Touch targets are comfortably sized, keyboard navigation reaches every control with a visible focus ring, every icon-only control has a label, and meaning is never carried by colour alone.

**Responsive.** The layout holds at phone, tablet and desktop widths and at every width between. At a narrow viewport nothing overflows sideways and every navigation target stays reachable; below the wide breakpoint the six navigation links collapse into a menu button.

**What it must not look like.** Opaque flat cards with no depth; a page dominated by a single hue with no second signal; marketing decoration standing where the working instruments belong.

## Technical requirements

**Stack.** TypeScript on Node.js 20. The frontend is SolidStart with server-rendered pages and hydrated islands for the interactive parts (palette, hotkey demonstration, context tray, version scrubber, help filters, forms). The backend is Express, which serves the SolidStart production build and the JSON API under `/api` from the same process on the same origin. HTML is produced on the server, so the browser receives complete, readable pages on first paint and every public route renders its content with scripting disabled. Data lives in PostgreSQL (`postgres`), email goes through Mailpit (`mailpit`), and billing accounts live in Kill Bill (`killbill`).

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor: the only backing services available in this environment are PostgreSQL, Mailpit and Kill Bill, and reaching for anything else is a contract violation.

**Environment.** Read everything from the environment, never hardcode a host or port: `DATABASE_URL`; `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS` (Mailpit takes no authentication, so user and password are empty); `PAYMENTS_API_URL`, `PAYMENTS_API_KEY`, `PAYMENTS_API_SECRET`, `PAYMENTS_ADMIN_USER`, `PAYMENTS_ADMIN_PASSWORD`; `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`. The email link and the feed's absolute URLs are built from `APP_PUBLIC_URL`.

**Kill Bill.** Every `/1.0/kb/*` call carries HTTP Basic credentials from `PAYMENTS_ADMIN_USER` and `PAYMENTS_ADMIN_PASSWORD`, the `X-Killbill-ApiKey` header from `PAYMENTS_API_KEY` and the `X-Killbill-ApiSecret` header from `PAYMENTS_API_SECRET`; writes also carry `X-Killbill-CreatedBy` naming the storefront. The tenant `orbit-labs` already exists. A founder account is looked up with `GET /1.0/kb/accounts?externalKey=<key>` (found or not found) and created with `POST /1.0/kb/accounts` and the body fields `name`, `externalKey`, `email`, `currency`, `country`; a conflict on an existing `externalKey` means the account already exists and is not an error. `GET /1.0/healthcheck` is the unauthenticated liveness check. Kill Bill is a billing ledger, not a card processor: this build creates no invoice, subscription, payment method or refund there.

**Health and logging.** `GET /api/health` answers `200` with `{"status": "ok"}` once PostgreSQL is reachable. The server writes one structured log line per request to stdout with the method, the path, the status and the duration, so every page view of a content route is recorded on the server rather than by an analytics provider; an access token in a path is written as `[token]`, never in full.

**Security headers.** Every response carries these security headers: `Strict-Transport-Security: max-age=31536000; includeSubDomains`, `X-Content-Type-Options: nosniff` and `Referrer-Policy: strict-origin-when-cross-origin`. The referrer policy is what stops an access link's address leaking to the binary host. The content security policy allows only the site's own origin: this environment has no reactive backend host, no bot-protection challenge host and no aggregate analytics host.

**Crawling and indexing.** `/sitemap.xml` lists the sixteen content routes as absolute addresses under `APP_PUBLIC_URL` (`/`, `/download`, `/use-cases`, the five use-case pages, `/changelog`, the notes of the current stable release, which is `/release-notes/0.2.3` from the seed, `/roadmap`, `/blog`, `/press`, `/contact`, `/privacy`, `/terms`) and nothing else, so publishing a release moves that one entry with it. `/robots.txt` excludes the download redirect, the function namespace, the access namespace and the checkout namespace with the lines `Disallow: /downloads/latest`, `Disallow: /api/`, `Disallow: /beta/access/` and `Disallow: /checkout/`, and points at the sitemap with `Sitemap: <APP_PUBLIC_URL>/sitemap.xml`. The access route additionally carries `<meta name="robots" content="noindex">` in its markup, because a token in a crawled address is a leaked credential. Every content route carries a canonical link to itself; the five use-case pages do not canonicalise to their index.

**Caching.** `/downloads/latest` is never cached (`Cache-Control: no-store`). Release notes are immutable once published and carry `Cache-Control: public, max-age=3600, stale-while-revalidate=86400`. `/changelog` carries `Cache-Control: no-store` and refreshes the moment a release is published or revoked, so a new version appears immediately.

**Update feed format.** `/appcast.xml` is an RSS 2.0 document declaring `xmlns:sparkle="http://www.andymatuschak.org/xml-namespaces/sparkle"`. Each `<item>` carries `<title>Lumen Prompt <version></title>`, `<sparkle:version>` (the build), `<sparkle:shortVersionString>` (the version), `<sparkle:minimumSystemVersion>` (the release's `min_os`), `<sparkle:releaseNotesLink>` (`<APP_PUBLIC_URL>/release-notes/<version>`) and one `<enclosure>` with `url`, `length`, `type="application/octet-stream"` and `sparkle:edSignature`. The signature is made over the exact bytes of the binary on the signing host with a key that never reaches this server; the registry stores the published signature and the feed repeats it unchanged.

**System boundary.** Two surfaces share one lifecycle. Surface A is this web platform. Surface B is the Mac application, whose data lives on the user's own machine and, when enabled, in that user's own private cloud container, which the publisher cannot read. They meet at exactly three points: M1, web to user to application (an access token, a redirect, a download event); M2, application to web (a version check through the feed, and after 1.0 a licence-scoped feed request); M3, application to and from web (a licence key, a device fingerprint and an entitlement window, after 1.0). No Blueprint, context file, rendered prompt or history row ever crosses that line, so no route here accepts one. Five commercial facts shape the rules above: there is no subscription and the copy promises there never will be; the founder cohort is a hard-capped, non-replenishable inventory of one thousand; money has not started moving yet, so registering holds a place that must stay unambiguously redeemable at 1.0; the product ships a signed binary that asks for accessibility permission, so the update channel must not be poisonable; and one person operates all of it and reads every message, so nothing needs a second person on a bad day. The publisher tracks success measures (visit to registration, registration to access-link open, access-link open to download start, download to first update check, founder allocation integrity, accepted spam registrations, and prompt content received by the publisher, which must stay at zero bytes); those measures are read from the stored events and are not screens in this build.

## Data model

Eight tables. All timestamps are UTC. Money is stored in integer minor units with lowercase currency `usd`.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

**`operators`**: `id`, `email` (unique), `display_name`, `password_hash`, `created_at`.

**`registrations`**: `id`, `email` (unique, stored trimmed and lowercased), `name` (up to 120 characters), `platform_version` (empty, `26.1`, `26.2`, `26.3` or `27`), `role` (up to 120), `primary_use` (up to 240), `consent_at`, `challenge_status` (`not_run`, `passed` or `failed`), `created_at`, `updated_at`.

**`founder_slots`**: `position` (1 to 1000, unique), `registration_id` (unique), `tier` (1 or 2), `price_minor` (2900 or 3900), `currency` (`usd`), `killbill_external_key` (unique, `lumen-founder-NNNN`), `claimed_at`. At most one row exists per position and per registration, no position outside 1 to 1000 can be stored, and two concurrent registrations can never produce two rows with the same position or leave a gap below the highest position. `tier` and `price_minor` always agree with `position`.

**`access_links`**: `id`, `registration_id`, `token_hash` (unique; the raw token is never stored), `status` (`active`, `revoked` or `superseded`), `opens` (0 to 5), `max_opens` (5), `created_at`, `expires_at` (14 days after `created_at`). `opens` never exceeds `max_opens`, even when the same link is opened several times at once.

**`access_clicks`**: `id`, `access_link_id`, `clicked_at`. At most one row per link in any 30-minute window.

**`releases`**: `version` (unique, three dot-separated numbers), `build` (unique integer, each new one greater than every existing one), `published_at`, `min_os`, `size_bytes`, `sha256` (64 lowercase hexadecimal characters), `ed_signature`, `download_url`, `summary`, `notes` (markdown), `status` (`published` or `revoked`).

**`download_events`**: `id`, `release_version`, `access_link_id` (empty for a visitor without a session), `created_at`.

**`data_requests`**: `id`, `email`, `kind` (`access`, `export`, `correction` or `deletion`), `status` (`open`), `created_at`.

**Derived, never stored:** a release's `download_count` (its download events), the cohort's `claimed`, `remaining`, `state`, `current_tier` and `current_price_minor` (from `founder_slots`), whether a link has expired (from `expires_at`), and the current stable release (the highest `build` whose `status` is `published`).

**Seed data.**

- `operators`: `operator@example.com`, `Devrim`.
- `registrations`: `registrant@example.com` (`Ada Registrant`), `registrant2@example.com` (`Ben Registrant`), `registrant3@example.com` (`Cy Registrant`), each with consent and `challenge_status` `not_run`.
- `founder_slots`: place 1 held by `registrant@example.com`, tier 1, `2900`, key `lumen-founder-0001`. The app opens the matching `killbill` account at first start if it is missing.
- `access_links` (raw token and state): `seed-live-4b7d9e2a61c3f085` for `registrant@example.com`, `active`, 0 of 5 opens, expiring 14 days after first start; `seed-revoked-9a4d7e1f5b20` for `registrant@example.com`, `revoked`; `seed-expired-7c1e2a9b4d36` for `registrant2@example.com`, `active`, created 15 days before first start, so already expired; `seed-usedup-3f8b6d0c2e71` for `registrant3@example.com`, `active`, 5 of 5 opens, expiring 14 days after first start.
- `releases`:
  - `0.2.3`, build `4`, published `2026-08-28`, `min_os` `26.1`, `24117248` bytes, sha256 `08035fead80e0cfe09a8ad0bc7d7486a353c38890810acd9ed2cb8372df9bb5a`, signature `72hn8fG8m3U31YYqCB378cZKcpDwXR+iNhBHIvstb8USInEGvUdXHuRZdNMAK0OyBz2RmbRD7zMyOz4RQa2cRg==`, `https://downloads.example.com/lumen-prompt/Lumen-Prompt-0.2.3.dmg`, `published`, summary `Faster search, steadier injection and a clearer version history.`
  - `0.2.2`, build `3`, published `2026-08-07`, `min_os` `26.1`, `23855104` bytes, sha256 `c2e5920ade47626fae119eb565b325979707e168705380a4791055818855780c`, signature `ltDS2MUPQgeuA+Z1N+PII/9zmDPiHSmTPikafE9dlpnhNemyHFCUH0h5024DhXw8CvuiCgTWI4YJ8vAu5cnJVA==`, `https://downloads.example.com/lumen-prompt/Lumen-Prompt-0.2.2.dmg`, `published`, summary `Context files can now be switched on and off before sending.`
  - `0.2.1`, build `2`, published `2026-07-17`, `min_os` `26.0`, `23592960` bytes, sha256 `6557b3ed2d20b07757b7c5080ef611a1b0c7b4c855393417a5060d5c20f03cda`, signature `a6Ua7KYh1AvSwE2D4ZbgXbKkNh7S6YtbynIAOvMyv+IhhZEjWvtY+Pywy6bnrtMk+GjrOTJe8bOsyD8I+fhuxw==`, `https://downloads.example.com/lumen-prompt/Lumen-Prompt-0.2.1.dmg`, `published`, summary `Import from four other tools, with a preview before anything is written.`
  - `0.2.0`, build `1`, published `2026-06-26`, `min_os` `26.0`, `23330816` bytes, sha256 `b10364b9f7d0b4a8ee44327567675ec333eafcd6d627a5935a9789c4fdb0e020`, signature `VVMY3peMs3lA7du1DIi98M1Wucbu3+DZhNEH87GT7jr85OT3PFh+ceOX3sYMjpGRvPhtwYSrg6q3T5I8AQXNuA==`, `https://downloads.example.com/lumen-prompt/Lumen-Prompt-0.2.0.dmg`, `revoked`, summary `The first open beta build.`

The release notes of `0.2.3` carry the sections listed under Release notes in the front-end specification; their `Also in this release` section names the import sources Espresso, Alder, Rayline and Obelisk, and their known issues are these: the paste needs the accessibility permission; some applications and secure fields refuse a synthetic paste, and the prompt stays on the clipboard; browser tabs cannot receive attached files; prompts imported from `Obelisk` arrive with form and choice placeholders as plain text; and the report-a-problem command can open an empty window when no mail handler is set, in which case it offers to copy the address and the body.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

This section carries the full visual and content specification for every surface. Capability requirements here are normative; where the source describes how the captured reference happened to implement something, that implementation is informational and yours to replace with anything that satisfies the capability.

### Identity and names

The product is Lumen Prompt (Lumen in running copy), published by Halyard Labs, whose founder Devrim signs the beta note. The four destination applications named in copy are Chatwell, Cadence, Vertan and Caret. The three adjacent tools in the comparison table are Notary Docs, Rayline Snippets and Provider Projects. The four import sources named in the `0.2.3` release notes are Espresso, Alder, Rayline and Obelisk. The affiliation disclaimer names the three AI vendors Northgate, Bellweather and Halcyon. The footer copyright year is 2026, the current stable release is `0.2.3` (build `4`), and the minimum supported system is macOS 26.1. The single inbound address for support, press and privacy is `hello@example.com`. Release binaries and the press kit are served from `https://downloads.example.com`. The update-feed signing key, the licence signing key (a different key), the bot-protection keys, the mail credential and the commerce webhook secret are never shipped in markup or anything the browser downloads; none is needed in this environment.

### The product the site sells

Lumen Prompt keeps the wording people reuse at work. Its loop is stated on the home route as four numbered beats, with this wording:

| Beat | Name | Description |
|---|---|---|
| 01 | Summon hotkey | Press the hotkey over your current Mac workspace. The prompt panel appears where you are already working. |
| 02 | Search library | Type a few letters to filter your Blueprint Library. Keyboard-first navigation keeps your hands on the work. |
| 03 | Fill variables | Variables become visible fields. Remembered values tied to context make repeated work faster. |
| 04 | Inject history | Copy the rendered prompt or inject it with context files. The application records the action in Injection History. |

Four capitalised nouns carry the product on every route: a **Blueprint** is a reusable prompt with variables, tags, context and version history attached; a **Context** bundles files, saved variables and project memory, and a Blueprint can be docked to a context; the **Time Machine** is per-Blueprint version history with a scrubber, star ratings, and compare and restore controls; **Injection History** records quick copies and full injections by date, size, target app and whether files were included.

### Navigation model

The information architecture is the sixteen content routes, the added access, status, legal, checkout and licence routes, and four addresses that are not pages. Six primary destinations: Product (home, features anchor), Workflow (home, workflow anchor), Use cases (the use-cases index), Pricing (home, pricing anchor), Blog (the blog index) and FAQ (home, help anchor). The primary action, labelled `Join beta`, is present in the navigation on every route without exception, again in the footer, and again at the end of every content route; it leads to `/download` and is the site's only conversion path. Anchor targets leave enough scroll margin that a linked section never lands underneath the navigation capsule, and on the home route active-section highlighting observes which section occupies the middle band of the viewport, so exactly one navigation item is active at a time.

### Colour, status and the inverted region

Two accent hues carry the brand: the light, soft blue for every action and selection, and the mid, vivid teal used only for attached material. Almost every surface and foreground carries some translucency, and flattening any of them into an opaque approximation destroys the depth. The page ground, resting panes, panes under the pointer, the brighter command surfaces and the recessed areas inside them, the default hairline, the lit edge on floating panes, the edge on command surfaces and the edge on the one dark panel each have their own role colour. The pill used for eyebrows has a faint accent fill, a slightly stronger accent edge and darker accent text (the pill-fg role, a mid, soft blue). The color-white and color-black roles are pure white and pure black, used only for highlights and the dark ledger. Selected text uses a translucent accent highlight.

The injection history panel is the only region that inverts to a dark ground, so a history of sent work reads as a record rather than as another card. Inside it the foreground, secondary and tertiary text are near-white at decreasing strength, the accent is a pale mint rather than the blue used everywhere else, and its border is a faint near-white line. Contrast inside this region, including the focus ring, is checked against the dark ground; if the blue ring fails there, that region takes a lighter ring.

The window mockups draw a title bar with the three platform-conventional traffic dots in red, amber and green, and those dots are decorative and hidden from assistive technology.

### Contrast obligations

Contrast is computed against the composited result at the worst scroll position, not against the colour token. Required: primary foreground on the page ground at least 7:1; secondary foreground on a resting pane at least 4.5:1; tertiary foreground where it carries meaning at least 4.5:1; tertiary foreground used only for placeholder text at least 3:1 and never the only carrier of meaning; pill text on pill fill at least 4.5:1; every foreground inside the inverted region at least 4.5:1. The tertiary metadata colour is the one most likely to fail, so check it everywhere it is used, assuming the backdrop blur is absent.

### Typography

Display and body text use the platform interface stack, falling back through a grotesque to a generic sans; the site sells a native application and renders in the native typeface. The only downloaded family is `IBM Plex Mono`, in weights `400`, `500` and `600`, each subset and each set to swap so text is never invisible while a face loads.

| Size | Weight | Line height | Used for |
|---|---|---|---|
| `16px` | `400` | `24px` | body prose, by far the most used |
| `12px` | `400` | `16px` | metadata, chips, footnotes |
| `16px` | `600` | `24px` | emphasised body and card titles |
| `10px` | `400` | `15px` | the smallest labels, always tracked |
| `11px` | `700` | `16.5px` | uppercase eyebrow labels |
| `14px` | `400` | `24px` | secondary prose |
| `24px` | `700` | `32px` | section headings at small widths |
| `18px` | `700` | `28px` | card headings |
| `18px` | `400` | `32px` | lead paragraphs |

Tracking runs inversely to size: large display type is set tight or normal, and every uppercase label smaller than `13px` is tracked open. Display sizes are derived fluidly from the viewport between a minimum and a maximum, in six steps, rather than from a fixed table; the top step is the hero headline, which sets on four lines at the widest width and stays readable without hyphenation at the narrowest.

### Space, radius, elevation and blur

Everything sits on one base unit and its multiples. Sections are separated by a generous block rhythm on wide screens and a tighter one on narrow screens, and consecutive sections do not collapse their spacing together. The content measure is wide on desktop and narrows its side gutter on phones; legal pages and articles use the two widest prose measures. Radii belong to classes of object: inputs, list rows and small containers share one soft radius; key caps, inline code and small chips a smaller one; buttons and controls their own; panes and cards a larger one; the fully rounded shape is reserved for things that are genuinely capsule-shaped (the navigation capsule, pills, capsule search fields and scrubber tracks); mockup chrome, diff rows, large linked cards, diagram nodes, the diagram stage and launcher result rows each keep their own. An interactive element inside a pane uses the control radius and the pane uses the pane radius; a third arbitrary value is a defect.

Two shadows carry the system and both pair a wide soft drop with a lit inset top edge: the card shadow on resting panes, and a deeper head-up shadow on floating instruments (the launcher panel, the palette and the small-width menu). The primary action button, the floating navigation bar and the selected launcher row each have a named shadow of their own, and the selected row's shadow is a blue glow rather than a grey drop, so the active row reads as lit from within.

Backdrop blur differs by surface and is not interchangeable: resting panes, the launcher and palette panels, buttons and chips, the palette scrim, the palette key cap, the navigation bar (the heaviest), the diagram nodes, the window mockup, the diagram core and the inverted history panel each have their own blur and saturation. Every blurred surface is paired with a background opaque enough to stand alone, because the property is dropped silently under several accessibility settings and graphics blocklists.

### The signature gradients and the grid

Four gradients carry the brand. The page ground is a soft diagonal white sheen over two large radial washes, a warm white from the top left and a pale blue from the top right. The command surfaces use a vertical white sheen over a teal radial at the upper right and a blue radial at the lower left, which makes the launcher panel and the palette read as one material. The page-transition curtain is a diagonal white band over a vertical ramp from near-white at the top through the page ground to a pale cool neutral at the bottom. The printed grid is two one-line gradients, horizontal and vertical, nearly invisible, tiling the page ground so large pale areas never read as empty.

### Focus and selection

The focus ring is a thin accent ring with a small offset in the colour of the surface actually behind the control (which differs between the page ground and the inside of a pane), over a wider soft ring. It shows on keyboard focus only, never for pointer users. A selected row carries the glow and a persistent left marker, so selection survives a screenshot and a reader who cannot separate the hues.

### Iconography

Sixty-four inline vector icons are drawn as strokes rather than filled shapes, inherit the current text colour and never carry their own palette; no icon font or sprite sheet is loaded. Inside a control an icon is small, square and never stretched; in a section heading or a diagram node it is a little larger; stroke width is the same at every size. Decorative icons are hidden from assistive technology and the accessible name lives on the control that contains them; an icon carrying meaning on its own always has visible text beside it, never only a hover title.

| Family | Members | Where |
|---|---|---|
| Actions | search, copy, inject arrow, open, edit, download, external link, check, close | controls throughout |
| Domain nouns | a document for a Blueprint, layered squares for a Context, a paper plane for an injection, a clock for history, a tag, a star | the four product nouns, used consistently |
| Verification | a shield with a check, a fingerprint, radio waves, a download tray | the distribution panel on `/download` |
| Navigation | a chevron down for an accordion, an arrow right for a forward link, a hamburger for the small-width menu, keyboard arrows | chrome |
| Status | a filled circle for present, a horizontal rule for absent, an exclamation in a circle for a warning | the comparison table and form states |

The wordmark is a circular mark to the left of the product name: a rounded glyph inside a filled disc in the accent blue. It is the only filled icon and the only one with its own colour.

### Global chrome

**The navigation bar is a floating capsule, not a full-width bar.** It is centred horizontally, does not touch the top of the viewport, does not span the measure, carries the heaviest blur on the site with its own navigation shadow, and sits above page content and below the palette and the small-width menu. Left to right it holds the wordmark with the product name, a hairline divider, the six text links, a key-cap button showing the palette shortcut, and the `Join beta` action as a filled blue pill. It never hides on scroll. Below the wide breakpoint the six links and the key cap collapse into a single menu button.

**The skip link** reads `Skip to content`, is the first focusable element, sits just above the viewport until it receives keyboard focus, uses the same pane material as the rest of the chrome, and moves focus into the main landmark rather than merely scrolling to it.

**The small-width menu** is a dialog, not a dropdown. It fades in while rising a short distance and growing slightly, and fades out while rising a slightly shorter distance; the asymmetry is deliberate. Its scrim is a plain opacity fade and the panel uses the head-up shadow. Focus is trapped inside, Escape releases it, and focus returns to the menu button on close. Page scroll is locked while it is open without the page jumping, and the background is made inert so assistive technology and the Tab key both stop at the panel edge.

**The footer** has four columns at the widest width, collapsing to two and then one: a brand block with the product name, a one-sentence description and three status chips, then three link columns.

| Column | Items |
|---|---|
| Product | Features, Workflow, Beta, Use cases, Changelog, Roadmap |
| Resources | FAQ, Blog, Templates, Version history, Join beta |
| Company | Contact, Privacy, Terms, Press |

`Templates` and `Version history` point at the matching acquisition pages and keep those labels. The base line carries `(c) 2026 Halyard Labs` and the legal disclaimer `Lumen Prompt is not affiliated with Northgate, Bellweather or Halcyon.`, set at full contrast and at no less than `12px`, never as faint fine print.

**The page-transition curtain** is a full-viewport sheet carrying the curtain gradient that sweeps across on each route change, hides the swap, runs once per navigation, never blocks input longer than its own run, never traps focus, and is skipped entirely under a reduced-motion preference; when it completes, the incoming route's main landmark receives focus.

### Motion language

**Curves.** Two named curves carry the system: frost, the house curve, on everything that moves under the pointer, and frost settle, the most used, on everything that arrives at rest. Both start slowly, reach most of their travel early and coast into rest; frost settle leaves marginally faster and arrives marginally softer. Three further curves appear: the framework default on colour transitions, a gentle one for exits, and one overshoot-free arrival.

**Durations**, named by feel: tap (the quickest, press feedback), fast (hover, colour, border, shadow and the focus ring), gentle (small transforms and disclosure), soft (pane and card entrances) and the framework default for generated colour utilities. The most common compound moves transform, border colour, background and shadow together on the fast duration and the house curve for every button and hoverable pane; a disclosed element stops receiving the pointer the instant it finishes leaving.

**Named sequences.**

| Sequence | Character | Target |
|---|---|---|
| workspace drift | a slow endless loop | the workspace behind the launcher panel, shifting upward and back |
| sweep | an endless loop, visible only for part of each cycle | a tilted specular band crossing a pane, peaking at just over half opacity |
| caret blink | an endless blink | the launcher search caret |
| history caret blink | an endless blink, slightly slower and slightly offset | the caret in the inverted history panel, so the two carets never blink in lockstep |
| key settle | once, holding both ends | the three key caps in the headline, dropping in from above while growing to full size |
| material settle | once, holding both ends | the launcher panel arriving from below while growing a hair to full size |
| summon float | an endless gentle rock and rise | the launcher panel |
| glint | a loop | a diagram node brightening while rising and turning slightly |
| trust pulse | a loop | a halo breathing between faint and strong while scaling slightly |
| selected row, diff highlight, preview glow | attention | the rows, diffs and preview cards they name |
| mobile panel in and out, mobile overlay out, toast out | arrival and departure | the small-width menu and toasts |
| accordion down and up | disclosure | the help panel |
| scrub thumb | demonstration | the Time Machine scrubber |
| hero rescue | safety net | the hero block |

Section entrances stagger their children briefly, capped at six children, beyond which the stagger stops. Only one sweep runs in a viewport at a time. Every loop stops when its element leaves the viewport and stops entirely under a reduced-motion preference.

**The safety net.** The hero is animated in by script, and one sequence exists only to guarantee it becomes fully visible when the scripted layer is slow, blocked or broken. Fetching `/` and discarding its scripts still yields the headline, the sub-headline, both hero actions and the three status chips, all visible.

**The pressed state.** Buttons rise slightly under the pointer and return when pressed, and their shadow shrinks with them; animating the position without the shadow produces a button that moves but does not feel pressed.

### Scroll and page transitions

**Smooth scrolling** is optional. If you add it, it is disabled under a reduced-motion preference, halted while any dialog is open and resumed on close, never breaks anchor navigation, the Home and End keys or Space and Page Down paging, never intercepts scrolling inside the two nested scrollable regions (the history ledger and the comparison table at intermediate widths), and never fights the browser's own scroll restoration on back navigation. If any of those cannot be met, ship native scrolling; nothing else depends on the smoothing.

**Scroll-linked drawing.** As the workflow section passes through the viewport, the connector threading the four steps draws progressively from nothing to its full length, and each step marker lights as the drawing tip passes it; scrolling back undraws it exactly. It is independent of frame rate, never reads layout during a scroll event, and renders fully drawn and fully lit when scripting is absent or motion is reduced.

**The depth stack.** The hero instrument is three layers under a shared perspective: the workspace behind is rotated a few degrees, pushed back and desaturated to just under three quarters; the search field in front is rotated slightly less and pushed back less, with a trace of blur; the window mockup on the product routes carries a gentle rotation on all three axes. Tilt plus desaturation plus the trace of blur is what makes the panel read as floating in front of a real screen.

**Layering**, bottom to top: the ground gradient and printed grid; page content; sticky elements inside sections; the navigation capsule; the page-transition curtain; the palette and the small-width menu. The three major home sections are isolated so a raised element inside one never escapes above the chrome.

### Command palette

The palette is the site's own demonstration of the product: a keyboard-summoned panel that filters a library and acts on a selection.

**Contents.** Group one, Blueprints, holds five demonstration entries, each with an icon, a title, an uppercase category and a truncated body containing double-brace variables. They are the same five that appear in the launcher instrument and the library mockup, identical in all three:

| Title | Category | Body |
|---|---|---|
| Client brief summary | WRITING | `Summarise {{document}} for {{client}} in five bullet points.` |
| Code review checklist | ENGINEERING | `Review {{diff}} against {{style_guide}} and list blocking issues.` |
| Research synthesis | RESEARCH | `Compare {{sources}} and list where they agree about {{topic}}.` |
| Meeting follow-up | OPERATIONS | `Draft a follow-up to {{attendees}} covering {{decisions}}.` |
| Release notes draft | PRODUCT | `Turn {{changes}} into release notes for {{version}}.` |

Group two, destinations, holds seventeen entries, each with a one-line description: Home, Join the beta, Use cases, Changelog, Roadmap, Blog, Press kit, Contact, Privacy, Release notes 0.2.3, the five acquisition pages and the two articles.

**Semantics.** The search input is a combobox with list autocompletion, an expanded state and a label naming both halves of what it searches; it controls the listbox by identifier and points at the active option by identifier, and the first Blueprint is the initial active option. Spellcheck and autocomplete are off. The dialog's title and description are present but visually hidden, so they name the dialog for assistive technology.

**Behaviour.**

- It opens on Cmd K (Ctrl K off macOS), on the key cap in the navigation, and on a forward slash when focus is not in a field; it does not open on the slash when focus is inside a text field, a text area or an editable region.
- Up and Down move the selection and wrap at both ends; Enter activates; Escape closes; Tab is trapped inside.
- The footer hint names three actions, and its middle verb is the product's own word for sending a prompt: `Inject`.
- Activating a Blueprint entry scrolls to the matching home section and flashes the matching instrument; it never appears to send anything anywhere.
- Search runs in the browser over an index built with the site, matching title, category, description and body; within each group it ranks an exact prefix above a word prefix above a substring, and wraps each matched run in a `<mark>` element.
- An empty query shows the full list in the order above; a query with no matches shows a state offering `/download` and `/contact`.
- Opening locks page scroll, makes the page inert, and returns focus to the trigger on close; the scrim and panel use the palette blur, the command-surface gradient and the head-up shadow.

**Weight.** The index is small and ships with the first page; the panel itself may load on first use, but the key listener is registered immediately so the first press is never dropped.

**Discoverability without scripting.** The key cap is visible in the navigation on wide screens, the small-width menu carries a labelled search entry, and every palette destination is also reachable from the navigation or the footer, so a visitor without scripting loses only the shortcut.

### The instrument system

Seven composed mockups carry the product's argument. They are built from markup and styles rather than images, on frosted stages, to the same tokens as the site:

| Instrument | Represents | Home section |
|---|---|---|
| the launcher | the hotkey panel over a workspace | hero |
| the runner | one loop executing | workflow |
| the window | the library, sidebar and list | Blueprint Library |
| the context tray | files and remembered values docking to a prompt | Context |
| the time theatre | the version rail, scrubber and difference view | Time Machine |
| the packet | the three parts of a prompt as three cards | packet |
| the ledger | the history of sent prompts | history |

Rules for all of them:

- Every instrument showing plausible content carries a visible label marking it as demonstration data; on the history ledger that label is mandatory, because the product's claim is that the publisher cannot see your history.
- Non-interactive scaffolding inside an instrument is hidden from assistive technology, and the instrument as a whole carries one descriptive summary.
- An interactive instrument is genuinely operable by keyboard, never focusable but inert.
- Every instrument is legible as a still image: motion emphasises and never carries the meaning.
- At the narrowest width an instrument either scales as a unit from its top centre or scrolls inside its own container; it never makes the page scroll sideways.

**The hotkey demonstration**, opened from the hero's secondary action `Try the hotkey` and by the application shortcut Cmd Shift Space (Ctrl Shift Space off macOS), is a dialog that simulates the launcher: type to filter the five Blueprints, arrows to move, Enter to render the finished prompt with its blanks filled in a card with the preview glow, Escape to close. It opens only when the window is both wide enough and tall enough to fit it, so never on a short landscape phone. It never writes to the clipboard unless its `Copy` control is pressed. The result count is announced politely after each filter change, once typing settles. Focus is trapped, the dialog is labelled, and focus returns to the trigger on close.

**The context tray** on the home route lets a visitor switch individual files in and out. Switching one visibly updates the counts of files, values and docked prompts beneath it, and dims the matching token inside the prompt body.

**The docking transition.** A chip for a file appears to travel continuously from one list to another, at full frame rate, without triggering layout; under reduced motion it arrives instantly with a short fade. The flying copy is hidden from assistive technology, the change is announced once on completion, and the dock target shows a receptive state before the drop, not only after it.

**The window mockup** draws a title bar with the three dots, a sidebar, a capsule search field, a list of rows and a detail strip, under the gentle three-axis rotation. Hovering or focusing a row updates the detail strip; the row list is keyboard operable.

### Home (`/`)

Fourteen sections in this order. Eyebrows are short uppercase labels above the heading and are not headings themselves; only section 1's eyebrow is a pill with a live green status dot.

| Order | Eyebrow | Heading |
|---|---|---|
| 1 | Open beta, macOS, Cmd Shift Space | Any prompt, one keystroke away. |
| 2 | Command flow | One loop, not four separate chores. |
| 3 | Product surfaces | A native workspace for reusable prompt work. |
| 4 | none | Keep your best prompts as reusable Blueprints. |
| 5 | none | Attach the files and facts your prompt depends on. |
| 6 | none | Every prompt iteration has a history. |
| 7 | Prompt packet | The prompt is not just text. It is the whole working packet. |
| 8 | Audit trail | Know what you sent, when, and where. |
| 9 | Open beta | Shape what ships next |
| 10 | Local-first | Prompt work stays with your Mac. |
| 11 | Compare | A different category, by design. |
| 12 | Pricing | Free during beta. One-time pricing at 1.0. |
| 13 | Help panel | The trust questions before you join. |
| 14 | Open beta | Build the prompt library you can keep. |

Section anchors: section 3 is `#features`, section 2 is `#workflow`, section 12 is `#pricing` and section 13 is `#help`.

**The hero.** The left column holds the status pill, the headline at the top display step breaking over four lines at the widest width, a hand-drawn blue underline stroke beneath the final word (a slightly irregular line, the only hand-drawn element), three separate key caps (`Cmd`, `Shift`, `Space`), the sub-headline `Lumen Prompt keeps the prompts you reuse at work one keystroke away, with their variables, files and history.`, two actions, a note `Free during beta. No card required.`, and three outlined status chips `Local-first`, `Signed builds` and `No subscription`. The primary action is a single filled blue control with two stacked lines, a small uppercase `FREE DURING BETA` above and `Join beta` below, with a mail icon at its left; the secondary action `Try the hotkey` is outlined and ends in a key-cap chip. The right column is the launcher instrument, tilted and floating, with three key caps above its top-right corner and a thin connector down to the panel. At rest the panel rocks and rises on its loop, the workspace drifts, the caret blinks and the band sweeps; below the small breakpoint, under reduced motion or without scripting it is a still composition with the first row selected; off-screen, every loop is paused; pointing at a row makes it the selected row and updates the context strip beneath it to that Blueprint's variables.

**The workflow section** threads the four beats with the scroll-linked connector, under a runner header showing the shortcut, a live-run label, the Blueprint being run (`Client brief summary`) and the claim `No context switch`. Beneath the steps an output card labelled `Finished prompt` shows the rendered sentence with its blanks filled.

**The product-surface sections** share one layout: copy on one side and the instrument on the other, stacking below the wide breakpoint with the instrument first.

| Section | Instrument | Three bullets |
|---|---|---|
| Blueprint Library | the window mockup | search and filter instantly; organise by workflow, tag and variable count; open for editing, injection or history |
| Context and Variables | the context tray | turn placeholders into visible fields; include or exclude files before injection; remember project-level variables |
| Time Machine | the time theatre | a version scrubber per Blueprint; star ratings for strong versions; compare and restore controls |

The time theatre shows a rail of four versions, each with a number, a state word and a relative date; a scrubber whose thumb demonstrates itself by stepping through three positions on a loop until the visitor touches it, after which the demonstration never runs again in that session; a difference panel with one added line and one removed line, each prefixed with a plus or a minus in text; a restored-prompt card; and four controls. The scrubber is a real range control operable by the arrow keys, Home and End, and announces the version label (for example `Version 3, starred`) rather than a bare number.

**The packet section** shows three numbered cards for the three parts of a prompt (the reusable instruction, the files and values, and the record of sending it), each with a domain-noun icon, a number, a title, a sentence and a token chip, under a header card showing a Blueprint title with the shortcut, its body and three status chips.

**The history section** is the inverted region: three feature cards above the ledger, then six ledger rows, each a monospace timestamp with aligned figures, a Blueprint name, an arrow, a target application (Chatwell, Cadence, Vertan or Caret) and a detail reading either a file count with a version or `Quick copy`. The ledger carries the label `Demonstration data`; the ledger scrolls inside its own container and never chains its scroll to the page; both carets stop under reduced motion; the focus ring is checked against the dark ground.

**The beta note** is the only first-person copy on the site: Devrim's signed note that every beta message is read and sets the order of the roadmap, with a forward link `See the roadmap` to `/roadmap`.

**The local-first section** states the central claim as a sentence and four short guarantees (Blueprints, contexts, version history and injection history stay on your Mac) beside a boundary diagram: a core node for the machine, nodes inside the boundary for the four things that stay, and vendor nodes outside it. The diagram is fully legible as a still image.

**The comparison section** is a real table with a caption, column headers and row headers: seven feature rows against the three adjacent tools and Lumen Prompt.

| Feature | Lumen Prompt | Notary Docs | Rayline Snippets | Provider Projects |
|---|---|---|---|---|
| Global hotkey launcher | present | absent | present | absent |
| Variables with remembered values | present | absent | Plain placeholders only | absent |
| Version history per prompt | present | Page history, not per prompt | absent | absent |
| Context files attached before sending | present | absent | absent | Per project, in the vendor's cloud |
| Injection history | present | absent | absent | absent |
| Stored on your Mac | present | absent | present | absent |
| One-time licence | present | absent | present | absent |

Present and absent render as a check and a horizontal rule with the words in their accessible names, and the three qualified cells show their text instead of a mark. The dated footnote `Comparison checked on 2026-08-15 against each tool's public documentation.` renders in every layout. Below the comparison breakpoint the table becomes one card per tool, each listing all seven features, never a sideways-scrolling table; at intermediate widths the Lumen Prompt column stays visible while the table scrolls inside its own container. The narrower reduced-layout table has its own distinct caption.

**The pricing section** is three cards in a row, not two: Free, the founder licence, and a forward-looking card for 1.0. The middle card has an accent border and the scarcity badge.

| Card | Contents |
|---|---|
| Free | `$0`; `Everything, during the beta`; after 1.0 a free tier limited to 25 Blueprints, 3 contexts and 30 days of Injection History |
| Founder licence | the tier price; `About the cost of 15 billable minutes`; `Every 1.x update, for life`; four bullets (`One-time payment`, `Numbered founder place`, `Signed builds and updates`, `Price locked to your place`); `Standard licence at 1.0: $49`; the action `Claim a founder place` to `/download`; the note `Checkout is not open yet. Registering holds your place.` |
| At 1.0 | `Standard licence` `$49` (one Mac, twelve months of updates); `Extended licence` `$79` (three Macs, twelve months of updates); `Update renewal` `$19` (twelve more months of updates); `Requires macOS 26.1 or later` |

The founder card reads the live cohort from `GET /api/founder/allocation`: with fewer than 500 places held it shows `$29` and `N of 500 founder places left at $29`; from 500 to 999 held it shows `$39`, `N claimed` and `N left`; with all 1000 held it shows `Founder places are all claimed` and its action becomes `Join the beta`. If the count cannot be read, the card shows its static content with no badge at all, never a spinner, a zero or a hidden section. There is no subscription anywhere, and nothing implies one.

**The help panel** is eight numbered questions in a disclosure list, framed as a help console with a title bar and an `Esc` chip, above four category filter chips (`Privacy`, `Pricing`, `Beta`, `Platform`):

| Number | Question | Category |
|---|---|---|
| 01 | Does Lumen Prompt send my prompts anywhere? | Privacy |
| 02 | Can Halyard Labs read my library? | Privacy |
| 03 | Is there a subscription? | Pricing |
| 04 | What happens to the founder price after 1.0? | Pricing |
| 05 | How do I get the beta? | Beta |
| 06 | How are updates delivered and verified? | Beta |
| 07 | Which Macs are supported? | Platform |
| 08 | Which apps can receive a prompt? | Platform |

Each trigger is a button inside a heading with an expanded state and a controlled region. Height animates against the measured content height. Several items may be open at once. Category chips filter without navigating and keep the open state of the items that stay visible. Each item is linkable as `#faq-01` to `#faq-08` and opens when linked. All eight answers are in the delivered markup, collapsed by style, so they are indexable and findable with the browser's own find command; answer 08 names Chatwell, Cadence, Vertan and Caret.

**The closing section** carries the heading, a paragraph, the primary action, the requirements note `Requires macOS 26.1 or later.` and a four-row card of what arrives with beta access: the signed download, updates through the feed, your founder place, and a direct line to Devrim.

### Join the beta (`/download`)

**Above the form:** a heading, a sub-heading and four confirmation chips, each with a filled check icon: `Free during beta`, `No card required`, `Open registration`, `Founder pricing before 1.0`.

**The distribution panel** is a frosted pane with a shield icon, the heading `Official distribution`, one paragraph, six labelled monospace rows, a published date and a link to `/changelog`. Every value comes from the release registry, so the next release can never ship a page that misstates its own checksum:

| Row | Bound to |
|---|---|
| Current version | the current stable version and build |
| Verification | the fixed claim `Signed and notarised binary; update feed signed with a separate key` |
| Download route | `/downloads/latest` |
| Update feed | `/appcast.xml` |
| Requirements | `macOS <min_os> or later` and the binary size, both from the registry |
| Checksum | the SHA-256 digest from the registry, shown truncated with a `Copy` control that copies the full value |

**The four-step explainer** is a numbered list of exactly four steps in the site's own words: register your address; open the link we email you; the access page records a token-scoped click and forwards you to the download; the application checks future updates through the feed. It never drifts from the access-link rules.

**The form** is seven fields in a two-column grid, the first spanning both columns:

| Order | Field | Type | Required | Notes |
|---|---|---|---|---|
| hidden | `company_website` | text | no | the trap: hidden by position rather than display, removed from the tab order and hidden from assistive technology, so no person is ever asked to fill it |
| 1 | email | email | yes | spans both columns, email autofill hint, spellcheck off |
| 2 | name | text | no | name autofill hint, placeholder `Optional` |
| 3 | platform version | select | no | five options: an empty first option reading `Not sure`, then `macOS 26.1`, `macOS 26.2`, `macOS 26.3`, `macOS 27` |
| 4 | role | text | no | placeholder `Consultant, researcher or engineer` |
| 5 | primary use | text | no | placeholder `Client briefs, code review or research notes` |
| 6 | consent | checkbox | yes | the sentence `Send me my beta access link and occasional beta updates at this address. I have read the privacy policy.` |
| widget | bot-protection challenge | widget | - | its box is reserved before anything loads |
| action | submit | button | - | `Join the beta`, tall, filled blue, full width at narrow widths |

Beneath it: the reassurance line `One email with your link. No newsletter.` and the fallback note `If no build is ready when you open your link, the page confirms your registration and we email you when the first build ships.`

**Validation** runs in three layers and only the server counts: markup constraints (required on email and consent, an email type), a client layer on blur and on submit that never blocks a submission it disagrees with, and the server on every submission. A missing email asks for an address so the link can be sent (`Enter an email address so we can send your access link.`), and a malformed one is flagged as a probable typo with its own message (`Check the address, it looks like a typo.`); length errors name the limit; a missing consent asks for confirmation (`Confirm you want the access link.`); the trap never produces a message.

**Error presentation.** Errors render beneath each field and in a summary at the top of the form that links to each invalid field; the summary takes focus on a failed submission and announces itself assertively. Each invalid control is marked invalid and points at its own message. Error text uses the darker danger text colour plus an icon plus the words, never colour alone. Errors clear as the visitor types, not on blur, and entered values survive every failure path, including a full reload after a server error.

**Success.** The form is replaced in place by the `Check your inbox` panel naming the address, suggesting the spam folder, and showing `Resend link` disabled for 60 seconds with a visible count. The panel also shows the cohort as a whole (places left, or `Founder places are all claimed`), never the visitor's own place, and it looks identical for a first and a repeat registration; the email is where a repeat registrant learns they were already on the list. If the cohort closed while the page still showed places remaining, the panel says so honestly and the pricing numbers update; the registration itself does not fail, because registration and founder allocation are two outcomes of one step and only the second can come back empty.

**States.** While submitting, the action shows progress and marks itself busy, fields disable, and a second submission is absorbed rather than duplicated. Offline, a message says so and every value is preserved. If the challenge widget fails to load, its box stays reserved and the submission still proceeds. A backend failure shows a try-again message with the values preserved.

### Use cases (`/use-cases`)

The page structure is a heading, a sub-heading explaining that these are pages for five specific search intentions, the radial diagram, then five numbered cards. Each whole card is the link, and its large monospace numeral is its dominant element.

| Number | Eyebrow | Card title | Route |
|---|---|---|---|
| 01 | Reusable templates | reusable prompt templates | `/use-cases/reusable-ai-prompt-templates` |
| 02 | Time Machine | prompt version history | `/use-cases/prompt-version-history` |
| 03 | Mac prompt manager | prompt manager for Mac | `/use-cases/prompt-manager-for-mac` |
| 04 | Local-first | local-first prompt library | `/use-cases/local-first-prompt-library` |
| 05 | Hotkey launcher | prompt launcher for Mac | `/use-cases/hotkey-prompt-injection-macos` |

**The radial diagram** is the centrepiece: a core node carrying the shortcut, an orbit ring turned slightly, and five nodes around it that are real links to the five pages. The core carries the diagram-core blur, the largest radius and a teal-and-blue bloom behind it; each node carries the diagram-node blur, a soft vertical white gradient and its own glint loop; a scan sweeps the ring and fades out toward the edges through a radial mask centred slightly above the middle rather than clipping; three short labels beneath name example pieces of work (`Client briefs`, `Code reviews`, `Research notes`). The orbit ring and the scan are decorative and hidden from assistive technology.

### Use-case pages

Five pages on one template. Each owns one search phrase and one first-level heading:

| Route | Eyebrow | Heading |
|---|---|---|
| `/use-cases/reusable-ai-prompt-templates` | Reusable templates | Reusable AI prompt templates for Mac, with variables that fill themselves. |
| `/use-cases/prompt-version-history` | Time Machine | Prompt version history that shows what changed and which version worked. |
| `/use-cases/prompt-manager-for-mac` | Mac prompt manager | A prompt manager for Mac that lives one keystroke away. |
| `/use-cases/local-first-prompt-library` | Local-first | A local-first prompt library that never leaves your Mac. |
| `/use-cases/hotkey-prompt-injection-macos` | Hotkey launcher | Hotkey prompt injection on macOS, into the app you already use. |

Blocks in order: the hero (eyebrow, heading, sub-heading, two actions, a note about beta terms, three proof chips); one instrument specific to the page; a contrast block with two columns headed `Without Lumen Prompt` and `With Lumen Prompt`; a product-proof block with a heading, a paragraph and a full application mockup; two argument blocks, each a heading, a paragraph and three bullets; four numbered steps specific to the page; a short disclosure list of search-intent questions; a `Related use cases` section holding the other four pages as cards (never the page itself); and the standard closing call to action.

Every page with an application mockup carries the synthetic-data disclaimer `The visual language follows the running application, but the content is purpose-built synthetic marketing data, not real workspace text.`, and the mockup itself carries the shorter label `Demonstration data`. Each page has one first-level heading carrying its phrase, a canonical link to itself, a `BreadcrumbList` trail in JSON-LD structured data, and `FAQPage` structured data for its disclosure list; `/` and `/download` carry `SoftwareApplication` structured data describing the application.

### Changelog (`/changelog`)

A heading, then the sub-heading `Release notes are linked from each version, so this page and the in-app updater share one source of truth.`, then the current stable block and the earlier releases. The current stable block shows the version and published date, the platform requirement, the recorded download count (a stored number read from the registry, omitted rather than shown as zero if it cannot be read), the release summary, a release film with a poster image, the static verification claim, the download route and feed path, the binary size and the full checksum, and two actions: `Download` (to `/downloads/latest`) and `Read the notes` (to the release's notes). Each earlier release shows its version, date, platform requirement, size, a truncated checksum, its summary, a film link and a notes link. A revoked release shows the notice `This release was revoked and is no longer offered.` and no download control. The whole route is a projection of the registry.

### Release notes (`/release-notes/{version}`)

A version heading with its date, an opening summary, the note `Lumen Prompt is free during the beta.`, then these sections in order: `What is new`, `Also in this release`, `Fixed`, `Performance`, `Known issues`, `Updates`, `Reporting problems`. The route has two audiences: it is served both to browsers and to the update panel inside the application, so it renders completely with no scripting, fits a small panel at a narrow width, follows a dark system appearance (the only route that does), and shows each version's content exactly as published. The known-issues section is a product-honesty surface and is always rendered when the release has one; the import note names `Obelisk`.

### Roadmap (`/roadmap`)

Three buckets with eleven items, each a title and a short paragraph, and the caveat `Order and scope change with beta feedback.` There are no dates, no percentages and no progress bars anywhere on the page.

| Bucket | Label | Items |
|---|---|---|
| Now | Active in the current open beta | Open beta hardening; Version-history refinements; Context workflow polish; Injection history |
| Next | Coming before 1.0 | Organisation improvements; Variable memory per Blueprint; Founder-terms finalisation; Release polish |
| Later | Planned for 1.0 and beyond | The 1.0 release; Sharing and export; Deeper injection options |

`Variable memory per Blueprint` says remembered values will be scoped per Blueprint rather than globally so one workflow's values do not bleed into another; `Sharing and export` says sharing will work without requiring an account layer or a shared server.

### Blog (`/blog` and the two articles)

The index lists `Stop rewriting your best prompt` (`/blog/stop-rewriting-your-best-prompt`, category `Workflow`, dated `2026-08-20`) above `Prompts are work product` (`/blog/prompts-are-work-product`, category `Essay`, dated `2026-07-30`), newest first, each card showing a category, a date, a reading time, the title and a two-sentence summary. The reading time is computed from the article body's word count, divided by 200 and rounded up, shown as `N min read`, never typed by hand. An article page shows the title, summary, date, reading time, the prose at the wider prose measure, related articles and the closing action. These are the only routes with no instrument and no mockup.

### Press (`/press`)

A heading; a three-sentence description of the product; a press kit download that states its size before the click, `Download the press kit (48 MB)`, pointing at `https://downloads.example.com/lumen-prompt/press-kit.zip`; a fact sheet; application captures; two silent motion loops; interface detail panels; and usage guidelines.

The fact sheet has seven rows: Name (Lumen Prompt); One-liner; Platform and distribution (macOS 26.1 or later, direct download, no app store); Status (open beta, founder licence `$29` then `$39`); Developer (Halyard Labs, Devrim); Contact (by way of `/contact`); Site (`APP_PUBLIC_URL`).

Twenty-three captioned captures, each available as a light and a dark variant; the caption describes what the image shows and is reused as its alternative text. Each image ships in a modern format with a fallback and explicit dimensions so the page never shifts as it loads. A `Light` / `Dark` control on the page chooses which variant is shown, independent of the reader's system setting. The two motion loops are muted, carry a poster frame, do not preload, and never play automatically under a reduced-motion preference. Everything below the fold loads lazily and this route adds nothing to the shared bundle used by the rest of the site.

The usage guidelines are two lists with visible headings. **You may:** publish the images unaltered; credit Lumen Prompt and Halyard Labs; link to the site; preserve the icon's proportions. **You may not:** recreate the interface with invented data; imply availability through an app store; quote prices beyond the published ones or imply a subscription; take assets from anywhere but this kit.

### Contact, Privacy and Terms

`/contact` has a heading, the sentence `Beta questions, support, privacy requests and press all reach a person at one address.`, the address `hello@example.com` as both a mail link and plain selectable text, and a line asking for the macOS version and the Lumen Prompt version from the About panel. The mail link carries the subject `Lumen Prompt support` and a body template with the labelled blanks `macOS version:` and `Lumen Prompt version:`.

`/privacy` and `/terms` render from source documents at the wider prose measure, with a generated table of contents, a stable identifier on every heading, and print styles that suppress backgrounds and write each link's address after its text.

| Page | Headings (identifier) |
|---|---|
| Privacy | What the website stores (`what-the-website-stores`); What never leaves your Mac (`what-never-leaves-your-mac`); Access links and sessions (`access-links-and-sessions`); Processors (`processors`); Analytics (`analytics`); Your rights (`your-rights`); Contact (`contact`) |
| Terms | The beta (`the-beta`); Founder licences (`founder-licences`); Updates and signing (`updates-and-signing`); Acceptable use (`acceptable-use`); Liability (`liability`); Contact (`contact`) |

The privacy page states that an access session lasts at most fourteen days, that no analytics of any kind load on the access route (or anywhere on the site), that the processors are the database host, the mail provider and the billing ledger, and that the website holds registrations while prompt work never leaves the user's machine. `/legal/data-request` is linked from `Your rights`.

### Access and error pages

The access route has no analytics, carries the no-index instruction, and rewrites its address to drop the token once the session is set, so the token never persists in history, a screenshot or a shared tab. It never forwards on its own when the visitor prefers reduced motion or arrived by keyboard; the `Download for Mac` control is always rendered and receives focus. The four failure pages each explain what happened in their own words and carry the re-request form (an email field and the reserved challenge box).

The not-found page is branded, offers the palette shortcut, and links to `/`, `/download`, `/changelog` and `/contact`. The error page is branded, shows a request identifier for support, offers a retry, and links to `/downloads/latest` directly because the download does not depend on the failing path. If the layout itself fails, a minimal page with inline styles and no dependencies still renders.

### The Mac application the pages describe

This background describes the native application that the pages, instruments and demonstrations portray. The application itself is not built here; nothing on the site may contradict this description.

It is a single-player program with no accounts, no other users and no server. Its five surfaces: the launcher (a floating panel over whatever is in front, summoned by the global shortcut), the main window (sidebar, list and detail, from the dock or the launcher), the inspector (a panel attached to the main window, with its own shortcut), the menu-bar companion (a small popover of favourites and recents) and settings (the standard preferences window).

- The launcher appears over the active workspace and takes keyboard focus while the application in front stays the destination for the finished prompt, captured at the moment of summoning. It appears on the screen with the pointer, on the active desktop, over full-screen applications. The search field takes focus the instant the panel opens. Dismissing returns focus with no visible flash. Summon to first keystroke stays quick on a library of five thousand saved prompts. It never appears in front of a secure input field. Search ranks exact title prefix, then title word prefix, then category, then body, breaking ties by use; operators for category, context, variable, favourite state and recency fall through to plain text when unrecognised; an empty query shows recent sends, each replayable with its previous values.
- The library has three panes (a sidebar of the four collections plus categories, archive and trash; a list; a detail view). Rows show title, category chips, a truncated body, a variable count, a context indicator, a favourite marker and a relative last-used date. It supports multiple selection with bulk categorise, archive and export; multi-select category filters combining as and; drag reordering that rewrites only the moved row; docking by dragging onto the context tray, or from the context menu and the inspector; archive (hidden, kept) distinct from trash (recoverable delete with a retention window); undo for destructive actions; and a list that stays smooth at ten thousand rows.
- The editor highlights double-brace variables as single objects while keeping ordinary text, offers completion after an opening brace pair, keeps the insertion point inside the braces while a name is typed, shares one renderer between reading and editing, grows with the window with long prompts scrolling inside their card, never lets typing contend with search indexing or sync, and keeps an undo stack covering text, token insertion, category changes and docking.
- Variables become labelled fields in document order with the first focused; saved values are offered with a use count; a ghost suggestion offers the most used value, accepted with Tab or the right arrow; a guard blocks sending until required fields are filled, naming and focusing the first; values are scoped per saved prompt; a live preview shows substituted values distinctly. Secret values are held in the platform credential store, masked while typed, and excluded from version snapshots, history, diagnostics and logs; a second machine asks for them to be set locally.
- A context bundles files, remembered values and notes, and a prompt docks to one. Files are added by drag, by picker, or by dragging a prompt onto the tray. Per-file switches show before sending; the tray shows live counts; a size estimate warns before a chosen model preset is exceeded; files are held as durable references. A file missing on another machine renders as unavailable with a locate control, and a send that depends on a missing file is blocked with a list of what is missing.
- Version history shows a rail with number, relative date, rating and label; a keyboard scrubber announcing the version; ratings per version; a word-level difference view with plus and minus in text; restoring creates a new version rather than rewinding; a fingerprint of attached files per version warns on restore; full snapshots rather than differences; comparisons computed only for the visible pair. When sync would discard local text, the losing text is saved as a rescued version and the person is told.
- Sending places the finished prompt on the clipboard and pastes it into the captured application. It needs the accessibility permission, whose absence is explained with a direct link to the settings pane. Secure fields and some applications refuse a synthetic paste; the prompt then stays on the clipboard and the person is told. Browser tabs cannot receive attached files, and a browser destination is detected and explained. Nothing is ever sent into a password field. Every outcome is recorded with its reason, and the previous clipboard contents are restored afterwards, including on every failure path. The application does not read keystrokes or record other applications' contents.
- History records every copy and send with time, prompt, version, destination, mode, file names and counts; filters by date, prompt, destination, mode and attached files; replays a record into the fill step; stores the finished text only when a setting (on by default) allows; always excludes secret values; and exports for the person's own records.
- Import runs four steps (choose a source, preview everything, resolve duplicates, read a summary): nothing is written until the final confirmation, duplicates are detected before any write with per-item and bulk resolutions, the whole import is one undoable step, a malformed file produces a per-item error in the preview, and the preview marks the one source whose form and choice placeholders arrive as plain text.
- Categories can be renamed, coloured from the design tokens and merged; a merge is previewed with counts, undoable, and never duplicates an assignment. Onboarding seeds a sample context and an optional tour ending in a practice surface where the first send lands safely, with a five-milestone checklist whose completion persists. Diagnostics builds a sanitised report, previewed in full, carrying versions, permission states, sync status, counts, error signatures and timings and never prompt bodies, variable names or values, file names or finished text; the report-a-problem command offers to copy the address and body when no mail handler exists.
- Every application surface is fully keyboard operable and labelled for the screen reader, the launcher announces its result count and selected row, larger text reflows, increased contrast and reduced transparency are honoured, reduced motion covers the tray and docking, no status is carried by colour alone, and the practice surface and permission explanations are readable before any system permission prompt appears.

## Constraints

- One public site plus the operator console; no second site, no admin panel beyond `/operator`.
- No cloud prompt library and no endpoint that accepts Blueprints, context files, rendered prompts or history rows.
- No call to any AI vendor.
- No end-user accounts, passwords, workspaces, teams or shared libraries; registrants have no password.
- No password reset and no external identity provider.
- No subscriptions, recurring billing or dunning.
- No checkout, invoice, payment method, refund or licence activation before 1.0.
- No analytics provider and no live bot-protection provider; no external network calls at runtime other than the three backing services.
- No general permission engine, organisation chart or approval chain.
- The native macOS application is not built here.
- No file uploads and no object storage; release binaries and the press kit live on the asset host.
- The site stays responsive with 1000 founder places, 10000 registrations and 100 releases.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials (or an explicit statement that there are none) are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.** Field names are exact. List endpoints return a top-level JSON array. A successful call returns the named shape; an invalid or unauthorized call is rejected as a client error, never a server error and never a silent success. Operator endpoints take `Authorization: Bearer <token>`; `/api/beta/status` reads the access session cookie; everything else needs no authentication.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | `{"status": "ok"}` |
| `POST /api/beta/register` | `email`, `name`, `platform_version`, `role`, `primary_use`, `consent`, `company_website` | `{"status": "sent", "message": "Check your inbox for your access link.", "email"}`; invalid: `{"errors": {field: message}}` |
| `POST /api/beta/resend` | `email` | `{"status": "sent", "message": "If that address is registered, a fresh access link is on its way."}` |
| `GET /api/beta/status` | access session | `{"email", "founder_position", "founder_tier", "founder_price_minor", "currency", "billing_account"}` |
| `GET /api/founder/allocation` | none | `{"cap", "tier_size", "claimed", "remaining", "state", "current_tier", "current_price_minor", "currency"}` |
| `GET /api/releases` | none | array, highest build first, of `{"version", "build", "published_at", "min_os", "size_bytes", "sha256", "ed_signature", "download_url", "summary", "status", "download_count"}` |
| `GET /api/releases/{version}` | none | one release with the same fields plus `notes`; unknown version: not found |
| `POST /api/checkout/founder` | any | rejected: `{"error": "checkout_not_open"}` |
| `POST /api/licence/activate` | any | rejected: `{"error": "licensing_not_open"}` |
| `POST /api/legal/data-requests` | `email`, `kind` | `{"status": "received", "message": "We will reply to that address within 30 days."}` |
| `POST /api/auth/login` | `email`, `password` | `{"access_token"}` |
| `GET /api/admin/registrations` | operator; optional `?email=<address>` | array, newest first, of `{"email", "name", "founder_position", "challenge_status", "created_at"}`; empty array when nothing matches |
| `POST /api/admin/releases` | operator; `version`, `build`, `min_os`, `size_bytes`, `sha256`, `ed_signature`, `download_url`, `summary`, `notes` | the stored release |
| `POST /api/admin/releases/{version}/revoke` | operator | the release with `status` `revoked` |
| `POST /api/admin/access-links/revoke` | operator; `email` | `{"revoked": n}` |
| `GET /beta/access/{token}` | none | the access page or one of the four failure pages |
| `GET /downloads/latest` | none | a redirect to the current stable `download_url` |
| `GET /appcast.xml` | none | the update feed |

**No mocks.** Each of these is a contract violation, however good the interface looks: a founder place held only in memory or only in the app's own tables with no matching account in `killbill`; a `killbill` response the app writes and answers to itself; an access email written to a log or a file instead of sent through Mailpit; a release list hard-coded in page templates instead of read from the `releases` table; a download count kept in the browser. The named provider is the fact: the app's UI and its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A visitor can register on `/download`, receive the access link by email, open it to reach the current signed build, and see their founder place. However many people register at once, the thousand founder places are held by exactly one address each, in order and with no gaps, each with its own billing account in `killbill`, and nobody receives a thousand-and-first. The changelog, the download redirect and the update feed always agree with the published releases.
