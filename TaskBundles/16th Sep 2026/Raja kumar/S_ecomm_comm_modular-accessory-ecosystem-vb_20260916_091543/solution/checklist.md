# Checklist: deku/modular-accessory-ecosystem-vb

Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC
Items: 166
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `ui` A stranger adds a Latch case with a compatible module to the cart from a model listing `src: Overview, the product route offers only the modules that genuinely attach`
- [ ] `C-OV-02` `constraint` The last unit is sold once when two orders race `src: Overview, the last unit sold exactly once`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor cannot place an order `src: User roles, Cannot place an order`
- [ ] `C-RL-02` `role` A visitor is denied the order history with the wishlist `src: User roles, Cannot read any order`
- [ ] `C-RL-03` `role` Another shopper is denied an order owned by someone else `src: User roles, Cannot read or pay another shopper's order`
- [ ] `C-RL-04` `constraint` A refused request leaves the protected order unchanged `src: User roles, leaving the protected state unchanged`
- [ ] `C-RL-05` `capability` A new phone becomes a shopper on the first accepted code `src: User roles, Signup is`
- [ ] `C-RL-06` `literal` The seeded shopper phone is `9876500001` `src: User roles, 9876500001`

## C-CF Core features

- [ ] `C-CF-01` `constraint` An invalid phone is refused `src: Core features, The one identity is a ten digit phone number`
- [ ] `C-CF-02` `constraint` A code for an existing phone goes only to the email on file `src: Core features, the code is sent to the email already on file`
- [ ] `C-CF-03` `constraint` A code request response does not reveal an existing phone `src: Core features, never reveals who is a shopper`
- [ ] `C-CF-04` `capability` A sign in code email arrives in the inbox with the six digits first `src: Core features, arrives as an email whose subject begins`
- [ ] `C-CF-05` `constraint` A sign in code cannot be used twice `src: Core features, A code works`
- [ ] `C-CF-06` `constraint` A newer sign in code cancels the older code `src: Core features, Requesting a new code cancels every earlier unused code`
- [ ] `C-CF-07` `literal` The fourth wrong code reports `That code did not match. Two attempts left.` `src: Core features, After the fourth wrong code`
- [ ] `C-CF-08` `constraint` Six wrong codes lock the phone even for the right code `src: Core features, Six wrong codes lock the phone`
- [ ] `C-CF-09` `constraint` A sixth code request inside ten minutes is refused `src: Core features, a sixth code request for the same phone`
- [ ] `C-CF-10` `capability` Sign out ends the session `src: Core features, Signing out ends the session`
- [ ] `C-CF-11` `data` Device options list unavailable models in rank order `src: Core features, The device options for a product list every non retired device model`
- [ ] `C-CF-12` `data` A retired model is excluded from the device models `src: Core features, A retired model leaves the navigation`
- [ ] `C-CF-13` `data` A device option keeps the colourway or falls back to the first colourway `src: Core features, keeps the chosen colourway when the target product has`
- [ ] `C-CF-14` `ui` Choosing a colour swaps the product in place without navigating `src: Core features, Choosing a colour`
- [ ] `C-CF-15` `ui` Choosing a device navigates to the product for that model `src: Core features, Choosing a different model`
- [ ] `C-CF-16` `data` A listing heading is generated from the model with the category `src: Core features, Its heading is generated, never authored`
- [ ] `C-CF-17` `constraint` A listing first page is full after unpublished products are excluded `src: Core features, A listing only ever contains published products`
- [ ] `C-CF-18` `data` A colour facet matches any colourway `src: Core features, matching a product when any of its colourways`
- [ ] `C-CF-19` `constraint` A feature filter excludes products that carry no features `src: Core features, A product that carries no features at all does not match`
- [ ] `C-CF-20` `data` A price band filters on the lowest live price `src: Core features, The five price bands`
- [ ] `C-CF-21` `data` A price sort uses the lowest colourway live price `src: Core features, both by a product's`
- [ ] `C-CF-22` `data` A discount sort uses the largest percentage off `src: Core features, by the largest percentage off across its colourways`
- [ ] `C-CF-23` `data` A newest sort orders by sequence `src: Core features, by sequence descending`
- [ ] `C-CF-24` `contract` A listing pages twenty four products per page `src: Core features, Listings page twenty four products at a time`
- [ ] `C-CF-25` `capability` Clearing the model widens the listing `src: Core features, Clearing the model constraint widens the listing`
- [ ] `C-CF-26` `capability` A retired model listing still resolves `src: Core features, A listing for a retired model still returns its products`
- [ ] `C-CF-27` `ui` An empty listing names the active facets with `Clear all filters` `src: Core features, A listing that matches nothing keeps its heading`
- [ ] `C-CF-28` `data` A product document carries variants in position order `src: Core features, one or more colourway variants in a fixed order`
- [ ] `C-CF-29` `literal` A product title reads `Umber Latch Clear Phone Case Cover for Arbone 16 Pro` `src: Core features, A title follows one pattern`
- [ ] `C-CF-30` `data` A build panel offers four published modules in rank order `src: Core features, Only published products appear`
- [ ] `C-CF-31` `constraint` A MagLock case is offered only the magnetic stand `src: Core features, A case whose line lacks the lock pattern`
- [ ] `C-CF-32` `data` A case without edges has an empty panel `src: Core features, the whole block including its heading is absent`
- [ ] `C-CF-33` `data` A module panel offers compatible cases symmetrically `src: Core features, on a module it offers the cases`
- [ ] `C-CF-34` `ui` Pressing `ADD` puts the module in the cart without the case `src: Core features, adds the module in its currently selected colourway`
- [ ] `C-CF-35` `constraint` An unpublished product is denied by handle `src: Core features, returns not found by handle for every caller`
- [ ] `C-CF-36` `constraint` An unpublished product is absent from search with listings `src: Core features, absent from every listing, every search result`
- [ ] `C-CF-37` `constraint` An unpublished variant is denied from the cart `src: Core features, cannot be added to a cart`
- [ ] `C-CF-38` `capability` A cart survives with the same cart token `src: Core features, it survives the session`
- [ ] `C-CF-39` `data` A cart totals two colourways at their own prices `src: Core features, Two colourways of one product at different live prices`
- [ ] `C-CF-40` `data` A cart discount is the list total minus the subtotal `src: Core features, the discount is the list total minus the subtotal`
- [ ] `C-CF-41` `constraint` A cart quantity above stock is refused unchanged `src: Core features, A quantity above the variant's stock is refused`
- [ ] `C-CF-42` `constraint` A cart quantity below one is refused `src: Core features, A quantity below one is refused`
- [ ] `C-CF-43` `data` A module without a case carries the compatibility warning `src: Core features, carries the warning`
- [ ] `C-CF-44` `constraint` An order to an unserved pincode is refused `src: Core features, The address pincode must be served`
- [ ] `C-CF-45` `data` An order is created pending then empties the cart `src: Core features, The order is created in state`
- [ ] `C-CF-46` `data` Concurrent orders for the last unit create exactly one order `src: Core features, exactly one order is created and stock ends at zero`
- [ ] `C-CF-47` `data` Contention over limited stock never goes negative `src: Core features, Stock never goes negative`
- [ ] `C-CF-48` `data` The losing order names the SKU with the cart line reduced to available stock `src: Core features, that shopper's cart line survives`
- [ ] `C-CF-49` `data` Order lines snapshot the title with the prices `src: Core features, An order line snapshots the title`
- [ ] `C-CF-50` `data` A paid order invoice in Kill Bill matches the total `src: Core features, creates exactly one invoice in Kill Bill for the order total`
- [ ] `C-CF-51` `data` The Kill Bill account is keyed by the shopper phone `src: Core features, identified by the external key`
- [ ] `C-CF-52` `data` A payment replay creates no second invoice `src: Core features, Paying an order that is already paid returns the same result`
- [ ] `C-CF-53` `capability` A paid order sends exactly one confirmation email `src: Core features, A paid order sends one email over SMTP`
- [ ] `C-CF-54` `constraint` An unpaid order sends no confirmation email `src: Core features, Creating an order that is never paid sends nothing`
- [ ] `C-CF-55` `data` The delivery check follows the served prefixes `src: Core features, A pincode is served when its first three digits`
- [ ] `C-CF-56` `capability` Search matches titles then redirects an exact model name `src: Core features, A query that exactly matches a non retired device model`
- [ ] `C-CF-57` `capability` A shopper saves then removes a wishlist item `src: Core features, A signed in shopper saves and removes products`
- [ ] `C-CF-58` `constraint` An unpublished product cannot be saved to a wishlist `src: Core features, An unpublished product cannot be saved`
- [ ] `C-CF-59` `data` The store directory lists active stores by type or place `src: Core features, The directory lists active stores only`
- [ ] `C-CF-60` `constraint` The newsletter answers repeat subscriptions identically `src: Core features, for a new address and for one already subscribed alike`
- [ ] `C-CF-61` `ui` A first time visitor is asked about cookies once `src: Core features, A first time visitor is asked once about non-essential cookies`
- [ ] `C-CF-62` `ui` A privacy page opens from the footer `src: Core features, A privacy page`
- [ ] `C-CF-63` `ui` An unknown handle renders the not found route with four exits `src: Core features, An unknown handle renders the not found route`
- [ ] `C-CF-64` `constraint` Simultaneous verifications of one code issue exactly one session `src: Core features, When several requests present the same code at the same instant`
- [ ] `C-CF-65` `constraint` A code presented with another phone is refused `src: Core features, A code is valid only for the phone it was requested for`
- [ ] `C-CF-66` `constraint` A burst of simultaneous wrong codes still locks the phone `src: Core features, Wrong codes are counted exactly however they arrive`
- [ ] `C-CF-67` `constraint` Simultaneous code requests send at most five codes `src: Core features, Simultaneous requests are counted the same way`
- [ ] `C-CF-68` `data` A refused order takes no stock from its other lines `src: Core features, A refused order takes no stock from any of its lines`
- [ ] `C-CF-69` `data` A catalogue edit after ordering leaves the order lines unchanged `src: Core features, A price or title edited in the catalogue after the order was placed`
- [ ] `C-CF-70` `data` Simultaneous payments for one order create one invoice `src: Core features, Pay requests for one order that arrive at the same instant`
- [ ] `C-CF-71` `data` A paid invoice itemises each line total plus paid delivery `src: Core features, The invoice carries one item per order line`

## C-UF User flow

- [ ] `C-UF-01` `contract` The listing route `/list/arbor/arbone-16-pro` pins one device model `src: User flow, A listing pinned to one device brand and model`
- [ ] `C-UF-02` `contract` A visitor opening `/account/orders` lands on `/login` `src: User flow, A visitor who opens a Shopper route lands on`
- [ ] `C-UF-03` `contract` A checkout with an empty cart redirects to the cart route `src: User flow, with an empty cart redirects to`
- [ ] `C-UF-04` `ui` The build panel on a Latch case reads grip, flex stand, wallet stand, lanyard `src: User flow, the rows read the grip`
- [ ] `C-UF-05` `ui` Solarion S25 Ultra shows the unavailable model caption `src: User flow, is shown with`
- [ ] `C-UF-06` `ui` Filtering by the magnetic feature leaves four cases `src: User flow, exactly four cases remain`
- [ ] `C-UF-07` `ui` The empty cart reads `YOUR SHOPPING CART IS EMPTY` `src: User flow, Open`
- [ ] `C-UF-08` `ui` A sign in button stays disabled until ten digits `src: User flow, stays disabled until the field holds ten digits`
- [ ] `C-UF-09` `ui` A waiting grid draws a skeleton at its final layout `src: User flow, draws a skeleton at its final layout`
- [ ] `C-UF-10` `ui` The help centre reads fully signed out `src: User flow, The help centre`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` One teal accent marks only affirmative actions `src: UI/UX notes, One accent carries every affirmative action and nothing else`
- [ ] `C-UX-02` `ui` Live price with struck price share one size on one baseline `src: UI/UX notes, Prices come in pairs`
- [ ] `C-UX-03` `ui` The storefront reads as restrained retail with products first `src: UI/UX notes, The register is`
- [ ] `C-UX-04` `ui` A destructive action takes neither the accent nor red `src: UI/UX notes, Destructive actions are never red`
- [ ] `C-UX-05` `ui` Hover gives a card no lift with no image zoom `src: UI/UX notes, Cards do not lift`
- [ ] `C-UX-06` `ui` Entering motion decelerates, leaving motion takes a sharp curve `src: UI/UX notes, Motion character is`
- [ ] `C-UX-07` `ui` Keyboard focus is visible on card, heart, swatch in order `src: UI/UX notes, every interactive element shows a visible focus ring`
- [ ] `C-UX-08` `ui` A phone width stacks the product route over a sticky buy bar `src: UI/UX notes, Below the cut point`
- [ ] `C-UX-09` `ui` Each route leads with one primary action `src: UI/UX notes, Each route leads with one clear primary action`
- [ ] `C-UX-10` `ui` Hero titles alone use the wide display face `src: UI/UX notes, used`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The header scrolls away without sticking `src: Front-end specification, it`
- [ ] `C-FE-02` `ui` The home category chips swap the rail without navigating `src: Front-end specification, swapping the rail beneath without navigating`
- [ ] `C-FE-03` `ui` The hero carousel active bullet fills like a timer `src: Front-end specification, its bullets double as a timer`
- [ ] `C-FE-04` `ui` A listing card swatch swaps title with price without navigating `src: Front-end specification, Selecting a swatch on a card swaps its media`
- [ ] `C-FE-05` `ui` The sort sheet offers six named options `src: Front-end specification, Sort, `
- [ ] `C-FE-06` `ui` A listing shows the model chip reading `Model:` `src: Front-end specification, the model chip`
- [ ] `C-FE-07` `ui` Active facets appear as removable chips `src: Front-end specification, Active facets become removable chips`
- [ ] `C-FE-08` `ui` The ecosystem route shows eight rails in assembly order `src: Front-end specification, Then eight rails in assembly order`
- [ ] `C-FE-09` `ui` The ecosystem route reads as an editorial story before selling `src: Front-end specification, Roughly ten screens`
- [ ] `C-FE-10` `ui` Product accordions open one at a time `src: Front-end specification, one open at a time`
- [ ] `C-FE-11` `ui` The media pane shows the badge with share plus save glyphs `src: Front-end specification, The media pane is square`
- [ ] `C-FE-12` `ui` The delivery check button is disabled until six digits `src: Front-end specification, disabled until six digits are entered`
- [ ] `C-FE-13` `ui` A checked pincode shows `Delivers in 3 to 5 days` `src: Front-end specification, replaced in place by the result`
- [ ] `C-FE-14` `ui` A cart line names colourway with device separately beside a plain `Remove` `src: Front-end specification, a quiet line naming the colourway and the device cut separately`
- [ ] `C-FE-15` `ui` The cart stepper minus is disabled at one `src: Front-end specification, The stepper's minus is disabled at one`
- [ ] `C-FE-16` `ui` The cart shows `Only 3 left` for a variant holding three units `src: Front-end specification, Filled:`
- [ ] `C-FE-17` `ui` The sign in panel shows the `+91` prefix with consent links `src: Front-end specification, locked in a prefix cell`
- [ ] `C-FE-18` `ui` The code entry reads `Enter the code we sent you` `src: Front-end specification, swaps the panel in place for`
- [ ] `C-FE-19` `ui` The store directory filters by `Airport Outlets` `src: Front-end specification, then chips`
- [ ] `C-FE-20` `ui` The search overlay shows result rows for `Cinnabar` `src: Front-end specification, Result rows appear as the query settles`
- [ ] `C-FE-21` `ui` The category route shows seven Arbor tiles `src: Front-end specification, Then a grid of circular tiles`
- [ ] `C-FE-22` `ui` A sold out card stays in place, still opening the product `src: Front-end specification, A sold out card desaturates its media`
- [ ] `C-FE-23` `ui` The device selector reads as a different control from the colour swatches `src: Front-end specification, The route owns the device`
- [ ] `C-FE-24` `ui` A standing page opens as one narrow reading column `src: Front-end specification, The standing pages are one narrow reading column`
- [ ] `C-FE-25` `ui` The account shell shows `REWARDS` reading `Coming soon` `src: Front-end specification, is inert, captioned`
- [ ] `C-FE-26` `ui` Filters open as a bottom sheet at phone width `src: Front-end specification, a bottom sheet at mobile`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Money reads as integer paise in `inr` `src: Technical requirements, Every amount the app's own API returns is integer paise`
- [ ] `C-TR-02` `data` Publication filtering happens before the listing page is taken `src: Technical requirements, Every filter, including publication, selects before the page is taken`
- [ ] `C-TR-03` `contract` A listing reports `total_count` with `has_more` plus `next_page` on every page `src: Technical requirements, A listing response carries`
- [ ] `C-TR-04` `contract` Order history refuses a `limit` outside one to fifty `src: Technical requirements, Order history takes`
- [ ] `C-TR-05` `data` The losing concurrent order receives a `409` conflict response `src: Technical requirements, rejected with a`
- [ ] `C-TR-06` `data` A payment replay returns the same invoice `src: Technical requirements, A replayed payment for an order that is already paid`
- [ ] `C-TR-07` `contract` The favicon is declared then served `src: Technical requirements, The shell declares a favicon`
- [ ] `C-TR-08` `data` Sign in codes with payments hold under simultaneous requests `src: Technical requirements, The same holds for sign in codes and payments`

## C-DM Data model

- [ ] `C-DM-01` `data` Generated basics rows match the stated rule `src: Data model, For every non retired phone model`
- [ ] `C-DM-02` `literal` Basics row `basics-clear-case-07-arbone-16-pro` reads `Cinnabar` `src: Data model, basics-clear-case-07-arbone-16-pro`
- [ ] `C-DM-03` `literal` Published products across categories total `404` `src: Data model, Counts that follow and must hold`
- [ ] `C-DM-04` `literal` The unconstrained case listing holds `399` `src: Data model, The unconstrained`
- [ ] `C-DM-05` `literal` The model case listing holds `60` across pages of 24, 24, 12 `src: Data model, holds`
- [ ] `C-DM-06` `literal` The magnetic feature filter holds `4` `src: Data model, Filtered to the`
- [ ] `C-DM-07` `data` The retired model `arbone-15` is excluded from device models `src: Data model, arbone-15`
- [ ] `C-DM-08` `data` The clear case variants read Umber then Cinnabar `src: Data model, latch-clear-phone-case-arbone-16-pro`
- [ ] `C-DM-09` `data` Compatibility edges rank grip, flex, wallet, lanyard for a Latch case `src: Data model, has six edges`
- [ ] `C-DM-10` `data` The Ochre signature variant starts with stock one `src: Data model, latch-signature-phone-case-arbone-16-pro`
- [ ] `C-DM-11` `data` The Cerise signature variant starts with stock three `src: Data model, Hand-seeded products`
- [ ] `C-DM-12` `data` The seeded store directory holds one inactive Mumbai store `src: Data model, LatticeGoods Store Colaba`
- [ ] `C-DM-13` `data` An order line is written once `src: Data model, An order line is written once and never updated`
- [ ] `C-DM-14` `data` Seeding twice duplicates no product row `src: Data model, Seeding must be idempotent`
- [ ] `C-DM-15` `literal` The second seeded shopper email is `shopper2@example.com` `src: Data model, Seeded as in User roles`
- [ ] `C-DM-16` `data` A catalogue edit shows on the next read `src: Data model, The catalogue is edited directly`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No password exists anywhere in sign in `src: Constraints, No password, no email sign in`
- [ ] `C-CN-02` `constraint` Payment is an invoice in Kill Bill rather than a card `src: Constraints, Payment is an invoice in Kill Bill`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app answers on `APP_PUBLIC_URL` `src: Deployment contract, The app must be reachable at`
- [ ] `C-DC-02` `contract` The API serves JSON under `/api` on the app origin `src: Deployment contract, The HTTP API is served on that same origin`
- [ ] `C-DC-03` `contract` The health route returns `200` once ready `src: Deployment contract, returns`
- [ ] `C-DC-04` `contract` The app starts from the image with no manual step `src: Deployment contract, The app starts from the environment image`
- [ ] `C-DC-05` `contract` The server outlives the session that started the server `src: Deployment contract, The server must keep running after this session ends`
- [ ] `C-DC-06` `contract` The listener binds all interfaces `src: Deployment contract, Bind`
- [ ] `C-DC-07` `contract` The backing services are used where the services already run `src: Deployment contract, The backing services named in this brief are already running`
- [ ] `C-DC-08` `contract` A list endpoint returns rows under `items` `src: Deployment contract, List endpoints return their rows under`
- [ ] `C-DC-09` `contract` An invalid call is refused as a client error `src: Deployment contract, an invalid or unauthorized call is rejected as a client error`
- [ ] `C-DC-10` `contract` Bearer auth guards the order history with the wishlist `src: Deployment contract, Bearer auth is required on`
- [ ] `C-DC-11` `contract` The cart works from the `cart_token` cookie without a bearer token `src: Deployment contract, The cart is identified by the`
- [ ] `C-DC-12` `contract` Code verification returns `access_token` `src: Deployment contract, POST /api/auth/verify-code`
- [ ] `C-DC-13` `contract` A stock conflict response carries the `sku` `src: Deployment contract, a stock conflict carries`
- [ ] `C-DC-14` `contract` The paid invoice lives in Kill Bill rather than an app flag `src: Deployment contract, A paid order's invoice must exist as a real invoice in Kill Bill`
- [ ] `C-DC-15` `contract` The sign in code arrives as a real email through Mailpit `src: Deployment contract, a sign in code or a confirmation must be delivered as a real email through Mailpit`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `9876500001` | the seeded shopper phone | `C-RL-06` |
| `That code did not match. Two attempts left.` | the fourth wrong code message | `C-CF-07` |
| `Umber Latch Clear Phone Case Cover for Arbone 16 Pro` | the worked product title | `C-CF-29` |
| `ADD` | the build panel action | `C-CF-34` |
| `Clear all filters` | the empty listing action | `C-CF-27` |
| `/list/arbor/arbone-16-pro` | the pinned model listing route | `C-UF-01` |
| `/account/orders` | the order history route | `C-UF-02` |
| `/login` | the sign in route | `C-UF-02` |
| `Not available for this model` | the unavailable model caption | `C-UF-05` |
| `YOUR SHOPPING CART IS EMPTY` | the empty cart heading | `C-UF-07` |
| `Model:` | the model chip label | `C-FE-06` |
| `Delivers in 3 to 5 days` | the standard delivery window | `C-FE-13` |
| `Remove` | the cart line removal action | `C-FE-14` |
| `Only 3 left` | the low stock line | `C-FE-16` |
| `+91` | the dialling prefix | `C-FE-17` |
| `Enter the code we sent you` | the code entry heading | `C-FE-18` |
| `Airport Outlets` | the airport store chip | `C-FE-19` |
| `Cinnabar` | the searched colourway | `C-FE-20` |
| `REWARDS` | the inert account entry | `C-FE-25` |
| `Coming soon` | the rewards caption | `C-FE-25` |
| `inr` | the app currency code | `C-TR-01` |
| `total_count` | the matching row count key | `C-TR-03` |
| `has_more` | the further page key | `C-TR-03` |
| `next_page` | the next page key | `C-TR-03` |
| `limit` | the order history page length | `C-TR-04` |
| `409` | the conflict response status | `C-TR-05` |
| `basics-clear-case-07-arbone-16-pro` | the worked basics row | `C-DM-02` |
| `404` | the published product count | `C-DM-03` |
| `399` | the unconstrained case count | `C-DM-04` |
| `60` | the model case count | `C-DM-05` |
| `4` | the magnetic case count | `C-DM-06` |
| `arbone-15` | the retired model | `C-DM-07` |
| `shopper2@example.com` | the second seeded shopper email | `C-DM-15` |
| `APP_PUBLIC_URL` | the public address | `C-DC-01` |
| `/api` | the API prefix | `C-DC-02` |
| `200` | the readiness response | `C-DC-03` |
| `items` | the list envelope key | `C-DC-08` |
| `cart_token` | the cart cookie | `C-DC-11` |
| `access_token` | the session token key | `C-DC-12` |
| `sku` | the conflict response key | `C-DC-13` |

### Referenced but not pinned

| Value | Item |
|---|---|
| the exact colour values, carried by family plus tone plus shade | `C-UX-01` |
| the exact radii, spacing, cut point, carried in words | `C-UX-08` |
| the exact motion durations with curves, carried by character | `C-UX-06` |

## Coverage ledger

| Section | Obligation sentences | Items |
|---|---|---|
| Overview | 1 | 2 |
| User roles | 2 | 6 |
| Core features | 20 | 71 |
| User flow | 9 | 10 |
| UI/UX notes | 5 | 10 |
| Front-end specification | 24 | 26 |
| Technical requirements | 6 | 8 |
| Data model | 14 | 16 |
| Constraints | 2 | 2 |
| Deployment contract | 14 | 15 |
