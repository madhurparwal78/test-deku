# Travel Luggage Storefront

Build and deploy a working web application from this brief. There is no starting codebase. When you
are done, a stranger must be able to open the app in a browser, find a suitcase by size or by
collection, choose a colourway, add it to the cart at its sale price and place an order that takes
the stock down and sends a confirmation email, without hitting an error page. Two shoppers placing
orders for the last unit of one colourway at the same moment must NOT both end up with a paid order
by any means, and the stock of that colourway must never read below zero. Every paid order must name
a billing account that exists as a real record in `killbill`; an order the app merely marks as paid
does not count. The confirmation must be a real email delivered to the shopper's inbox in Mailpit; a
message the app only shows on screen does not count.

## Overview

valisette is the direct-to-consumer storefront of a travel goods brand that designs and sells its
own luggage, backpacks, briefcases, totes, slings, accessories and wallets. One brand owns every item
in the catalogue: there are no other sellers, no listings from outside the business, no bidding and
no marketplace. The wordmark is the brand name in lower case, `valisette`, and it is written that way
everywhere.

The catalogue is organised on two independent axes that cross each other: a size axis (cabin,
check-in, check-in large, trunk, kids and sets) and a collection axis of six named lines (Passage,
Meridian, Coastal, Contour, Ridge and Solstice). A shopper can enter from either axis and land in the
same wall of product cards. Every product exists in several colourways, and each colourway has its
own stock, its own drawn pictures and its own price.

Three commercial mechanics carry the product, and all three are real. A running sale, `Road Week`,
whose discount is arithmetic between two stored prices rather than a badge painted on a card. A cart
that survives the session, and a checkout that opens a billing account at the payments provider,
takes the stock down for exactly the colourways bought and sends a confirmation email. And stock that
can never go negative, including when two shoppers buy the last unit at the same instant. Around
those sit the reading surfaces: a home page that merchandises collections and bestsellers, collection
pages with sorting and filtering, product pages deep enough to answer every question before buying, a
directory of physical stores, a search, standing policy pages and an account area.

It deliberately is not a marketplace, an auction, a review site, a live chat, a subscription service
or a loyalty scheme, and personalisation is recorded as initials and a placement rather than drawn as
a preview. The genuinely hard part is that money and stock must agree under pressure: the price
charged is the price in force at checkout, a repeated submission of one checkout produces one order,
and the last unit of a colourway is sold exactly once.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| visitor, signed out | Browse, search, filter and sort; open products; keep a cart; check out as a guest; find stores; subscribe to the newsletter; check a gift card balance | **Cannot** open any signed-in `/account` route, read any order, or call any owner endpoint |
| `customer` | Everything a visitor can, plus keep a cart attached to the account, save delivery addresses, and read the account's own orders | **Cannot** read another account's orders or addresses, and **cannot** call any owner endpoint |
| `owner` | Everything a customer can, plus rename, reprice and delist products and colourways, record stock movements, move the end of the running sale, and list, fulfil and cancel any order | **Cannot** edit or delete a stock movement once written, and **cannot** move an order out of `cancelled` or `fulfilled` |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `customer` session to any `owner`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected state
unchanged. The same holds for a signed-out caller on any guarded endpoint, and for one customer
reaching for another customer's orders or addresses.

Signup is open: every account created at `/account/register` is a `customer`, and no request body,
form field or header can choose or change a role. The only `owner` is the seeded one.

Seeded accounts, every one of them using the password `deku-demo-pw-2026`:

| Email | Role | Name | Seeded state |
|---|---|---|---|
| `owner@example.com` | owner | Kiran Rao | no orders, no addresses |
| `customer@example.com` | customer | Aarav Mehta | one default address; orders `VS-100001` and `VS-100002` |
| `customer2@example.com` | customer | Noor Haddad | order `VS-100003`; no saved address |

## Core features

### Accounts and sessions

valisette runs its own sign-in with an email address and a password. Only a slow salted hash of each
password is kept, no response ever carries a password or its hash, and every signed-in call to the
API carries the bearer token that sign-in handed back.

1. `POST /api/auth/signup` with `name`, `email` and `password` creates a `customer` and returns an
   `access_token`. Emails are stored lowercased and are unique: a second signup with an address
   already in use, in any letter case, is rejected as invalid and creates nothing. A password
   shorter than ten characters is rejected as invalid and creates nothing.
2. `POST /api/auth/login` with `email`, `password` and an optional `remember` flag returns an
   `access_token`, the account's `role` and `expires_at`. A token issued without `remember` expires
   twelve hours after sign-in; with `remember` set to true it expires thirty days after sign-in.
3. A wrong password and an unknown email are refused with the same status and the same body, whose
   `message` is `That email and password do not match.`, so the answer never tells which of the two
   was wrong.
4. `POST /api/auth/logout` ends the session, and the same token is turned away by every guarded
   endpoint afterwards.
5. Every guarded endpoint turns away a call that arrives without a token, or with a token the app
   never issued, and whatever that call tried to change stays as it was.
6. A signup body that names a `role` still creates a `customer`.
7. `POST /api/auth/recover` with an `email` always answers with the same status and the same
   `message`, `If we know that address, a reset link is on its way.`, whether or not the address has
   an account. For an address that has an account, the app sends one email to that address whose
   subject is exactly `Reset your valisette password` and whose body opens with the reset link,
   `<APP_PUBLIC_URL>/account/reset/<token>`. For an unknown address it sends nothing.
8. `POST /api/auth/reset` with that `token` and a new `password` of ten characters or more replaces
   the password: the new password signs in and the old one no longer does. A reset token works once;
   a used or unknown token is rejected as invalid and changes nothing.
9. `GET /api/me` returns the signed-in account's `name`, `email` and `role`.

### The catalogue

Every product belongs to exactly one category and to at most one of the six lines. A luggage product
also carries exactly one size class, and a bag carries exactly one bag type. Each product exists in
one or more colourways. A colourway is not a separate product: it is a variant of one product,
identified by its `sku`, carrying its own stock, its own drawn pictures, its own price and its own
list price.

The colourways, with the code that ends every `sku` and the colour family the colour filter matches:

| Colourway | Code | Family |
|---|---|---|
| `Field Olive` | `OLV` | `green` |
| `Night Shift` | `NSH` | `black` |
| `Deep End Blue` | `DEB` | `blue` |
| `Salt Flat` | `SFL` | `white` |
| `Slow Sunday` | `SSU` | `beige` |
| `Corner Shop Pink` | `CSP` | `pink` |
| `Hold The Grey` | `HTG` | `grey` |
| `Static Blue` | `STB` | `blue` |
| `Cloud Cover` | `CCV` | `grey` |
| `Fast Lane Amber` | `FLA` | `yellow` |
| `Home Turf Amber` | `HTA` | `yellow` |
| `Long Way Round` | `LWR` | `beige` |
| `Coastal Mist` | `CMI` | `grey` |

Each colourway's swatch colour is stored as a `#RRGGBB` string and reads as its family: an olive
reads green, an amber reads yellow, and `Salt Flat` is a near-white.

The products, in `position` order. A colourway's `sku` is the product's SKU prefix, a hyphen and the
colourway code, so `PSG-CAB` in `Field Olive` is `PSG-CAB-OLV`. Prices are integer cents in `usd`:
`17900` is `$179`, not `179` and not `179.00`. Unless stated below the table, every colourway of a
product carries the product's price and list price and holds 20 units.

| # | Handle | Title | Category | Line | Size class or bag type | Uses | Tags | Badge | Price | List price | Units sold | Launched | SKU prefix | Colourways, in order |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `passage-luggage-cabin` | Passage Luggage - Cabin | `luggage` | Passage | `cabin` | travel | - | hot | 17900 | 29900 | 940 | 2026-03-02 | `PSG-CAB` | OLV, NSH, DEB, SFL, SSU, CSP |
| 2 | `passage-luggage-medium` | Passage Luggage - Medium | `luggage` | Passage | `check-in` | travel | - | - | 22900 | 37900 | 610 | 2026-03-02 | `PSG-MED` | OLV, NSH, DEB |
| 3 | `passage-luggage-large` | Passage Luggage - Large | `luggage` | Passage | `check-in-large` | travel | - | - | 25900 | 42900 | 380 | 2026-03-02 | `PSG-LRG` | OLV, NSH |
| 4 | `passage-luggage-set-of-3` | Passage Luggage - Set of 3 | `luggage` | Passage | `set` | travel | - | must-have | 59900 | 109900 | 520 | 2026-03-09 | `PSG-SET` | NSH, OLV |
| 5 | `meridian-luggage-cabin` | Meridian Luggage - Cabin | `luggage` | Meridian | `cabin` | travel | - | - | 17900 | 29900 | 870 | 2026-05-18 | `MRD-CAB` | HTG, STB, CCV, FLA, HTA, LWR, NSH |
| 6 | `meridian-luggage-medium` | Meridian Luggage - Medium | `luggage` | Meridian | `check-in` | travel | - | - | 22900 | 37900 | 450 | 2026-05-18 | `MRD-MED` | HTG, STB, CCV |
| 7 | `meridian-luggage-large` | Meridian Luggage - Large | `luggage` | Meridian | `check-in-large` | travel | - | - | 25900 | 42900 | 300 | 2026-05-18 | `MRD-LRG` | HTG, CCV |
| 8 | `meridian-luggage-set-of-3` | Meridian Luggage - Set of 3 | `luggage` | Meridian | `set` | travel | - | - | 59900 | 109900 | 260 | 2026-05-25 | `MRD-SET` | HTG, STB |
| 9 | `coastal-luggage-cabin` | Coastal Luggage - Cabin | `luggage` | Coastal | `cabin` | travel | - | hot | 17900 | 29900 | 790 | 2026-01-12 | `CST-CAB` | DEB, SFL, NSH |
| 10 | `coastal-luggage-medium` | Coastal Luggage - Medium | `luggage` | Coastal | `check-in` | travel | - | - | 22900 | 37900 | 330 | 2026-01-12 | `CST-MED` | DEB, SFL |
| 11 | `coastal-luggage-large` | Coastal Luggage - Large | `luggage` | Coastal | `check-in-large` | travel | - | - | 25900 | 42900 | 210 | 2026-01-12 | `CST-LRG` | DEB, NSH |
| 12 | `contour-luggage-cabin` | Contour Luggage - Cabin | `luggage` | Contour | `cabin` | travel | clearance | - | 17900 | 29900 | 240 | 2025-09-01 | `CTR-CAB` | FLA, CSP, NSH |
| 13 | `contour-luggage-medium` | Contour Luggage - Medium | `luggage` | Contour | `check-in` | travel | clearance | - | 22900 | 37900 | 150 | 2025-09-01 | `CTR-MED` | FLA, NSH |
| 14 | `contour-luggage-large` | Contour Luggage - Large | `luggage` | Contour | `check-in-large` | travel | clearance | - | 25900 | 42900 | 90 | 2025-09-01 | `CTR-LRG` | FLA, NSH |
| 15 | `ridge-trunk-medium` | Ridge Trunk - Medium | `luggage` | Ridge | `trunk` | travel | - | - | 28900 | 45900 | 420 | 2026-06-22 | `RDG-TRM` | NSH, CMI, SFL |
| 16 | `ridge-trunk-large` | Ridge Trunk - Large | `luggage` | Ridge | `trunk` | travel | - | - | 31900 | 49900 | 180 | 2026-06-22 | `RDG-TRL` | NSH, SFL |
| 17 | `ridge-cabin-pro` | Ridge Cabin Pro | `luggage` | Ridge | `cabin` | work, travel | tech | must-have | 19900 | 32900 | 560 | 2026-07-06 | `RDG-CPR` | NSH, CMI |
| 18 | `solstice-kids-cabin` | Solstice Kids Cabin | `luggage` | Solstice | `kids` | travel, diaper-and-kids | - | - | 9900 | 15900 | 270 | 2026-04-06 | `SLS-KCB` | CSP, FLA, DEB |
| 19 | `solstice-kids-trolley` | Solstice Kids Trolley | `luggage` | Solstice | `kids` | travel, diaper-and-kids | - | - | 11900 | 18900 | 140 | 2026-04-06 | `SLS-KTR` | CSP, DEB |
| 20 | `solstice-luggage-set-of-2` | Solstice Luggage - Set of 2 | `luggage` | Solstice | `set` | travel | - | - | 18900 | 31900 | 120 | 2026-04-13 | `SLS-SET` | SSU, LWR |
| 21 | `passage-backpack-30l` | Passage Backpack - 30L | `backpacks-and-briefcases` | Passage | `backpack` | work, travel | tech | hot | 8900 | 14900 | 900 | 2026-02-16 | `PSG-B30` | NSH, OLV, HTG |
| 22 | `overnight-backpack-23l` | Overnight Backpack - 23L | `backpacks-and-briefcases` | Meridian | `backpack` | travel | tech | - | 7900 | 12900 | 480 | 2026-02-23 | `OVN-B23` | NSH, DEB |
| 23 | `kettle-backpack` | Kettle Backpack | `backpacks-and-briefcases` | - | `backpack` | work | - | - | 6900 | 10900 | 350 | 2025-11-03 | `KTL-BPK` | HTG, SSU, CSP |
| 24 | `swerve-backpack` | Swerve Backpack | `backpacks-and-briefcases` | - | `backpack` | travel | clearance | - | 5900 | 9900 | 160 | 2025-08-11 | `SWV-BPK` | NSH, FLA |
| 25 | `passage-briefcase` | Passage Briefcase | `backpacks-and-briefcases` | Passage | `briefcase` | work | tech | - | 11900 | 19900 | 230 | 2026-02-16 | `PSG-BRF` | NSH, HTG |
| 26 | `transit-duffle` | Transit Duffle | `backpacks-and-briefcases` | - | `duffle` | travel | - | - | 9900 | 16900 | 310 | 2026-07-20 | `TRN-DUF` | NSH, OLV |
| 27 | `nest-diaper-backpack` | Nest Diaper Backpack | `backpacks-and-briefcases` | - | `diaper-bag` | diaper-and-kids | - | - | 7900 | 12900 | 200 | 2026-08-03 | `NST-DBP` | SSU, HTG |
| 28 | `solstice-kids-backpack` | Solstice Kids Backpack | `backpacks-and-briefcases` | Solstice | `kids-backpack` | diaper-and-kids | - | - | 4900 | 7900 | 170 | 2026-04-06 | `SLS-KBP` | CSP, FLA |
| 29 | `marigold-tote` | Marigold Tote | `totes` | - | `-` | work | - | - | 6900 | 11900 | 640 | 2026-03-30 | `MRG-TOT` | FLA, SSU |
| 30 | `ripple-tote` | Ripple Tote | `totes` | - | `-` | work | - | must-have | 6900 | 11900 | 590 | 2026-06-08 | `RPL-TOT` | DEB, SFL, NSH |
| 31 | `coastal-weekender` | Coastal Weekender | `totes` | Coastal | `-` | travel | - | - | 7900 | 12900 | 280 | 2026-01-19 | `CST-WKD` | DEB, SSU |
| 32 | `mini-sling` | Mini Sling | `slings-and-crossbodies` | - | `-` | travel | - | hot | 4900 | 7900 | 820 | 2026-05-04 | `MNI-SLG` | NSH, CSP, OLV |
| 33 | `passage-crossbody` | Passage Crossbody | `slings-and-crossbodies` | Passage | `-` | travel | - | - | 5900 | 9900 | 250 | 2026-02-16 | `PSG-XBD` | NSH, HTG |
| 34 | `packing-cubes-set-of-6` | Packing Cubes (Set of 6) | `accessories` | - | `-` | travel | - | - | 2900 | 2900 | 700 | 2025-10-06 | `PCK-CUB` | HTG, SSU |
| 35 | `travel-pillow` | Travel Pillow | `accessories` | - | `-` | travel | - | - | 3500 | 3500 | 440 | 2025-10-06 | `TRV-PLW` | HTG, DEB |
| 36 | `stretch-luggage-cover` | Stretch Luggage Cover | `accessories` | - | `-` | travel | - | - | 2400 | 2400 | 100 | 2025-10-20 | `STR-CVR` | NSH |
| 37 | `vault-card-sleeve` | Vault Card Sleeve | `wallets` | - | `-` | work | - | - | 3900 | 5900 | 660 | 2026-08-17 | `VLT-SLV` | NSH, OLV |
| 38 | `vault-bifold-wallet` | Vault Bifold Wallet | `wallets` | - | `-` | work | - | - | 5900 | 5900 | 390 | 2026-08-17 | `VLT-BIF` | NSH, HTG |
| 39 | `vault-card-case` | Vault Card Case | `wallets` | - | `-` | work | - | - | 4900 | 4900 | 130 | 2026-08-24 | `VLT-CSE` | NSH, SFL |

Exceptions to the table: `MRD-CAB-STB` is priced `19900` over `29900`. `PSG-CAB-CSP` and
`VLT-CSE-NSH` hold 0 units, `CTR-CAB-CSP` holds 2 units, and `RDG-TRL-SFL` holds exactly 1 unit.

Size classes are `cabin`, `check-in`, `check-in-large`, `trunk`, `kids` and `set`. Bag types are
`backpack`, `briefcase`, `duffle`, `diaper-bag` and `kids-backpack`. Uses are `work`, `travel` and
`diaper-and-kids`. Tags are `tech` and `clearance`. Badges are `hot` and `must-have`.

1. `GET /api/products/{handle}` returns the product with `handle`, `title`, `category`, `line`,
   `size_class`, `bag_type`, `badge`, `personalisable`, `units_sold`, `weight_kg`,
   `capacity_litres`, `dimensions`, `description` and its `variants` in the table's order. Each
   variant carries `sku`, `colourway`, `colour_family`, `swatch`, `price`, `list_price`,
   `discount_percent`, `on_sale`, `stock`, `in_stock`, `badge` and `media`. The product also carries
   `siblings`: the other products of the same line whose size class is `cabin`, `check-in`,
   `check-in-large` or `set`, each with its `handle`, `title` and `size_class`.
2. `price` in every response is the live price. `discount_percent` is derived, never stored:
   `(list_price - price) / list_price x 100`, rounded to the nearest whole number with halves rounding
   up. `17900` over `29900` is `40`; `19900` over `29900` is `33`; `59900` over `109900` is `45`; a
   colourway sold at its list price is `0`. A percentage typed onto a card is a defect.
3. A colourway's `badge` is decided in this order, and only one ever applies: `sold-out` when that
   colourway has no stock; otherwise `hot` or `must-have` when the product carries that badge;
   otherwise none. So `Passage Luggage - Cabin` reads `sold-out` in `Corner Shop Pink` and `hot` in
   every other colourway, and `Vault Card Case` reads `sold-out` in `Night Shift`.
4. `units_sold` is the table figure plus the units of every `paid` or `fulfilled` order placed since
   the app first started; a cancelled order stops counting.
5. Products in the `luggage` category are `personalisable`; nothing else is.
6. The weight, capacity and external dimensions of luggage follow its size class. A set is the sum of
   its pieces: `Passage Luggage - Set of 3` and `Meridian Luggage - Set of 3` are one cabin, one
   check-in and one check-in large piece, and `Solstice Luggage - Set of 2` is two kids pieces.

   | Size class | `weight_kg` | `capacity_litres` | `dimensions` |
   |---|---|---|---|
   | `cabin` | `3.23` | `40` | `54 x 37.5 x 23.5 cm` |
   | `check-in` | `3.95` | `68` | `66 x 44 x 27 cm` |
   | `check-in-large` | `4.70` | `98` | `76 x 50 x 30 cm` |
   | `trunk` | `5.10` | `90` | `70 x 45 x 34 cm` |
   | `kids` | `2.10` | `22` | `45 x 32 x 20 cm` |
   | a set of 3 | `11.88` | `206` | `54 x 37.5 x 23.5 cm, 66 x 44 x 27 cm, 76 x 50 x 30 cm` |
   | a set of 2 | `4.20` | `44` | `45 x 32 x 20 cm, 45 x 32 x 20 cm` |

   Bags, totes, slings, accessories and wallets carry figures of your choosing in the same fields.
7. `media` lists the drawn pictures of a colourway: four `image` shots at positions 1 to 4, the front,
   side, back and interior views, each with `alt` text naming the product and the colourway, for
   example `Passage Luggage - Cabin in Field Olive, front view`.
8. A delisted product (`published` false) answers not found on its page and on its API, leaves every
   collection, the search and the home page, and cannot be added to a cart.

### Collections

Every browsing destination is a collection: there is no route shape for a size, a use or a highlight
that is not also a collection. A collection has a `handle`, a `name`, a `kind`, a `position` and a
`strapline`, and the products it holds are decided by the rule in its row, never by a hand-kept list.

| # | Handle | Name | Kind | Holds | Strapline | Products |
|---|---|---|---|---|---|---|
| 1 | `passage` | Passage | `line` | products in the Passage line | The everyday classic, refined | 7 |
| 2 | `meridian` | Meridian | `line` | products in the Meridian line | The new face of movement | 5 |
| 3 | `coastal` | Coastal | `line` | products in the Coastal line | Salt air, sure footing | 4 |
| 4 | `contour` | Contour | `line` | products in the Contour line | Lines that hold their shape | 3 |
| 5 | `ridge` | Ridge | `line` | products in the Ridge line | Trunks for the long haul | 3 |
| 6 | `solstice` | Solstice | `line` | products in the Solstice line | Small cases for small travellers | 4 |
| 7 | `tech-range` | Tech Range | `size` | products tagged `tech` | Room for the laptop, too | 4 |
| 8 | `cabin` | Cabin | `size` | size class `cabin` | Made for the overhead bin | 5 |
| 9 | `check-in` | Check-in | `size` | size class `check-in` | A week away, sorted | 4 |
| 10 | `check-in-large` | Check-in Large | `size` | size class `check-in-large` | For the long trip | 4 |
| 11 | `trunk` | Trunk | `size` | size class `trunk` | Deep enough for everything | 2 |
| 12 | `kids-luggage` | Kids Luggage | `size` | size class `kids` | Their own suitcase at last | 2 |
| 13 | `sets` | Sets | `size` | size class `set` | More pieces, less to pay | 3 |
| 14 | `luggage` | Luggage | `category` | category `luggage` | Every suitcase we make | 20 |
| 15 | `backpacks-and-briefcases` | Backpacks & Briefcases | `category` | category `backpacks-and-briefcases` | Carry for the commute and beyond | 8 |
| 16 | `totes` | Totes | `category` | category `totes` | Open, easy, everyday | 3 |
| 17 | `slings-and-crossbodies` | Slings & Crossbodies | `category` | category `slings-and-crossbodies` | Hands free, essentials close | 2 |
| 18 | `accessories` | Accessories | `category` | category `accessories` | Small things that make a trip | 3 |
| 19 | `wallets` | Wallets | `category` | category `wallets` | Slim by design | 3 |
| 20 | `backpacks` | Backpacks | `type` | bag type `backpack` | Two straps, every day | 4 |
| 21 | `briefcases` | Briefcases | `type` | bag type `briefcase` | Sharp for the office | 1 |
| 22 | `duffles` | Duffles | `type` | bag type `duffle` | Throw it all in | 1 |
| 23 | `diaper-bags` | Diaper Bags | `type` | bag type `diaper-bag` | Ready for small emergencies | 1 |
| 24 | `kids-backpacks` | Kids Backpacks | `type` | bag type `kids-backpack` | Sized for school days | 1 |
| 25 | `work` | Work | `use` | use `work` | Built for the working week | 9 |
| 26 | `travel` | Travel | `use` | use `travel` | Pack once, go anywhere | 30 |
| 27 | `diaper-and-kids` | Diaper & Kids | `use` | use `diaper-and-kids` | For the smallest travellers | 4 |
| 28 | `best-sellers` | Best Sellers | `highlight` | the twenty products with the most units sold | What everyone is packing | 20 |
| 29 | `on-sale` | On Sale | `highlight` | products with a colourway whose live price is below its list price | Road Week prices | 34 |
| 30 | `clearance-sale` | Clearance Sale | `highlight` | products tagged `clearance` | Last call on these | 4 |
| 31 | `all` | All Products | `all` | every published product | The whole range | 39 |

1. `GET /api/collections` lists every collection in the order of the table, each with `handle`,
   `name`, `kind` and `product_count`.
2. `GET /api/collections/{handle}` returns the collection with its `strapline`, its `banner_title`
   and its `siblings`: the other collections of the same kind in table order, followed by the kind's
   parent, which is `luggage` for `line` and `size`, `backpacks-and-briefcases` for `type` and `use`,
   and `all` for `category` and `highlight`; the siblings of `all` are the six categories. A line's
   `banner_title` is `The <name> Series`, for
   example `The Meridian Series`; every other collection's `banner_title` is its `name`. An unknown
   handle answers not found.
3. `GET /api/collections/{handle}/products` returns `products`, `total`, `page` and `page_size`.
   `page_size` is `24`, `page` counts from 1, and `total` counts every product that survives the
   filters. Each card carries `handle`, `title`, `lowest_price`, `colourways` (the product's first
   four colourways, each with `sku`, `colourway`, `swatch`, `price`, `list_price`, `in_stock` and
   `badge`) and `more_colourways`, the number of colourways beyond those four.
4. `sort` is one of `featured` (by `position`, the default), `best-selling` (by `units_sold`, most
   first), `price-asc` and `price-desc` (by the product's lowest live price), and `newest` (by launch
   date, latest first). Ties fall back to `position`. Any other value is rejected as invalid.
5. Filters are `size` (repeatable, size classes), `colour` (repeatable, colour families; a product
   matches when any of its colourways is in a chosen family), `price_min` and `price_max` (cents,
   compared with the product's lowest live price, both ends included) and `in_stock` (`true` keeps
   only products with at least one colourway in stock). A product must satisfy every filter group
   given, and any one value within a group.
6. Sorting and filtering are applied by the server over the whole collection before paging, so page 2
   of a sorted, filtered collection continues exactly where page 1 stopped, however many times the
   shopper has loaded more.
7. Worked examples on the seeded catalogue, with the sale active:
   - `/api/collections/luggage/products` has `total` `20`.
   - `/api/collections/on-sale/products?page=2` returns 10 cards and `total` `34`.
   - `/api/collections/luggage/products?size=cabin&colour=pink` returns `Passage Luggage - Cabin`
     then `Contour Luggage - Cabin`.
   - `/api/collections/luggage/products?sort=price-desc` starts with `Passage Luggage - Set of 3`.
   - `/api/collections/all/products?sort=best-selling` starts with `Passage Luggage - Cabin`, then
     `Passage Backpack - 30L`.
   - `/api/collections/wallets/products?price_min=4000&price_max=5000` returns only `Vault Card Case`.
   - `Meridian Luggage - Cabin` shows `more_colourways` `3`, and `Passage Luggage - Cabin` shows `2`.
8. The `best-sellers` collection holds the twenty products with the most `units_sold`, most first,
   and the home page shows the same twenty in the same order.
9. `/collections/all` stacks the six categories in table order, each under its own banner and followed
   by its own products.

### The running sale

1. The running sale is named `Road Week`. `GET /api/sale` returns `name`, `ends_at`, `active` and
   `server_time`. The seeded sale ends at 00:00 UTC on the seventh day after the UTC date the app
   first starts.
2. While the sale is active, every colourway sells at its stored sale price. Once `ends_at` has passed,
   every read and every checkout uses the list price: `price` equals `list_price`, `discount_percent`
   is `0`, `on_sale` is false, the `on-sale` collection is empty, and no struck price is shown anywhere.
   Moving `ends_at` back into the future brings the sale prices back.
3. `PATCH /api/owner/sale` with `ends_at` moves the end of the sale. Only the owner may call it.
4. The countdown on a product page is computed from `ends_at` and the `server_time` the page read,
   never from the visitor's own clock, so two visitors in different places see the same remaining
   time. When it reaches zero the offer strip is removed and the page reads its prices again, so a
   sale price is never shown after its sale has ended.

### The cart

1. `POST /api/carts` creates an empty cart and returns its `token`, a string of at least 24 random
   letters and digits that is the only key to that cart. When the call carries a bearer token, the
   cart is attached to that account. `POST /api/carts/{token}/claim`, signed in, attaches a
   signed-out cart to the caller; claiming a cart already attached to another account is denied.
   `GET /api/me/cart` returns the caller's most recently changed cart that still has lines, and
   answers not found when there is none.
2. `GET /api/carts/{token}` returns `token`, `lines`, `item_count`, `subtotal`, `discount`,
   `delivery`, `total` and `currency`. An unknown token answers not found.
3. `POST /api/carts/{token}/lines` with `sku`, `quantity` (a whole number of at least 1) and optional
   `properties` adds a line. Adding a `sku` already in the cart with the same properties adds to that
   line's quantity instead of creating a second line; different properties make a separate line. An
   unknown or delisted `sku` is rejected as invalid.
4. A line carries `id`, `sku`, `product_title`, `colourway`, `size_class`, `quantity`, `unit_price`,
   `list_price`, `line_total` (`unit_price x quantity`), `line_saving`
   (`(list_price - unit_price) x quantity`), `properties` and `sold_out`. A line's colourway never
   changes: switching colourway is removing the line and adding another.
5. The summary is arithmetic over the lines: `subtotal` is the sum of `list_price x quantity`,
   `discount` is the sum of every `line_saving`, `delivery` is `0` in the cart, and `total` is
   `subtotal - discount + delivery`. `item_count` is the sum of the lines' quantities, so 1 x
   `PSG-CAB-OLV` plus 2 x `MNI-SLG-NSH` gives 3, and the item count shown in the rail and in the
   drawer heading is that number.
6. **A line can never hold more units than its colourway has in stock, read from the store at the
   moment of every add and every change, never from what the page loaded.** An add or change that
   would pass the stock is refused as a client error with `error` `insufficient_stock`, `available`
   set to the units in stock and `message` `Only <available> left in stock.`, for example
   `Only 2 left in stock.` for `CTR-CAB-CSP`, and the line keeps the quantity it had. A colourway with
   no stock is refused the same way with the `message` `Sorry, the last one just sold out.`
7. `PATCH /api/carts/{token}/lines/{id}` with `quantity` changes a line, and `DELETE` on the same path
   removes it. A quantity below 1 is rejected as invalid.
8. Adding to a cart holds no stock. Stock only moves when an order is paid.
9. A cart and its lines persist across reloads, browser restarts and sign-ins. A cart is emptied only
   by a completed checkout or by removing its lines.

### Personalisation, a recorded intent

1. A line of a personalisable product may carry `properties` with `initials` (1 to 7 characters drawn
   from letters, digits and spaces, stored in capitals) and `placement` (`front` or `top`). Any other
   placement, an empty or longer text, any other character, or properties on a product that is not
   personalisable is rejected as invalid.
2. The properties travel unchanged from the cart line to the order line, and are shown on the cart
   line, the confirmation, the order page and the confirmation email as `Initials: <initials>,
   <placement>`, for example `Initials: AM, front`.
3. Personalisation is a stub that records intent: there is no preview pipeline, nothing renders a
   preview of the initials, and nothing generates artwork. Before anything is entered, the personalise panel reads `Design not created yet. Start customising`.

### Checkout and payment

1. `POST /api/checkout` takes `cart_token`, `checkout_key` (8 to 64 characters, generated by the page
   once per checkout attempt), `email`, `address` (`name`, `line1`, optional `line2`, `city`,
   `region`, `postcode`, `country`, `phone`), `delivery_method` (`standard` or `express`) and an
   optional `corporate_account`. A signed-in call links the order to the account; a signed-out call
   creates a guest order.
2. Validation happens before anything is written. An empty cart is refused with `error` `cart_empty`.
   An address missing a required field, a `postcode` that is not five digits, or a `country` other
   than `US` is rejected as invalid with `field` naming the first bad field. An `email` that is not an
   address, or a `delivery_method` outside the two, is rejected as invalid.
3. `standard` delivery costs `0` and arrives 3 to 5 days after the order's UTC date; `express` costs
   `1500` and arrives 1 to 2 days after it. `GET /api/delivery-estimate?method=standard` returns
   `method`, `cost`, `from` and `to`, where `from` and `to` are UTC dates counted from today.
4. **Prices are read again at checkout.** When any line's live price differs from the `unit_price`
   the cart shows, the checkout is refused with `error` `price_changed` and `message`
   `The price of one item changed while you were shopping. Review before paying.`, the cart's lines
   take the live prices, and nothing else is written. Submitting again then proceeds at those prices.
   The amount charged is always the price in force at checkout.
5. **Stock is checked in the same step that pays the order.** When a line asks for more units than
   its colourway has, the checkout is refused with `error` `out_of_stock`, the `sku` and the message
   from the cart rules, the line is marked `sold_out` when none are left, and no order, no movement
   and no billing account is written.
6. **Payment.** An accepted checkout gives the order its `number`, `VS-` followed by six digits,
   counting up from `VS-100004`. The app then opens the order's billing account in `killbill` with
   `POST /1.0/kb/accounts`, sending `name` from the address, `externalKey` `valisette-<number>` (for
   example `valisette-VS-100004`), `email` from the checkout, `currency` `USD` and `country` from the
   address. The order becomes `paid` only once
   `GET /1.0/kb/accounts?externalKey=valisette-VS-100004` answers with that account, and its
   `billing_account` is that key. The app never marks an order paid on the strength of its own request
   alone.
7. **Corporate billing.** When `corporate_account` is given, the app opens no new account and reads
   `GET /1.0/kb/accounts?externalKey=<corporate_account>` instead. When the provider holds no such
   account, the checkout is refused with `error` `billing_account_unknown` and `message`
   `We could not find that corporate account.` When the account's currency is not `USD`, it is
   refused with `error` `billing_account_currency` and `message`
   `That corporate account is billed in <currency>. Corporate orders are billed in USD.`, for example
   `That corporate account is billed in EUR. Corporate orders are billed in USD.` for `orbit-acme`.
   Otherwise the order is billed to that account, and its `billing_account` is the key given. The
   provider already holds `orbit-northwind` (Northwind Trading, `USD`), `orbit-acme`
   (Acme Partner Ltd, `EUR`) and `orbit-amelia` (Amelia Ortega, `EUR`). A refused corporate checkout
   writes no order and moves no stock.
8. **One step, all or nothing.** Marking the order paid, writing its lines with the prices captured at
   that moment, taking the stock down for each colourway bought (one `sale` movement per line) and
   emptying the cart happen together or not at all. A failed checkout leaves no order without its
   lines and no movement without its order.
9. **A repeat is the same order.** A checkout repeated with the same `checkout_key` returns the order
   the first attempt created, with the same number, and creates no second order, no second movement,
   no second billing account and no second email, including when both attempts arrive in the same
   moment. The provider refuses a second account whose `externalKey` is already in use.
10. **The last unit is sold once.** Two checkouts for the last unit of one colourway, arriving in the
    same moment, produce exactly one paid order and one `out_of_stock` refusal, and the colourway's
    stock ends at `0`, never below.
11. An accepted checkout answers with the order: `number`, `state`, `email`, `lines`, `address`,
    `delivery_method`, `delivery_from`, `delivery_to`, `subtotal`, `discount`, `delivery`, `total`,
    `currency` (`usd`), `billing_account` and `placed_at`. Each order line carries `sku`,
    `product_title`, `colourway`, `size_class`, `quantity`, `unit_price`, `list_price` and
    `properties`, and `address` carries the fields the checkout took. Order totals follow the cart
    arithmetic with the chosen delivery cost added.
12. Worked examples with the sale active, except the last row:

    | Cart | Delivery | `subtotal` | `discount` | `delivery` | `total` | The email opens |
    |---|---|---|---|---|---|---|
    | 1 x `PSG-CAB-OLV` + 2 x `MNI-SLG-NSH` | `standard` | 45700 | 18000 | 0 | 27700 | `Order <number>, total charged $277.` |
    | the same cart | `express` | 45700 | 18000 | 1500 | 29200 | `Order <number>, total charged $292.` |
    | 1 x `MRD-CAB-STB` + 1 x `PCK-CUB-HTG` | `standard` | 32800 | 10000 | 0 | 22800 | `Order <number>, total charged $228.` |
    | 1 x `PSG-SET-NSH`, after the sale has ended | `standard` | 109900 | 0 | 0 | 109900 | `Order <number>, total charged $1,099.` |

    Amounts in an email or on a page are written in dollars with a thousands separator, without cents when
    the cents are zero and with two decimals otherwise: `$277`, `$1,099`, `$44.75`.

### The confirmation email

1. When an order becomes `paid`, and only then, the app sends one email over SMTP to the checkout
   `email`, no cc and no bcc, from `orders@valisette.example.com`. The subject is exactly
   `Your valisette order <number> is confirmed`, for example
   `Your valisette order VS-100004 is confirmed`.
2. The body opens with `Order <number>, total charged <amount>.`, for example
   `Order VS-100004, total charged $277.`, then lists every line with its title, colourway, size
   class, quantity and personalisation, then the delivery address and the arrival window.
3. A refused checkout, a repeated checkout, a cart change, a signup, a sign-in and a newsletter
   subscription send no email.

### Orders and addresses

1. `GET /api/me/orders` lists the caller's own orders, newest first, each with `number`, `placed_at`,
   `total`, `currency` and `state`.
2. `GET /api/orders/{number}` returns an order to the account that placed it, with its lines,
   address, state, delivery window, totals and `billing_account`. A call without a session is turned away
   as unauthenticated first. **Any other signed-in caller, and any number that does not exist, gets
   the same refusal, with the same status and the same body**, so the refusal never tells an existing
   order from a missing one. A guest order is read only through the
   owner endpoints.
3. An order line keeps the `product_title`, `colourway`, `size_class`, `unit_price` and `list_price`
   captured when the order was placed. Renaming, repricing or delisting the product or colourway
   later never changes what a past order says.
4. An order's `state` is one of `pending`, `paid`, `fulfilled` and `cancelled`. `order number` is
   unique and is the only order identifier that ever appears in a web address.
5. `GET /api/owner/orders` lists every order, newest first, each in the same shape as the order an
   accepted checkout answers with. `POST /api/owner/orders/{number}/fulfil`
   moves a `paid` order to `fulfilled`. `POST /api/owner/orders/{number}/cancel` moves a `paid` order
   to `cancelled` and writes one `cancellation` movement per line, with the line's quantity as a
   positive delta, so the stock comes back while the original `sale` movements stay. Any other
   transition is rejected as invalid and changes nothing, and cancelling moves no money at the
   provider.
6. `GET /api/me/addresses` and `POST /api/me/addresses` list and save the caller's delivery addresses,
   and `PATCH /api/me/addresses/{id}` and `DELETE /api/me/addresses/{id}` change and remove one. An
   address is validated like a checkout address. The first address saved is the default; `is_default`
   true on a save or a change makes that address the only default; deleting the default makes the
   oldest remaining address the default. Another account's address id answers not found and changes
   nothing.

### Stock movements

1. Stock is never a number somebody edits: every change is a stock movement with `sku`, `delta`,
   `kind` (`sale`, `restock`, `cancellation` or `adjustment`), `order_number` for a `sale` or a
   `cancellation`, `note` and `created_at`, and a colourway's `stock` always equals the sum of its
   movements' deltas. A movement is never updated and never deleted.
2. `POST /api/owner/stock-movements` with `sku`, `delta` (a whole number other than zero), `kind`
   (`restock` or `adjustment`) and `note` records a movement. A movement that would take the stock
   below zero is rejected and writes nothing, and `sale` or `cancellation` movements cannot be written
   by hand.
3. `GET /api/owner/stock-movements?sku=<sku>` lists a colourway's movements, oldest first.
4. **Stock never reads below zero, under any interleaving of checkouts, cancellations and owner
   movements.**

### Owner catalogue edits

1. `PATCH /api/owner/products/{handle}` changes `title` and `published`; the owner endpoints reach a
   delisted product as well as a published one.
2. `PATCH /api/owner/variants/{sku}` changes `colourway`, `price` and `list_price`. A `price` above
   the `list_price`, or either figure at or below zero, is rejected as invalid and changes nothing.
3. Every owner endpoint denies a `customer` and a signed-out caller, and the catalogue stays as it
   was.

### Search

1. `GET /api/search?q=<text>` returns `query`, `count` and `products`, the products as collection
   cards. Matching ignores letter case and covers the product title, the colourway names and the name
   of the product's line, so a shopper searching a colour finds products whose titles never contain
   the word: `olive` returns the 8 products that come in `Field Olive`.
2. Ranking puts title matches first, then colourway matches, then line-name matches, each group in
   `position` order. `coastal` returns the four products titled `Coastal`, then `Ridge Trunk - Medium`
   and `Ridge Cabin Pro` for their `Coastal Mist` colourway. `meridian` ends with
   `Overnight Backpack - 23L`, which matches only through its line.
3. The `sort` values of the collection rules may reorder the results; filters do not apply to search.
4. A query with no match returns `count` `0`; the search page quotes the query back and offers the
   `best-sellers`, `on-sale` and `luggage` collections instead.
5. Recent searches and recently viewed products are kept in the visitor's own browser and never sent
   to the server, and a single control clears the recent searches.

### The store directory

1. `GET /api/stores` lists every store ordered by `city`, then by `name`, each with `name`, `city`,
   `region`, `address`, `postcode`, `phone` and `hours`. `q` narrows the list to stores whose city or
   name contains the text, ignoring letter case, in the same order: `port` returns the two Portland
   stores, and `new` returns `Newbury Street`, `Hudson Yards` and `SoHo`.
2. The fourteen stores:

   | Name | City | Region | Address | Postcode | Phone | Hours |
   |---|---|---|---|---|---|---|
   | `South Congress` | `Austin` | TX | 1400 South Congress Avenue | 78704 | `+1 512 555 0131` | Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00 |
   | `Newbury Street` | `Boston` | MA | 234 Newbury Street | 02116 | `+1 617 555 0142` | Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00 |
   | `Fulton Market` | `Chicago` | IL | 900 West Randolph Street | 60607 | `+1 312 555 0153` | Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00 |
   | `Magnificent Mile` | `Chicago` | IL | 540 North Michigan Avenue | 60611 | `+1 312 555 0164` | Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00 |
   | `LoDo` | `Denver` | CO | 1650 Wazee Street | 80202 | `+1 303 555 0175` | Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00 |
   | `Abbot Kinney` | `Los Angeles` | CA | 1305 Abbot Kinney Boulevard | 90291 | `+1 310 555 0186` | Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00 |
   | `Wynwood` | `Miami` | FL | 2520 NW 2nd Avenue | 33127 | `+1 305 555 0197` | Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00 |
   | `Hudson Yards` | `New York` | NY | 20 Hudson Yards | 10001 | `+1 212 555 0108` | Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00 |
   | `SoHo` | `New York` | NY | 118 Greene Street | 10012 | `+1 212 555 0119` | Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00 |
   | `Lloyd Center` | `Portland` | OR | 2201 Lloyd Center | 97232 | `+1 503 555 0120` | Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00 |
   | `Pearl District` | `Portland` | OR | 1120 NW Couch Street | 97209 | `+1 503 555 0110` | Mon to Sun 10:00 to 21:00 |
   | `Hayes Valley` | `San Francisco` | CA | 432 Hayes Street | 94102 | `+1 415 555 0121` | Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00 |
   | `Union Square` | `San Francisco` | CA | 170 O'Farrell Street | 94102 | `+1 415 555 0132` | Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00 |
   | `Pike Place` | `Seattle` | WA | 1501 Pike Place | 98101 | `+1 206 555 0143` | Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00 |

3. The directory is useful with the filter empty: every store is listed, with no map, no geolocation
   prompt and no distance sort.

### Newsletter and gift cards

1. `POST /api/newsletter` with `email` stores the address lowercased and answers with `message`
   `Thank you for subscribing!`. Subscribing an address already stored answers the same and stores
   nothing new. A value that is not an email address is rejected as invalid.
2. `POST /api/gift-cards/balance` with `code` answers `balance` in cents and `currency` for an active
   card: `VSGC-2026-AMBER` holds `5000`. Every other code, including the expired `VSGC-2025-LAPSED`, is
   refused with the same status and the same body, whose `message` is `That code is not recognised.`,
   so the form never reveals whether a code was ever valid.

### Standing pages, privacy and the not-found page

1. Ten standing pages live at `/pages/<handle>`, and `GET /api/pages/{handle}` returns `handle`,
   `title` and `body`:

   | Handle | Title | Footer link text |
   |---|---|---|
   | `faq` | `FAQ` | `FAQ` |
   | `warranty` | `Warranty` | `Claim My Warranty` |
   | `terms` | `Terms & Conditions` | `Terms & Conditions` |
   | `airline-damage-policy` | `Airline Damage Policy` | `Airline Damage Policy` |
   | `journal` | `Journal` | `Blogs` |
   | `trial` | `30 Day Trial` | `Claim 30 Day Trial` |
   | `returns` | `Return & Refund Policy` | `Return & Refund Policy` |
   | `privacy` | `Privacy Policy` | `Privacy Policy` |
   | `careers` | `Careers` | `Join our team! - careers@valisette.example.com` |
   | `gift-cards` | `Gift Cards` | `Check Gift Card Balance` |

2. The privacy page states what valisette keeps about a shopper (account details, saved addresses,
   orders, carts and the newsletter address), how long each is kept (orders seven years, carts ninety
   days after their last change, accounts and newsletter addresses until the shopper asks for
   removal), that no card details are ever collected, and that search history and recently viewed
   products never leave the visitor's browser. The footer of every page links it.
3. An unknown address, and a product, collection or page handle that matches nothing, renders
   valisette's own not-found page inside the full chrome, with the heading
   `That page has moved on without us.`, one line of apology, and three links: `/`,
   `/collections/all` and `/pages/stores`. It answers with a not-found status, never with a success
   status carrying an apology.
4. An unknown address under `/api` answers a JSON body with `error` `not_found` and a not-found
   status, never an HTML page.
5. Every internal link on every page resolves to a page that exists.
6. Every document declares a favicon in its head, and the favicon it declares answers as an image:
   the suitcase glyph, served by the app itself as vector markup.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | home: ticker, rail, hero carousel, collection tiles, category tiles, bestseller grid with editorial tiles, video tile, newsletter and footer | public |
| `/collections/<handle>` | one collection: trail, chip strip, banner, product grid and load more, with sort and filter in the rail | public |
| `/collections/all` | every product, stacked by category, each group under its banner | public |
| `/products/<handle>` | one product: media stack, buy panel, coverage details, offer countdown, accordions, compare and recently viewed | public |
| `/search?q=<text>` | search results with the query in the address | public |
| `/cart` | the cart and its summary, with its empty state | public |
| `/checkout` | contact and delivery, delivery method and payment, then the confirmation | public |
| `/pages/stores` | the store directory with its city and name filter | public |
| `/pages/<handle>` | standing pages: FAQ, warranty, terms, airline damage policy, journal, trial, returns, privacy, careers, gift card balance | public |
| `/account/login` | sign in | public |
| `/account/register` | create an account | public |
| `/account/recover` | request a password reset link | public |
| `/account/reset/<token>` | choose a new password | reset link |
| `/account` | the signed-in overview: greeting, default address and three latest orders | signed in |
| `/account/orders` | order history, newest first | signed in |
| `/account/orders/<number>` | one order with its lines, state, delivery window and amount charged | signed in |
| `/account/addresses` | saved delivery addresses with the default marked | signed in |

**Entry and redirects.** A signed-out request for `/account`, `/account/orders`,
`/account/orders/<number>` or `/account/addresses` lands on `/account/login?next=<path>`, and signing
in returns to that path; signing in without a `next` lands on `/account`. Signing out returns to `/`
and the token stops working. A signed-in visitor opening `/account/login` or `/account/register` is
sent to `/account`. Requesting `/checkout` with an empty cart
redirects to `/cart`. An unknown product, collection or page handle renders the not-found page inside
the chrome. Another account's order number shows the same not-found page as a number that does not
exist.

**Journeys.**

1. **Browse by size, then by collection.** Open `/`, open the `Luggage` entry of the rail to show its
   panel, choose `Cabin` under `By Size`, and land on `/collections/cabin` showing five cards with
   `Cabin` in the trail. Choose the `Sets` chip in the chip strip and land on `/collections/sets` with
   three cards. Open the panel again, choose `Meridian` under `By Collection`, and land on
   `/collections/meridian` under the banner `The Meridian Series`.
2. **Buy a suitcase as a guest.** Open `/products/passage-luggage-cabin`, choose the `Deep End Blue`
   thumbnail and find `Color: Deep End Blue`, the price `$179` beside the struck `$299`, and the
   address ending in `?sku=PSG-CAB-DEB`. Choose `ADD TO CART`, find the cart drawer open with the
   line, choose `Checkout`, fill `Contact & delivery` with a new email and a Portland address,
   choose `Standard` under `Delivery method`, keep `Pay now` under `Payment`, choose `Place order`, and
   land on `Thank you. Your order is confirmed.` with a `VS-` number, the line, the address and the
   arrival window.
3. **Personalise before adding.** Open `/products/meridian-luggage-cabin`, open the `Personalise`
   tab and read `Design not created yet. Start customising`, enter `AM` with the `front` placement,
   add to the cart, and find `Initials: AM, front` on the line in `/cart`; then remove the line.
4. **Filter and sort a collection.** Open `/collections/luggage`, open `FILTER BY` in the rail, choose
   the `pink` colour and the `cabin` size, apply, and find two cards, a filter count beside
   `FILTER BY`, and the choices in the address. Reload and find the same two cards. Choose
   `Clear all` and find twenty cards again.
5. **Load more.** Open `/collections/on-sale`, find twenty-four cards, choose `Load more`, find
   thirty-four cards and `page=2` in the address; open a product, go back, and find all thirty-four
   still shown.
6. **Hit the stock ceiling.** Add `Contour Luggage - Cabin` in `Corner Shop Pink` to the cart, raise
   the line to 3 with the stepper, read `Only 2 left in stock.` beside the alert mark, and find the
   line still at the quantity it had; then remove the line.
7. **Find a store.** Open `/pages/stores`, read `14 stores`, type `port` and read `2 stores`, open
   `Pearl District`, and find its opening hours, its phone number and a directions link.
8. **Search by colour.** Choose `SEARCH` in the rail, type `olive` in the overlay and submit, land on
   `/search?q=olive` reading `8 results for "olive"`, then open the overlay again and find `olive`
   under `Recent Searches`.
9. **Read my orders.** Sign in at `/account/login` as `customer@example.com` with
   `deku-demo-pw-2026`, open `Order History` from the rail, find `VS-100002` above `VS-100001`, open
   `VS-100001`, and find `Passage Luggage - Cabin` in `Field Olive` at `$179` and the state
   `Fulfilled`.
10. **Stay in your lane.** Signed in as `customer2@example.com`, open `/account/orders/VS-100001` and
    find the not-found page.
11. **Refused corporate billing.** With a line in the cart, check out choosing `Bill a corporate
    account` with `orbit-acme`, and read
    `That corporate account is billed in EUR. Corporate orders are billed in USD.` with the cart
    unchanged.
12. **Check a gift card.** Open `/pages/gift-cards`, check `VSGC-2026-AMBER` and read `Balance: $50`,
    then check `VSGC-2025-LAPSED` and read `That code is not recognised.`
13. **Subscribe.** At the foot of `/`, enter an address in `Enter Email Address`, submit, and find the
    field replaced by `Thank you for subscribing!` on the same page.
14. **Forget a password.** Open `/account/recover`, submit `customer@example.com`, and read
    `If we know that address, a reset link is on its way.`

**States.** Every grid shows loading cells at their final size before its cards arrive, so nothing
moves when the cards land. A collection or search with no match shows its empty state rather than a
blank page: `Nothing here matches that yet.` over `Clear the filters, or browse the whole range.` on a
collection, and `Nothing matched that.` over `Try a colour, a size, or one of these.` on search. An
empty cart shows `Your cart is empty` and `CONTINUE SHOPPING`. An account with no orders shows
`No orders yet.`, and one with no addresses shows `No saved addresses yet.` A grid that fails to load
more keeps the cards it has and adds one row carrying the alert mark and a `Try again` control. No
failure takes a page down, and errors never show a stack trace.

## UI/UX notes

**North star.** Somebody arriving should understand at once that this is a shop selling one brand's
own bags, that the sale is on, and that every bag comes in colours they can see before they commit;
the product itself is the first thing seen on every page. **Register.** This is a consumer retail
storefront: it carries the brand's point of view, but the working surface of a shop (the wall of
products, the buy panel, the cart) is dense, ruled and scannable, and the atmosphere lives in the
drawn imagery rather than in decoration around it. Two stances hold it together, and a competing
store could rationally hold the opposite of either: **rules over gaps**, because the grid reads as one
continuous ruled sheet rather than floating cards, and **controls beside the products over controls
above them**, because sorting and filtering live in the left column next to the wall they change.

**Mode.** The product is designed light, fully: a white page with a black navigation column. There is
no dark mode to design or to show.

**Palette by role.** Two grounds and no third. The page is pure white. Product pictures sit on a
near-white neutral tile, a hair off white, with a second near-white neutral one barely-perceptible
step deeper wherever two tiles meet and the seam would otherwise vanish. The navigation column and
every panel that opens from it are pure black, with white ink inside. On the page, ink is black;
secondary ink is a mid cool neutral grey; and the single most used colour in the product is a light
cool neutral hairline, which is what makes the grid read as a grid at all. A slightly heavier light
neutral divider separates blocks on a pale panel, and a form field at rest carries a light cool
neutral border. One accent carries the brand: a saturated, vivid amber yellow. At full strength it is
the ground of the promotional ticker and appears nowhere else. Two tints carry it into smaller
places: a marginally lighter vivid amber behind the coverage term on a product page, and a pale soft
amber wash for the active label inside the black panel, the underline of a pointed-at rail link and
the rule beneath the wordmark on a product page. **Apart from the drawn illustrations, whose suitcases, wheels and stripes are amber by design,
nothing in the interface that is not promotional borrows the amber.** Three colours carry meaning and appear nowhere except where they mean it: a vivid red is the
ground of the badge on a product that is selling fast, black is the ground of the badge on a colourway
that has sold out, and a vivid orange is the warning mark beside a form or cart error. The single
green in the product is reserved for the size tile that leads to a set, marking the saving. Scrims are
translucent black: under a caption laid on a picture, the veil behind a dialog, and the floating
header on a phone, which is mostly opaque. Column headings inside the black panel are white at
reduced strength rather than a separate grey. Swatches are product data rather than palette: a disc is
whatever colour its colourway is, and a very pale disc gets a hairline edge so it does not disappear
on the tile. The exact shades are yours, so long as the page stays white and black, the amber stays
promotional in the interface, and each meaning colour keeps its meaning to itself.

**Type and typography.** One sans-serif family carries the whole product, taken from the reader's own
system so that no font file is ever downloaded and first paint never waits for type; aim for a
geometric grotesque character with a single-storey a and a tall x-height, and let a system stack
stand in for it. Nearly everything is set at one body size: product titles, prices, rail links and
running text. A step down sets secondary text, accordion bodies and address lines; a smaller step sets
the legal and specification text in the product accordions; the smallest steps set badges, the tax
line, the delivery estimate, the swatch label and the ticker, which is set in capitals. The largest
text on any page is a section heading, about half again the body size. There is no display size:
the biggest words in the product are drawn into the pictures, never set as text. Weight carries
emphasis sparingly: a medium weight for the active rail entry, the main action label and the overflow
count of swatches; a semibold for the captions under the size tiles; the boldest weight for the image
card titles in the black panel, the `SEARCH` row and the headings inside policy pages. Figures line up
in a column wherever prices, totals and quantities stack. The family and the sizes are yours, so long
as one family carries everything and the section heading stays the largest text on the page.

**Shape and density.** Corners are square nearly everywhere: product cells, tiles, banners, fields and
buttons. The round shapes are few enough that they read as controls: colourway swatches are full
discs while the carousel indicators stay short thin bars, the floating header on a phone is a pill, the swatch label and the small
chips and loading blocks are softly rounded, the image cards in the black panel are a little rounder,
and the badge on a card is flush to the left edge of its cell and rounded only on the side that leaves
it. Only two things cast a shadow: the swatch label, a small soft shadow, and the search panel, one
deep wide shadow. Everything else is separated by hairlines. Two things blur what is behind them: the
floating phone header, lightly, and the search veil, a little less. The grid is dense: cells abut with
no gap, text sits inset by one even margin on every side beneath a picture that fills its cell edge to
edge, and a full wall of products fits a laptop screen. Every gap is a multiple of one base unit, which
is yours to choose. The layout archetype is `sidebar-nav`: a fixed left column holds the wordmark, the
categories and the actions, and the working surface sits beside it.

**Motion.** Motion is spent on state changes, never on scenery: nothing slides in as the page
scrolls, and nothing follows the pointer. Everything that eases uses one of two curves. The first is
symmetric and unremarkable and serves every hover, every open and close and every colour change; the
second overshoots its end and settles back, and it is spent in exactly one place, the cart count's
confirmation when something is added, so the one moment the site is pleased with itself is the moment
a shopper commits. No component brings a curve of its own. Durations follow one ladder: colour changes
on a control are the quickest; the fade half of a drawer opening comes next; small movements such as
the swatch label and the badge are a touch longer; anything that covers area, such as a panel, the
cart drawer or the search overlay, takes about a third of a second; drawers that grow take longer
still, their height growing more slowly than their content fades in. The promotional ticker is the
one continuous movement: a duplicated row glides leftward at a slow constant pace, a full lap taking
about a minute, joined so seamlessly that the restart is invisible, driven by time and never by
scrolling. Opening a panel lifts it a short distance into place while it fades in, and its inner group
grows very slightly to full size in the same window. On the product page a small aeroplane crosses the
coverage strip from left to right and starts again; it is decoration. A drawer opens by growing to its
height, never by blinking into place, and its plus mark never rotates: the open row instead takes a
heavier weight and its hairline turns black. The floating phone header changes width smoothly when its
state changes, and it is the only element that animates its width. Under a reduced-motion request the
ticker holds still showing its first pair of items, the aeroplane stops, the cart count changes
instantly without the overshoot, the loading bars hold still, and every drawer, panel and overlay still opens, only without the
transition.

**Hover and focus.** A pointed-at rail link gains an underline in the pale amber wash; a pointed-at
product card crossfades its picture to the second view of the same colourway; a pointed-at swatch gains
a black ring set just off the disc and shows its label; the main action keeps its black ground while
its label turns the pale amber wash; a footer link gains an underline. Every hover state has a focus
state at least as visible, and no information exists only on hover.

**Components.** Each valisette control, from a size tile to the quantity stepper to a checkout field,
carries five states of its own: resting, pointed-at, pressed, focused and unavailable, and an
unavailable control says so in wording or shape too, never by colour alone. There is one main action style, a black ground with a
white capitalised label, and one quieter alternative, a black outline with a black label on the page
ground; each page leads with one primary action, visibly distinct from every secondary one. Drawers,
panels, the search overlay and dialogs close with Escape and return focus to the control that opened
them. Destructive actions (removing an address) ask once before acting, in place.

**Accessibility floors for the storefront.** Every valisette page meets WCAG 2.2 level AA.
Body text reaches a contrast of at least `4.5:1` against its ground, and large text, interface
components and the focus indicator reach at least `3:1`; this applies to white text in the black
column as much as to black text on the page. The live price is set in full-strength ink and the struck
list price in the secondary grey, so both pass. Touch targets meet the WCAG 2.2 minimum target size.
Keyboard navigation reaches every control, every panel, drawer, overlay and dialog is operable by
keyboard alone, focus is held inside a dialog and inside the phone navigation drawer and nowhere else,
and tab order follows the visual order at every width. Each colourway swatch is a control whose
accessible name is the colourway name, the group of swatches is labelled with the product name, and
the chosen swatch is marked pressed, so a visitor who cannot see or cannot hover still gets the names.
Icon-only controls, such as the search, account, cart and close glyphs, carry a text label, and no
meaning, whether a sold-out colourway, an error or a saving, is carried by colour alone. Every drawn product
picture carries alternative text naming the product and the colourway, and every drawn editorial tile
carries alternative text describing its scene, because its words live inside the picture.

**Responsive.** From a phone up to a wide desktop the storefront layout is responsive and holds at
every viewport width, in three arrangements. On a wide screen the black column is fixed at the left and the grid
is four across; on a middle-width screen the column narrows and the grid is three across; on a phone
the column gives way to a floating translucent pill header and the grid is two across. Where those
breakpoints fall is yours. Nothing is hidden on a smaller screen: every product, every filter and every
policy link stays reachable on a phone, and nothing scrolls sideways except a strip that is meant to.

**What it must not look like.** Not a page washed in yellow, not a card grid with gaps and shadows
where a ruled sheet belongs, not a marketing banner stack in place of the wall of products, not a
product picture that is a grey placeholder box, and not a price whose saving has to be worked out from
colour alone.

## Technical requirements

- Front end: Svelte with Vite, written in TypeScript, built for production into static assets that
  the back end serves. The browser runs a single-page application that talks to the JSON API on the
  same origin; the document served for `/collections/<handle>` and `/collections/all` already carries
  the first page of product titles and live prices, rendered by the server from the same Svelte
  components, so a collection page is readable before its script has run.
- Back end: Express on Node.js 20, in TypeScript, serving the HTTP API under the `/api` prefix and the
  built front end on the same origin. It answers the not-found status itself for an unknown address or
  an unknown product, collection or page handle, while still serving the page chrome.
- Store: PostgreSQL, reached at `DATABASE_URL`, which the environment also exports as `DB_URL` with the
  same value, through the `pg` driver.
- Payments: `killbill`, the billing platform, reached at `PAYMENTS_API_URL`. Every `/1.0/kb/*` call
  carries HTTP Basic credentials from `PAYMENTS_API_USER` and `PAYMENTS_API_PASSWORD`, the header
  `X-Killbill-ApiKey` set to `PAYMENTS_API_KEY` and the header `X-Killbill-ApiSecret` set to
  `PAYMENTS_API_SECRET`; a write also carries `X-Killbill-CreatedBy`. `GET /1.0/healthcheck` answers
  without credentials. The surface this product uses is exactly `POST /1.0/kb/accounts`, whose body is
  `{"name", "externalKey", "email", "currency", "country"}` and which answers `201` on create and
  `409` when the `externalKey` is already held, and `GET /1.0/kb/accounts?externalKey=<key>`, which
  answers `200` for an account that exists and `404` for one that does not. Kill Bill is a billing
  platform, not a card processor: there is no card, no card token and no decline in this environment.
- Mail: Mailpit, reached over SMTP at `SMTP_HOST` and `SMTP_PORT`, with `SMTP_USER` and `SMTP_PASS`
  when they are set, sent through `nodemailer`.
- Auth: app-implemented email and password with bearer tokens; passwords are hashed with a slow salted
  algorithm.
- Health: `GET /api/health` returns `200` with `{"status": "ok"}` once PostgreSQL and `killbill`
  both answer.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing services
available in this environment are PostgreSQL, `killbill` and Mailpit, and reaching for anything else
is a contract violation.

PostgreSQL, `killbill` and Mailpit are already running and reachable at those variables. Do not
download, install, compile or start a copy of any of them, and read every host, port and credential
from the environment rather than writing one into the code. The billing accounts of the two seeded
self-paid orders are opened in `killbill` by the app the first time it starts, and the app keeps
retrying until the payments service answers.

- The storefront's own script budget is one hundred and eighty kilobytes: the scripts a page's
  document references directly add up to no more than 180 KB once compressed with gzip.
- No page requests a raster image, a video, a font file or an icon sprite: product pictures,
  editorial tiles, the video still and every icon are drawn by the page itself. The favicon is the one
  file an image request fetches, and it is drawn vector markup served by the app.
- Nothing the browser downloads carries a database credential, a payments credential or another
  shopper's token.
- All timestamps are UTC and are sent as ISO 8601 strings ending in `Z`; dates are `YYYY-MM-DD`.
- A list endpoint returns a top-level JSON array, except the collection and search endpoints, which
  return the named object with its `products` array.
- The end of the sale, the expiry of a token and the arrival window are worked out when they are
  read, so moving the end of the sale takes effect on the very next read.

## Data model

Nineteen tables, one per entity. All timestamps are UTC. Every table has an integer `id`.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

- **`account`**: `id`, `email` unique and stored lowercased, `password_hash`, `name`, `role`
  (`customer` or `owner`), `created_at`.
- **`session_token`**: `id`, `account_id`, `token_hash` unique, `expires_at`, `revoked_at`,
  `created_at`.
- **`password_reset`**: `id`, `account_id`, `token_hash` unique, `used_at`, `created_at`.
- **`address`**: `id`, `account_id`, `name`, `line1`, `line2`, `city`, `region`, `postcode`,
  `country`, `phone`, `is_default`, `created_at`. At most one default address per account.
- **`category`**: `id`, `handle` unique, `name`, `position`.
- **`collection`**: `id`, `handle` unique, `name`, `kind` (`line`, `size`, `category`, `type`, `use`,
  `highlight` or `all`), `rule`, `strapline`, `position`.
- **`product`**: `id`, `handle` unique, `title`, `category_id`, `line`, `size_class`, `bag_type`,
  `uses`, `tags`, `badge`, `personalisable`, `weight_kg`, `capacity_litres`, `dimensions`,
  `description`, `seed_units_sold`, `launched_on`, `position`, `published`.
- **`variant`**: `id`, `product_id`, `sku` unique, `colourway`, `colour_family`, `swatch`, `price`,
  `list_price`, `position`. A `price` never exceeds its `list_price`, and both are greater than zero.
- **`media`**: `id`, `variant_id`, `kind` (`image` or `video`), `position`, `alt`.
- **`stock_movement`**: `id`, `variant_id`, `delta`, `kind` (`sale`, `restock`, `cancellation` or
  `adjustment`), `order_id`, `note`, `created_at`. Rows are only ever added.
- **`store`**: `id`, `name`, `city`, `region`, `address`, `postcode`, `phone`, `hours`.
- **`cart`**: `id`, `token` unique, `account_id`, `created_at`, `updated_at`.
- **`cart_line`**: `id`, `cart_id`, `variant_id`, `quantity`, `properties`, `unit_price_captured`,
  `added_at`. Quantities are at least 1.
- **`orders`**: `id`, `number` unique, `account_id`, `email`, `address_snapshot`, `delivery_method`,
  `subtotal`, `discount`, `delivery`, `total`, `currency`, `state` (`pending`, `paid`, `fulfilled` or
  `cancelled`), `checkout_key` unique, `billing_account`, `placed_at`. One order per `checkout_key`,
  however many times or however simultaneously it is submitted.
- **`order_line`**: `id`, `order_id`, `variant_id`, `sku`, `product_title`, `colourway`, `size_class`,
  `quantity`, `unit_price`, `list_price`, `properties`.
- **`subscriber`**: `id`, `email` unique and stored lowercased, `created_at`.
- **`gift_card`**: `id`, `code` unique, `balance`, `currency`, `expires_on`.
- **`sale`**: `id`, `name`, `ends_at`.
- **`page`**: `id`, `handle` unique, `title`, `body`.

Derived rather than stored: a colourway's `stock` (the sum of its movements), `in_stock`,
`discount_percent`, `on_sale`, the live `price` once the sale has ended, `badge` on a colourway,
`units_sold`, a product's lowest live price, a collection's members and `product_count`, the sale's
`active`, a cart's `subtotal`, `discount`, `delivery` and `total`, a line's `line_total` and
`line_saving`, and an order's delivery window. None of them is a column that can drift from what it
is derived from.

**Invariants.**

- For every colourway, the stock equals the sum of its movements' deltas and is never below zero,
  whatever the interleaving of checkouts, cancellations and owner movements.
- A stock movement is never updated or deleted; a cancellation is a new movement with a positive
  delta.
- An order line keeps the title, colourway, size class and prices of the moment it was written.
- An order in `paid`, `fulfilled` or `cancelled` has its `billing_account` set and has one `sale`
  movement per line.
- A failed action leaves no partial row: no order without its lines, no line without a colourway, no
  movement without an order where its kind requires one.
- Two checkouts for the last unit of one colourway never both become `paid`: exactly one wins and the
  other is refused.

**Seed data.**

- The categories, the thirty-one collections, the thirty-nine products, their colourways, stock and
  media, exactly as the tables in Core features state. Seeding writes, per colourway, one `restock`
  movement for its table quantity plus the units the seeded orders took, then one `sale` movement per
  seeded order line, so every colourway starts at its table quantity.
- The three accounts in User roles. `customer@example.com` has one default address: `Aarav Mehta`,
  `42 Alder Lane`, `Apt 3`, `Portland`, `OR`, `97205`, `US`, `+1 503 555 0177`.
- The three orders:

  | Number | Account | State | Placed | Lines | Delivery | `subtotal` | `discount` | `delivery` | `total` | `billing_account` |
  |---|---|---|---|---|---|---|---|---|---|---|
  | `VS-100001` | `customer@example.com` | `fulfilled` | 20 days before first start | 1 x `PSG-CAB-OLV` at 17900, list 29900 | `standard` | 29900 | 12000 | 0 | 17900 | `valisette-VS-100001` |
  | `VS-100002` | `customer@example.com` | `paid` | 2 days before first start | 1 x `MNI-SLG-NSH` at 4900, list 7900; 1 x `PCK-CUB-HTG` at 2900, list 2900 | `express` | 10800 | 3000 | 1500 | 9300 | `valisette-VS-100002` |
  | `VS-100003` | `customer2@example.com` | `paid` | 1 day before first start | 2 x `VLT-SLV-OLV` at 3900, list 5900 | `standard` | 11800 | 4000 | 0 | 7800 | `orbit-northwind` |

  `VS-100001` and `VS-100002` ship to the default address of `customer@example.com`; `VS-100003` ships to
  `Noor Haddad`, `9 Birch Court`, `Seattle`, `WA`, `98101`, `US`, `+1 206 555 0188`. The lines carry the
  titles, colourways and size classes of the catalogue as seeded.

- The fourteen stores, the ten standing pages, the `Road Week` sale, and two gift cards:
  `VSGC-2026-AMBER` with `5000` in `usd` and no expiry, and `VSGC-2025-LAPSED` with `2500`, expired on
  `2025-12-31`.

Seeding must be idempotent - restarting the app must not duplicate rows, must not write a second set
of seed movements, and must not open a second billing account.

## Front-end specification

The visual detail the sections above state as intent, surface by surface. Every paragraph describes
something a visitor can see; the values behind it are yours.

**Chrome, the same on every page.** Four parts surround every page: the ticker, the navigation column
(the rail), the search overlay and the footer. The first control on every page is a skip link reading
`Skip to content`, hidden until it is focused. The page has one banner region holding the ticker and
the rail, one main region, and one content-information region holding the footer.

**The ticker.** A thin full-width band on the vivid amber ground, above everything including the rail,
with a slim inset at its ends. Inside it one row of small black capitalised items runs horizontally,
alternating two strings, `Road Week - Up to 50% off` and `LIVE NOW`, with a small upright rounded bar in
the pale amber wash between each pair. The row is duplicated end to end and glides left forever, as
motion describes; it never shifts the layout of the page when it wraps, the page never scrolls with it,
and every item is a link to `/collections/on-sale`. It is the one element that looks identical on every
screen size. It is hidden entirely once the sale has ended.

**The rail.** On a wide and a middle-width screen the rail is a fixed black column against the left
edge, running the full height of the window and never scrolling with the page. It holds three stacked
blocks, separated from each other by a sliver of page ground so they read as three cards rather than
one bar. The wordmark block carries `valisette` in white. The category block lists, one per line in
white, `Luggage`, `Backpacks & Briefcases`, `Totes`, `Slings & Crossbodies`, `Accessories`, `Wallets`,
`Gift Card` and `Clearance Sale`; the first two open a panel, and the rest go straight to
`/collections/totes`, `/collections/slings-and-crossbodies`, `/collections/accessories`,
`/collections/wallets`, `/pages/gift-cards` and `/collections/clearance-sale`. The actions block sits on
a white ground rather than black and lists `SEARCH` in the boldest weight above `ACCOUNT` and `CART`,
each capitalised with its drawn glyph aligned to the right of the row and a hairline between rows. The
cart row shows the item count beside `CART` and disappears entirely while the cart is empty rather than
showing a zero. Signed in, the account row shows `Order History` and `Logout` beneath it instead of
going straight to a page. On a collection page a fourth white block appears beneath the actions
carrying `SORT BY` with the plus mark above `FILTER BY` with the filter mark and the count of active
filters; the search page shows the same block with `SORT BY` alone, and no other page shows it. On a product page the rail collapses to the wordmark block alone, with a pale amber
rule along its lower edge, so the buy panel gets the width of the page.

**The panels.** The `Luggage` and `Backpacks & Briefcases` entries each open a wide black panel whose
left edge meets the rail's right edge with no seam, running almost to the right edge of the page and
floating above the content. Inside, three text columns sit beside two image cards. The luggage panel's
columns are `By Size` (`Tech Range`, `Cabin`, `Check-in`, `Check-in Large`, `Trunk`, `Kids Luggage`,
`Sets`, `View All`), `By Collection` (`Passage`, `Contour`, `Meridian`, `Ridge`, `Coastal`,
`Solstice`, `Kids Luggage`) and `Highlights` (`Best Sellers`, `On Sale`), and its image cards are
`Passage Collection` and `Meridian Collection`. The bags panel's columns are `Collection`
(`Backpacks`, `Briefcases`, `Duffles`, `Diaper Bags`, `Kids Backpacks`, `View All`), `By Use` (`Work`,
`Travel`, `Diaper & Kids`) and the same `Highlights`, with image cards for the `Backpacks` and
`Briefcases` collections. Every entry leads to the collection of the same name, and `View All` leads to
the panel's category. Column headings are capitalised white at reduced strength; entries are solid
white, one per line; the entry for the collection being viewed carries the pale amber wash; image cards
are rounded, with a bold white title laid over a drawn picture. A panel opens when the pointer enters
its rail entry and closes when the pointer has left both the entry and the panel, with a short grace so
crossing the gap does not close it. The rail entry is also a keyboard control: it toggles the panel,
focus moves into the panel, and Escape closes it and returns focus to the entry.

**The search overlay.** `SEARCH` opens a full-page overlay rather than a new page: a translucent black
veil softly blurring the whole page, and a full-width white panel covering most of the window (all of
it on a phone) with the one deep shadow. The panel holds a text input with a larger, lighter search
glyph, then two blocks: `Recent Searches`, a capitalised heading over the visitor's own last queries
with a `Clear` control, and `Recently Viewed Products`, a centred section heading over a horizontal
strip of product cards. Submitting goes to `/search?q=<text>`. Escape closes the overlay and returns
focus to the `SEARCH` row.

**The footer and the newsletter.** Above the footer, outside it, sits the newsletter block: a section
heading `Warm Hugs, valisette.`, two lines of body reading
`We'll email you important updates, new launch info and the occasional silly picture.`, and one
full-width field with the placeholder `Enter Email Address` beside a square submit button carrying an
up-and-right arrow. On success the field is replaced in place by `Thank you for subscribing!`; the block
never navigates away. The footer itself is full width on a black ground with a drawn landscape behind
it at low contrast, so white text stays readable. It has five columns: the wordmark, large; a contact
block headed `Need assistance?` with
`Write to us at care@valisette.example.com or call us at +1 503 555 0142. We're available on weekdays from 10:00 AM to 7:00 PM and on Saturdays from 10:00 AM to 6:00 PM.`,
the address and the number as links, then `For Gifting & Corporate orders` with
`Message us at +1 503 555 0199 or email gifting@valisette.example.com`; a link column with `FAQ`,
`Claim My Warranty`, `Terms & Conditions`, `Airline Damage Policy` and `Blogs`; a second link column
with `Claim 30 Day Trial`, `Return & Refund Policy`, `Privacy Policy`,
`Join our team! - careers@valisette.example.com` and `Check Gift Card Balance`; and the brand essay
headed `#KeepMoving`, reading
`We believe people have to keep moving to thrive. To grow. To feel alive. As long as there is a destination in mind, whether it's a life goal, a career aim or a trip, there is a purpose. We're on a mission to help folks travel with ease and arrive looking sharp. Every trip starts the minute you have a destination in mind, not when you get there.`
On a phone the two link columns become drawers with a down chevron. The footer is the one place every
public destination is visible at once.

**Iconography.** Every icon is drawn by the page from geometry, never loaded as a file, with round
joins and caps. The set is: a magnifier for search, a head-and-shoulders outline for the account, a
trolley with two wheels for the cart, a cross for close, right and left chevrons, a small filled wedge
for the trail, a house with a door for home, a plus that opens a drawer and the sort list and never
rotates, three tapering horizontal lines for the filter, a tick for the chosen sort, a map pin, a bank
card for the payment row, a filled circle with an exclamation mark in the warning orange, a white play
triangle, a down chevron for the footer drawers, and an up-and-right arrow for the newsletter button.
One larger drawing is the size tile suitcase: an amber-yellow body with a thin black outline, two black
wheels at its lower corners, a telescopic handle of two bars joined by a bridge rising above the body,
a black label plate, and seven evenly spaced grooves running across the body. Larger sizes draw the same
suitcase with a taller body, so cabin, medium and large read as one family at a glance, and a set tile
draws two or three of them side by side, smaller. The favicon is the same suitcase.

**The zero-asset substitution: drawn pictures.** The product ships with no photograph and no product
photography of any kind. Every product picture is drawn by the
page on the near-white tile ground, with the object floating in generous margin, and the same colourway
always draws the same picture, derived from its `sku`, across reloads. Hard-shell luggage is a rounded
body shaded from a lighter version of the swatch colour at the top to a darker one at the bottom, with
eight to twelve thin grooves running vertically across its middle, a darker plate at the upper right,
four wheels at the lower corners (amber on cabin and check-in pieces, a very dark tint of the swatch
otherwise), a handle of two bars joined across the top, and, on half the colourways, one contrasting
amber stripe running vertically at a third of the width. Soft bags and backpacks are a rounded trapezoid
narrowing towards the top, a flap over the upper third with a slight overhang and a thin shadow line
beneath it, two straps behind the body, and one or two small pocket shapes, with the same shading and
stripe rules. Totes are a body with a gently convex lower edge and two long handle arcs, with no
hardware. Wallets are a small rounded rectangle, noticeably wider than tall, with one amber stripe near
the bottom and a thin lighter line at the top suggesting the opening. Every object sits over one soft
elliptical shadow wider than itself. The four shots of a colourway are the front, side, back and
interior views of the same object. Editorial tiles and banners stand in for lifestyle photography
and are drawn compositions: a three-stop
gradient ground from one of six duotone moods (forest, coast, desert, dusk, snow and interior), a soft
darkening towards the edges, one large product silhouette offset to a third of the frame, two or three
soft organic shapes for depth, and their words drawn into the picture in white with a thin dark edge
so they survive a pale ground. The video tile shows a drawn still frame with the play triangle; pressing
play runs a slow drawn pan and crossfade between two compositions, and no video file is ever fetched.
A drawn picture is a diagram of the object, not a photograph, and it keeps the right silhouette, colour,
proportions and ground.

**The product card.** The card is identical wherever it appears: home, collections, search, the
recently viewed strip and the cross-sell block. Its anatomy: a cell of the ruled grid with square corners and
no shadow, bordered on every side by the hairline it shares with its neighbours. Top to bottom: the
picture, square, filling the cell; the title on one line, cut with an ellipsis when too long, as a link
to `/products/<handle>?sku=<sku>` for the chosen colourway; the price row, the live price in full ink
then, after a small gap, the struck list price in the secondary grey at a smaller size (no struck price
when the two are equal); and the swatch row, up to four discs a small gap apart, then the overflow
count written `+<n>` in the medium weight, which is not a control and does not expand the row. The text
block is inset by one even margin. The whole cell is one link except the discs, which switch the card's
picture, live price, list price and link to that colourway in place, without reloading the grid and
without moving the card. The chosen disc carries a black ring with a gap, drawn so the disc itself
keeps its size. A badge may sit in the top left corner, flush to the cell's edge, one at a time:
`SOLD OUT` on black when the shown colourway has no stock, `HOT` on the vivid red for a product selling
fast, or `MUST HAVE` on black, set on two lines, for a staff pick; the labels are small, white and
capitalised. A sold-out colourway also shows its picture faded. Pointing at a swatch shows a small black
label above the disc, softly rounded and softly shadowed, carrying the colourway name and centred on the
disc whatever the name's length. While cards are loading, each cell is already at its final size, with
its picture area and three text bars in the hairline colour, softly rounded and gently pulsing, and
motionless under a reduced-motion request, so the grid never moves when the cards arrive. A failed load keeps the cards
already shown and adds one row carrying the warning mark and `Try again`.

**Home page.** The longest page, several screens tall and meant to be scrolled; every block earns its
height. It opens with a hero carousel the full width of the content column: three drawn slides, each a
scene of a bag in use with no text and no button over it, each one link, to `/collections/passage`,
`/collections/meridian` and `/collections/on-sale`. Beneath the slides sit short thin indicator bars,
the active one solid white and the rest faint. The carousel changes slide when an indicator is pressed,
when the slides are dragged, or with the arrow keys, never on a timer, and a slide change is a
translation of the whole track on the standard curve. Next come two strips, each a section heading
over a row of drawn tiles with a white caption laid in the bottom corner over a translucent black
scrim: `Luggage Collections`, with `Passage Collection`, `Coastal Collection` and
`Meridian Collection`, leading to `/collections/passage`, `/collections/coastal` and
`/collections/meridian`, which never scrolls; and `Categories`, with `Luggage`, `Bags & Backpacks`,
`Totes & Handbags`, `Travel Accessories` and `Wallets`, leading to `/collections/luggage`,
`/collections/backpacks-and-briefcases`, `/collections/totes`, `/collections/accessories` and
`/collections/wallets`, which scrolls sideways on the middle-width screen and on a phone. Then the main
event: the heading `Bestsellers` at the left and an underlined `View All` at the right leading to
`/collections/best-sellers`, over the ruled grid of the twenty bestsellers, four across on a wide
screen. Two drawn editorial tiles are cut into that grid as ordinary cells, keeping every rule
unbroken: after the first row, a two-cell tile reading `ELEVATE` over `your daily carry` that leads to
`/collections/backpacks-and-briefcases`; after the third row, a one-cell tile reading
`THE CRAFTSMANSHIP OF A` over `tuxedo` over `TAILORED FOR YOUR POCKET.` that leads to
`/collections/wallets`. Editorial tiles lead to collections, never to a product. The grid is not paged
here, and the page closes with the full-width video tile, the newsletter block and the footer.

**Collection page.** A slim pale grey band across the content column carries the trail: the home
glyph, the wedge, then the collection name with a wedge beside it that opens a list of its siblings.
Beneath the trail runs the chip strip: square chips, each a drawn picture on the tile ground with the
collection name beneath it, one per sibling collection, with a thin black border on the chip of the
collection being viewed and none on the rest, and a last chip reading `View all` that leads to the
parent. The strip is how a shopper moves sideways without going back to the panel, so the page needs
no side tree of categories. Then the banner: a full-bleed drawn picture with the `banner_title` drawn
into it in white and, beneath it, the one-line strapline. Then the ruled grid, four across on a wide
screen, with editorial tiles cut in as on the home page, and beneath the grid a `Load more` control
that appends the next twenty-four cards. `/collections/all` stacks the six categories, each banner then
its grid, and is the only page that repeats a banner.

**Sort and filter.** Both live in the rail's fourth block and neither appears above the grid. `SORT BY`
opens a list under its own row: `Featured`, `Best selling`, `Price, low to high`,
`Price, high to low` and `Newest`, the chosen one on a black row with a small white tick. Choosing
re-orders the grid in place without a page change. `FILTER BY` opens four groups the same way: `Size`
(check boxes for the six size classes), `Colour` (the swatch discs of the colour families), `Price`
(a two-handle range spanning the collection's own lowest and highest price, rounded outwards to whole
dollars) and `Availability` (`In stock only`), with `Clear all` and `Apply`. Each chosen value can be
cleared on its own. The address always carries the same parameters as the API, for example
`/collections/luggage?size=cabin&colour=pink&sort=price-asc&page=2`, so the view survives a reload,
can be sent to somebody, and the back gesture returns to the same depth rather than to the first
twenty-four. A filter with no result shows the collection empty state, never a blank page.

**Product page.** Beneath the trail, two columns. The left column is the media stack: the four drawn
views of the chosen colourway at full size in one column, scrolling with the page; choosing another
colourway replaces the whole stack. Beneath the views sits a numbered feature carousel of eight panels,
each a drawn picture with a counter such as `1/8`, a heading and a paragraph; the headings are
`Aviation-grade telescope handle`, `Silent wheels`, `Water resistant`,
`Indestructible and lightweight`, `Thoughtful details`, `Make it truly yours`, `3 years warranty` and
`30 day trial`. The right column is the buy panel, which stays in view as the media scrolls past and
releases when the accordions reach it. Top to bottom, the buy panel holds: the title as a section
heading; on luggage, the coverage strip; three tabs, `Colors`, `Personalise` and `Compare`, the active
one in full ink with a thick underline and the others faded; the colourway row, square picture
thumbnails with a thin black border on the chosen one, ending in the `+<n>` count when there are more
than fit; the line `Color:` in the boldest weight followed by the colourway name; on luggage, the size
tiles, one for the product being viewed (marked chosen) and one for each sibling, each a drawn
suitcase over a semibold caption, where `cabin` reads `Cabin`, `check-in` reads `Medium`,
`check-in-large` reads `Large` and a set reads `Save on Sets` in the single green; the price row, the live price at section
heading size, then `MRP:` and the struck list price small in the secondary grey; `Incl of all taxes`,
small and grey; the instalment line, `or pay in 4 - <first instalment> today - 0% interest`, where the
first instalment is the live price divided by four and rounded up to the cent, for example
`or pay in 4 - $44.75 today - 0% interest` at `$179`; the offer strip; a full-width `PERSONALISE`
button in the quieter style; and a full-width `ADD TO CART` button in the main style. Choosing a
colourway writes its `sku` into the address, so a colourway can be linked to, and a sold-out colourway
turns `ADD TO CART` into an unavailable `SOLD OUT` button. Adding opens the cart drawer, whose
heading carries the cart's item count, and runs that count's one overshoot; the collapsed rail stays
the wordmark block alone. Below the buttons come a cross-sell block headed `Pair It With` with
`Packing Cubes (Set of 6)` over `The End of Digging.` and `Travel Pillow` over
`Your Window Seat Upgrade.`, each with an `ADD` control that adds its first colourway; the delivery
estimate, `Expected Delivery in <from> - <to>` with the standard window written as day and short month,
for example `Expected Delivery in 21 Sep - 23 Sep`; three trust chips, `Durable, Lightweight shell`,
`30 Day Return Policy` and `3 Years Warranty`; and the accordions.

**The coverage strip and its dialog.** On luggage, directly under the title, one detailed row: the
small aeroplane crossing, the term `1-Year` on the lighter amber highlight, `AIRLINE DAMAGE COVER` in
small capitals, and on a second line the notional price `$49` struck through, `Free with this luggage`,
a middle separator and a `Details` link with a single chevron. `Details` opens a dialog, not a page, on
the translucent veil, holding focus and closing with Escape or the drawn cross. The dialog carries the
eyebrow `Included with this luggage`; the headline `1 year of airline damage cover. Free.`; the promise
`If an airline damages your bag in transit, we repair or replace it. No extra cost, no fine print gymnastics.`;
two callouts, `Plan value` over `FREE` and `Validity` over `1 Year`; a three-step list headed
`How it works`: `Spot damage at the belt?` over
`Get a damage report from the airline desk before you leave the airport.`, `Tell us within 7 days` over
`Share the report and photographs of the damage.`, and `We repair or replace` over
`Your luggage. Free.`; three cards headed `Also covered under warranty`: `Shell` over
`Cracks, dents & colour fades`, `Wheels & trolley` over `Wobbles, stiff handles, buttons`, and
`Hardware` over `Zippers, handles, feet & logo plate`; a row of exclusion tags after `Not covered`:
`Theft & loss`, `Overpacking`, `Wear & tear`, `Scratches & scuffs`, `Heat, fire & chemicals` and
`Commercial use`; and a closing line, `Part of valisette Shield, valisette's damage protection programme.`,
with a `Know More` link to `/pages/airline-damage-policy`.

**The offer strip and the countdown.** Under the price, a strip carrying two offers, each a bold term
over an italic qualifier, `The Road Week Sale` over `Up to 50% off` and `Pay in 4` over
`Interest-free on every order`, and a countdown: the label `Sale Extended! Ends in`, then days, hours,
minutes and seconds as four figures separated by colons, each labelled beneath with `D`, `H`, `M` or
`S`. The strip disappears with the sale.

**The personalise and compare tabs.** `Personalise` shows a short form: a text field for up to seven
characters with its remaining count, and two choices of placement, `front` and `top`, with the empty
state `Design not created yet. Start customising` until something is entered; the `PERSONALISE`
button opens this tab. What is entered travels with the next add to the cart. `Compare` lets the
shopper choose another product from the same category and shows the two side by side, `Your Pick`
against the choice, with their weight, capacity and external dimensions aligned in rows.

**The accordions and the tail.** Four drawers, in this order, each opening by the drawer behaviour in
motion: `Dimension`, open on arrival, with `Weight`, `Capacity` and `External dimensions` shown as
label and value pairs such as `3.23 Kg`, `40L` and `54 x 37.5 x 23.5 cm`; `Description`, four or five
bold lead-ins each followed by a sentence; `Warranty & Return`, carrying `Not 100% Sure?`,
`Order and try valisette for 30 days.`, `No strings attached.`,
`We know you'll love it, but if you don't, just send it back. We'll give you a full refund. We offer a 30 day risk free return on all our luggage. To start a return, email us at care@valisette.example.com.`,
then `3 Years worry-free warranty.` over
`We love our products. If anything breaks we fix or replace it for you.`; and `More Information`,
the legal block, `Manufactured, Imported and Marketed by:`, `Valisette Travelware Co.`,
`Unit 4, Coastline Works`, `118 Canal Street`, `Portland, OR 97209, USA`, `Country of Origin:` and
`Vietnam, Mexico`, in the smaller legal size. After the accordions come the trial banner, a large `30`
over `days trial` over
`Try out your valisette for 30 days. If you still feel it's not the one for you, return it for a full refund.`;
the compare module headed `COMPARE` with `Wish to Compare your bag?` and `Your Pick`; and a
`Recently Viewed` strip of product cards.

**Cart drawer and cart page.** The cart is a page as well as a drawer: adding opens a drawer from the
right under a heading with the item count, showing the same lines and summary, and the rail's cart row leads to `/cart`. A line shows the
colourway's drawn picture small on the tile ground, the title, the colourway name and size class
beneath it in secondary grey, any personalisation, a quantity stepper, the line total and a remove
control, with a hairline between lines. The summary sits to the right of the lines on a wide screen and
beneath them on a phone: `Subtotal` at list prices, `Discount` as a negative amount, `Delivery` reading
`Free`, and `Total`, then a full-width black `Checkout` button, which sticks to the bottom of the window
on a phone. A stepper that would pass the stock leaves the quantity where it was and shows the warning
mark with the one line naming the available number; a line whose colourway sold out during checkout is
marked `SOLD OUT` with its quantity controls unavailable. The empty cart shows a centred section heading
`Your cart is empty`, the drawn trolley large beneath it, and a black `CONTINUE SHOPPING` button leading
to `/collections/all`.

**Checkout.** Three sections on one page, each opening as the one before it completes, with the order
summary beside them on a wide screen: `Contact & delivery` (email, name, two address lines, city,
region, postcode, country fixed to the United States, phone; signed in, the email and the default
address are filled in), `Delivery method` (`Standard` with `Free, 3 to 5 days` and `Express` with
`$15, 1 to 2 days`, and the total updating as the choice changes), and `Payment` (`Pay now`, chosen by
default, with the line `Your order is billed through our payments partner when you place it.`, or
`Bill a corporate account` with a `Corporate account reference` field), ending in a full-width black
`Place order` button that shows a busy state and cannot be pressed twice while an order is being
placed. Every field rejects invalid input next to the field it names, keeps what was typed and writes
nothing. A price change, a sold-out line or a refused corporate account is explained above the button
in the warning style, with the cart intact. The page stays still while an order is being placed: no
motion, plain wording, nothing decorative. On success the page replaces itself with the confirmation:
the heading `Thank you. Your order is confirmed.`, the order number, the lines as bought, the delivery
address, and the arrival window written as `Arriving <from> - <to>`.

**Store directory.** A flat list, not a map. Above it, one text field with the placeholder
`Find a store by city or name` filters as the visitor types, with the result count beside it, such as
`14 stores` or `1 store`. Each row carries the store name at section heading size, the full address
beneath it in black, and the plus mark at the right; rows are separated by the hairline and open by the
drawer behaviour to reveal `Opening hours` with the hours, `Call the store` as a telephone link, and
`Directions` with the drawn map pin, linking to a map search for the address. A filter with no match
reads `No store matches that yet.`

**Search page.** The header restates the query and the count, for example `8 results for "olive"`,
above the ruled grid of cards. `SORT BY` is available in the rail and `FILTER BY` is absent: the
results are already ranked. The empty state quotes the query, shows `Nothing matched that.` over
`Try a colour, a size, or one of these.`, and offers `Best Sellers`, `On Sale` and `Luggage` as
chips.

**Standing pages and the gift card form.** Warranty, returns, terms, privacy, the airline damage
policy, the trial, careers, the FAQ and the journal share one reading shape: the trail, a section
heading, and one column of body text at a comfortable reading measure, about the width of a paperback
page, with headings in the boldest weight and a hairline above and below any list. None of them carries
a picture, a form or a control beyond the chrome. The gift card page is the exception: under
`Check Gift Card Balance` it carries one field labelled `Gift card code` and a `CHECK BALANCE` button,
and answers in place with `Balance: <amount>`, such as `Balance: $50`, or `That code is not recognised.`

**The not-found page.** The full chrome, a section heading `That page has moved on without us.`, the
line `The page you asked for is not here any more.`, and three links, `Home`, `Shop all` and
`Find a store`.

**Account pages.** Sign in is a centred form on the page ground: the section heading `Login`, a field
labelled `Email` with the placeholder `Enter your email`, a field labelled `Password` with the
placeholder `Enter your password`, a `Remember me` check box at the left and a `Forgot password?` link
at the right on one line, then a full-width black `LOGIN` button, with a link to create an account
below. A failed sign-in shows `That email and password do not match.` in the warning style above the
button. Register has the heading `Create an account`, fields labelled `Name`, `Email`, `Password` and
`Confirm password`, and a `CREATE ACCOUNT` button; two passwords that differ show
`The two passwords do not match.` beside the second field and send nothing. Recover has the heading
`Reset your password`, one email field and a `SEND RESET LINK` button, and answers in place. The reset
page has the heading `Choose a new password`, one password field and a `SAVE PASSWORD` button, and on
success reads `Your password has been changed.` with a link to sign in. `/account` greets the shopper
as `Hello, <first name>`, such as `Hello, Aarav`, shows the default address and the three latest
orders, and links `Order History` and `Addresses`. `/account/orders` is a table of number, date,
total and state, newest first, with the state written as a word: `Pending`, `Paid`, `Fulfilled` or
`Cancelled`. An order page shows the lines as bought with their colourway, size class, quantity,
personalisation and captured prices, the delivery address, the state, the arrival window and the amount
charged. `/account/addresses` lists the saved addresses with a `Default` marker on one, and lets each
be edited, made default or removed.

**Phone arrangement.** On a phone the rail becomes a floating pill header inset from the edges of the
window, translucent black over a lightly blurred page, carrying a menu control, the wordmark, the
search glyph and the cart glyph with its count; it changes width smoothly when it condenses on scroll.
The menu control opens a full-height drawer from the left holding the category list; an entry with a
panel steps into its columns as a list, and a `Back` control steps up one level. Focus is held inside
the drawer while it is open. Sort and filter move from the rail into a dialog opened from a bar that
sticks beneath the header on collection pages, and sort alone moves there on the search page. The product page stacks the media above the buy panel,
which no longer stays in view. The categories strip and the recently viewed strip scroll sideways.
Every product, every filter and every policy link stays reachable.

**Machine-readable hooks.** These attribute names and values are exact. Each swatch disc, on a
card and in the buy panel, is a button whose `aria-label` is the colourway name and whose
`aria-pressed` is `true` on the chosen disc and `false` on the others, and each row of discs is a
`role="group"` whose `aria-label` is the product title. Each drawn picture is an element with
`role="img"` whose `aria-label` is its alternative text. The countdown element carries
`data-ends-at`, holding the sale's `ends_at`, and each of its four figures sits in an element whose
`data-unit` is `d`, `h`, `m` or `s`. Every page has exactly one `banner`, one `main` and one
`contentinfo` landmark.

**Loading and performance feel.** The collection page's first screen of cards arrives with the page
itself. Pictures below the first screen are drawn only as they approach the window, while the hero is
drawn at once. Every drawn picture reserves its size before it is drawn, so nothing on the page moves
when pictures appear, and system type means no text reflows after first paint.

## Constraints

- One brand, one storefront. No second seller, no marketplace, no auction and no listings from
  outside the business.
- No customer reviews, no live chat or conversational assistant, no subscription plan, no loyalty or
  rewards scheme, and no wish list.
- No card collection, no card tokens, no refunds at the provider and no payment callbacks: billing is
  a real account in `killbill`, and money is recorded in the app's own orders in `usd`.
- Delivery addresses are in the United States only. The product has one currency, US dollars, and
  one language, English: no multi currency pricing and no locale switching.
- No personalisation preview and no generated artwork: personalisation is recorded, not drawn.
- No map, no geolocation prompt and no distance sort in the store directory.
- No owner console in the browser: owner work happens through the owner endpoints.
- No third-party analytics, tag manager, identity drawer, instalment widget, affiliate tracker, font
  host or content delivery network, and no other network call at runtime apart from `killbill` and
  Mailpit.
- No image, video, font or icon file is fetched by any page; every picture is drawn by the page.
- No native app and no offline mode.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.** Field names are exact. A successful call returns the named resource or shape; an
invalid or unauthorized call is rejected as a client error, never as a server error and never as a
silent success, and carries `error` and a `message` naming the reason. `{handle}` is a product,
collection or page handle, `{token}` a cart token, `{id}` a cart line or address `id`, `{sku}` a
colourway `sku`, and `{number}` an order number.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | - | `status` |
| `POST /api/auth/signup` | `name`, `email`, `password` | `access_token`, `email`, `role` |
| `POST /api/auth/login` | `email`, `password`, `remember` | `access_token`, `role`, `expires_at` |
| `POST /api/auth/logout` | - | an empty success |
| `POST /api/auth/recover` | `email` | `message` |
| `POST /api/auth/reset` | `token`, `password` | an empty success |
| `GET /api/me` | - | `name`, `email`, `role` |
| `GET /api/sale` | - | `name`, `ends_at`, `active`, `server_time` |
| `GET /api/collections` | - | `handle`, `name`, `kind`, `product_count` |
| `GET /api/collections/{handle}` | - | `handle`, `name`, `kind`, `strapline`, `banner_title`, `siblings` |
| `GET /api/collections/{handle}/products` | `sort`, `size`, `colour`, `price_min`, `price_max`, `in_stock`, `page` | `products`, `total`, `page`, `page_size` |
| `GET /api/products/{handle}` | - | the product with its `variants` and `siblings` |
| `GET /api/search` | `q`, `sort` | `query`, `count`, `products` |
| `GET /api/stores` | `q` | `name`, `city`, `region`, `address`, `postcode`, `phone`, `hours` |
| `GET /api/pages/{handle}` | - | `handle`, `title`, `body` |
| `GET /api/delivery-estimate` | `method` | `method`, `cost`, `from`, `to` |
| `POST /api/newsletter` | `email` | `message` |
| `POST /api/gift-cards/balance` | `code` | `balance`, `currency` |
| `POST /api/carts` | - | the cart, with its `token` |
| `GET /api/carts/{token}` | - | `token`, `lines`, `item_count`, `subtotal`, `discount`, `delivery`, `total`, `currency` |
| `POST /api/carts/{token}/lines` | `sku`, `quantity`, `properties` | the cart |
| `PATCH /api/carts/{token}/lines/{id}` | `quantity` | the cart |
| `DELETE /api/carts/{token}/lines/{id}` | - | the cart |
| `POST /api/carts/{token}/claim` | - | the cart |
| `GET /api/me/cart` | - | the cart |
| `POST /api/checkout` | `cart_token`, `checkout_key`, `email`, `address`, `delivery_method`, `corporate_account` | the order |
| `GET /api/me/orders` | - | `number`, `placed_at`, `total`, `currency`, `state` |
| `GET /api/orders/{number}` | - | the order with its `lines`, `address` and `billing_account` |
| `GET /api/me/addresses` | - | `id`, `name`, `line1`, `line2`, `city`, `region`, `postcode`, `country`, `phone`, `is_default` |
| `POST /api/me/addresses` | the address fields, `is_default` | the address |
| `PATCH /api/me/addresses/{id}` | any address field, `is_default` | the address |
| `DELETE /api/me/addresses/{id}` | - | an empty success |
| `PATCH /api/owner/products/{handle}` | `title`, `published` | the product |
| `PATCH /api/owner/variants/{sku}` | `colourway`, `price`, `list_price` | the variant |
| `GET /api/owner/stock-movements` | `sku` | `sku`, `delta`, `kind`, `order_number`, `note`, `created_at` |
| `POST /api/owner/stock-movements` | `sku`, `delta`, `kind`, `note` | the movement, with the colourway's new `stock` |
| `PATCH /api/owner/sale` | `ends_at` | the sale |
| `GET /api/owner/orders` | - | every order, newest first, in the order shape |
| `POST /api/owner/orders/{number}/fulfil` | - | the order |
| `POST /api/owner/orders/{number}/cancel` | - | the order |

Bearer auth is required on everything under `/api/me`, `/api/orders` and `/api/owner`, and on
`/api/auth/logout` and the cart claim; the owner endpoints additionally require the `owner` role.
Every other endpoint answers without a session, and a cart endpoint is reached by its token.

**No mocks.** `killbill` is the only place a billing account exists, Mailpit is the only place a
confirmation email is delivered, and PostgreSQL is the only place the app's records exist. A billing
account the app pretends to have opened, a hardcoded `{"status": "paid"}` the app answers to itself, an
in-memory list of orders or stock, a stock figure kept in process memory, a confirmation written to a
log instead of sent, or a photograph shipped with the app are all the same failure in different
clothes. The named provider is the fact - the app's UI and its own tables can only reflect what lives
in the provider, never substitute for it.

## Definition of done

A shopper can find a suitcase by size or by collection, choose a colourway, see the sale price
against the list price, and place an order that opens its billing account in `killbill`, takes the
stock down and delivers a confirmation email. Two shoppers buying the last unit of a colourway get one
order and one honest refusal, a repeated checkout is one order, and a past order still says what was
bought and what it cost after the catalogue changes.
