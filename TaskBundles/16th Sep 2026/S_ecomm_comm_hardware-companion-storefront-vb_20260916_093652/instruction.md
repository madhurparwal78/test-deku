# Opal

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser,
read the founder letter over the workshop film, add a camera to the cart, check
out as a guest, and receive an order confirmation email, without hitting an error
page. Placing an order must raise exactly one invoice on the buyer's account in
the payments provider for the exact order total and currency, because a separate
check reads the payments provider, the mailbox and the database directly and an
order that only exists on screen does not count.

---

## Overview

Opal is the direct to consumer site for a small company that designs and sells its
own cameras. A visitor reads a founder letter over a full screen film of the
workshop, buys a camera and its accessories, registers the device to an account,
downloads the companion desktop application, reads its release notes, and flashes
new firmware from the browser. The commercial spine is a server side cart and a
three step guest checkout.

The genuinely hard parts are two. The money must be honest: placing an order
raises one invoice on the buyer's account for the exact re-priced total, and
submitting the same checkout twice must never raise a second invoice. And the
side effects must be real: the invoice lives in the payments provider and the
confirmation lives in the mailbox, not merely on the success screen.

---

## User roles

| Role | Can do |
|---|---|
| `customer` | Browse the storefront and read the founder letter without signing in; add items to a server side cart; check out as a guest or signed in; after an order, turn the guest order into an account; sign in to see their own orders, register a purchased camera by serial, flash a registered device to a newer firmware, and read the companion application releases. **Cannot** read another account's orders or devices, and **cannot** flash a device they do not own. |

Signup is open: anyone may create an account with an email address and a password.
Guest checkout is the default and needs no account. Authorization is enforced
server side on every mutating endpoint and on every read of an order or a device:
a direct API call from one account for another account's order or device, or from
an anonymous caller for any account-scoped resource, must be rejected by the
server, leaving the protected state unchanged.

Two accounts are seeded for demonstration: `customer@example.com`, who owns one
delivered order and one registered device, and `customer2@example.com`, with an
empty cart. Both use the seeded password.

---

## Core features

### Accounts and sessions

Email and password accounts. Passwords are hashed at rest and never stored or
logged in plaintext. Login returns a bearer token the client sends as
`Authorization: Bearer <token>`; tokens expire after 8 hours. Signup rejects an
already registered email and a password shorter than 8 characters, each with a
client error that names the field. There is no password reset and no third party
login.

### The storefront and the founder letter

A catalogue lists the cameras and their accessories, each with a name, a kind of
`camera` or `accessory`, and a price in whole minor units of `usd`. A product
detail page shows the media, the description, the variants and the price. The
founder letter plays over a full screen video stage that is muted and looped. The
catalogue and the letter are public and readable without an account.

### The cart

The cart lives on the server and is keyed to the signed in customer or to an
opaque cart token, never held in the browser. Rules, each individually checkable:

1. Adding a variant to the cart creates or updates the caller's cart line and the
   cart read returns the line with its quantity and its unit price.
2. A cart line stores the unit price at the moment it was added, and every cart
   read compares that against the variant's current price and shows a notice on a
   change rather than updating silently.
3. Adding to the cart reserves no stock; stock is committed at order creation.

### Checkout and the order

Checkout collects contact and delivery details, a shipping method, and payment,
then places the order. Rules, each individually checkable:

1. Checkout re-prices every line from the current variant price before the order
   is placed, and the total placed is the exact integer raised on the invoice.
2. Placing an order raises exactly one invoice on the buyer's account in the
   payments provider for the order total and the currency `usd`.
3. Placing an order records the order with a status of `paid` and sends the buyer
   a confirmation email whose subject carries the order reference.
4. Guest checkout is the default; creating an account is offered only after the
   order is placed.

### The account: orders, devices and firmware

A signed in `customer` sees their own orders newest first, each with its
reference, total and status. A customer registers a purchased camera to their
account by its serial number, and a serial already registered is refused. A
customer flashes a registered device to a newer firmware release, which records
the update and moves the device to the flashed version; a device belonging to
another account cannot be flashed. A camera model exposes its firmware releases,
each with a version, release notes and a checksum, and the companion desktop
application exposes its releases with a version and release notes.

### Consent, telemetry and abuse control

A first time visitor is asked once about non-essential cookies, and the answer
survives a reload. Each page view is recorded with its route and a timestamp, and
an owner can read the recorded page views. A contact form carries an unattended
decoy field and refuses a submission when the decoy is filled or when the same
form is submitted repeatedly in quick succession.

---

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | The founder letter over the video stage | No |
| `/shop` | The catalogue of cameras and accessories | No |
| `/product/{slug}` | A product detail page with its variants and price | No |
| `/cart` | The server side cart with its lines and totals | No |
| `/checkout` | The three step checkout: contact, shipping, payment | No |
| `/signup` | Create an account | No |
| `/login` | Email and password login | No |
| `/account/orders` | The customer's own orders, paginated | `customer` |
| `/account/devices` | Registered devices, registration and browser flash | `customer` |
| `/downloads` | The companion application releases and firmware notes | No |

**Entry and redirects.** An unauthenticated visit to an account route redirects
to `/login`. Successful login lands on `/account/orders`. Logout returns to `/`.
An expired token acting mid page redirects to `/login` without crashing the view.

**Journeys.**

1. **Buy a camera.** Open `/shop`, add the Opal One to the cart, open `/checkout`,
   enter a delivery address, choose a shipping method, and place the order. The
   order shows as `paid`, an invoice is raised on the buyer account, and a
   confirmation email arrives.
2. **Register and flash.** Sign in as `customer@example.com`, register a camera by
   its serial on `/account/devices`, then flash it to the newest firmware release
   and confirm the device moves to that version.
3. **Read the letter.** Open `/`, watch the founder letter play over the muted
   looped workshop film, and follow the single primary action into `/shop`.
4. **Guest to account.** Check out as a guest, then accept the offer to turn the
   guest order into an account, and sign in to see the order under `/account/orders`.

**States.** Every list and the cart have a loading state and an empty state ("Your
cart is empty" with a link to the shop). Rule rejections surface the specific
reason inline. A network failure shows an inline retry, never a blank screen.

---

## UI/UX notes

The site reads as printed matter from a workshop: a warm off-white neutral paper
ground, white neutral raised surfaces, a near black neutral ink for text, and a
light neutral hairline between regions. A mid neutral grey carries secondary text.
Colour is spent sparingly: one hot orange marks the single primary action on a
page, and a bright amber yellow is used only as a highlight. State is never carried
by colour alone; every status also carries a text label, and each page leads with
exactly one clear primary action set apart from every secondary control.

**Type.** A grotesque display face carries the headings and the founder letter,
and a plain grotesque carries body text. Prices, totals and counts use tabular
numerals so columns align.

**Motion.** Motion is restrained: panels and checkout steps ease to a stop and
nothing bounces. The video stage behind the founder letter plays muted and
looped. Use a short eased transition on hover, focus and step changes. Respect
`prefers-reduced-motion` by disabling every non essential animation and pausing
the video.

**Accessibility and responsiveness.** Meet WCAG AA contrast for body text, give
every interactive control a visible focus ring, and support full keyboard
navigation through the catalogue and the checkout steps. Icon only controls carry
text labels. Every content image carries alternative text and a purely decorative
image declares itself decorative. The layout is responsive: it holds from a narrow
viewport up to a wide desktop, and at a narrow viewport nothing overflows sideways.

---

## Technical requirements

- **Frontend:** React 18 with Vite and TypeScript.
- **Backend:** Node.js 20 with Express.
- **Database:** PostgreSQL, read the connection string from `DATABASE_URL`. The
  service is already running; do not install or start your own.
- **Payments:** killbill, reached with `PAYMENTS_API_URL`, `PAYMENTS_API_KEY` and
  `PAYMENTS_API_SECRET`. Placing an order raises an invoice on the buyer's account
  in killbill; the running check reads the invoice back from killbill, never from
  the app's own tables.
- **Email:** Mailpit over SMTP, reached with `SMTP_HOST` and `SMTP_PORT`. The order
  confirmation is a real message sent to Mailpit, read back from its inbox by the
  running check.
- **Auth:** in app email and password, hashed at rest, stateless bearer tokens with
  an 8 hour expiry.
- **Health:** `GET /api/health` returns `200` when the app and its backing services
  are ready.
- **Logging:** requests and errors to stdout.

**Checkout under concurrency.** Placing an order must stay correct when the same checkout is submitted more than once.
Two checkout requests for one cart carrying the same `Idempotency-Key` must place exactly one order and raise exactly one invoice.
The second request must return the first order's reference and must not create a second order.
A replay of that request with the same key must produce no second charge and no second invoice.
The same key sent with a different cart is rejected with `409 Conflict`.
Application level checks alone are not sufficient under this contention; state the observable outcome and choose any approach that delivers it.

**Paginated reads.** The catalogue and the account orders are read as pages. Each
list endpoint accepts a `limit=` query parameter, named `page_size`, with a default
of 20 and a maximum of 100. The client fetches the following page by passing an
opaque cursor back unchanged. The opaque cursor stays stable as the catalogue
grows, so paging never repeats or skips a row across thousands of orders. Every
list response carries `next_cursor`, which is null on the final page, and a
`has_more` boolean. A request for a page beyond the end returns an empty page with
`has_more` false rather than an error.

- **No secrets in the browser bundle.** Payments, database and SMTP credentials
  are used only on the server and must never be compiled into or served with the
  frontend bundle.

Use only the libraries named here plus their direct dependencies. Do not introduce
a second database, a cache, a message queue, an object store, an identity provider
or a second payment or mail vendor: the only backing services in this environment
are PostgreSQL at `DATABASE_URL`, killbill at `PAYMENTS_API_URL` and Mailpit at
`SMTP_HOST`, and reaching for anything else is a contract violation.

---

## Data model

All timestamps are UTC. Money is whole minor units of `usd`.

> **Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
> fixture data, not a secret. Hash it as normal; the exact literal must work at
> login, and it must be written into `/app/USER_README.md` alongside each account
> so a reviewer can sign in.

**`accounts`** id; email (unique, lowercased); password_hash; role (`customer`);
created_at.

**`products`** id; name; kind (`camera` or `accessory`); slug (unique);
description; active; created_at.

**`variants`** id; product_id (the owning product); sku (unique); price_minor
(whole minor units); currency; created_at.

**`carts`** id; token (opaque, unique); customer_id (null for a guest);
currency; created_at.

**`cart_lines`** id; cart_id; variant_id; quantity (1 to 10); unit_price_minor
(the price snapshot at add time).

**`orders`** id; reference (unique); customer_id (null for a guest order); email;
external_key (the idempotency key for the placement); status (`paid`);
total_minor; currency; invoice_ref (the payments provider invoice id); created_at.

**`order_lines`** id; order_id; variant_id; quantity; unit_price_minor.

**`devices`** id; account_id (the owner); product_id; serial (unique);
firmware_version; registered_at.

**`firmware_releases`** id; product_id; version; notes; checksum; released_at.

**`app_releases`** id; channel; version; notes; released_at.

**`page_views`** id; route; occurred_at; account_id (null for an anonymous view).

**Rules the data must keep.** An order's total equals the sum of its re-priced
lines, and the invoice raised in killbill matches that total and currency exactly.
Two placements of one checkout with the same `external_key` leave exactly one order
and one invoice. A registered `serial` is unique, and flashing a device changes
only its `firmware_version`. A rejected checkout leaves neither an order row nor an
invoice behind.

**Derived, never stored:** each list page's cursor, the cart totals and the price
change notice are computed on read. There is no stored total that can drift from
its lines.

**Seed data, exact and idempotent, relative to first start:**

- Products: `Opal One`, a `camera`, priced at `79900`; `Opal Grip`, an
  `accessory`, at `4900`; `Opal Strap`, an `accessory`, at `2900`. All in `usd`.
- Accounts, both with the seeded password: `customer@example.com` (`customer`) and
  `customer2@example.com` (`customer`).
- `customer@example.com` owns one order with status `paid` for an `Opal One`, and
  one device registered by serial on firmware version `1.0.0`.
- Firmware releases for the `Opal One`: version `1.0.0` and a newer `1.1.0`, each
  with notes and a checksum. Companion application releases: `2.0.0` and `2.1.0`.

Seeding must be idempotent: restarting the app must not duplicate rows.

---

## Build plan

1. **Setup** scaffold the frontend and backend; `GET /api/health` returns `200`.
   Exit: health green through the public URL.
2. **Database and services** create the tables above and confirm the app can reach
   killbill and Mailpit; idempotent seed of products, accounts, the seeded order,
   the device and the releases. Exit: seed rows in Postgres, a reachable payments
   API, a reachable inbox.
3. **Auth** signup, login and bearer middleware. Exit: seeded accounts log in with
   the pinned password; an account route rejects an anonymous call.
4. **Storefront** the catalogue, the product detail page, and the founder letter
   over the video stage. Exit: a visitor reads the letter and opens a product.
5. **Cart** the server side cart, the price snapshot and the change notice. Exit:
   adding a variant returns a line, and a price change renders a notice.
6. **Checkout** re-price, place the order, raise one killbill invoice, send one
   confirmation email. Exit: an order shows `paid`, an invoice exists in killbill,
   an email arrives in Mailpit.
7. **Idempotency** the concurrency and replay outcomes. Exit: a duplicated key
   places one order and raises one invoice, and a replay charges nothing further.
8. **Account** orders, device registration, browser flash, and the release feeds.
   Exit: a device registers by serial and flashes to a newer firmware version.
9. **UI, consent and hardening** palette, type, states, motion, responsive layout,
   the cookie choice, the page view log, the contact decoy, form validation. Exit:
   every viewport holds with no sideways scroll and every negative case returns its
   named reason.
10. **Deploy and self test** production build, detached start, then walk every
    journey in a real browser. Exit: all four journeys pass against the deployed
    app, cold.

---

## Constraints

- One storefront for one company; no multi-vendor marketplace and no reseller tiers.
- No card processor: an order is booked as an invoice on the buyer's account in
  killbill, not collected from a card vendor, and the app never sees a card number.
- No digital wallets, no accelerated one-tap checkout and no buy-now-pay-later.
- No shipment protection line, no tax engine and no shipping-zone resolver beyond a
  chosen method with a flat price.
- No warranty, returns, support desk or operations console.
- No object store: firmware and application releases are database records with a
  version, notes and a checksum, and a flash records a device firmware update.
- No webhooks, no presets, no cloud sync and no search index.
- No second datastore, cache or queue beyond the PostgreSQL, killbill and Mailpit
  named here, and no external network calls at runtime beyond them.
- Responsive web only; no native app.
- The catalogue and the orders list must stay responsive with thousands of rows.

---

## Deployment contract

Your application is served over HTTP and opened in a browser after your session
has ended.

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`: `4173` is the container internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written
  to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the
  app root, empty.
- Serve a production build behind a static or preview server, never a dev
  server.
- The server must keep running after this session ends and must not be a child
  of the shell. An ordinary background job dies with its shell, and the app will
  not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy
  of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

Write `/app/USER_README.md` with the seeded accounts and their password.

### API shapes

| Endpoint | Request body or query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{email, password}` | `{token}` |
| `POST /api/auth/login` | `{email, password}` | `{token}` |
| `GET /api/products` | `?kind=&page_size=&cursor=` | `{items, next_cursor, has_more}` |
| `GET /api/products/{id}` | the product | the product with its variants |
| `GET /api/cart` | the caller's cart | `{lines, subtotal_minor, currency, notices}` |
| `POST /api/cart/lines` | `{variant_id, quantity}` | the cart |
| `POST /api/checkout` | `{email, address, shipping_method}`, optional `Idempotency-Key` header | the order `{id, reference, status, total_minor, currency, invoice_ref}` |
| `GET /api/orders` | `?page_size=&cursor=` | `{items, next_cursor, has_more}` of the caller's orders |
| `GET /api/orders/{id}` | one order for its owner | the order |
| `POST /api/devices` | `{product_id, serial}` | the registered device |
| `GET /api/devices` | the caller's devices | `{items}` |
| `POST /api/devices/{id}/flash` | `{version}` | the device with its new `firmware_version` |
| `GET /api/firmware` | `?product_id=` | firmware releases with notes |
| `GET /api/app-releases` | the companion releases | `{items}` |
| `POST /api/contact` | `{name, email, message}` and the decoy field | the submission, or a refusal |
| `GET /api/health` | readiness | `{ok: true}` |

Field names are exact. List endpoints return their rows under `items` with
`next_cursor` and `has_more`. Every business rule violation returns a client error
naming the reason, never a server error and never a silent success. Every account
scoped endpoint requires a valid bearer token; an anonymous caller to one is
rejected.

### No mocks

Orders, carts, devices and releases live in the real PostgreSQL at `DATABASE_URL`,
every order's invoice lives in real killbill at `PAYMENTS_API_URL`, and every
confirmation email is a real message in Mailpit at `SMTP_HOST`, and nowhere else.
An in memory list, a stubbed invoice, a logged-not-sent email, or a grid rendered
from client state that was never persisted is a contract violation. An order that
shows on screen but is absent from Postgres, or whose invoice is absent from
killbill, does not count. The named provider is the fact.

---

## Definition of done

The app is deployed and healthy. A stranger can read the founder letter over the
workshop film, add a camera to the cart, check out as a guest, and receive a
confirmation email, with exactly one invoice raised on the buyer's account for the
exact total and currency. Submitting the same checkout twice with one key places
exactly one order and raises no second invoice. A signed in customer registers a
camera by serial and flashes it to a newer firmware version, and no customer can
read or flash another account's device. Every total and count shown matches the
database, the invoice in killbill, and the message in Mailpit.
