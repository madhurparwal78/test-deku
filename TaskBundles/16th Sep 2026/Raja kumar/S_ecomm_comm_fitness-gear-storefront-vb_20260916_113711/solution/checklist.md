# Checklist: deku/fitness-gear-storefront-vb

Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC
Items: 226
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` A cash on delivery order is invoiced only when the courier collects `src: Overview, invoiced only when the courier collects`
- [ ] `C-OV-02` `constraint` Stock is held once, sold once `src: Overview, stock held and sold once`
- [ ] `C-OV-03` `constraint` Totals are recomputed on the server `src: Overview, totals recomputed on the server`
- [ ] `C-OV-04` `constraint` Payment on delivery is re-checked at placement `src: Overview, payment on delivery re-checked`
- [ ] `C-OV-05` `constraint` A carrier event applies once `src: Overview, carrier events that apply once and never move an order backwards`
- [ ] `C-OV-06` `constraint` A carrier event never moves an order backwards `src: Overview, carrier events that apply once and never move an order backwards`
- [ ] `C-OV-07` `ui` Every price shows three numbers together `src: Overview, every price is a discount, shown as three numbers together`
- [ ] `C-OV-08` `capability` The department menu renders real products rather than links `src: Overview, the department menu is a shop, rendering real products rather than links`
- [ ] `C-OV-09` `ui` The promotional strip at the top is permanent furniture `src: Overview, the promotional strip at the top is permanent furniture`

## C-RL User roles

- [ ] `C-RL-01` `role` A guest reads no personal order detail from an order number `src: User roles, Cannot read or cancel any order by number alone.`
- [ ] `C-RL-02` `role` A signed in customer cannot read another customer's order `src: User roles, Cannot read, cancel or return another customer's order.`
- [ ] `C-RL-03` `role` A signed in customer cannot cancel another customer's order `src: User roles, Cannot read, cancel or return another customer's order.`
- [ ] `C-RL-04` `role` A customer session reaches no merchant route `src: User roles, Cannot reach a merchant route`
- [ ] `C-RL-05` `role` A merchant cannot type a struck through price `src: User roles, Cannot type a struck through price.`
- [ ] `C-RL-06` `role` A merchant sees no numeric confidence figure `src: User roles, Cannot see a confidence score`
- [ ] `C-RL-07` `constraint` A refused merchant call leaves the protected state unchanged `src: User roles, leaving the protected state unchanged`
- [ ] `C-RL-08` `capability` A phone becomes a customer on the first verified code `src: User roles, a phone that has never verified a code becomes a customer when its first code is verified`

## C-CF Core features

- [ ] `C-CF-01` `constraint` A prepaid order is invoiced when placed `src: Core features, A prepaid order is invoiced when it is placed.`
- [ ] `C-CF-02` `constraint` A cash on delivery order is invoiced only once delivered `src: Core features, A cash on delivery order is invoiced only when delivered, and never if it is cancelled or refused.`
- [ ] `C-CF-03` `constraint` A refused cash on delivery order raises no invoice `src: Core features, A cash on delivery order is invoiced only when delivered, and never if it is cancelled or refused.`
- [ ] `C-CF-04` `constraint` A cancelled cash on delivery order raises no invoice `src: Core features, A cash on delivery order is invoiced only when delivered, and never if it is cancelled or refused.`
- [ ] `C-CF-05` `capability` A partial advance is invoiced twice: the advance at placement, the rest at delivery `src: Core features, A partial advance is invoiced twice: the advance at placement, the rest at delivery.`
- [ ] `C-CF-06` `constraint` A repeated delivery report invoices nothing more `src: Core features, A repeated delivery report invoices nothing more.`
- [ ] `C-CF-07` `constraint` A sign in code works once `src: Core features, A code is used once, belongs to one phone, and for a known phone goes only to the email on file`
- [ ] `C-CF-08` `constraint` A sign in code belongs to one phone `src: Core features, A code is used once, belongs to one phone, and for a known phone goes only to the email on file`
- [ ] `C-CF-09` `constraint` A code for a known phone goes only to the email on file `src: Core features, A code is used once, belongs to one phone, and for a known phone goes only to the email on file`
- [ ] `C-CF-10` `constraint` A cash on delivery order needs the phone verified by code before acceptance `src: Core features, A cash on delivery order needs the phone verified by code before it is accepted, or gets 422.`
- [ ] `C-CF-11` `capability` Checkout completes with no account `src: Core features, Checkout needs no account.`
- [ ] `C-CF-12` `constraint` A stale total stops the order, naming what changed `src: Core features, A stale total or a changed price stops the order with 409 and names what changed`
- [ ] `C-CF-13` `constraint` Two customers racing for the last unit never both get the unit `src: Core features, two customers racing for the last unit never both get it`
- [ ] `C-CF-14` `constraint` Stock in a bag counts as unavailable `src: Core features, Stock in a bag is held and counted as unavailable`
- [ ] `C-CF-15` `constraint` Cash on delivery is re-checked at placement by postal code `src: Core features, Cash on delivery is re-checked at placement by postal code, cart value, product and delivery confidence`
- [ ] `C-CF-16` `constraint` Cash on delivery is re-checked at placement by cart value `src: Core features, Cash on delivery is re-checked at placement by postal code, cart value, product and delivery confidence`
- [ ] `C-CF-17` `constraint` Cash on delivery is re-checked at placement by delivery confidence `src: Core features, Cash on delivery is re-checked at placement by postal code, cart value, product and delivery confidence`
- [ ] `C-CF-18` `capability` Prepaid stays offered whenever cash on delivery is refused `src: Core features, prepaid is always offered`
- [ ] `C-CF-19` `constraint` One idempotency key makes one order `src: Core features, Placing the same order twice with one idempotency key makes one order.`
- [ ] `C-CF-20` `constraint` Refused stays a state apart from returned to origin `src: Core features, refused and returned to origin are separate states, and stock returns exactly once`
- [ ] `C-CF-21` `capability` A customer may cancel until the order is packed `src: Core features, A customer may cancel until the order is packed, then gets 409, and never cancels someone else's order.`
- [ ] `C-CF-22` `constraint` Cancellation after packing is refused `src: Core features, A customer may cancel until the order is packed, then gets 409, and never cancels someone else's order.`
- [ ] `C-CF-23` `constraint` Tracking by number plus four digits shows the timeline only `src: Core features, Tracking by order number and the phone's last four digits shows the timeline and nothing else`
- [ ] `C-CF-24` `constraint` Tracking stops answering after repeated wrong guesses `src: Core features, answers 429 after repeated wrong guesses`
- [ ] `C-CF-25` `constraint` A return refunds what the line actually paid `src: Core features, A return refunds what the line actually paid, within seven days of delivery; later requests get 422.`
- [ ] `C-CF-26` `constraint` A return later than seven days after delivery is refused `src: Core features, A return refunds what the line actually paid, within seven days of delivery; later requests get 422.`
- [ ] `C-CF-27` `constraint` A struck through price comes from recorded price history `src: Core features, A struck through price is a price the product was really sold at, taken from its recorded price history`
- [ ] `C-CF-28` `constraint` A low stock badge counts units held in bags `src: Core features, a low stock badge counts units held in bags`
- [ ] `C-CF-29` `constraint` Only a customer with a delivered order of a product may review the product `src: Core features, Only a customer whose order of a product was delivered may review it; anyone else gets 403.`
- [ ] `C-CF-30` `capability` An unknown address renders Peakfit's own not-found page `src: Core features, An unknown address renders Peakfit's own not-found page, with a search field and the best sellers, answering 404.`
- [ ] `C-CF-31` `capability` A privacy page is linked from every page's footer `src: Core features, A privacy page, linked from every page's footer, states what Peakfit records about a customer and how long it keeps it.`

## C-UF User flow

- [ ] `C-UF-01` `capability` Every storefront route serves a stranger `src: User flow, Every storefront route is public.`
- [ ] `C-UF-02` `constraint` A merchant route refuses a session without the merchant role `src: User flow, A merchant route without a merchant session renders the not-found page.`
- [ ] `C-UF-03` `ui` The bag slides over from the right `src: User flow, the bag slides over from the right showing the line and how far the bag is from the next offer`
- [ ] `C-UF-04` `capability` The bag lists the line with a meter naming how far the bag is from the next offer `src: User flow, the bag slides over from the right showing the line and how far the bag is from the next offer`
- [ ] `C-UF-05` `capability` A guest reads the timeline from the order number plus the phone's last four digits `src: User flow, enters the order number and the phone's last four digits, and reads the timeline`
- [ ] `C-UF-06` `capability` A signed in customer returns one line of a delivered order `src: User flow, A signed in customer returns one line of a delivered order with a reason from the list.`
- [ ] `C-UF-07` `ui` Loading on every screen is a skeleton `src: User flow, Every screen has loading as a skeleton`
- [ ] `C-UF-08` `capability` A guest checkout lands on a full page confirmation `src: User flow, lands on a full page confirmation stating the amount due to the courier`
- [ ] `C-UF-09` `capability` Opening /account without a session shows sign in by phone `src: User flow, /account without a session shows sign in by phone`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Headings are heavy tracked capitals over lowercase Inter product names `src: UI/UX notes, Headings are very heavy, tightly tracked capitals in the display family; product names beneath them are lowercase Inter`
- [ ] `C-UX-02` `ui` The amber accent sits behind display type, never on a button `src: UI/UX notes, One signature light, vivid amber, the brand yellow, sits behind a word of display type and inside promotional emphasis, never on a button.`
- [ ] `C-UX-03` `ui` Prices use near-black, a warm neutral struck original, a green saving `src: UI/UX notes, Prices speak in near-black neutral, a mid warm neutral for the struck original, and a mid, vivid green for the saving.`
- [ ] `C-UX-04` `ui` Slides, drawers, panels ride a house curve leaving fast, settling long `src: UI/UX notes, a house curve leaving fast and settling long for slides, drawers and panels`
- [ ] `C-UX-05` `ui` Labels sit above fields with errors below `src: UI/UX notes, labels sit above fields and errors below`
- [ ] `C-UX-06` `ui` A transient message confirms an outcome then dismisses itself `src: UI/UX notes, a transient message confirms an outcome then dismisses itself`
- [ ] `C-UX-07` `capability` The bag drawer closes on Escape `src: UI/UX notes, drawers and sheets close on Escape`
- [ ] `C-UX-08` `capability` Icon-only controls carry accessible names `src: UI/UX notes, icon-only controls are labelled`
- [ ] `C-UX-09` `ui` The primary action is near-black, lightening on hover `src: UI/UX notes, The primary action is near-black, lightening on hover`
- [ ] `C-UX-10` `capability` Removing a bag line asks first `src: UI/UX notes, removing a bag line asks first`
- [ ] `C-UX-11` `ui` State pairs its colour with a word `src: UI/UX notes, state is never carried by colour alone`
- [ ] `C-UX-12` `ui` Reduced motion steps the marquee, stills the carousel `src: UI/UX notes, Under a reduced motion preference the marquee steps instead of scrolling, the carousel does not advance, and drawers open without travel.`
- [ ] `C-UX-13` `ui` Every control shows a visible focus ring from the keyboard `src: UI/UX notes, keyboard navigation reaches every control with a visible focus ring`
- [ ] `C-UX-14` `constraint` Every content image carries alternative text `src: UI/UX notes, Every content image carries alternative text, and decorative images declare themselves decorative.`
- [ ] `C-UX-15` `ui` Cards run two columns on a phone, three on a tablet, four on a desktop `src: UI/UX notes, two columns of cards on a phone, three on a tablet, four on a desktop, with a sticky action bar on a phone product page`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The marquee translates with no seam, pausing on hover `src: Front-end specification, translating continuously with no seam, because its content is drawn twice. It pauses on hover.`
- [ ] `C-FE-02` `ui` The header turns solid once the hero scrolls past `src: Front-end specification, a translucent dark ground with a blur behind it, becoming the solid near-black neutral once the hero has scrolled past`
- [ ] `C-FE-03` `ui` The header sets department tabs left, the wordmark centre, the rounded search field right `src: Front-end specification, Left, the four department tabs EQUIPMENTS, SPORTS SHOES, SNEAKERS, APPAREL; centre, the wordmark; right, a fully rounded search field with the placeholder Search For Apparels`
- [ ] `C-FE-04` `capability` The department menu shows real products with live prices `src: Front-end specification, The menu renders real products with live prices and stock, not a static list.`
- [ ] `C-FE-05` `ui` The filter bar stays sticky under the header `src: Front-end specification, sticky under the header, holding the filter control, the sort select and the active filter chips`
- [ ] `C-FE-06` `ui` The cart drawer slides over from the right over a scrim `src: Front-end specification, Opens from the bag glyph, sliding over from the right, full height, over a scrim.`
- [ ] `C-FE-07` `ui` The carousel stops for good once a visitor uses a control `src: Front-end specification, The carousel stops permanently once a visitor uses a control`
- [ ] `C-FE-08` `ui` The promotional countdown survives a reload `src: Front-end specification, The countdown reflects a real promotion expiry, the same for every visitor, and it survives a reload.`
- [ ] `C-FE-09` `ui` A product card never reflows as badges or ratings appear `src: Front-end specification, The card never reflows when its badges or rating appear`
- [ ] `C-FE-10` `constraint` An out of stock product stays listed `src: Front-end specification, An out of stock product stays listed, greyed, with Notify me replacing the action`
- [ ] `C-FE-11` `ui` Shelves bounce a hint of sideways scrolling `src: Front-end specification, a small vertical bounce that tells a shopper a shelf scrolls sideways`
- [ ] `C-FE-12` `ui` The delivery check is a first class element of the buy column `src: Front-end specification, It is a first class element of the buy column, not a link to a policy page.`
- [ ] `C-FE-13` `ui` The kit builder shows one card per slot with a swap control `src: Front-end specification, One card per slot with its role, the chosen product, its price, a swap control offering the other candidates`
- [ ] `C-FE-14` `literal` The not-found page reads That page does not exist. `src: Front-end specification, That page does not exist.`
- [ ] `C-FE-15` `literal` The delivery check answers 110001 as a postal code that is prepaid only `src: Front-end specification, This postal code is prepaid only.`
- [ ] `C-FE-16` `literal` The delivery check reads Delivering to 560001 by a date, Cash on delivery available here `src: Front-end specification, Delivering to 560001 by Thursday, 12 March in that shape, then Cash on delivery available here`
- [ ] `C-FE-17` `capability` Unavailable sizes show struck through, disabled with a reason `src: Front-end specification, showing unavailable combinations as struck through rather than hidden, disabled with a reason`
- [ ] `C-FE-18` `literal` The quantity stepper stops at the per-order limit of 5 `src: Front-end specification, a stepper from 1 to the per-order limit of 5`
- [ ] `C-FE-19` `literal` The meter reads Add <amount> more for a free gift `src: Front-end specification, Add 320 more for a free gift`
- [ ] `C-FE-20` `literal` Zero search results read Nothing matched "<query>" with best sellers `src: Front-end specification, Zero results read Nothing matched "<query>"`
- [ ] `C-FE-21` `literal` The code resend control reads Not received? Resend in 30s `src: Front-end specification, Not received? Resend in 30s`
- [ ] `C-FE-22` `literal` The skip link reads Skip to content `src: Front-end specification, Skip to content`
- [ ] `C-FE-23` `capability` The returns page states the window, exclusions, return shipping, refund time in that order `src: Front-end specification, the seven day window, what is excluded, who pays return shipping, and how long a refund takes`
- [ ] `C-FE-24` `capability` Filter state lives in the address, surviving a reload `src: Front-end specification, Filter state lives in the address, so a filtered view is shareable and survives a reload`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Every public route's HTML carries its own social preview tags `src: Technical requirements, every public route's HTML is served with its own title, description and social preview tags already in it`
- [ ] `C-TR-02` `contract` The Kill Bill account key is peakfit- followed by the phone `src: Technical requirements, A customer's account has the external key peakfit- followed by the ten digit phone, the currency INR and the country IN.`
- [ ] `C-TR-03` `literal` Each invoice item description begins Order followed by the order number `src: Technical requirements, Every invoice this storefront creates carries exactly one item whose description begins Order followed by the order number`
- [ ] `C-TR-04` `constraint` A replayed placement never produces a second invoice `src: Technical requirements, A placement replayed, a delivered event reported twice, or two requests arriving together never produce a second invoice for the same payment.`
- [ ] `C-TR-05` `constraint` Simultaneous placements never produce a second invoice `src: Technical requirements, A placement replayed, a delivered event reported twice, or two requests arriving together never produce a second invoice for the same payment.`
- [ ] `C-TR-06` `contract` The hold length comes from CART_HOLD_SECONDS `src: Technical requirements, its length in seconds is read from CART_HOLD_SECONDS, which this environment sets to 45`
- [ ] `C-TR-07` `literal` The code email is Your Peakfit code with the six digits alone first `src: Technical requirements, Your Peakfit code | the six digits alone`
- [ ] `C-TR-08` `literal` The cash on delivery placed email opens Order <number> placed. Have <amount> ready for the courier. `src: Technical requirements, Order <number> placed. Have <amount> ready for the courier.`
- [ ] `C-TR-09` `constraint` An amount shows paise only when not zero `src: Technical requirements, paise only when they are not zero`
- [ ] `C-TR-10` `literal` The out for delivery email names the window with the amount due `src: Technical requirements, Your order arrives today between <window>. Amount due: <amount>.`
- [ ] `C-TR-11` `capability` A medium band order is asked to confirm by email `src: Technical requirements, Please confirm Peakfit order <number>`
- [ ] `C-TR-12` `constraint` The confirmation message stays under 160 characters `src: Technical requirements, The confirmation message stays under 160 characters`
- [ ] `C-TR-13` `contract` A second code request inside thirty seconds answers resend_too_soon `src: Technical requirements, A second code request for the same phone inside thirty seconds of the last is refused with 429 and resend_too_soon`
- [ ] `C-TR-14` `contract` The refusal carries retry_after_seconds from 1 to 30 `src: Technical requirements, the error object carrying retry_after_seconds as a whole number from 1 to 30`
- [ ] `C-TR-15` `constraint` Another phone's code is refused with invalid_code `src: Technical requirements, A wrong, expired, used or other phone's code is refused with 401 and invalid_code.`
- [ ] `C-TR-16` `constraint` available is on_hand less the units held in live bags `src: Technical requirements, A variant's available is on_hand less the units held in live bags`
- [ ] `C-TR-17` `constraint` An ended hold frees its units exactly once `src: Technical requirements, From that instant the units are available again, exactly once`
- [ ] `C-TR-18` `constraint` A bag whose hold ended never buys a unit another live bag holds `src: Technical requirements, never a unit another live bag now holds`
- [ ] `C-TR-19` `constraint` After a recount placements take stock in placement order `src: Technical requirements, placements then take stock in the order they are placed, and the rest are refused`
- [ ] `C-TR-20` `contract` Holding more than is available answers insufficient_stock `src: Technical requirements, A request to hold more than is available is refused with 409 and insufficient_stock, carrying available.`
- [ ] `C-TR-21` `constraint` Two placements needing more than on_hand leave exactly one winner `src: Technical requirements, when two placements would together need more than on_hand, exactly one succeeds`
- [ ] `C-TR-22` `constraint` LOW STOCK reads available at or below the low threshold `src: Technical requirements, A variant carries LOW STOCK when it is not backorderable and available is above zero and at or below its low_threshold`
- [ ] `C-TR-23` `constraint` SOLD OUT shows at zero available `src: Technical requirements, SOLD OUT when available is zero and it is not backorderable`
- [ ] `C-TR-24` `constraint` compare_at_minor is derived from price history, never typed `src: Technical requirements, compare_at_minor is derived from that history, never typed`
- [ ] `C-TR-25` `constraint` The compare price is the highest price of the last ninety days `src: Technical requirements, the highest price the variant carried at any moment in the ninety days before now`
- [ ] `C-TR-26` `contract` A typed compare price answers compare_at_not_settable `src: Technical requirements, A merchant request carrying compare_at_minor is refused with 422 and compare_at_not_settable and changes nothing.`
- [ ] `C-TR-27` `constraint` saving_percent rounds down to a whole number `src: Technical requirements, rounded down to a whole number`
- [ ] `C-TR-28` `constraint` Bags merge on claim by summing quantities `src: Technical requirements, the two merge on claim by summing quantities, never by replacing`
- [ ] `C-TR-29` `contract` A line whose price changed carries price_changed `src: Technical requirements, When the two differ the line carries price_changed`
- [ ] `C-TR-30` `constraint` Thresholds read the merchandise subtotal alone `src: Technical requirements, Thresholds are measured against that subtotal and nothing else`
- [ ] `C-TR-31` `constraint` The two threshold discounts never stack `src: Technical requirements, The two threshold discounts never stack: only the highest reached applies.`
- [ ] `C-TR-32` `constraint` A code applies to its eligible lines only `src: Technical requirements, A code applies to its eligible lines and stacks with the threshold discount`
- [ ] `C-TR-33` `constraint` remaining_minor counts from the subtotal `src: Technical requirements, for the lowest threshold above the subtotal, how far away it is as remaining_minor`
- [ ] `C-TR-34` `contract` A code applying to no line answers not_applicable `src: Technical requirements, A code that applies to no line of the bag is refused with 422 and not_applicable.`
- [ ] `C-TR-35` `constraint` A subtotal of 199900 adds the shaker bottle at no charge `src: Technical requirements, a merchandise subtotal of 199900 or more adds one PF-GIFT-SHAKER at no charge`
- [ ] `C-TR-36` `constraint` Leftover paise go to the largest fractions, ties to the earlier line `src: Technical requirements, the paise left over go one at a time to the lines with the largest fraction discarded, ties to the earlier line`
- [ ] `C-TR-37` `constraint` paid_minor is the line total less the allocated discount `src: Technical requirements, its paid_minor is its line total less that`
- [ ] `C-TR-38` `contract` The delivery check accounts for the product `src: Technical requirements, cod_available also accounts for the variant's product`
- [ ] `C-TR-39` `constraint` Payment on delivery holds only up to a total of 999900 `src: Technical requirements, the order total is at most 999900`
- [ ] `C-TR-40` `constraint` A product marked not eligible blocks payment on delivery `src: Technical requirements, no line's product is marked not eligible`
- [ ] `C-TR-41` `contract` A cash on delivery refusal names its reason `src: Technical requirements, placement answers 422 with cod_unavailable and a reason of postal_code, cart_value, product or delivery_confidence`
- [ ] `C-TR-42` `constraint` A signed in customer on the account's own phone needs no code `src: Technical requirements, unless the order comes from a signed in customer placing it with their own verified phone`
- [ ] `C-TR-43` `constraint` The advance is twenty per cent rounded up to the rupee `src: Technical requirements, an advance of twenty per cent of the total, rounded up to the whole rupee, is paid at placement`
- [ ] `C-TR-44` `constraint` The client's total is never trusted `src: Technical requirements, The client's total is never trusted.`
- [ ] `C-TR-45` `contract` A price refusal carries the changes `src: Technical requirements, placement answers 409 with price_changed, carrying changes as`
- [ ] `C-TR-46` `constraint` Placing again with the new total succeeds `src: Technical requirements, each line's price at add becomes its current price, so placing again with the new total succeeds`
- [ ] `C-TR-47` `constraint` A stock refusal creates nothing, taking no stock `src: Technical requirements, creates nothing and takes no stock`
- [ ] `C-TR-48` `constraint` A replay with the same body returns the same order `src: Technical requirements, The same Idempotency-Key with the same body returns the same order with 200 and creates nothing more`
- [ ] `C-TR-49` `constraint` Two identical placements at one moment make one order `src: Technical requirements, Two such requests arriving at the same moment make exactly one order.`
- [ ] `C-TR-50` `contract` A key reused with another body answers idempotency_key_reused `src: Technical requirements, The same key with a different body is refused with 409 and idempotency_key_reused.`
- [ ] `C-TR-51` `contract` An ordered bag answers cart_closed `src: Technical requirements, placing it again under a new key is refused with 409 and cart_closed`
- [ ] `C-TR-52` `contract` A missing code answers verification_required `src: Technical requirements, A missing code for payment on delivery is refused with 422 and verification_required`
- [ ] `C-TR-53` `constraint` The order's address is a copy, never a reference `src: Technical requirements, The order's address is a copy, never a reference.`
- [ ] `C-TR-54` `ui` Checkout is one page of three steps `src: Technical requirements, One page, three steps, no account required`
- [ ] `C-TR-55` `constraint` Two refused or undelivered orders block payment on delivery `src: Technical requirements, two or more of those orders reached refused or undelivered`
- [ ] `C-TR-56` `constraint` Exactly one refusal puts an order in the low band `src: Technical requirements, exactly one reached refused or undelivered`
- [ ] `C-TR-57` `constraint` Two delivered orders in an ordinary postal code are high `src: Technical requirements, two or more reached delivered, and the postal code's refusal history is ordinary`
- [ ] `C-TR-58` `constraint` Postal refusal history alone never lowers a band below medium `src: Technical requirements, Postal refusal history alone never makes a band lower than medium`
- [ ] `C-TR-59` `constraint` No numeric confidence figure exists in any response `src: Technical requirements, No numeric score exists in any response.`
- [ ] `C-TR-60` `constraint` A customer never sees a band `src: Technical requirements, A customer never sees a band or a signal.`
- [ ] `C-TR-61` `contract` Packing a low band order first answers confirmation_required `src: Technical requirements, packed is refused with 409 and confirmation_required`
- [ ] `C-TR-62` `capability` The merchant works a confirmation queue `src: Technical requirements, The merchant surface is the confirmation queue`
- [ ] `C-TR-63` `constraint` A carrier event with a bad or stale signature changes nothing `src: Technical requirements, An event with a missing or wrong signature, or a t more than three hundred seconds from now, is refused with 401 and changes nothing.`
- [ ] `C-TR-64` `constraint` An event applies at most once by its event_id `src: Technical requirements, An event is applied at most once, by its event_id`
- [ ] `C-TR-65` `capability` A new out for delivery event records a further attempt `src: Technical requirements, a new out_for_delivery event on an order already out for delivery is a further attempt`
- [ ] `C-TR-66` `constraint` A state never moves backwards `src: Technical requirements, A state never moves backwards.`
- [ ] `C-TR-67` `contract` A skip ahead answers illegal_transition `src: Technical requirements, An event that skips ahead to a status the current state cannot reach answers 409 and illegal_transition.`
- [ ] `C-TR-68` `constraint` returned_to_origin restores on_hand exactly once `src: Technical requirements, returned_to_origin puts the order's units back into on_hand, exactly once`
- [ ] `C-TR-69` `constraint` delivered_at is the event's occurred_at `src: Technical requirements, delivered sets delivered_at to the event's occurred_at`
- [ ] `C-TR-70` `contract` Cancelling from packed onward answers already_packed `src: Technical requirements, From packed onward the same request is refused with 409 and already_packed`
- [ ] `C-TR-71` `constraint` A cancellation returns the units to on_hand `src: Technical requirements, its units return to on_hand`
- [ ] `C-TR-72` `constraint` Tracking answers number, state, timeline, nothing else `src: Technical requirements, answers {"number", "state", "timeline"} and nothing else`
- [ ] `C-TR-73` `constraint` Wrong digits answer exactly as an unknown order number `src: Technical requirements, A wrong pair of digits answers exactly as an unknown order number does`
- [ ] `C-TR-74` `contract` After five wrong attempts every attempt answers too_many_attempts `src: Technical requirements, every attempt on that number, right or wrong, answers 429 with too_many_attempts`
- [ ] `C-TR-75` `contract` An unlisted return reason answers invalid_reason `src: Technical requirements, anything else is refused with 422 and invalid_reason`
- [ ] `C-TR-76` `contract` A return before delivery answers not_delivered `src: Technical requirements, An order not yet delivered is refused with 422 and not_delivered`
- [ ] `C-TR-77` `contract` A line already returned answers already_returned `src: Technical requirements, a line already in a return with 409 and already_returned`
- [ ] `C-TR-78` `constraint` Each returned line refunds its own paid_minor `src: Technical requirements, Each returned line refunds its own paid_minor, never its list price`
- [ ] `C-TR-79` `contract` A cash on delivery return refunds to store credit `src: Technical requirements, refund_method of original for prepaid orders and store_credit for payment on delivery and partial advance orders`
- [ ] `C-TR-80` `contract` A prepaid return refunds to the original method `src: Technical requirements, refund_method of original for prepaid orders and store_credit for payment on delivery and partial advance orders`
- [ ] `C-TR-81` `contract` A review without a delivered order answers not_eligible `src: Technical requirements, anyone else is refused with 403 and not_eligible`
- [ ] `C-TR-82` `contract` A second review answers already_reviewed `src: Technical requirements, A second review of one product by one customer is refused with 409 and already_reviewed.`
- [ ] `C-TR-83` `constraint` Ratings count published reviews only `src: Technical requirements, count published reviews only`
- [ ] `C-TR-84` `contract` A customer session on a merchant route answers forbidden `src: Technical requirements, a customer session is refused with 403 and forbidden and changes nothing`
- [ ] `C-TR-85` `constraint` Filters apply before paging `src: Technical requirements, Filters apply before paging, so every page carries only matching products and count is the number of matching products.`
- [ ] `C-TR-86` `constraint` Price sorts order by price_minor, then handle `src: Technical requirements, the price sorts order by price_minor and then by handle`
- [ ] `C-TR-87` `constraint` Out of stock products stay listed unless in stock only is asked for `src: Technical requirements, Out of stock products stay listed with in_stock false unless in_stock=true is asked for.`
- [ ] `C-TR-88` `contract` Claiming a bag merges the bag into the account's bag `src: Technical requirements, the account's bag, with this bag merged into it`
- [ ] `C-TR-89` `contract` Every refusal answers the error object `src: Technical requirements, Every refusal answers {"error": {"code", "message", "field"}}`
- [ ] `C-TR-90` `constraint` The not-found page is never a redirect to home `src: Technical requirements, It is never a redirect to the home page.`
- [ ] `C-TR-91` `constraint` No two public routes share a preview title `src: Technical requirements, no two routes share a title, and the preview image is served from the app's own origin and resolves`
- [ ] `C-TR-92` `constraint` No credential reaches anything the browser receives `src: Technical requirements, No secret key, database address, Kill Bill credential, mail credential or carrier secret appears in any script, style or document the browser receives.`
- [ ] `C-TR-93` `constraint` The privacy page states what Peakfit records `src: Technical requirements, states what Peakfit records about a customer`
- [ ] `C-TR-94` `constraint` tax_minor is the eighteen per cent already inside the total, rounded half up `src: Technical requirements, tax_minor is the tax already inside the total at eighteen per cent: total_minor * 18 / 118 rounded half up`
- [ ] `C-TR-95` `constraint` Shipping is 9900 below a merchandise subtotal of 99900 `src: Technical requirements, Shipping is free when the merchandise subtotal is 99900 or more and 9900 otherwise.`
- [ ] `C-TR-96` `contract` A merchant cancellation without a reason answers reason_required `src: Technical requirements, A merchant cancellation needs a reason, refused with 422 and reason_required without one.`
- [ ] `C-TR-97` `contract` Every response carries an X-Request-Id header `src: Technical requirements, every response carries an X-Request-Id header`
- [ ] `C-TR-98` `constraint` Five wrong codes void the phone's current code `src: Technical requirements, Five wrong codes for a phone void its current code.`
- [ ] `C-TR-99` `capability` Verifying a phone claims the guest orders placed with the phone `src: Technical requirements, Verifying a phone that placed guest orders claims those orders`
- [ ] `C-TR-100` `contract` An exchange on equipment answers exchange_not_offered `src: Technical requirements, Equipment offers no exchange and exchange_sku there is refused with 422 and exchange_not_offered.`
- [ ] `C-TR-101` `constraint` Every price block announces itself as one sentence `src: Technical requirements, Every price block announces itself as one sentence`
- [ ] `C-TR-102` `ui` Focus is a clear ring in the link blue `src: Technical requirements, Focus is a clear ring in the link blue, offset from the control.`
- [ ] `C-TR-103` `ui` A phone header hides departments behind a menu control `src: Technical requirements, departments behind a menu control, search as a glyph opening a sheet`

## C-DM Data model

- [ ] `C-DM-01` `data` Money is integer paise in INR `src: Data model, Money is integer paise with the currency INR, never a decimal.`
- [ ] `C-DM-02` `data` An order stores the address copied at placement `src: Data model, the contact and the address copied as they were at placement`
- [ ] `C-DM-03` `data` A carrier event_id is unique `src: Data model, carrier event_id unique`
- [ ] `C-DM-04` `data` compare_at_minor is derived, never stored `src: Data model, available, compare_at_minor, saving_percent and badges are derived, never stored`
- [ ] `C-DM-05` `data` A refund never exceeds what the covered lines paid `src: Data model, a refund never exceeds what was paid for the lines it covers, including apportioned discounts`
- [ ] `C-DM-06` `data` order_confidence has no column for a numeric confidence figure `src: Data model, No score column.`
- [ ] `C-DM-07` `data` A review exists only against a delivered order line `src: Data model, Exists only against a delivered order line.`
- [ ] `C-DM-08` `data` A hold returns its stock exactly once `src: Data model, A hold returns its stock exactly once.`
- [ ] `C-DM-09` `literal` The merchant is 9000000001, merchant@example.com, Mira Kapoor `src: Data model, 9000000001 | merchant@example.com | Mira Kapoor | merchant`
- [ ] `C-DM-10` `literal` Arjun Mehta holds PF-100001 plus PF-100002, both delivered to 560001 `src: Data model, orders PF-100001 and PF-100002, both delivered to 560001`
- [ ] `C-DM-11` `literal` Kavya Iyer holds PF-100003, refused in 560001 `src: Data model, order PF-100003, refused, in 560001`
- [ ] `C-DM-12` `literal` Rohan Das holds PF-100004 refused, PF-100005 undelivered `src: Data model, order PF-100004 refused and order PF-100005 undelivered, both in 560001`
- [ ] `C-DM-13` `literal` Neha Joshi is 9000000014 with customer4@example.com `src: Data model, 9000000014 | customer4@example.com`
- [ ] `C-DM-14` `literal` Vikram Rao is 9000000015 with customer5@example.com `src: Data model, 9000000015 | customer5@example.com | Vikram Rao`
- [ ] `C-DM-15` `literal` The massage gun is kinetra-compact-mini-massage-gun `src: Data model, kinetra-compact-mini-massage-gun | kinetra compact mini massage gun`
- [ ] `C-DM-16` `data` The massage gun's compare price is 349900, not 399900 `src: Data model, which is why its compare price is 349900 and not 399900`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No password exists; identity is a verified phone `src: Constraints, No password, no email-only sign in; identity is a verified phone.`
- [ ] `C-CN-02` `constraint` No typed compare price `src: Constraints, No per-visitor countdown, no randomised scarcity, no typed compare price.`
- [ ] `C-CN-03` `constraint` No confidence figure is shown to anyone `src: Constraints, No confidence score shown to anyone.`
- [ ] `C-CN-04` `constraint` Invoices live in Kill Bill `src: Constraints, prepaid is recorded as paid, invoices live in Kill Bill`
- [ ] `C-CN-05` `constraint` Messages travel as email through Mailpit `src: Constraints, messages travel as email through Mailpit`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app answers at APP_PUBLIC_URL `src: Deployment contract, The app must be reachable at APP_PUBLIC_URL.`
- [ ] `C-DC-02` `contract` The API is served under /api on the app origin `src: Deployment contract, The HTTP API is served on that same origin under the /api prefix.`
- [ ] `C-DC-03` `contract` The listener binds 0.0.0.0 `src: Deployment contract, Bind 0.0.0.0, never 127.0.0.1 or localhost.`
- [ ] `C-DC-04` `contract` The server outlives the session that started the server `src: Deployment contract, The server must keep running after this session ends`
- [ ] `C-DC-05` `contract` An invoice exists as a real invoice in Kill Bill `src: Deployment contract, An invoice must exist as a real invoice in Kill Bill`
- [ ] `C-DC-06` `contract` A code arrives as a real email through Mailpit `src: Deployment contract, A code or an order message must be delivered as a real email through Mailpit.`

## Pinned literals

- `4173` the container-internal port
- `45` the bag hold in seconds this environment sets
- `999900` the payment on delivery cap in paise
- `peakfit-` the Kill Bill external key prefix before the phone
- `9000000001` the seeded merchant phone

### Referenced but not pinned

- the exact colour values, carried in words by role
- the exact motion curves and durations, carried as characters

## Coverage ledger

- sections carried: 10
- obligations recorded: 226
