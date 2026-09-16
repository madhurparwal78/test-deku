# Handsel

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, pick a tier on a product page, apply a discount code, pay, and land in a
library holding what they bought, without hitting an error page. A different
stranger, signed in as the other reader, must NOT be able to see that order or
that entitlement by any means, and must never see what the creator earned on it.
The purchase cannot be faked inside the app: the invoice must exist as a real
record in `killbill` for the exact amount and currency the app itself computed,
and the receipt must arrive as a real message in Mailpit addressed to the buying
reader alone. A row the app writes to its own tables while the billing platform
holds nothing is not a sale.

## Overview

Handsel is a merchant-of-record commerce product for exactly one independent
creator selling digital work. It has two faces. The **creator console** is the
working environment of a one-person business: the catalog, the orders, the
money, the discount codes and the pricing decomposition. The **buyer surfaces**
are a branded storefront, a product page, a checkout and a durable library, and
they are where the creator's customers discover, buy and keep the work.

The creator can make the thing in a week and lose the business to everything
around it. Files have to be delivered and re-delivered. Prices have to carry tax.
Money has to reconcile at the end of the month. Each of those is a job a company
hands to a person the creator does not have, so the ceiling on the business is
not how much they can make, it is how much administration each sale costs them.
Handsel exists to take that administration away. The problem it solves is
administrative rather than creative, and the goal is that its arithmetic is
right every time, because a creator who cannot trust the figures has to redo
the work by hand anyway.

One account, one creator, two audiences. The creator's records belong to the
account. A reader is scoped to their own purchases: they see no creator-side
figure and no order they did not place. That boundary is the product's
load-bearing fact and it is enforced on the server, never in the interface.

Handsel is the seller of record on every transaction. It is Handsel's legal
entity that contracts with the reader, and Handsel that is responsible for the
tax collected. That single fact is why every order carries a resolved
jurisdiction and rate, why the ledger holds a tax liability per jurisdiction, and
why the checkout and the receipt both name the selling entity alongside the
creator's brand.

What it deliberately is not: no memberships and no recurring billing, no refunds
or disputes, no payouts, no custom domains, no storefront design tool, no
marketplace search, no file uploads, no reviews, no affiliates, no broadcasts and
no automation engine. It sells a catalog of digital products once, to people who
keep them.

The genuinely hard part is that two records have to agree at the same instant.
The invoice in the billing platform has to carry the amount the app computed, and
the ledger entry for that same order has to balance, with a rounded tax figure
and a rounded payment fee inside it. An app that agrees with itself and disagrees
with the billing platform has not sold anything.

## User roles

| Role | Can do |
|---|---|
| `creator` | Own the catalog: raise, edit, publish and unpublish products and their tiers. Raise discount codes. Read every order with its full money decomposition. Read the chart of accounts, the entry stream and the trial balance. Read the pricing decomposition for any product. **Cannot buy anything, cannot hold an entitlement, cannot reach a reader's library, and cannot change a ledger entry once it is posted.** |
| `reader` | Browse published products, open a checkout, apply a discount code, confirm a purchase, read their own library, open an entitlement they hold, and read their own order with the reader-scoped decomposition. **Cannot see any creator-side figure, cannot see another reader's order or entitlement, and cannot reach any console route or any creator-only endpoint.** |

The permission table above is the whole of the authorization model, and it is
enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a `reader` session
to any `creator`-only endpoint must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged.

Signup is open. Anyone may create an account and it is always a `reader`; the
`creator` is seeded and cannot be created by signing up. A request for an order
or an entitlement the caller does not hold is answered as **absent**, not as
forbidden, because a refusal would disclose that the record exists.

Seeded accounts, every one with the password `deku-demo-pw-2026`:

| Email | Name | Role | Country |
|---|---|---|---|
| `creator@example.com` | `Marlowe Quill` | `creator` | `US` |
| `buyer@example.com` | `Ines Calder` | `reader` | `IE` |
| `buyer2@example.com` | `Tobias Renn` | `reader` | `US` |

## Core features

### Auth

1. Email and password, implemented by the app. Passwords are stored hashed,
   never reversibly.
2. `POST /api/auth/login` takes `email` and `password` and returns a bearer token
   under the key `access_token`. Every authenticated request carries it as
   `Authorization: Bearer <token>`.
3. `POST /api/auth/signup` takes `email`, `display_name`, `country` and
   `password` and creates a `reader`. An email already in use is refused and no
   second account is created.
4. `GET /api/me` returns the signed-in principal and its role.
5. A request with no token, or an expired one, to any authenticated route is
   denied and the protected state is unchanged.
6. The signup form carries an unattended decoy field named `company_website`.
   A submission arriving with that field filled is refused and nothing is
   written, and so is the same signup submitted repeatedly in quick succession.

### The catalog and the product page

1. `GET /api/storefront/products` lists every `published` product with its
   permalink, its name and its tiers. `GET
   /api/storefront/products/{permalink}` returns one, with every tier's `code`,
   `name` and `price_minor`. Both are public.
2. A `draft` product is not readable by a stranger at either endpoint, and its
   permalink does not resolve on the storefront.
3. A product that has been `unpublished` keeps its page, which renders a designed
   unavailable state offering the storefront rather than an error. A dead link in
   a creator's old post is a lost sale, not an error condition.
4. A permalink is human-legible, unique in the account, and may be changed freely
   until the product takes its first paid order. After that first paid order the
   permalink is fixed and an attempt to change it is refused.
5. `GET /api/products`, `POST /api/products`, `PATCH
   /api/products/{permalink}`, `POST /api/products/{permalink}/publish` and
   `POST /api/products/{permalink}/unpublish` are the creator's catalog
   surface. Each is denied to a reader.
6. Every storefront page carries its own title and description in the served
   HTML, and the price of a product is present in that HTML before any script
   runs. A product page that needs script to show its price is a failed page.

### Checkout

1. `POST /api/checkout/sessions` takes `permalink`, `tier_code`, `quantity`,
   `attribution_channel` and `idempotency_key`, and opens a session. It is the
   point at which the unit price, the resolved tax jurisdiction and the tax rate
   are **locked**. `GET /api/checkout/sessions/{session_id}` returns one.
2. `attribution_channel` is `direct` or `marketplace` and nothing else. It
   records who supplied the demand and it selects the platform fee tier.
3. The tax jurisdiction is the buying reader's country. `IE` is taxed at `1900`
   basis points and `US` at `0` basis points.
4. A session honours its locked figures for its whole life. If the creator
   reprices the tier while a session is open, the confirm still uses the price
   the session locked.
5. `POST /api/checkout/sessions/{session_id}/discounts` takes a `code` and
   applies it. The code is matched without regard to case. The discount is
   computed on the subtotal, and the tax is then re-resolved on the discounted
   base, so a discount reduces the tax as well as the price.
6. A code is refused, with the reason named and the session total unchanged,
   when its window has closed, when its total usage cap is exhausted, when this
   reader has already used it as many times as its per-reader cap allows, or when
   it is not a code in this account.
7. `POST /api/checkout/sessions/{session_id}/confirm` takes an
   `idempotency_key` and completes the purchase. Confirming a session twice with
   the same key produces exactly one order, one invoice, one entitlement, one
   ledger entry and one receipt, and returns the same order both times.
8. A confirm that cannot complete leaves nothing behind: no order, no invoice,
   no entitlement, no ledger entry and no mail.
9. The checkout surface carries the decomposition on demand and never a bare
   figure: the reader can see the unit price, the discount, the tax and the
   total as separate lines.
10. The checkout session endpoint also carries the `company_website` decoy
    field and refuses a submission that fills it.

### The money decomposition

1. Every order decomposes into `subtotal_minor`, `discount_minor`, `tax_minor`,
   `total_minor`, `platform_fee_minor`, `payment_fee_minor`,
   `affiliate_fee_minor` and `net_minor`.
2. `net_minor` is exactly `subtotal_minor` less `discount_minor`, less
   `platform_fee_minor`, less `payment_fee_minor`, less `affiliate_fee_minor`.
   This identity holds on every order. `affiliate_fee_minor` is always `0`.
3. `total_minor` is the subtotal less the discount, plus the tax.
4. The platform fee is two-tiered on the attribution channel, because what
   Handsel charges depends on who supplied the customer. On `direct` it is
   `1000` basis points of the discounted subtotal plus a fixed `30` minor units.
   On `marketplace` it is `2000` basis points of the discounted subtotal and no
   fixed component.
5. The payment fee is `290` basis points of the total plus a fixed `30` minor
   units. It is itemised separately from the platform fee on every order, so the
   creator can always see the difference between what Handsel charged and what
   moving the money cost.
6. Every step rounds half up to the nearest minor unit.
7. The worked case, which every other case follows: `buyer@example.com`, whose
   country is `IE`, buys `field-notes-vol-one` at tier `standard` for a
   subtotal of `2400`, on the `direct` channel, with the code `LAUNCH20`. The
   discount is `480`. The tax is `1900` basis points of `1920`, which is `365`.
   The total is `2285`. The platform fee is `1000` basis points of `1920` plus
   `30`, which is `222`. The payment fee is `290` basis points of `2285` plus
   `30`, which is `96`. The affiliate share is `0`. The net is `1602`.
8. The second worked case, on the other channel and a zero-rated jurisdiction:
   `buyer2@example.com`, whose country is `US`, buys the same tier on the
   `marketplace` channel with no code. The subtotal is `2400`, the discount is
   `0`, the tax is `0`, the total is `2400`, the platform fee is `480`, the
   payment fee is `100` and the net is `1820`.

### The ledger

1. Every financial fact is an immutable `ledger_entries` row with two or more
   balanced `ledger_postings` legs. Balances, earnings and the trial balance are
   **derived** from postings and are never stored as counters.
2. The chart of accounts is seeded and fixed: `1100` Provider receivable, an
   asset; `2000` Creator payable, a liability; `2100` Tax payable, a liability,
   held once per jurisdiction so there is a row for `IE` and a row for `US`;
   `4000` Platform fee revenue, a revenue account; and `5000` Payment
   processing expense, an expense account.
3. A paid order posts one entry. It debits `1100` by the order total, and
   credits `2100` for that order's jurisdiction by the tax, `4000` by the
   platform fee, `5000` by the payment fee and `2000` by the net.
4. For the worked case that entry is a debit of `2285` to `1100` against credits
   of `365` to `2100` for `IE`, `222` to `4000`, `96` to `5000` and `1602` to
   `2000`.
5. A leg worth nothing is not written at all, so the zero-rated case posts three
   credits rather than four.
6. **Within one entry the debit legs and the credit legs sum to the same amount,
   per currency.** An entry that would not balance is refused whole and never
   written in part.
7. **The trial balance is exactly zero per currency at all times.** `GET
   /api/ledger/trial-balance` returns it, and it reads zero after every order.
8. No account of type `liability` ever holds a negative balance.
9. A posted entry is never changed and never removed. `GET
   /api/ledger/accounts` and `GET /api/ledger/entries` are readable by the
   creator and denied to a reader.

### The billing record

1. The books Handsel keeps are its own; the record a buyer could be shown lives
   in `killbill`, already running at `PAYMENTS_API_URL`. Treat it as a
   subscription-billing platform rather than a card processor. There is no card
   here, no token, no decline and no test card: the objects are accounts,
   catalogue plans and invoices, and a brief that reaches past those three is
   describing a service this environment does not run.
2. Authentication is three parts on every `/1.0/kb/*` call, and all three are
   read from the environment rather than written down: HTTP Basic from
   `PAYMENTS_ADMIN_USER` with `PAYMENTS_ADMIN_PASSWORD`, an
   `X-Killbill-ApiKey` header from `PAYMENTS_API_KEY`, an `X-Killbill-ApiSecret`
   header from `PAYMENTS_API_SECRET`. Anything that writes adds
   `X-Killbill-CreatedBy` naming the writer. Liveness is
   `GET /1.0/healthcheck`, which takes no credentials; the similarly named
   `/1.0/kb/healthcheck` sits behind the tenant filter, answers unauthorized
   forever, and is never a probe.
3. **Exactly one billing account exists per reader.** Its identity is the
   `externalKey`, built as `handsel-` followed by that reader's display name in
   lowercase kebab-case, so `Ines Calder` resolves to `handsel-ines-calder` and
   `Tobias Renn` to `handsel-tobias-renn`. Read it back with
   `GET /1.0/kb/accounts?externalKey=<key>`: found means the account is there,
   not found means the key is free. Create with `POST /1.0/kb/accounts` carrying
   `name`, `externalKey`, `email`, `currency`, `country`.
4. **Uniqueness is the store's to enforce, not the app's.** The external key is
   unique inside the tenant, so a second create on a key already taken comes
   back refused from `killbill` itself. Do not guard it with a lookup in
   application code: two requests can pass the same lookup before either writes.
   Whatever the app does, `GET /1.0/kb/accounts/pagination` holds one account
   per reader.
5. **Exactly one invoice exists per paid order**, on that reader's billing
   account, carrying the order's `total_minor` in the order's currency and
   readable at `GET /1.0/kb/invoices/pagination`. Amounts come back there as a
   decimal with the currency upper-cased, so the worked case's `2285` minor
   units reads as `22.85` against `USD`.
6. An order is complete only once that invoice exists. Handsel's own tables
   report what the billing platform holds; they never stand in for it.

### Entitlement, library and the receipt

1. A paid order grants one entitlement, for the product and tier that were
   bought. `GET /api/library` returns every entitlement the signed-in reader
   holds and no other reader's.
2. **The entitlement is the source of truth for access; the receipt is a
   convenience.** A reader whose receipt never arrived still has full library
   access.
3. `POST /api/library/entitlements/{entitlement_id}/access` records the access
   and returns the deliverable. `GET
   /api/library/orders/{order_number}` returns one order in the reader-scoped
   form.
4. Unpublishing a product does **not** revoke an entitlement already granted.
   Nothing in this product revokes one: an entitlement granted by a paid order
   stands for as long as the reader's account does.
5. The receipt is addressed to the buying reader's email address, with no cc and
   no bcc. Its subject begins with `Handsel receipt: ` followed by the product
   name, so a `Field Notes Volume One` receipt reads `Handsel receipt: Field
   Notes Volume One`. The body is not empty and names the product, the tier and
   the total paid.
6. **The non-transition rule:** a refused discount, a refused confirm, a sold-out
   confirm, a product being published, a product being unpublished and a library
   read all send no mail at all. Only a paid order sends a receipt, and it sends
   exactly one.

### The contention rule

1. `lantern-press-kit` has exactly one unit. A product carrying a quantity limit
   never sells more units than it has.
2. **Two readers confirming the last unit at the same moment produce exactly one
   order.** One reader gets the order, the invoice, the entitlement, the ledger
   entry and the receipt. The other is told the product is sold out and offered
   the storefront, and nothing is written for them anywhere: no order, no
   invoice, no entitlement, no ledger entry and no mail. This must hold under
   real simultaneous requests.

### The pricing decomposition

1. `GET /api/pricing/{permalink}` takes `tier_code`, `discount_bps`,
   `attribution_channel` and `tax_jurisdiction`, and returns the same eight
   figures an order carries.
2. **It is the same arithmetic the ledger uses, to the minor unit.** The figures
   it returns for a given set of parameters are the figures the order would
   carry. A pricing surface that disagrees with the books by one minor unit is
   worse than no pricing surface, because it teaches the creator to distrust
   their own accounts.
3. Asked for `field-notes-vol-one` at tier `standard`, a discount depth of
   `2000` basis points, jurisdiction `IE` and channel `direct`, it returns the
   worked case above and a net of `1602`. Asked for the same with channel
   `marketplace`, the platform fee is `384` and the net is `1440`.
4. When a parameter change moves the net, the surface **names the component that
   moved** and by how much, and never presents the moved total alone. Moving the
   worked case to `marketplace` falls by `162` and the surface attributes that
   fall to the platform fee. A creator who cannot see why the net fell has been
   shown a number rather than given an instrument.

### Audience isolation

1. A reader-facing order response carries `subtotal_minor`, `discount_minor`,
   `tax_minor` and `total_minor` and nothing else of the money. It carries no
   `platform_fee_minor`, no `payment_fee_minor`, no `affiliate_fee_minor` and no
   `net_minor`.
2. A reader asking for an order or an entitlement belonging to another reader is
   answered as absent.
3. A reader reaching `GET /api/orders`, `GET /api/ledger/entries`, `GET
   /api/ledger/trial-balance`, `GET /api/pricing/{permalink}`, `POST
   /api/products` or `POST /api/discount-codes` is denied, and the protected
   state is unchanged.
4. The creator holds no entitlements and reaches no reader's library.

### Discount codes

1. `GET /api/discount-codes` and `POST /api/discount-codes` are the creator's
   surface, and both are denied to a reader. A code carries a `code`, a
   `value_bps`, a `max_uses`, a `max_per_reader`, a `starts_at` and an
   `ends_at`.
2. `LAUNCH20` is seeded at `2000` basis points with a total cap of `5` uses and
   a per-reader cap of `1`, inside its window. `EXPIRED10` is seeded at `1000`
   basis points with its window already closed.
3. A code whose window has already closed is refused when it is raised as well
   as when it is applied, and a depth that would take a total below zero is
   refused.

### The terms page and the surfaces every page owes

1. A terms page at `/terms` is reachable from the footer of every page and is
   linked from the signup form. It states what the product stores and it names
   the seller of record, `Handsel Commerce Ltd`, alongside the creator's brand.
   That disclosure is mandatory and cannot be suppressed by branding, because a
   reader is entitled to know who they contracted with. The same disclosure
   appears at checkout and on the receipt.
2. Every form rejects invalid input inline, names the field that was wrong, and
   writes nothing when it does.
3. An unknown address renders the product's own not-found page, with a way back,
   and answers not-found.
4. Every list has an empty state naming the next concrete action. A blank region
   is a defect.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Storefront home: every published product | public |
| `/p/{permalink}` | Product page: tiers, prices, the buy action | public |
| `/terms` | Terms, and the seller-of-record disclosure | public |
| `/login` | Sign in | public |
| `/signup` | Open signup, which creates a reader | public |
| `/checkout/{session_id}` | One open checkout session | session-bound |
| `/thanks/{order_number}` | Immediate access and the receipt summary | reader |
| `/library` | Every entitlement this reader holds | reader |
| `/library/orders/{order_number}` | One order, reader-scoped decomposition | reader |
| `/console` | Creator home: what sold and what it netted | creator |
| `/console/products` | The catalog beside the selected product | creator |
| `/console/products/{permalink}` | The same surface with one product selected | creator |
| `/console/orders` | The order list beside the selected order | creator |
| `/console/orders/{order_number}` | The same surface with one order selected | creator |
| `/console/money` | The chart of accounts beside the entry stream | creator |
| `/console/discounts` | Discount codes | creator |
| `/console/pricing/{permalink}` | The pricing decomposition for one product | creator |

### Entry and redirects

- An unauthenticated request for a reader route or a console route goes to
  `/login`, and after a successful sign-in lands on the route that was asked
  for.
- A reader signing in with no destination lands on `/library`. The creator lands
  on `/console`.
- Signing out returns to `/` and ends the session; going back does not restore
  it.
- A reader session reaching any `/console` route, or any creator-only endpoint by
  direct call, is denied by the server and the protected state is unchanged.
- A creator session reaching `/library` is denied the same way.
- A token that expires part way through an action leaves the action undone and
  returns to `/login` with the reason stated.
- A request for an order or an entitlement the caller does not hold is answered
  as absent rather than as forbidden.

### Journeys

1. **A stranger buys.** Open `/p/field-notes-vol-one` cold. The page already
   carries the name `Field Notes Volume One`, the tier `Standard` and its price.
   Pick `Standard`, press the buy action, sign in as `buyer@example.com` with
   `deku-demo-pw-2026`, and land back on `/checkout/{session_id}`. The unit
   price, the tax resolved for `IE` and the total are shown as separate lines.
   Apply `LAUNCH20`: the discount line appears, the tax is re-resolved on the
   discounted base, and the total becomes `2285`. Confirm.
   `/thanks/HS-00001` shows the order and a way into the library, and the
   receipt arrives for `buyer@example.com` alone.
2. **The reader comes back.** Sign in as `buyer@example.com` and open
   `/library`. The entitlement for `Field Notes Volume One` is listed with its
   tier. Open it, and the access is recorded. Open
   `/library/orders/HS-00001` and see the subtotal, the discount, the tax and
   the total, and no other figure.
3. **The creator publishes.** Sign in as `creator@example.com` and open
   `/console/products`. Raise a new product from the modal with a name and a
   permalink; it lands as a draft, selected in the right column. Add a tier and
   a price, then publish it. The storefront home now lists it.
4. **The creator reads the money.** Open `/console/orders` and select
   `HS-00001`. The right column carries the full decomposition down to the net
   of `1602`. Open `/console/money`: the account tree lists the seeded accounts,
   the entry stream carries that order's entry, expanding it shows its legs, and
   the trial balance reads zero.
5. **The creator prices.** Open `/console/pricing/field-notes-vol-one`, set the
   depth to `2000` basis points and the jurisdiction to `IE` on the `direct`
   channel, and the net reads `1602`. Move to `marketplace` and the net falls to
   `1440`, with the platform fee named as the component that moved.
6. **The last unit.** `lantern-press-kit` has one unit and two readers confirm
   at the same moment. One order exists and one invoice exists; the other reader
   is told it is sold out.
7. **A refused code.** Apply `EXPIRED10` at checkout. It is refused, the reason
   names the closed window, and the total is unchanged.

### States

Every list has an empty state that names the next concrete action, never a blank
region: an empty catalog, an empty order list, an empty library, an empty entry
stream. Every page has a loading state whose placeholder occupies the space the
content will occupy, so nothing jumps when the content arrives. An unknown
address renders the product's own not-found page with a way back. An unpublished
product renders a designed unavailable state offering the storefront. Errors are
stated in place and never leave the app unusable.

## UI/UX notes

The north star is comprehension on both sides. A stranger should understand, in
the first moment on a product page, what they are buying and exactly what it will
cost them; a creator should understand, in the first moment in the console, what
sold and what it netted. The product sells other people's work and must never
look like it is selling itself.

The register is split, deliberately. The buyer surfaces carry craft, because that
is where the creator's credibility is won. The console carries density, because
speed of work decides how much one person can carry. Both are drawn from one set
of tokens.

**Palette by role.** The page ground is a near-white warm neutral; a raised
surface sits a shade lighter and a sunk surface a shade darker. Primary text is a
near-black neutral, and muted text is that same hue held lighter, used for labels
and never for a figure. The primary action wears a mid, vivid orange, and it is
the only thing on a page wearing it. Revenue and success carry a mid, vivid
green; anything declined or lost carries a mid, vivid red; a caution carries a
light, vivid amber; something still in progress carries a mid, muted blue. Each
of those four means one thing and is used for nothing else. The money
decomposition carries its own ordered ramp, one distinguishable colour for each
of gross, discount, platform fee, payment fee, tax, affiliate share and net, and
every segment carries a written label as well as its colour. Every semantic
colour ships with a foreground that holds WCAG AA contrast against it; a colour
without that pair is incomplete. The exact shades are yours, so long as they hold
those role rules and that bar.

Dark mode is optional. If it ships, it redefines the ground tokens only and never
a component rule, and the brand lightens as the page darkens so contrast holds.

**Type.** The typography is two families, and the split is functional rather
than decorative. A
variable grotesque carries interface and storefront text. A monospace carries
money, order numbers and identifiers. Every numeric context uses tabular figures,
so a column of amounts does not jitter while it changes. Body text is `16px` on a
`24px` line, interface text `14px` on `20px`, a section heading `24px`, a page
heading `32px`, a storefront hero heading `48px`, and small print `12px`. The
storefront may take a creator-supplied display face in place of the grotesque;
the monospace is never overridable, because money legibility is a correctness
concern rather than a branding one.

**Shape and density.** Corners are softened rather than round, with the same
softness on every surface. Elevation has four levels and no more, and a raised
surface separates from the page by its shadow rather than by a border wherever it
can. The console is compact, so a full order list fits one screen. The buyer
surfaces are spacious, so the product and its price have room and sections read
as separate at a glance without needing a dividing line.

**Motion.** The character is eased: entrances and exits carry a considered ease,
so movement reads as a designed interface rather than as a machine responding.
Four rules govern it and each is a requirement rather than a taste. Money does
not bounce: no overshoot and no elastic easing on a monetary figure, a total, or
any control on the buy path, because overshoot on a price reads as instability.
Nothing on the checkout surface may delay input, move a target after it has
appeared, or animate a total, since motion at the point of payment is risk rather
than craft. Where one thing causes another, the second begins its transition at
the first's position. Anything in flight is interruptible: a transition
re-triggered or reversed part way through re-targets from where it is, and never
restarts from its origin or snaps. The named moments a person can see are these four. A
skeleton whose blocks occupy the space the content will occupy ends by
settling into that content. A changed figure arrives by
counting to its new value. A filtered list reorders by
sliding its rows to their new positions. A confirmed purchase arrives as
one settled state, rather than as a sequence of flashes. Reduced motion is honoured throughout, and it removes the movement rather
than the information: a figure still arrives at its value and a list still shows
its new order.

**Components.** Every interactive component carries all seven states: resting,
pointed at, pressed, focused, unavailable, loading and errored. A loading control
keeps its width so nothing beside it moves. A destructive control confirms first
and names what it will destroy. Unavailable is never signalled by colour alone.
Each page leads with one clear primary action, visually distinct from every
secondary one on that page. Every money figure is rendered with its currency
written out, at full precision, in tabular figures.

**Accessibility, and these are contract rather than taste.** WCAG 2.2 Level AA
across every surface, with effects active. Every content image carries
alternative text, and a decorative image declares itself decorative. Touch
targets are comfortably sized and anything on the buy path is larger still. Full
keyboard navigation with a visible focus ring on every interactive element.
Icon-only controls carry labels. Meaning is never carried by colour alone: the
money ramp, the ledger direction and every status all carry a word or a glyph
beside the colour.

**Responsive.** The layout holds at every width between a narrow phone and a wide
desktop, not only at the named tiers. At a narrow viewport nothing overflows
sideways and every navigation target stays reachable. The console rail collapses
to icons at medium widths and becomes a bottom bar at narrow ones, and a console
split pane becomes a list and then a detail. The product page becomes a single
column with the buy action pinned to the foot of the viewport. Checkout is a
single column at every width.

**What it must not look like.** A storefront that reads as one wash of a single
hue, with nothing but that hue to separate a success from a refusal, has lost
the only signal a buyer needs. Ornament standing where content belongs is the
second failure, and the third is an editorial composition dropped onto a working
surface: the console is somewhere a person does the same job forty times a week,
so an oversized hero in it is a defect rather than a flourish. Checkout is the
strictest of the three. Nothing there is asked to be interesting.

## Front-end specification

The console carries a persistent left rail with seven destinations: home,
products, orders, money, discounts, pricing and sign out. The rail is the only
console chrome. Every console working route is a split detail pane: the list
holds the left column, the selected record holds the right, and selecting a
record changes the right column and the address without losing the left.

The buyer surfaces carry no application chrome at all. A branded header, the
page, and a footer that links the terms page from every route.

Raising a new product and raising a new discount code each open a modal over
their list, and each returns to the list with the new record selected.

Every confirmation and every refusal appears as a
banner at the top of the working pane. A banner names what happened and, when something was refused, why
and what to do next. It persists until it is dismissed or the pane changes. A
message that disappears on its own cannot carry a reason a person needs to act
on.

The product page shows a gallery placeholder, the title, the price block, the
tier selector and the buy action, then the creator's block. The price block
states the currency explicitly beside every figure. The buy action is reachable
by keyboard within a short run of tab stops from the start of the document on
every width.

Checkout is a single column of at most four fields: email, the optional discount
code, the decoy field, and the confirm control. The total decomposes on demand
into the unit price, the discount and the tax. It never shows a bare number.

The ledger surface renders debit and credit distinguishably without colour, and
every entry expands to show its legs with the account code and name on each.

Iconography is drawn inline rather than loaded as a font, because an icon font breaks
under a font swap and in assistive technology. A decorative icon is hidden from
assistive technology and a meaningful one carries a label beside it.

Creator branding controls presentation only. It never alters the money
decomposition ramp, the meaning of the success and failure colours, the focus
ring's contrast, the monospace family, or the contrast of any control on the
checkout surface. Branding controls how the product looks, never what it means,
and never the surface where money is taken.

## Technical requirements

The server produces the HTML for every route, so a stranger landing on a product
page from a link receives the product name, its tier prices and the buy action in
the first response, before any script runs. Interaction is layered over that
document rather than replacing it.

Backend: Django with its own template layer. Frontend: Alpine.js over those
server-rendered templates. Datastore: PostgreSQL, reached at `DATABASE_URL`.
Billing: `killbill`, reached at `PAYMENTS_API_URL`. Mail: Mailpit over real SMTP,
reached at `SMTP_HOST` and `SMTP_PORT` with `SMTP_USER` and `SMTP_PASS`. Auth is
app-implemented email and password with bearer tokens. `GET /api/health` returns
`200` once the app is ready.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor: the only backing services available in this environment are
PostgreSQL, `killbill` and Mailpit, and reaching for anything else is a contract
violation.

All money is an integer count of minor units with a currency code beside it. No
monetary value is ever held as a floating-point number anywhere in the system,
including on the pricing decomposition surface, which rounds to minor units
before it returns. Rounding is half up at every step.

Security: passwords are stored hashed and are never recoverable, and no
credential, API key or admin token appears in anything the browser downloads.

There are three third-party integrations and only three, and each is reached at
its own environment variables: the datastore, the billing platform and the mail
server named above.

Every mutating request accepts an idempotency key and a replay with the same key
returns the stored outcome rather than performing the work a second time.

## Data model

Sixteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account
so a grader can sign in.

Seeding is idempotent: restarting the app creates no second copy of any seeded
row.

### `accounts`

`handle`, unique; `display_name`; `payout_currency`; `fee_schedule_version`;
`mor_entity`. Exactly one row: handle `marlowe-quill`, display name
`Marlowe Quill`, payout currency `usd`, fee schedule version `1`, seller of
record `Handsel Commerce Ltd`.

### `users`

`email`, unique; `display_name`; `role`, which is `creator` or `reader`;
`country`; `password_hash`; `created_at`. Seeded with the three accounts in
`## User roles`.

### `products`

`account_id`; `permalink`, unique per account; `name`; `state`, which is
`draft`, `published` or `unpublished`; `description`; `quantity_limit`, absent
when the product is unlimited; `quantity_sold`; `first_paid_at`;
`published_at`. Seeded with `field-notes-vol-one` named `Field Notes Volume One`
and published; `lantern-press-kit` named `Lantern Press Kit`, published, with a
quantity limit of `1` and nothing sold; and `tide-tables-draft` named
`Tide Tables Draft`, still a draft.

### `tiers`

`product_id`; `code`, unique per product; `name`; `price_minor`; `currency`;
`position`; `deliverable`. Seeded: `field-notes-vol-one` carries `standard`
named `Standard` at `2400` and `studio` named `Studio` at `5600`;
`lantern-press-kit` carries `standard` named `Standard` at `1000`;
`tide-tables-draft` carries `standard` named `Standard` at `1800`.

### `discount_codes`

`account_id`; `code`, unique per account and compared without regard to case;
`kind`, which is `percent`; `value_bps`; `max_uses`; `use_count`;
`max_per_reader`; `starts_at`; `ends_at`. Seeded with `LAUNCH20` and
`EXPIRED10` as described in `## Core features`.

### `fee_schedules`

`version`; `channel`, which is `direct` or `marketplace`; `rate_bps`;
`fixed_minor`. Unique on version and channel together. Seeded at version `1`
with `direct` at `1000` and `30`, and `marketplace` at `2000` and `0`.

### `tax_rates`

`jurisdiction`, unique; `rate_bps`. Seeded with `IE` at `1900` and `US` at `0`.

### `checkout_sessions`

`reader_id`; `product_id`; `tier_id`; `quantity`; `state`, which is `open`,
`confirmed`, `refused` or `expired`; `locked_unit_price_minor`; `currency`;
`discount_code_id`; `discount_minor`; `tax_jurisdiction`; `tax_rate_bps`;
`tax_minor`; `subtotal_minor`; `total_minor`; `attribution_channel`;
`idempotency_key`; `expires_at`. The locked price, the jurisdiction and the rate
are written when the session opens and are not recomputed afterwards.

### `orders`

`account_id`; `reader_id`; `checkout_session_id`; `number`, unique per account;
`state`; `currency`; `subtotal_minor`; `discount_minor`; `tax_minor`;
`total_minor`; `platform_fee_minor`; `payment_fee_minor`;
`affiliate_fee_minor`; `net_minor`; `attribution_channel`;
`fee_schedule_version`; `idempotency_key`, unique per account; `placed_at`.
The order number is `HS-` followed by five digits, counted per account from
`HS-00001`.

### `billing_accounts`

`user_id`; `external_key`, unique; `currency`; `created_at`.

### `invoices`

`order_id`, unique; `external_key`; `amount_minor`; `currency`; `provider_ref`.

### `entitlements`

`order_id`; `reader_id`; `product_id`; `tier_id`; `state`, which is `active` or
`revoked`; `granted_at`; `revoked_at`; `revoke_reason`. Unique on the order, the
product and the tier together.

### `access_events`

`entitlement_id`; `occurred_at`.

### `ledger_accounts`

`account_id`; `code`; `name`; `type`, which is `asset`, `liability`, `revenue`
or `expense`; `currency`; `jurisdiction`. Unique on the account, the code, the
currency and the jurisdiction together. Seeded with the chart of accounts in
`## Core features`.

### `ledger_entries`

`account_id`; `occurred_at`; `description`; `source_type`; `source_id`;
`idempotency_key`, unique per account; `reverses_entry_id`. A row here is never
updated and never deleted; a correction is a new entry that points at the one it
reverses.

### `ledger_postings`

`entry_id`; `ledger_account_id`; `direction`, which is `debit` or `credit`;
`amount_minor`; `currency`. Every amount is greater than zero, so a leg worth
nothing is not written.

Derived rather than stored: every balance, the creator's earnings and the trial
balance are computed from `ledger_postings` and are held in no counter anywhere.

## Constraints

- One creator account and one catalog. There is no second creator, no
  organization, no team and no delegated administration.
- No memberships, no recurring billing, no dunning and no tier-gated content.
- No refunds, no disputes and no chargebacks.
- No payouts, no tax filing and no held funds. The creator's payable accrues and
  is readable; nothing settles it.
- No custom domains and no certificates. The app serves the hostname it is given.
- No storefront design tool, no live collaboration and no multiplayer presence.
- No provenance watermarking, no leak matching and no cohort analysis.
- No audience records, no segments, no broadcasts and no automation engine.
- No marketplace browse and no search. The attribution channel is carried on the
  checkout session and nothing else of the marketplace exists.
- No file upload, no media processing and no object storage. A tier's deliverable
  is a record, not a file.
- No reviews and no ratings. The product carries no review surface, so nothing in
  it can be edited by the seller.
- No affiliate portal. The affiliate share stays on every order as a figure and
  is always zero.
- No collaborators, no webhooks, no public API keys and no audit export.
- One currency. There is no presentment currency, no purchasing-power adjustment
  and no exchange rate.
- One interface language.
- No native application.
- No external network call at runtime beyond PostgreSQL, `killbill` and Mailpit.
- The app stays responsive with three seeded products, two seeded readers and the
  orders one session produces. Nothing here needs pagination.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` where `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of
  the shell. An ordinary background job dies with its shell, and the app will not
  be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy
  of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `display_name`, `country`, `password`, `company_website` | the created reader |
| `POST /api/auth/login` | `email`, `password` | `access_token` |
| `GET /api/me` | | the signed-in principal and its role |
| `GET /api/storefront/products` | | a top-level array of published products |
| `GET /api/storefront/products/{permalink}` | | one product with its tiers |
| `POST /api/checkout/sessions` | `permalink`, `tier_code`, `quantity`, `attribution_channel`, `idempotency_key`, `company_website` | the session with its locked figures |
| `GET /api/checkout/sessions/{session_id}` | | the session |
| `POST /api/checkout/sessions/{session_id}/discounts` | `code` | the session with the discount and the re-resolved tax |
| `POST /api/checkout/sessions/{session_id}/confirm` | `idempotency_key` | the order and its entitlement |
| `GET /api/library` | | a top-level array of this reader's entitlements |
| `POST /api/library/entitlements/{entitlement_id}/access` | | the deliverable |
| `GET /api/library/orders/{order_number}` | | one order, reader-scoped |
| `GET /api/products` | | a top-level array of the creator's products |
| `POST /api/products` | `name`, `permalink` | the created product |
| `PATCH /api/products/{permalink}` | any editable field | the product |
| `POST /api/products/{permalink}/publish` | | the product |
| `POST /api/products/{permalink}/unpublish` | | the product |
| `GET /api/orders` | | a top-level array of orders with the full decomposition |
| `GET /api/orders/{order_number}` | | one order with the full decomposition |
| `GET /api/discount-codes` | | a top-level array of codes |
| `POST /api/discount-codes` | `code`, `value_bps`, `max_uses`, `max_per_reader`, `starts_at`, `ends_at` | the created code |
| `GET /api/ledger/accounts` | | a top-level array of ledger accounts |
| `GET /api/ledger/entries` | | a top-level array of entries with their legs |
| `GET /api/ledger/trial-balance` | | the balance per currency |
| `GET /api/pricing/{permalink}` | `tier_code`, `discount_bps`, `attribution_channel`, `tax_jurisdiction` | the eight figures |
| `GET /api/health` | | `200` |

Field names are exact. A list endpoint returns a top-level JSON array. A
successful call returns the named resource or shape; an invalid or unauthorized
call is rejected as a client error, never as a server error and never as a silent
success. Bearer auth is carried on everything except login, signup, health, the
public storefront reads and the terms page.

### No mocks

An in-memory list of invoices, a hardcoded success response the app returns to
itself, a receipt written to a log file instead of sent over SMTP, an order row
written with no invoice in `killbill`, and a billing account the app records
locally but never creates in the tenant are each a violation. The named provider
is the fact: the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.

## Definition of done

A stranger can open a product page on a phone, pick a tier, apply a discount code,
pay, and reach what they bought in a library that still works when they come
back. Every paid order carries one invoice in the billing platform for the amount
the app computed, one receipt to the buyer alone, and one balanced ledger entry,
and the trial balance reads zero afterwards. Two readers confirming the last unit
of a limited product produce exactly one order between them. A reader never sees
what the creator earned, and never sees an order they did not place.
